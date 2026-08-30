## MODIFIED Requirements

### Requirement: Reemplazo de calls directos actuales

Los calls directos `registrar_auditoria()` y `notificar_nuevo_registro()` / `notificar_nuevo_usuario()` desde controllers SHALL reemplazarse por `publish()` del evento correspondiente; los services de email/auditoria SHALL migrar a handlers suscritos. Tras el cierre, ningún `presentation` SHALL importar `app.services.auditoria_service` ni `app.services.email_service` directo; `perfil` y `registro` SHALL usar `publish(AvatarActualizado)` / `AlumnoRegistrado` según corresponda.

#### Scenario: Registro ya no importa auditoria
- **WHEN** `app/modules/registro/presentation/controller.py` crea un alumno
- **THEN** el archivo no contiene `from app.services.auditoria_service import registrar_auditoria` y en su lugar hace `publish(AlumnoRegistrado(...))`

#### Scenario: Auditoría vía evento
- **WHEN** `AlumnoRegistrado` es publicado
- **THEN** `app/modules/auditoria/application/event_handlers.py:on_alumno_registrado` inserta fila con `accion="Creación de registro"`, `modulo="Registro"`, `ip_address` del request

#### Scenario: Perfil avatar vía evento
- **WHEN** `perfil_controller` actualiza avatar
- **THEN** no hace `registrar_auditoria()` directo sino `publish(AvatarActualizado(...))` y `identidad/application/event_handlers.py` registra auditoría

### Requirement: Handlers desacoplados entre módulos

Ningún módulo SHALL importar handlers de otro módulo directamente. Cada módulo SHALL registrar sus handlers en su `application/event_handlers.py` y el bootstrap `app/__init__.py:create_app()` SHALL suscribirlos al bus al iniciar. `notifications` SHALL seguir este patrón con su `application/event_handlers.py` suscrito en `create_app()`.

#### Scenario: Handler registrado vía bootstrap
- **WHEN** la app inicia y `app/modules/auditoria/application/event_handlers.py` registra `on_alumno_registrado`
- **THEN** publicar `AlumnoRegistrado` dispara la inserción en `auditorias` sin que `registro` importe `auditoria`

#### Scenario: Import directo de handler prohibido
- **WHEN** `app/modules/registro/application/service.py` hace `from app.modules.auditoria.application.event_handlers import on_alumno_registrado`
- **THEN** el linter de fronteras falla

#### Scenario: Notifications suscrito vía bootstrap
- **WHEN** la app inicia y `app/modules/notifications/application/event_handlers.py` registra `on_alumno_registrado` y `on_usuario_creado`
- **THEN** publicar esos eventos dispara envío de email sin que `registro`/`identidad` importen `notifications`
