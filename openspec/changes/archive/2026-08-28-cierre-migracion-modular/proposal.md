## Why

La reestructura a monolito modular está al 85%: identidad y registro están completos, pero quedan dos deudas que rompen la claridad del sistema — el módulo `notifications` solo existe como `application/event_handlers.py` sin `domain/infrastructure/presentation/public.py`, y los shims legacy `app/controllers/`, `app/models/`, `app/services/` mantienen una doble vía de imports (módulos vs shims). Cada nuevo dev debe aprender dos formas de hacer lo mismo y el linter no puede cerrar el ciclo. Hay que consolidar para dejar una sola forma canónica: módulos + `public.py` + bus de eventos.

## What Changes

- **BREAKING (interno, no URLs/BD):** Eliminar `app/controllers/*.py` y `app/models/*.py` como shims (re-export) una vez que todos los imports internos usen `app/modules/*/presentation` y `app/modules/*/domain` o `public.py`.
- Completar `app/modules/notifications/` al layout oficial: `domain/` (vacío o tipos), `infrastructure/` (si aplica), `presentation/` (si aplica), `public.py` (fachada si se expone), y mover `app/services/email_service.py` a `notifications/infrastructure/email_adapter.py` o `application/` sin que otros módulos importen `app.services` directo.
- Migrar llamadas directas restantes `registrar_auditoria()` / `notificar_nuevo_*()` en `identidad/presentation/*` y `registro/presentation/*` a `publish(DomainEvent)` + handlers suscritos (auditoria y notifications ya escuchan; falta desacoplar perfil/avatar si aplica).
- Ajuste menor en `registro/public.py:dashboard_get_totales()` que hoy importa `identidad.public` — documentar como excepción controlada o mover la agregación a `dashboard` para romper el ciclo conceptual registro→identidad.
- Sin cambios de URLs, templates, ni esquema BD; migraciones existentes intactas.

## Capabilities

### New Capabilities
- `notifications`: Estructura completa del módulo notifications y contrato de envío de emails vía eventos (sin import directo desde otros módulos).

### Modified Capabilities
- `modular-boundaries`: Cierre de shims legacy y exigencia de layout completo para todos los módulos (incluido notifications).
- `domain-events`: Reemplazo total de calls directos por `publish()` para auditoría/notifications; `perfil` avatar también vía eventos si aplica.

## Impact

- **Código afectado:** `app/modules/notifications/**`, `app/services/email_service.py`, `app/services/auditoria_service.py`, `app/controllers/*`, `app/models/*`, `app/modules/identidad/presentation/perfil_controller.py`, `app/modules/registro/presentation/registro_controller.py`, `app/__init__.py` (bootstrap sigue igual), `setup.cfg` (añadir contratos para notifications si faltan).
- **APIs/URLs:** Sin cambios observables.
- **Riesgo:** Bajo. Refactor interno verificable con `make lint-boundaries` y `pytest` verdes; shims se eliminan al final para rollback simple re-registrando blueprint legacy.
