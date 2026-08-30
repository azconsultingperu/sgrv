## 1. Asset de sonido

- [x] 1.1 Mover `~/Descargas/vadim_makes_sound-ui-error-denied-sound-2-547856.mp3` a `app/static/sounds/error.mp3` (crear directorio si no existe, nombre indicativo) y verificar que `GET /static/sounds/error.mp3` responde 200 y es `audio/mpeg`

## 2. Corrección del toast de login

- [x] 2.1 Quitar `{% set _ = get_flashed_messages(with_categories=true) %}` de `app/templates/auth/login.html:14` y verificar que tras `POST /auth/login` con credenciales inválidas el HTML contiene `#flashData` con `danger` y `main.js` genera 1 `mc-toast danger` visible

## 3. Hook de audio en notificaciones

- [x] 3.1 En `app/static/js/main.js:347` (donde se crea `mc-toast`), añadir reproducción de `new Audio('/static/sounds/error.mp3')` con `volume=0.35`, `preload="auto"`, `play().catch(()=>{})` solo para `tipo danger`, y verificar que login inválido muestra toast + suena una vez y que el toast sigue visible si el navegador bloquea el audio
- [x] 3.2 Verificar reutilización: disparar toast danger desde `registrar` (1 solo toast tras el fix de Paso A) y desde `recuperar` (error genérico) y confirmar que ambos suenan sin duplicar código de audio

## 4. Verificación integral

- [x] 4.1 Recargar `/auth/login` con datos inválidos y `/auth/recuperar` con DNI/correo no coincidente en 360/768/1024 y confirmar 1 toast danger + sonido por intento, sin toasts duplicados, y ejecutar `FLASK_ENV=testing venv/bin/python -m pytest tests/test_auth.py -q` sin regresión
