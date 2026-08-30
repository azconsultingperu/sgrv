## MODIFIED Requirements

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
