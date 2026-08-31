## Context

Ver `proposal.md - Why`. Estado actual: `base.html:20` carga `bootstrap-icons@1.11.2` y todos los templates usan `bi-*` (~80 ocurrencias). Lucide usa `data-lucide` + `lucide.createIcons()` para reemplazarlos por SVG.

## Goals / Non-Goals

**Goals:**
- Reemplazo 1:1 de `bi-*` a Lucide manteniendo tamaños/colores y sin tocar layout.

**Non-Goals:**
- Rediseño de layout o nueva iconografía custom.
- Cambiar lógica de negocio o permisos.

## Decisions

### 1. CDN Lucide + createIcons
- **Decisión:** Reemplazar `<link bootstrap-icons>` por `<script src="https://unpkg.com/lucide@latest"></script>` en `base.html` y llamar `lucide.createIcons()` en `main.js` tras `DOMContentLoaded` y tras cada `htmx`/`turbo` si aplica.
- **Rationale:** Sin build step, purga de caché con `?v=`.
- **Alternativa:** `npm install lucide` + bundler — rechazada: requiere build.

### 2. Mapeo directo
- **Decisión:** Tabla `bi-speedometer2→gauge`, `bi-building→school`, `bi-people→users`, `bi-person-vcard→id-card`, `bi-eye→eye`, `bi-eye-slash→eye-off`, etc., manteniendo clases de color.
- **Alternativa:** Rediseñar set de íconos — rechazada: fuera de alcance.

### 3. Compatibilidad
- **Decisión:** Buscar/reemplazar global `bi-` → `data-lucide` con `class="w-4 h-4"` para tamaño, y eliminar `bi` font.
- **Rationale:** Lucide escala con `width/height`, no con `font-size`.

## Risks / Trade-offs

- **Ícono sin equivalente 1:1** → Mitigación: usar el más cercano y documentar en PR; fallback temporal a `help-circle`.
- **FOUC de íconos** → Mitigación: `createIcons` en `DOMContentLoaded` y ocultar `data-lucide` hasta render.

## Migration Plan

1. Cambiar CDN en `base.html`, añadir `createIcons` en `main.js`.
2. Reemplazo masivo `bi-` → `data-lucide` en templates.
3. Verificar en 360/1024 que no queden `bi-*` y que los tamaños coincidan.
4. Rollback: revertir CDN y `data-lucide` → `bi`.

## Open Questions

- ¿Usar `strokeWidth` 1.5 o 2 para Lucide en SGRV? Default: 2 (más visible en cards pequeñas).
