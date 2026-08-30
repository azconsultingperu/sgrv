## Why

Recuperar contraseña se siente desconectada del login: sin footer institucional, ícono con proporción distinta, y sin guía clara sobre qué pasará con el correo. Además usa tooltips nativos del navegador que tapan campos y no ofrece feedback de carga/éxito, lo que genera dudas y errores repetidos.

## What Changes

- **Consistencia con login:** agregar footer `¡Crea, Innova e Inspira!` bajo "Volver al Login", igualar tamaño del ícono de candado al logo del login (55px) y unificar `padding-bottom` del card vía variable CSS (`--auth-card-padding-bottom` o `auth-card-padding`) para que ambas tarjetas cierren igual.
- **Microcopy:** bajo subtítulo agregar línea de ayuda "Te enviaremos un enlace de recuperación al correo registrado con este DNI." y bajo campo correo un hint "Usamos ambos datos para verificar tu identidad" (texto ajustable al flujo real que valida DNI+correo).
- **Feedback de estado:** botón "Enviar Instrucciones" con estado `loading` (disabled + spinner + "Enviando..."); tras éxito mostrar confirmación clara (reemplazo del form por mensaje o alert/toast "Hemos enviado las instrucciones a tu correo. Revisa tu bandeja de entrada."); error genérico sin enumerar si DNI o correo falla: "Si los datos son correctos, recibirás un correo con las instrucciones".
- **Validación inline reutilizable:** desactivar nativa con `novalidate`, implementar componente JS reutilizable que muestre borde rojo + mensaje bajo el input con badge "!" (ej. "Este campo es requerido", "El DNI debe tener 8 dígitos"), empujando layout (sin overlay), timing `blur` o `submit` para mostrar y `input` para limpiar; validaciones DNI (requerido, 8 dígitos numéricos) y correo (requerido, formato email válido).
- No cambia lógica de backend de envío ni autenticación; solo HTML/CSS/JS del template y manejo frontend de estados (fetch/AJAX para no recargar sin feedback si hace falta).

## Capabilities

### New Capabilities
- `recover-password`: UX alineada con login, microcopy, feedback de carga/éxito/error genérico y validación inline reutilizable para DNI y correo en recuperar contraseña.

### Modified Capabilities
- _Ninguna_ — no altera specs de dominio existentes; `login-layout` permanece como está (se reutiliza como referencia visual).

## Impact

- **Código afectado:** `app/templates/auth/recuperar.html` (estructura, footer, microcopy, novalidate, contenedores de error), `app/static/css/auth.css` (tamaño ícono, padding-bottom variable, estilos de error inline badge), nuevo JS reutilizable `app/static/js/auth-validation.js` o bloque `<script>` en recuperar (y futuro login), `app/templates/auth/login.html` solo como referencia (sin tocar lógica).
- **Dependencias:** Bootstrap 5.3 + Bootstrap Icons existentes; sin nueva lib.
- **Riesgo:** Bajo, solo frontend; sin impacto en `auth/recuperar` backend (sigue validando DNI+correo y enviando correo).
