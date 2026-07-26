from app import db
from datetime import datetime

class Carrera(db.Model):
    __tablename__ = 'carreras'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), unique=True, nullable=False)
    area_profesional = db.Column(db.String(100), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Carrera {self.nombre}>'
