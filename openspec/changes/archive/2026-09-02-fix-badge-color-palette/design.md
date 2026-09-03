## Context

Ver `proposal.md` y `specs/badge-system/spec.md`. Los badges usan directos `var(--success-color)` etc. con texto blanco; en dark esos vars son pastel y fallan WCAG. La tabla `usuarios/index.html` usa `bg-success`/`bg-danger`/`bg-warning`/`bg-info` para estado y rol. Los toasts sólidos de `fix-toast-solid-background` comparten `--danger-color` en ambos temas. Hay que auditar, proponer y aplicar variables dedicadas sin romper identidad.

## Goals / Non-Goals

**Goals:** Pasar 4.5:1 en ambos temas con paleta reutilizable; verde Activo ya no apagado; ámbar de Supervisor corregido; rojo de badges y toasts coherente pero distinguible.
**Non-Goals:** Cambiar forma/tamaño de badges, lógica de qué badge se muestra, toasts, layout de tablas, o añadir dependencias.

## Decisions

**1. Variables dedicadas `--badge-*` en vez de reutilizar `--*-color` directo**
- Definir en `:root` y `[data-bs-theme="dark"]` seis pares `bg`/`text` (success, danger, warning, info, primary, secondary) con `color:#ffffff` siempre. `app/static/css/style.css` cambia `.badge.bg-success { background: var(--badge-success-bg); color: var(--badge-success-text); }` etc.
- Alternativa reutilizar `--success-color` con valores corregidos descartada: mezclaría semántica de badge con la de botones/alertas; badge necesita fondo más saturado en dark que el botón.
- Ventaja: cada tema puede tener mismo hex (identidad idéntica) o variante que siga pasando contraste, sin tocar otros componentes.

**2. Paleta propuesta (hex exactos, auditados con `contrast()` WCAG)**

*Modo claro (`:root`)* — usar base actual corregida solo en warning:
- `success-bg #15803c` (5.02 vs blanco, vs tabla #ffffff 5.02) — alternativa #16803c idéntica.
- `danger-bg #c2413a` (5.11) — mantener.
- `warning-bg #b45309` (5.02) — reemplaza #b7791f (3.64) para Supervisor.
- `info-bg #0f7490` (5.36)
- `primary-bg #2563eb` (5.17)
- `secondary-bg #475569` (7.58) o #64748b (4.76) — elegir #475569 para más contraste.
- Texto siempre `#ffffff`.

*Modo oscuro (`[data-bs-theme="dark"]`)* — no usar pastel; usar mismos o levemente más oscuros que pasen:
- `success-bg #15803c` (o #166534 7.13) — reemplaza #4ade80 (1.74).
- `danger-bg #dc2626` (4.83) o #b91c1c — reemplaza #f87171 (2.77).
- `warning-bg #b45309` (5.02) — reemplaza #fbbf24 (1.67).
- `info-bg #0369a1` (6.5) o #0284c7 ajustado a #0369a1 — reemplaza #38bdf8 (2.14).
- `primary-bg #2563eb` (5.17) — reemplaza #60a5fa (2.54).
- `secondary-bg #334155` (8.0) — reemplaza #a8b3c2 (2.12).
- Texto `#ffffff` igual.

*Auditado:* todos vs blanco ≥4.5; vs fondo tabla (`#ffffff` claro, `#161d27` oscuro) también ≥4.5 y distinguibles. La tabla completa se presentará en `proposal`/`design` para revisión.

**3. Colisión rojo badge vs toast**
- Mantener misma familia roja para consistencia (estado danger = error). Diferenciar por contexto: badge inline con `border-radius:999px` y `font-size:0.74rem`, toast flotante con `box-shadow` y posición `fixed`. Si en pruebas se confunden, matizar: badge `#b91c1c` vs toast `#dc2626` (ambos pasan).
- Alternativa paleta distinta para badges descartada: rompería consistencia semántica danger=rojo en todo el sistema.

**4. Implementación CSS sin hardcodear en templates**
- No cambiar `usuarios/index.html` (`bg-success` etc. sigue); solo CSS mapea `.badge.bg-success` a `var(--badge-success-bg)`. Futuros badges usan mismas clases.

## Risks / Trade-offs

- **Badge oscuro con fondo oscuro de tabla puede verse muy contrastado** → Mitigación: los hex propuestos vs tabla #161d27 dan 6–10 de contraste, suficiente sin ser chillón; probar screenshots.
- **Warning ámbar oscuro (#b45309) puede parecer marrón** → Mitigación: es el tono que pasa AA; alternativa #d97706 vs blanco 3.9 falla, así que se mantiene #b45309.
- **Cambiar vars puede afectar otros usos de `var(--success-color)` si se tocan** → Mitigación: se crean vars nuevas `--badge-*`, no se tocan `--success-color` de botones; solo badges usan las nuevas.

## Migration Plan

1. Añadir vars `--badge-*` en `:root` y `[data-bs-theme="dark"]` en `style.css`.
2. Cambiar reglas `.badge.bg-*` para consumir `var(--badge-*-bg)` y `var(--badge-*-text)`.
3. Bump `?v=` en `base.html` para `style.css`.
4. Verificar en `usuarios/index.html` Activo/Administrador/Supervisor/Operador en claro y oscuro con DevTools contrast, y toast de error sobre tabla para colisión.
5. Rollback: revertir vars y reglas, bump inverso.

## Open Questions

- Ninguna — paleta pendiente de aprobación con hex exactos arriba; si se aprueba, se aplica tal cual.
