## 1. Infraestructura de íconos

- [x] 1.1 Reemplazar CDN de `bootstrap-icons@1.11.2` por `lucide@latest` en `app/templates/base.html:20` y añadir `lucide.createIcons()` en `app/static/js/main.js` tras `DOMContentLoaded`, y verificar que `GET /` ya no carga `bootstrap-icons.css` y que `data-lucide` se convierte a SVG

## 2. Reemplazo masivo de íconos

- [x] 2.1 Reemplazar todos los `bi-*` por `data-lucide` equivalentes en `app/templates/base.html`, `partials/sidebar.html`, `partials/navbar.html`, `dashboard/index.html`, `registro/*`, `consulta/*`, `usuarios/*`, `auditoria/*`, `perfil/*` y `auth/*`, y verificar con `grep -r "bi-" app/templates` que quede en 0
- [x] 2.2 Ajustar tamaños y colores de Lucide (`class="w-4 h-4"` o `width/height` + `strokeWidth`) para que coincidan con los `bi-*` previos en `stat-icon` y `kpi-band`, y verificar visualmente en 360/1024 que no hay desalineaciones

## 3. Verificación integral

- [x] 3.1 Recargar todas las vistas principales y confirmar que no hay `bi-*` huérfanos, que los toasts y botones mantienen su icono, y ejecutar `FLASK_ENV=testing venv/bin/python -m pytest tests/test_auth.py -q` sin regresión
