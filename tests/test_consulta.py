"""Tests de consulta: lista y detalle (el bug del 'observar' 500 queda congelado aqui)."""
from app.modules.registro.domain.alumno import Alumno
from app import db
from app.utils.time_utils import peru_now


def _crear_alumno(app, dni, promotor_id=1):
    with app.app_context():
        a = Alumno(apellidos='CONSULTA', nombres=f'TEST{dni[-3:]}', dni=dni,
                   fecha_nacimiento=__import__('datetime').date(2006, 1, 1), edad=20,
                   sexo='M', celular='999000111', email=None, direccion=None,
                   institucion_id=1, carrera_id=1)
        db.session.add(a)
        db.session.flush()
        from app.modules.registro.domain.visita import Visita
        v = Visita(alumno_id=a.id, promotor_id=promotor_id, usuario_id=1,
                   fecha_visita=peru_now().date(), hora_visita=peru_now().time(),
                   observaciones='test')
        db.session.add(v)
        db.session.commit()
        return a.id


def test_lista_consulta_carga(auth_client):
    r = auth_client.get('/consulta/')
    assert r.status_code == 200


def test_detalle_del_alumno_200(auth_client, app):
    """Bug 2026-08: get_or_404 encadenado con filter_by lanzaba InvalidRequestError 500."""
    vid = _crear_alumno(app, '71344001')
    assert auth_client.get(f'/consulta/detalle/{vid}').status_code == 200


def test_detalle_sin_promotor_muestra_no_asignado(auth_client, app):
    vid = _crear_alumno(app, '71344002', promotor_id=None)
    r = auth_client.get(f'/consulta/detalle/{vid}')
    assert r.status_code == 200
    assert 'No asignado' in r.get_data(as_text=True)


def test_detalle_de_eliminado_da_404(auth_client, app):
    vid = _crear_alumno(app, '71344003')
    with app.app_context():
        a = db.session.get(Alumno, vid)
        a.eliminado = True
        db.session.commit()
    assert auth_client.get(f'/consulta/detalle/{vid}').status_code == 404


def test_verificar_dni_endpoint(auth_client, app):
    _crear_alumno(app, '71344004')
    assert b'true' in auth_client.get('/consulta/verificar-dni?dni=71344004').data.lower()
    assert b'false' in auth_client.get('/consulta/verificar-dni?dni=71999999').data.lower()
