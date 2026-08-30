## 1. Hint de DNI como usuario

- [x] 1.1 Agregar hint bajo input DNI en `app/templates/usuarios/crear.html:14` con texto "Este DNI será el usuario con el que la persona iniciará sesión" usando clase `password-requirements` y verificar que se ve debajo del campo DNI en 360/1024 sin superponerse al `invalid-feedback`

## 2. Un solo toast en registrar

- [x] 2.1 Colapsar `for e in errores: flash(e, 'danger')` en `app/modules/registro/presentation/registro_controller.py:90` a un solo `flash` (1 error → mensaje específico, ≥2 → "Faltan datos por completar. Revisa los campos marcados.") y verificar que `POST /registro/` vacío genera exactamente 1 mensaje `danger` en `get_flashed_messages` y 1 `mc-toast` visible
- [x] 2.2 Verificar que con un solo error (ej. solo DNI inválido) sigue mostrando el mensaje específico y no el genérico, y que `FLASK_ENV=testing venv/bin/python -m pytest tests/test_registro.py -q` pasa

## 3. Verificación integral

- [x] 3.1 Recargar `/usuarios/crear` y `/registro/` en 360/768/1024 y confirmar hint visible y 1 solo toast en vacío, y ejecutar `make lint-boundaries` sin nuevos acoplamientos
