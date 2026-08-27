# -*- coding: utf-8 -*-
"""Facade pública del módulo identidad - único punto de acoplamiento cross-módulo."""
from app.modules.identidad.domain.usuario import Usuario
from app.modules.identidad.domain.rol import Rol
from app.modules.identidad.domain.sesion import Sesion
from app.modules.identidad.infrastructure.usuario_repository import UsuarioRepository

_repo = UsuarioRepository()

def get_usuario(usuario_id: int):
    return _repo.find_by_id(usuario_id)

def get_usuario_by_dni(dni: str):
    return _repo.find_by_dni(dni)

def get_usuario_by_username(username: str):
    return _repo.find_by_username(username)

def list_usuarios_activos():
    return _repo.list_active()

def crear_usuario(*args, **kwargs):
    # delega a application si existe, sino directo
    u = Usuario(*args, **kwargs)
    return _repo.save(u)

def get_rol(rol_id: int):
    return Rol.query.get(rol_id)

def count_usuarios():
    return Usuario.query.count()
