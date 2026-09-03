## Why

El formulario de registro tiene 3 campos con reglas no obvias (DNI con futuro RENIEC, celular de 9 dígitos, área como texto libre) y el dashboard tiene métricas sin explicación, donde un `?` con cartelito aclara el "por qué" que el `placeholder` no cubre, sin recargar el resto del sistema.

## What Changes

- Añadir icono `?` (`i[data-lucide="circle-help"]` con `data-bs-toggle="tooltip"`) en `registro/index.html` y `registro/editar.html` para `DNI` ("8 dígitos, se autocompletará vía RENIEC"), `Celular` ("9 dígitos") y `Área Profesional` (texto libre), y en `dashboard/index.html` para 2-3 stat-cards (ej. Tasa de Conversión).
- Reutilizar `bootstrap.Tooltip` ya inicializado en `main.js:219` (hover en desktop, focus/click en móvil) sin nueva dependencia.
- Mantener `?` solo donde hay regla oculta; no añadir en filtros `consulta`/`auditoria` ni en checkboxes ya explícitos.

## Capabilities

### New Capabilities
- `help-tooltip`: Iconos de ayuda contextual con tooltip para campos y métricas con reglas no obvias, con trigger hover/focus y contenido accesible.

### Modified Capabilities
- Ninguna

## Impact

- `app/templates/registro/index.html`, `app/templates/registro/editar.html` — 3 `?` con `data-bs-title`.
- `app/templates/dashboard/index.html` — 2-3 `?` en stat-cards.
- `app/static/css/style.css` — estilo opcional para `circle-help` (tamaño, color muted, hover).
- Sin impacto en backend, `main.js` (ya inicializa tooltips) ni `auth-validation.js`.
