# -*- coding: utf-8 -*-
import os
import uuid
from io import BytesIO
from flask import Blueprint, render_template, request, jsonify, current_app, abort, send_file
from flask_login import login_required, current_user
from app.models.usuario import Usuario
from app.services.auditoria_service import registrar_auditoria
from app import db
from app.utils.time_utils import peru_now

perfil_bp = Blueprint('perfil', __name__, url_prefix='/perfil')


def _avatar_dir():
    directorio = current_app.config['PERFIL_AVATAR_DIR']
    os.makedirs(directorio, exist_ok=True)
    return directorio


def _path_seguro(nombre):
    real = os.path.realpath(os.path.join(_avatar_dir(), nombre))
    if not real.startswith(os.path.realpath(_avatar_dir()) + os.sep):
        raise ValueError('Ruta inválida')
    return real


def _drop_avatar_files(usuario):
    """Borra los archivos de avatar del usuario, salvo que una auditoría
    los referencie como snapshot histórico."""
    if not usuario.avatar:
        return
    from app.models.auditoria import Auditoria
    for sufijo in ('', '_min'):
        nombre = usuario.avatar[:-5] + sufijo + usuario.avatar[-5:]
        if Auditoria.query.filter_by(avatar=nombre).first():
            continue
        try:
            ruta = _path_seguro(nombre)
            if os.path.isfile(ruta):
                os.remove(ruta)
        except (ValueError, OSError):
            pass
    usuario.avatar = None


@perfil_bp.route('/avatar/archivo/<path:nombre>')
@login_required
def servir_avatar_archivo(nombre):
    """Sirve un archivo de avatar por nombre (snapshots históricos de auditoría).
    Si el archivo no existe (foto eliminada), devuelve el default.
    Si el thumb no existe, sirve la versión completa (fallback)."""
    from app.models.usuario import Usuario
    def ruta_segura(n):
        try:
            return _path_seguro(n)
        except ValueError:
            return None

    ruta = ruta_segura(nombre)
    if ruta is None or not os.path.isfile(ruta):
        if nombre.endswith('_min.webp'):
            base = nombre[:-9] + nombre[-5:]
            ruta = ruta_segura(base)
    if ruta is None or not os.path.isfile(ruta):
        return send_file(os.path.join(current_app.static_folder, 'img', 'avatar-default.svg'),
                         mimetype='image/svg+xml', max_age=86400)
    resp = send_file(ruta, mimetype='image/webp', conditional=True)
    resp.headers['Cache-Control'] = 'private, max-age=0, must-revalidate'
    return resp


@perfil_bp.route('/')
@login_required
def index():
    return render_template('perfil/index.html')


@perfil_bp.route('/avatar/<int:usuario_id>')
@login_required
def servir_avatar(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    if not usuario.avatar:
        abort(404)
    nombre = usuario.avatar
    if request.args.get('t'):
        nombre = usuario.avatar[:-5] + '_min' + usuario.avatar[-5:]
    try:
        ruta = _path_seguro(nombre)
    except ValueError:
        abort(404)
    if not os.path.isfile(ruta):
        abort(404)
    resp = send_file(ruta, mimetype='image/webp', conditional=True)
    resp.headers['Cache-Control'] = 'private, max-age=0, must-revalidate'
    return resp


@perfil_bp.route('/avatar', methods=['POST'])
@login_required
def subir_avatar():
    return _procesar_avatar(current_user, request)


@perfil_bp.route('/avatar/<int:usuario_id>', methods=['POST'])
@login_required
def subir_avatar_admin(usuario_id):
    if current_user.id != usuario_id and current_user.rol_id != 1:
        return jsonify({'ok': False, 'error': 'No tiene permisos para modificar esta foto.'}), 403
    usuario = Usuario.query.get_or_404(usuario_id)
    return _procesar_avatar(usuario, request)


@perfil_bp.route('/avatar', methods=['DELETE'])
@login_required
def borrar_avatar():
    _drop_avatar_files(current_user)
    db.session.commit()
    registrar_auditoria(current_user.id, 'Actualización de perfil', 'Perfil',
        'Foto de perfil eliminada', avatar='')
    return jsonify({'ok': True})


@perfil_bp.route('/avatar/<int:usuario_id>', methods=['DELETE'])
@login_required
def borrar_avatar_admin(usuario_id):
    if current_user.id != usuario_id and current_user.rol_id != 1:
        return jsonify({'ok': False, 'error': 'No tiene permisos para modificar esta foto.'}), 403
    usuario = Usuario.query.get_or_404(usuario_id)
    _drop_avatar_files(usuario)
    db.session.commit()
    registrar_auditoria(current_user.id, 'Actualización de perfil', 'Perfil',
        f'Foto de perfil eliminada (usuario {usuario.username})', avatar='')
    return jsonify({'ok': True})


def _procesar_avatar(usuario, request):
    archivo = request.files.get('file')
    if archivo is None or archivo.filename == '':
        return jsonify({'ok': False, 'error': 'No se recibió ningún archivo.'}), 400

    nombre_original = archivo.filename
    extension = nombre_original.rsplit('.', 1)[-1].lower() if '.' in nombre_original else ''
    if extension not in current_app.config['PERFIL_AVATAR_EXTENSIONS']:
        return jsonify({'ok': False, 'error': 'Formato no permitido. Use JPG, PNG, WebP o GIF.'}), 400

    from PIL import Image, ImageOps
    max_dim = current_app.config['PERFIL_AVATAR_MAX_DIM']
    try:
        datos = archivo.read(current_app.config['PERFIL_AVATAR_MAX_SIZE'] + 1)
    except Exception:
        return jsonify({'ok': False, 'error': 'Error al leer el archivo.'}), 400

    if len(datos) > current_app.config['PERFIL_AVATAR_MAX_SIZE']:
        return jsonify({'ok': False, 'error': 'La imagen supera los 2 MB de tamaño máximo.'}), 413

    try:
        img = Image.open(BytesIO(datos))
        ancho, alto = img.size
        if ancho > max_dim or alto > max_dim or (ancho * alto) > 50_000_000:
            return jsonify({'ok': False, 'error': f'Resolución máxima permitida: {max_dim}x{max_dim} px.'}), 400
        img.verify()
        img = Image.open(BytesIO(datos))
        img = ImageOps.exif_transpose(img)
        ancho, alto = img.size
        if ancho > max_dim or alto > max_dim or (ancho * alto) > 50_000_000:
            return jsonify({'ok': False, 'error': f'Resolución máxima permitida: {max_dim}x{max_dim} px.'}), 400
    except Exception:
        return jsonify({'ok': False, 'error': 'El archivo no es una imagen válida.'}), 400

    if img.mode in ('RGBA', 'LA', 'P'):
        img = img.convert('RGBA')
    else:
        img = img.convert('RGB')

    full_dim = current_app.config['PERFIL_AVATAR_FULL_DIM']
    img.thumbnail((full_dim, full_dim), Image.LANCZOS)

    base = f"{usuario.id}_{uuid.uuid4().hex}"
    nombre_full = f"{base}.webp"
    nombre_thumb = f"{base}_min.webp"

    directorio = _avatar_dir()
    buf_full = BytesIO()
    img.save(buf_full, format='WEBP', quality=85)
    with open(os.path.join(directorio, nombre_full), 'wb') as f:
        f.write(buf_full.getvalue())

    thumb_dim = current_app.config['PERFIL_AVATAR_THUMB_DIM']
    thumb = img.copy()
    thumb.thumbnail((thumb_dim, thumb_dim), Image.LANCZOS)
    buf_thumb = BytesIO()
    thumb.save(buf_thumb, format='WEBP', quality=80)
    with open(os.path.join(directorio, nombre_thumb), 'wb') as f:
        f.write(buf_thumb.getvalue())

    _drop_avatar_files(usuario)
    usuario.avatar = nombre_full
    db.session.commit()

    if usuario.id == current_user.id:
        registrar_auditoria(current_user.id, 'Actualización de perfil', 'Perfil',
            'Foto de perfil actualizada', avatar=usuario.avatar)
    else:
        registrar_auditoria(current_user.id, 'Actualización de perfil', 'Perfil',
            f'Foto de perfil actualizada (usuario {usuario.username})', avatar=usuario.avatar)
    return jsonify({'ok': True, 'src': usuario.avatar_url(), 'thumbSrc': usuario.avatar_url(True)})
