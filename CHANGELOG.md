# Changelog

Todas las mejoras y correcciones del proyecto SGRV.

## [2026-08-20] — Fase 1: cimientos (tests, migraciones, arranque sin efectos)

### Agregado

- **Suite de tests de regresión (pytest)**: 22 tests sobre los flujos críticos — auth (login, credenciales inválidas, lockout por intentos), registro de alumnos (exitoso, sin promotor, DNI duplicado/inválido, fecha inválida), consulta (lista, detalle 200/404, verificar-dni), usuarios (DNI duplicado, soft-delete oculto en lista) y reportes (CSV/Excel, permisos por rol). Los bugs críticos de agosto quedan congelados como tests.
- **Migración Alembic `c7e1a92f4b30`**: `visitas.promotor_id` pasa a nullable (una visita puede registrarse sin promotor y asignarse después).
- **Comando `flask init-db`**: inicialización explícita de BD para entornos nuevos.

### Cambiado

- **El arranque ya no muta la base de datos en producción** (`INIT_DB_ON_START=False` vía `ProductionConfig` con `FLASK_ENV=production`). `create_all` + seed + parches legacy solo corren en desarrollo o vía `flask init-db`. Reiniciar la app en cPanel deja de ser un evento con efectos sobre la BD.
- Selección de configuración por entorno (`FLASK_ENV`): ProductionConfig / DevelopmentConfig / TestingConfig.
- README: documentados el flujo de migraciones y la suite de tests.

### Corregido (con reproducción y test de regresión)

- **"Observar" un alumno lanzaba error 500 siempre**: `Alumno.query.filter_by(eliminado=False).get_or_404(id)` es inválido en SQLAlchemy 2.x (`Query.get() with existing criterion`). Fix: `first_or_404()` con filtro incluido.
- **Registro silenciosamente fallido sin promotor**: `visitas.promotor_id NOT NULL` + formulario opcional → IntegrityError con rollback total y mensaje invisible. Fix: columna nullable + template None-safe ("No asignado").
- Detalle del alumno tolera visita sin promotor.

---

## [2026-08-17] — Despliegue en producción (cPanel + MySQL)

### Desplegado

- **SGRV en producción**: https://sgrv.azconsultingperu.com — hosting cPanel de FranTech Solutions (PONYNET), servidor `c6`, IP `198.251.89.30`, con Python App + Passenger (Python 3.12).
- **Motor de BD en producción**: MySQL (el hosting no tiene PostgreSQL). Tablas creadas automáticamente por `create_all` al primer arranque con el `.env` configurado; driver `pymysql` añadido al venv del servidor.
- **Datos migrados**: los 507 registros (roles, usuarios, colegios, carreras, promotores, 305 auditorías, 172 sesiones, 10 reportes) exportados desde PostgreSQL local como `datos.sql` (INSERTs con IDs preservados, fechas sin microsegundos, `SET FOREIGN_KEY_CHECKS=0`) e importados en `azconsultingperu_sgrv_visitas`.
- **Acceso al panel**: https://cpanel.azconsultingperu.com (el dominio principal `azconsultingperu.com` sigue en GitHub Pages; los subdominios `cpanel`, `webmail` y `sgrv` apuntan al hosting).

### Configurado en el servidor

- **`.env`** de producción: `DATABASE_URL=mysql+pymysql://...` (contraseña con caracteres especiales URL-encoded), `CLOUDFLARE_TUNNEL=0`, `FLASK_ENV=production`. No se sube al repositorio.
- `passenger_wsgi.py` como punto de arranque de Passenger.

### Verificado

- Login, dashboard y métricas funcionando contra MySQL desde la URL pública.

### Notas de seguridad (a completar por el operador)

- Cambiar `SECRET_KEY` del `.env` por una generada (`secrets.token_hex(32)`).
- Cambiar la contraseña del usuario administrador de fábrica (`12345678`).
- Eliminar `datos.sql` del servidor tras el import (expuesto en la carpeta web).

---

## [2026-08-17] — Preparación para despliegue en cPanel

### Agregado

- **`passenger_wsgi.py`**: punto de arranque para cPanel (Python App + Passenger). Carga `.env`, crea la app Flask en la variable `application` y expone el blueprint de arranque que espera Passenger. Verificado localmente (HTTP 200 contra PostgreSQL).

### Documentado

- **README.md**: nueva subsección «Despliegue en cPanel (Python App + Passenger)» con el paso a paso completo (requisitos del plan, subida excluyendo carpetas locales, creación de BD PostgreSQL, instalación de dependencias, uso de `passenger_wsgi.py` y migración de datos).

---

## [2026-08-17] — Migración de base de datos a PostgreSQL

### Cambiado

- **Motor de base de datos: SQLite → PostgreSQL**. La BD activa del sistema ahora es PostgreSQL (`gestion_visitas`, usuario `sgrv`), definida en `DATABASE_URL` del `.env`. SQLite queda solo como fallback de desarrollo sin servidor.
- **`requirements.txt`**: `psycopg2-binary==2.9.9` ya estaba declarado; instalado y verificado en el entorno.
- **Entorno virtual recreado**: el `venv/` existente estaba roto (apuntaba a la ruta anterior `/home/juan/sgrv` y no era compatible con Python 3.14 del sistema). Recreado con Python 3.12 vía `uv` (`uv venv --python 3.12 venv`) e instaladas todas las dependencias de `requirements.txt`.

### Agregado

- **Base de datos PostgreSQL local** (`gestion_visitas`, owner `sgrv`), con el esquema creado y el versionado Alembic marcado en la revisión `53ea819ab516` (`flask db stamp`), de modo que las migraciones futuras se apliquen sin conflicto.

### Migrado

- **505 filas migradas de SQLite a PostgreSQL** con integridad referencial e IDs originales preservados (crítico para los nombres de archivo de las fotos de perfil y los snapshots de auditoría): 4 roles, 4 usuarios, 6 instituciones educativas, 3 carreras, 3 promotores, 304 auditorías, 171 sesiones, 10 reportes. Verificado: los conteos coinciden 1:1 entre ambos motores y el login de los usuarios seed funciona contra PostgreSQL.

### Documentado

- **README.md**: sección «Base de Datos» reescrita (PostgreSQL como motor principal, pasos para crear usuario/BD, nota de primer arranque con `create_all`, y comando `flask db stamp` para BD nuevas); tabla de solución de problemas con errores comunes de PostgreSQL (`connection refused`, `database does not exist`); estructura del proyecto y tecnologías actualizadas.
- **`.env` / `.env.example`**: `DATABASE_URL` apunta a PostgreSQL, con el formato de conexión documentado y la alternativa SQLite comentada.
- **STRUCTURE.md**: `instance/database/` marcado como backup de la BD original; tabla «Dónde se edita cada cosa» actualizada con la BD activa en PostgreSQL.

### Preservado

- **La BD SQLite original se conserva intacta** en `instance/database/gestion_visitas.db` como respaldo (`instance/` está en `.gitignore`).

---

## [2026-08-09]

### Documentado

- **`STRUCTURE.md` creado**: mapa del repositorio (árbol de carpetas verificado, dónde se edita cada parte y recursos) separado del README.
- **README**: sección «Estructura del Proyecto» reducida a los directorios clave con enlace a `STRUCTURE.md`.

## [2026-08-08] — Corrección de usuarios por defecto contra la BD real

### Fixed

- **Tabla de usuarios por defecto corregida contra la base de datos activa**: se agregó `71184654` (JUAN DAVID RIVERA HUANCAS, Administrador) que sí está registrado en `instance/database/gestion_visitas.db` y faltaba en el README. Se quitó de la tabla el usuario `99998888` (Consultas) que no existe en la BD activa — solo existe en el seed de fábrica (`app/utils/seed.py`), por lo que quedó documentado como nota al pie.

## [2026-08-08] — Optimización de imágenes y auditoría visual multi-pantalla

### Agregado
- **Imágenes en AVIF/WebP**: `logo.png`, `recuperar.png` y `frontis.jpg` convertidos a AVIF/WebP (`app/static/img/`), con ahorro total de ~89% (frontis -87%, logo -86%, recuperar -98%). Los `<picture>` e `image-set()` de las plantillas y `auth.css` ya apuntaban a estos formatos; quedaron operativos. `frontis.avif` re-codificado a `-q 60` (RMSE 0.017 < 0.02). Originales conservados como fallback.
- **Permisos visibles por rol en la UI**: la barra lateral muestra "Registrar" solo a Administrador/Supervisor (antes lo veía también el Operador), y los botones "Nuevo Registro"/"Editar" (consulta y detalle) se ocultan a roles que el backend no autoriza. Antes rol 3/4 veían acciones que fallaban al usarlas.
- **Estados vacíos diferenciados** en consulta y auditoría: "No hay registros todavía" (con CTA "Registrar la primera visita" cuando hay permiso) vs "Sin resultados para los filtros aplicados".
- **Charts del dashboard con datos vacíos**: registros por mes, alumnos por colegio y por distrito muestran overlay "Sin datos registrados" en vez de un gráfico en blanco.
- **Clases de avatar reutilizables** `.avatar-xs` (24px) y `.avatar-sm` (32px) en `style.css`; eliminados los estilos inline de `object-fit` en tablas de usuarios y auditoría. Clase `.profile-table` para el ancho fijo de la columna en "Mi Perfil".

### Cambiado
- `style.css` versionado `?v=40` → `?v=41`.

### Documentado
- **README.md restaurado a la versión completa** (465 líneas, formato tutorial con secciones de Codespaces, instalación por OS, multi-OS colaborativo, roles, módulos, BD, ML y despliegue). Se revirtió el compactado previo al estilo "terse reference", conservando solo lo específico del proyecto.

---

## [2026-08-06] — UX/Accesibilidad: vinculación de inputs con labels en pantallas auth

### Agregado
- **Inputs vinculados con labels (`for`/`id`)** en las 3 vistas de autenticación: `templates/auth/login.html`, `templates/auth/recuperar.html` y `templates/auth/reset_password.html`. Antes los `<label>` no tenían atributo `for`, y los inputs carecían de `id`, por lo que el lector de pantalla y el clic en el label no enfocaban el input. Ahora cada label está vinculado a su input mediante `for="login-username"`, `for="login-password"`, `for="recuperar-username"`, `for="recuperar-email"`, `for="reset-password"` y `for="reset-confirm"` (con `id` correspondiente en cada input). El checkbox "Recordar usuario" ya estaba vinculado correctamente.
- **Card de "Recuperar Contraseña" diferenciada**: añadida la clase `auth-recuperar` al `<div class="login-card">` de la vista de recuperar, y reglas `.login-card.auth-recuperar .card-body { display: flex; flex-direction: column; padding-bottom: 4rem }` + `> form { flex: 1 1 auto }` en `auth.css`. Permite mover los botones "Enviar Instrucciones" / "Volver al Login" usando `mt-auto` (aprovechando el padding inferior existente) **sin** agrandar el card.

### Cambiado
- **`app/templates/auth/login.html`**: el `<form>` interior ahora es `d-flex flex-column h-100`, y los botones están envueltos en `<div class="mt-auto pt-3">` para empujarlos al fondo del card usando el padding-bottom existente (no se añade padding nuevo).
- **`app/templates/auth/recuperar.html`**: idem patrón `mt-auto` en el contenedor de botones. Subtítulo cambiado de "Ingrese sus datos para recuperar el acceso" a "Ingrese sus credenciales para recuperar el acceso".
- **`app/templates/auth/reset_password.html`**: el input "Nueva Contraseña" cambió de `id="password"` a `id="reset-password"` (más descriptivo y único). El JS `checkPasswordStrength()` ya no depende del `id` del input sino que lo recibe por parámetro, así se mantuvo funcional.

### Eliminado
- **`app/templates/auth/login.html`**: eliminada la línea `<p class="auth-tagline">Sistema de Registro de Visitas</p>` del card. La card de login queda más limpia: SGRV → IESTP "Paiján" → descripción → R.M.

### Beneficios
- **Accesibilidad**: clic en el label o Según por teclado ahora enfoca el input correspondiente; lectores de pantalla asocian ambos elementos.
- **Card de recuperar más equilibrada**: botones ya no pegados a los inputs, sin necesidad de padding extra (no crece el card).

---

## [2026-08-05] — UI: centrado de iconos, layout responsive y limpieza de notificaciones redundantes

### Corregido
- **Icono `bi-building` descentrado en su cajita del navbar**: la caja `.navbar-logo` (36×36 px) usaba `display: inline-grid` que no alineaba correctamente el glifo Bootstrap Icons por sus métricas de font y `line-height`. Cambiado a `display: inline-flex` + `align-items: center` + `justify-content: center` + `line-height: 1` para centrar el icono perfectamente tanto en su eje horizontal como vertical. Sin cambios en HTML ni diseño visual.
- **"Últimos datos actualizados" caía debajo de "Dashboard" en mobile**: en `@media (max-width: 767.98px)`, `.page-header` aplicaba `flex-direction: column` que apilaba el `<small class="status-pill">` bajo el título. Reemplazado por `flex-wrap: nowrap` + `align-items: center` + `flex-shrink: 0` en `h4` y `status-pill` para mantener el pill a la derecha del título "Dashboard" en el mismo renglón, incluso en pantallas estrechas.
- **Botón "Iniciar Sesión" se tapaba al final de la página en desktop (viewport bajo)**: `.login-bg` tenía `overflow: hidden` + `min-height: 100vh`, lo que clip-eaba el contenido excedente en laptops con altura reducida. Cambiado a `overflow-x: hidden; overflow-y: auto` para permitir scroll interno y respetar el padding `2rem 0` simétrico (mismo aire arriba y abajo). El botón "Iniciar Sesión" y el motto "¡Crea, Innova e Inspira!" quedan completamente visibles.
- **"¿Olvidó su contraseña?" demasiado cerca del centro en mobile**: en pantallas pequeñas, el `.form-check` "Recordar usuario" empujaba visualmente el link hacia el centro. Añadido `.login-link { margin-left: auto; text-align: right; }` dentro de `@media (max-width: 575.98px)` para anclar el link al lateral derecho.

### Cambiado
- **Notificaciones flash innecesarias removidas**:
  - `app/__init__.py`: eliminado `login_manager.login_message = 'Por favor inicie sesión para acceder.'` junto con `login_message_category`. Esta advertencia aparecía en cada intento de acceso a ruta protegida sin sesión — es información implícita al ser redirigido al login y molestaba.
  - `app/controllers/auth_controller.py:85`: eliminado `flash('Sesión cerrada correctamente.', 'info')`. El logout redirige al login; no es necesaria una confirmación visual cada vez que se cierra sesión.

### Documentado
- **README.md — Sección "Estructura del Proyecto"**: actualizada para reflejar la nueva organización (`templates/perfil/`, `templates/email/`, `static/fonts/`, `static/uploads/`, `instance/database/` como BD activa, `database/` con `.bak` preservado, `.devcontainer/`, y aclaraciones por subcarpeta). Facilita que otros desarrolladores o agentes de IA localicen dónde trabajar por funcionalidad (Login → `controllers/auth_controller.py` + `models/usuario.py` + `templates/auth/`; Dashboard → `controllers/dashboard_controller.py` + `services/estadistica_service.py` + `templates/dashboard/`; etc.).
- **README.md — Nueva sección "Vista previa"**: añadida captura de pantalla del sistema (`app/static/img/exampleSGRV.png`) mostrando el dashboard principal con métricas, gráficos y menú lateral, accesible desde el inicio del README para dar contexto visual inmediato del proyecto.

---

## [2026-08-05] — Reorganización de estructura y consistencia de configuración de BD

### Cambiado
- **`app/templates/perfil.html` → `app/templates/perfil/index.html`**: se movió el template de "Mi Perfil" a su propia carpeta (`perfil/`) para mantener la convención del resto de módulos (`auth/`, `dashboard/`, `registro/`, `consulta/`, `usuarios/`, `auditoria/`, `reportes/`), que ya estaban organizados por funcionalidad. Actualizada la referencia en `perfil_controller.py:76`.
- **`app/config.py` (default de `SQLALCHEMY_DATABASE_URI`)**: la URI por defecto pasó de ruta absoluta (`'sqlite:///' + os.path.join(os.path.dirname(basedir), 'database', 'gestion_visitas.db')`) a ruta relativa (`'sqlite:///database/gestion_visitas.db'`). Flask-SQLAlchemy resuelve las rutas SQLite relativas contra `app.instance_path` (`/home/juan/sgrv/instance/`), por lo que el default ahora apunta a `instance/database/gestion_visitas.db` — la BD activa real — en lugar de bifurcar hacia `database/gestion_visitas.db` (raíz del proyecto).

### Corregido
- **Inconsistencia de configuración de base de datos**: el default de `app/config.py` (ruta absoluta) y `.env.example` (ruta relativa `sqlite:///database/gestion_visitas.db`) apuntaban a **dos bases de datos SQLite distintas**. Una instalación nueva sin `.env` creaba `database/gestion_visitas.db`, mientras que una con `.env` usaba `instance/database/gestion_visitas.db`. Este era el origen de la duplicación de BD observada en el proyecto. Con la corrección, ambos caminos son coherentes y resuelven a `instance/database/gestion_visitas.db` (la BD gestionada por Flask-Migrate, con tabla `alembic_version`).
- **Backup de BD obsoleta**: `database/gestion_visitas.db` (previa a las migraciones, sin `alembic_version`, sin datos reales) fue preservada como `database/gestion_visitas.db.bak` para no perder información histórica. No se eliminó ningún archivo.

### Documentado
- **Sección "Estructura del Proyecto" del README**: actualizada para reflejar la nueva estructura — se añadieron `templates/perfil/`, `templates/email/`, `static/fonts/`, `static/uploads/`, `instance/database/` (BD activa), `database/` (backup `.bak`), `.devcontainer/`, y se aclaró el contenido de cada subcarpeta de templates y static. Facilita que otros desarrolladores o agentes de IA localicen rápidamente dónde trabajar según la funcionalidad.

### Beneficios
- **Localización por funcionalidad**: cualquier agente de IA o desarrollador nuevo puede identificar de un vistazo el código de cada módulo (Login → `controllers/auth_controller.py` + `models/usuario.py` + `templates/auth/`; Dashboard → `controllers/dashboard_controller.py` + `services/estadistica_service.py` + `templates/dashboard/`; etc.).
- **Una sola BD**: se elimina el riesgo de bifurcación de BD por configuración divergente. Con o sin `.env`, la app siempre usará `instance/database/gestion_visitas.db`.
- **Permanencia**: no se modificó lógica de negocio, diseño visual, modelos, migraciones, ni se eliminaron archivos. Sólo se movió 1 template, se cambió 1 línea de configuración y se renombró 1 BD obsoleta a `.bak`.

---

## [2026-08-04] — Fix: foto de perfil no se actualiza + documentación

### Corregido
- **Foto de perfil no se actualiza en "Mi Perfil"** (y en edición de usuarios): la ruta `servir_avatar` devolvía la imagen con `max_age=86400` (24 horas de cache del navegador). Como la URL es solo `/perfil/avatar/<id>` (sin el nombre del archivo), el navegador cacheaba la versión anterior de la foto. Corregido cambiando a `Cache-Control: private, max-age=0, must-revalidate` (revalidación condicional con ETag, sin caché del navegador).
- **Cache-buster en JS del perfil**: `actualizarAvatar()` en `perfil.js` ahora añade `?_=Date.now()` al `src` de la imagen al subir una foto nueva, invalidando cualquier cache residual del navegador.
- **Función `no_cache_html` duplicada** en `__init__.py`: se consolidaron dos funciones idénticas en una sola.

### Cambiado
- **`perfil.js`** versionado: `?v=7` → `?v=8` (perfil.html y usuarios/editar.html).

---

## [2026-08-04] — UI: navbar, sidebar y paginación

### Agregado
- **Navbar rediseñado**: sombra bajo la barra, altura mínima de 58px, cajita con icono institucional (edificio) junto al título, badge del reloj con fondo vítreo, botón hamburguesa destacado y botones outline más visibles. El título "Sistema de Gestión de Registro de Visitas" ahora se muestra **completo en pantallas grandes** (antes se truncaba con "…" siempre por un `max-width` fijo de 200px).
- **Sidebar rediseñado**: items con icono en cajita (32×32, esquinas redondeadas, hover con escala), etiqueta "MENÚ", item activo con gradiente, sombra y barra marcadora lateral, y **footer de usuario** con avatar, nombre, rol y accesos a "Mi Perfil" y "Cerrar Sesión" (el botón de salida ya no está dentro de la lista de enlaces).
- **Paginación inteligente tipo Google**: nuevo partial `partials/paginacion.html` aplicado en **Auditoría y Consulta**. Muestra primera/última página + 2 vecinas de la actual con `…` en los huecos, flechas ‹ › (Anterior/Siguiente) que se deshabilitan en los extremos, y **`…` clicable** que salta al centro del hueco de páginas ocultas (con `title` descriptivo y hover resaltado).
- **Modo oscuro con bordes visibles**: cards, tablas y componentes ahora muestran bordes y separadores con contraste (`--border-color`, superficies `--surface-1/2`) en lugar de desaparecer sobre el fondo; reglas dark para `.card.shadow-sm`/`.border-0` (excepto stat-cards y kpi-bands).
- **Charts del dashboard adaptados al tema**: líneas de grid, ticks y ejes cambian de color al alternar modo claro/oscuro (evento `sgrv:themechange`), antes invisibles en modo oscuro.

### Cambiado
- **Título del navbar responsive**: usa `flex: 1 1 auto` con truncado con ellipsis solo cuando realmente no cabe; en móviles (<576px) el reloj se oculta para dar espacio al título.
- **Hardcodes de color** (`#142e1c`, `#0f2618`, `#1a3d24`, etc.) reemplazados por tokens CSS en card-headers, barras de progreso y modal de confirmación.
- **`style.css`** versionado: `?v=28` → `?v=35`; `main.js` `?v=21` → `?v=23`.

### Corregido
- **Título del navbar cortado** ("Sistema de Gesti…") incluso en pantalla completa: se eliminó el `max-width: 200px` fijo que lo limitaba siempre.
- **Paginador con todos los números** ("1 2 3 … 15 16 17"): con muchas páginas se desbordaba el footer; ahora siempre muestra un máximo de 7 números + flechas.
- **Error de sintaxis Jinja** en el partial de paginación (`ns.shown.append` → `ns.shown + [p]`).

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
