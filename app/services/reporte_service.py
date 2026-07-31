from app.models.alumno import Alumno
from app.models.visita import Visita
from app.models.institucion_educativa import InstitucionEducativa
from app.models.carrera import Carrera
from app.models.promotor import Promotor
from app import db
import io
import csv
from datetime import datetime

def generar_reporte_csv(tipo, params=None):
    output = io.StringIO()
    writer = csv.writer(output)
    if tipo == 'alumnos':
        writer.writerow(['DNI', 'Nombres', 'Apellidos', 'Edad', 'Sexo', 'Celular', 'Email', 'Institución', 'Carrera'])
        query = Alumno.query.join(InstitucionEducativa, Alumno.institucion_id == InstitucionEducativa.id).filter(Alumno.eliminado == False)
        for a in query:
            writer.writerow([a.dni, a.nombres, a.apellidos, a.edad, a.sexo, a.celular, a.email, a.institucion.nombre, a.carrera.nombre if a.carrera else ''])
    elif tipo == 'visitas':
        writer.writerow(['Fecha', 'Hora', 'Alumno', 'DNI', 'Colegio', 'Promotor'])
        query = Visita.query.join(Alumno).join(Promotor).filter(Alumno.eliminado == False)
        if params and params.get('fecha_desde'):
            query = query.filter(Visita.fecha_visita >= datetime.strptime(params['fecha_desde'], '%Y-%m-%d').date())
        if params and params.get('fecha_hasta'):
            query = query.filter(Visita.fecha_visita <= datetime.strptime(params['fecha_hasta'], '%Y-%m-%d').date())
        for v in query:
            writer.writerow([v.fecha_visita, v.hora_visita, f'{v.alumno.nombres} {v.alumno.apellidos}', v.alumno.dni, v.alumno.institucion.nombre, f'{v.promotor.nombres} {v.promotor.apellidos}'])
    elif tipo == 'colegios':
        writer.writerow(['Colegio', 'Distrito', 'Provincia', 'Región', 'Tipo', 'Total Alumnos'])
        for ie in InstitucionEducativa.query.all():
            total = Alumno.query.filter_by(institucion_id=ie.id, eliminado=False).count()
            writer.writerow([ie.nombre, ie.distrito, ie.provincia, ie.region, ie.tipo, total])
    elif tipo == 'carreras':
        writer.writerow(['Carrera', 'Área', 'Total Alumnos'])
        for c in Carrera.query.all():
            total = Alumno.query.filter_by(carrera_id=c.id, eliminado=False).count()
            writer.writerow([c.nombre, c.area_profesional, total])
    return output.getvalue()

def generar_reporte_excel(tipo, params=None):
    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = tipo.capitalize()
    if tipo == 'alumnos':
        ws.append(['DNI', 'Nombres', 'Apellidos', 'Edad', 'Sexo', 'Celular', 'Email', 'Institución', 'Carrera'])
        for a in Alumno.query.join(InstitucionEducativa).filter(Alumno.eliminado == False):
            ws.append([a.dni, a.nombres, a.apellidos, a.edad, a.sexo, a.celular, a.email, a.institucion.nombre, a.carrera.nombre if a.carrera else ''])
    elif tipo == 'visitas':
        ws.append(['Fecha', 'Hora', 'Alumno', 'DNI', 'Colegio', 'Promotor'])
        for v in Visita.query.join(Alumno).join(Promotor).filter(Alumno.eliminado == False):
            ws.append([str(v.fecha_visita), str(v.hora_visita), f'{v.alumno.nombres} {v.alumno.apellidos}', v.alumno.dni, v.alumno.institucion.nombre, f'{v.promotor.nombres} {v.promotor.apellidos}'])
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output
