# -*- coding: utf-8 -*-
from flask import request
from app.shared.db import db
from app.shared.events import AlumnoRegistrado, AlumnoEliminado, AlumnoActualizado, UsuarioCreado, UsuarioEliminado

def _ip_ua():
    try:
        ip = request.remote_addr if request else None
        ua = request.user_agent.string if request and request.user_agent else None
    except RuntimeError:
        ip = None
        ua = None
    return ip, ua

def on_alumno_registrado(event: AlumnoRegistrado):
    from app.modules.auditoria.domain.auditoria import Auditoria
    ip, ua = _ip_ua()
    aud = Auditoria(
        usuario_id=event.actor_id,
        accion='Creación de registro',
        modulo='Registro',
        detalle=f'Registro creado: Alumno {event.dni} - {event.nombres} {event.apellidos}',
        ip_address=ip,
        user_agent=ua
    )
    db.session.add(aud)
    db.session.commit()

def on_alumno_eliminado(event: AlumnoEliminado):
    from app.modules.auditoria.domain.auditoria import Auditoria
    ip, ua = _ip_ua()
    aud = Auditoria(
        usuario_id=event.actor_id,
        accion='Eliminación de registro',
        modulo='Registro',
        detalle=f'Registro eliminado (soft delete): Alumno {event.dni}',
        ip_address=ip,
        user_agent=ua
    )
    db.session.add(aud)
    db.session.commit()

def on_alumno_actualizado(event: AlumnoActualizado):
    from app.modules.auditoria.domain.auditoria import Auditoria
    ip, ua = _ip_ua()
    aud = Auditoria(
        usuario_id=event.actor_id,
        accion='Edición de registro',
        modulo='Registro',
        detalle=f'Registro editado: Alumno {event.dni}',
        ip_address=ip,
        user_agent=ua
    )
    db.session.add(aud)
    db.session.commit()

def on_usuario_creado(event: UsuarioCreado):
    from app.modules.auditoria.domain.auditoria import Auditoria
    ip, ua = _ip_ua()
    aud = Auditoria(
        usuario_id=event.actor_id,
        accion='Creación de usuario',
        modulo='Usuarios',
        detalle=f'Usuario creado: {event.username} ({event.dni})',
        ip_address=ip, user_agent=ua
    )
    db.session.add(aud)
    db.session.commit()

def on_usuario_eliminado(event: UsuarioEliminado):
    from app.modules.auditoria.domain.auditoria import Auditoria
    ip, ua = _ip_ua()
    aud = Auditoria(usuario_id=event.actor_id, accion='Eliminación de usuario', modulo='Usuarios', detalle=f'Usuario eliminado (soft delete): {event.username}', ip_address=ip, user_agent=ua)
    db.session.add(aud)
    db.session.commit()

def register(bus):
    bus.subscribe(AlumnoRegistrado, on_alumno_registrado)
    bus.subscribe(AlumnoEliminado, on_alumno_eliminado)
    bus.subscribe(AlumnoActualizado, on_alumno_actualizado)
    bus.subscribe(UsuarioCreado, on_usuario_creado)
    bus.subscribe(UsuarioEliminado, on_usuario_eliminado)
