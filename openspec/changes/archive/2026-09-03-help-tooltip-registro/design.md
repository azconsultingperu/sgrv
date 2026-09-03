## Context

Ver `proposal.md`. `registro/index.html` ya tiene placeholders y `custom-select`/`custom-checkbox`; solo 3 campos tienen regla oculta que el placeholder no cubre. `main.js:219` ya inicializa `bootstrap.Tooltip` para `[data-bs-toggle="tooltip"]`. No hay `?` previos.

## Goals / Non-Goals

**Goals:** 3 `?` en registro + 2-3 en dashboard con tooltip nativo de Bootstrap, sin nueva dependencia, accesible en móvil.
**Non-Goals:** Añadir `?` en cada campo, cambiar validación, tocar backend, traer Tippy/Popper extra.

## Decisions

**1. `circle-help` de Lucide + `data-bs-toggle="tooltip"`**
- Usar `i[data-lucide="circle-help"]` con `class="ms-1"` junto al `label`, con `data-bs-title` con texto. `main.js` ya hace `new bootstrap.Tooltip` para ese selector, por lo que basta con añadir el atributo y re-ejecutar `lucide.createIcons()`.
- Alternativa Tippy descartada: añade peso y tema custom innecesario; Bootstrap ya está y respeta light/dark.

**2. Solo 3 campos en registro + 2 en dashboard**
- `DNI`, `Celular`, `Área Profesional` son los únicos donde el placeholder no explica el efecto (RENIEC, validación 9 dígitos, texto libre). `Modalidad` es opcional pero su tooltip sería redundante con las opciones visibles.
- Dashboard: `Tasa de Conversión` y `Total Registros` son métricas calculadas que confunden sin explicación.

**3. Trigger `hover focus` por defecto de Bootstrap**
- En desktop `hover`, en móvil `tap`/`focus` muestra el tooltip y `blur` lo oculta. No se necesita `click` custom.

## Risks / Trade-offs

- **Tooltip tapado por `custom-select-menu` con `z-index`** → Mitigación: tooltip de Bootstrap usa `z-index:1080` por encima del menú (`1050`), no hay colisión.
- **Demasiados `?` saturan** → Mitigación: limitar a 3+2 como se propone; no añadir en filtros.

## Migration Plan

1. Añadir `i` con `circle-help` y `data-bs-title` en `registro/index.html`, `editar.html` y `dashboard/index.html`.
2. Asegurar `lucide.createIcons()` tras inyección y que `main.js` inicialice tooltips.
3. Probar hover en desktop y tap en móvil que el cartelito aparece y no tapa el `custom-select`.
4. Rollback: quitar los `i` y el tooltip sigue sin romperse.

## Open Questions

- Ninguna.
