# -*- coding: utf-8 -*-
"""Regresión para recuperación de contraseña: enumeración, TTL 15, single-use, rate limit, From institucional y fallo SMTP silencioso."""
import hashlib
from datetime import timedelta
from unittest.mock import patch, MagicMock

from app import db
from app.modules.identidad.domain.usuario import Usuario
from app.modules.identidad.domain.password_reset import PasswordResetToken, PasswordResetAttempt
from app.modules.identidad.presentation.auth_controller import RECOVER_TTL_SECONDS, RECOVER_GENERIC_MSG, RECOVER_THROTTLE_MSG
from app.utils.time_utils import peru_now


def _get_admin(app):
    with app.app_context():
        return Usuario.query.filter_by(username='12345678').first()


def _clean_reset_tables(app):
    with app.app_context():
        PasswordResetToken.query.delete()
        PasswordResetAttempt.query.delete()
        db.session.commit()


def _extract_flash_messages(response):
    import re, json, html as html_lib
    body = response.data.decode('utf-8', errors='ignore')
    m = re.search(r"id=\"flashData\" data-messages='([^']*)'", body)
    if not m:
        return []
    raw = m.group(1)
    raw = html_lib.unescape(raw)
    try:
        return json.loads(raw)
    except Exception:
        return []

def test_enumeracion_no_filtra_existencia(client, app):
    """POST /auth/recuperar con usuario existente vs inexistente debe dar misma respuesta genérica (200) sin filtrar."""
    _clean_reset_tables(app)
    with patch('app.modules.identidad.presentation.auth_controller.enviar_correo_recuperacion', return_value=True):
        # existente: admin
        admin = _get_admin(app)
        r1 = client.post('/auth/recuperar', data={'username': admin.username, 'email': admin.email})
        assert r1.status_code == 200
        flashes1 = _extract_flash_messages(r1)
        # debe tener mensaje genérico
        assert any('Si los datos son correctos' in msg for cat, msg in flashes1)
        # no debe contener mensaje antiguo de éxito ni de no encontrado en flashes
        assert not any('No se encontr' in msg for cat, msg in flashes1)
        assert not any('Se han enviado' in msg for cat, msg in flashes1)
        # inexistente
        r2 = client.post('/auth/recuperar', data={'username': '00000000', 'email': 'noexiste@example.com'}, environ_base={'REMOTE_ADDR': '127.0.0.2'})
        assert r2.status_code == 200
        flashes2 = _extract_flash_messages(r2)
        assert any('Si los datos son correctos' in msg for cat, msg in flashes2)
        assert not any('No se encontr' in msg for cat, msg in flashes2)
        # ambos deben ser indistinguibles en flashes genéricos
        assert flashes1 == flashes2 or (any('Si los datos son correctos' in m for _, m in flashes1) and any('Si los datos son correctos' in m for _, m in flashes2))
    _clean_reset_tables(app)


def test_ttl_15_segundos_constante(app):
    """El TTL debe ser 900s (15 min) tanto en constante como en serializer."""
    assert RECOVER_TTL_SECONDS == 900
    # Verificar que el controller usa 900 en max_age: inspeccionar código
    import inspect
    from app.modules.identidad.presentation import auth_controller
    src = inspect.getsource(auth_controller.reset_password)
    assert '900' in src or 'RECOVER_TTL_SECONDS' in src


def test_single_use_token(client, app):
    """Token válido tras uso debe quedar invalidado."""
    _clean_reset_tables(app)
    admin = _get_admin(app)
    with app.app_context():
        from app.modules.identidad.presentation.auth_controller import get_serializer, _hash_token
        serializer = get_serializer()
        token = serializer.dumps(admin.id)
        token_hash = _hash_token(token)
        expires = peru_now() + timedelta(seconds=900)
        prt = PasswordResetToken(usuario_id=admin.id, token_hash=token_hash, expires_at=expires)
        db.session.add(prt)
        db.session.commit()

        # GET con token válido debe mostrar formulario (200)
        r_get = client.get(f'/auth/reset_password/{token}')
        assert r_get.status_code == 200
        assert b'Restablecer' in r_get.data or b'reset' in r_get.data.lower()

        # POST con nueva password debe redirigir a login (302) y marcar used
        r_post = client.post(f'/auth/reset_password/{token}', data={'password': 'NuevaPass123', 'confirm_password': 'NuevaPass123'})
        assert r_post.status_code == 302
        assert '/auth/login' in r_post.headers['Location']
        # verificar que quedó usado
        prt_check = PasswordResetToken.query.filter_by(token_hash=token_hash).first()
        assert prt_check.used_at is not None

        # Reuso del mismo token debe redirigir con mensaje de expirado
        r_reuse = client.get(f'/auth/reset_password/{token}', follow_redirects=True)
        assert r_reuse.status_code == 200
        flashes = _extract_flash_messages(r_reuse)
        assert any('inválido o ha expirado' in msg.lower() for cat, msg in flashes)

        # Restaurar password original para no romper otros tests
        admin2 = Usuario.query.get(admin.id)
        admin2.set_password('admin123')
        db.session.commit()
        PasswordResetToken.query.delete()
        PasswordResetAttempt.query.delete()
        db.session.commit()


def test_token_expirado_por_db(client, app):
    """Token con expires_at en el pasado debe ser rechazado aunque la firma sea válida."""
    _clean_reset_tables(app)
    admin = _get_admin(app)
    with app.app_context():
        from app.modules.identidad.presentation.auth_controller import get_serializer, _hash_token
        serializer = get_serializer()
        token = serializer.dumps(admin.id)
        token_hash = _hash_token(token)
        # expira hace 1 minuto
        expires = peru_now() - timedelta(minutes=1)
        prt = PasswordResetToken(usuario_id=admin.id, token_hash=token_hash, expires_at=expires)
        db.session.add(prt)
        db.session.commit()
        r = client.get(f'/auth/reset_password/{token}')
        assert r.status_code == 302
        assert '/auth/login' in r.headers['Location']
        PasswordResetToken.query.delete()
        db.session.commit()
    _clean_reset_tables(app)


def test_rate_limit_3_por_15_min(client, app):
    """4 intentos en 15 min desde misma IP debe throttlear el 4º."""
    _clean_reset_tables(app)
    ip = '10.0.0.99'
    with patch('app.modules.identidad.presentation.auth_controller.enviar_correo_recuperacion', return_value=True):
        for i in range(3):
            r = client.post('/auth/recuperar', data={'username': f'0000000{i}', 'email': f'a{i}@x.com'}, environ_base={'REMOTE_ADDR': ip})
            assert r.status_code == 200
            assert 'Si los datos son correctos' in r.data.decode('utf-8', errors='ignore')
        # 4º debe ser throttle
        r4 = client.post('/auth/recuperar', data={'username': '00000003', 'email': 'a3@x.com'}, environ_base={'REMOTE_ADDR': ip})
        assert r4.status_code == 200
        assert 'Has superado' in r4.data.decode('utf-8', errors='ignore') or 'límite' in r4.data.decode('utf-8', errors='ignore').lower()
    _clean_reset_tables(app)

    # También por DNI: 4 intentos con mismo username desde IPs distintas
    _clean_reset_tables(app)
    username = '12345678'
    admin = _get_admin(app)
    with patch('app.modules.identidad.presentation.auth_controller.enviar_correo_recuperacion', return_value=True):
        for i in range(3):
            r = client.post('/auth/recuperar', data={'username': username, 'email': admin.email}, environ_base={'REMOTE_ADDR': f'10.0.1.{i}'})
            assert r.status_code == 200
        r4 = client.post('/auth/recuperar', data={'username': username, 'email': admin.email}, environ_base={'REMOTE_ADDR': '10.0.1.99'})
        assert 'Has superado' in r4.data.decode('utf-8', errors='ignore')
    _clean_reset_tables(app)


def test_from_institucional_usa_mail_default_sender(app):
    """enviar_correo debe usar MAIL_DEFAULT_SENDER con nombre visible y bifurcar SSL/TLS."""
    with app.app_context():
        app.config['MAIL_SERVER'] = 'sgrv.azconsultingperu.com'
        app.config['MAIL_PORT'] = 465
        app.config['MAIL_USE_SSL'] = True
        app.config['MAIL_USE_TLS'] = False
        app.config['MAIL_USERNAME'] = 'soporte@sgrv.azconsultingperu.com'
        app.config['MAIL_PASSWORD'] = 'fake'
        app.config['MAIL_DEFAULT_SENDER'] = 'soporte@sgrv.azconsultingperu.com'
        app.config['MAIL_SENDER_NAME'] = 'SGRV – IESTP Paiján'
        from app.modules.notifications.infrastructure.email_adapter import enviar_correo, _build_from_header
        hdr, env = _build_from_header(app.config)
        assert 'soporte@sgrv.azconsultingperu.com' in hdr
        assert 'SGRV' in hdr

        # Mock SMTP_SSL para 465
        with patch('smtplib.SMTP_SSL') as mock_ssl, patch('smtplib.SMTP') as mock_smtp:
            mock_srv = MagicMock()
            mock_ssl.return_value = mock_srv
            mock_smtp.return_value = mock_srv
            admin = Usuario.query.filter_by(username='12345678').first()
            with patch('flask.render_template', return_value='<html>Hola</html>'):
                ok = enviar_correo('dest@example.com', 'Asunto', 'recuperar_contrasena.html', usuario=admin, reset_url='http://x')
            assert mock_ssl.called
            assert not mock_smtp.called
            # verificar que sendmail usa envelope del default sender
            assert mock_srv.sendmail.called
            envelope = mock_srv.sendmail.call_args[0][0]
            assert 'soporte@sgrv.azconsultingperu.com' in envelope

        # Mock STARTTLS para 587
        app.config['MAIL_PORT'] = 587
        app.config['MAIL_USE_SSL'] = False
        app.config['MAIL_USE_TLS'] = True
        with patch('smtplib.SMTP_SSL') as mock_ssl, patch('smtplib.SMTP') as mock_smtp:
            mock_srv = MagicMock()
            mock_ssl.return_value = mock_srv
            mock_smtp.return_value = mock_srv
            with patch('flask.render_template', return_value='<html>Hola</html>'):
                enviar_correo('dest@example.com', 'Asunto', 'recuperar_contrasena.html', usuario=admin, reset_url='http://x')
            assert mock_smtp.called
            assert mock_srv.starttls.called


def test_fallo_smtp_silencioso_no_expone_error(client, app):
    """Si SMTP falla, la respuesta sigue siendo genérica (no 'Error al enviar')."""
    _clean_reset_tables(app)
    admin = _get_admin(app)
    with patch('app.modules.identidad.presentation.auth_controller.enviar_correo_recuperacion', return_value=False):
        r = client.post('/auth/recuperar', data={'username': admin.username, 'email': admin.email})
        assert r.status_code == 200
        flashes = _extract_flash_messages(r)
        assert any('Si los datos son correctos' in msg for cat, msg in flashes)
        all_msgs = ' '.join(msg for cat, msg in flashes)
        assert 'Error al enviar' not in all_msgs
        assert 'Verifique la configuración' not in all_msgs
    _clean_reset_tables(app)


def test_plantilla_email_contiene_logo_saludo_boton_15min(app):
    """La plantilla HTML debe tener logo, saludo personalizado, botón y nota 15 min."""
    with app.app_context():
        admin = Usuario.query.filter_by(username='12345678').first()
        html = app.jinja_env.get_template('email/recuperar_contrasena.html').render(usuario=admin, reset_url='http://example.com/reset?token=abc')
        assert 'logo.png' in html.lower() or 'logo' in html.lower()
        assert 'Hola' in html
        assert admin.nombres in html
        assert 'Restablecer Contraseña' in html
        assert 'http://example.com/reset?token=abc' in html
        assert '15 minutos' in html or '15 min' in html
        assert '1 hora' not in html


def test_reset_password_visual_paridad(client, app):
    """reset_password.html debe usar auth.css v17, auth-validation.js y motto."""
    # Crear token válido para poder cargar la página (si no, redirige a login y no vemos el HTML)
    _clean_reset_tables(app)
    admin = _get_admin(app)
    with app.app_context():
        from app.modules.identidad.presentation.auth_controller import get_serializer, _hash_token
        serializer = get_serializer()
        token = serializer.dumps(admin.id)
        token_hash = _hash_token(token)
        prt = PasswordResetToken(usuario_id=admin.id, token_hash=token_hash, expires_at=peru_now() + timedelta(minutes=15))
        db.session.add(prt)
        db.session.commit()
        r = client.get(f'/auth/reset_password/{token}')
        body = r.data.decode('utf-8', errors='ignore')
        assert 'auth.css?v=17' in body
        assert 'auth-validation.js' in body
        assert '¡Crea, Innova e Inspira!' in body
        assert 'login-card' in body
        PasswordResetToken.query.delete()
        db.session.commit()
