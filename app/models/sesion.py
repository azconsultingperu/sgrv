from app import db
from app.utils.time_utils import peru_now

class Sesion(db.Model):
    __tablename__ = 'sesiones'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    token = db.Column(db.String(256), unique=True, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(200), nullable=True)
    inicio = db.Column(db.DateTime, default=peru_now)
    fin = db.Column(db.DateTime, nullable=True)
    activa = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Sesion Usuario {self.usuario_id} - {self.inicio}>'
