# -*- coding: utf-8 -*-
from app.shared.db import db
from app.modules.registro.domain.alumno import Alumno
from app.modules.registro.domain.visita import Visita

class AlumnoRepository:
    def find_by_dni(self, dni: str):
        return Alumno.query.filter_by(dni=dni).first()

    def find_by_id(self, alumno_id: int):
        return Alumno.query.get(alumno_id)

    def find_active(self, alumno_id: int):
        return Alumno.query.filter_by(id=alumno_id, eliminado=False).first()

    def list_active(self):
        return Alumno.query.filter_by(eliminado=False).all()

    def list_with_includes(self):
        return Alumno.query.options(
            db.joinedload(Alumno.institucion),
            db.joinedload(Alumno.carrera)
        ).filter_by(eliminado=False)

    def save(self, alumno: Alumno):
        db.session.add(alumno)
        return alumno

class VisitaRepository:
    def save(self, visita: Visita):
        db.session.add(visita)
        return visita

    def find_by_alumno(self, alumno_id: int):
        return Visita.query.filter_by(alumno_id=alumno_id).first()

    def delete_by_alumno(self, alumno_id: int):
        Visita.query.filter_by(alumno_id=alumno_id).delete()
