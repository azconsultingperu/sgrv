## Context

Ver `proposal.md`. `registro/index.html` ya tiene 5 secciones con `h5` + icono, pero sin numeración ni progreso; 8 inputs sin placeholder y `dni`/`celular` sin `inputmode`; 6 checkboxes nativos en 4 templates. `registro/editar.html` comparte estructura. La validación es `required`/`pattern` + `is-invalid`/`invalid-feedback`.

## Goals / Non-Goals

**Goals:**Jerarquía clara sin wizard, placeholders consistentes en index/editar, inputmode numérico, checkboxes custom cuadrados uniformes, todo sin romper validación.
**Non-Goals:** Convertir en stepper/wizard, cambiar orden de campos, tocar backend, usar switch/toggle, añadir librería JS pesada, modificar `auth-validation.js` salvo CSS de focus.

## Decisions

**1. Jerarquía — headers numerados + border + barra fina (opción C)**
- Añadir `span.badge` con `01`–`05` dentro de cada `h5` y `border-bottom:1px solid var(--border-color)` con `padding-bottom:0.6rem`. Barra fina: `div#registroProgress` de `height:3px` con `position:sticky; top:60px` (bajo navbar) y `width` por `scroll` (`window.scroll` → % del `form` con `requestAnimationFrame`, sin librería).
- Alternativa stepper/wizard descartada: cambia flujo y añade JS de pasos innecesario para registro continuo.
- Mantiene 5 secciones idénticas, solo refuerza espaciado (`mb-4` a `mb-5` sutil).

**2. Placeholders — ejemplos concretos**
- `apellidos: Ej. García López`, `nombres: Ej. Juan Carlos`, `dni: Ej. 12345678`, `celular: Ej. 987654321`, `email: Ej. juan@ejemplo.com`, `direccion: Ej. Jr. Lima 123, Paiján`, `area_interes: Ej. Ingeniería de Sistemas`, `observaciones: Ej. Interesado en beca, visita con padres...`. Se duplica en `editar.html`.
- Alternativa placeholder genérico descartada: ejemplo concreto guía mejor.

**3. Inputmode — numeric**
- `dni` y `celular` añaden `inputmode="numeric"` y `autocomplete="off"` (dni) / `tel` (celular ya es `type="tel"`). No afecta `pattern` ni `maxlength`.

**4. Custom checkbox cuadrado**
- CSS puro `appearance:none; width:18px; height:18px; border:1.2px solid var(--border-color); border-radius:4px; background:var(--surface-1);` + `:checked { background:var(--primary-color); border-color:var(--primary-color); }` con `::after` para check (`border-right:2px solid #fff; border-bottom:2px solid #fff; transform:rotate(45deg)`). `focus` con `box-shadow`. Mantiene `form-check-input` y `name`/`value`.
- Switch/toggle descartado: comunica preferencia, no dato formal; custom cuadrado es tono institucional.

**5. Nota RENIEC futura (no implementar)**
- El campo `dni` deja espacio a la derecha para futuro ícono de estado (`span#dniStatus` con `position:absolute` dentro de wrapper relativo) sin rediseñar: placeholder corto no ocupa todo el ancho, y el wrapper tiene `position:relative` para alojar `buscando...`, `check` o `error`. Los campos autocompletados usarán resaltado `transition: background-color 0.3s` y mensaje `Datos encontrados en RENIEC`, pero ahora solo se asegura que el placeholder y el borde no bloqueen añadir esos elementos después. Documentar en `design.md` como consideración, no en `tasks.md`.

## Risks / Trade-offs

- **Barra sticky puede tapar contenido bajo navbar** → Mitigación: `top:60px` (altura navbar) y `z-index:1020` por debajo de `navbar` (1025).
- **Placeholder largo en `observaciones` puede cortarse** → Mitigación: usar `placeholder` corto y `rows=3` ya da espacio.
- **Custom checkbox con `appearance:none` en Safari viejo** → Mitigación: fallback a nativo (se ve cuadrado sin check custom, sigue funcional).

## Migration Plan

1. Editar `registro/index.html` y `editar.html` (placeholders, inputmode, headers numerados, barra).
2. Añadir CSS para headers, barra y custom checkbox en `style.css`.
3. Probar validación `is-invalid` y envío con checkboxes marcados.
4. Bump `?v=` en `base.html` si se edita CSS.
5. Rollback: revertir templates y CSS.

## Open Questions

- Ninguna — nota RENIEC es solo constancia de diseño, no tarea.
