## Why

Los badges de estado/rol (Activo, Administrador, Supervisor, Operador) usan `var(--success-color)` etc. con texto blanco, pero en modo oscuro los colores son pastel (`#4ade80`, `#f87171`...) y el contraste vs blanco cae a 1.6–2.7 (WCAG AA requiere 4.5:1). El verde de "Activo" (#4ade80 vs blanco 1.74) es el peor caso y se ve apagado sobre `var(--surface-1)` #161d27. En modo claro solo el ámbar de Supervisor falla (3.64). Además el rojo de Administrador comparte tono con los toasts de error sólidos, lo que puede confundir si ambos aparecen juntos.

## What Changes

- Auditar contraste WCAG AA (4.5:1) de cada badge actual (texto blanco vs fondo) en claro y oscuro, identificando fallos.
- Definir paleta de estado reutilizable para cualquier badge/etiqueta futura (success=verde, danger/admin=rojo, warning/supervisor=ámbar, info/operador=azul, primary/secondary) como variables CSS dedicadas `--badge-*` con variante por tema que preserve identidad de marca pero cumpla contraste.
- Proponer valores hex exactos para claro y oscuro que pasen 4.5:1 vs blanco y se distingan del fondo de tabla (`#ffffff` en claro, `#161d27` en oscuro).
- Verificar que el rojo de badges no choque con el rojo de toasts sólidos; documentar si pueden compartir tono o necesitan matiz distinto.

## Capabilities

### New Capabilities
- `badge-system`: Paleta y contrato visual de badges/etiquetas de estado/rol (success, danger, warning, info, primary, secondary) con variables por tema, contraste AA y uso consistente en tablas, toasts y futuros componentes.

### Modified Capabilities
- Ninguna — no existe spec previo de badges; `notifications` (toasts) no se modifica en requisitos, solo se audita colisión visual.

## Impact

- `app/static/css/style.css` — nuevas vars `--badge-success-bg/text` etc. en `:root` y `[data-bs-theme="dark"]`, y reglas `.badge.bg-*` que las consumen en vez de `var(--success-color)` directo.
- `app/templates/usuarios/index.html` y otras tablas con `badge` — sin cambio de markup, solo CSS.
- Sin impacto en backend, `notifications` o `toast-system` salvo verificación visual de coexistencia toast+badge.
