from flask import Blueprint, render_template, request, send_file, flash, Response, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app.modules.reportes.application.reporte_service import generar_reporte_csv, generar_reporte_excel
from functools import wraps
from app import db

def _auditar(usuario_id, accion, modulo, detalle=None):
    try:
        from app.modules.auditoria.domain.auditoria import Auditoria
        aud = Auditoria(usuario_id=usuario_id, accion=accion, modulo=modulo, detalle=detalle, ip_address=request.remote_addr if request else None, user_agent=request.user_agent.string if request and getattr(request, 'user_agent', None) else None)
        db.session.add(aud)
        db.session.commit()
        return aud
    except Exception:
        try:
            db.session.rollback()
        except Exception:
            pass
        return None

reportes_bp = Blueprint('reportes', __name__, url_prefix='/reportes')

TITULOS = {
    'alumnos': 'Lista de alumnos',
    'visitas': 'Registro de visitas',
    'colegios': 'Instituciones educativas',
    'carreras': 'Carreras y postulantes',
}

def supervisor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.rol_id not in (1, 2):
            flash('No tiene permisos para acceder a esta sección.', 'danger')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function

@reportes_bp.route('/')
@login_required
@supervisor_required
def index():
    return render_template('reportes/index.html')


@reportes_bp.route('/registrar', methods=['POST'])
@login_required
@supervisor_required
def registrar():
    """Registra la exportación en auditoría, solo tras descargar el archivo."""
    tipo = request.form.get('tipo', '')
    formato = request.form.get('formato', '').upper()
    if tipo not in TITULOS or formato not in ('CSV', 'EXCEL'):
        return jsonify({'ok': False}), 400
    _auditar(
        current_user.id,
        f'Exportación {formato}',
        'Reportes',
        f'Exportado {tipo}'
    )
    return jsonify({'ok': True})


def exportar_csv(tipo, filename):
    try:
        data = generar_reporte_csv(tipo, request.args)
    except ValueError as e:
        flash(str(e), 'danger')
        return redirect(url_for('reportes.index'))
    return Response(
        data,
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename={filename}'}
    )

def exportar_excel(tipo, filename):
    try:
        output = generar_reporte_excel(tipo, request.args)
    except ValueError as e:
        flash(str(e), 'danger')
        return redirect(url_for('reportes.index'))
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
