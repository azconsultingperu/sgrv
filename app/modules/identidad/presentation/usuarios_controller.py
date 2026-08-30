import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.modules.identidad.domain.usuario import Usuario
from app.modules.identidad.domain.rol import Rol
from app.shared.events import publish, UsuarioCreado, UsuarioEliminado
from app import db
from app.utils.decorators import admin_required
from app.utils.helpers import validar_fortaleza_password, sanitizar_input

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@usuarios_bp.route('/')
@login_required
@admin_required
def index():
    usuarios = Usuario.query.options(db.joinedload(Usuario.rol)).filter_by(eliminado=False).all()
    roles = Rol.query.all()
    return render_template('usuarios/index.html', usuarios=usuarios, roles=roles)

@usuarios_bp.route('/crear', methods=['GET', 'POST'])
@login_required
@admin_required
def crear():
    roles = Rol.query.all()
    if request.method == 'POST':
        dni = request.form.get('dni', '').strip()
        nombres = request.form.get('nombres', '').strip().upper()
        apellidos = request.form.get('apellidos', '').strip().upper()
        username = dni
        password = request.form.get('password', '')
        email = request.form.get('email', '').strip()
        rol_id = request.form.get('rol_id', type=int)

        if not re.match(r'^\d{8}$', dni):
            flash('El DNI debe tener exactamente 8 dígitos numéricos.', 'danger')
            return render_template('usuarios/crear.html', roles=roles, form=request.form)

        if Usuario.query.filter_by(dni=dni).first():
            flash('El DNI ya está registrado.', 'danger')
            return render_template('usuarios/crear.html', roles=roles, form=request.form)

        if Usuario.query.filter_by(username=dni).first():
            flash('El DNI ya está registrado como usuario.', 'danger')
            return render_template('usuarios/crear.html', roles=roles, form=request.form)

        if not email or not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            flash('El correo electrónico no es válido.', 'danger')
            return render_template('usuarios/crear.html', roles=roles, form=request.form)

        if Usuario.query.filter_by(email=email).first():
            flash('El correo electrónico ya está registrado.', 'danger')
            return render_template('usuarios/crear.html', roles=roles, form=request.form)

        usuario = Usuario(
            dni=dni, nombres=nombres, apellidos=apellidos,
            username=username, email=email, rol_id=rol_id
        )
        errores_password = validar_fortaleza_password(password)
        if errores_password:
            for e in errores_password:
                flash(e, 'danger')
            return render_template('usuarios/crear.html', roles=roles, form=request.form)
        usuario.set_password(password)
        db.session.add(usuario)
        db.session.commit()

        publish(UsuarioCreado(usuario_id=usuario.id, username=usuario.username, dni=usuario.dni, actor_id=current_user.id))
        flash('Usuario creado exitosamente.', 'success')
        return redirect(url_for('usuarios.index'))

    return render_template('usuarios/crear.html', roles=roles, form=request.form)

@usuarios_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar(id):
    usuario = Usuario.query.get_or_404(id)
    roles = Rol.query.all()
    if request.method == 'POST':
        usuario.nombres = request.form.get('nombres', '').strip().upper()
        usuario.apellidos = request.form.get('apellidos', '').strip().upper()
        usuario.rol_id = request.form.get('rol_id', type=int)
        usuario.estado = request.form.get('estado') == 'on'

        email = request.form.get('email', '').strip()
        if not email or not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            flash('El correo electrónico no es válido.', 'danger')
            return render_template('usuarios/editar.html', usuario=usuario, roles=roles)
        existe = Usuario.query.filter(Usuario.email == email, Usuario.id != usuario.id).first()
        if existe:
            flash('El correo electrónico ya está registrado por otro usuario.', 'danger')
            return render_template('usuarios/editar.html', usuario=usuario, roles=roles)
        usuario.email = email

        password = request.form.get('password', '')
        if password:
            errores_password = validar_fortaleza_password(password)
            if errores_password:
                for e in errores_password:
                    flash(e, 'danger')
                return render_template('usuarios/editar.html', usuario=usuario, roles=roles)
            usuario.set_password(password)
            # auditoría de cambio de contraseña vía evento si se desea; por ahora directa vía handler de avatar no aplica
            from app.modules.auditoria.domain.auditoria import Auditoria
            from flask import request as _req
            try:
                ip = _req.remote_addr if _req else None
                ua = _req.user_agent.string if _req and _req.user_agent else None
            except RuntimeError:
                ip = None
                ua = None
            db.session.flush()
            aud = Auditoria(usuario_id=current_user.id, accion='Cambio de contraseña', modulo='Usuarios', detalle=f'Contraseña cambiada para: {usuario.username}', ip_address=ip, user_agent=ua)
            db.session.add(aud)

        db.session.commit()
        # auditoría de edición - directa vía dominio (identidad puede importar auditoria sin violar registro→auditoria)
        from app.modules.auditoria.domain.auditoria import Auditoria as _Aud
        from flask import request as _rq
        try:
            ip2 = _rq.remote_addr if _rq else None
            ua2 = _rq.user_agent.string if _rq and _rq.user_agent else None
        except RuntimeError:
            ip2 = None
            ua2 = None
        aud2 = _Aud(usuario_id=current_user.id, accion='Edición de usuario', modulo='Usuarios', detalle=f'Usuario editado: {usuario.username}', ip_address=ip2, user_agent=ua2)
        db.session.add(aud2)
        db.session.commit()
        flash('Usuario actualizado exitosamente.', 'success')
        return redirect(url_for('usuarios.index'))

    return render_template('usuarios/editar.html', usuario=usuario, roles=roles)

@usuarios_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
@admin_required
def eliminar(id):
    usuario = Usuario.query.get_or_404(id)
    if usuario.id == current_user.id:
        flash('No puede eliminarse a sí mismo.', 'danger')
        return redirect(url_for('usuarios.index'))

    # Soft Delete
    nombre_completo = f'{usuario.nombres} {usuario.apellidos}'
    username = usuario.username
    usuario_id = usuario.id

    usuario.eliminado = True
    usuario.estado = False

    # Invalidate active sessions
    from app.modules.identidad.domain.sesion import Sesion
    from app.utils.time_utils import peru_now
    sesiones_activas = Sesion.query.filter_by(usuario_id=usuario.id, activa=True).all()
    for s in sesiones_activas:
        s.activa = False
        s.fin = peru_now()

    db.session.commit()
    publish(UsuarioEliminado(usuario_id=usuario_id, username=username, actor_id=current_user.id))
    flash(f'Usuario "{nombre_completo}" eliminado correctamente.', 'success')
    return redirect(url_for('usuarios.index'))

@usuarios_bp.route('/verificar-dni')
@login_required
def verificar_dni():
    dni = request.args.get('dni', '').strip()
    if not re.match(r'^\d{8}$', dni):
        return jsonify({'existe': False})
    existe = Usuario.query.filter_by(dni=dni).first() is not None
    return jsonify({'existe': existe})
