from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.time_utils import peru_now

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.String(8), unique=True, nullable=False, index=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    estado = db.Column(db.Boolean, default=True)
    ultimo_acceso = db.Column(db.DateTime)
    intentos_fallidos = db.Column(db.Integer, default=0)
    bloqueado_hasta = db.Column(db.DateTime, nullable=True)
    creado_en = db.Column(db.DateTime, default=peru_now)
    actualizado_en = db.Column(db.DateTime, default=peru_now, onupdate=peru_now)
    debe_cambiar_password = db.Column(db.Boolean, default=False)

    rol = db.relationship('Rol', backref='usuarios')
    auditorias = db.relationship('Auditoria', backref='usuario', lazy='dynamic')

    def has_permission(self, permiso):
        if self.rol_id == 1:
            return True
        return False

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
