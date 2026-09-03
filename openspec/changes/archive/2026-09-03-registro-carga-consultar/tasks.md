## 1. Spinner al aterrizar desde registro/eliminar

- [x] 1.1 Añadir overlay con spinner grande (48px) + texto "Cargando estudiantes..." centrado sobre `.table-responsive` en `app/templates/consulta/index.html` (inicialmente oculto con `display:none`) y estilos en `app/static/css/style.css` con fondo semitransparente, y verificar que es invisible en carga normal.
- [x] 1.2 Modificar JS en `consulta/index.html` (o `main.js`) para detectar flash `success` de registro ("Registro creado exitosamente") o eliminación ("Registro eliminado") en `flashData`, mostrar overlay por 1000ms (800–1200ms) y luego disparar `mostrarToast` correspondiente, y verificar que en aterrizaje desde registro se ve spinner y luego toast, mientras en visita normal no hay delay.
- [x] 1.3 Verificar que la duración no es 3s (medir con `performance.now` o inspección visual) y que al recargar manualmente no vuelve a aparecer el spinner.
- [x] 1.4 Verificación E2E: completar `POST /registro/` válido → `GET /consulta/` muestra spinner 1s → toast success y nuevo alumno en tabla; repetir con `POST /registro/eliminar` → spinner + toast de eliminación; entrar a `/consulta` directo → sin spinner.
