## 1. Reloj navbar con AM/PM e iconografía

- [x] 1.1 Actualizar `app/templates/partials/navbar.html` para dividir `#relojNavbar` en spans con icono `clock` + hora + AM/PM + fecha (fecha con `d-none d-sm-inline`) y atributos `title`/`aria-label` iniciales, y verificar que el HTML tiene estructura con spans/icono.
- [x] 1.2 Reescribir `actualizarReloj()` en `app/static/js/main.js` para usar `toLocaleString('es-PE', {hour12:true})` con normalización a `AM/PM`, fecha corta `day month` en español y `title` completo, manteniendo `setInterval 1000`, y verificar que a las 14:05 muestra `02:05 PM` y que `title` contiene fecha larga.
- [x] 1.3 Refinar `.clock-badge` en `app/static/css/style.css` a `inline-flex` con `gap`, `tabular-nums`, hora `font-weight:700` y fecha `text-muted`, y verificar que el badge no vibra al cambiar segundos y que en 375px solo se ve hora.
- [x] 1.4 Verificación E2E: cargar cualquier página autenticada en 1024px y 375px, comprobar que el reloj muestra hora AM/PM + fecha (desktop) / solo hora (móvil), que el hover muestra `title` y que el icono Lucide renderiza.
