## Why

Los promotores de campo entran al sistema con rol Operador (rol 3), pero el código solo permite registrar, editar y ver reportes a Administrador y Supervisor. El seed declara que el Operador "puede registrar alumnos y consultar registros", mas los guards y el menú nunca lo implementaron: el reporte de campo ("no pueden registrar") es correcto. Sin este cambio el registro en campo depende de cuentas prestadas de Supervisor.

## What Changes

- Rol Operador (rol 3) puede abrir `/registro/` (GET+POST) y `/registro/editar/<id>` (GET+POST): guards pasan de `(1, 2)` a `(1, 2, 3)` en `registrar` y `editar`.
- Rol Operador puede ver Reportes: guards `supervisor_required` de reportes pasan a aceptar rol 3 (solo lectura y generación de sus reportes; sin cambios en el contenido).
- El sidebar muestra "Registrar" y "Reportes" al Operador (`rol_id <= 2` → incluye 3 donde aplique).
- Sin cambios para: Eliminar (solo admin), Usuarios (solo admin), Auditoría (solo admin), Consultar (ya abierto a todos), Dashboard y Perfil (ya abiertos).
- Sin cambios para rol Consultas (rol 4): sigue sin registrar ni editar; nota aparte — hoy el menú le muestra Reportes pero el guard lo rebota; este change lo deja como está (decisión pendiente).

## Capabilities

### New Capabilities
- `acceso-operador`: matriz de permisos del rol Operador — qué módulos y acciones puede usar (registrar, editar, consultar todos, reportes, dashboard, perfil propio) y cuáles le quedan prohibidos (eliminar, usuarios, auditoría).

### Modified Capabilities
- (vacío — ningún spec existente declara requisitos por rol; `registro-form` describe el formulario, no quién lo usa)

## Impact

- `app/modules/registro/presentation/registro_controller.py` (guards locales `admin_or_supervisor_required` en `registrar` y `editar`).
- `app/modules/reportes/presentation/reportes_controller.py` (`supervisor_required` en todas sus rutas).
- `app/templates/partials/sidebar.html` (condiciones `rol_id <= 2` y `<= 2 or == 4`).
- Auditoría ya registra `actor_id`: los registros creados por operadores quedan trazados sin cambios extra.
- Riesgo: operadores ven todos los alumnos en Consultar (decisión aprobada: sí, todos).
