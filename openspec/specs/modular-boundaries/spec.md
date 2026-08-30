## Purpose

Establecer fronteras estrictas entre módulos del monolito para que SGRV crezca añadiendo módulos sin acoplamiento cruzado ni regresiones, verificables automáticamente en CI.

## Requirements

### Requirement: Estructura de módulos por dominio

El sistema SHALL organizar el código bajo `app/modules/<dominio>/` donde cada dominio expone su API pública únicamente vía `public.py` (o `__init__.py` re-export) y mantiene `domain/`, `application/`, `infrastructure/`, `presentation/` como subpaquetes internos. Todos los módulos, incluido `notifications`, SHALL cumplir este layout; `app/controllers/` y `app/models/` legacy SHALL no existir tras el cierre (solo shims temporales durante migración).

#### Scenario: Nuevo módulo respeta layout
- **WHEN** se crea `app/modules/seguimiento/` sin `public.py` o con archivos fuera de las cuatro capas
- **THEN** la validación de estructura falla y el PR es rechazado

#### Scenario: Módulo existente migrado conserva comportamiento
- **WHEN** `app/controllers/registro_controller.py` se reubica a `app/modules/registro/presentation/controller.py` y `app/modules/registro/public.py` re-exporta `registro_bp`
- **THEN** `GET /registro/` responde igual (status, template, permisos) que antes de la migración

#### Scenario: Notifications completo
- **WHEN** se lista `app/modules/notifications/`
- **THEN** contiene `domain/`, `application/`, `infrastructure/`, `presentation/` y `public.py` y no hay `from app.services.email_service import` en otros módulos

### Requirement: Capas y dirección de dependencias

Cada módulo SHALL respetar la dirección `presentation → application → domain ← infrastructure` y SHALL prohibir que `domain` importe `application`, `infrastructure` o `presentation`, y que `infrastructure` sea importado por otros módulos.

#### Scenario: Dependencia ilegal en domain
- **WHEN** `app/modules/registro/domain/alumno.py` importa `from app.modules.registro.application.registro_service import X`
- **THEN** el linter de fronteras reporta violación y el build falla

#### Scenario: Dependencia válida
- **WHEN** `app/modules/registro/application/registro_service.py` importa `from app.modules.registro.domain.alumno import Alumno`
- **THEN** la validación pasa

### Requirement: API pública como único punto de acoplamiento cross-módulo

Un módulo SHALL acceder a otro módulo únicamente vía su `public.py` (facade / use-cases expuestos) o vía eventos de dominio. La importación directa de `domain`, `infrastructure` o `presentation` de otro módulo SHALL ser prohibida.

#### Scenario: Import cross-módulo directo bloqueado
- **WHEN** `app/modules/consulta/presentation/controller.py` hace `from app.modules.registro.domain.alumno import Alumno`
- **THEN** el check de fronteras falla con mensaje que indica usar `app.modules.registro.public` o evento

#### Scenario: Import vía facade permitido
- **WHEN** `app/modules/consulta/application/query_service.py` hace `from app.modules.registro.public import buscar_alumnos`
- **THEN** la validación pasa

### Requirement: Repositorios y prohibición de query directa cross-módulo

Cada agregado SHALL exponer un `Repository` interface en `domain` y su implementación SQLAlchemy en `infrastructure`. Los controllers y services de otros módulos SHALL no ejecutar `Model.query` / `db.session.query(Model)` sobre modelos que no pertenecen a su dominio.

#### Scenario: Query directa cross-módulo detectada
- **WHEN** `app/modules/dashboard/application/stats_service.py` ejecuta `Alumno.query.filter_by(eliminado=False)`
- **THEN** el linter reporta violación y sugiere usar `alumno_repository` vía facade

#### Scenario: Repositorio propio permitido
- **WHEN** `app/modules/registro/infrastructure/alumno_repository.py` ejecuta `Alumno.query.filter_by(...)`
- **THEN** la validación pasa

### Requirement: Shared Kernel mínimo y explícito

El sistema SHALL proveer `app/shared/` que contenga únicamente infraestructura transversal (db, time_utils `peru_now`, `events`, `errors`, `config`). Ningún módulo SHALL importar `shared` que a su vez importe dominio; y ningún módulo SHALL añadir a `shared` código de dominio sin revisión.

#### Scenario: Shared importa dominio bloqueado
- **WHEN** `app/shared/events.py` importa `from app.modules.registro.domain.alumno import Alumno`
- **THEN** la validación de fronteras falla

#### Scenario: Uso legítimo de shared
- **WHEN** `app/modules/registro/domain/alumno.py` importa `from app.shared.time_utils import peru_now`
- **THEN** la validación pasa

### Requirement: Verificación automática en CI

El pipeline SHALL ejecutar el check de fronteras (`import-linter` o equivalente) en cada PR y en `pytest` local, fallando el build si hay ciclos o violaciones.

#### Scenario: CI bloquea violación
- **WHEN** un PR introduce una importación ilegal entre módulos
- **THEN** `lint:boundaries` falla, el PR no es mergeable y el log indica la arista violada

#### Scenario: Build verde sin violaciones
- **WHEN** todos los imports respetan `public.py` y capas
- **THEN** `lint:boundaries` pasa y el pipeline continúa a `pytest`

### Requirement: Migración incremental compatible

La migración SHALL mantener compatibilidad observable: mismas URLs, mismos templates, misma BD y migraciones Alembic existentes. Cada módulo migrado SHALL pasar los tests de regresión (`tests/test_*.py`) sin modificarlos salvo imports. Tras el cierre, `app/controllers/`, `app/models/` y `app/services/` legacy SHALL estar eliminados y `lint-boundaries` + `pytest` SHALL seguir verdes.

#### Scenario: URLs sin cambio
- **WHEN** se migra `usuarios` a `app/modules/identidad/`
- **THEN** `GET /usuarios/` y `POST /usuarios/crear` mantienen `url_prefix`, permisos y redirects

#### Scenario: Rollback por módulo
- **WHEN** un módulo migrado causa regresión
- **THEN** se puede revertir re-registrando el blueprint legacy en `app/__init__.py:42` sin tocar BD ni otros módulos

#### Scenario: Shims eliminados sin ruptura
- **WHEN** `app/controllers/` y `app/models/` se borran tras migrar todos los imports
- **THEN** `pytest tests/` y `venv/bin/lint-imports` siguen pasando y todas las rutas responden igual
