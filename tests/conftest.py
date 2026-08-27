import pytest
from app import create_app, db
from app.utils.seed import seed_data


@pytest.fixture(scope='session')
def app():
    """App de prueba con SQLite en memoria y datos sembrados una sola vez."""
    import os
    os.environ['FLASK_ENV'] = 'testing'
    application = create_app()
    application.config.update({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
    })
    with application.app_context():
        db.create_all()
        seed_data()
    # IMPORTANTE: cerrar el contexto antes del yield. Si los tests corrieran dentro
    # de este app_context, Flask-Login cachearia current_user en `g` y un login
    # contaminaria a todos los tests siguientes.
    yield application


@pytest.fixture()
def client(app):
    """Cliente anonimo fresco por test (sin cookies heredadas)."""
    return app.test_client()


@pytest.fixture()
def auth_client(app):
    """Cliente ya autenticado como administrador, uno nuevo por test."""
    c = app.test_client()
    r = c.post('/auth/login', data={'username': '12345678', 'password': 'admin123'})
    assert r.status_code == 302, 'El login del admin debe funcionar en los tests'
    return c


@pytest.fixture
def alumno_base():
    """Payload valido para el formulario de registro."""
    return {
        'apellidos': 'TESTEO', 'nombres': 'ALUMNO', 'dni': '55556666',
        'fecha_nacimiento': '2006-03-15', 'sexo': 'M', 'celular': '999111222',
        'email': 'test@alumno.com', 'direccion': 'Jr. Test 456',
        'institucion_id': '1', 'carrera_id': '1', 'area_interes': 'TIC',
        'desea_estudiar': 'on', 'solicita_info': '',
        'modalidad_contacto': 'CORREO', 'fecha_visita': '', 'hora_visita': '',
        'promotor_id': '', 'observaciones': 'creado por tests',
    }


@pytest.fixture(autouse=True)
def _limpiar_datos_de_prueba(app):
    """Borra los registros que crean los tests para no contaminar la sesion."""
    yield
    with app.app_context():
        from app.models.alumno import Alumno
        from app.models.usuario import Usuario
        from app.models.visita import Visita
        dnis_alumno = [f'71234{n:03d}' for n in range(0, 10)] + ['71344001', '71344002', '71344003', '71344004']
        alumnos = Alumno.query.filter(Alumno.dni.in_(dnis_alumno)).all()
        for a in alumnos:
            Visita.query.filter_by(alumno_id=a.id).delete(synchronize_session=False)
        Alumno.query.filter(Alumno.dni.in_(dnis_alumno)).delete(synchronize_session=False)
        Usuario.query.filter(Usuario.dni.in_(['71444123', '71184654'])).delete(synchronize_session=False)
        db.session.commit()

        # restaurar estado del operador por si algun test lo bloqueo
        u = Usuario.query.filter_by(dni='11112222').first()
        if u and (u.intentos_fallidos or u.bloqueado_hasta):
            u.intentos_fallidos = 0
            u.bloqueado_hasta = None
            db.session.commit()
