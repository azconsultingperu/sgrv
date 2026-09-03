# -*- coding: utf-8 -*-
import os
import uuid
from io import BytesIO

from flask import current_app
from PIL import Image, ImageOps


def _foto_dir():
    directorio = current_app.config['ALUMNO_FOTO_DIR']
    os.makedirs(directorio, exist_ok=True)
    return directorio


def _path_seguro(nombre):
    real = os.path.realpath(os.path.join(_foto_dir(), nombre))
    if not real.startswith(os.path.realpath(_foto_dir()) + os.sep):
        raise ValueError('Ruta inválida')
    return real


def _drop_foto_files(alumno):
    """Borra archivos de foto del alumno si existen."""
    if not alumno.foto:
        return
    for sufijo in ('', '_min'):
        nombre = alumno.foto[:-5] + sufijo + alumno.foto[-5:] if alumno.foto.endswith('.webp') else alumno.foto
        try:
            ruta = _path_seguro(nombre)
            if os.path.isfile(ruta):
                os.remove(ruta)
        except (ValueError, OSError):
            pass
    alumno.foto = None


def guardar_foto(alumno, file_storage):
    """
    Valida y guarda foto para alumno. Retorna (ok, error_msg).
    Si ok, alumno.foto queda seteado pero NO hace commit (caller debe commit).
    """
    if file_storage is None or file_storage.filename == '':
        return False, 'No se recibió ningún archivo.'

    nombre_original = file_storage.filename
    extension = nombre_original.rsplit('.', 1)[-1].lower() if '.' in nombre_original else ''
    if extension not in current_app.config['ALUMNO_FOTO_EXTENSIONS']:
        return False, 'Formato no permitido. Use JPG, PNG, WebP o GIF.'

    try:
        datos = file_storage.read(current_app.config['ALUMNO_FOTO_MAX_SIZE'] + 1)
    except Exception:
        return False, 'Error al leer el archivo.'

    if len(datos) > current_app.config['ALUMNO_FOTO_MAX_SIZE']:
        return False, 'La imagen supera los 2 MB de tamaño máximo.'

    try:
        img = Image.open(BytesIO(datos))
        img.verify()
        img = Image.open(BytesIO(datos))
        img = ImageOps.exif_transpose(img)
        ancho, alto = img.size
        if (ancho * alto) > 50_000_000:
            return False, 'La imagen es demasiado grande.'
    except Exception:
        return False, 'El archivo no es una imagen válida.'

    if img.mode in ('RGBA', 'LA', 'P'):
        img = img.convert('RGBA')
    else:
        img = img.convert('RGB')

    full_dim = current_app.config['ALUMNO_FOTO_FULL_DIM']
    img.thumbnail((full_dim, full_dim), Image.LANCZOS)

    # Borrar foto anterior antes de crear nueva
    _drop_foto_files(alumno)

    base = f"{alumno.id}_{uuid.uuid4().hex}" if alumno.id else uuid.uuid4().hex
    nombre_full = f"{base}.webp"
    nombre_thumb = f"{base}_min.webp"

    directorio = _foto_dir()
    buf_full = BytesIO()
    img.save(buf_full, format='WEBP', quality=85)
    with open(os.path.join(directorio, nombre_full), 'wb') as f:
        f.write(buf_full.getvalue())

    thumb_dim = current_app.config['ALUMNO_FOTO_THUMB_DIM']
    thumb = img.copy()
    thumb.thumbnail((thumb_dim, thumb_dim), Image.LANCZOS)
    buf_thumb = BytesIO()
    thumb.save(buf_thumb, format='WEBP', quality=80)
    with open(os.path.join(directorio, nombre_thumb), 'wb') as f:
        f.write(buf_thumb.getvalue())

    alumno.foto = nombre_full
    return True, None
