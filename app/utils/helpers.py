import secrets
import string
from markupsafe import escape

def sanitizar_input(texto):
    if not isinstance(texto, str):
        return texto
    return escape(texto)

def validar_fortaleza_password(password):
    errores = []
    if len(password) < 8:
        errores.append('La contraseña debe tener al menos 8 caracteres.')
    return errores

def generar_password_segura(longitud=16):
    caracteres = string.ascii_letters + string.digits + '!@#$%^&*'
    return secrets.token_urlsafe(longitud)[:longitud]