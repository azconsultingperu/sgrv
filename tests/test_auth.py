"""Tests de autenticacion: login, credenciales y bloqueo por intentos."""
from datetime import timedelta
from app import db
from app.modules.identidad.domain.usuario import Usuario
from app.utils.time_utils import peru_now


def test_login_exitoso(client):
    r = client.post('/auth/login', data={'username': '12345678', 'password': 'admin123'})
    assert r.status_code == 302
    assert '/dashboard' in r.headers['Location']


def test_login_password_incorrecta(client):
    r = client.post('/auth/login', data={'username': '12345678', 'password': 'clave-mala'})
    assert r.status_code == 200, 'Password incorrecta re-renderiza el formulario'
    assert b'login' in r.data.lower()


def test_login_usuario_inexistente(client):
    r = client.post('/auth/login', data={'username': '00000000', 'password': 'x1234567'})
    assert r.status_code == 200


def test_ruta_protegida_redirige_a_login(client):
    r = client.get('/registro/')
    assert r.status_code == 302
    assert '/auth/login' in r.headers['Location']


def test_lockout_tras_intentos_fallidos(client, app):
    """5 intentos fallidos activan el bloqueo temporal de la cuenta."""
    with app.app_context():
        u = Usuario.query.filter_by(dni='11112222').first()
        u.intentos_fallidos = app.config['MAX_LOGIN_ATTEMPTS']
        u.bloqueado_hasta = peru_now() + timedelta(minutes=10)
        db.session.commit()

    # La cuenta bloqueada NO debe poder entrar (el login ya no muestra mensajes,
    # asi que verificamos la seguridad, no el texto).
    r = client.post('/auth/login', data={'username': '11112222', 'password': 'opera123'})
    assert r.status_code == 200, 'Re-render del formulario, nunca redirect al dashboard'
    with client.session_transaction() as s:
        assert '_user_id' not in s, 'La sesion no debe autenticarse con la cuenta bloqueada'

    with app.app_context():
        u = Usuario.query.filter_by(dni='11112222').first()
        u.intentos_fallidos = 0
        u.bloqueado_hasta = None
        db.session.commit()
