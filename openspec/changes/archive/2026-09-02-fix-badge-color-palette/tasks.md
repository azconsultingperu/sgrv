## 1. Auditoría y paleta

- [x] 1.1 Auditar contraste WCAG AA (4.5:1) de cada badge actual (blanco vs fondo) en claro y oscuro con script `contrast()` y documentar tabla; verificar que `warning #b7791f` en claro 3.64 FAIL y todos en oscuro 1.6–2.7 FAIL con `Activo #4ade80` 1.74 como peor caso; guardar captura de tabla para revisión.

- [x] 1.2 Definir paleta propuesta como variables `--badge-success-bg/text`, `--badge-danger-bg/text`, `--badge-warning-bg/text`, `--badge-info-bg/text`, `--badge-primary-bg/text`, `--badge-secondary-bg/text` con hex exactos para `:root` (claro: success #15803c, danger #c2413a, warning #b45309, info #0f7490, primary #2563eb, secondary #475569) y para `[data-bs-theme="dark"]` (success #15803c o #166534, danger #dc2626, warning #b45309, info #0369a1, primary #2563eb, secondary #334155) y verificar con script que cada par vs blanco ≥4.5 y vs fondo de tabla (`#ffffff`/`#161d27`) también ≥4.5; presentar tabla para aprobación.

## 2. Implementación CSS

- [x] 2.1 Añadir variables `--badge-*` en `app/static/css/style.css` en `:root` y `[data-bs-theme="dark"]` y cambiar reglas `.badge.bg-success`, `.bg-danger`, `.bg-warning`, `.bg-info`, `.bg-primary`, `.bg-secondary` para usar `background: var(--badge-*-bg)` y `color: var(--badge-*-text)` en vez de `var(--*-color)` directo; verificar con `grep -n "badge" app/static/css/style.css` y DevTools que los badges usan las nuevas vars.

- [x] 2.2 Verificar colisión visual toast vs badge: mostrar toast de error sólido sobre tabla con badge `Administrador` en ambos temas y confirmar que comparten familia roja pero son distinguibles por forma/sombra/posición; si confunden, documentar matiz alternativo (badge #b91c1c vs toast #dc2626) sin romper contraste.

## 3. Verificación

- [x] 3.1 Probar en `Gestión de Usuarios` (Activo/Inactivo, Administrador/Supervisor/Operador) y otras tablas con badges en modo claro y oscuro que todos los badges pasan contraste percibido (no apagados), el verde Activo ya no se ve deslavado, y el ámbar de Supervisor ya no falla; hacer bump de `?v=` en `app/templates/base.html` para `style.css` y verificar recarga.
