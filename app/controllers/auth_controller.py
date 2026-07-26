from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models.usuario import Usuario
from app.models.sesion import Sesion
from app.services.auditoria_service import registrar_auditoria
from app import db
import secrets
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        dni = request.form.get('dni', '').strip()
        password = request.form.get('password', '')
        recordar = request.form.get('recordar')

        usuario = Usuario.query.filter_by(dni=dni).first()

        if not usuario:
            flash('DNI o contraseña incorrectos.', 'danger')
            return render_template('auth/login.html')

        if not usuario.estado:
            flash('Su cuenta está desactivada. Contacte al administrador.', 'danger')
            return render_template('auth/login.html')

        if usuario.is_bloqueado():
            flash('Cuenta bloqueada por múltiples intentos. Intente en 30 minutos.', 'danger')
            return render_template('auth/login.html')

        if usuario.check_password(password):
            usuario.resetear_intentos()
            usuario.ultimo_acceso = datetime.utcnow()
            session.permanent = True if recordar else False
            login_user(usuario, remember=bool(recordar))

            token = secrets.token_hex(32)
            sesion = Sesion(
                usuario_id=usuario.id,
                token=token,
                ip_address=request.remote_addr,
                user_agent=request.user_agent.string
            )
            db.session.add(sesion)
            db.session.commit()

            registrar_auditoria(usuario.id, 'Inicio de sesión', 'Auth', f'Inicio de sesión exitoso desde {request.remote_addr}')
            flash(f'Bienvenido {usuario.nombres} {usuario.apellidos}', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            usuario.incrementar_intentos()
            intentos_restantes = 5 - usuario.intentos_fallidos
            if intentos_restantes > 0:
                flash(f'Contraseña incorrecta. Le quedan {intentos_restantes} intentos.', 'danger')
            else:
                flash('Cuenta bloqueada por 30 minutos debido a múltiples intentos fallidos.', 'danger')
            return render_template('auth/login.html')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    registrar_auditoria(current_user.id, 'Cierre de sesión', 'Auth', 'Cierre de sesión')
    sesion_activa = Sesion.query.filter_by(usuario_id=current_user.id, activa=True).first()
    if sesion_activa:
        sesion_activa.activa = False
        sesion_activa.fin = datetime.utcnow()
        db.session.commit()
    logout_user()
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        dni = request.form.get('dni', '').strip()
        email = request.form.get('email', '').strip()
        usuario = Usuario.query.filter_by(dni=dni, email=email).first()
        if usuario:
            flash('Si los datos coinciden, recibirá instrucciones para recuperar su contraseña.', 'info')
        else:
            flash('No se encontró una cuenta con esos datos.', 'danger')
    return render_template('auth/recuperar.html')
