from app.models.auditoria import Auditoria
from app import db
from flask import request

def registrar_auditoria(usuario_id, accion, modulo, detalle=None):
    auditoria = Auditoria(
        usuario_id=usuario_id,
        accion=accion,
        modulo=modulo,
        detalle=detalle,
        ip_address=request.remote_addr if request else None,
        user_agent=request.user_agent.string if request and request.user_agent else None
    )
    db.session.add(auditoria)
    db.session.commit()
    return auditoria
