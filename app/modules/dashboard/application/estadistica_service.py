# -*- coding: utf-8 -*-
"""Estadística del dashboard - delega a registro.public para evitar cross-import directo."""
from app.modules.registro import public as registro_public

class EstadisticaService:
    @staticmethod
    def get_totales():
        return registro_public.dashboard_get_totales()

    @staticmethod
    def get_alumnos_por_colegio():
        return registro_public.dashboard_get_alumnos_por_colegio()

    @staticmethod
    def get_alumnos_por_distrito():
        return registro_public.dashboard_get_alumnos_por_distrito()

    @staticmethod
    def get_edad_promedio():
        return registro_public.dashboard_get_edad_promedio()

    @staticmethod
    def get_alumnos_por_sexo():
        return registro_public.dashboard_get_alumnos_por_sexo()

    @staticmethod
    def get_registros_por_mes():
        return registro_public.dashboard_get_registros_por_mes()

    @staticmethod
    def get_registros_dia():
        return registro_public.dashboard_get_registros_dia()

    @staticmethod
    def get_registros_semana():
        return registro_public.dashboard_get_registros_semana()

    @staticmethod
    def get_registros_mes():
        return registro_public.dashboard_get_registros_mes()

    @staticmethod
    def get_ranking_colegios():
        return registro_public.dashboard_get_ranking_colegios()

    @staticmethod
    def get_proyeccion_postulantes():
        return registro_public.dashboard_get_proyeccion_postulantes()

    @staticmethod
    def get_carreras_mas_solicitadas():
        return registro_public.dashboard_get_carreras_mas_solicitadas()
