from app.shared.db import db
from app.shared.time_utils import peru_now

class Visita(db.Model):
    __tablename__ = 'visitas'

    id = db.Column(db.Integer, primary_key=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumnos.id'), nullable=False)
    promotor_id = db.Column(db.Integer, db.ForeignKey('promotores.id'), nullable=True)
    # Promotor responsable de tipo Operador (usuario con rol Operador). A lo sumo
    # uno de (promotor_id, operador_promotor_id) debe estar seteado; ambos NULL
    # significa "sin promotor asignado". Se referencia por nombre de clase para
    # no importar identidad.domain (frontera modular: registro usa identidad.public).
    operador_promotor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    operador_promotor = db.relationship('Usuario', foreign_keys=[operador_promotor_id])
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha_visita = db.Column(db.Date, nullable=False, index=True)
    hora_visita = db.Column(db.Time, nullable=False)
    observaciones = db.Column(db.Text, nullable=True)
    creado_en = db.Column(db.DateTime, default=peru_now)
    actualizado_en = db.Column(db.DateTime, default=peru_now, onupdate=peru_now)

    def __repr__(self):
        return f'<Visita {self.id} - Alumno {self.alumno_id}>'

    @property
    def promotor_ref(self):
        """Referencia del select: 'operador:<id>', 'promotor:<id>' o ''."""
        if self.operador_promotor_id:
            return f'operador:{self.operador_promotor_id}'
        if self.promotor_id:
            return f'promotor:{self.promotor_id}'
        return ''

    @property
    def promotor_nombre(self):
        """Nombre del promotor responsable sea clásico u Operador; None si no hay.

        Resolución tolerante: si el Operador fue dado de baja, el objeto igual
        existe en BD (soft delete) y se muestra su nombre; nunca lanza."""
        try:
            if self.operador_promotor is not None:
                return f'{self.operador_promotor.nombres} {self.operador_promotor.apellidos}'.strip() or None
            if self.promotor is not None:
                return f'{self.promotor.nombres} {self.promotor.apellidos}'.strip() or None
        except Exception:
            return None
        return None
