## 1. Backend

- [x] 1.1 Hacer que `POST /auth/recuperar` con `X-Requested-With: XMLHttpRequest` devuelva JSON throttled/genérico sin `flash`, y que `GET` posterior no contenga `Has superado` en `flashData`; verificar con test `POST throttled -> GET flash []`.

## 2. Frontend

- [x] 2.1 Actualizar `recuperar.html` para manejar JSON (`status`/`message`) en vez de `res.text.includes`, manteniendo fallback a HTML; verificar que `POST` muestra un único toast y `F5` no lo repite.

## 3. Tests

- [x] 3.1 Añadir `tests/test_flash_consumo.py` con los 3 escenarios del spec; `pytest -v` pasa.
