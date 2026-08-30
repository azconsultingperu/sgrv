## Context

SGRV está en `app/modules/` con kernel `app/shared/` ya probado (events+UoW). Ver `proposal.md - Why`. Dos deudas impiden cerrar: `notifications` incompleto y shims `app/controllers`, `app/models`, `app/services` que duplican la vía canónica. `setup.cfg` ya tiene 5 contratos lint-imports y `tests/test_boundaries.py` los congela.

## Goals / Non-Goals

**Goals:**
- Completar `notifications` al layout oficial sin cambiar comportamiento observable (mismo email, mismos eventos).
- Migrar calls directos restantes a `publish()` para que `app/services` deje de ser importado cross-módulo.
- Eliminar shims legacy manteniendo URLs/BD/templates idénticos, verificable con `lint-boundaries` + `pytest`.

**Non-Goals:**
- Cambiar URLs, templates, esquema BD ni migraciones Alembic.
- Rediseño visual o nuevas dependencias.
- Cambiar `dashboard_get_totales()` más allá de documentar la excepción registro→identidad o mover agregación mínima si no rompe tests.

## Decisions

### 1. Notifications como módulo completo con adapter de email
- **Decisión:** Crear `app/modules/notifications/domain/` (tipos mínimos), `infrastructure/email_adapter.py` (wrapping de `smtplib` actual), `application/event_handlers.py` ya existente, `public.py` si expone facade. `app/services/email_service.py` pasa a shim re-export o se elimina tras migrar.
- **Rationale:** Mantiene `notifications` alineado a `modular-boundaries` spec y evita que `registro`/`identidad` importen `app.services` directo.
- **Alternativa:** Dejar `email_service` en `app/services` — rechazada: perpetúa doble vía.

### 2. Auditoría 100% vía bus, sin `registrar_auditoria()` directo en controllers
- **Decisión:** `perfil_controller` y `registro_controller` que hoy hacen `registrar_auditoria()` directo pasan a `publish(AvatarActualizado/ AlumnoRegistrado)` o mantienen auditoría vía evento ya existente; `app/services/auditoria_service.py` queda como handler o shim.
- **Rationale:** Ya existe `auditoria/application/event_handlers.py:15` suscrito; completar el desacoplo cierra `domain-events` Requirement 7.
- **Alternativa:** Mantener calls directos — rechazada: viola spec domain-events.

### 3. Eliminación de shims al final, con rollback simple
- **Decisión:** Migrar todos los imports internos primero (`app/models` → `modules/*/domain`, `app/controllers` → `modules/*/presentation`), verificar `pytest` y `lint-imports` verdes, luego borrar directorios legacy en un commit final.
- **Rationale:** Permite revertir re-registrando blueprint legacy en `app/__init__.py:33` sin tocar BD.
- **Alternativa:** Borrar shims al inicio — rechazada: rompe tests intermedios.

### 4. `dashboard_get_totales()` documentado como excepción controlada
- **Decisión:** Dejar `registro/public.py:47` importando `identidad.public.count_usuarios` pero añadir comentario y contrato en `setup.cfg` que `public→public` está permitido; si el linter lo bloquea, mover agregación a `dashboard/application/estadistica_service.py` que ya delega.
- **Rationale:** Evita refactor grande solo para romper ciclo menor; `dashboard` ya delega correctamente.

## Risks / Trade-offs

- **Borrar shims rompe imports externos no migrados** → Mitigación: grep `from app.models` / `from app.controllers` / `from app.services` antes de borrar; mantener `app/services` como shim 1 commit más si hay uso externo.
- **Email handler con `request` fuera de contexto** → Mitigación: `notifications` y `auditoria` ya usan `try: request.remote_addr` con fallback `None`; mantener pattern.
- **Ciclo registro→identidad en `public`** → Mitigación: documentar excepción; si `lint-imports` falla, mover conteo a `dashboard`.

## Migration Plan

1. Completar `notifications` layout + adapter email, migrar imports.
2. Migrar `perfil_controller`/`registro_controller` de `registrar_auditoria` directo a `publish()` donde falte.
3. Reemplazar todos `from app.models` / `from app.controllers` / `from app.services` por `modules/*/public` o eventos; `make lint-boundaries` verde.
4. Borrar `app/controllers/`, `app/models/`, `app/services/` legacy; `pytest` verde.
5. Rollback: re-crear shims re-export y re-registrar blueprint en `app/__init__.py`.

## Open Questions

- ¿`notifications/public.py` debe exponer `send_email()` facade o solo handlers internos? Default: solo handlers, sin facade pública por ahora.
