## Why

Al completar un registro (o eliminar), el sistema redirige a `consultar` y muestra inmediatamente la tabla con el nuevo dato y un toast `success`. Sin transición, el usuario que viene de un formulario largo no percibe que el listado se actualizó y duda "¿qué hago aquí?". Añadir un estado de carga breve solo en ese aterrizaje, seguido del toast, crea continuidad y confirma que "se está cargando al nuevo usuario".

## What Changes

- **Solo al aterrizar desde registro/eliminar:** `consultar/index.html` muestra un overlay/spinner grande centrado sobre la tabla **solo** cuando la navegación viene de `POST /registro/` o `POST /registro/eliminar` exitoso. En visitas normales a `consultar` no hay spinner.
- **Secuencia:** `POST /registro/` → `302 /consulta?flash=success` → `consultar` detecta flag (flash `success` de registro o query `?recien=creado`) → muestra spinner grande "Cargando estudiantes..." por **800–1200ms** (no 3s) → oculta spinner y dispara `mostrarToast('success', ...)` . Para eliminar, mismo flujo con `danger`/`success` de eliminación.
- **Duración 3s:** 3 segundos es solo decoración y frustra; se fija en **1s** como feedback funcional (suficiente para percibir carga, no para esperar). El spinner es decorativo en sentido técnico (los datos ya llegaron con el HTML), pero funcional en UX (puente cognitivo entre "guardé" y "aquí está").
- **Spinner visual:** Overlay semitransparente sobre `.table-responsive` con `spinner-border` grande (48px) + texto "Cargando estudiantes..." centrado, reutilizando `var(--primary-color)` y sin bloquear el resto del layout.

## Capabilities

### New Capabilities
- Ninguna

### Modified Capabilities
- `consulta-listado`: Añade estado de carga breve al aterrizar desde registro/eliminar antes de mostrar el toast, sin afectar visitas normales.

## Impact

- `app/modules/registro/presentation/registro_controller.py` — añade query `?recien=creado` o deja flash `success` como trigger (sin cambiar lógica de guardado).
- `app/templates/consulta/index.html` — overlay spinner + JS que detecta flag y orquesta spinner → toast.
- `app/static/css/style.css` — estilos para overlay/spinner grande (si hace falta).
- Sin cambios en modelo, sin migración, sin backend extra.
