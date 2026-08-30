# -*- coding: utf-8 -*-
"""Facade pública del módulo registro - único punto de acoplamiento cross-módulo."""
from datetime import datetime
from app.shared.db import db
from app.modules.registro.domain.alumno import Alumno
from app.modules.registro.domain.visita import Visita
from app.modules.registro.domain.institucion_educativa import InstitucionEducativa
from app.modules.registro.domain.promotor import Promotor
from app.modules.registro.domain.carrera import Carrera

def get_alumno(alumno_id: int):
    return Alumno.query.filter_by(id=alumno_id, eliminado=False).first()

def get_alumno_or_404(alumno_id: int):
    return Alumno.query.filter_by(id=alumno_id, eliminado=False).first_or_404()

def get_visita_by_alumno(alumno_id: int):
    return Visita.query.filter_by(alumno_id=alumno_id).first()

def existe_dni(dni: str) -> bool:
    return Alumno.query.filter_by(dni=dni).first() is not None

def buscar_alumnos(**filters):
    q = Alumno.query.filter_by(eliminado=False)
    if 'dni' in filters and filters['dni']:
        q = q.filter(Alumno.dni.like(f"%{filters['dni']}%"))
    return q

def list_alumnos_activos():
    return Alumno.query.filter_by(eliminado=False).all()

def list_instituciones():
    return InstitucionEducativa.query.all()

def list_carreras():
    return Carrera.query.all()

# ── Helpers para dashboard (expuestos vía public para evitar cross-import) ──
from sqlalchemy import func, extract
from app.shared.time_utils import peru_today
from datetime import timedelta as _td

def dashboard_get_totales():
    from app.modules.registro.domain.visita import Visita as _Visita
    from app.modules.registro.domain.institucion_educativa import InstitucionEducativa as _IE
    from app.modules.registro.domain.promotor import Promotor as _Prom
    # Excepción controlada public→public: registro necesita conteo de usuarios para dashboard.
    # Está permitido por diseño (public→public no está prohibido en setup.cfg); si el linter
    # lo bloqueara, mover la agregación a dashboard/application/estadistica_service.py.
    from app.modules.identidad.public import count_usuarios as _count_usuarios  # noqa: F401 - excepción public→public controlada
    return {
        'total_registros': _Visita.query.count(),
        'total_colegios': _IE.query.count(),
        'total_promotores': _Prom.query.count(),
        'total_alumnos': Alumno.query.filter_by(eliminado=False).count(),
        'total_usuarios': _count_usuarios()
    }

def dashboard_get_alumnos_por_colegio():
    from app.modules.registro.domain.institucion_educativa import InstitucionEducativa as _IE
    results = db.session.query(
        _IE.nombre, func.count(Alumno.id)
    ).join(Alumno, Alumno.institucion_id == _IE.id).filter(Alumno.eliminado == False).group_by(_IE.nombre).all()
    return [{'colegio': r[0], 'total': r[1]} for r in results]

def dashboard_get_alumnos_por_distrito():
    from app.modules.registro.domain.institucion_educativa import InstitucionEducativa as _IE
    results = db.session.query(_IE.distrito, func.count(Alumno.id)).join(Alumno, Alumno.institucion_id == _IE.id).filter(Alumno.eliminado == False).group_by(_IE.distrito).all()
    return [{'distrito': r[0], 'total': r[1]} for r in results]

def dashboard_get_edad_promedio():
    result = db.session.query(func.avg(Alumno.edad)).filter(Alumno.eliminado == False).scalar()
    return round(result, 1) if result else 0

def dashboard_get_alumnos_por_sexo():
    results = db.session.query(Alumno.sexo, func.count(Alumno.id)).filter(Alumno.eliminado == False).group_by(Alumno.sexo).all()
    return [{'sexo': r[0], 'total': r[1]} for r in results]

def dashboard_get_registros_por_mes():
    from app.modules.registro.domain.visita import Visita as _Visita
    results = db.session.query(extract('year', _Visita.fecha_visita).label('anio'), extract('month', _Visita.fecha_visita).label('mes'), func.count(_Visita.id)).group_by('anio', 'mes').order_by('anio', 'mes').all()
    return [{'anio': int(r[0]), 'mes': int(r[1]), 'total': r[2]} for r in results]

def dashboard_get_registros_dia():
    from app.modules.registro.domain.visita import Visita as _Visita
    return _Visita.query.filter(_Visita.fecha_visita == peru_today()).count()

def dashboard_get_registros_semana():
    from app.modules.registro.domain.visita import Visita as _Visita
    hoy = peru_today()
    inicio = hoy - _td(days=hoy.weekday())
    return _Visita.query.filter(_Visita.fecha_visita >= inicio).count()

def dashboard_get_registros_mes():
    from app.modules.registro.domain.visita import Visita as _Visita
    hoy = peru_today()
    return _Visita.query.filter(extract('month', _Visita.fecha_visita) == hoy.month, extract('year', _Visita.fecha_visita) == hoy.year).count()

def dashboard_get_ranking_colegios():
    from app.modules.registro.domain.visita import Visita as _Visita
    from app.modules.registro.domain.institucion_educativa import InstitucionEducativa as _IE
    results = db.session.query(_IE.nombre, func.count(_Visita.id).label('total')).join(Alumno, _Visita.alumno_id == Alumno.id).join(_IE, Alumno.institucion_id == _IE.id).group_by(_IE.nombre).order_by(func.count(_Visita.id).desc()).limit(10).all()
    return [{'colegio': r[0], 'total': r[1]} for r in results]

def dashboard_get_proyeccion_postulantes():
    total = Alumno.query.filter_by(eliminado=False).count()
    interesados = Alumno.query.filter_by(desea_estudiar=True, eliminado=False).count()
    tasa = (interesados / total * 100) if total else 0
    return {'total_alumnos': total, 'interesados': interesados, 'tasa_conversion': round(tasa,2), 'proyeccion': round(total * (tasa/100)*1.1,0)}

def dashboard_get_carreras_mas_solicitadas():
    results = db.session.query(Carrera.nombre, func.count(Alumno.id)).join(Alumno, Alumno.carrera_id == Carrera.id).group_by(Carrera.nombre).order_by(func.count(Alumno.id).desc()).all()
    return [{'carrera': r[0], 'total': r[1]} for r in results]

def consultar_alumnos_paginado(page=1, per_page=20, filtros=None):
    """
    Replica la lógica de consulta_controller para que consulta no importe domain.
    filtros: dict con dni, nombres, apellidos, colegio, distrito, sexo, carrera_id, edad_desde, edad_hasta, promotor, fecha_desde, fecha_hasta
    Retorna pagination object.
    """
    filtros = filtros or {}
    query = Alumno.query.options(
        db.joinedload(Alumno.institucion),
        db.joinedload(Alumno.carrera)
    ).filter_by(eliminado=False)

    dni = filtros.get('dni')
    nombres = filtros.get('nombres')
    apellidos = filtros.get('apellidos')
    colegio = filtros.get('colegio')
    distrito = filtros.get('distrito')
    sexo = filtros.get('sexo')
    carrera_id = filtros.get('carrera_id')
    edad_desde = filtros.get('edad_desde')
    edad_hasta = filtros.get('edad_hasta')
    promotor = filtros.get('promotor')
    fecha_desde = filtros.get('fecha_desde')
    fecha_hasta = filtros.get('fecha_hasta')

    if dni:
        query = query.filter(Alumno.dni.like(f'%{dni}%'))
    if nombres:
        query = query.filter(Alumno.nombres.like(f'%{nombres}%'))
    if apellidos:
        query = query.filter(Alumno.apellidos.like(f'%{apellidos}%'))
    if colegio:
        query = query.join(InstitucionEducativa).filter(InstitucionEducativa.nombre.like(f'%{colegio}%'))
    if distrito:
        # si ya se hizo join a Institucion por colegio, evitar duplicado: usar ya unido o re-join
        if not colegio:
            query = query.join(InstitucionEducativa)
        query = query.filter(InstitucionEducativa.distrito.like(f'%{distrito}%'))
    if sexo:
        query = query.filter(Alumno.sexo == sexo)
    if carrera_id:
        query = query.filter(Alumno.carrera_id == carrera_id)
    if edad_desde:
        query = query.filter(Alumno.edad >= edad_desde)
    if edad_hasta:
        query = query.filter(Alumno.edad <= edad_hasta)

    # fechas y promotor requieren join a Visita
    f_desde = None
    f_hasta = None
    if fecha_desde:
        try:
            f_desde = datetime.strptime(fecha_desde, '%Y-%m-%d').date()
        except ValueError:
            f_desde = None
    if fecha_hasta:
        try:
            f_hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
        except ValueError:
            f_hasta = None

    if promotor or f_desde or f_hasta:
        query = query.join(Visita, Visita.alumno_id == Alumno.id)
        if promotor:
            query = query.join(Promotor, Visita.promotor_id == Promotor.id).filter(
                db.or_(
                    Promotor.nombres.like(f'%{promotor}%'),
                    Promotor.apellidos.like(f'%{promotor}%')
                )
            )
        if f_desde:
            query = query.filter(Visita.fecha_visita >= f_desde)
        if f_hasta:
            query = query.filter(Visita.fecha_visita <= f_hasta)

    query = query.order_by(Alumno.fecha_registro.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination
