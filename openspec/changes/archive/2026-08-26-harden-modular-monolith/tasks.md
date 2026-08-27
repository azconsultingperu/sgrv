## 1. Infraestructura transversal y guard de fronteras

- [x] 1.1 Crear `app/shared/events.py` con `Event`, `EventBus` (publish/subscribe síncrono, orden determinístico, aislado de errores) y verify con `pytest` que `publish` sin suscriptor no falla y con suscriptor entrega en orden
- [x] 1.2 Crear `app/shared/db.py` re-exportando `db` de `app/__init__.py:10` y `app/shared/errors.py` / `app/shared/time_utils.py` wrapper, y verify que `from app.shared.db import db` funciona y `peru_now` sigue importable
- [x] 1.3 Implementar `app/shared/unit_of_work.py` (context manager con `commit/rollback` y drenaje de `events`) y verify con test que `rollback` descarta eventos y `commit` los despacha
- [x] 1.4 Añadir `import-linter` a `requirements.txt` (dev) y crear `.importlinter` / `setup.cfg` con contratos `layers` y `forbidden` en modo `warn`, y verify que `lint-imports` / `pytest -m import_linter` corre en local sin romper build
- [x] 1.5 Integrar `lint:boundaries` en CI (GitHub Actions o script `make`) y verify que un import ilegal de prueba hace fallar el job

## 2. Módulo `identidad` (usuarios / roles / auth / sesión / perfil) — strangler fase 1

- [x] 2.1 Crear `app/modules/identidad/{domain,application,infrastructure,presentation}/` y mover `app/models/usuario.py:17`, `rol.py`, `sesion.py` a `domain/` (sin cambiar esquema) y verify que `pytest tests/test_auth.py` sigue verde con shim `app/models/usuario.py` re-export
- [x] 2.2 Crear `app/modules/identidad/infrastructure/usuario_repository.py` (`find_by_dni`, `find_by_id`, `save`) y `app/modules/identidad/public.py` facade (`get_usuario`, `crear_usuario`) y verify con test de repositorio que `find_by_dni("12345678")` retorna admin seed
- [x] 2.3 Mover `app/controllers/auth_controller.py:15`, `usuarios_controller.py:12`, `perfil_controller.py:12` a `presentation/` y re-registrar blueprints en `app/__init__.py:33-49` desde nueva ruta, manteniendo `url_prefix` y verify que `GET /auth/login` y `GET /usuarios/` responden igual y `tests/test_usuarios.py` pasa
- [x] 2.4 Registrar handlers de `identidad` (ej. `AvatarActualizado`) en `application/event_handlers.py:register(bus)` y bootstrap en `create_app()` y verify que `publish(AvatarActualizado)` inserta auditoría sin import directo

## 3. Módulo `registro` + catálogo de eventos — strangler fase 2

- [x] 3.1 Crear `app/modules/registro/{domain,application,infrastructure,presentation}/` y mover `app/models/alumno.py:4`, `visita.py`, `institucion_educativa.py`, `carrera.py`, `promotor.py` a `domain/` y verify que `db.create_all()` no genera migraciones nuevas y `tests/test_registro.py` pasa vía shim
- [x] 3.2 Crear `AlumnoRepository`/`VisitaRepository` interfaces en `domain` e impl SQLAlchemy en `infrastructure/` (filtros `eliminado=False`, `joinedload`) y `unit_of_work` usage en `application/registro_service.py` y verify que `crear_alumno` con `desecha promotor_id=None` persiste (regresión `c7e1a92f4b30`)
- [x] 3.3 Definir eventos `AlumnoRegistrado`, `AlumnoEliminado` en `app/shared/events.py` (o `registro/domain/events.py` re-export) y reemplazar `registrar_auditoria`/`notificar_nuevo_registro` en `registro_controller.py:146-149` por `publish()` dentro de UoW y verify que `POST /registro/` con payload válido publica `AlumnoRegistrado` (spy en `TestingConfig`) y no contiene `from app.services.auditoria_service`
- [x] 3.4 Migrar `app/services/auditoria_service.py:5` y `email_service.py:29` a handlers `app/modules/auditoria/application/event_handlers.py` y `app/modules/notifications/application/event_handlers.py` suscritos a `AlumnoRegistrado`/`UsuarioCreado` y verify que crear alumno genera fila en `auditorias` y (mock) email sin call directo
- [x] 3.5 Activar contratos `forbidden: registro → auditoria` directo e `infrastructure` cross-módulo en `.importlinter` y verify que importar `from app.modules.auditoria.domain import X` desde `registro` falla el linter

## 4. Módulos `consulta`, `dashboard`, `reportes` — consumo vía facade

- [x] 4.1 Mover `app/controllers/consulta_controller.py:12` a `app/modules/consulta/presentation/` y refactorizar para usar `registro.public.buscar_alumnos` / `registro.public.get_alumno` en lugar de `Alumno.query` directo y verify que filtros combinados (`dni`, `colegio`, `distrito`, `fecha_desde/hasta`, `edad`) y paginación siguen pasando `tests/test_consulta.py`
- [x] 4.2 Mover `app/controllers/dashboard_controller.py:5` + `app/services/estadistica_service.py:12` a `app/modules/dashboard/` y hacer que `get_totales`/`get_alumnos_por_colegio` consuman `registro.public` o `alumno_repository` vía DI y verify que dashboard renderiza con datos seed sin `Alumno.query` directo
- [x] 4.3 Mover `app/controllers/reportes_controller.py:7` + `app/services/reporte_service.py:11` a `app/modules/reportes/` y corregir `generar_reporte_excel` para respetar `eliminado=False` y filtros de fecha consistentes con CSV, y verify que `tests/test_reportes.py` CSV/Excel + permisos por rol pasan

## 5. Endurecimiento, compatibilidad y limpieza

- [x] 5.1 Cambiar `.importlinter` de `warn` a `error` bloqueante y añadir `presentation → application → domain` layers para todos los módulos, y verify que `pytest` + `lint-imports` fallan ante violación y pasan sin ella
- [x] 5.2 Eliminar shims legacy `app/controllers/*.py` y re-exports `app/models/*.py`/`app/services/*.py` (tras 1 sprint de coexistencia) y verify que `git grep "from app.controllers"` y `git grep "from app.models.alumno"` retornan 0 y `pytest` sigue verde
- [x] 5.3 Actualizar `STRUCTURE.md` y `README.md` con nuevo layout `app/modules/` + `app/shared/` y guía de contribución ("cómo añadir un módulo") y verify que `README` sección Estructura coincide con árbol real `tree app/modules`
- [x] 5.4 Añadir tests de boundaries (`tests/test_boundaries.py`) que asertan que `import-linter` contracts existen y que `publish`/`rollback` semantics se mantienen, y verify que `pytest tests/test_boundaries.py -v` pasa en `TestingConfig`
