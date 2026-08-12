import os
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///database/gestion_visitas.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
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
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or True
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL') or False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'azconsultingperu@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or ''
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'azconsultingperu@gmail.com'
    NOTIFY_EMAIL = os.environ.get('NOTIFY_EMAIL') or 'azconsultingperu@gmail.com'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://usuario:password@localhost:5432/gestion_visitas'
    SESSION_COOKIE_SECURE = True

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
