# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.modules.identidad.domain.usuario import Usuario
from app.modules.identidad.domain.sesion import Sesion
from app.modules.identidad.domain.password_reset import PasswordResetToken, PasswordResetAttempt
from app.modules.notifications.infrastructure.email_adapter import enviar_correo_recuperacion
from app import db
from app.utils.time_utils import peru_now
from app.utils.helpers import validar_fortaleza_password, generar_password_segura, sanitizar_input
import secrets
import hashlib
import threading
from datetime import timedelta
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Constantes de recuperación (spec: password-recovery-hardening)
RECOVER_TTL_SECONDS = 900  # 15 minutos
RECOVER_RATE_LIMIT_MAX = 3
RECOVER_RATE_LIMIT_WINDOW_MINUTES = 15
RECOVER_GENERIC_MSG = 'Si los datos son correctos, recibirás un correo con las instrucciones'
RECOVER_THROTTLE_MSG = 'Has superado el límite de intentos. Intenta en 15 minutos.'

def _auditar(usuario_id, accion, modulo, detalle=None):
    """Helper local para auditoría sin importar app.services (evita ciclo)."""
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

def get_serializer():
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'], salt='password-reset')

def _hash_token(token):
    return hashlib.sha256(token.encode('utf-8')).hexdigest()

def _is_rate_limited(ip_address, username):
    window_start = peru_now() - timedelta(minutes=RECOVER_RATE_LIMIT_WINDOW_MINUTES)
    ip_count = 0
    user_count = 0
    try:
        if ip_address:
            ip_count = PasswordResetAttempt.query.filter(
                PasswordResetAttempt.ip_address == ip_address,
                PasswordResetAttempt.created_at > window_start
            ).count()
        if username:
            user_count = PasswordResetAttempt.query.filter(
                PasswordResetAttempt.username == username,
                PasswordResetAttempt.created_at > window_start
            ).count()
    except Exception:
        # Si falla la query de rate limit, no bloquear por seguridad (fail open para no DoS)
        return False
    return ip_count >= RECOVER_RATE_LIMIT_MAX or user_count >= RECOVER_RATE_LIMIT_MAX

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
            flash('Usuario o contraseña incorrectos.', 'danger')
            return render_template('auth/login.html')

        if not usuario.estado or usuario.eliminado:
            flash('Su cuenta está desactivada. Contacte al administrador.', 'danger')
            return render_template('auth/login.html')

        if usuario.is_bloqueado():
            flash('Cuenta bloqueada por múltiples intentos. Intente en 30 minutos.', 'danger')
            return render_template('auth/login.html')

        if usuario.check_password(password):
            usuario.resetear_intentos()
            usuario.ultimo_acceso = peru_now()
            session.clear()
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

            _auditar(usuario.id, 'Inicio de sesión', 'Auth', f'Inicio de sesión exitoso desde {request.remote_addr}')
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
    _auditar(current_user.id, 'Cierre de sesión', 'Auth', 'Cierre de sesión')
    sesion_activa = Sesion.query.filter_by(usuario_id=current_user.id, activa=True).first()
    if sesion_activa:
        sesion_activa.activa = False
        sesion_activa.fin = peru_now()
        db.session.commit()
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        ip = request.remote_addr

        # Rate limit 3/15min por IP y por DNI (username) — desactivable solo en dev/testing
        if not current_app.config.get('DISABLE_RATE_LIMIT') and _is_rate_limited(ip, username):
            # Registrar intento throttled para mantener ventana deslizante
            try:
                att = PasswordResetAttempt(ip_address=ip, username=username)
                db.session.add(att)
                db.session.commit()
            except Exception:
                try:
                    db.session.rollback()
                except Exception:
                    pass
            # Para fetch (JS) devolver JSON sin flash para consumo único; para POST normal mantener flash
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return current_app.response_class(
                    response='{"status":"throttled","message":"Has superado el límite de intentos. Intenta en 15 minutos."}',
                    status=200, mimetype='application/json'
                )
            flash(RECOVER_THROTTLE_MSG, 'warning')
            return render_template('auth/recuperar.html')

        # Registrar intento (para todos, exista o no el usuario -> anti-enumeración)
        try:
            att = PasswordResetAttempt(ip_address=ip, username=username)
            db.session.add(att)
            db.session.commit()
        except Exception:
            try:
                db.session.rollback()
            except Exception:
                pass

        usuario = Usuario.query.filter_by(username=username, email=email, eliminado=False).first()

        if usuario:
            serializer = get_serializer()
            token = serializer.dumps(usuario.id)
            token_hash = _hash_token(token)
            expires_at = peru_now() + timedelta(seconds=RECOVER_TTL_SECONDS)
            try:
                prt = PasswordResetToken(usuario_id=usuario.id, token_hash=token_hash, expires_at=expires_at)
                db.session.add(prt)
                db.session.commit()
            except Exception:
                try:
                    db.session.rollback()
                except Exception:
                    pass
                # Si falla persistencia, igualmente responder genérico (no exponer error)
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return current_app.response_class(
                        response='{"status":"ok","message":"Si los datos son correctos, recibirás un correo con las instrucciones"}',
                        status=200, mimetype='application/json'
                    )
                flash(RECOVER_GENERIC_MSG, 'success')
                return render_template('auth/recuperar.html')

            reset_url = url_for('auth.reset_password', token=token, _external=True)
            # Enviar correo en segundo plano para respuesta inmediata (no bloquear el fetch)
            app = current_app._get_current_object()
            _uid, _email_copy, _reset_url_copy = usuario.id, email, reset_url
            def _send_async(app_obj, uid, email_addr, url):
                with app_obj.app_context():
                    try:
                        from app.modules.identidad.domain.usuario import Usuario as _U
                        _usr = _U.query.get(uid)
                        if not _usr:
                            return
                        ok = enviar_correo_recuperacion(_usr, url)
                        if ok:
                            _auditar(uid, 'Solicitud de recuperación', 'Auth',
                                f'Correo de recuperación enviado a {email_addr}')
                        else:
                            app_obj.logger.warning(f'Fallo SMTP silencioso (async) para recuperación usuario {uid} -> {email_addr}')
                    except Exception as _e:
                        try:
                            app_obj.logger.error(f'Error async en recuperar para {email_addr}: {_e}')
                        except Exception:
                            pass
            try:
                threading.Thread(target=_send_async, args=(app, _uid, _email_copy, _reset_url_copy), daemon=True).start()
            except Exception as _e:
                current_app.logger.error(f'No se pudo lanzar hilo async de correo: {_e}')
            # No hacer flash distinto si falla SMTP -> genérico igual (la respuesta ya no espera al correo)

        # Respuesta siempre genérica (exista o no) — para fetch devolver JSON sin flash
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return current_app.response_class(
                response='{"status":"ok","message":"Si los datos son correctos, recibirás un correo con las instrucciones"}',
                status=200, mimetype='application/json'
            )
        flash(RECOVER_GENERIC_MSG, 'success')

    return render_template('auth/recuperar.html')

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        serializer = get_serializer()
        usuario_id = serializer.loads(token, max_age=RECOVER_TTL_SECONDS)
    except (BadSignature, SignatureExpired):
        flash('El enlace de recuperación es inválido o ha expirado.', 'danger')
        return redirect(url_for('auth.login'))

    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        flash('Usuario no encontrado.', 'danger')
        return redirect(url_for('auth.login'))

    # Validar single-use: buscar token_hash en DB, no usado y no expirado
    token_hash = _hash_token(token)
    prt = PasswordResetToken.query.filter_by(token_hash=token_hash, usuario_id=usuario.id).first()
    if not prt:
        flash('El enlace de recuperación es inválido o ha expirado.', 'danger')
        return redirect(url_for('auth.login'))
    if prt.is_used():
        flash('El enlace de recuperación es inválido o ha expirado.', 'danger')
        return redirect(url_for('auth.login'))
    if prt.is_expired():
        flash('El enlace de recuperación es inválido o ha expirado.', 'danger')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        errores = validar_fortaleza_password(password)
        if errores:
            for e in errores:
                flash(e, 'danger')
            return render_template('auth/reset_password.html', token=token)

        if password != confirm:
            flash('Las contraseñas no coinciden.', 'danger')
            return render_template('auth/reset_password.html', token=token)

        usuario.set_password(password)
        usuario.debe_cambiar_password = False
        # Marcar token como usado en el mismo commit
        prt.used_at = peru_now()
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            flash('Error al restablecer la contraseña. Intente nuevamente.', 'danger')
            return render_template('auth/reset_password.html', token=token)
        _auditar(usuario.id, 'Cambio de contraseña', 'Auth',
            'Contraseña restablecida mediante recuperación')
        flash('Contraseña restablecida exitosamente. Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', token=token)
