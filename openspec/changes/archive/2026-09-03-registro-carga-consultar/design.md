## Context

Ver `proposal.md` Why. Hoy `POST /registro/` hace `302 /consulta/` y el flash `success` se muestra vía `mostrarToast` inmediato. El usuario no percibe transición y duda. Se quiere spinner grande solo en ese aterrizaje, con toast después.

## Goals / Non-Goals

**Goals:** Spinner grande centrado 800–1200ms solo al aterrizar desde registro/eliminar, luego toast; sin spinner en visitas normales; sin duplicar toast.

**Non-Goals:** No hacer polling real de datos (los datos ya vienen en el HTML del redirect), no bloquear 3s, no spinner en cada visita a consultar, no cambiar backend de guardado.

## Decisions

**Decisión 1: Trigger por flash `success` de registro/eliminación (no por query `?recien`)**
- *Por qué:* El flash ya existe (`Registro creado exitosamente.` / `Registro eliminado correctamente.`) y es el indicador natural de "vengo de registro". Detectarlo en `consultar/index.html` via `flashData` evita ensuciar la URL con `?recien=creado` y evita que el usuario comparta URL con spinner.
- *Alternativa descartada:* Query `?recien=creado` → queda en historial y se puede recargar con spinner infinito; flash se consume solo una vez.

**Decisión 2: Overlay absoluto sobre `.table-responsive` con `spinner-border` 48px**
- *Por qué:* Reutiliza `.confirm-overlay` pero más simple: `position:absolute; inset:0; display:flex; align-items:center; justify-content:center; background:rgba(255,255,255,0.6)` (y `rgba(0,0,0,0.4)` en dark). No bloquea navbar/sidebar, solo la tabla.
- *Alternativa descartada:* Fullscreen overlay → tapa todo y parece que la app se colgó.

**Decisión 3: Duración 800–1200ms (no 3000ms)**
- *Por qué:* 3s es solo decoración y frustra (Nielsen: >1s sin feedback ya se percibe como lento, >2s el usuario quiere abandonar). 1s es suficiente para que el ojo registre "ah, está cargando al nuevo" y luego vea el toast, sin espera real. El spinner es decorativo con función UX, no espera de red.
- *Alternativa descartada:* 3s → decoración pura, penaliza al usuario rápido; 0ms → no se percibe.

**Decisión 4: Orquestación JS `setTimeout` + `mostrarToast`**
- *Por qué:* `consultar/index.html` ya tiene `main.js` con `mostrarToast`. Al detectar flash de registro, se hace `preventDefault` del toast inmediato, se muestra overlay, y tras `setTimeout(1000)` se oculta overlay y se llama `mostrarToast`. Si no hay flash de registro, se deja que `main.js` muestre toasts normales sin delay.
- *Alternativa descartada:* Delay en backend con `sleep` → bloquearía el request 1s innecesariamente.

## Risks / Trade-offs

- **Flash consumido dos veces (main.js y nuevo JS)** → Mitigación: El nuevo JS intercepta antes que `main.js` procese `flashData`; si detecta flash de registro, lo quita del array y lo guarda para mostrar después del spinner.
- **Usuario recarga manualmente durante spinner** → Mitigación: Al recargar, el flash ya se consumió, así que no hay overlay en la segunda carga (comportamiento deseado).
- **Accesibilidad: spinner sin texto** → Mitigación: `aria-live="polite"` y texto "Cargando estudiantes..." visible.

## Migration Plan

- Solo frontend: `consulta/index.html` + `style.css` + `main.js` (o inline JS en consulta). Sin migración. Rollback: quitar overlay y volver a toast inmediato.

## Open Questions

- Ninguna — duración fijada en 1s; si el usuario quiere exactamente 3s se puede parametrizar, pero se desaconseja por UX.
