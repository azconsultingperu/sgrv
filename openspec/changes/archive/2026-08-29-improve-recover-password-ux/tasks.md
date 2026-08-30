## 1. Paridad visual con login

- [x] 1.1 Agregar footer `¡Crea, Innova e Inspira!` en `recuperar.html` debajo de "Volver al Login" (igual que `login.html:56` `p.auth-motto`) y verificar que ambas tarjetas cierran con el mismo elemento y no se sienten cortadas en 1024px
- [x] 1.2 Igualar tamaño del ícono de candado a 55px (`auth.css:106` `.auth-icon` de 68px → 55px o variante `.auth-icon--recover`) y verificar que en 1024px `getBoundingClientRect().height` del ícono de recuperar ≈ 55px igual que `.auth-logo` del login
- [x] 1.3 Unificar `padding-bottom` del card vía variable CSS (`--auth-card-padding-bottom: 0.7rem`) en `auth.css:223` y usarla en `.login-card .card-body` y `.login-card.auth-recuperar .card-body` (reemplaza `4rem` hardcodeado) y verificar que ambas plantillas comparten el mismo valor y no hay espacio sobrante distinto en DevTools

## 2. Microcopy y claridad

- [x] 2.1 Insertar línea de ayuda bajo subtítulo en `recuperar.html:19` (`<p class="auth-help small">Te enviaremos un enlace...</p>`) y verificar que se renderiza debajo de "Ingrese sus credenciales..." en 360/1024 sin romper layout
- [x] 2.2 Agregar hint bajo campo correo (`<small class="form-text">Usamos ambos datos para verificar tu identidad</small>`) y verificar que aparece con color secundario y no interfiere con mensaje de error inline

## 3. Feedback de estado (carga, éxito, error genérico)

- [x] 3.1 Implementar estado de carga en `recuperar.html` (`id="recoverBtn"`): al submit deshabilitar botón, mostrar spinner + "Enviando..." y prevenir doble submit, y verificar que el botón queda `disabled` y el spinner es visible durante `fetch`
- [x] 3.2 Mostrar confirmación de éxito tras `200` reemplazando el form o mostrando `#recoverSuccess` con "Hemos enviado las instrucciones a tu correo. Revisa tu bandeja de entrada." y verificar que el formulario no queda visible sin cambios tras éxito
- [x] 3.3 Definir mensaje de error genérico para DNI/correo no coincidente ("Si los datos son correctos, recibirás un correo...") y verificar que no revela si el DNI existe, manteniendo el mismo mensaje para ambos casos de fallo

## 4. Validación inline reutilizable (sin tooltips nativos)

- [x] 4.1 Añadir `novalidate` al `<form>` en `recuperar.html:21` y crear `app/static/js/auth-validation.js` con `initAuthValidation(form, rules)` que inyecta `.invalid-feedback` con badge `!` (círculo rojo) + mensaje, aplica `is-invalid` con borde rojo y empuja layout (sin overlay), y verificar que el tooltip nativo "Completa este campo" no aparece al enviar vacío
- [x] 4.2 Implementar reglas y timing: DNI (requerido, 8 dígitos `^\d{8}$`), correo (requerido, formato email válido); mostrar error en `blur` si inválido o en `submit`, limpiar en `input` al corregir, y verificar que escribir por primera vez sin `blur` no muestra error prematuro y que al corregir el error desaparece en tiempo real
- [x] 4.3 Verificar reutilización en login: importar `initAuthValidation` en `login.html` sin activarlo aún (o con reglas usuario/contraseña comentadas) y confirmar que `auth-validation.js` es independiente del form y no duplica código, y que `make lint-boundaries` no reporta nuevos acoplamientos

## 5. Verificación integral

- [x] 5.1 Recargar `/auth/recuperar` en 360/768/1024 y confirmar footer, ícono 55px, microcopy, spinner, validación inline sin overlay y sin tooltips nativos, y ejecutar `FLASK_ENV=testing venv/bin/python -m pytest tests/test_auth.py -q` sin regresión (backend sin tocar, solo frontend)
