## Purpose

Completar el módulo notifications al layout oficial del monolito modular y centralizar el envío de emails vía eventos de dominio sin imports directos cross-módulo.

## ADDED Requirements

### Requirement: Estructura completa de notifications

El módulo `app/modules/notifications/` SHALL respetar el layout `domain/`, `application/`, `infrastructure/`, `presentation/` + `public.py` (o `__init__.py` re-export) como los demás módulos, y SHALL exponer su comportamiento solo vía `public.py` o eventos.

#### Scenario: Layout válido
- **WHEN** se lista `app/modules/notifications/`
- **THEN** existen `domain/`, `application/`, `infrastructure/`, `presentation/` y `public.py` (aunque `domain`/`presentation` puedan ser mínimos) y `make lint-boundaries` pasa.

#### Scenario: Sin import directo a services
- **WHEN** `app/modules/registro` o `identidad` necesitan enviar email
- **THEN** no contienen `from app.services.email_service import` y en su lugar publican `AlumnoRegistrado`/`UsuarioCreado` que `notifications` escucha.

### Requirement: Envío de email vía eventos

`notifications` SHALL enviar emails solo como handler suscrito a `AlumnoRegistrado` y `UsuarioCreado` vía `app/shared/events.py`, usando un adapter de infraestructura que envuelva `smtplib` y SHALL aislar errores sin revertir la transacción ya commiteada.

#### Scenario: Email tras registro
- **WHEN** `registro_service.crear_alumno_con_visita` publica `AlumnoRegistrado` y hace commit
- **THEN** `notifications/application/event_handlers.py:on_alumno_registrado` intenta enviar email y, si SMTP falla, loguea y no bloquea el request (302 éxito).

#### Scenario: Sin evento no hay email
- **WHEN** se crea un alumno pero la transacción hace rollback
- **THEN** ningún email se envía.
