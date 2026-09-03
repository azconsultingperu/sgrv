## 1. CSS — fondo sólido por tipo

- [x] 1.1 Redefinir en `app/static/css/style.css` `.mc-toast` base (sin `border-left-width`/`border-left-color`, con `color:#ffffff`) y las 4 variantes `.mc-toast.error` (`background:var(--danger-color); border-color:var(--danger-color)`), `.success` (`var(--success-color)`), `.warning` (`var(--warning-color)`), `.info` (`var(--info-color)`), cada una con `color:#ffffff`; verificar en DevTools que el fondo es sólido del color de estado y no neutro.

- [x] 1.2 Ajustar en `app/static/css/style.css` `.mc-toast-titulo` y `.mc-toast-descripcion` a `color:#ffffff` (o `rgba(255,255,255,0.92)` para descripción) y `.mc-toast-icono` a `color:#ffffff !important; background:transparent !important;`, y `.mc-toast-cerrar` a `color:rgba(255,255,255,0.92)` con `:hover { color:#ffffff; background:transparent !important; }` sin caja; verificar que ícono y X son blancos sobre fondo sólido.

- [x] 1.3 Mantener/ajustar hover ` .mc-toast:hover { border-color:#ffffff; }` con `transition: border-color 200ms ease` sobre fondo sólido y simplificar/eliminar la regla `[data-bs-theme="light"] .mc-toast` con `box-shadow` reforzada (ya no necesaria) dejando sombra uniforme `var(--shadow-md)`; verificar que el borde blanco aparece sin blur en ambos temas.

## 2. Verificación

- [x] 2.1 Probar `mostrarToast('error'|'success'|'warning'|'info', ...)` en dashboard/registrar/consultar con toggle sol/luna (claro y oscuro) que los 4 tipos muestran fondo sólido de su color, texto/ícono/X blancos, hover con borde blanco 1.2px, y que son idénticos en ambos temas y distinguibles del fondo de la página; hacer bump de `?v=` en `app/templates/base.html` para `style.css` si se editó y verificar recarga.
