# -*- coding: utf-8 -*-
from app.shared.db import db
from app.shared.time_utils import peru_now


class PasswordResetToken(db.Model):
    __tablename__ = 'password_reset_tokens'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False, index=True)
    token_hash = db.Column(db.String(128), nullable=False, index=True)
    expires_at = db.Column(db.DateTime, nullable=False)
    used_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=peru_now, index=True)

    usuario = db.relationship('Usuario', backref='reset_tokens')

    def is_expired(self):
        return peru_now() > self.expires_at

    def is_used(self):
        return self.used_at is not None

    def __repr__(self):
        return f'<PasswordResetToken usuario={self.usuario_id} used={self.is_used()}>'


class PasswordResetAttempt(db.Model):
    __tablename__ = 'password_reset_attempts'

    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(45), nullable=True, index=True)
    username = db.Column(db.String(50), nullable=True, index=True)
    created_at = db.Column(db.DateTime, default=peru_now, index=True)

    def __repr__(self):
        return f'<PasswordResetAttempt ip={self.ip_address} user={self.username} at={self.created_at}>'
