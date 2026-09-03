# -*- coding: utf-8 -*-
"""Tests para reactivación de usuario eliminado (soft delete + índice parcial)."""
from datetime import timedelta
from app import db
from app.modules.identidad.domain.usuario import Usuario
from app.modules.auditoria.domain.auditoria import Auditoria
from app.utils.time_utils import peru_now


def _crear_usuario_activo(app, dni='71444200', email='activo@iestp.edu.pe'):
    with app.app_context():
        u = Usuario(dni=dni, nombres='ACTIVO', apellidos='TEST', username=dni, email=email, rol_id=3)
        u.set_password('Clave1234')
        db.session.add(u)
        db.session.commit()
        return u.id

def _eliminar_usuario(app, uid):
    with app.app_context():
        u = db.session.get(Usuario, uid)
        u.eliminado = True
        u.estado = False
        db.session.commit()


def test_reactivar_dni_eliminado_actualiza_y_no_duplica(auth_client, app):
    """Crear sobre DNI eliminado debe reactivar la misma fila, actualizar campos y resetear bloqueo."""
    with app.app_context():
        u = Usuario(dni='71444201', nombres='VIEJO', apellidos='USER', username='71444201', email='viejo@iestp.edu.pe', rol_id=3)
        u.set_password('OldPass123')
        u.intentos_fallidos = 5
        u.bloqueado_hasta = peru_now() + timedelta(minutes=10)
        db.session.add(u)
        db.session.commit()
        uid = u.id
        # soft delete
        u.eliminado = True
        u.estado = False
        db.session.commit()
        count_antes = Usuario.query.filter_by(dni='71444201').count()

    # Intentar crear con mismo DNI pero datos nuevos
    r = auth_client.post('/usuarios/crear', data={
        'dni': '71444201', 'nombres': 'JUAN DAVID', 'apellidos': 'RIVERA HUANCAS',
        'password': 'NuevaPass123', 'email': 'nuevo@iestp.edu.pe', 'rol_id': '1',
    }, follow_redirects=True)
    assert 'reactivado' in r.get_data(as_text=True).lower()

    with app.app_context():
        # No duplica fila
        assert Usuario.query.filter_by(dni='71444201').count() == count_antes
        u2 = db.session.get(Usuario, uid)
        assert u2.eliminado is False
        assert u2.estado is True
        assert u2.nombres == 'JUAN DAVID'
        assert u2.apellidos == 'RIVERA HUANCAS'
        assert u2.email == 'nuevo@iestp.edu.pe'
        assert u2.rol_id == 1
        assert u2.check_password('NuevaPass123')
        assert u2.intentos_fallidos == 0
        assert u2.bloqueado_hasta is None


def test_crear_dni_activo_bloquea(auth_client, app):
    uid = _crear_usuario_activo(app, dni='71444202', email='activo2@iestp.edu.pe')
    try:
        r = auth_client.post('/usuarios/crear', data={
            'dni': '71444202', 'nombres': 'DUP', 'apellidos': 'USER',
            'password': 'Clave1234', 'email': 'otro@iestp.edu.pe', 'rol_id': '3',
        }, follow_redirects=True)
        assert 'ya está registrado' in r.get_data(as_text=True).lower()
        with app.app_context():
            # No se creó duplicado
            assert Usuario.query.filter_by(dni='71444202').count() == 1
    finally:
        with app.app_context():
            u = db.session.get(Usuario, uid)
            if u:
                db.session.delete(u)
                db.session.commit()


def test_verificar_dni_filtra_eliminados(auth_client, app):
    # Crear y eliminar
    with app.app_context():
        u = Usuario(dni='71444203', nombres='ELIM', apellidos='TEST', username='71444203', email='elim3@iestp.edu.pe', rol_id=3)
        u.set_password('Clave1234')
        db.session.add(u)
        db.session.commit()
        uid = u.id
        u.eliminado = True
        db.session.commit()

    r = auth_client.get('/usuarios/verificar-dni?dni=71444203')
    assert r.get_json()['existe'] is False

    # Reactivar y verificar que ahora sí existe
    with app.app_context():
        u = db.session.get(Usuario, uid)
        u.eliminado = False
        db.session.commit()
    r2 = auth_client.get('/usuarios/verificar-dni?dni=71444203')
    assert r2.get_json()['existe'] is True

    # Cleanup
    with app.app_context():
        u = db.session.get(Usuario, uid)
        db.session.delete(u)
        db.session.commit()


def test_indice_parcial_impide_dos_activos_mismo_dni(app):
    """Índice parcial solo permite un activo por DNI, pero permite histórico eliminado."""
    with app.app_context():
        # Limpiar previos
        Usuario.query.filter(Usuario.dni.in_(['71444204', '71444205'])).delete(synchronize_session=False)
        db.session.commit()

        u1 = Usuario(dni='71444204', nombres='A', apellidos='A', username='71444204', email='a1@iestp.edu.pe', rol_id=3)
        u1.set_password('Clave1234')
        db.session.add(u1)
        db.session.commit()

        # Segundo activo con mismo DNI debe fallar por índice parcial
        u_dup = Usuario(dni='71444204', nombres='B', apellidos='B', username='71444204_dup', email='b1@iestp.edu.pe', rol_id=3)
        # Usar username distinto para aislar solo DNI
        u_dup.username = '71444204_dup2'
        u_dup.email = 'b1_dup@iestp.edu.pe'
        # Forzar mismo dni pero distinto username/email, pero activo
        u_dup.dni = '71444204'
        u_dup.set_password('Clave1234')
        db.session.add(u_dup)
        try:
            db.session.commit()
            assert False, "Debe violar índice parcial"
        except Exception:
            db.session.rollback()

        # En cambio, con eliminado=True sí permite duplicar DNI
        u_hist = Usuario(dni='71444204', nombres='HIST', apellidos='HIST', username='71444204_hist', email='hist@iestp.edu.pe', rol_id=3, eliminado=True)
        u_hist.set_password('Clave1234')
        db.session.add(u_hist)
        db.session.commit()
        # Debe haber 2 filas con mismo DNI (una activa, una eliminada)
        assert Usuario.query.filter_by(dni='71444204').count() == 2

        # Cleanup
        Usuario.query.filter(Usuario.dni == '71444204').delete(synchronize_session=False)
        db.session.commit()


def test_auditoria_usuario_reactivado(auth_client, app):
    with app.app_context():
        u = Usuario(dni='71444206', nombres='AUD', apellidos='TEST', username='71444206', email='aud@iestp.edu.pe', rol_id=3)
        u.set_password('OldPass123')
        db.session.add(u)
        db.session.commit()
        uid = u.id
        u.eliminado = True
        db.session.commit()
        # Limpiar auditorías previas de ese DNI para aislar
        Auditoria.query.filter(Auditoria.detalle.like('%71444206%')).delete(synchronize_session=False)
        db.session.commit()

    r = auth_client.post('/usuarios/crear', data={
        'dni': '71444206', 'nombres': 'AUD2', 'apellidos': 'TEST2',
        'password': 'NuevaPass123', 'email': 'aud2@iestp.edu.pe', 'rol_id': '3',
    }, follow_redirects=True)
    assert 'reactivado' in r.get_data(as_text=True).lower()

    with app.app_context():
        aud = Auditoria.query.filter_by(accion='Usuario reactivado').order_by(Auditoria.id.desc()).first()
        assert aud is not None
        assert '71444206' in aud.detalle
        assert aud.modulo == 'Usuarios'
