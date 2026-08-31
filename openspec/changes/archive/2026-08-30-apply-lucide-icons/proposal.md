## Why

Los íconos actuales de Bootstrap Icons se perciben toscos y desactualizados frente al estilo limpio del SGRV (cards compactas, avatares, toasts). Lucide ofrece trazos más finos, consistentes y modernos, elevando la calidad visual sin cambiar layout.

## What Changes

- Reemplazar Bootstrap Icons (`bi-*`) por Lucide (`lucide-*` / `data-lucide`) en toda la app: `base.html`, `partials/sidebar.html`, `partials/navbar.html`, `dashboard/index.html`, `registro/*`, `consulta/*`, `usuarios/*`, `auditoria/*`, `perfil/*`, `auth/*` y cualquier `bi-` restante.
- Cambiar CDN/import: quitar `bootstrap-icons@1.11.2` y cargar Lucide (CDN `https://unpkg.com/lucide@latest` o npm `lucide` con `createIcons`).
- Mapeo 1:1 de íconos (ej. `bi-speedometer2` → `gauge`, `bi-building` → `school`, `bi-people` → `users`, `bi-person-vcard` → `id-card`, `bi-eye` → `eye`, etc.) manteniendo tamaños y clases de color actuales.
- Mantener `Bootstrap Icons` como fallback opcional solo si algún `bi-*` no tiene equivalente directo, pero objetivo es 100% Lucide.

## Capabilities

### New Capabilities
- `lucide-icons`: Sistema de íconos Lucide unificado para toda la UI del SGRV.

### Modified Capabilities
- _Ninguna_ — no altera specs de dominio existentes.

## Impact

- **Código afectado:** `app/templates/base.html` (CDN), `app/static/js/main.js` (inicialización `lucide.createIcons()`), todos los templates con `bi-` (~80 ocurrencias), `app/static/css/style.css` si hay ajustes de tamaño/alineación de íconos.
- **Dependencias:** Cambio de CDN de íconos (sin nueva lógica de negocio).
- **Riesgo:** Bajo, solo visual; sin impacto en rutas, BD o permisos. Requiere purga de caché (`?v=`).
