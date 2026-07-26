from app import db
from datetime import datetime

class Visita(db.Model):
    __tablename__ = 'visitas'

    id = db.Column(db.Integer, primary_key=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumnos.id'), nullable=False)
    promotor_id = db.Column(db.Integer, db.ForeignKey('promotores.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha_visita = db.Column(db.Date, nullable=False, index=True)
    hora_visita = db.Column(db.Time, nullable=False)
    observaciones = db.Column(db.Text, nullable=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Visita {self.id} - Alumno {self.alumno_id}>'
