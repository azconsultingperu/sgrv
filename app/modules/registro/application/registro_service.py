# -*- coding: utf-8 -*-
from datetime import datetime
from app.shared.unit_of_work import UnitOfWork
from app.shared.events import AlumnoRegistrado, AlumnoEliminado
from app.modules.registro.domain.alumno import Alumno
from app.modules.registro.domain.visita import Visita
from app.modules.registro.infrastructure.alumno_repository import AlumnoRepository, VisitaRepository
from app.shared.time_utils import peru_today, peru_now

def calcular_edad(fecha_nac):
    hoy = peru_today()
    return hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))

def crear_alumno_con_visita(datos: dict, actor_id: int):
    """
    Crea Alumno + Visita en una transacción atómica y publica AlumnoRegistrado solo en commit.
    datos espera claves: apellidos, nombres, dni, fecha_nacimiento (date), sexo, celular, email, direccion,
    institucion_id, carrera_id, area_interes, desea_estudiar, solicita_info, modalidad_contacto,
    fecha_visita (date), hora_visita (time), promotor_id, observaciones
    """
    alum_repo = AlumnoRepository()
    visita_repo = VisitaRepository()
    with UnitOfWork() as uow:
        alumno = Alumno(
            apellidos=datos['apellidos'],
            nombres=datos['nombres'],
            dni=datos['dni'],
            fecha_nacimiento=datos['fecha_nacimiento'],
            edad=calcular_edad(datos['fecha_nacimiento']),
            sexo=datos['sexo'],
            celular=datos['celular'],
            email=datos.get('email'),
            direccion=datos.get('direccion'),
            institucion_id=datos['institucion_id'],
            carrera_id=datos.get('carrera_id'),
            area_interes=datos.get('area_interes'),
            desea_estudiar=datos.get('desea_estudiar', False),
            solicita_info=datos.get('solicita_info', False),
            modalidad_contacto=datos.get('modalidad_contacto')
        )
        alum_repo.save(alumno)
        # flush to get id
        from app.shared.db import db as _db
        _db.session.flush()

        visita = Visita(
            alumno_id=alumno.id,
            promotor_id=datos.get('promotor_id'),
            usuario_id=actor_id,
            fecha_visita=datos.get('fecha_visita') or peru_today(),
            hora_visita=datos.get('hora_visita') or peru_now().time(),
            observaciones=datos.get('observaciones')
        )
        visita_repo.save(visita)

        # publica evento dentro de UoW - se despachará solo en commit
        uow.publish(AlumnoRegistrado(
            alumno_id=alumno.id,
            dni=alumno.dni,
            nombres=alumno.nombres,
            apellidos=alumno.apellidos,
            actor_id=actor_id
        ))
        # commit despacha
    return alumno, visita
