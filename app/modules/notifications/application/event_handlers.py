# -*- coding: utf-8 -*-
import logging
import threading
from app.shared.events import AlumnoRegistrado, UsuarioCreado

logger = logging.getLogger(__name__)

def _async_send(target, *args, **kwargs):
    try:
        from flask import current_app
        app = current_app._get_current_object()
    except RuntimeError:
        from app import create_app
        app = create_app()
    def _run():
        try:
            with app.app_context():
                target(*args, **kwargs)
        except Exception as e:
            logger.exception("Async email failed: %s", e)
    t = threading.Thread(target=_run, daemon=True)
    t.start()

def _send_alumno_notification(event):
    from app.modules.registro.domain.alumno import Alumno
    from app.modules.registro.domain.visita import Visita
    from app.modules.notifications.infrastructure.email_adapter import notificar_nuevo_registro
    alumno = Alumno.query.get(event.alumno_id)
    if not alumno:
        return
    visita = Visita.query.filter_by(alumno_id=alumno.id).first()
    notificar_nuevo_registro(alumno, visita)

def _send_usuario_notification(event):
    from app.modules.identidad.domain.usuario import Usuario
    from app.modules.notifications.infrastructure.email_adapter import notificar_nuevo_usuario
    usuario = Usuario.query.get(event.usuario_id)
    if not usuario:
        return
    notificar_nuevo_usuario(usuario, password="(ver sistema)")

def on_alumno_registrado(event: AlumnoRegistrado):
    try:
        _async_send(_send_alumno_notification, event)
    except Exception as e:
        logger.exception("Error encolando notificación de alumno %s: %s", event.dni, e)

def on_usuario_creado(event: UsuarioCreado):
    try:
        _async_send(_send_usuario_notification, event)
    except Exception as e:
        logger.exception("Error encolando notificación de usuario %s: %s", event.username, e)

def register(bus):
    bus.subscribe(AlumnoRegistrado, on_alumno_registrado)
    bus.subscribe(UsuarioCreado, on_usuario_creado)
