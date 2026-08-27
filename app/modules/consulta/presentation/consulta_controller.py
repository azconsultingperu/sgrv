from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app.modules.registro.public import consultar_alumnos_paginado, get_alumno_or_404, get_visita_by_alumno, existe_dni, list_instituciones, list_carreras

consulta_bp = Blueprint('consulta', __name__, url_prefix='/consulta')

@consulta_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    # filtros desde query params
    filtros = {
        'dni': request.args.get('dni', '').strip(),
        'nombres': request.args.get('nombres', '').strip(),
        'apellidos': request.args.get('apellidos', '').strip(),
        'colegio': request.args.get('colegio', '').strip(),
        'distrito': request.args.get('distrito', '').strip(),
        'promotor': request.args.get('promotor', '').strip(),
        'fecha_desde': request.args.get('fecha_desde', '').strip(),
        'fecha_hasta': request.args.get('fecha_hasta', '').strip(),
        'sexo': request.args.get('sexo', '').strip(),
        'carrera_id': request.args.get('carrera_id', type=int),
        'edad_desde': request.args.get('edad_desde', type=int),
        'edad_hasta': request.args.get('edad_hasta', type=int),
    }
    # limpiar vacíos para no contaminar
    filtros = {k: v for k, v in filtros.items() if v not in ('', None)}

    page = request.args.get('page', 1, type=int)

    pagination = consultar_alumnos_paginado(page=page, per_page=20, filtros=filtros)
    alumnos = pagination.items
    colegios = list_instituciones()
    carreras = list_carreras()

    return render_template('consulta/index.html',
        alumnos=alumnos, pagination=pagination,
        colegios=colegios, carreras=carreras,
        search_params=request.args,
        search_params_without_page={k: v for k, v in request.args.items() if k != 'page'})

@consulta_bp.route('/detalle/<int:id>')
@login_required
def detalle(id):
    alumno = get_alumno_or_404(id)
    visita = get_visita_by_alumno(alumno.id)
    return render_template('consulta/detalle.html', alumno=alumno, visita=visita)

@consulta_bp.route('/verificar-dni')
@login_required
def verificar_dni():
    dni = request.args.get('dni', '').strip()
    existe = existe_dni(dni)
    return jsonify({'existe': existe})
