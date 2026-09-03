import os
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))

def _parse_bool_env(value, default):
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in ('1', 'true', 'yes', 'on')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///database/gestion_visitas.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    INIT_DB_ON_START = True
    WTF_CSRF_ENABLED = True
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600
    MAX_LOGIN_ATTEMPTS = 5
    UPLOAD_FOLDER = os.path.join(os.path.dirname(basedir), 'app', 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
    PERFIL_AVATAR_DIR = os.path.join(os.path.dirname(basedir), 'app', 'static', 'uploads', 'perfil')
    PERFIL_AVATAR_MAX_SIZE = 10 * 1024 * 1024
    PERFIL_AVATAR_MAX_DIM = 1000
    PERFIL_AVATAR_FULL_DIM = 600
    PERFIL_AVATAR_THUMB_DIM = 90
    PERFIL_AVATAR_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}
    ALUMNO_FOTO_DIR = os.path.join(os.path.dirname(basedir), 'app', 'static', 'uploads', 'alumnos')
    ALUMNO_FOTO_MAX_SIZE = 2 * 1024 * 1024
    ALUMNO_FOTO_MAX_DIM = 1000
    ALUMNO_FOTO_FULL_DIM = 600
    ALUMNO_FOTO_THUMB_DIM = 90
    ALUMNO_FOTO_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'sgrv.azconsultingperu.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 465)
    MAIL_USE_TLS = _parse_bool_env(os.environ.get('MAIL_USE_TLS'), False)
    MAIL_USE_SSL = _parse_bool_env(os.environ.get('MAIL_USE_SSL'), True)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'soporte@sgrv.azconsultingperu.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or ''
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'soporte@sgrv.azconsultingperu.com'
    MAIL_SENDER_NAME = os.environ.get('MAIL_SENDER_NAME') or 'SGRV \u2013 IESTP Paij\u00e1n'
    NOTIFY_EMAIL = os.environ.get('NOTIFY_EMAIL') or 'soporte@sgrv.azconsultingperu.com'
    # DX: desactiva rate limit de recuperar solo en dev/testing, nunca en prod
    DISABLE_RATE_LIMIT = _parse_bool_env(os.environ.get('DISABLE_RATE_LIMIT'), False)

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://usuario:password@localhost:5432/gestion_visitas'
    SESSION_COOKIE_SECURE = True
    INIT_DB_ON_START = False
    DISABLE_RATE_LIMIT = False  # nunca desactivar en prod, aunque env lo pida

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    INIT_DB_ON_START = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
