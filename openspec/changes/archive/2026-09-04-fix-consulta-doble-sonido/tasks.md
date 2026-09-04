## 1. Fix de carrera de scripts

- [x] 1.1 Mover IIFE intercept síncrono de `consulta/index.html:152` (que detecta `Registro creado|eliminado`, vacía `flashData` y setea `window._consultaCargaTrigger`) a `app/templates/base.html` justo después de `<div id="flashData">` y antes de `<script src="main.js">`, con guard de no-op si no hay `#consultaCargaOverlay`, y verificar en browser que POST /registro → GET /consulta no muestra toast inmediato.
- [x] 1.2 Simplificar `app/templates/consulta/index.html` para eliminar el IIFE duplicado y dejar solo el handler `DOMContentLoaded` del overlay (4500ms) que hace `window._consultaCargaTrigger=null` antes de `mostrarToast`, y verificar que sigue mostrando overlay + 1 toast delayed.
- [x] 1.3 Verificar `app/static/js/main.js:487` guard `if(window._consultaCargaTrigger && /Registro (creado|eliminado)/i)` sigue bloqueando Audio/toast inmediato y que el delayed suena exactamente 1 vez, probando con recarga manual durante overlay (segunda carga sin overlay).

## 2. Validación

- [x] 2.1 Crear test manual/automático que registra alumno vía POST y verifica que GET /consulta con flash success tiene 0 toasts inmediatos y 1 toast delayed (o verifica que no hay doble Audio), y que visitas normales a /consulta muestran toast inmediato normal, y verificar `FLASK_ENV=testing pytest tests/test_consulta.py -v` pasa.
- [x] 2.2 Verificar `venv/bin/lint-imports` y prueba manual: registrar → consultar → escuchar 1 sonido solo al final; eliminar → mismo; entrar directo a consulta → sin overlay y con sonido inmediato si hay flash otro; sin regresión en otros módulos.
