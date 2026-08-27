from app.shared.db import db
from app.shared.time_utils import peru_now

class Promotor(db.Model):
    __tablename__ = 'promotores'

    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.String(8), unique=True, nullable=False)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    telefono = db.Column(db.String(15), nullable=True)
    activo = db.Column(db.Boolean, default=True)
    creado_en = db.Column(db.DateTime, default=peru_now)

    visitas = db.relationship('Visita', backref='promotor', lazy='dynamic')

    def __repr__(self):
        return f'<Promotor {self.nombres} {self.apellidos}>'
