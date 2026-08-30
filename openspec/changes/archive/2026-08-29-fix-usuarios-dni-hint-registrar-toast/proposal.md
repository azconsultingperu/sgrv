## Why

En crear usuario el campo DNI no explica que será el nombre de usuario para entrar, y en registrar visita dejar todo vacío dispara 3 carteles de error seguidos en vez de uno. Ambos rompen la claridad y generan ruido.

## What Changes

- En `usuarios/crear.html` agregar bajo el input DNI un hint estilo `Mínimo 8 caracteres...` que diga "Este DNI será el usuario con el que la persona iniciará sesión" (mismo estilo que el hint de contraseña, sin tocar validación).
- En `registro_controller.py` colapsar el `for e in errores: flash(e, 'danger')` a un solo `flash` cuando `errores` no está vacío: si hay 1 error mostrar ese texto, si hay ≥2 mostrar "Faltan datos por completar. Revisa los campos marcados." y/o lista compacta, para que el JS de `main.js` genere 1 toast en vez de 3.
- Sin cambiar lógica de validación (siguen las mismas reglas DNI 8 dígitos, celular 9, etc.), solo la presentación del error.

## Capabilities

### New Capabilities
- `usuarios-dni-hint`: Indicador bajo el campo DNI en crear usuario que aclara que el DNI será el usuario.
- `registrar-single-toast`: Mostrar un solo cartel de error cuando faltan datos en registrar, en vez de uno por cada campo.

### Modified Capabilities
- _Ninguna_

## Impact

- **Código afectado:** `app/templates/usuarios/crear.html` (hint), `app/static/css/auth.css` o estilo inline para el hint (reusa `password-requirements`), `app/modules/registro/presentation/registro_controller.py:90` (colapso de flashes).
- **Dependencias:** Ninguna nueva.
- **Riesgo:** Bajo, solo UI y agregación de mensajes; no toca BD ni permisos.
