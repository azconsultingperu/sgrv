import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import render_template
from flask import current_app

def enviar_correo(destinatario, asunto, template, **kwargs):
    config = current_app.config
    mensaje = MIMEMultipart('alternative')
    mensaje['From'] = config['MAIL_USERNAME']
    mensaje['To'] = destinatario
    mensaje['Subject'] = asunto

    html = render_template(f'email/{template}', **kwargs)
    parte_html = MIMEText(html, 'html')
    mensaje.attach(parte_html)

    try:
        server = smtplib.SMTP(config['MAIL_SERVER'], config['MAIL_PORT'])
        server.starttls()
        server.login(config['MAIL_USERNAME'], config['MAIL_PASSWORD'])
        server.sendmail(config['MAIL_USERNAME'], destinatario, mensaje.as_string())
        server.quit()
        return True
    except Exception as e:
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
