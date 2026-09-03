## Why

El formulario de "Registrar Nueva Visita" tiene 5 secciones bien agrupadas pero sin jerarquía visual, 8 campos sin placeholder/guía y checkboxes nativos genéricos, lo que lo hace sentir plano y poco guiado frente al diseño pulido del resto del sistema (login, badges, toasts).

## What Changes

- **Jerarquía visual (opción C):** headers de sección numerados (`01` con badge) + `border-bottom` separador + barra de progreso fina (`height:3px`, `position:sticky` bajo navbar) que se llena con scroll, sin convertir en wizard/stepper; mantiene las 5 secciones tal cual.
- **Placeholders:** añadir `placeholder` a 8 campos sin guía (apellidos, nombres, dni, celular, email, direccion, area_interes, observaciones) en `registro/index.html` y replicar en `registro/editar.html` para consistencia; ejemplos concretos (`dni: "Ej. 12345678"`, `celular: "Ej. 987654321"`, `observaciones: "Ej. Interesado en beca, visita con padres..."`).
- **Inputmode numérico:** agregar `inputmode="numeric"` (y `autocomplete` donde aplique) a `dni` y `celular` para teclado numérico en móvil.
- **Custom checkbox cuadrado:** reemplazar `form-check-input` nativo por estilo custom `appearance:none` (cuadrado 18px, borde 1.2px, check blanco, focus con halo `primary-soft`) para los 6 checkboxes del sistema (registro/index 2, registro/editar 2, usuarios/editar 1, login "Recordar" 1); no usar switch/toggle.
- **Consistencia editar:** todos los cambios de placeholder/checkbox se aplican a `registro/editar.html` además de `index.html`.

## Capabilities

### New Capabilities
- `registro-form`: UX del formulario de registro/edición de visitas (jerarquía entre secciones, placeholders/guía, inputmode numérico y estilo de checkboxes) con validación preservada.

### Modified Capabilities
- Ninguna — no existe spec previo de formulario de registro; `auth-validation` no cambia de requisitos.

## Impact

- `app/templates/registro/index.html` y `app/templates/registro/editar.html` — placeholders, inputmode, headers numerados, barra de progreso.
- `app/static/css/style.css` — estilos para headers numerados, barra de progreso fina, custom checkbox `appearance:none`.
- `app/static/js/registro.js` (o inline en template) ligero para barra de progreso por scroll, sin afectar validación.
- Sin impacto en backend, `auth-validation.js` ni `custom-select.js` salvo integración visual.
