## 1. Investigación — distrito y provincia por código

- [x] 1.1 Consultar ESCALE/Identicole para cada código modular (80055, 80085, 80850, 80057, 80878, 80053, 80050) y para los 3 sin código (José Andrés Rázuri Pto. Chicama, Nuestra Señora de Lourdes, Leoncio Prado) por nombre+UGEL Ascope — documentar fuente y distrito/provincia hallados en tabla dentro de `design.md` o comentario de migración
- [x] 1.2 Definir lista final de 10 tuplas `(nombre, codigo_modular, distrito, provincia, region, tipo)` con `provincia=Ascope` y `region=La Libertad` salvo hallazgo distinto — verificar que ninguna colisione con las 6 existentes (`SELECT nombre FROM instituciones_educativas`)

## 2. Migración y seed

- [x] 2.1 Crear migración Alembic `migrations/versions/xxxx_add_nuevas_instituciones.py` con `op.bulk_insert` de las 10 filas (idempotente, con `codigo_modular` único) — verificar `flask db upgrade` inserta 10 y `flask db downgrade` las remueve
- [x] 2.2 Actualizar `app/utils/seed.py` para incluir las mismas 10 en `colegios_data` con misma data y lógica `if not exists` — verificar `seed_data()` en instalación limpia crea 16

## 3. Verificación en formulario

- [x] 3.1 Verificar `GET /registro/` y `GET /registro/editar/<id>` renderizan 16 `<option data-provincia>` e incluyen una nueva (ej. `Alfonso Ugarte - Licapa` con `data-distrito="Paiján"`) — verificar autocompletado de provincia funciona al seleccionar
- [x] 3.2 Ejecutar `FLASK_ENV=testing pytest tests/test_registro.py tests/test_boundaries.py -q` — verificar sin regresión y conteo esperado
