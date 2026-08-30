# -*- coding: utf-8 -*-
import logging
from app.shared.events import AlumnoRegistrado, UsuarioCreado

logger = logging.getLogger(__name__)

def on_alumno_registrado(event: AlumnoRegistrado):
    try:
        # Lazy import to avoid circular
        from app.modules.registro.domain.alumno import Alumno
        from app.modules.registro.domain.visita import Visita
        from app.modules.notifications.infrastructure.email_adapter import notificar_nuevo_registro
        alumno = Alumno.query.get(event.alumno_id)
        if not alumno:
            return
        visita = Visita.query.filter_by(alumno_id=alumno.id).first()
        notificar_nuevo_registro(alumno, visita)
    except Exception as e:
        logger.exception("Error enviando notificación de alumno %s: %s", event.dni, e)

def on_usuario_creado(event: UsuarioCreado):
    try:
        from app.modules.identidad.domain.usuario import Usuario
        from app.modules.notifications.infrastructure.email_adapter import notificar_nuevo_usuario
        usuario = Usuario.query.get(event.usuario_id)
        if not usuario:
            return
        # Note: password not available in event; email will be sent without password or with placeholder
        notificar_nuevo_usuario(usuario, password="(ver sistema)")
    except Exception as e:
        logger.exception("Error enviando notificación de usuario %s: %s", event.username, e)

def register(bus):
    bus.subscribe(AlumnoRegistrado, on_alumno_registrado)
    bus.subscribe(UsuarioCreado, on_usuario_creado)
