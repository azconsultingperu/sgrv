from app.models.rol import Rol
from app.models.usuario import Usuario
from app.models.promotor import Promotor
from app.models.carrera import Carrera
from app.models.institucion_educativa import InstitucionEducativa
from app import db
from datetime import datetime

def seed_data():
    if Rol.query.count() == 0:
        roles = [
            Rol(nombre='Administrador', descripcion='Acceso total al sistema'),
            Rol(nombre='Supervisor', descripcion='Puede registrar, consultar, editar y generar reportes'),
            Rol(nombre='Operador', descripcion='Puede registrar alumnos y consultar registros'),
            Rol(nombre='Consultas', descripcion='Acceso solo de lectura a Dashboard, Consultar y Reportes'),
        ]
        db.session.add_all(roles)
        db.session.commit()

    if Usuario.query.count() == 0:
        admin = Usuario(
            dni='12345678',
            nombres='Administrador',
            apellidos='del Sistema',
            username='12345678',
            email='admin@iestppaijan.edu.pe',
            rol_id=1,
            estado=True
        )
        admin.set_password('admin123')
        db.session.add(admin)

        supervisor = Usuario(
            dni='87654321',
            nombres='Supervisor',
            apellidos='Principal',
            username='87654321',
            email='supervisor@iestppaijan.edu.pe',
            rol_id=2,
            estado=True
        )
        supervisor.set_password('super123')
        db.session.add(supervisor)

        operador = Usuario(
            dni='11112222',
            nombres='Operador',
            apellidos='de Campo',
            username='11112222',
            email='operador@iestppaijan.edu.pe',
            rol_id=3,
            estado=True
        )
        operador.set_password('opera123')
        db.session.add(operador)
        db.session.commit()

    if Carrera.query.count() == 0:
        carreras = [
            Carrera(nombre='Administración de Centros de Cómputo', area_profesional='Tecnologías de la Información'),
            Carrera(nombre='Enfermería Técnica', area_profesional='Ciencias de la Salud'),
            Carrera(nombre='Producción Agropecuaria', area_profesional='Agroindustria'),
        ]
        db.session.add_all(carreras)
        db.session.commit()

    if InstitucionEducativa.query.count() == 0:
        colegios = [
            InstitucionEducativa(nombre='I.E. San Juan', distrito='Paiján', provincia='Ascope', region='La Libertad', tipo='Público'),
            InstitucionEducativa(nombre='I.E. Santa Rosa', distrito='Paiján', provincia='Ascope', region='La Libertad', tipo='Público'),
            InstitucionEducativa(nombre='I.E. José Carlos Mariátegui', distrito='Paiján', provincia='Ascope', region='La Libertad', tipo='Público'),
            InstitucionEducativa(nombre='I.E. Divino Maestro', distrito='Paiján', provincia='Ascope', region='La Libertad', tipo='Privado'),
            InstitucionEducativa(nombre='I.E. San Martín de Porres', distrito='Rázuri', provincia='Ascope', region='La Libertad', tipo='Público'),
            InstitucionEducativa(nombre='I.E. Manuel Gonzales Prada', distrito='Chicama', provincia='Ascope', region='La Libertad', tipo='Público'),
        ]
        db.session.add_all(colegios)
        db.session.commit()

    if Promotor.query.count() == 0:
        promotores = [
            Promotor(dni='22223333', nombres='Carlos', apellidos='López Pérez', email='clopez@iestppaijan.edu.pe', telefono='987654321'),
            Promotor(dni='33334444', nombres='María', apellidos='García Torres', email='mgarcia@iestppaijan.edu.pe', telefono='987654322'),
            Promotor(dni='44445555', nombres='Juan', apellidos='Rodríguez Silva', email='jrodriguez@iestppaijan.edu.pe', telefono='987654323'),
        ]
        db.session.add_all(promotores)
        db.session.commit()
