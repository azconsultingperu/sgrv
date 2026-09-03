## Context

Ver `proposal.md`. Hoy `usuarios_controller.crear()` hace `filter_by(dni).first()` sin `eliminado` y el modelo tiene `unique=True` global en `dni`/`username`, por lo que un soft delete deja el DNI bloqueado. Se quiere reactivar la misma fila para preservar FKs de auditoría.

## Goals / Non-Goals

**Goals:**
- Reusar DNI de eliminado reactivando la fila existente y manteniendo historial.
- Unicidad garantizada solo entre activos vía índice parcial.
- Trazabilidad con `Usuario reactivado` en auditoría.
- `verificar_dni` coherente con la misma regla.

**Non-Goals:**
- Permitir dos activos con mismo DNI (siempre 1).
- Crear fila nueva y dejar la vieja como histórica duplicada.
- Cambiar soft delete de `eliminar` (sigue `eliminado=True`).
- Tocar `recuperar`/`login` ni flujo de sesión más allá de `resetear_intentos`.

## Decisions

**1. Filtrar por `eliminado=False` en checks**
- `crear()` hará `filter_by(dni=dni, eliminado=False)` (y análogos para `username`/`email`). Si encuentra eliminado, entra a rama de reactivación en vez de `flash` de duplicado.
- Alternativa `filter_by(dni=dni).first() and check eliminado flag` descartada por más ramas; el filtro directo es más claro y usa índice parcial.

**2. Reactivar vs crear**
- Si existe `eliminado=True` con el DNI, se hace `update` sobre esa instancia: `eliminado=False`, `estado=True`, campos del form, `set_password`, `actualizado_en`, `avatar=None` si no se migran, `intentos_fallidos=0`, `bloqueado_hasta=None`. No se hace `db.session.add()` nuevo. Se evita `INSERT` y se respeta FKs de auditorías pasadas.
- Alternativa crear nueva fila y dejar la vieja con `dni` renombrado (ej. `dni_71184654_old`) descartada por romper trazabilidad simple y requerir renombres.

**3. Índice único parcial**
- PostgreSQL: `CREATE UNIQUE INDEX uq_usuarios_dni_activo ON usuarios(dni) WHERE eliminado = false` (análogo `username` y `email`). SQLite en tests soporta `WHERE` desde 3.8.0, que es el de `sqlite:///:memory:` en `TestingConfig`.
- Se elimina el `unique=True` del `Column` y se reemplaza por `Index(..., unique=True, postgresql_where=..., sqlite_where=...)` o DDL raw en migración. Se mantiene `index=True` base.
- Alternativa dejar `unique=True` y en reactivación hacer `DELETE` físico de la fila eliminada descartada por perder auditoría.
- Migración: `batch_alter_table` no puede alterar `unique`; se hace `drop_constraint`/`drop_index` + `create_index` parcial. Para downgrade se revierte a `unique=True` global (con check de que no haya duplicados activos).

**4. Auditoría `Usuario reactivado`**
- Se inserta `Auditoria(accion='Usuario reactivado', modulo='Usuarios', detalle=f'Usuario reactivado: {dni} ({nombres})', ip, ua)` en el mismo `commit` que la reactivación, sin `publish` de evento nuevo (se puede añadir `UsuarioReactivado` a `events.py` si se quiere, pero v1 es solo auditoría directa para no ampliar bus).
- Distinto de `Usuario creado` para que el historial no se confunda.

**5. `verificar_dni`**
- Cambia a `filter_by(dni=dni, eliminado=False)`. Mantiene respuesta `{"existe": false}` para eliminados, permitiendo al frontend habilitar el submit.

## Risks / Trade-offs

- **Índice parcial no soportado en MySQL cPanel** → Mitigación: cPanel usa MySQL, que no soporta `WHERE` en índice único; se deja el `UNIQUE` global y la reactivación se hace vía `UPDATE` (no necesita duplicar), por lo que la violación no ocurre si no se inserta duplicado. La migración detecta `dialect` y solo crea índice parcial en PG/SQLite, en MySQL mantiene `unique` pero la lógica de `UPDATE` evita el conflicto. Documentar limitación.
- **Condición de carrera: dos creates concurrentes con mismo DNI eliminado** → Mitigación: la segunda transacción verá la fila ya reactivada (`eliminado=False`) y caerá en `unique` parcial → se traduce a `flash` de duplicado; no hay duplicado activo.
- **Email duplicado entre activo y eliminado** → Mitigación: mismo patrón `eliminado=False` para `email`; si el email del reactivado colisiona con otro activo distinto, se bloquea con `El correo ya está registrado` (se valida antes de reactivar).
- **Sesiones viejas del eliminado** → Mitigación: al reactivar, `sesiones` antiguas ya están `activa=False` desde el soft delete; no se reactivan.

## Migration Plan

1. Migración Alembic: `drop` de `unique` en `dni`/`username`/`email` + `create_unique_index` parcial `WHERE eliminado = false`.
2. Deploy código: `crear()` y `verificar_dni()` con filtro, rama de reactivación.
3. `flask db upgrade` en dev y `FLASK_APP=passenger_wsgi.py flask db upgrade` en cPanel (MySQL: la migración detecta dialect y skip índice parcial).
4. Rollback: `flask db downgrade` recrea `UNIQUE` global (requiere que no haya dos activos con mismo DNI, que no habrá por lógica).

## Open Questions

- Ninguna; el índice parcial en MySQL queda como limitación documentada, sin cambiar spec.
