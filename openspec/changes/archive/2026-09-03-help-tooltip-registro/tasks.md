## 1. Tooltips en registro

- [x] 1.1 Añadir icono `?` (`i[data-lucide="circle-help"]` con `data-bs-toggle="tooltip"` y `data-bs-title`) junto a los labels de `DNI`, `Celular` y `Área Profesional` en `app/templates/registro/index.html` y replicar en `app/templates/registro/editar.html` con los textos definidos en spec; verificar en DevTools que el `?` aparece al lado del label y que `bootstrap.Tooltip` lo inicializa.

## 2. Tooltips en dashboard

- [x] 2.1 Añadir `?` con tooltip en 2-3 stat-cards de `app/templates/dashboard/index.html` (ej. Tasa de Conversión y Total Registros) con `data-bs-title` explicativo; verificar que el tooltip aparece en hover (desktop) y tap (móvil) sin tapar el `custom-select` y que no se añade en filtros de `consulta`/`auditoria`.

## 3. Verificación

- [x] 3.1 Probar en `registro` y `dashboard` en modo claro y oscuro que los tooltips aparecen con hover/focus, se ocultan al salir, no saturan la UI (solo 3+2), y que `lucide.createIcons()` renderiza el `circle-help`; verificar que no hay regresión en `custom-select` ni `auth-validation.js`.
