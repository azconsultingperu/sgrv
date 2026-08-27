# -*- coding: utf-8 -*-
from app.modules.identidad.domain.usuario import Usuario
from app.shared.db import db

class UsuarioRepository:
    def find_by_dni(self, dni: str):
        return Usuario.query.filter_by(dni=dni).first()

    def find_by_id(self, usuario_id: int):
        return Usuario.query.get(usuario_id)

    def find_by_username(self, username: str):
        return Usuario.query.filter_by(username=username).first()

    def find_by_email(self, email: str):
        return Usuario.query.filter_by(email=email).first()

    def list_active(self):
        return Usuario.query.filter_by(eliminado=False).all()

    def save(self, usuario: Usuario):
        db.session.add(usuario)
        db.session.commit()
        return usuario
