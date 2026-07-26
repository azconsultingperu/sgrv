from app import db
from datetime import datetime

class InstitucionEducativa(db.Model):
    __tablename__ = 'instituciones_educativas'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False, index=True)
    distrito = db.Column(db.String(100), nullable=False)
    provincia = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    codigo_modular = db.Column(db.String(20), unique=True, nullable=True)
    latitud = db.Column(db.Float, nullable=True)
    longitud = db.Column(db.Float, nullable=True)
    activo = db.Column(db.Boolean, default=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Institucion {self.nombre}>'
