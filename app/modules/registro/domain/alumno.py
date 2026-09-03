import hashlib

from flask import url_for

from app.shared.db import db
from app.shared.time_utils import peru_now

class Alumno(db.Model):
    __tablename__ = 'alumnos'
    __table_args__ = (
        db.Index('uq_alumnos_dni_activo', 'dni', unique=True,
                 postgresql_where=db.text('eliminado = false'),
                 sqlite_where=db.text('eliminado = 0')),
    )

    id = db.Column(db.Integer, primary_key=True)
    apellidos = db.Column(db.String(100), nullable=False)
    nombres = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(8), nullable=False, index=True)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    sexo = db.Column(db.String(1), nullable=False)
    celular = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    direccion = db.Column(db.String(250), nullable=True)
    institucion_id = db.Column(db.Integer, db.ForeignKey('instituciones_educativas.id'), nullable=False, index=True)
    carrera_id = db.Column(db.Integer, db.ForeignKey('carreras.id'), nullable=True, index=True)
    area_interes = db.Column(db.String(100))
    desea_estudiar = db.Column(db.Boolean, default=False)
    solicita_info = db.Column(db.Boolean, default=False)
    modalidad_contacto = db.Column(db.String(50))
    fecha_registro = db.Column(db.DateTime, default=peru_now, index=True)
    actualizado_en = db.Column(db.DateTime, default=peru_now, onupdate=peru_now)
    activo = db.Column(db.Boolean, default=True)
    eliminado = db.Column(db.Boolean, default=False)
    fecha_eliminacion = db.Column(db.DateTime, nullable=True)
    foto = db.Column(db.String(255), nullable=True)

    institucion = db.relationship('InstitucionEducativa', backref='alumnos')
    carrera = db.relationship('Carrera', backref='alumnos')
    visitas = db.relationship('Visita', backref='alumno', lazy='dynamic')

    AVATAR_COLORS = ['#2d8a4e', '#1a6d8a', '#8a5a1a', '#8a1a2a', '#5a1a8a', '#1a4a8a']
    DEFAULT_FOTO = 'img/avatar-default.svg'

    def iniciales(self):
        nombres = (self.nombres or '').split()
        apellidos = (self.apellidos or '').split()
        letras = (nombres[0][0] if nombres else '') + (apellidos[0][0] if apellidos else '')
        return letras.upper() or (self.dni[:2].upper() if self.dni else 'AL')

    def foto_color(self):
        base = f'{self.nombres} {self.apellidos} {self.dni}'.strip() or self.dni or 'alumno'
        idx = int(hashlib.md5(base.encode()).hexdigest(), 16) % len(self.AVATAR_COLORS)
        return self.AVATAR_COLORS[idx]

    def tiene_foto(self):
        return bool(self.foto)

    def foto_url(self, thumb=False):
        if self.foto:
            if thumb:
                return url_for('registro.servir_foto', alumno_id=self.id, t=1)
            return url_for('registro.servir_foto', alumno_id=self.id)
        return url_for('static', filename=self.DEFAULT_FOTO)

    def __repr__(self):
        return f'<Alumno {self.dni} - {self.nombres} {self.apellidos}>'