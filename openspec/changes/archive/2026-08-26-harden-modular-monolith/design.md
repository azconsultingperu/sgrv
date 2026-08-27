## Context

SGRV es un monolito modular laxo: 8 blueprints en `app/controllers/*.py` (`app/__init__.py:42`), 11 modelos en `app/models/*.py`, 4 services en `app/services/*.py` y `app/config.py:6`. No hay fronteras de importación: cualquier controller importa cualquier modelo (`app/controllers/consulta_controller.py:17`, `app/controllers/registro_controller.py:3-7`). Calls directos `registrar_auditoria` (`app/controllers/registro_controller.py:8`) y `notificar_nuevo_registro` (`app/controllers/registro_controller.py:9`) acoplan registro→auditoría/email. Ver análisis en `proposal.md - Why`. La BD es única (PostgreSQL/SQLite) con `migrations/` Alembic; URLs y `create_app()` deben permanecer compatibles.

## Goals / Non-Goals

**Goals:**
- Fronteras verificables automáticamente que impidan imports cruzados ilegales y ciclos.
- Desacople de módulos vía eventos en-proceso con atomicidad transaccional.
- Repositorios + UoW para aislar `Model.query` dentro del módulo dueño.
- Migración incremental (strangler) sin downtime ni cambio de BD/framework.

**Non-Goals:**
- Microservicios, brokers externos (RabbitMQ/Kafka), o split de BD.
- Reescritura de templates/static o de `migrations/` existentes.
- DDD táctico completo (aggregates/event sourcing); solo el slice necesario para fronteras.
- Cambiar `Flask-Login`, `Flask-Migrate`, `psycopg2`, `peru_now` time handling.

## Decisions

### 1. Estructura `app/modules/<dominio>/` + `app/shared/` (sobre `app/controllers|models|services` planos)
- **Decisión:** Crear `app/modules/identidad` (usuarios/roles/auth/sesion/perfil), `app/modules/registro` (alumno/visita/promotor/institucion/carrera), `app/modules/consulta`, `app/modules/dashboard`, `app/modules/auditoria`, `app/modules/reportes`; y `app/shared/` para `db` (`app/__init__.py:10`), `time_utils`, `events`, `errors`, `config` re-export.
- **Rationale:** Features verticales reducen blast radius; `shared` mínimo evita "utils" bote de basura. Un módulo por bounded context real del dominio SGRV, no por capa técnica.
- **Alternativas:** Mantener layout plano + solo linter → rechazada: sin reubicación física el coupling sigue invisible. Full DDD con aggregates → over-engineering para 2k LOC de controllers.
- **Migración:** Mover archivos (git mv), re-exportar `public.py` por módulo, y en `app/__init__.py` importar blueprints desde nueva ruta. Mantener alias `app/controllers/*` como shim deprecado 1 versión.

```
app/
├── shared/
│   ├── db.py (re-export de app/__init__.py:db)
│   ├── events.py
│   ├── time_utils.py
│   ├── errors.py
│   └── config.py
└── modules/
    ├── identidad/
    │   ├── domain/ (usuario, rol, sesion, avatar)
    │   ├── application/ (auth_service, user_service, event_handlers, unit_of_work)
    │   ├── infrastructure/ (usuario_repository, avatar_storage)
    │   ├── presentation/ (auth_controller, usuarios_controller, perfil_controller)
    │   └── public.py  ← facade: login(), crear_usuario(), get_usuario()
    ├── registro/      ← alumno, visita, institucion, carrera, promotor
    ├── consulta/
    ├── dashboard/
    ├── auditoria/
    └── reportes/
```

### 2. `import-linter` como guard de fronteras (sobre ruff solo)
- **Decisión:** `import-linter==1.13` con contrato `forbidden` + `layers` en `.importlinter` / `setup.cfg`. Checks: `identidad.domain` no depende de nadie, `modules.*.domain` independiente, `presentation → application → domain`, prohibición `modules.X → modules.Y.domain/infrastructure/presentation`.
- **Rationale:** `import-linter` valida grafo de imports estático sin runtime; integra con `pytest --import-linter` y CI. Ruff solo puede banear patterns sueltos.
- **Alternativa:** `deptry`, `tach` → menos maduras para layers/contracts. Validación manual en `conftest.py` → frágil.
- **CI:** `make lint-boundaries` / `pytest -m import_linter` falla PR si viola.

### 3. Repository + Unit of Work (sobre `Model.query` directo)
- **Decisión:** Interface `AlumnoRepository` en `domain` (`save`, `find_by_dni`, `list`), impl `SqlAlumnoRepository` en `infrastructure` usando `db.session`. `UnitOfWork` context manager (`__enter__/__exit__`) hace `commit/rollback` y drena `events` publicados.
- **Rationale:** Encapsula `eliminado=False` y `joinedload` repetidos (`app/controllers/consulta_controller.py:17`), permite mock en tests, y es prerequisite para atomicidad de eventos.
- **Alternativa:** Seguir con `Model.query` + service layer fino → no resuelve coupling cross-módulo. SQLAlchemy 2.0 `select()` puro → migración mayor sin beneficio inmediato.
- **Compat:** Repos usan mismo `db` y modelos SQLAlchemy existentes; no cambia esquema ni `migrations/env.py`.

### 4. Event bus síncrono en-proceso con outbox en memoria (sobre broker externo)
- **Decisión:** `app/shared/events.py` con `EventBus` singleton, `publish(event)` encola en `UoW.events`, `commit()` drena y despacha sincrónicamente en orden de suscripción. Si handler falla → log + continúa. Sin persistencia de outbox en BD en v1 (YAGNI hasta necesitar retry).
- **Rationale:** SGRV no necesita eventual consistency distribuida; sync en-proceso mantiene semántica request/response actual y garantiza que auditoría/email no requieran infra extra. Atomicidad vía UoW evita "evento publicado pero rollback" (ver `specs/domain-events`).
- **Alternativa:** Celery/RQ → complejidad operativa cPanel. Outbox table + poller → justificar cuando email deba ser retryable tras caída SMTP.
- **Bootstrap:** `create_app()` importa `app/modules/*/application/event_handlers.py:register(bus)` al final de `app/__init__.py:50`.

### 5. Facade `public.py` como contrato cross-módulo
- **Decisión:** Cada módulo expone funciones de alto nivel (`registro.public.buscar_alumnos(filtros)`, `identidad.public.get_usuario(id)`). Internamente delegan a `application`. Otros módulos solo importan `public`.
- **Rationale:** Un punto de importación auditable por `import-linter`, evolución sin romper callers.
- **Alternativa:** Importar `application` directo → expone demasiada superficie.

## Risks / Trade-offs

- **Migración parcial deja dos layouts conviviendo** → Mitigación: strangler por módulo, shims `app/controllers/*.py` re-exportan desde `modules/` y se eliminan al final; `tasks.md` ordena `identidad` primero (más aislado).
- **Over-abstracción (repos para CRUD trivial)** → Mitigación: repos solo donde hay cross-módulo o lógica `eliminado`; `consulta` puede usar facade `registro` sin repo propio.
- **Eventos sync alargan request si handler lento (email SMTP)** → Mitigación: email handler hace `try/except` y no bloquea; en `specs/domain-events` el error no revierte commit. Futuro: mover email a job async sin cambiar contrato `publish`.
- **Linter falsos positivos por imports dinámicos** → Mitigación: allowlist explícita en `.importlinter` para `app/shared`, y `import-linter` solo sobre `app/modules`.
- **Circular import en `create_app` al registrar handlers** → Mitigación: `register(bus)` importa lazy dentro de función, no a nivel módulo; bootstrap al final de `create_app()`.

## Migration Plan

1. **Fase 0 - Infra sin mover código:** Crear `app/shared/events.py` + `app/shared/db.py` re-export, `UnitOfWork`, y `.importlinter` en modo `warn`. CI en `allow_failure`.
2. **Fase 1 - `identidad` (menor coupling):** Mover `usuario/rol/sesion` + `auth/usuarios/perfil` controllers. Registrar blueprint desde nueva ruta. Activar `forbidden: identidad.domain → application`. Verificar `pytest tests/test_auth.py tests/test_usuarios.py`.
3. **Fase 2 - `registro` + eventos:** Mover `alumno/visita/institucion/carrera/promotor`. Reemplazar `registrar_auditoria`/`notificar_nuevo_registro` por `publish(AlumnoRegistrado)`. Migrar `auditoria` y `email` a handlers. Activar regla `registro → auditoria` prohibida directo.
4. **Fase 3 - `consulta/dashboard/reportes`:** Consumir `registro.public` vía facade/repos, no `Alumno.query` directo. Endurecer linter a `error`.
5. **Fase 4 - Limpieza:** Eliminar shims `app/controllers/`/`app/models/` legacy (quedan como re-exports vacíos 1 sprint), `app/services/` deprecado, `.importlinter` en `error` bloqueante.
6. **Rollback:** Cada fase es revertible: `app/__init__.py:42` vuelve a importar blueprint legacy. BD/migraciones nunca cambian.

## Open Questions

- ¿Outbox persistido en `auditorias`/`event_outbox` para retry de email tras caída SMTP en prod cPanel, o es suficiente log + reintento manual en v1? (No bloquea specs; default v1 = sin outbox.)
- ¿Incluir `perfil` (avatars) en `identidad` o módulo propio `perfil`? Propuesta: dentro de `identidad` (avatar es atributo de `Usuario`), pero se puede split sin cambiar `public.py` si crece.
