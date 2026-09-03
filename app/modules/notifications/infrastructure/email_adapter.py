# -*- coding: utf-8 -*-
"""Adapter de email - infraestructura del módulo notifications.

Envuelve smtplib y Flask render_template. Es la única implementación
de envío de correo; app/services/email_service.py es shim legacy que
re-exporta desde aquí para no romper imports externos durante la migración.
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.utils import formataddr, formatdate, make_msgid
from flask import render_template
from flask import current_app


def _build_from_header(config):
    email = config.get('MAIL_DEFAULT_SENDER') or config.get('MAIL_USERNAME') or 'soporte@sgrv.azconsultingperu.com'
    name = config.get('MAIL_SENDER_NAME') or 'SGRV \u2013 IESTP Paij\u00e1n'
    return formataddr((name, email)), email


def enviar_correo(destinatario, asunto, template, **kwargs):
    config = current_app.config
    # Estructura: related (html + inline image) con alternative (plain + html) dentro
    # Esto permite cid:logo_sgrv en el HTML
    html = render_template(f'email/{template}', **kwargs)
    # Texto plano alternativo para mejorar entregabilidad y evitar spam
    text_plain = None
    if 'usuario' in kwargs and 'reset_url' in kwargs:
        usr = kwargs.get('usuario')
        url = kwargs.get('reset_url')
        try:
            nombre = getattr(usr, 'nombres', '') or getattr(usr, 'username', '')
            text_plain = f"Hola {nombre},\n\nRecibimos una solicitud para restablecer tu contraseña en SGRV.\nUsuario: {getattr(usr, 'username', '')}\nEnlace (vence en 15 minutos): {url}\n\nSi no solicitaste este cambio, ignora este correo.\n\nSGRV – IESTP Paiján"
        except Exception:
            text_plain = None

    # Mensaje contenedor related para CID
    mensaje = MIMEMultipart('related')
    from_header, envelope_from = _build_from_header(config)
    # Normalizar From a ASCII para evitar =?utf-8?q? que suma score en SpamAssassin
    try:
        # Si el nombre contiene "–" (en dash), usar guion simple ASCII
        _email_only = config.get('MAIL_DEFAULT_SENDER') or envelope_from
        _ascii_name = 'SGRV - IESTP Paijan'
        from_header = formataddr((_ascii_name, _email_only))
    except Exception:
        pass
    mensaje['From'] = from_header
    mensaje['To'] = destinatario
    mensaje['Subject'] = asunto
    mensaje['Date'] = formatdate(localtime=True)
    mensaje['Message-ID'] = make_msgid(domain='sgrv.azconsultingperu.com')

    # Parte alternative para plain/html
    alternative = MIMEMultipart('alternative')
    if text_plain:
        alternative.attach(MIMEText(text_plain, 'plain', 'utf-8'))
    parte_html = MIMEText(html, 'html', 'utf-8')
    alternative.attach(parte_html)
    mensaje.attach(alternative)

    # Adjuntar logo como CID inline para todos los correos
    try:
        logo_path = os.path.join(current_app.root_path, 'static', 'img', 'logo.png')
        if os.path.exists(logo_path):
            with open(logo_path, 'rb') as f:
                img_data = f.read()
            logo_img = MIMEImage(img_data)
            logo_img.add_header('Content-ID', '<logo_sgrv>')
            logo_img.add_header('Content-Disposition', 'inline', filename='logo.png')
            mensaje.attach(logo_img)
        else:
            current_app.logger.warning(f'Logo CID no encontrado en {logo_path}, se envía sin imagen embebida')
    except Exception as e:
        current_app.logger.warning(f'No se pudo adjuntar logo CID: {e}')

    try:
        use_ssl = bool(config.get('MAIL_USE_SSL'))
        use_tls = bool(config.get('MAIL_USE_TLS'))
        port = int(config.get('MAIL_PORT') or 465)
        timeout = 10
        # Puerto 465 implica SSL directo aunque el flag no esté seteado
        if use_ssl or port == 465:
            server = smtplib.SMTP_SSL(config['MAIL_SERVER'], port, timeout=timeout)
            if config.get('MAIL_USERNAME') and config.get('MAIL_PASSWORD'):
                server.login(config['MAIL_USERNAME'], config['MAIL_PASSWORD'])
        else:
            server = smtplib.SMTP(config['MAIL_SERVER'], port, timeout=timeout)
            if use_tls:
                server.starttls()
            if config.get('MAIL_USERNAME') and config.get('MAIL_PASSWORD'):
                server.login(config['MAIL_USERNAME'], config['MAIL_PASSWORD'])
        server.sendmail(envelope_from, destinatario, mensaje.as_string())
        server.quit()
        return True
    except Exception as e:
        # No exponer password ni trace técnico al usuario; solo log interno
        current_app.logger.error(f'Error al enviar correo a {destinatario}: {e}')
        return False


def notificar_nuevo_registro(alumno, visita):
    asunto = f'Nuevo registro: {alumno.nombres} {alumno.apellidos} - {alumno.dni}'
    destinatario = current_app.config['NOTIFY_EMAIL']
    return enviar_correo(destinatario, asunto, 'nuevo_registro.html',
                         alumno=alumno, visita=visita)


def notificar_nuevo_usuario(usuario, password):
    asunto = f'Nuevo usuario creado: {usuario.username}'
    destinatario = current_app.config['NOTIFY_EMAIL']
    return enviar_correo(destinatario, asunto, 'nuevo_usuario.html',
                         usuario=usuario, password=password)


def enviar_correo_recuperacion(usuario, reset_url):
    asunto = 'Recuperación de Contraseña - SGRV IESTP Paiján'
    destinatario = usuario.email
    return enviar_correo(destinatario, asunto, 'recuperar_contrasena.html',
                         usuario=usuario, reset_url=reset_url)
