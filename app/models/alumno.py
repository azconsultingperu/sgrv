from app import db
from app.utils.time_utils import peru_now

class Alumno(db.Model):
    __tablename__ = 'alumnos'

    id = db.Column(db.Integer, primary_key=True)
    apellidos = db.Column(db.String(100), nullable=False)
    nombres = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(8), unique=True, nullable=False, index=True)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    sexo = db.Column(db.String(1), nullable=False)
    celular = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    direccion = db.Column(db.String(250), nullable=True)
    institucion_id = db.Column(db.Integer, db.ForeignKey('instituciones_educativas.id'), nullable=False)
    carrera_id = db.Column(db.Integer, db.ForeignKey('carreras.id'), nullable=True)
    area_interes = db.Column(db.String(100))
    desea_estudiar = db.Column(db.Boolean, default=False)
    solicita_info = db.Column(db.Boolean, default=False)
    modalidad_contacto = db.Column(db.String(50))
    fecha_registro = db.Column(db.DateTime, default=peru_now)
    actualizado_en = db.Column(db.DateTime, default=peru_now, onupdate=peru_now)
    activo = db.Column(db.Boolean, default=True)

    institucion = db.relationship('InstitucionEducativa', backref='alumnos')
    carrera = db.relationship('Carrera', backref='alumnos')
    visitas = db.relationship('Visita', backref='alumno', lazy='dynamic')

    def __repr__(self):
        return f'<Alumno {self.dni} - {self.nombres} {self.apellidos}>'
