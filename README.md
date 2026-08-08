# SISTEMA DE GESTIÓN DE REGISTRO DE VISITAS (SGRV)

## IESTP "Paiján"

Sistema web para registrar y gestionar las visitas realizadas por promotores institucionales a colegios de 5to de secundaria, con el objetivo de generar una base de datos para analizar, segmentar y predecir potenciales estudiantes interesados en estudiar en el Instituto de Educación Superior Tecnológico Público "Paiján".

![Vista previa del SGRV — Dashboard principal](app/static/img/exampleSGRV.png)

---

## Stack

- **Backend**: Python 3.10–3.12, Flask 3.0, SQLAlchemy 2.0, Flask-Login, Flask-WTF (CSRF), Flask-Migrate
- **Frontend:** Jinja2 + Bootstrap 5.3 + Chart.js 4.4 + Bootstrap Icons, CSS plano con tokens (`app/static/css/style.css`)
- **BD:** SQLite (dev) / PostgreSQL (producción)
- **Imágenes:** AVIF/WebP con fallback (originals en `app/static/img/`)

## Estructura

```
sgrv/
├── app/
│   ├── controllers/     # Blueprints: auth, dashboard, registro, consulta, usuarios, auditoria, reportes, perfil
│   ├── models/          # Modelos SQLAlchemy (alumnos, visitas, usuarios, roles, auditorías, ...)
│   ├── services/        # auditoria_service, email_service, estadistica_service, reporte_service
│   ├── templates/
│   │   ├── auth/ dashboard/ registro/ consulta/ usuarios/ auditoria/ reportes/ perfil/ errors/
│   │   ├── email/       # Plantillas de correo (estilo table inline, requerido por clientes de email)
│   │   └── partials/    # sidebar, navbar, paginación
│   ├── static/          # css/ js/ img/ fonts/ uploads/ (avatares subidos, no versionado)
│   ├── services/  utils/  config.py
├── instance/database/   # BD SQLite activa (las rutas relativas las resuelve Flask-SQLAlchemy contra instance/)
│   └── gestion_visitas.db
├── database/            # Solo contiene gestion_visitas.db.bak (backup histórico)
├── migrations/          # Flask-Migrate / Alembic
├── logs/                # server.log y tunel.txt (URL del túnel Cloudflare)
├── run.py               # Arranque Flask + túnel Cloudflare
├── requirements.txt · .env / .env.example · .devcontainer/
└── CHANGELOG.md
```

## Requisitos

- Python **3.10 – 3.12**. Con Python 3.13+ `pandas==2.1.4` no compila (no hay binarios precompilados): usa `uv venv --python 3.12 venv`.

## Instalación

```bash
git clone https://github.com/azconsultingperu/sgrv.git
cd sgrv
python -m venv venv
# activar venv (source venv/bin/activate, venv\Scripts\Activate.ps1, ...)
pip install -r requirements.txt
cp .env.example .env
python -m flask db upgrade    # solo si hay migraciones nuevas al hacer pull
```

## Ejecutar

```bash
python run.py
```

- Local: `http://localhost:5000`
- Red local: `http://<tu-IP-local>:5000`
- Túnel público: al arrancar se crea automáticamente una URL `https://XXXX.trycloudflare.com` (se guarda en `logs/tunel.txt`, expira al cerrar el servidor; desactívala con `CLOUDFLARE_TUNNEL=0` en `.env`).
- Si el túnel falla en Linux con `[Errno 13] Permission denied`: `chmod +x venv/lib/python3.12/site-packages/pycloudflared/cloudflared-linux-amd64` (run.py intenta corregirlo solo).

## Variables de entorno

| Variable | Requerida | Descripción |
| --- | --- | --- |
| `SECRET_KEY` | no | Clave de sesión/CSRF; si está vacía se genera una automática al iniciar |
| `DATABASE_URL` | no | Default `sqlite:///database/gestion_visitas.db` (resuelto a `instance/database/`); PostgreSQL en producción |
| `CLOUDFLARE_TUNNEL` | no | `1` (default) activa el túnel público, `0` lo desactiva |
| `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USERNAME`, `MAIL_PASSWORD` | no | SMTP para recuperación de contraseña y notificaciones (Gmail app password) |
| `MAIL_DEFAULT_SENDER`, `NOTIFY_EMAIL` | no | Remitente y destinatario de las notificaciones automáticas |

## Usuarios por defecto (acceso = DNI)

| DNI | Contraseña | Rol |
|---|---|---|
| 12345678 | admin123 | Administrador |
| 87654321 | super123 | Supervisor |
| 11112222 | opera123 | Operador |
| 99998888 | consul123 | Consultas |

Roles del sistema: **1** Administrador, **2** Supervisor, **3** Operador, **4** Consultas. Cambiar las contraseñas predeterminadas después del primer inicio.

## Producción

```bash
export DATABASE_URL=postgresql://usuario:password@localhost:5432/gestion_visitas
gunicorn -w 4 -b 0.0.0.0:8000 run:app     # Linux/macOS
pip install waitress && waitress-serve --port=8000 run:app   # Windows
```

## Solución de problemas

| Error | Causa / solución |
|---|---|
| `too few arguments to function '_PyLong_AsByteArray'` al instalar pandas | Python 3.13+: crea el venv con Python 3.12 (`uv venv --python 3.12 venv`) |
| `sqlite3.OperationalError: unable to open database file` | Persiste una `DATABASE_URL` heredada del shell: `unset DATABASE_URL` y reinicia |
| `[Errno 13] Permission denied: cloudflared-linux-amd64` | `chmod +x venv/lib/…/pycloudflared/cloudflared-linux-amd64` |

## Changelog

Ver [CHANGELOG.md](./CHANGELOG.md).

---

**Desarrollado por:** azconsultingperu — repositorio de https://github.com/azconsultingperu/sgrv. Proyecto propiedad del IESTP "Paiján".