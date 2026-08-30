## Context

Ver `proposal.md - Why`. Estado actual: `recuperar.html:7` usa `.login-card.auth-recuperar` con `col-lg-5` (más ancho que login tras `redesign-login-layout` que capó a 400/480px) y `p-4 p-md-5` pero `auth.css:228` fuerza `padding-bottom: 4rem` solo en recuperar, dejando espacio cortado sin footer. Ícono `.auth-icon.warning` es 68px vs logo 55px del login. No hay microcopy ni feedback de carga; el form usa `required` nativo que dispara tooltips del navegador que tapan el campo.

## Goals / Non-Goals

**Goals:**
- Paridad visual login↔recuperar (footer, ícono, padding).
- Microcopy y feedback de carga/éxito/error genérico.
- Validación inline con badge, sin tooltips nativos, reutilizable en login.

**Non-Goals:**
- Cambiar `auth/recuperar` backend (validación DNI+correo y envío de correo sigue igual).
- Rediseño del fondo `frontis` o tipografía base.
- Nueva dependencia JS.

## Decisions

### 1. Footer + ícono + padding unificado
- **Decisión:** En `recuperar.html` agregar `<p class="auth-motto ...">¡Crea, Innova e Inspira!</p>` bajo "Volver al Login" igual que `login.html:56`. En `auth.css:106` ajustar `.auth-icon { width:68px;height:68px }` a 55px o crear `.auth-icon--recover { width:55px;height:55px }` para paridad con `.auth-logo`. Crear variable `--auth-card-padding-bottom: 0.7rem` y usarla en `.login-card .card-body` y `.login-card.auth-recuperar .card-body` (reemplaza `4rem` hardcodeado).
- **Rationale:** Reutiliza token de login; variable evita divergencia futura.
- **Alternativa:** Dejar `4rem` y solo agregar footer — rechazada: deja hueco doble (padding + footer).

### 2. Microcopy
- **Decisión:** Insertar `<p class="auth-help small text-muted">Te enviaremos...</p>` bajo subtítulo y `<small class="form-text text-muted">Usamos ambos...</small>` bajo input correo, con `font-size: 0.8rem` y `color:#6b7a8d` (ya usado en `.auth-desc`).
- **Alternativa:** Tooltip `title` — rechazada: no visible sin hover.

### 3. Feedback de estado (loading/success/error)
- **Decisión:** En `recuperar.html` dar `id="recoverForm"` y `id="recoverBtn"` al botón; JS hace `fetch`/`POST` con `preventDefault`, deshabilita botón, inyecta `<span class="spinner-border spinner-border-sm me-2">` + "Enviando...", y al `200` reemplaza `form.innerHTML` por `<div class="alert alert-success">Hemos enviado...</div>` o muestra `#recoverSuccess` oculto. En error genérico muestra `alert-secondary` con "Si los datos son correctos..." sin distinguir campo.
- **Rationale:** Reemplazo del form evita que quede visible sin cambios; `fetch` permite controlar spinner sin recarga.
- **Alternativa:** Depender de `flash` del backend con recarga — rechazada: no permite spinner ni evitar doble submit sin JS extra y pierde control de timing.

### 4. Validación inline reutilizable
- **Decisión:** Crear `app/static/js/auth-validation.js` con `export function initAuthValidation(form, fields)` que: añade `novalidate` si no está, crea contenedor `.invalid-feedback` bajo cada input con estructura `<span class="badge bg-danger rounded-circle">!</span> mensaje`, aplica `is-invalid` (borde `#dc3545` vía `auth.css`), muestra en `blur` si inválido o en `submit` (previniendo envío), limpia en `input` cuando pasa validación. Reglas: DNI `required + /^\d{8}$/`, correo `required + valid email (input.type=email + checkValidity)`. El contenedor empuja layout (`display:block; margin-top:0.35rem`), nunca `position:absolute`.
- **Rationale:** Desacoplado del form, reutilizable en `login.html` (usuario requerido, contraseña requerida) sin duplicar; timing evita ruido mientras escribe.
- **Alternativa:** Librería `validate.js` — rechazada: añade dependencia para 2 campos; nativo con `setCustomValidity` no permite badge custom ni empuje de layout.

## Risks / Trade-offs

- **Fetch vs POST tradicional rompe `flash` existente** → Mitigación: mantener fallback `POST` síncrono si `fetch` no disponible; el JS detecta `response.redirected` y sigue mostrando mensaje; backend no cambia.
- **Badge rojo puede confundirse con `is-invalid` de Bootstrap** → Mitigación: usar `background: #dc3545` y `color:#fff` ya usado en sistema para error, con `border-color` igual en input para consistencia.
- **Mensaje genérico de error puede confundir usuario legítimo con typo en correo** → Mitigación: es intencional por seguridad; se complementa con hint "Usamos ambos datos..." para que revise ambos.

## Migration Plan

1. Editar `recuperar.html` (footer, microcopy, `novalidate`, ids, contenedores de error) y `auth.css` (ícono, variable padding, estilos `.invalid-feedback` badge).
2. Añadir `auth-validation.js` y cargarlo en `recuperar.html` (y opcional en `login.html` sin activar hasta siguiente iteración).
3. Verificar en 360/768/1024: footer igual que login, ícono 55px, padding, microcopy, spinner, validación inline sin overlay, y que `python -m pytest tests/test_auth.py -q` sigue verde (backend sin tocar).
4. Rollback: revertir `recuperar.html` y `auth.css` a versión previa (un commit).

## Open Questions

- ¿El mensaje de éxito debe reemplazar todo el form o mostrarse como toast arriba del form manteniendo los inputs? Default: reemplazo del form por mensaje de éxito (más claro), con botón "Volver al Login" debajo.
