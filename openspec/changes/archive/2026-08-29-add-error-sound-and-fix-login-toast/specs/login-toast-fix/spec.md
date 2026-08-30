## Purpose

Corregir que los mensajes de login inválido no llegan al sistema de toasts porque la plantilla los consume antes de que el JS los lea.

## ADDED Requirements

### Requirement: Mensajes de login visibles como toast

Los mensajes `flash` generados por `auth/login` con `danger` SHALL llegar a `base.html #flashData` y ser renderizados por `main.js` como `mc-toast danger` sin ser consumidos previamente por `login.html`.

#### Scenario: Login con contraseña incorrecta
- **WHEN** se hace `POST /auth/login` con usuario válido y contraseña incorrecta
- **THEN** la respuesta HTML contiene `#flashData` con `["danger", "Usuario o contraseña incorrectos."]` y el JS muestra 1 `mc-toast danger` visible.

#### Scenario: Login con usuario inexistente
- **WHEN** se hace `POST /auth/login` con usuario inexistente
- **THEN** se muestra el mismo toast genérico sin revelar si el usuario existe.

### Requirement: No consumo prematuro en login.html

`app/templates/auth/login.html` SHALL no hacer `{% set _ = get_flashed_messages(...) %}` que vacíe la cola antes de `base.html`.

#### Scenario: Plantilla sin consumo
- **WHEN** se inspecciona `login.html` tras el cambio
- **THEN** no contiene `get_flashed_messages` y deja que `base.html` lo lea.

#### Scenario: Regresión sin duplicado
- **WHEN** se recarga login con múltiples errores seguidos
- **THEN** no aparecen 2 toasts idénticos por doble lectura.
