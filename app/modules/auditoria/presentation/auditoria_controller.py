from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.modules.auditoria.domain.auditoria import Auditoria
from app.modules.identidad.domain.usuario import Usuario
from app.shared.db import db
from datetime import datetime
from app.utils.decorators import admin_required

auditoria_bp = Blueprint('auditoria', __name__, url_prefix='/auditoria')

@auditoria_bp.route('/')
@login_required
@admin_required
def index():
    query = Auditoria.query.options(db.joinedload(Auditoria.usuario))

    usuario_id = request.args.get('usuario_id', type=int)
    accion = request.args.get('accion', '').strip()
    modulo = request.args.get('modulo', '').strip()
    fecha_desde = request.args.get('fecha_desde', '').strip()
    fecha_hasta = request.args.get('fecha_hasta', '').strip()
    page = request.args.get('page', 1, type=int)

    if usuario_id:
        query = query.filter(Auditoria.usuario_id == usuario_id)
    if accion:
        query = query.filter(Auditoria.accion.like(f'%{accion}%'))
    if modulo:
        query = query.filter(Auditoria.modulo == modulo)
    try:
        f_desde = datetime.strptime(fecha_desde + ' 00:00:00', '%Y-%m-%d %H:%M:%S') if fecha_desde else None
        f_hasta = datetime.strptime(fecha_hasta + ' 23:59:59', '%Y-%m-%d %H:%M:%S') if fecha_hasta else None
    except ValueError:
        flash('Rango de fechas inválido. Use el formato AAAA-MM-DD.', 'danger')
        return redirect(url_for('auditoria.index'))
    if f_desde:
        query = query.filter(Auditoria.creado_en >= f_desde)
    if f_hasta:
        query = query.filter(Auditoria.creado_en <= f_hasta)

    query = query.order_by(Auditoria.creado_en.desc())
    pagination = query.paginate(page=page, per_page=30, error_out=False)
    auditorias = pagination.items
    usuarios = Usuario.query.all()

    return render_template('auditoria/index.html',
        auditorias=auditorias, pagination=pagination, usuarios=usuarios,
        search_params=request.args,
        search_params_without_page={k: v for k, v in request.args.items() if k != 'page'})
