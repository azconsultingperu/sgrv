## 1. Modelo y migración

- [x] 1.1 Añadir `Visita.operador_promotor_id` (FK nullable → `usuarios.id`) + helper `promotor_nombre` que resuelve Operador / Promotor clásico / None, y verificar con `python -c "from app.modules.registro.domain.visita import Visita; print(hasattr(Visita,'operador_promotor_id'))"`.
- [x] 1.2 Crear migración Alembic (upgrade añade columna nullable + FK, downgrade la retira) y verificar con `alembic upgrade head && alembic downgrade -1 && alembic upgrade head` en SQLite local sin errores.

## 2. Fuente unión en registro

- [x] 2.1 En `registro_controller.registrar` y `editar` (GET + re-render tras error) consultar operadores activos (`rol_id=3, estado=True, eliminado=False`, ordenados) y pasarlos al template junto a `promotores`, y verificar abriendo `GET /registro/` como admin que el contexto incluye ambas listas.
- [x] 2.2 Renderizar `#promotor_id` en `registro/index.html` y `editar.html` como unión con valores prefijados (`promotor:<id>` / `operador:<id>`), `data-origen` por opción y placeholder `Seleccionar promotor...` primero, y verificar que el HTML contiene `data-origen="operador"` y el nombre del Operador seed.
- [x] 2.3 Parsear el prefijo en `POST /registro/` y `POST /registro/editar/<id>` (vacío → ambos NULL; `operador:<id>` → `operador_promotor_id`; `promotor:<id>` → `promotor_id`; rechazar ambos a la vez) con `promotor_id` clásico intacto, y verificar creando una visita con cada variante vía tests.

## 3. Persistencia y visualización

- [x] 3.1 Extender el comparador `|string` de `selected` y el rehidratado tras error para valores con prefijo Operador en `index.html` y `editar.html`, y verificar enviando `POST /registro/` con Operador + DNI inválido → re-render 200 mantiene ese Operador como `selected`.
- [x] 3.2 Usar el helper de resolución en consulta/detalle, `reporte_service.py` (CSV/Excel) y `email/nuevo_registro.html` para que muestren el nombre del Operador y sigan mostrando clásico o "No asignado" en los demás casos, y verificar abriendo detalle/reporte/email de una visita con Operador, una clásica y una NULL sin `AttributeError`.

## 4. Verificación integral

- [x] 4.1 Añadir tests de regresión (Operador aparece en `GET /registro/`; nuevo Operador vía `POST /usuarios/crear` aparece sin pasos extra; visita con Operador se guarda y se muestra; inactivo/eliminado desaparece; clásicas/NULL intactas) y verificar con `pytest tests/ -q` en verde.
- [x] 4.2 Verificación E2E manual como admin (lista unión en registro y editar, crear Operador → aparece, guardar visita con Operador → detalle/reporte correctos) y verificar cada scenario de `specs/registro-form/spec.md` marcado.
