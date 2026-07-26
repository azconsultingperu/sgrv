from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.models.usuario import Usuario
from app.models.sesion import Sesion
from app.services.auditoria_service import registrar_auditoria
from app.services.email_service import enviar_correo_recuperacion
from app import db
import secrets
from datetime import datetime, timedelta
from itsdangerous import URLSafeTimedSerializer

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def get_serializer():
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'], salt='password-reset')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        recordar = request.form.get('recordar')

        usuario = Usuario.query.filter_by(username=username).first()

        if not usuario:
            flash('Usuario o contraseÃ±a incorrectos.', 'danger')
            return render_template('auth/login.html')

        if not usuario.estado:
            flash('Su cuenta estÃ¡ desactivada. Contacte al administrador.', 'danger')
            return render_template('auth/login.html')

        if usuario.is_bloqueado():
            flash('Cuenta bloqueada por mÃºltiples intentos. Intente en 30 minutos.', 'danger')
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

            registrar_auditoria(usuario.id, 'Inicio de sesiÃ³n', 'Auth', f'Inicio de sesiÃ³n exitoso desde {request.remote_addr}')
            flash(f'Bienvenido {usuario.nombres} {usuario.apellidos}', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            usuario.incrementar_intentos()
            intentos_restantes = 5 - usuario.intentos_fallidos
            if intentos_restantes > 0:
                flash(f'ContraseÃ±a incorrecta. Le quedan {intentos_restantes} intentos.', 'danger')
            else:
                flash('Cuenta bloqueada por 30 minutos debido a mÃºltiples intentos fallidos.', 'danger')
            return render_template('auth/login.html')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    registrar_auditoria(current_user.id, 'Cierre de sesiÃ³n', 'Auth', 'Cierre de sesiÃ³n')
    sesion_activa = Sesion.query.filter_by(usuario_id=current_user.id, activa=True).first()
    if sesion_activa:
        sesion_activa.activa = False
        sesion_activa.fin = datetime.utcnow()
        db.session.commit()
    logout_user()
    flash('SesiÃ³n cerrada correctamente.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        usuario = Usuario.query.filter_by(username=username, email=email).first()

        if usuario:
            serializer = get_serializer()
            token = serializer.dumps(usuario.id)
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            try:
                enviar_correo_recuperacion(usuario, reset_url)
                registrar_auditoria(usuario.id, 'Solicitud de recuperaciÃ³n', 'Auth',
                    f'Correo de recuperaciÃ³n enviado a {email}')
                flash('Se han enviado las instrucciones a su correo electrÃ³nico.', 'success')
            except Exception as e:
                flash('Error al enviar el correo. Intente mÃ¡s tarde.', 'danger')
        else:
            flash('No se encontrÃ³ una cuenta con esos datos.', 'danger')

    return render_template('auth/recuperar.html')

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        serializer = get_serializer()
        usuario_id = serializer.loads(token, max_age=3600)
    except:
        flash('El enlace de recuperaciÃ³n es invÃ¡lido o ha expirado.', 'danger')
        return redirect(url_for('auth.login'))

    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        flash('Usuario no encontrado.', 'danger')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        if not password or len(password) < 6:
            flash('La contraseÃ±a debe tener al menos 6 caracteres.', 'danger')
            return render_template('auth/reset_password.html', token=token)

        if password != confirm:
            flash('Las contraseÃ±as no coinciden.', 'danger')
            return render_template('auth/reset_password.html', token=token)

        usuario.set_password(password)
        db.session.commit()
        registrar_auditoria(usuario.id, 'Cambio de contraseÃ±a', 'Auth',
            'ContraseÃ±a restablecida mediante recuperaciÃ³n')
        flash('ContraseÃ±a restablecida exitosamente. Ya puedes iniciar sesiÃ³n.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', token=token)
