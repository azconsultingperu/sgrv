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
    login_manager.login_message = 'Por favor inicie sesión para acceder.'
    login_manager.login_message_category = 'warning'

    from app.controllers.auth_controller import auth_bp
    from app.controllers.dashboard_controller import dashboard_bp
    from app.controllers.registro_controller import registro_bp
    from app.controllers.consulta_controller import consulta_bp
    from app.controllers.usuarios_controller import usuarios_bp
    from app.controllers.auditoria_controller import auditoria_bp
    from app.controllers.reportes_controller import reportes_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(registro_bp)
    app.register_blueprint(consulta_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(auditoria_bp)
    app.register_blueprint(reportes_bp)

    @app.route('/')
    def index():
        return redirect(url_for('dashboard.index'))

    @app.context_processor
    def inject_now():
        return {'now': peru_now}

    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(500)
    def internal_error(e):
        return render_template('errors/500.html'), 500

    with app.app_context():
        from app.models import usuario, rol, alumno, institucion_educativa, visita, promotor, auditoria, sesion, carrera, reporte, dashboard_estadistica
        db.create_all()
        from app.utils.seed import seed_data
        seed_data()

    return app
