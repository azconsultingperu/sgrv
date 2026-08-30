## 1. Completar módulo notifications al layout oficial

- [x] 1.1 Crear `app/modules/notifications/domain/__init__.py`, `infrastructure/__init__.py`, `presentation/__init__.py` y `public.py` (fachada mínima) y verificar que `ls app/modules/notifications/{domain,infrastructure,presentation}/` existe y `public.py` importa sin error
- [x] 1.2 Crear `app/modules/notifications/infrastructure/email_adapter.py` moviendo lógica SMTP de `app/services/email_service.py` (sin cambiar comportamiento) y verificar que `notifications/application/event_handlers.py` importa el adapter y no `app.services` directo
- [x] 1.3 Añadir contratos `importlinter` para `notifications` en `setup.cfg` si faltan y verificar `venv/bin/lint-imports` pasa

## 2. Migrar calls directos a publish() (domain-events)

- [x] 2.1 Reemplazar `from app.services.auditoria_service import registrar_auditoria` en `app/modules/identidad/presentation/perfil_controller.py` por `publish(AvatarActualizado/AvatarEliminado)` vía `app/shared/events.py` y verificar que `grep -r "registrar_auditoria" app/modules/identidad/presentation/perfil_controller.py` no encuentra import directo y `pytest tests/test_boundaries.py -k publish` pasa
- [x] 2.2 Verificar que `app/modules/registro/presentation/registro_controller.py` ya usa `crear_alumno_con_visita` + `UoW publish(AlumnoRegistrado)` y no importa `auditoria_service`/`email_service` directo, y que `grep -r "app.services" app/modules/registro/` vacío
- [x] 2.3 Asegurar bootstrap en `app/__init__.py:52` suscribe `notifications` handlers (`_register_notif`) y verificar que `create_app()` registra 3 módulos (identidad, auditoria, notifications) y `bus.publish(AlumnoRegistrado)` dispara ambos handlers sin error

## 3. Eliminar shims legacy manteniendo compatibilidad

- [x] 3.1 Reemplazar todos `from app.models.*` y `from app.controllers.*` y `from app.services.*` restantes en `app/` y `tests/` por imports desde `app/modules/*/domain` o `public.py`/`shared` y verificar `grep -r "from app\.models\|from app\.controllers\|from app\.services" app/ tests/ --include="*.py" | grep -v ".pyc" | grep -v "__pycache__"` vacío salvo shims
- [x] 3.2 Borrar `app/controllers/*.py` y `app/models/*.py` (excepto `reporte.py`/`dashboard_estadistica.py` si aún no migrados — moverlos a `reportes/domain` o `shared` antes) y verificar `ls app/controllers app/models` no existe o solo contiene `__init__.py` y `pytest tests/` pasa con 200 en `/registro/`, `/consulta/`, `/dashboard/`, `/usuarios/`
- [x] 3.3 Convertir `app/services/auditoria_service.py` y `email_service.py` en shims re-export o eliminarlos tras 3.1, y verificar `venv/bin/lint-imports` y `FLASK_ENV=testing venv/bin/python -m pytest tests/ -v` verdes

## 4. Documentar excepción registro→identidad y cierre

- [x] 4.1 Añadir comentario en `app/modules/registro/public.py:47` explicando `from app.modules.identidad.public import count_usuarios` como excepción `public→public` controlada y verificar que `setup.cfg` permite `public→public` y `lint-imports` pasa
- [x] 4.2 Ejecutar validación integral `make lint-boundaries && FLASK_ENV=testing venv/bin/python -m pytest tests/test_boundaries.py tests/test_registro.py tests/test_consulta.py -v` y verificar todo verde y sin `from app.services` residual
