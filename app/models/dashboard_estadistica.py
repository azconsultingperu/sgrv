from app import db
from datetime import datetime

class DashboardEstadistica(db.Model):
    __tablename__ = 'dashboard_estadisticas'

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False, index=True)
    clave = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<DashboardEstadistica {self.tipo} - {self.clave}>'
