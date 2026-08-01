# SISTEMA DE GESTIÓN DE REGISTRO DE VISITAS (SGRV)

## IESTP "Paiján"

Sistema web para registrar y gestionar las visitas realizadas por promotores institucionales a colegios de 5to de secundaria, con el objetivo de generar una base de datos para analizar, segmentar y predecir potenciales estudiantes interesados en estudiar en el Instituto de Educación Superior Tecnológico Público "Paiján".

---

## Características

- **Dashboard interactivo** con gráficos estadísticos y métricas en tiempo real
- **Registro de visitas** con formulario inteligente y validaciones
- **Búsqueda avanzada** con filtros múltiples
- **Gestión de usuarios** con 3 roles (Administrador, Supervisor, Operador)
- **Auditoría completa** de todas las acciones del sistema
- **Reportes exportables** en CSV y Excel
- **Modo oscuro/claro** con persistencia de preferencia
- **Diseño responsive** adaptado a dispositivos móviles
- **Seguridad**: contraseñas hasheadas, sesiones protegidas, CSRF, validación de intentos fallidos

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

```
sgrv/
├── app/
│   ├── controllers/     # Controladores (blueprints)
│   ├── models/          # Modelos SQLAlchemy
│   ├── views/           # Vistas (reservado)
│   ├── templates/       # Plantillas HTML
│   │   ├── auth/        # Login, recuperar contraseña
│   │   ├── dashboard/   # Dashboard principal
│   │   ├── registro/    # Registro y edición de visitas
│   │   ├── consulta/    # Búsqueda y detalle
│   │   ├── usuarios/    # Gestión de usuarios
│   │   ├── auditoria/   # Registro de auditoría
│   │   ├── reportes/    # Generación de reportes
│   │   ├── errors/      # Páginas de error
│   │   └── partials/    # Componentes reutilizables
│   ├── static/
│   │   ├── css/         # Estilos personalizados
│   │   ├── js/          # Scripts del frontend
│   │   └── img/         # Imágenes
│   ├── services/        # Lógica de negocio
│   ├── utils/           # Utilidades y seed data
│   └── config.py        # Configuración de la aplicación
├── database/            # Archivos de base de datos
├── migrations/          # Migraciones de base de datos
├── logs/                # URL temporal del túnel (logs/tunel.txt)
├── requirements.txt     # Dependencias del proyecto
├── run.py               # Punto de entrada
├── .env.example         # Plantilla de variables de entorno
├── .gitignore           # Archivos ignorados por Git
├── CHANGELOG.md         # Registro de cambios
└── README.md            # Este archivo
```

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

```bash
python -m venv venv
```

> **¿Qué hace?** Crea una carpeta `venv/` con un Python aislado del sistema, para que las librerías del proyecto no se mezclen con las de tu equipo.

**Si tu Python es 3.10 – 3.12 (Debian/Ubuntu, Fedora, etc.):**
```bash
python -m venv venv
```

**Si tu Python es 3.13 o superior (por ejemplo Arch Linux, Manjaro, Fedora reciente):**
```bash
uv venv --python 3.12 venv
```
> por tal caso: las librerías del proyecto solo funcionan con Python 3.12, y `uv` lo instala automáticamente dentro del venv sin tocar tu sistema. Si no lo tienes, instálalo según tu distro: `sudo pacman -S uv` (Arch/Manjaro), `sudo apt install uv` (Debian/Ubuntu), `sudo dnf install uv` (Fedora) o desde [docs.astral.sh/uv](https://docs.astral.sh/uv/).

**Activar el entorno virtual:**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

> ⚠ Si creaste el venv con `uv`, este **no incluye `pip`** (daría `error: externally-managed-environment`); en el paso 5 usa `uv pip install` en su lugar.

### 4. Configurar variables de entorno

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

> **Nota:** Si `SECRET_KEY` se deja vacía, la aplicación genera una automáticamente en cada inicio (solo para desarrollo).

> **⚠ Importante:** crea la carpeta `database/` **antes de ejecutar la aplicación**. No viene en el repositorio (sus archivos `.db` están en `.gitignore`) y SQLite **no la crea automáticamente** — sin ella la app falla al iniciar con `sqlite3.OperationalError: unable to open database file`:
> ```bash
> mkdir -p database
> ```
>
> Si vas a ejecutar la app desde otro directorio o sigues teniendo el error, cambia en tu `.env` la variable `DATABASE_URL` a una **ruta absoluta**:
> ```bash
> DATABASE_URL=sqlite:////ruta/absoluta/al/proyecto/database/gestion_visitas.db
> ```

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
- `http://192.168.0.131:5000` (red local)
- `https://XXXX.trycloudflare.com` (URL pública temporal vía túnel Cloudflare)

> **URL temporal:** al iniciar, la app crea automáticamente un túnel de Cloudflare para acceder desde cualquier dispositivo con internet. La URL se muestra en la consola y se guarda en `logs/tunel.txt`. Expira al cerrar el servidor. La primera vez descarga el binario de cloudflared (~52 MB).
>
> Para desactivar el túnel: `CLOUDFLARE_TUNNEL=0` en el `.env`.

### 7. Solución de problemas comunes

| Error | Causa | Solución |
|---|---|---|
| `ModuleNotFoundError: No module named 'flask_sqlalchemy'` | No se activó el entorno virtual o no se instalaron las dependencias | Activa el venv (`source venv/bin/activate`) y ejecuta `pip install -r requirements.txt` |
| `error: too few arguments to function '_PyLong_AsByteArray'` al instalar `pandas` | Python 3.13+ no es compatible con las versiones fijadas en `requirements.txt` (no existen binarios precompilados y no compilan desde fuente) | Crea el entorno virtual con Python 3.12: `uv venv --python 3.12 venv` (o instala `python312` con tu gestor de paquetes) |
| `sqlite3.OperationalError: unable to open database file` | La carpeta `database/` no existe (está en `.gitignore`) y SQLite no la crea automáticamente | `mkdir -p database` y vuelve a ejecutar |
| El error anterior persiste | La `DATABASE_URL` del `.env` es una ruta relativa y la app se ejecuta desde otro directorio | Usa una ruta absoluta en `.env`: `DATABASE_URL=sqlite:////ruta/absoluta/al/proyecto/database/gestion_visitas.db` |

---

## Usuarios por defecto

| Usuario (DNI) | Contraseña | Rol            |
|---------------|-----------|----------------|
| 12345678      | admin123  | Administrador  |
| 87654321      | super123  | Supervisor     |
| 11112222      | opera123  | Operador       |
| 99998888      | consul123 | Consultas      |

> **Nota**: El usuario de acceso es el **DNI**. Cambie estas credenciales inmediatamente después del primer inicio de sesión.

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
- Paginación de resultados
- Ver detalle, editar, eliminar

### 5. Usuarios
- CRUD completo de usuarios
- Asignación de roles
- Control de estado (activo/inactivo)
- Indicador visual de fortaleza de contraseña al crear/editar
- Cambio de contraseña obligatorio en el primer inicio (según política)

### 6. Auditoría
- Registro automático de acciones
- Filtros por usuario, acción, módulo, fecha
- Seguimiento de IP y user-agent

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
3. Configurar variables de entorno:
```bash
set DATABASE_URL=postgresql://usuario:password@localhost:5432/gestion_visitas
```

### Servidor de producción

```bash
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

---

## Licencia

Este proyecto es propiedad del Instituto de Educación Superior Tecnológico Público "Paiján".

---

## Contacto

**Desarrollado por:** azconsultingperu
**GitHub:** [https://github.com/azconsultingperu](https://github.com/azconsultingperu)
**Repositorio:** [https://github.com/azconsultingperu/sgrv](https://github.com/azconsultingperu/sgrv)
