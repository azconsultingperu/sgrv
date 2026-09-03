# -*- coding: utf-8 -*-
from app.shared.db import db
from flask_login import UserMixin
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for
import hashlib
from app.shared.time_utils import peru_now

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    __table_args__ = (
        db.Index('uq_usuarios_dni_activo', 'dni', unique=True,
                 postgresql_where=db.text('eliminado = false'),
                 sqlite_where=db.text('eliminado = 0')),
        db.Index('uq_usuarios_username_activo', 'username', unique=True,
                 postgresql_where=db.text('eliminado = false'),
                 sqlite_where=db.text('eliminado = 0')),
        db.Index('uq_usuarios_email_activo', 'email', unique=True,
                 postgresql_where=db.text('eliminado = false'),
                 sqlite_where=db.text('eliminado = 0')),
    )

    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.String(8), nullable=False, index=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    estado = db.Column(db.Boolean, default=True)
    ultimo_acceso = db.Column(db.DateTime)
    intentos_fallidos = db.Column(db.Integer, default=0)
    bloqueado_hasta = db.Column(db.DateTime, nullable=True)
    creado_en = db.Column(db.DateTime, default=peru_now)
    actualizado_en = db.Column(db.DateTime, default=peru_now, onupdate=peru_now)
    debe_cambiar_password = db.Column(db.Boolean, default=False)
    avatar = db.Column(db.String(255), nullable=True)
    eliminado = db.Column(db.Boolean, default=False)

    rol = db.relationship('Rol', backref='usuarios')
    auditorias = db.relationship('Auditoria', backref='usuario', lazy='dynamic')

    AVATAR_COLORS = ['#2d8a4e', '#1a6d8a', '#8a5a1a', '#8a1a2a', '#5a1a8a', '#1a4a8a']
    DEFAULT_AVATAR = 'img/avatar-default.svg'

    def has_permission(self, permiso):
        if self.rol_id == 1:
            return True
        return False

    def iniciales(self):
        nombres = (self.nombres or '').split()
        apellidos = (self.apellidos or '').split()
        letras = (nombres[0][0] if nombres else '') + (apellidos[0][0] if apellidos else '')
        return letras.upper() or self.username[:2].upper()

    def avatar_color(self):
        base = f'{self.nombres} {self.apellidos} {self.username}'.strip() or self.username
        idx = int(hashlib.md5(base.encode()).hexdigest(), 16) % len(self.AVATAR_COLORS)
        return self.AVATAR_COLORS[idx]

    def tiene_avatar(self):
        return bool(self.avatar)

    def avatar_url(self, thumb=False):
        if self.avatar:
            if thumb:
                return url_for('perfil.servir_avatar', usuario_id=self.id, t=1)
            return url_for('perfil.servir_avatar', usuario_id=self.id)
        return url_for('static', filename=self.DEFAULT_AVATAR)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_bloqueado(self):
        if self.bloqueado_hasta and self.bloqueado_hasta > peru_now():
            return True
        return False

    def incrementar_intentos(self):
        self.intentos_fallidos += 1
        if self.intentos_fallidos >= 5:
            self.bloqueado_hasta = peru_now() + timedelta(minutes=30)
        db.session.commit()

    def resetear_intentos(self):
        self.intentos_fallidos = 0
        self.bloqueado_hasta = None
        db.session.commit()

    def __repr__(self):
        return f'<Usuario {self.username}>'
