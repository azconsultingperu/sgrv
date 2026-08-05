from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
import os

from app.utils.time_utils import peru_now

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'auth.login'

    from app.controllers.auth_controller import auth_bp
    from app.controllers.dashboard_controller import dashboard_bp
    from app.controllers.registro_controller import registro_bp
    from app.controllers.consulta_controller import consulta_bp
    from app.controllers.usuarios_controller import usuarios_bp
    from app.controllers.auditoria_controller import auditoria_bp
    from app.controllers.reportes_controller import reportes_bp
    from app.controllers.perfil_controller import perfil_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(registro_bp)
    app.register_blueprint(consulta_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(auditoria_bp)
    app.register_blueprint(reportes_bp)
    app.register_blueprint(perfil_bp)

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
        return render_template('errors/500.html', error_code=500,
            error_title='Error del Servidor', error_message='Ha ocurrido un error interno. Contacte al administrador.'), 500

    with app.app_context():
        from pathlib import Path
        # Flask-SQLAlchemy resuelve las rutas SQLite relativas contra `instance/` (app.instance_path),
        # por lo que el engine puede apuntar a una carpeta que aún no existe. La creamos aqui.
        engine_url = db.engine.url
        if (
            engine_url.drivername.startswith('sqlite')
            and engine_url.database
            and engine_url.database != ':memory:'
        ):
            Path(engine_url.database).parent.mkdir(parents=True, exist_ok=True)
        from app.models import usuario, rol, alumno, institucion_educativa, visita, promotor, auditoria, sesion, carrera, reporte, dashboard_estadistica
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

    return app
