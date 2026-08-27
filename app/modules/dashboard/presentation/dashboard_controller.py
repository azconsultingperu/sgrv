from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.modules.dashboard.application.estadistica_service import EstadisticaService

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def index():
    totales = EstadisticaService.get_totales()
    alumnos_por_colegio = EstadisticaService.get_alumnos_por_colegio()
    alumnos_por_distrito = EstadisticaService.get_alumnos_por_distrito()
    edad_promedio = EstadisticaService.get_edad_promedio()
    alumnos_por_sexo = EstadisticaService.get_alumnos_por_sexo()
    registros_por_mes = EstadisticaService.get_registros_por_mes()
    registros_dia = EstadisticaService.get_registros_dia()
    registros_semana = EstadisticaService.get_registros_semana()
    registros_mes = EstadisticaService.get_registros_mes()
    ranking_colegios = EstadisticaService.get_ranking_colegios()
    proyeccion = EstadisticaService.get_proyeccion_postulantes()
    carreras_solicitadas = EstadisticaService.get_carreras_mas_solicitadas()

    return render_template('dashboard/index.html',
        totales=totales,
        alumnos_por_colegio=alumnos_por_colegio,
        alumnos_por_distrito=alumnos_por_distrito,
        edad_promedio=edad_promedio,
        alumnos_por_sexo=alumnos_por_sexo,
        registros_por_mes=registros_por_mes,
        registros_dia=registros_dia,
        registros_semana=registros_semana,
        registros_mes=registros_mes,
        ranking_colegios=ranking_colegios,
        proyeccion=proyeccion,
        carreras_solicitadas=carreras_solicitadas
    )
