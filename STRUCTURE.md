# STRUCTURE — SGRV (Sistema de Gestión de Registro de Visitas)

Mapa del repositorio para desarrollo y mantenimiento. Verificado contra los archivos reales.

```
sgrv/
├── app/
│   ├── controllers/        # Blueprints = rutas HTTP (auth, dashboard, registro, consulta, usuarios, auditoria, reportes, perfil)
│   ├── models/             # Modelos SQLAlchemy (alumno, usuario, rol, visita, auditoria, carrera, promotor, ...)
│   ├── services/           # Lógica de negocio (auditoria, email, estadística, reporte)
│   ├── utils/              # Helpers, decorators, time_utils, seed de fábrica
│   ├── templates/          # Plantillas Jinja2
│   │   ├── auth/ dashboard/ registro/ consulta/ usuarios/ auditoria/ reportes/ perfil/
│   │   ├── email/          # Plantillas de correo
│   │   ├── errors/         # 403, 404, 500
│   │   └── partials/       # navbar, sidebar, paginación
│   ├── static/
│   │   ├── css/            # style.css, auth.css
│   │   ├── js/             # main.js, perfil.js
│   │   ├── img/            # logos, frontis, avatar por defecto
│   │   ├── fonts/          # Inter
│   │   └── uploads/        # Avatares subidos (no versionado)
│   └── config.py           # Configuración de la aplicación
├── instance/database/gestion_visitas.db   # BD SQLite ACTIVA (runtime)
├── database/gestion_visitas.db.bak        # Backup de BD obsoleta (no se usa)
├── migrations/             # Migraciones Alembic (Flask-Migrate)
├── logs/                   # server.log y URL del túnel Cloudflare (tunel.txt)
├── requirements.txt        # Dependencias (Python 3.10–3.12; pandas 2.1.4 no compila en 3.13+)
├── run.py                  # Punto de entrada (Flask + túnel Cloudflare)
├── .env / .env.example     # Variables de entorno reales / plantilla
├── .devcontainer/          # VS Code Dev Containers
└── venv/                   # Entorno virtual local (no versionado)
```

## Dónde se edita cada cosa

| Qué | Archivo |
|---|---|
| Rutas HTTP | `app/controllers/*.py` |
| Tablas/ORM | `app/models/*.py` |
| Reglas de negocio | `app/services/*.py` (auditoría, reportes, estadística) |
| Vistas | `app/templates/**` (Jinja2) |
| Estilos | `app/static/css/*.css` (versionado con `?v=` en plantillas) |
| Scripts frontend | `app/static/js/*.js` |
| Migraciones | `migrations/versions/*.py` (`python -m flask db upgrade`) |
| Usuarios iniciales | `app/utils/seed.py` (solo al recrear la BD desde cero) |
| BD activa | `instance/database/gestion_visitas.db` (no se versiona) |