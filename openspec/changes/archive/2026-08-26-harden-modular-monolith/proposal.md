## Why

SGRV hoy es un monolito modular laxo (`app/controllers/` + `app/models/` compartidos sin fronteras de importación). Cualquier blueprint puede importar cualquier modelo (`app/controllers/consulta_controller.py:17` importa `Alumno`, `Visita`, `InstitucionEducativa` directamente), lo que hace que agregar un módulo nuevo o cambiar `Alumno` propague efectos a `registro`, `consulta`, `dashboard`, `reportes` y `estadistica_service`. Con 11 modelos, 8 blueprints y el roadmap de crecimiento (nuevos colegios/carreras, ML, notificaciones), el acoplamiento actual convierte cada cambio en regresión potencial. Es el momento de endurecer fronteras sin pagar el costo operativo de microservicios.

## What Changes

- **Estructura de módulos con fronteras explícitas**: Migrar de `app/controllers|models|services` planos a `app/modules/<dominio>/` con capas `domain / application / infrastructure / presentation`. Cada módulo expone solo una API pública (`__init__.py` / `public.py`); el resto es privado.
- **Reglas de dependencia verificables**: Introducir linter de imports (`import-linter` o `ruff` + `conftest` de verificación) que prohíbe dependencias circulares y el acceso directo cross-módulo a modelos. Contratos permitidos: `presentation → application → domain` dentro del módulo; cross-módulo solo vía `application.facade` o eventos.
- **Desacople por eventos de dominio en-proceso**: Bus síncrono `app/shared/events.py` (publish/subscribe en memoria) + `DomainEvent` tipados (`AlumnoRegistrado`, `UsuarioCreado`, `AvatarActualizado`). `registro` publica, `auditoria`/`email`/`estadística` suscriben. Elimina imports directos `from app.services.email_service import notificar_nuevo_registro` desde controllers (`app/controllers/registro_controller.py:9`).
- **Capa de acceso a datos por repositorio**: Interfaces `AlumnoRepository`, `VisitaRepository` en `domain`, implementaciones SQLAlchemy en `infrastructure`. Transacciones gestionadas por `application/unit_of_work.py`. Los controllers dejan de hacer `Alumno.query.filter_by` directo.
- **Shared Kernel mínimo y explícito**: `app/shared/` (`db`, `time_utils`, `events`, `errors`, `config`) versionado y con regla de no importar dominio. Lo que no está en `shared` no es compartible.
- **Migración incremental y compatible**: Mantiene `app/__init__.py:create_app()` y `DATABASE_URL`/`migrations/` intactos. Los blueprints existentes se reubican sin cambiar URLs ni esquema. Feature-flag por módulo para rollback.

No se convierte a microservicios, no se cambia de framework ni de BD.

## Capabilities

### New Capabilities
- `modular-boundaries`: Estructura de módulos, capas por módulo, reglas de importación y linter de fronteras. Define qué puede importar qué, cómo se expone la API pública de cada módulo y cómo se verifica automáticamente.
- `domain-events`: Bus de eventos de dominio en-proceso, catálogo de eventos, contratos de publicación/suscripción y garantías de entrega/atómica con la transacción.

### Modified Capabilities
- _Ninguna existente (openspec/specs vacío)_ — el cambio es aditivo sobre comportamiento existente sin alterar requisitos previos.

## Impact

- **Código afectado**: `app/__init__.py:42-49` (registro de blueprints), todos los controllers (`app/controllers/*.py`), modelos (`app/models/*.py`), services (`app/services/*.py`), `app/config.py`, `tests/conftest.py`, `migrations/env.py` (imports). `app/templates/` y `app/static/` no cambian de ruta lógica (solo referencias).
- **APIs**: URLs públicas sin cambio (compatibilidad). Nuevas APIs internas: `app/modules/*/public.py` (facades) y `app/shared/events.py`.
- **Dependencias**: Añade `import-linter` (o `pytest-import-linter`) como dev-dependency; sin nuevos servicios infra.
- **Sistemas**: Build/test (`pytest`), CI (nuevo check `lint:boundaries`), deploy cPanel/Passenger sin cambio. Riesgo principal: imports rotos durante la migración incremental — mitigado con fase strangler por módulo.
