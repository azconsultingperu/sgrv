## Why

Eliminar un usuario hace soft delete (`eliminado=True`, fila queda en BD) pero crear con el mismo DNI vuelve a fallar con “El DNI ya está registrado”, aunque el usuario ya no aparece en Gestión de Usuarios. Esto bloquea flujos reales de prueba y rotación de personal y obliga a usar DNIs ficticios. Con trazabilidad ya cubierta por Auditoría, se quiere permitir reusar el DNI reactivando la misma fila para no duplicar historial.

## What Changes

- Validaciones de unicidad en `POST /usuarios/crear` SHALL consultar solo usuarios activos (`eliminado=False`) para `dni`, `username` (que es el DNI) y `email`; coincidencias solo con filas eliminadas no bloquean.
- Si el DNI enviado coincide con una fila `eliminado=True`, el sistema SHALL **reactivar** esa fila existente en lugar de crear una nueva: `eliminado=False`, `estado=True`, `resetear_intentos()`, actualizar `nombres`, `apellidos`, `email`, `rol_id`, `password_hash` (nueva contraseña), `actualizado_en=peru_now()`, y `avatar`/`debe_cambiar_password` según flujo normal.
- El índice `UNIQUE` de BD en `usuarios.dni` y `usuarios.username` SHALL cambiar a índice único **parcial** `WHERE eliminado = false` (PostgreSQL/SQLite) para permitir múltiples filas históricas con el mismo DNI pero solo una activa.
- El endpoint `GET /usuarios/verificar-dni?dni=...` SHALL aplicar el mismo filtro `eliminado=False` para no reportar “existe” cuando el DNI solo está en un eliminado.
- Cada reactivación SHALL registrar en Auditoría un evento distinto `Usuario reactivado` (usuario objetivo, actor, IP, user-agent, detalle con DNI/username), separado de `Usuario creado` y `Usuario eliminado`, para trazabilidad del ciclo.

## Capabilities

### New Capabilities
- `usuario-reactivacion`: Ciclo de vida de usuario con soft delete y reactivación — filtrado por `eliminado=False` en validaciones, reactivación de fila existente sobre DNI eliminado, índice parcial y auditoría de reactivación.

### Modified Capabilities
<!-- No se modifica spec existente: usuarios-dni-hint es solo hint visual, no validación -->

## Impact

- Código: `app/modules/identidad/domain/usuario.py` (índice), `app/modules/identidad/presentation/usuarios_controller.py` (`crear()`, `verificar_dni()`), `app/modules/auditoria/domain/auditoria.py` (nuevo tipo de evento), `migrations/` (reemplazo de UNIQUE por índice parcial), `tests/` (regresión de reactivación).
- BD: PostgreSQL soporta `CREATE UNIQUE INDEX ... WHERE eliminado = false`; SQLite en testing usa el mismo DDL condicional; requiere migración Alembic con `batch_alter_table` + `create_index` parcial.
- Auditoría: nuevo `Auditoria` con `accion='Usuario reactivado'` y `modulo='Usuarios'`.
- Sin impacto en `recuperar`/`login`: `username` sigue siendo DNI y `password` se re-hashea al reactivar.
