"""Regresion: usuarios Operador como Promotor Responsable (union en vivo)."""
import pytest
from app.modules.registro.domain.alumno import Alumno
from app.modules.identidad.domain.usuario import Usuario


@pytest.fixture(scope='module')
def promotores_clasicos(app):
    """Crea 2 promotores clasicos propios (el seed ya no los provee)."""
    from app import db
    from app.modules.registro.domain.promotor import Promotor
    with app.app_context():
        p1 = Promotor(dni='90000001', nombres='Clasico', apellidos='Uno')
        p2 = Promotor(dni='90000002', nombres='Clasico', apellidos='Dos')
        db.session.add_all([p1, p2])
        db.session.commit()
        ids = (p1.id, p2.id)
    yield ids
    with app.app_context():
        Promotor.query.filter(Promotor.dni.in_(['90000001', '90000002'])).delete(synchronize_session=False)
        db.session.commit()


def _payload(dni, promotor=''):
    return {
        'apellidos': 'PROM', 'nombres': 'TEST', 'dni': dni,
        'fecha_nacimiento': '2006-03-15', 'sexo': 'M', 'celular': '999111222',
        'email': '', 'direccion': '',
        'institucion_id': '1', 'carrera_id': '1',
        'fecha_visita': '', 'hora_visita': '',
        'promotor_id': promotor, 'observaciones': '',
    }


def _operador_seed(app):
    with app.app_context():
        op = Usuario.query.filter_by(dni='11112222').first()
        return op.id, f'{op.nombres} {op.apellidos}'


def test_operador_seed_aparece_en_registro(auth_client, app, promotores_clasicos):
    _, nombre = _operador_seed(app)
    r = auth_client.get('/registro/')
    html = r.get_data(as_text=True)
    assert r.status_code == 200
    assert 'data-origen="operador"' in html
    assert nombre in html
    assert 'data-origen="promotor"' in html


def test_nuevo_operador_aparece_sin_pasos_extra(auth_client):
    r = auth_client.post('/usuarios/crear', data={
        'dni': '71444123', 'nombres': 'Nuevo', 'apellidos': 'Operador',
        'email': 'nuevo.operador@test.com', 'password': 'opera1234', 'rol_id': '3',
    }, follow_redirects=True)
    assert 'exitosamente' in r.get_data(as_text=True).lower()
    html = auth_client.get('/registro/').get_data(as_text=True)
    assert 'NUEVO OPERADOR' in html


def test_registro_con_operador_guarda_visita(auth_client, app):
    oid, nombre = _operador_seed(app)
    dni = '71234005'
    r = auth_client.post('/registro/', data=_payload(dni, f'operador:{oid}'))
    assert r.status_code == 302
    with app.app_context():
        v = Alumno.query.filter_by(dni=dni).first().visitas.first()
        assert v.promotor_id is None
        assert v.operador_promotor_id == oid
        assert v.promotor_nombre == nombre


def test_registro_con_promotor_clasico_prefijado(auth_client, app, promotores_clasicos):
    pid, _ = promotores_clasicos
    dni = '71234006'
    r = auth_client.post('/registro/', data=_payload(dni, f'promotor:{pid}'))
    assert r.status_code == 302
    with app.app_context():
        v = Alumno.query.filter_by(dni=dni).first().visitas.first()
        assert v.promotor_id == pid and v.operador_promotor_id is None


def test_registro_con_promotor_legado_entero(auth_client, app, promotores_clasicos):
    _, pid = promotores_clasicos
    dni = '71234007'
    r = auth_client.post('/registro/', data=_payload(dni, str(pid)))
    assert r.status_code == 302
    with app.app_context():
        v = Alumno.query.filter_by(dni=dni).first().visitas.first()
        assert v.promotor_id == pid and v.operador_promotor_id is None


def test_operador_elegido_persiste_tras_error(auth_client, app):
    oid, _ = _operador_seed(app)
    r = auth_client.post('/registro/', data=_payload('123', f'operador:{oid}'))
    html = r.get_data(as_text=True)
    assert r.status_code == 200
    assert f'value="operador:{oid}" data-origen="operador" selected' in html


def test_detalle_muestra_operador(auth_client, app):
    oid, nombre = _operador_seed(app)
    dni = '71234008'
    auth_client.post('/registro/', data=_payload(dni, f'operador:{oid}'))
    with app.app_context():
        aid = Alumno.query.filter_by(dni=dni).first().id
    html = auth_client.get(f'/consulta/detalle/{aid}').get_data(as_text=True)
    assert nombre in html


def test_operador_inactivo_desaparece_pero_historico_permanece(auth_client, app):
    from app import db
    oid, nombre = _operador_seed(app)
    dni = '71234009'
    auth_client.post('/registro/', data=_payload(dni, f'operador:{oid}'))
    with app.app_context():
        Usuario.query.filter_by(dni='11112222').first().estado = False
        db.session.commit()
    try:
        html = auth_client.get('/registro/').get_data(as_text=True)
        assert nombre not in html
        with app.app_context():
            v = Alumno.query.filter_by(dni=dni).first().visitas.first()
            assert v.promotor_nombre == nombre
    finally:
        with app.app_context():
            Usuario.query.filter_by(dni='11112222').first().estado = True
            db.session.commit()


def test_reporte_visitas_con_operador_y_null_no_explota(auth_client, app):
    oid, nombre = _operador_seed(app)
    auth_client.post('/registro/', data=_payload('71344003', f'operador:{oid}'))
    auth_client.post('/registro/', data=_payload('71344004', ''))
    r = auth_client.get('/reportes/visitas/csv')
    assert r.status_code == 200
    txt = r.get_data(as_text=True)
    assert nombre in txt
    assert 'No asignado' in txt


def test_editar_cambia_a_operador(auth_client, app):
    oid, nombre = _operador_seed(app)
    dni = '71344001'
    auth_client.post('/registro/', data=_payload(dni, ''))
    with app.app_context():
        aid = Alumno.query.filter_by(dni=dni).first().id
    r = auth_client.post(f'/registro/editar/{aid}', data={
        'dni': dni, 'apellidos': 'PROM', 'nombres': 'TEST',
        'celular': '999111222', 'institucion_id': '1',
        'promotor_id': f'operador:{oid}',
    })
    assert r.status_code == 302
    with app.app_context():
        v = Alumno.query.filter_by(dni=dni).first().visitas.first()
        assert v.operador_promotor_id == oid and v.promotor_id is None
        assert v.promotor_nombre == nombre
    html = auth_client.get(f'/registro/editar/{aid}').get_data(as_text=True)
    assert f'value="operador:{oid}" data-origen="operador" selected' in html
