from app.models.alumno import Alumno
from app.models.visita import Visita
from app.models.institucion_educativa import InstitucionEducativa
from app.models.promotor import Promotor
from app.models.usuario import Usuario
from app.models.carrera import Carrera
from app import db
from datetime import datetime, timedelta, date
from sqlalchemy import func, extract

class EstadisticaService:

    @staticmethod
    def get_totales():
        return {
            'total_registros': Visita.query.count(),
            'total_colegios': InstitucionEducativa.query.count(),
            'total_promotores': Promotor.query.count(),
            'total_alumnos': Alumno.query.count(),
            'total_usuarios': Usuario.query.count()
        }

    @staticmethod
    def get_alumnos_por_colegio():
        results = db.session.query(
            InstitucionEducativa.nombre,
            func.count(Alumno.id)
        ).join(Alumno, Alumno.institucion_id == InstitucionEducativa.id)\
         .group_by(InstitucionEducativa.nombre).all()
        return [{'colegio': r[0], 'total': r[1]} for r in results]

    @staticmethod
    def get_alumnos_por_distrito():
        results = db.session.query(
            InstitucionEducativa.distrito,
            func.count(Alumno.id)
        ).join(Alumno, Alumno.institucion_id == InstitucionEducativa.id)\
         .group_by(InstitucionEducativa.distrito).all()
        return [{'distrito': r[0], 'total': r[1]} for r in results]

    @staticmethod
    def get_edad_promedio():
        result = db.session.query(func.avg(Alumno.edad)).scalar()
        return round(result, 1) if result else 0

    @staticmethod
    def get_alumnos_por_sexo():
        results = db.session.query(Alumno.sexo, func.count(Alumno.id)).group_by(Alumno.sexo).all()
        return [{'sexo': r[0], 'total': r[1]} for r in results]

    @staticmethod
    def get_registros_por_mes():
        results = db.session.query(
            extract('year', Visita.fecha_visita).label('anio'),
            extract('month', Visita.fecha_visita).label('mes'),
            func.count(Visita.id)
        ).group_by('anio', 'mes').order_by('anio', 'mes').all()
        return [{'anio': int(r[0]), 'mes': int(r[1]), 'total': r[2]} for r in results]

    @staticmethod
    def get_registros_dia():
        return Visita.query.filter(Visita.fecha_visita == date.today()).count()

    @staticmethod
    def get_registros_semana():
        inicio_semana = date.today() - timedelta(days=date.today().weekday())
        return Visita.query.filter(Visita.fecha_visita >= inicio_semana).count()

    @staticmethod
    def get_registros_mes():
        return Visita.query.filter(
            extract('month', Visita.fecha_visita) == date.today().month,
            extract('year', Visita.fecha_visita) == date.today().year
        ).count()

    @staticmethod
    def get_ranking_colegios():
        results = db.session.query(
            InstitucionEducativa.nombre,
            func.count(Visita.id).label('total')
        ).join(Alumno, Visita.alumno_id == Alumno.id)\
         .join(InstitucionEducativa, Alumno.institucion_id == InstitucionEducativa.id)\
         .group_by(InstitucionEducativa.nombre)\
         .order_by(func.count(Visita.id).desc()).limit(10).all()
        return [{'colegio': r[0], 'total': r[1]} for r in results]

    @staticmethod
    def get_proyeccion_postulantes():
        total_alumnos = Alumno.query.count()
        interesados = Alumno.query.filter_by(desea_estudiar=True).count()
        if total_alumnos > 0:
            tasa_conversion = (interesados / total_alumnos) * 100
        else:
            tasa_conversion = 0
        return {
            'total_alumnos': total_alumnos,
            'interesados': interesados,
            'tasa_conversion': round(tasa_conversion, 2),
            'proyeccion': round(total_alumnos * (tasa_conversion / 100) * 1.1, 0)
        }

    @staticmethod
    def get_carreras_mas_solicitadas():
        results = db.session.query(
            Carrera.nombre,
            func.count(Alumno.id)
        ).join(Alumno, Alumno.carrera_id == Carrera.id)\
         .group_by(Carrera.nombre)\
         .order_by(func.count(Alumno.id).desc()).all()
        return [{'carrera': r[0], 'total': r[1]} for r in results]
