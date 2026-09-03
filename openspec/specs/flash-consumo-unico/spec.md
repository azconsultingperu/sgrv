# flash-consumo-unico Specification

## Purpose
Asegurar que un toast de rate limit se muestre una sola vez y no reaparezca al recargar la página sin nuevo intento.

## Requirements

### Requirement: Consumo único de flash throttled

Un `POST /auth/recuperar` throttled SHALL mostrar el toast una sola vez y un `GET /auth/recuperar` posterior sin nuevo `POST` SHALL no mostrarlo.

#### Scenario: POST throttled muestra toast una vez
- **WHEN** se hace `POST` con `DISABLE_RATE_LIMIT=false` y ya hay 3 intentos en 15min
- **THEN** la respuesta contiene el mensaje throttled y el JS muestra un único toast `Límite alcanzado`.

#### Scenario: GET posterior sin POST no repite
- **WHEN** después de ese `POST` throttled se hace `GET /auth/recuperar` (F5)
- **THEN** la respuesta no contiene `Has superado` en `flashData` y no se muestra toast.

#### Scenario: Fetch no deja flash residual
- **WHEN** el `POST` es vía `fetch` con `X-Requested-With: XMLHttpRequest`
- **THEN** la sesión no queda con `_flashes` pendientes para el siguiente `GET`.
