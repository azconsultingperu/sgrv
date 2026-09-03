# -*- coding: utf-8 -*-
"""Verifica que POST /auth/recuperar responde sin esperar al SMTP (async)."""
import time
from unittest.mock import MagicMock, patch


def test_post_no_espera_smtp_lento(app):
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['DISABLE_RATE_LIMIT'] = True
    # Limpiar intentos previos
    with app.app_context():
        from app.modules.identidad.domain.password_reset import PasswordResetAttempt
        from app.shared.db import db
        PasswordResetAttempt.query.delete()
        db.session.commit()

    # Mock que simula SMTP lento (10s) — si fuera síncrono, el POST tardaría 10s
    def fake_smtp_ssl(*args, **kwargs):
        mock_srv = MagicMock()
        def fake_login(*a, **kw):
            time.sleep(0.05)  # pequeño delay para login
            return (235, b'ok')
        def fake_sendmail(*a, **kw):
            time.sleep(10)  # simula DATA lento a Gmail
            return {}
        mock_srv.login.side_effect = fake_login
        mock_srv.sendmail.side_effect = fake_sendmail
        mock_srv.ehlo.return_value = (250, b'ok')
        mock_srv.quit.return_value = None
        return mock_srv

    with patch('app.modules.notifications.infrastructure.email_adapter.smtplib.SMTP_SSL', side_effect=fake_smtp_ssl):
        with patch('app.modules.notifications.infrastructure.email_adapter.smtplib.SMTP') as mock_smtp:
            # Por si cae en rama TLS, también mockearla con delay
            mock_srv2 = MagicMock()
            mock_srv2.login.return_value = (235, b'ok')
            def fake_send2(*a, **kw):
                time.sleep(10)
                return {}
            mock_srv2.sendmail.side_effect = fake_send2
            mock_smtp.return_value = mock_srv2

            with app.test_client() as client:
                start = time.time()
                r = client.post('/auth/recuperar',
                                data={'username': '71184654', 'email': 'juandavidriverahuancas0@gmail.com'},
                                headers={'X-Requested-With': 'XMLHttpRequest'})
                elapsed = time.time() - start
                assert r.status_code == 200
                assert r.mimetype == 'application/json'
                # Debe volver en <500ms aunque el SMTP mock duerme 10s
                assert elapsed < 0.5, f"POST tardó {elapsed:.3f}s, debería ser <0.5s (async)"
                data = r.get_json()
                assert data['status'] == 'ok'
                # Dar tiempo al hilo background para que intente enviar (no bloquea el assert anterior)
                time.sleep(0.2)
