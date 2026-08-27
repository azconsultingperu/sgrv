## Purpose

Desacoplar la comunicación entre módulos mediante eventos de dominio en-proceso para eliminar dependencias directas tipo import de email/auditoría desde registro y permitir crecimiento sin acoplamiento.

## ADDED Requirements

### Requirement: Bus de eventos en-proceso

El sistema SHALL proveer un bus síncrono en memoria `app/shared/events.py` con `publish(event)` y `subscribe(event_type, handler)` que entregue eventos en el mismo proceso y request, sin broker externo.

#### Scenario: Publicación entrega a suscriptor
- **WHEN** `publish(AlumnoRegistrado(alumno_id=1, dni="71234001"))` se invoca dentro de un request
- **THEN** todos los handlers suscritos a `AlumnoRegistrado` se ejecutan antes de que `publish` retorne

#### Scenario: Sin suscriptor no falla
- **WHEN** se publica un evento sin handlers registrados
- **THEN** `publish` retorna sin error ni efecto colateral

### Requirement: Eventos tipados y catálogo

Cada evento SHALL ser un dataclass inmutable con `event_type`, `occurred_at` (`peru_now`), `actor_id` y payload tipado. El catálogo inicial SHALL incluir `AlumnoRegistrado`, `AlumnoEliminado`, `UsuarioCreado`, `UsuarioEliminado`, `AvatarActualizado`, `AvatarEliminado`.

#### Scenario: Evento con schema válido
- **WHEN** `AlumnoRegistrado` se construye con `alumno_id`, `dni`, `nombres`, `actor_id`
- **THEN** el evento contiene `occurred_at` autocompletado y es serializable a dict

#### Scenario: Evento con campo faltante
- **WHEN** se intenta construir `AlumnoRegistrado` sin `dni`
- **THEN** la construcción falla con error de validación

### Requirement: Atomicidad con la transacción

Los handlers SHALL ejecutarse solo si la transacción que publicó el evento hace `commit` exitoso. Si la transacción hace `rollback`, los eventos publicados en ese `unit_of_work` SHALL descartarse y ningún handler SHALL ejecutarse.

#### Scenario: Commit dispara handlers
- **WHEN** `registro_service.crear_alumno()` publica `AlumnoRegistrado` y hace `commit`
- **THEN** los handlers de auditoría y email se ejecutan y `auditorias` contiene el registro

#### Scenario: Rollback descarta eventos
- **WHEN** `crear_alumno()` publica `AlumnoRegistrado` pero luego falla y hace `rollback`
- **THEN** ningún handler se ejecuta y no queda fila en `auditorias` ni email enviado

### Requirement: Handlers desacoplados entre módulos

Ningún módulo SHALL importar handlers de otro módulo directamente. Cada módulo SHALL registrar sus handlers en su `application/event_handlers.py` y el bootstrap `app/__init__.py:create_app()` SHALL suscribirlos al bus al iniciar.

#### Scenario: Handler registrado vía bootstrap
- **WHEN** la app inicia y `app/modules/auditoria/application/event_handlers.py` registra `on_alumno_registrado`
- **THEN** publicar `AlumnoRegistrado` dispara la inserción en `auditorias` sin que `registro` importe `auditoria`

#### Scenario: Import directo de handler prohibido
- **WHEN** `app/modules/registro/application/service.py` hace `from app.modules.auditoria.application.event_handlers import on_alumno_registrado`
- **THEN** el linter de fronteras falla

### Requirement: Orden y error aislado de handlers

El bus SHALL ejecutar handlers en orden de suscripción y SHALL aislar errores: si un handler lanza excepción, SHALL loguear y continuar con los siguientes sin revertir la transacción ya commiteada.

#### Scenario: Error en un handler no bloquea otros
- **WHEN** `email.on_alumno_registrado` falla (SMTP caído) y `auditoria.on_alumno_registrado` está suscrito después
- **THEN** `auditoria` se registra igual, el error de email queda en `logs` y el request retorna 302 éxito al usuario

#### Scenario: Orden determinístico
- **WHEN** dos handlers `A` y `B` se suscriben en ese orden a `AlumnoRegistrado`
- **THEN** `A` se ejecuta antes que `B` en cada `publish`

### Requirement: Reemplazo de calls directos actuales

Los calls directos `registrar_auditoria()` y `notificar_nuevo_registro()` / `notificar_nuevo_usuario()` desde controllers SHALL reemplazarse por `publish()` del evento correspondiente; los services de email/auditoria SHALL migrar a handlers suscritos.

#### Scenario: Registro ya no importa auditoria
- **WHEN** `app/modules/registro/presentation/controller.py` crea un alumno
- **THEN** el archivo no contiene `from app.services.auditoria_service import registrar_auditoria` y en su lugar hace `publish(AlumnoRegistrado(...))`

#### Scenario: Auditoría vía evento
- **WHEN** `AlumnoRegistrado` es publicado
- **THEN** `app/modules/auditoria/application/event_handlers.py:on_alumno_registrado` inserta fila con `accion="Creación de registro"`, `modulo="Registro"`, `ip_address` del request

### Requirement: Compatibilidad en tests

Los tests SHALL poder publicar y asertar eventos sin infraestructura externa, usando un bus de prueba o spy que capture eventos publicados.

#### Scenario: Test aserta evento publicado
- **WHEN** `test_registro.py` hace `POST /registro/` con payload válido en `TestingConfig`
- **THEN** el test puede asertar que `AlumnoRegistrado(dni="55556666")` fue publicado sin enviar email real
