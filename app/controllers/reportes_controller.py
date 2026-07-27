from flask import Blueprint, render_template, request, send_file, flash, Response
from flask_login import login_required, current_user
from app.services.reporte_service import generar_reporte_csv, generar_reporte_excel
from app.services.auditoria_service import registrar_auditoria
from app.models.reporte import Reporte
from app import db
from datetime import datetime
import io
import csv
from functools import wraps

reportes_bp = Blueprint('reportes', __name__, url_prefix='/reportes')

def supervisor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.rol_id not in (1, 2, 4):
            flash('No tiene permisos para acceder a esta sección.', 'danger')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function

@reportes_bp.route('/')
@login_required
@supervisor_required
def index():
    reportes = Reporte.query.order_by(Reporte.creado_en.desc()).limit(20).all()
    return render_template('reportes/index.html', reportes=reportes)

def exportar_csv(tipo, filename):
    data = generar_reporte_csv(tipo, request.args)
    registrar_auditoria(current_user.id, 'Exportación CSV', 'Reportes', f'Exportado {tipo}')
    return Response(
        data,
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename={filename}'}
    )

def exportar_excel(tipo, filename):
    output = generar_reporte_excel(tipo, request.args)
    registrar_auditoria(current_user.id, 'Exportación Excel', 'Reportes', f'Exportado {tipo}')
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=filename
    )

@reportes_bp.route('/alumnos/csv')
@login_required
@supervisor_required
def alumnos_csv():
    return exportar_csv('alumnos', 'alumnos.csv')

@reportes_bp.route('/alumnos/excel')
@login_required
@supervisor_required
def alumnos_excel():
    return exportar_excel('alumnos', 'alumnos.xlsx')

@reportes_bp.route('/visitas/csv')
@login_required
@supervisor_required
def visitas_csv():
    return exportar_csv('visitas', 'visitas.csv')

@reportes_bp.route('/visitas/excel')
@login_required
@supervisor_required
def visitas_excel():
    return exportar_excel('visitas', 'visitas.xlsx')

@reportes_bp.route('/colegios/csv')
@login_required
@supervisor_required
def colegios_csv():
    return exportar_csv('colegios', 'colegios.csv')

@reportes_bp.route('/colegios/excel')
@login_required
@supervisor_required
def colegios_excel():
    return exportar_excel('colegios', 'colegios.xlsx')

@reportes_bp.route('/carreras/csv')
@login_required
@supervisor_required
def carreras_csv():
    return exportar_csv('carreras', 'carreras.csv')

@reportes_bp.route('/carreras/excel')
@login_required
@supervisor_required
def carreras_excel():
    return exportar_excel('carreras', 'carreras.xlsx')
