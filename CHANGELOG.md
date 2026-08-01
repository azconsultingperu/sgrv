# Changelog

Todas las mejoras y correcciones del proyecto SGRV.

## [2026-08-01] — Auditoría y compatibilidad multi-OS

### Agregado
- **`.gitattributes`**: normaliza los saltos de línea a LF en el repositorio para todos los SO. Archivos `.bat`, `.cmd` y `.ps1` de Windows conservan CRLF. Previene conflictos al colaborar entre Linux, Windows y macOS.
- **Sección "Trabajo colaborativo con Git (multi-OS)"** en el README: explica qué se comparte y qué no entre colaboradores de distintos SO, el flujo `push/pull` habitual y advertencias sobre saltos de línea, permisos y rutas.
- **Auto-fix de permisos de cloudflared** (`run.py`): función `_fix_cloudflared_permissions()` que detecta y aplica `chmod +x` automáticamente al binario antes de lanzar el túnel, eliminando el error `[Errno 13] Permission denied` sin necesidad de pasos manuales.

### Corregido
- **`run.py`**: el binario `cloudflared-linux-amd64` ahora recibe permisos de ejecución automáticamente en Linux/macOS. Antes requería ejecutar `chmod +x` a mano tras cada instalación de dependencias.
- **README — IP hardcodeada**: se eliminó la IP `192.168.0.131` (que corresponde a un equipo específico) y se reemplazó por `<tu-IP-local>` para no generar confusión en otros colaboradores.
- **README — Carpeta `views/` inexistente**: se eliminó de la estructura del proyecto porque no existe en el código real.
- **README — Variables de entorno en producción**: la sección solo mostraba `set` de Windows CMD; ahora incluye las variantes para Linux/macOS (`export`) y Windows PowerShell (`$env:`).
- **README — `gunicorn` en Windows**: se aclaró que `gunicorn` no está disponible en Windows y se añadió la alternativa con `waitress`.
- **`.env.example`**: corregidos caracteres con encoding roto (`Ã³`, `Ã©`, `Ã±` → `ó`, `é`, `ñ`) causados por abrir el archivo con codificación incorrecta.
- **`.devcontainer/devcontainer.json`**: imagen actualizada de Python 3.11 a Python 3.12 para alinear con los requisitos de `requirements.txt` (pandas, numpy, etc.).

### Documentado
- **Solución de problemas**: nuevo caso `[Errno 13] Permission denied` en la tabla de errores del README, con el comando `chmod +x` como solución manual de respaldo.
- **Activación del venv en Windows**: se diferencian las variantes PowerShell (`Activate.ps1`) y CMD (`activate.bat`).

## [2026-07-31]

### Agregado
- **URL pública temporal vía túnel Cloudflare**: `run.py` inicia automáticamente un túnel `trycloudflare.com` al arrancar (URL guardada en `logs/tunel.txt`). Se desactiva con `CLOUDFLARE_TUNNEL=0` en el `.env`. Dependencia: `pycloudflared==0.3.0`.
- **Reloj en el navbar**: indicador de fecha y hora en tiempo real en la barra superior, visible en todos los módulos y en cualquier tamaño de pantalla.
- **Barra de fortaleza de contraseña**: indicador con riel visible y relleno progresivo (rojo → amarillo → verde) al crear/editar usuarios y al restablecer contraseña.
- **Labels conectados a inputs**: al hacer clic en "Apellidos", "Celular", etc. se enfoca el campo correspondiente en todos los formularios.
- **Mensajes de datos vacíos**: el KPI "Alumnos por Sexo" y el "Ranking de Colegios Visitados" muestran "Sin datos registrados" cuando no hay información.
- **Opción "Otros" en sexo**: el campo sexo del formulario de registro ahora incluye "Otros" (valor `O`), visible también en el dashboard, consulta, detalle y email de notificación.

### Cambiado
- **SECRET_KEY automática**: si no está definida en `.env`, la app genera una aleatoria al iniciar (antes lanzaba error).
- **Sidebar fijo**: la barra lateral ahora ocupa toda la altura de la ventana, "Cerrar Sesión" queda siempre visible; ancho reducido de 250px a 220px.
- **Estilos de formularios y cards**: estilos `.password-strength` movidos a `style.css` (aplican en todo el sistema, no solo en login); sombras de cards eliminadas a petición del usuario.
- **Graficos del dashboard**: los 4 gráficos usan `maintainAspectRatio: false` con altura fija (300px) y se redibujan al redimensionar la ventana (se corrige la franja blanca al maximizar).
- **Indicador del dashboard**: se reemplazó el timestamp "Última actualización" por el estado "Últimos datos actualizados".

### Corregido
- **Reloj invisible**: el badge del reloj usaba `d-none d-md-inline` (oculto en pantallas <768px) y el código quedaba al final de `main.js`, después de bloques que podían fallar y matarlo; se movió al inicio con `try/catch`.
- **Barra de contraseña invisible** en "Añadir usuario": los estilos solo existían en `auth.css`, que no se cargaba en módulos internos.
- **Espacio sobrante en la barra de contraseña**: el estado verde ocupaba 75% y dejaba un hueco; ahora ocupa el 100%.
- **Dashboard blanco al redimensionar**: Chart.js no redibujaba los gráficos al cambiar el tamaño de ventana; se agregó `chart.resize()` con debounce.

### Seguridad y permisos
- **RBAC aplicado**: solo Administrador y Supervisor pueden registrar/editar visitas; solo Administrador puede eliminar; los roles 1-2 y 4 acceden a reportes.
- **Decoradores centralizados** en `app/utils/decorators.py` (`admin_required`, `supervisor_required`, `admin_or_supervisor_required`, `permiso_requerido`).
- **Sanitización de entrada**: `sanitizar_input` en `app/utils/helpers.py`.
- **Validación de contraseña**: mínima de 8 caracteres (server-side y client-side).

## [2026-07-31] — Instalación y documentación

### Cambiado
- **Guía de instalación generalizada para cualquier sistema operativo**: la documentación explica cada caso por separado (Windows, Linux/Mac) e incluye instrucciones para distros con Python 3.13+ (Arch Linux, Manjaro, Fedora reciente) usando `uv` con Python 3.12, ya que las dependencias fijadas (`pandas==2.1.4`, etc.) no tienen binarios para versiones nuevas de Python y no compilan desde fuente.
- **Nombre del repositorio corregido en toda la documentación**: ahora apunta a `azconsultingperu/sgrv` (antes decía `gestion-registro-visitas` en varias secciones).
- **Nueva sección "Solución de problemas comunes"** en el README con los errores de instalación más frecuentes y su corrección (`ModuleNotFoundError: flask_sqlalchemy`, fallo de compilación de pandas, `unable to open database file`, variables de entorno heredadas).

### Corregido
- **Error `sqlite3.OperationalError: unable to open database file`**: la aplicación ahora crea automáticamente la carpeta `database/` y el archivo SQLite en el primer arranque (`app/__init__.py`), sin pasos manuales; antes fallaba en instalaciones nuevas porque la carpeta no existía en el repositorio.
