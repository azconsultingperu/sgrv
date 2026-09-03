## Purpose

Permitir reusar el DNI de un usuario eliminado reactivando la misma fila (soft delete) para no duplicar historial, manteniendo unicidad solo entre usuarios activos y trazabilidad en Auditoría.

## ADDED Requirements

### Requirement: Validación de unicidad solo sobre activos

Al crear un usuario en `POST /usuarios/crear`, las checks de unicidad para `dni`, `username` y `email` SHALL filtrar `eliminado=False`; una coincidencia solo con filas `eliminado=True` no SHALL bloquear la creación y SHALL disparar el flujo de reactivación.

#### Scenario: DNI solo en eliminado no bloquea
- **WHEN** existe un usuario con `dni=71184654` y `eliminado=True` y se envía `POST /usuarios/crear` con `dni=71184654`, `email=nuevo@x.com`, `rol` y `password` válidos
- **THEN** la respuesta no contiene `El DNI ya está registrado` y el sistema procede a reactivar (ver siguiente requirement), con status 302 a `/usuarios/` en caso feliz.

#### Scenario: Email solo en eliminado no bloquea
- **WHEN** existe un usuario eliminado con `email=a@x.com` y se crea con `email=a@x.com` y DNI libre
- **THEN** no se muestra `El correo electrónico ya está registrado` y la creación procede.

#### Scenario: Coincidencia con activo sí bloquea
- **WHEN** existe un usuario con `dni=12345678` y `eliminado=False` y se intenta crear con el mismo DNI
- **THEN** se muestra `El DNI ya está registrado` y no se crea ni se reactiva.

### Requirement: Reactivación de fila existente sobre DNI eliminado

Cuando `POST /usuarios/crear` trae un `dni` que existe con `eliminado=True`, el sistema SHALL reutilizar esa fila: `eliminado=False`, `estado=True`, actualizar `nombres`, `apellidos`, `email`, `rol_id`, `password_hash` (nueva contraseña), `actualizado_en=peru_now()`, y `avatar` según flujo, sin crear fila nueva; además SHALL resetear `intentos_fallidos` y `bloqueado_hasta`.

#### Scenario: Reactivar actualiza campos y no duplica fila
- **WHEN** `71184654` está eliminado con `nombres=VIEJO` y se crea con `nombres=JUAN DAVID`, `apellidos=RIVERA HUANCAS`, `email=juandavid@x.com`, `rol=1`, `password=NuevaPass123`
- **THEN** tras el `POST`, `Usuario.query.filter_by(dni='71184654').count() == 1`, ese registro tiene `eliminado=False`, `estado=True`, `nombres=JUAN DAVID`, `email=juandavid@x.com` y `check_password('NuevaPass123') is True`, y el conteo total de filas no aumenta en 1 extra.

#### Scenario: Reactivar limpia bloqueo previo
- **WHEN** el registro eliminado tenía `intentos_fallidos=5` y `bloqueado_hasta` en futuro
- **THEN** tras reactivar, `intentos_fallidos == 0` y `bloqueado_hasta is None`.

### Requirement: Índice único parcial en BD

La BD SHALL tener `UNIQUE` solo para filas activas: `CREATE UNIQUE INDEX ... ON usuarios(dni) WHERE eliminado = false` y análogo para `username` (y para `email` si se decide unicidad activa), reemplazando el `UNIQUE` global; así puede haber múltiples filas históricas con el mismo DNI pero solo una con `eliminado=False`.

#### Scenario: Dos filas históricas con mismo DNI permitidas
- **WHEN** se inserta (vía migración/seed) una fila `dni=71184654, eliminado=True` y otra `dni=71184654, eliminado=False`
- **THEN** la BD lo permite; en cambio, dos filas con `eliminado=False` y mismo DNI violan el índice y la BD rechaza el `INSERT`.

#### Scenario: Intentar crear duplicado activo falla a nivel BD
- **WHEN** ya existe `dni=12345678, eliminado=False` y se intenta `INSERT` directo con mismo DNI y `eliminado=False`
- **THEN** la BD lanza violación de unicidad y el handler la traduce a `El DNI ya está registrado`.

### Requirement: Auditoría de reactivación

Cada reactivación SHALL registrar en `auditorias` un evento `Usuario reactivado` en `modulo=Usuarios` con `usuario_id` del actor, `ip_address` y `user_agent` del request, y `detalle` que incluya `dni`/`username` reactivado, distinto de `Usuario creado` y `Usuario eliminado`.

#### Scenario: Auditoría tras reactivar
- **WHEN** se completa la reactivación de `71184654` por el admin `12345678` desde `1.2.3.4`
- **THEN** existe `Auditoria(accion='Usuario reactivado', modulo='Usuarios', detalle LIKE '%71184654%', ip_address='1.2.3.4')` y no se crea un `UsuarioCreado` duplicado para auditoría de creación.

### Requirement: Verificación en tiempo real filtra eliminados

`GET /usuarios/verificar-dni?dni=...` SHALL responder `{"existe": false}` cuando el único registro con ese DNI tiene `eliminado=True`, y `true` solo si hay coincidencia con `eliminado=False`.

#### Scenario: Verificar DNI eliminado retorna false
- **WHEN** `71184654` solo existe como `eliminado=True` y se llama `GET /usuarios/verificar-dni?dni=71184654`
- **THEN** la respuesta JSON es `{"existe": false}` y el frontend no muestra "ya existe".

#### Scenario: Verificar DNI activo retorna true
- **WHEN** `12345678` existe con `eliminado=False` y se verifica
- **THEN** la respuesta es `{"existe": true}`.
