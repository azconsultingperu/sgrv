from app import db
from app.utils.time_utils import peru_now

class Auditoria(db.Model):
    __tablename__ = 'auditorias'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False, index=True)
    accion = db.Column(db.String(100), nullable=False)
    modulo = db.Column(db.String(50), nullable=False)
    detalle = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(200), nullable=True)
    creado_en = db.Column(db.DateTime, default=peru_now, index=True)

    def __repr__(self):
        return f'<Auditoria {self.accion} - {self.creado_en}>'
