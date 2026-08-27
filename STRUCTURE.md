# STRUCTURE — SGRV (Sistema de Gestión de Registro de Visitas)

Mapa del repositorio para desarrollo y mantenimiento. Verificado contra los archivos reales.

```
sgrv/
├── app/
│   ├── shared/               # Kernel compartido (infra transversal)
│   │   ├── db.py             # SQLAlchemy instance (importado por app/__init__.py)
│   │   ├── events.py         # Bus síncrono + catálogo DomainEvent (AlumnoRegistrado, AvatarActualizado...)
│   │   ├── unit_of_work.py   # UoW con publish atómico (commit despacha, rollback descarta)
│   │   ├── time_utils.py     # Wrapper de app.utils.time_utils (peru_now)
│   │   └── errors.py         # DomainError, NotFoundError
│   ├── modules/              # Monolito modular estricto (1 módulo = 1 bounded context)
│   │   ├── identidad/        # usuarios, roles, auth, sesión, perfil/avatar
│   │   │   ├── domain/       # Usuario, Rol, Sesion (SQLAlchemy, sin imports a application)
│   │   │   ├── application/  # event_handlers (Avatar...), (futuro auth_service)
│   │   │   ├── infrastructure/ # usuario_repository, avatar_storage
│   │   │   ├── presentation/ # auth_controller, usuarios_controller, perfil_controller
│   │   │   └── public.py     # Facade: get_usuario, count_usuarios, etc.
│   │   ├── registro/         # alumno, visita, institución, carrera, promotor
│   │   │   ├── domain/       # Alumno, Visita, InstitucionEducativa, Carrera, Promotor
│   │   │   ├── application/  # registro_service (crear_alumno_con_visita + UoW)
│   │   │   ├── infrastructure/ # alumno_repository, visita_repository
│   │   │   ├── presentation/ # registro_controller (usa registro_service + publish)
│   │   │   └── public.py     # Facade: consultar_alumnos, get_alumno, dashboard helpers
│   │   ├── consulta/         # Búsqueda y detalle (consume registro.public)
│   │   │   └── presentation/ # consulta_controller (filtros via registro.public)
│   │   ├── dashboard/        # Métricas (consume registro.public)
│   │   │   ├── application/  # estadistica_service (delega a registro.public)
│   │   │   └── presentation/ # dashboard_controller
│   │   ├── auditoria/        # Auditoría (event handlers)
│   │   │   ├── domain/       # Auditoria
│   │   │   └── application/  # event_handlers (AlumnoRegistrado -> auditoria)
│   │   └── reportes/         # Exportes CSV/Excel (usa registro.domain, fix excel)
│   │       ├── application/  # reporte_service (excel con filtros y eliminado=False)
│   │       └── presentation/ # reportes_controller
│   ├── controllers/          # [LEGACY shims] re-exportan desde modules/* (1 sprint)
│   ├── models/               # [LEGACY shims] re-exportan desde modules/*/domain
│   ├── services/             # [LEGACY] auditoria_service, email_service, estadistica_service (shim)
│   ├── utils/                # Helpers, decorators, time_utils, seed de fábrica
│   ├── templates/            # Plantillas Jinja2
│   │   ├── auth/ dashboard/ registro/ consulta/ usuarios/ auditoria/ reportes/ perfil/
│   │   ├── email/            # Plantillas de correo
│   │   ├── errors/           # 403, 404, 500
│   │   └── partials/         # navbar, sidebar, paginación
│   ├── static/
│   │   ├── css/              # style.css, auth.css
│   │   ├── js/               # main.js, perfil.js
│   │   ├── img/              # logos, frontis, avatar por defecto
│   │   ├── fonts/            # Inter
│   │   └── uploads/          # Avatares subidos (no versionado)
│   └── config.py             # Configuración de la aplicación
├── instance/database/gestion_visitas.db   # Backup SQLite de la BD original (ya migrada a PostgreSQL)
├── database/gestion_visitas.db.bak        # Backup de BD obsoleta (no se usa)
├── migrations/               # Migraciones Alembic (Flask-Migrate)
├── logs/                     # server.log y URL del túnel Cloudflare (tunel.txt)
├── requirements.txt          # Dependencias (incluye import-linter, grimp)
├── setup.cfg                 # Contratos import-linter (layers + forbidden)
├── Makefile                  # Targets: lint-boundaries, test
├── .github/workflows/ci.yml  # CI: lint-boundaries + pytest
├── run.py                    # Punto de entrada (Flask + túnel Cloudflare)
├── .env / .env.example       # Variables de entorno reales / plantilla
├── .devcontainer/            # VS Code Dev Containers
└── venv/                     # Entorno virtual local (no versionado)
```

## Dónde se edita cada cosa

| Qué | Archivo |
|---|---|
| Kernel compartido | `app/shared/*.py` (db, events, unit_of_work) |
| Dominio identidad | `app/modules/identidad/domain/*.py` |
| Dominio registro | `app/modules/registro/domain/*.py` |
| Lógica de aplicación registro | `app/modules/registro/application/registro_service.py` |
| Repositorios | `app/modules/*/infrastructure/*_repository.py` |
| Rutas HTTP (nuevo) | `app/modules/*/presentation/*_controller.py` |
| Rutas HTTP (legacy shim) | `app/controllers/*.py` (re-export) |
| Tablas/ORM (legacy shim) | `app/models/*.py` (re-export) |
| Reglas de negocio transversales | `app/shared/events.py` + `app/modules/*/application/event_handlers.py` |
| Vistas | `app/templates/**` (Jinja2) |
| Estilos | `app/static/css/*.css` (versionado con `?v=` en plantillas) |
| Scripts frontend | `app/static/js/*.js` |
| Migraciones | `migrations/versions/*.py` (`python -m flask db upgrade`) |
| Contratos de fronteras | `setup.cfg` (`lint-imports`) |
| Usuarios iniciales | `app/utils/seed.py` (solo al recrear la BD desde cero) |
| BD activa | PostgreSQL local (`DATABASE_URL` en `.env`, usuario `sgrv`, BD `gestion_visitas`) |
| BD SQLite original | `instance/database/gestion_visitas.db` (backup, no se usa) |

## Cómo añadir un módulo nuevo

1. Crear `app/modules/<nombre>/{domain,application,infrastructure,presentation}/` + `public.py` y `__init__.py` en cada capa.
2. Definir modelos en `domain/` (solo `from app.shared.db import db` y `from app.shared.time_utils import peru_now`; prohibido importar `application`).
3. Exponer casos de uso en `public.py` (facade) — único import permitido desde otros módulos.
4. Registrar blueprint en `app/__init__.py:create_app()` y sus handlers en `app/shared/events.py` via `register(bus)`.
5. Añadir contratos en `setup.cfg` si el módulo tiene fronteras nuevas; verificar con `make lint-boundaries`.
6. Mantener `app/controllers/` y `app/models/` como shims 1 sprint; luego eliminar.

## Verificación de fronteras

```bash
make lint-boundaries   # o venv/bin/lint-imports
FLASK_ENV=testing venv/bin/python -m pytest tests/test_boundaries.py -v
```
