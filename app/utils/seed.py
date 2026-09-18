from app.modules.identidad.domain.rol import Rol
from app.modules.identidad.domain.usuario import Usuario
# Promotor clásico: sin seed. El Promotor Responsable sale de usuarios con rol
# Operador (union en vivo en registro_controller); la tabla promotores queda
# solo para historial de visitas antiguas.
from app.modules.registro.domain.carrera import Carrera
from app.modules.registro.domain.institucion_educativa import InstitucionEducativa
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

    if not Rol.query.filter_by(nombre='Consultas').first():
        db.session.add(Rol(nombre='Consultas', descripcion='Acceso solo de lectura a Dashboard, Consultar y Reportes'))
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

        consultas = Usuario(
            dni='99998888',
            nombres='Usuario',
            apellidos='Consultas',
            username='99998888',
            email='consultas@iestppaijan.edu.pe',
            rol_id=4,
            estado=True
        )
        consultas.set_password('consul123')
        db.session.add(consultas)
        db.session.commit()

    if Carrera.query.count() == 0:
        carreras = [
            Carrera(nombre='Administración de Centros de Cómputo', area_profesional='Tecnologías de la Información'),
            Carrera(nombre='Enfermería Técnica', area_profesional='Ciencias de la Salud'),
            Carrera(nombre='Producción Agropecuaria', area_profesional='Agroindustria'),
        ]
        db.session.add_all(carreras)
        db.session.commit()

    # Catálogo 2026-09-18 (imagen de dirección): solo las 10 I.E. visitadas.
    # Las 6 seed originales (San Juan, Santa Rosa, Mariátegui, Divino Maestro,
    # San Martín de Porres, Gonzales Prada) se eliminaron del catálogo; en BDs
    # con historial quedan con activo=false (ver migración siguiente).
    # Idempotente: solo inserta las que falten (por codigo_modular o nombre+distrito).
    # 10 I.E. de imagen 2026-09-15 (ver migración 64fa6966886d)
    nuevas_instituciones = [
        ("I.E. 80055 Juan Ignacio Gutiérrez Fuente", "80055", "Paiján", "Ascope", "La Libertad", "Público"),
        ("I.E. José Andrés Rázuri - Pto. Chicama", None, "Rázuri", "Ascope", "La Libertad", "Público"),
        ("I.E. 80085 Miguel Grau Seminario - Macabí Alto", "80085", "Rázuri", "Ascope", "La Libertad", "Público"),
        ("I.E. Nuestra Señora de Lourdes", None, "Ascope", "Ascope", "La Libertad", "Público"),
        ("I.E. 80850 San Salvador", "80850", "Paiján", "Ascope", "La Libertad", "Público"),
        ("I.E. 80057 Inmaculada Concepción", "80057", "Chicama", "Ascope", "La Libertad", "Público"),
        ("I.E. Leoncio Prado", None, "Paiján", "Ascope", "La Libertad", "Público"),
        ("I.E. 80878 Alfonso Ugarte - Licapa", "80878", "Paiján", "Ascope", "La Libertad", "Público"),
        ("I.E. 80053 José Olaya Balandra - La Arenita", "80053", "Paiján", "Ascope", "La Libertad", "Público"),
        ("I.E. 80050 José Félix Black", "80050", "Paiján", "Ascope", "La Libertad", "Público"),
    ]
    for nombre, codigo, distrito, provincia, region, tipo in nuevas_instituciones:
        exists = None
        if codigo:
            exists = InstitucionEducativa.query.filter_by(codigo_modular=codigo).first()
        else:
            exists = InstitucionEducativa.query.filter_by(nombre=nombre, distrito=distrito).first()
        if not exists:
            db.session.add(InstitucionEducativa(
                nombre=nombre, codigo_modular=codigo, distrito=distrito,
                provincia=provincia, region=region, tipo=tipo, activo=True
            ))
    db.session.commit()
