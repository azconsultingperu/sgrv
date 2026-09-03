# -*- coding: utf-8 -*-
"""Test para logo CID incrustado en emails."""
from unittest.mock import patch, MagicMock
import pytest


def test_plantilla_no_url_externa_y_contiene_cid(app):
    with app.app_context():
        from flask import render_template
        from app.modules.identidad.domain.usuario import Usuario
        u = Usuario.query.filter_by(username='12345678').first()
        html = render_template('email/recuperar_contrasena.html', usuario=u, reset_url='https://example.com/reset?token=xyz')
        assert 'cid:logo_sgrv' in html, "HTML debe usar cid:logo_sgrv"
        assert 'raw.githubusercontent' not in html, "No debe contener URL externa raw.githubusercontent"
        assert 'sgrv.azconsultingperu.com/static' not in html, "No debe contener URL absoluta a static"
        # Verifica otras plantillas también
        for tmpl, kwargs in [
            ('nuevo_registro.html', {'alumno': MagicMock(dni='12345678', nombres='A', apellidos='B', edad=17, sexo='M', celular='999', email='a@b.com', institucion=MagicMock(nombre='IE', distrito='Paijan'), carrera=MagicMock(nombre='TIC'), desea_estudiar=True), 'visita': MagicMock(promotor=MagicMock(nombres='P', apellidos='Q'), observaciones='obs', fecha_visita=None, hora_visita=None)}),
            ('nuevo_usuario.html', {'usuario': u, 'password': 'pass123'}),
        ]:
            html2 = render_template(f'email/{tmpl}', **kwargs)
            assert 'cid:logo_sgrv' in html2
            assert 'raw.githubusercontent' not in html2


def test_enviar_correo_adjunta_logo_cid(app):
    with app.app_context():
        from app.modules.identidad.domain.usuario import Usuario
        from app.modules.notifications.infrastructure.email_adapter import enviar_correo
        # asegurar config para SSL path
        app.config['MAIL_SERVER'] = 'sgrv.azconsultingperu.com'
        app.config['MAIL_PORT'] = 465
        app.config['MAIL_USE_SSL'] = True
        app.config['MAIL_USE_TLS'] = False
        app.config['MAIL_USERNAME'] = 'soporte@sgrv.azconsultingperu.com'
        app.config['MAIL_PASSWORD'] = 'dummy'
        u = Usuario.query.filter_by(username='12345678').first()
        with patch('smtplib.SMTP_SSL') as mock_ssl:
            mock_srv = MagicMock()
            mock_ssl.return_value = mock_srv
            ok = enviar_correo('test@example.com', 'Asunto Test', 'recuperar_contrasena.html', usuario=u, reset_url='https://example.com/reset')
            assert ok is True
            assert mock_srv.sendmail.called
            sent_str = mock_srv.sendmail.call_args[0][2]
            assert 'Content-ID: <logo_sgrv>' in sent_str or 'logo_sgrv' in sent_str
            assert 'image/png' in sent_str
            assert 'multipart/related' in sent_str
            assert 'multipart/alternative' in sent_str
