from app import db
from app.utils.time_utils import peru_now

class Rol(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.String(200))
    creado_en = db.Column(db.DateTime, default=peru_now)

    def __repr__(self):
        return f'<Rol {self.nombre}>'
