## Why

La tarjeta de login es demasiado ancha para dos inputs, deja aire muerto a los lados y la fila `Recordar usuario + ¿Olvidó su contraseña?` compite por atención con el botón principal. Mover el link debajo del botón y compactar la tarjeta mejora jerarquía y reduce desplazamiento visual en el primer contacto del usuario.

## What Changes

- Reducir `max-width` de `.login-card` de ~520–540px (col-lg-5 + padding) a **380–420px** (ej. `max-width: 400px` + `margin: 0 auto`), manteniendo centrado horizontal y padding proporcional en `p-4 p-md-5`.
- Reestructurar fila de opciones: dejar `Recordar usuario` solo en su propia fila alineado a la izquierda (sin link a la derecha); mover `¿Olvidó su contraseña?` debajo de `Iniciar Sesión`, centrado, como link secundario con `font-size ~0.85rem`, color `var(--primary-color)`, sin subrayado hasta `hover`.
- Compensar espacio vertical: reducir `margin-bottom` de la fila checkbox (de `mb-4` a `mb-3` o `16px → 10–12px`), usar `margin-top: 8–12px` entre botón y link olvidó, y ajustar `margin-top` del footer `¡Crea, Innova e Inspira!` para conjunto compacto sin aire excesivo debajo del botón.
- Orden final: Logo + título/institución → Usuario → Contraseña → Checkbox solo → Botón → Link olvidó centrado → Footer. Sin tocar `name/id` de campos ni lógica de autenticación.

## Capabilities

### New Capabilities
- `login-layout`: Layout compacto y jerarquía visual del formulario de login (ancho de tarjeta, posición del link olvidó y espaciado vertical equilibrado).

### Modified Capabilities
- _Ninguna_ — no altera specs de dominio existentes (`domain-events`, `modular-boundaries`, `notifications`, `dashboard-barcharts`).

## Impact

- **Código afectado:** `app/templates/auth/login.html` (estructura HTML: contenedor `col-*`, fila `.login-options`, posición del link) y `app/static/css/auth.css` ( `max-width` de `.login-card`, márgenes `login-options`/`login-btn`/`.auth-motto`, responsivo `@media (max-width: 575.98px)`).
- **Dependencias:** Ninguna nueva (Bootstrap 5.3 existente).
- **Riesgo:** Bajo, solo HTML/CSS visual; sin impacto en `auth_controller`, validación, CSRF o BD.
