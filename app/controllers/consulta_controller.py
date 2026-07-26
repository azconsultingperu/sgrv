from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_required, current_user
from app.models.alumno import Alumno
from app.models.visita import Visita
from app.models.institucion_educativa import InstitucionEducativa
from app.models.promotor import Promotor
from app.models.carrera import Carrera
from app.services.auditoria_service import registrar_auditoria
from app import db
from datetime import datetime

consulta_bp = Blueprint('consulta', __name__, url_prefix='/consulta')

@consulta_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    query = Alumno.query

    dni = request.args.get('dni', '').strip()
    nombres = request.args.get('nombres', '').strip()
    apellidos = request.args.get('apellidos', '').strip()
    colegio = request.args.get('colegio', '').strip()
    distrito = request.args.get('distrito', '').strip()
    promotor = request.args.get('promotor', '').strip()
    fecha_desde = request.args.get('fecha_desde', '').strip()
    fecha_hasta = request.args.get('fecha_hasta', '').strip()
    sexo = request.args.get('sexo', '').strip()
    carrera_id = request.args.get('carrera_id', type=int)
    edad_desde = request.args.get('edad_desde', type=int)
    edad_hasta = request.args.get('edad_hasta', type=int)

    page = request.args.get('page', 1, type=int)

    if dni:
        query = query.filter(Alumno.dni.like(f'%{dni}%'))
    if nombres:
        query = query.filter(Alumno.nombres.like(f'%{nombres}%'))
    if apellidos:
        query = query.filter(Alumno.apellidos.like(f'%{apellidos}%'))
    if colegio:
        query = query.join(InstitucionEducativa).filter(InstitucionEducativa.nombre.like(f'%{colegio}%'))
    if distrito:
        query = query.join(InstitucionEducativa).filter(InstitucionEducativa.distrito.like(f'%{distrito}%'))
    if sexo:
        query = query.filter(Alumno.sexo == sexo)
    if carrera_id:
        query = query.filter(Alumno.carrera_id == carrera_id)
    if edad_desde:
        query = query.filter(Alumno.edad >= edad_desde)
    if edad_hasta:
        query = query.filter(Alumno.edad <= edad_hasta)

    if promotor:
        query = query.join(Visita).join(Promotor).filter(
            db.or_(
                Promotor.nombres.like(f'%{promotor}%'),
                Promotor.apellidos.like(f'%{promotor}%')
            )
        )

    if fecha_desde:
        query = query.join(Visita).filter(Visita.fecha_visita >= datetime.strptime(fecha_desde, '%Y-%m-%d').date())
    if fecha_hasta:
        query = query.join(Visita).filter(Visita.fecha_visita <= datetime.strptime(fecha_hasta, '%Y-%m-%d').date())

    query = query.order_by(Alumno.fecha_registro.desc())
    pagination = query.paginate(page=page, per_page=20, error_out=False)
    alumnos = pagination.items
    colegios = InstitucionEducativa.query.all()
    carreras = Carrera.query.all()

    return render_template('consulta/index.html',
        alumnos=alumnos, pagination=pagination,
        colegios=colegios, carreras=carreras,
        search_params=request.args)

@consulta_bp.route('/detalle/<int:id>')
@login_required
def detalle(id):
    alumno = Alumno.query.get_or_404(id)
    visita = Visita.query.filter_by(alumno_id=alumno.id).first()
    return render_template('consulta/detalle.html', alumno=alumno, visita=visita)

@consulta_bp.route('/verificar-dni')
@login_required
def verificar_dni():
    dni = request.args.get('dni', '').strip()
    existe = Alumno.query.filter_by(dni=dni).first() is not None
    return jsonify({'existe': existe})
