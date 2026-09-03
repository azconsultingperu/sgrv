## 1. Modelo y migración de índice parcial

- [x] 1.1 Reemplazar `unique=True` en `Usuario.dni`/`username`/`email` por `Index` único parcial `WHERE eliminado = false` (PG/SQLite) manteniendo compatibilidad MySQL, y verificar con `grep -n "Index.*eliminado" app/modules/identidad/domain/usuario.py` y `venv/bin/python -c "from app.modules.identidad.domain.usuario import Usuario; print([i.name for i in Usuario.__table__.indexes])"`.
- [x] 1.2 Generar migración Alembic `flask --app run.py db migrate -m "partial unique index for active usuarios"` y editarla para `drop` de `UNIQUE` previo + `create_unique_index` con `postgresql_where`/`sqlite_where`, con branch para MySQL que omite `WHERE`; verificar `flask --app run.py db upgrade` y `flask --app run.py db downgrade` en dev sin perder datos y `make lint-boundaries` pasa.

## 2. Lógica de creación / reactivación

- [x] 2.1 Modificar `POST /usuarios/crear` en `app/modules/identidad/presentation/usuarios_controller.py` para filtrar `eliminado=False` en checks de `dni`/`username`/`email` y, si existe `eliminado=True` con el DNI, reactivar esa fila (`eliminado=False`, `estado=True`, update de `nombres`/`apellidos`/`email`/`rol_id`, `set_password`, `intentos_fallidos=0`, `bloqueado_hasta=None`), sin `db.session.add()` nuevo; verificar con `POST` manual que `Usuario.query.filter_by(dni='71184654').count()==1` y `check_password` ok.
- [x] 2.2 Insertar auditoría `Usuario reactivado` en `modulo=Usuarios` con `ip`/`user_agent` y `detalle` con DNI, en el mismo `commit` que la reactivación, sin duplicar `UsuarioCreado`; verificar en `auditorias` que tras reactivar existe `accion='Usuario reactivado'`.

## 3. Verificación en tiempo real

- [x] 3.1 Actualizar `GET /usuarios/verificar-dni` para usar `filter_by(dni=dni, eliminado=False)` y verificar con `curl`/`pytest` que `?dni=71184654` con solo eliminado retorna `{"existe": false}` y con activo retorna `true`.

## 4. Tests y regresión

- [x] 4.1 Añadir `tests/test_usuario_reactivacion.py` que cubra: crear sobre DNI eliminado reactiva (no duplica, actualiza campos y resetea bloqueo), crear sobre DNI activo bloquea, `verificar-dni` filtra, índice parcial impide dos activos con mismo DNI, y auditoría `Usuario reactivado` se registra; verificar `FLASK_ENV=testing venv/bin/python -m pytest tests/test_usuario_reactivacion.py -v` y `venv/bin/python -m pytest tests/test_usuarios.py -v` sin regresión.
