"""Tests de reportes: exportaciones CSV y Excel."""
import io


def test_reportes_index_carga(auth_client):
    assert auth_client.get('/reportes/').status_code == 200


def test_csv_colegios(auth_client):
    r = auth_client.get('/reportes/colegios/csv')
    assert r.status_code == 200
    assert 'text/csv' in r.headers['Content-Type']


def test_excel_colegios(auth_client):
    r = auth_client.get('/reportes/colegios/excel')
    assert r.status_code == 200
    data = r.data
    # los xlsx empiezan con el magic bytes PK
    assert data[:2] == b'PK'


def test_excel_alumnos_vacio_no_explota(auth_client):
    r = auth_client.get('/reportes/alumnos/excel')
    assert r.status_code == 200


def test_reportes_requieren_rol(client, auth_client, app):
    """Un operador (rol 3) no debe poder exportar."""
    from app.modules.identidad.domain.usuario import Usuario
    from app import db
    with app.app_context():
        u = Usuario.query.filter_by(dni='11112222').first()
        u.intentos_fallidos = 0
        u.bloqueado_hasta = None
        db.session.commit()
    c = app.test_client()
    c.post('/auth/login', data={'username': '11112222', 'password': 'opera123'})
    r = c.get('/reportes/', follow_redirects=False)
    assert r.status_code == 302 and '/dashboard' in r.headers['Location']
