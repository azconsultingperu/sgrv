from app.shared.db import db
from app.shared.time_utils import peru_now

class Auditoria(db.Model):
    __tablename__ = 'auditorias'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False, index=True)
    accion = db.Column(db.String(100), nullable=False)
    modulo = db.Column(db.String(50), nullable=False)
    detalle = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(200), nullable=True)
    avatar = db.Column(db.String(255), nullable=True)
    creado_en = db.Column(db.DateTime, default=peru_now, index=True)

    def avatar_url(self, thumb=False):
        from flask import url_for
        _default = 'img/avatar-default.svg'
        if self.avatar == '':
            return url_for('static', filename=_default)
        if self.avatar:
            if thumb and not self.avatar.endswith('_min.webp'):
                nombre = self.avatar[:-5] + '_min' + self.avatar[-5:]
            else:
                nombre = self.avatar
            return url_for('perfil.servir_avatar_archivo', nombre=nombre)
        if self.usuario:
            return self.usuario.avatar_url(thumb)
        return url_for('static', filename=_default)

    def __repr__(self):
        return f'<Auditoria {self.accion} - {self.creado_en}>'
