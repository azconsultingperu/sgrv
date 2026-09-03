# -*- coding: utf-8 -*-
"""Regresión para consumo único de flash throttled (fix-flash-persistente)."""
import re
import html as html_lib
import json


def _get_flash(response):
    body = response.data.decode('utf-8', errors='ignore')
    m = re.search(r"id=\"flashData\" data-messages='([^']*)'", body)
    if not m:
        return []
    return json.loads(html_lib.unescape(m.group(1)))


def test_post_throttled_devuelve_json_sin_flash_y_get_no_repite(app):
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['DISABLE_RATE_LIMIT'] = False
    with app.app_context():
        from app.modules.identidad.domain.password_reset import PasswordResetAttempt
        from app.shared.db import db
        PasswordResetAttempt.query.delete()
        db.session.commit()

    with app.test_client() as client:
        # 3 intentos para llenar ventana
        for _ in range(3):
            client.post('/auth/recuperar', data={'username': '71184654', 'email': 'a@b.com'},
                        headers={'X-Requested-With': 'XMLHttpRequest'})
        # 4to throttled debe ser JSON sin flash en sesión
        r4 = client.post('/auth/recuperar', data={'username': '71184654', 'email': 'a@b.com'},
                         headers={'X-Requested-With': 'XMLHttpRequest'})
        assert r4.status_code == 200
        assert r4.mimetype == 'application/json'
        data = json.loads(r4.data)
        assert data['status'] == 'throttled'
        assert 'Has superado' in data['message']
        # GET posterior no debe contener flash throttled
        r_get = client.get('/auth/recuperar')
        flash_get = _get_flash(r_get)
        assert not any('Has superado' in msg for cat, msg in flash_get), f"GET no debe repetir flash, got {flash_get}"


def test_post_ok_devuelve_json_sin_flash_y_get_no_repite(app):
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['DISABLE_RATE_LIMIT'] = True  # para no throttlear este test
    with app.app_context():
        from app.modules.identidad.domain.password_reset import PasswordResetAttempt
        from app.shared.db import db
        PasswordResetAttempt.query.delete()
        db.session.commit()

    with app.test_client() as client:
        r = client.post('/auth/recuperar', data={'username': '71184654', 'email': 'juandavidriverahuancas0@gmail.com'},
                        headers={'X-Requested-With': 'XMLHttpRequest'})
        assert r.status_code == 200
        assert r.mimetype == 'application/json'
        data = json.loads(r.data)
        assert data['status'] == 'ok'
        assert 'Si los datos son correctos' in data['message']
        r_get = client.get('/auth/recuperar')
        flash_get = _get_flash(r_get)
        assert not any('Si los datos son correctos' in msg for cat, msg in flash_get)


def test_post_no_ajax_mantiene_flash_legacy(app):
    """Sin X-Requested-With debe seguir usando flash + HTML (compatibilidad)."""
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['DISABLE_RATE_LIMIT'] = False
    with app.app_context():
        from app.modules.identidad.domain.password_reset import PasswordResetAttempt
        from app.shared.db import db
        PasswordResetAttempt.query.delete()
        db.session.commit()
    with app.test_client() as client:
        # Sin header XMLHttpRequest
        r = client.post('/auth/recuperar', data={'username': '71184654', 'email': 'a@b.com'})
        assert r.status_code == 200
        # Debe ser HTML con flashData, no JSON
        assert 'text/html' in r.mimetype
        flash = _get_flash(r)
        assert any('Si los datos son correctos' in msg for cat, msg in flash)
