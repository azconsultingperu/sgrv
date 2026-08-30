## 1. Tarjeta compacta y centrada

- [x] 1.1 Añadir `max-width: 400px; margin: 0 auto; width: 100%` a `.login-card` en `app/static/css/auth.css:38` (mantener `p-4 p-md-5` y `border-radius`) y verificar que en 1024px `document.querySelector('.login-card').getBoundingClientRect().width` ≤ 420px y `offsetLeft` ≈ `offsetRight` (±8px)
- [x] 1.2 Ajustar contenedor de `login.html:16` de `col-lg-5` a `col-lg-4` o mantener capado con `max-width` y verificar que en 360px no hay scroll horizontal y en 992px la tarjeta no supera 400px

## 2. Reestructurar checkbox y link olvidó

- [x] 2.1 Reemplazar fila `div.d-flex.login-options` en `login.html:44` por solo checkbox (`<div class="login-options mb-3"><div class="form-check">...</div></div>` alineado a la izquierda) y verificar que el DOM ya no contiene link junto al checkbox y que el checkbox queda alineado con el borde del input
- [x] 2.2 Insertar link `¿Olvidó su contraseña?` debajo del botón `login.html:51` como `<div class="text-center mt-2"><a class="login-link login-link--secondary" href="...">` y crear variante `.login-link--secondary { font-size: 0.85rem; }` en `auth.css:190` (subrayado solo en hover) y verificar que el link está centrado y es menor que `.login-label`

## 3. Compensar espaciado vertical

- [x] 3.1 Ajustar márgenes en `auth.css`: `.login-options` a `margin-bottom: 0.75rem`, link olvidó a `margin-top: 10px`, `.auth-motto` a `margin-top: 0.9rem` y verificar que distancia checkbox→botón es 10–12px y botón→link es 8–12px y link→footer es 12–16px (inspección en DevTools, sin aire >24px)
- [x] 3.2 Verificar responsivo `@media (max-width:575.98px)` sigue sin `flex-direction` conflictivo y que `make lint-boundaries` no reporta cambios Python (solo CSS/HTML)

## 4. Verificación integral

- [x] 4.1 Recargar `/auth/login` en 360/768/1024/1400 y confirmar orden Logo → Usuario → Contraseña → checkbox solo → botón → link centrado → footer, y ejecutar `FLASK_ENV=testing venv/bin/python -m pytest tests/test_auth.py -q` sin regresión y que el submit conserva `name=username/password/recordar` y `csrf_token`
