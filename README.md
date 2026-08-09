# SISTEMA DE GESTIÓN DE REGISTRO DE VISITAS (SGRV)

## IESTP "Paiján"

Sistema web para registrar y gestionar las visitas realizadas por promotores institucionales a colegios de 5to de secundaria, con el objetivo de generar una base de datos para analizar, segmentar y predecir potenciales estudiantes interesados en estudiar en el Instituto de Educación Superior Tecnológico Público "Paiján".

---

## Vista previa

![Vista previa del SGRV — Dashboard principal](app/static/img/exampleSGRV.png)

_Vista del sistema en producción: dashboard con métricas, gráficos estadísticos y menú lateral._

---

## Características

- **Dashboard interactivo** con gráficos estadísticos y métricas en tiempo real
- **Registro de visitas** con formulario inteligente y validaciones
- **Búsqueda avanzada** con filtros múltiples y paginación inteligente
- **Gestión de usuarios** con 3 roles (Administrador, Supervisor, Operador)
- **Auditoría completa** de todas las acciones del sistema
- **Reportes exportables** en CSV y Excel
- **Modo oscuro/claro** con persistencia de preferencia
- **Diseño responsive** adaptado a dispositivos móviles
- **Seguridad**: contraseñas hasheadas, sesiones protegidas, CSRF, validación de intentos fallidos
- **Mi Perfil**: gestión de foto de perfil con upload, vista previa en tiempo real y eliminación
- **Soft delete**: eliminación lógica de usuarios y registros (no se borran datos de la base)

---

## Tecnologías

### Backend
- Python 3.10 – 3.12
- Flask 3.0
- SQLAlchemy 2.0
- Flask-Login
- Flask-WTF (CSRF)
- Flask-Migrate

### Frontend
- HTML5
- CSS3
- JavaScript (ES6+)
- Bootstrap 5.3
- Chart.js 4.4
- Bootstrap Icons

### Base de Datos
- SQLite (desarrollo)
- PostgreSQL (producción)

### Control de Versiones
- Git
- GitHub

---

## Estructura del Proyecto

El mapa completo del repositorio (árbol de carpetas, dónde se edita cada cosa y recursos) vive en [STRUCTURE.md](STRUCTURE.md). Resumen de los directorios clave:

- `app/controllers/` — rutas HTTP (blueprints)
- `app/models/` — modelos SQLAlchemy
- `app/templates/` — plantillas Jinja2
- `app/services/` — lógica de negocio (auditoría, email, estadística, reporte)
- `app/utils/` — helpers, decorators, seed
- `instance/database/` — BD SQLite activa (runtime)
- `migrations/` — migraciones Alembic (Flask-Migrate)

---

## GitHub Codespaces (recomendado para probar desde el navegador)

1. Ir a https://github.com/azconsultingperu/sgrv
2. Click en **"Code"** → **"Open with Codespaces"** → **"New codespace"**
3. Esperar a que se configure el entorno automáticamente (~2 min)
4. La app se iniciará sola y se abrirá una vista previa en `http://localhost:5000`
5. Si no se abre, ejecuta manualmente: `python run.py`


> **Credenciales predeterminadas:** Usuario: `12345678` / Contraseña: `admin123`

---

## Instalación Local

### 1. Requisitos previos

- Python 3.10, 3.11 o **3.12** (ver advertencia abajo)
- Git
- Navegador web moderno

> **⚠ IMPORTANTE:** usa Python **3.10 – 3.12** para el entorno virtual. Con **Python 3.13 o superior** (por ejemplo el Python por defecto de Arch Linux, Manjaro o Fedora reciente) la instalación falla al compilar `pandas==2.1.4` desde el código fuente, porque no existen binarios precompilados para esas versiones y el compilador no las soporta. Ver [Solución de problemas](#7-solución-de-problemas-comunes).

### 2. Clonar el repositorio

```bash
git clone https://github.com/azconsultingperu/sgrv.git
cd sgrv
```

### 3. Crear entorno virtual

**Si tu Python es 3.10 – 3.12 (Debian/Ubuntu, Fedora, macOS, Windows):**
```bash
python -m venv venv
```

**Si tu Python es 3.13 o superior (Arch Linux, Manjaro, Fedora reciente):**
```bash
uv venv --python 3.12 venv
```
> `uv` instala Python 3.12 automáticamente dentro del venv sin tocar el sistema.  
> Si no lo tienes: `sudo pacman -S uv` (Arch/Manjaro), `sudo apt install uv` (Debian/Ubuntu), `sudo dnf install uv` (Fedora) o desde [docs.astral.sh/uv](https://docs.astral.sh/uv/).

> **¿Qué hace `python -m venv venv`?** Crea una carpeta `venv/` con un Python aislado del sistema, para que las librerías del proyecto no interfieran con las de tu equipo.

**Activar el entorno virtual:**

```bash
# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Windows (CMD)
venv\Scripts\activate.bat

# Linux / macOS
source venv/bin/activate
```

> ⚠ Si creaste el venv con `uv`, este **no incluye `pip`** (daría `error: externally-managed-environment`); en el paso 5 usa `uv pip install` en su lugar.

### 4. Configurar variables de entorno

```bash
# Windows (PowerShell o CMD)
copy .env.example .env

# Linux / macOS
cp .env.example .env
```

> **Nota:** Si `SECRET_KEY` se deja vacía, la aplicación genera una automáticamente en cada inicio (solo para desarrollo).
>
> **No necesitas crear nada manualmente:** la aplicación crea automáticamente la carpeta `database/` y el archivo de la base de datos en el primer arranque (funciona igual en Windows, Linux y macOS).

### 5. Instalar dependencias

```bash
pip install -r requirements.txt
```

> **Windows:** si `pip` no está en el PATH, usa:
> ```bash
> python -m pip install -r requirements.txt
> ```
>
> **Si creaste el venv con `uv`** (distros con Python 3.13+):
> ```bash
> uv pip install -r requirements.txt
> ```

### 6. Ejecutar la aplicación

```bash
python run.py
```

La aplicación se iniciará en:
- `http://localhost:5000` (local)
- `http://<tu-IP-local>:5000` (red local, la IP varía según tu equipo)
- `https://XXXX.trycloudflare.com` (URL pública temporal vía túnel Cloudflare)

> **URL temporal:** al iniciar, la app crea automáticamente un túnel de Cloudflare para acceder desde cualquier dispositivo con internet. La URL se muestra en la consola y se guarda en `logs/tunel.txt`. Expira al cerrar el servidor. La primera vez descarga el binario de cloudflared (~52 MB).
>
> Para desactivar el túnel: `CLOUDFLARE_TUNNEL=0` en el `.env`.

> **Linux:** si aparece `[Errno 13] Permission denied` al iniciar el túnel, ejecuta una sola vez:
> ```bash
> chmod +x venv/lib/python3.12/site-packages/pycloudflared/cloudflared-linux-amd64
> ```

### 7. Solución de problemas comunes

| Error | Causa | Solución |
|---|---|---|
| `ModuleNotFoundError: No module named 'flask_sqlalchemy'` | No se activó el entorno virtual o no se instalaron las dependencias | Activa el venv (`source venv/bin/activate` / `venv\Scripts\activate`) y ejecuta `pip install -r requirements.txt` |
| `error: too few arguments to function '_PyLong_AsByteArray'` al instalar `pandas` | Python 3.13+ no es compatible con las versiones fijadas en `requirements.txt` (no existen binarios precompilados y no compilan desde fuente) | Crea el entorno virtual con Python 3.12: `uv venv --python 3.12 venv` (o instala `python312` con tu gestor de paquetes) |
| `[Errno 13] Permission denied: '…/cloudflared-linux-amd64'` | El binario de Cloudflare no tiene permiso de ejecución (solo ocurre en Linux) | `chmod +x venv/lib/python3.12/site-packages/pycloudflared/cloudflared-linux-amd64` |
| `sqlite3.OperationalError: unable to open database file` | Estás usando una versión antigua del proyecto (las versiones nuevas crean la carpeta `database/` automáticamente) | Actualiza el proyecto: `git pull` |
| El error anterior persiste | Hay una variable `DATABASE_URL` con ruta inválida en la terminal (si antes pegaste un comando `DATABASE_URL=...`) | Ejecuta `unset DATABASE_URL` (Linux/macOS) o cierra y vuelve a abrir la terminal (Windows), y vuelve a arrancar |

---

## Trabajo colaborativo con Git (multi-OS)

Este proyecto es seguro de usar en equipo con colaboradores que usen **diferentes sistemas operativos** (Linux, Windows, macOS), siempre que se respeten estas consideraciones:

### ¿Qué NO se comparte entre colaboradores?

Los siguientes elementos están en `.gitignore` y **no se sincronizan** con Git (cada colaborador los configura localmente):

| Elemento | Motivo |
|---|---|
| `venv/` | El entorno virtual es específico de cada OS y versión de Python |
| `.env` | Contiene datos sensibles (claves, contraseñas) |
| `database/*.db` | La base de datos SQLite de desarrollo es local |
| `logs/` | URLs de túnel temporales, no se comparten |
| `instance/` | Carpeta interna de Flask, generada automáticamente |

### ¿Qué SÍ se comparte?

Todo el código fuente: `app/`, `migrations/`, `run.py`, `requirements.txt`, `.env.example`, `README.md`, etc.

### Flujo de trabajo habitual

```
# Colaborador A (Linux) hace cambios y los sube:
git add .
git commit -m "feat: nueva funcionalidad"
git push

# Colaborador B (Windows) recibe los cambios:
git pull
# Si se agregaron nuevas dependencias:
pip install -r requirements.txt
# Si hay nuevas migraciones:
python -m flask db upgrade
# Ejecutar:
python run.py
```

### Advertencias cross-OS

| Situación | Detalle |
|---|---|
| **Saltos de línea** | Git en Windows puede convertir LF → CRLF. Para evitar problemas, el colaborador Windows debe ejecutar: `git config --global core.autocrlf true` |
| **Permisos de archivos** | Los archivos ejecutables (como el binario de cloudflared) pueden perder sus permisos al pasar por Windows. Si esto ocurre en Linux/macOS, ejecuta el `chmod +x` de la sección anterior. |
| **Rutas de archivos** | El proyecto usa `os.path.join` y `pathlib.Path`, que son compatibles con todos los sistemas operativos. No hay rutas hardcodeadas. |
| **Python y venv** | Cada colaborador debe crear su propio `venv` localmente con la versión de Python compatible. |

---

## Usuarios por defecto

| Usuario (DNI) | Contraseña | Rol            |
|---------------|-----------|----------------|
| 12345678      | admin123  | Administrador  |
| 71184654      | (creada por el administrador) | Administrador (Juan D. R. Huancas) |
| 87654321      | super123  | Supervisor     |
| 11112222      | opera123  | Operador       |

> **Nota**: El usuario de acceso es el **DNI**. Cambie estas credenciales inmediatamente después del primer inicio de sesión.
>
> La tabla anterior refleja los usuarios presentes en la base de datos activa (`instance/database/gestion_visitas.db`). El seed de fábrica (`app/utils/seed.py`) además prevé un usuario de consultas (`99998888` / `consul123`) que solo aplica al recrear la BD desde cero.

---

## Roles y Permisos

### Administrador (rol 1)
- Acceso total al sistema
- Gestión de usuarios (crear, editar, eliminar)
- Gestión de auditoría
- Eliminación de registros (eliminación lógica)

### Supervisor (rol 2)
- Registrar visitas
- Consultar registros
- Editar registros
- Generar reportes

### Operador (rol 3)
- Registrar visitas
- Consultar registros

### Consultas (rol 4)
- Consultar registros
- Ver reportes

---

## Módulos del Sistema

### 1. Login
- Autenticación por DNI y contraseña
- Mostrar/ocultar contraseña
- Recordar sesión
- Recuperación de contraseña
- Bloqueo por intentos fallidos

### 2. Dashboard
- Métricas principales (totales)
- Gráficos interactivos (Chart.js)
- Alumnos por colegio, distrito, sexo
- Edad promedio
- Registros del día, semana, mes
- Ranking de colegios visitados
- Proyección de postulantes

### 3. Registrar
- Formulario completo de registro
- Validación de DNI único
- Cálculo automático de edad
- Fecha y hora automática
- Verificación de duplicados

### 4. Consultar
- Búsqueda por múltiples criterios
- Filtros combinados
- Paginación inteligente de resultados (1 … N con elipsis clicable)
- Ver detalle, editar, eliminar

### 5. Usuarios
- CRUD completo de usuarios
- Asignación de roles
- Control de estado (activo/inactivo)
- Indicador visual de fortaleza de contraseña al crear/editar
- Cambio de contraseña obligatorio en el primer inicio (según política)
- Foto de perfil con upload, vista previa y eliminación
- Avatar por defecto con iniciales generadas automáticamente
- Snapshots históricos de foto de perfil en auditoría

### 6. Auditoría
- Registro automático de acciones
- Filtros por usuario, acción, módulo, fecha
- Seguimiento de IP y user-agent
- Paginación inteligente (1 … N con elipsis clicable)
- Snapshot de la foto de perfil del usuario en el momento de cada acción

### 7. Reportes
- Exportación a CSV
- Exportación a Excel
- Reportes de alumnos, visitas, colegios, carreras

---

## Base de Datos

### Tablas principales

- `usuarios` - Usuarios del sistema
- `roles` - Roles y permisos
- `alumnos` - Alumnos registrados (con eliminación lógica: `eliminado`, `fecha_eliminacion`)
- `instituciones_educativas` - Colegios
- `visitas` - Registro de visitas
- `promotores` - Promotores institucionales
- `auditorias` - Registro de auditoría
- `sesiones` - Sesiones de usuario
- `carreras` - Carreras profesionales
- `reportes` - Reportes generados
- `dashboard_estadisticas` - Estadísticas del dashboard

### Migraciones

El proyecto usa Alembic (Flask-Migrate). Para aplicar migraciones:

```bash
python -m flask db upgrade
```

> **Nota:** la base de datos usa SQLite por defecto (`database/gestion_visitas.db`); no requiere servidor externo.

---

## Preparado para Machine Learning

El sistema incluye tablas y estructura de datos preparada para implementar modelos predictivos:

- Regresión Logística
- Random Forest
- Decision Tree
- KNN
- XGBoost

### Indicadores predictivos disponibles:
- Probabilidad de postulación
- Probabilidad de matrícula
- Segmentación de alumnos
- Ranking de captación

---

## Despliegue en Producción

### Configuración para PostgreSQL

1. Instalar PostgreSQL
2. Crear base de datos:
```sql
CREATE DATABASE gestion_visitas;
```
3. Configurar la variable de entorno `DATABASE_URL`:

```bash
# Linux / macOS
export DATABASE_URL=postgresql://usuario:password@localhost:5432/gestion_visitas

# Windows (PowerShell)
$env:DATABASE_URL="postgresql://usuario:password@localhost:5432/gestion_visitas"

# Windows (CMD)
set DATABASE_URL=postgresql://usuario:password@localhost:5432/gestion_visitas
```

> **Recomendado:** define esta variable directamente en el archivo `.env` para que persista entre sesiones.

### Servidor de producción

```bash
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

> `gunicorn` solo está disponible en Linux/macOS. En Windows puedes usar `waitress`:
> ```bash
> pip install waitress
> waitress-serve --port=8000 run:app
> ```

---

## Licencia

Este proyecto es propiedad del Instituto de Educación Superior Tecnológico Público "Paiján".

---

## Contacto

**Desarrollado por:** azconsultingperu  
**GitHub:** [https://github.com/azconsultingperu](https://github.com/azconsultingperu)  
**Repositorio:** [https://github.com/azconsultingperu/sgrv](https://github.com/azconsultingperu/sgrv)
