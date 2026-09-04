## Why

Al registrar o eliminar un estudiante, el redirect a `/consulta` muestra overlay "Cargando estudiantes..." y luego toast `Registro creado/eliminado` con sonido. Hoy el sonido suena 2 veces: al inicio (toast inmediato de `main.js`) y al final (toast delayed del overlay), cuando la regla es "toda noti suena solo cuando se hace visible". La causa es carrera de scripts: `main.js` lee `flashData` antes que el intercept de `consulta/index.html` la vacíe, así que el guard `window._consultaCargaTrigger` nunca bloquea a tiempo.

## What Changes

- **Sonido 1:1 con toast visible:** Garantizar que `Registro creado/eliminado` suene exactamente 1 vez, solo cuando el toast delayed aparece tras el overlay, nunca durante "Cargando".
- **Carga solo al venir de registrar/eliminar:** Mantener overlay solo en ese caso; visitas directas a `/consulta` siguen con toast inmediato normal + sonido.
- **Fix de carrera:** Reordenar intercept para que corra antes que `main.js` (mover script a `base.html` antes de `main.js` o hacer `main.js` esperar DOMContentLoaded), y asegurar guard bloquea inmediato correctamente.

## Capabilities

### New Capabilities
- Ninguna

### Modified Capabilities
- `consulta-listado`: Comportamiento de notificación con sonido y overlay al aterrizar desde registro/eliminación — corrige doble sonido y timing.

## Impact

- `app/templates/base.html` — mover intercept antes de `main.js` o ajustar orden de scripts (1 línea).
- `app/templates/consulta/index.html` — simplificar intercept (ya no necesita limpiar flashData si base lo hace).
- `app/static/js/main.js` — asegurar guard `window._consultaCargaTrigger` bloquea `Audio` inmediato y solo delayed suena; sin nueva dependencia.
- Sin migración, sin cambio de rutas, sin dependencia nueva. Tests de consulta.
