"""Tests del flujo de registro de alumnos (los bugs criticos de agosto 2026 quedan congelados aqui)."""
from app.models.alumno import Alumno


def _dni_unico(n=0):
    return f'71234{n:03d}'


def test_registro_exitoso_completo(auth_client, alumno_base):
    alumno_base['dni'] = _dni_unico(1)
    r = auth_client.post('/registro/', data=alumno_base)
    assert r.status_code == 302, 'El registro valido debe redirigir a consulta'
    assert '/consulta' in r.headers['Location']
    with auth_client.application.app_context():
        assert Alumno.query.filter_by(dni=_dni_unico(1)).first() is not None


def test_registro_sin_promotor_se_guarda(auth_client, alumno_base):
    """Bug 2026-08: visitas.promotor_id era NOT NULL y el registro sin promotor
    fallaba silenciosamente. Debe crear alumno y visita con promotor NULL."""
    dni = _dni_unico(2)
    alumno_base['dni'] = dni
    r = auth_client.post('/registro/', data=alumno_base)
    assert r.status_code == 302
    with auth_client.application.app_context():
        a = Alumno.query.filter_by(dni=dni).first()
        assert a is not None, 'El alumno debe crearse aunque no haya promotor'
        v = a.visitas.first()
        assert v is not None and v.promotor_id is None


def test_registro_dni_duplicado_rechazado(auth_client, alumno_base):
    dni = _dni_unico(3)
    alumno_base['dni'] = dni
    auth_client.post('/registro/', data=alumno_base)
    r = auth_client.post('/registro/', data=alumno_base, follow_redirects=True)
    assert 'ya est' in r.get_data(as_text=True).lower()


def test_registro_dni_invalido_rechazado(auth_client, alumno_base):
    alumno_base['dni'] = '123'
    r = auth_client.post('/registro/', data=alumno_base, follow_redirects=True)
    assert 'DNI debe tener' in r.get_data(as_text=True)


def test_registro_fecha_invalida_no_crea(auth_client, alumno_base):
    """Bug 2026-08 (dead code): una fecha invalida no debe crear nada ni colgar."""
    dni = _dni_unico(4)
    alumno_base['dni'] = dni
    alumno_base['fecha_nacimiento'] = 'fecha-mala'
    r = auth_client.post('/registro/', data=alumno_base, follow_redirects=True)
    assert 'La fecha de nacimiento' in r.get_data(as_text=True)
    with auth_client.application.app_context():
        assert Alumno.query.filter_by(dni=dni).first() is None
