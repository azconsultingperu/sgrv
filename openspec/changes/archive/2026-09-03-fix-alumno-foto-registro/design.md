## Context

Ver `proposal.md` Why. Estado tras `alumno-foto-registro-detalle`: `registro_controller.registrar` hace `UnitOfWork` commit + segundo `db.session.commit()` para foto y dos `flash` (danger+success) en el mismo request; `registro/index.html` tiene `#alumnoFotoWrap` con placeholder "--" y botón siempre "Cambiar foto" aunque no haya foto; en móvil los botones quedan a la izquierda por `d-flex` sin `justify-content-center`. La notificación success a veces no se ve porque el doble flash se pisa o el `rollback` vacía la sesión.

## Goals / Non-Goals

**Goals:** Unificar a un solo flash por POST, centrar en móvil, botón dinámico Añadir→Cambiar y placeholder svg sin tocar storage/serving ni migración.

**Non-Goals:** No cambiar validación PIL, tamaños, rutas, ni layout de detalle/listado (ya correctos).

## Decisions

**Decisión 1: Un solo flash y evitar rollback tras UoW**
- *Por qué:* `crear_alumno_con_visita` ya hizo commit; hacer `rollback` después vacía la sesión Flask y puede borrar `flash` queue. Si foto falla, no hacer `rollback`, solo `flash danger` y no `success`; si foto ok o sin foto, solo `success`. Nunca dos flashes en el mismo redirect. Si foto falla pero alumno ya existe, se mantiene el alumno (foto opcional) pero el mensaje es solo danger explicando que se guardó sin foto o que la foto fue ignorada — evita "no se completa" percibido.
- *Alternativa descartada:* Mantener dos flashes → `get_flashed_messages` los pone en array y `main.js` los muestra ambos, pero el usuario ve danger y success superpuestos y cree que falló.

**Decisión 2: Centrado móvil con `justify-content-center` + `text-center` y `justify-content-md-start` en desktop**
- *Por qué:* Mantiene desktop alineado a la izquierda (como resto del form) y en `<768px` centra. No requiere media query custom, usa Bootstrap utilities.
- *Alternativa descartada:* CSS custom con `@media` → más código, mismo efecto.

**Decisión 3: Botón dinámico vía JS**
- *Por qué:* El label depende de estado (sin foto → Añadir, con foto → Cambiar). JS ya maneja `FileReader`; extender para cambiar `textContent` y mostrar/ocultar Eliminar es trivial y no requiere roundtrip.
- *Alternativa descartada:* Render distinto desde Jinja con `if` → no reacciona tras seleccionar sin recargar.

**Decisión 4: Placeholder svg en vez de "--"**
- *Por qué:* Reusa `avatar-default.svg` ya usado como fallback de `foto_url()` y perfil, da coherencia visual y evita texto crudo. Dentro de círculo 110px con `object-fit:cover` y opacidad 0.7 se ve como avatar vacío.
- *Alternativa descartada:* Iniciales dinámicas según nombres → requiere JS para actualizar mientras escribe, más complejidad sin ganancia.

## Risks / Trade-offs

- **Foto falla pero alumno queda sin foto sin que usuario lo note** → Mitigación: flash danger explícito "Registro guardado, pero la foto fue ignorada: <motivo>" para que sepa reintentar en editar.
- **Cambiar texto del botón puede desorientar si el usuario espera siempre "Cambiar"** → Mitigación: icono `camera` + texto claro; en editar con foto existente mantiene "Cambiar" desde el inicio.
- **Centrado móvil puede dejar mucho aire en desktop si se aplica mal** → Mitigación: usar `justify-content-center justify-content-md-start` para solo centrar en móvil.

## Migration Plan

- Sin migración. Deploy: reemplazar templates y controller, hard refresh `?v=` en `style.css` si se toca. Rollback: revertir commits, el alumno queda sin foto pero sin pérdida de datos.

## Open Questions

- Ninguna.
