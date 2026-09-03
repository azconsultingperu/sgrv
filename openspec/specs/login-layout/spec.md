## Purpose

Define el layout compacto del login para que la tarjeta sea estrecha y centrada, el link de recuperación quede como acción secundaria debajo del botón y el espaciado vertical quede equilibrado sin afectar autenticación.

## Requirements

### Requirement: Tarjeta estrecha y centrada

La tarjeta `.login-card` SHALL tener `max-width` entre 400px y 480px (valor canónico 480px tras ajuste +20% solicitado) y SHALL permanecer centrada horizontalmente con padding proporcional en `p-4 p-md-5` para inputs, sin cambiar `name/id` de campos.

#### Scenario: Ancho en desktop
- **WHEN** se carga `/auth/login` en viewport ≥ 992px
- **THEN** el ancho renderizado de `.login-card` es ≤ 480px y está centrado (margen lateral izquierdo ≈ derecho, diferencia < 8px) y los inputs mantienen padding lateral ≥ 12px.

#### Scenario: Responsive sin desborde
- **WHEN** se carga en 360px
- **THEN** la tarjeta ocupa `col-11` con `max-width` capado y no genera scroll horizontal.

### Requirement: Link olvidó debajo del botón y checkbox solo

El formulario SHALL mostrar `Recordar usuario` solo en su propia fila (sin link a la derecha) alineado a la izquierda, el botón `Iniciar Sesión` en fila completa, y el link `¿Olvidó su contraseña?` centrado debajo del botón como acción secundaria con `font-size` menor que el body del formulario (ej. 0.85rem), color `var(--primary-color)` y subrayado solo en `hover`.

#### Scenario: Orden vertical
- **WHEN** se inspecciona el DOM de `app/templates/auth/login.html` tras el cambio
- **THEN** el orden es Logo → Usuario → Contraseña → checkbox solo → botón → link olvidó centrado → footer `¡Crea, Innova e Inspira!`, sin link junto al checkbox.

#### Scenario: Estilo del link secundario
- **WHEN** el link olvidó está en reposo
- **THEN** no tiene subrayado y su tamaño es menor que `.login-label`; en `hover` subraya y cambia a `var(--primary-hover)`.

### Requirement: Espaciado vertical compacto y equilibrado

El espaciado entre checkbox → botón → link olvidó → footer SHALL ser compacto: fila checkbox con `margin-bottom` 10–12px (no 1.5rem), botón a link con `margin-top` 8–12px, y footer con `margin-top` 12–16px, evitando aire excesivo debajo del botón.

#### Scenario: Compacidad
- **WHEN** se mide distancia vertical entre la base del botón y la parte superior del link olvidó
- **THEN** es 8–12px; y entre link olvidó y footer `¡Crea, Innova e Inspira!` es 12–16px, sin salto > 24px entre checkbox y botón.

#### Scenario: Sin impacto en lógica
- **WHEN** se envía el formulario con `username`/`password`/`recordar` y `csrf_token`
- **THEN** la autenticación funciona igual (mismos `name/id`, mismo `POST` a `auth.login`).
