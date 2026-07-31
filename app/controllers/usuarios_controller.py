import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.services.auditoria_service import registrar_auditoria
from app.services.email_service import notificar_nuevo_usuario
from app import db
from app.utils.decorators import admin_required
from app.utils.helpers import validar_fortaleza_password, sanitizar_input

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@usuarios_bp.route('/')
@login_required
@admin_required
def index():
    usuarios = Usuario.query.all()
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

        registrar_auditoria(current_user.id, 'Creación de usuario', 'Usuarios',
            f'Usuario creado: {username} ({dni})')
        try:
            notificar_nuevo_usuario(usuario, password)
        except Exception as e:
            print(f'Error al enviar notificación: {e}')
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
            registrar_auditoria(current_user.id, 'Cambio de contraseña', 'Usuarios',
                f'Contraseña cambiada para: {usuario.username}')

        db.session.commit()
        registrar_auditoria(current_user.id, 'Edición de usuario', 'Usuarios',
            f'Usuario editado: {usuario.username}')
        flash('Usuario actualizado exitosamente.', 'success')
        return redirect(url_for('usuarios.index'))

    return render_template('usuarios/editar.html', usuario=usuario, roles=roles)

@usuarios_bp.route('/eliminar/<int:id>')
@login_required
@admin_required
def eliminar(id):
    usuario = Usuario.query.get_or_404(id)
    if usuario.id == current_user.id:
        flash('No puede eliminarse a sí mismo.', 'danger')
        return redirect(url_for('usuarios.index'))
    username = usuario.username
    db.session.delete(usuario)
    db.session.commit()
    registrar_auditoria(current_user.id, 'Eliminación de usuario', 'Usuarios',
        f'Usuario eliminado: {username}')
    flash('Usuario eliminado.', 'success')
    return redirect(url_for('usuarios.index'))

@usuarios_bp.route('/verificar-dni')
@login_required
def verificar_dni():
    dni = request.args.get('dni', '').strip()
    if not re.match(r'^\d{8}$', dni):
        return jsonify({'existe': False})
    existe = Usuario.query.filter_by(dni=dni).first() is not None
    return jsonify({'existe': existe})
