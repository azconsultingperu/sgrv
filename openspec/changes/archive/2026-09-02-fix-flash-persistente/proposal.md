## Why

El toast `Has superado el límite...` reaparece al recargar `GET /auth/recuperar` sin nuevo `POST`, confundiendo al usuario y haciendo parecer que el rate limit sigue activo aunque la BD ya esté limpia. Evidencia en test client: `POST 4` throttled → `GET` posterior con `flashData []` (no persiste) en el harness, pero en navegador real el usuario reporta que sí aparece al cargar, sin `POST` en Network, lo que apunta a flash residual en sesión o a `fetch` que no consume la cola.

## What Changes

- Para `POST /auth/recuperar` vía `fetch` (`X-Requested-With: XMLHttpRequest`), no usar `flash()` para el caso throttled/genérico; devolver JSON `{"status": "throttled"|"ok", "message": "..."}` y dejar que el JS muestre el toast sin tocar la sesión, de modo que un `GET` posterior no repinte el mismo mensaje.
- Para `POST` no-AJAX (fallback sin JS), mantener `flash` + `render_template` pero asegurar que `get_flashed_messages` lo consume en esa misma respuesta y no queda para el siguiente `GET`.
- Alternativa si se mantiene `flash` para `fetch`: hacer `session.pop('_flashes', None)` o `get_flashed_messages` en la misma request y no dejarlo para el siguiente `GET`.

## Capabilities

### New Capabilities
- `flash-consumo-unico`: Garantía de que un mensaje flash de rate limit se muestra una sola vez y no reaparece en `GET` posteriores sin nuevo `POST`.

### Modified Capabilities
- `notifications`: no, es de rate limit, pero si hay spec de `password-recovery-hardening` que menciona el mensaje throttled, se añade el requisito de consumo único.

## Impact

- `app/modules/identidad/presentation/auth_controller.py` (ramas `recuperar` throttled y genérica)
- `app/templates/auth/recuperar.html` (JS `fetch` → manejar JSON en vez de parsear `res.text` con `includes`)
- `tests/` (regresión: `POST` throttled → `GET` sin flash)
