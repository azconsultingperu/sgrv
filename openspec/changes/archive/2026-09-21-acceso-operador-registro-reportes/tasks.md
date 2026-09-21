## 1. Guards de registro y reportes

- [x] 1.1 Ampliar `admin_or_supervisor_required` local de `registro_controller.py` a `(1, 2, 3)` y verificar que operador abre `/registro/` y `/registro/editar/<id>` sin flash de permisos.
- [x] 1.2 Ampliar `supervisor_required` local de `reportes_controller.py` a `(1, 2, 3)` y verificar que operador abre el índice y descarga un reporte sin rebote.

## 2. Menú lateral

- [x] 2.1 Mostrar "Registrar" (`rol_id in (1, 2, 3)`) y "Reportes" (agregar rol 3) al operador en `sidebar.html`, manteniendo ocultos "Usuarios" y "Auditoría", y verificar los 4 roles en emulación (operador ve Registrar+Reportes, consultas no ve Registrar).

## 3. Verificación por rol y despliegue

- [x] 3.1 Probar matriz completa con cliente de pruebas (operador: registra/edita/reportes OK, eliminar/usuarios/auditoría rebotan; supervisor/admin intactos; consultas sin cambios) y verificar que la suite `pytest tests/ -q` pasa sin regresiones.
- [x] 3.2 Desplegar `registro_controller.py`, `reportes_controller.py` y `sidebar.html` por cPanel File Manager + `tmp/restart.txt`, y verificar en producción con cuenta operadora real que registra un alumno de prueba.
