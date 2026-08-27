# -*- coding: utf-8 -*-
from flask import request
from app.shared.events import AvatarActualizado, AvatarEliminado
from app.shared.db import db

def _registrar_auditoria(usuario_id, accion, modulo, detalle=None, avatar=None):
    from app.models.auditoria import Auditoria
    # Import here to avoid circular
    # Use request info if available
    try:
        ip = request.remote_addr if request else None
        ua = request.user_agent.string if request and request.user_agent else None
    except RuntimeError:
        ip = None
        ua = None
    aud = Auditoria(
        usuario_id=usuario_id,
        accion=accion,
        modulo=modulo,
        detalle=detalle,
        avatar=avatar if avatar is not None else None,
        ip_address=ip,
        user_agent=ua
    )
    db.session.add(aud)
    db.session.commit()
    return aud

def on_avatar_actualizado(event: AvatarActualizado):
    # event.avatar contains filename, event.usuario_id
    # actor_id is who performed action (maybe same as usuario_id or admin)
    actor = event.actor_id or event.usuario_id
    # If handler is called for self-update, detalle = 'Foto de perfil actualizada'
    # If admin updating other user, we need to distinguish: actor != usuario_id
    # For simplicity, use same message as before but include actor
    if event.actor_id and event.actor_id != event.usuario_id:
        # admin case: need to fetch username? keep generic
        detalle = f'Foto de perfil actualizada (usuario {event.usuario_id})'
        _registrar_auditoria(actor, 'Actualización de perfil', 'Perfil', detalle, avatar=event.avatar)
    else:
        _registrar_auditoria(actor, 'Actualización de perfil', 'Perfil', 'Foto de perfil actualizada', avatar=event.avatar)

def on_avatar_eliminado(event: AvatarEliminado):
    actor = event.actor_id or event.usuario_id
    _registrar_auditoria(actor, 'Actualización de perfil', 'Perfil', 'Foto de perfil eliminada', avatar='')

def register(bus):
    bus.subscribe(AvatarActualizado, on_avatar_actualizado)
    bus.subscribe(AvatarEliminado, on_avatar_eliminado)
