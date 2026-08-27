## Why

En móviles el card inferior del sidebar (nombre + avatar + icono salir) queda oculto bajo el viewport y solo se ve la parte superior. El sidebar usa `height:100vh` sin `dvh` ni `safe-area`, y el layout `mb-auto` no garantiza que el card sea visible sin scroll en pantallas de 600-700px.

## What Changes

- Cambiar `sidebar` a `height:100dvh` / `min-height:100dvh` con `padding-bottom: env(safe-area-inset-bottom)` para que el fondo llegue al borde real del dispositivo.
- Hacer que `ul.nav` sea el área scrollable (`flex:1 1 auto; min-height:0; overflow-y:auto`) y `sidebar-user` quede anclado con `margin-top:auto; flex-shrink:0;` en vez de depender de `mb-auto` del nav.
- Asegurar que `sidebar-user` nunca quede bajo el home indicator y sea siempre visible sin necesidad de scroll extra en 360px.

## Capabilities

### New Capabilities
- `sidebar-mobile`: Sidebar visible y usable en móvil, con card inferior siempre accesible y respeto de safe-area.

### Modified Capabilities
- _Ninguna_ — fix puntual aislado; no altera `responsive-layout` ni `ui-components` existentes.

## Impact

- **Código afectado:** `app/static/css/style.css` (reglas `.sidebar`, `.sidebar .nav`, `.sidebar-user`) y `app/templates/partials/sidebar.html` (clases de layout). Sin cambios en JS ni backend.
- **Riesgo:** Bajo. Solo CSS de layout móvil; desktop mantiene `244px` fijo y `transform` actual.
