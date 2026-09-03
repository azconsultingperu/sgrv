## Context

Ver `proposal.md` Why. Hoy `navbar.html:12` es `<span class="badge clock-badge" id="relojNavbar">--:--:--</span>` y `main.js:11` pone `dd/MM/yyyy HH:mm:ss` 24h sin icono ni jerarquía. `style.css:686` lo define como `monospace, 0.78rem, surface-2`. El usuario lo ve básico y no entiende a primera vista qué número es qué.

## Goals / Non-Goals

**Goals:** Hora 12h AM/PM legible, fecha corta en español, iconografía Lucide y jerarquía (hora bold, fecha muted), responsive y accesible, sin nueva dependencia.

**Non-Goals:** No sincronizar con servidor (sigue hora local), no añadir selector de zona horaria, no hacer calendario desplegable.

## Decisions

**Decisión 1: Formato 12h con `toLocaleString('es-PE', {hour:'2-digit', minute:'2-digit', second:'2-digit', hour12:true})` + fecha `weekday:'short', day:'2-digit', month:'short'`**
- *Por qué:* Usa Intl nativo, respeta locale es-PE, da `02:05:22 p. m.` que normalizamos a `PM`. Evita aritmética manual de `>12` y el bug de `00`/`12`.
- *Alternativa descartada:* Manual `h%12 || 12` → más código y fácil olvidar `00` → `12 AM`.

**Decisión 2: Estructura badge con spans separados y icono Lucide `clock` (14px)**
- *Por qué:* Permite `d-none d-sm-inline` para ocultar fecha en móvil sin JS y `tabular-nums` solo en números. Lucide ya está cargado globalmente.
- *Alternativa descartada:* Dos badges separados → ocupa más ancho; emoji `🕒` → no respeta `stroke-width` del sistema.

**Decisión 3: CSS `inline-flex + gap + tabular-nums + font-weight`**
- *Por qué:* `tabular-nums` evita vibración al cambiar segundos; `gap` es más limpio que `&nbsp;`. Mantiene `surface-2` y `border-color` existentes, solo refina tipografía.
- *Alternativa descartada:* `monospace` puro → se ve técnico y no usa `Inter`.

**Decisión 4: `title`/`aria-label` con fecha larga**
- *Por qué:* Da contexto sin ensuciar el badge. El `title` ya lo soporta el browser, no necesita tooltip custom.
- *Alternativa descartada:* Tooltip de Bootstrap → requiere inicialización y más JS.

## Risks / Trade-offs

- **Locale `es-PE` puede dar `a. m.` con puntos** → Mitigación: normalizar a `AM/PM` con `.replace(/\.\s*/g,'').toUpperCase()` y testear en Chrome/Firefox.
- **Badge más ancho en desktop por fecha + icono** → Mitigación: ocultar fecha en `<576px` y usar `max-width` con `text-overflow` si el navbar se satura.
- **Intl sin soporte en browser viejo** → Mitigación: fallback a manual `pad` si `toLocaleString` falla.

## Migration Plan

- Solo frontend. Cambia `navbar.html`, `style.css`, `main.js`. No migración. Rollback: revertir 3 archivos.

## Open Questions

- Ninguna — formato `03 sep 2026` vs `mié, 03 sep` lo dejamos en `mié, 03 sep 2026` para incluir día de semana sin alargar demasiado; si prefieres sin día, se ajusta en 1 línea.
