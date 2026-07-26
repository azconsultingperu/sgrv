from app import db
from datetime import datetime

class Reporte(db.Model):
    __tablename__ = 'reportes'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    formato = db.Column(db.String(10), nullable=False)
    parametros = db.Column(db.Text, nullable=True)
    archivo_generado = db.Column(db.String(200), nullable=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Reporte {self.titulo} - {self.tipo}>'
