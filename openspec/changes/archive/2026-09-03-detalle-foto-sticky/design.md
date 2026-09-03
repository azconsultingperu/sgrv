## Context

Ver `proposal.md` Why. `detalle.html` ya es 2 cards (`col-md-4` foto 110px + `col-md-8` tabla) y `base.html` usa `.main-content { overflow-y:auto; height:100dvh }` con `.navbar { position:sticky; top:0; z-index:1025 }`. El scroll ocurre en `.main-content`, no en `window`, por lo que `sticky` anclado a ese contenedor funciona sin JS.

## Goals / Non-Goals

**Goals:** Foto visible al scrollear en desktop con 1 clase CSS, sin JS, con top que deja aire bajo el navbar.

**Non-Goals:** No parallax, no fixed con JS, no sticky en móvil, no cambios en perfil.

## Decisions

**Decisión 1: `position:sticky; top:80px` + `@media (min-width:768px)`**
- *Por qué:* 80px = 60px navbar + 16px padding `p-4` + 4px borde. Si usamos `top:24px` la card quedaría debajo del navbar (solapada 36px). Con 80px queda justo debajo sin solape y sin dejar hueco grande. `align-self:flex-start` evita que flex estire la columna y rompa el sticky. `z-index:1` por debajo de navbar (1025) pero por encima de la tabla.
- *Alternativa descartada:* `top:24px` pegado → se ve cortada bajo el navbar. `position:fixed` con JS → necesita recalcular en resize y al abrir sidebar, más código y peor performance.

**Decisión 2: Aplicar a la `.card` dentro de `col-md-4`, no a la columna**
- *Por qué:* La columna es flex item; el sticky en la columna falla si la columna es más alta que el contenido. La card es más baja que la derecha, por eso `sticky` ahí funciona y no necesita `height:fit-content`.
- *Alternativa descartada:* Sticky en `col-md-4` → en algunos browsers no pega por ser flex item sin `align-self`.

## Risks / Trade-offs

- **Foto más alta que viewport (si algún día crece)** → `sticky` dejaría parte fuera → Mitigación: foto actual es 110px + texto ≈ 260px, muy por debajo de `100dvh`, no hay riesgo.
- **Móvil con sticky taparía tabla** → Mitigación: media query lo desactiva `<768px`.
- **Safari antiguo sin `sticky` dentro de `overflow:auto`** → Mitigación: degradación elegante: sin sticky queda como hoy, sin romper.

## Migration Plan

- Sin migración. Cambio solo CSS + clase. Rollback: quitar clase y regla.

## Open Questions

- Ninguna.
