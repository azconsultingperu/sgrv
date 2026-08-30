from flask import Flask, render_template, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
import os

from app.utils.time_utils import peru_now
from app.shared.db import db

login_manager = LoginManager()
csrf = CSRFProtect()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    entorno = os.environ.get('FLASK_ENV', 'development')
    config_map = {
        'production': 'app.config.ProductionConfig',
        'testing': 'app.config.TestingConfig',
        'development': 'app.config.DevelopmentConfig',
    }
    app.config.from_object(config_map.get(entorno, 'app.config.Config'))

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = None

    @login_manager.user_loader
    def load_user(user_id):
        from app.modules.identidad.domain.usuario import Usuario
        try:
            u = Usuario.query.get(int(user_id))
        except Exception:
            return None
        if u and u.estado and not u.is_bloqueado() and not u.eliminado:
            return u
        return None

    from app.modules.identidad.presentation.auth_controller import auth_bp
    from app.modules.dashboard.presentation.dashboard_controller import dashboard_bp
    from app.modules.registro.presentation.registro_controller import registro_bp
    from app.modules.consulta.presentation.consulta_controller import consulta_bp
    from app.modules.identidad.presentation.usuarios_controller import usuarios_bp
    from app.modules.auditoria.presentation.auditoria_controller import auditoria_bp
    from app.modules.reportes.presentation.reportes_controller import reportes_bp
    from app.modules.identidad.presentation.perfil_controller import perfil_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(registro_bp)
    app.register_blueprint(consulta_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(auditoria_bp)
    app.register_blueprint(reportes_bp)
    app.register_blueprint(perfil_bp)

    # Bootstrap de eventos de dominio
    try:
        from app.shared.events import bus as _bus
        from app.modules.identidad.application.event_handlers import register as _register_identidad
        from app.modules.auditoria.application.event_handlers import register as _register_auditoria
        from app.modules.notifications.application.event_handlers import register as _register_notif
        _register_identidad(_bus)
        _register_auditoria(_bus)
        _register_notif(_bus)
    except Exception as e:
        # No bloquear arranque si falla registro
        print(f"Warning: no se pudo registrar handlers: {e}")

    @app.route('/robots.txt')
    def robots_txt():
        return send_from_directory(os.path.join(app.root_path, '..'), 'robots.txt', mimetype='text/plain')

    @app.route('/sitemap.xml')
    def sitemap_xml():
        return send_from_directory(os.path.join(app.root_path, '..'), 'sitemap.xml', mimetype='application/xml')

    @app.route('/')
    def index():
        return redirect(url_for('dashboard.index'))

    @app.context_processor
    def inject_now():
        return {'now': peru_now}

    @app.after_request
    def no_cache_html(response):
        if response.mimetype == 'text/html' or (
            response.content_type and response.content_type.startswith('text/html')):
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
        return response

    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html', error_code=404,
            error_title='Página no encontrada', error_message='La página que buscas no existe.'), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html', error_code=403,
            error_title='Acceso Denegado', error_message='No tienes permisos para acceder a esta sección.'), 403

    @app.errorhandler(500)
    def internal_error(e):
        try:
            db.session.rollback()
        except Exception:
            pass
        return render_template('errors/500.html', error_code=500,
            error_title='Error del Servidor', error_message='Ha ocurrido un error interno. Contacte al administrador.'), 500

    @app.teardown_appcontext
    def _cerrar_sesion_por_error(exc):
        if exc is not None:
            try:
                db.session.rollback()
            except Exception:
                pass

    if app.config.get('INIT_DB_ON_START'):
        with app.app_context():
            _preparar_ruta_sqlite()
            _inicializar_bd()

    @app.cli.command('init-db')
    def init_db_command():
        """Crea tablas y datos iniciales. Solo para entornos nuevos o de desarrollo."""
        with app.app_context():
            _preparar_ruta_sqlite()
            _inicializar_bd()
        print('Base de datos inicializada.')

    return app


def _preparar_ruta_sqlite():
    """Flask-SQLAlchemy resuelve las rutas SQLite relativas contra `instance/`
    (app.instance_path); creamos la carpeta si falta."""
    from pathlib import Path
    engine_url = db.engine.url
    if (
        engine_url.drivername.startswith('sqlite')
        and engine_url.database
        and engine_url.database != ':memory:'
    ):
        Path(engine_url.database).parent.mkdir(parents=True, exist_ok=True)


def _inicializar_bd():
    """create_all + parches legacy + seed. Solo en desarrollo o via `flask init-db`.

    En produccion el esquema cambia EXCLUSIVAMENTE con migraciones (`flask db upgrade`).
    """
    # Importar dominios para registrar modelos en SQLAlchemy (antes vía app.models shims)
    from app.modules.identidad.domain import usuario, rol, sesion  # noqa: F401
    from app.modules.registro.domain import alumno, institucion_educativa, visita, promotor, carrera  # noqa: F401
    from app.modules.auditoria.domain import auditoria  # noqa: F401
    from app.modules.reportes.domain import reporte  # noqa: F401
    from app.modules.dashboard.domain import dashboard_estadistica  # noqa: F401
    db.create_all()

    from sqlalchemy import inspect, text
    inspector = inspect(db.engine)
    if 'usuarios' in inspector.get_table_names():
        columnas = {c['name'] for c in inspector.get_columns('usuarios')}
        if 'avatar' not in columnas:
            db.session.execute(text('ALTER TABLE usuarios ADD COLUMN avatar VARCHAR(255)'))
            db.session.commit()
        if 'eliminado' not in columnas:
            db.session.execute(text('ALTER TABLE usuarios ADD COLUMN eliminado BOOLEAN DEFAULT 0'))
            db.session.commit()

    from app.utils.seed import seed_data
    seed_data()
