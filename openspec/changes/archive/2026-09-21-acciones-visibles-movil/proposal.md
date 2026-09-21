## Why

En móviles (verificado con Pixel 7 emulado 360×640 y fotos reales del usuario) los botones de acción no se alcanzan: el scroll vive dentro de `.main-content` (`height:100dvh + overflow-y:auto`) en vez del `body`, así que Chrome móvil no esconde su barra inferior y esta tapa Guardar/Actualizar/Volver aunque se haga scroll; además las tablas miden ~639px en 321px visibles y las columnas de acciones quedan fuera de pantalla. Afecta a todos los roles en todo el sitio.

## What Changes

- En `<=991px` el scroll vuelve al `body` (se retira el scroller interno de `.main-content`) para que Chrome esconda su barra y el final de página sea alcanzable.
- `padding-bottom` con `env(safe-area-inset-bottom)` en el contenedor móvil para compensar la barra de gestos de Android.
- Acciones de tabla siempre alcanzables en móvil: columna de acciones fija visible o su equivalente sin swipe horizontal adivinable.
- Drawer móvil con cierre completo: botón ✕ visible, Escape y swipe, además del backdrop actual.
- Sin cambios en desktop ni en permisos por rol.

## Capabilities

### New Capabilities

- `responsive-movil`: comportamiento móvil del layout — scroll de página, zona segura inferior, acciones de tabla visibles y drawer cerrable en `<=991px`.

### Modified Capabilities

- Ninguna. Lo responsive existente (detalles dispersos en `consulta-listado`, `login-layout`, etc.) no cambia de requisito; se concentra la nueva conducta en la capacidad nueva.

## Impact

- Afectado: `app/templates/base.html` (estructura de scroll), `app/static/css/style.css` (media `<=991px`, safe-area, tablas, drawer), `app/static/js/main.js` (toggle/lock del drawer, `detectarDispositivoMovil`), `partials/sidebar.html` + `partials/navbar.html` (botón ✕), templates con tablas de acciones (consulta, usuarios, reportes, auditoría).
- Riesgo principal: `position: sticky` actuales (navbar, barra de progreso de registro) dependen del scroller interno; al scrollear el body hay que re-anclarlos. Sin migración de BD.
