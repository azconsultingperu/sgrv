## Why

El formulario de registro solo ofrece 6 instituciones (seed inicial), pero la promoción del IESTP Paiján visita colegios adicionales listados por dirección (ver imagen 2026-09-15). Sin ellos los promotores deben registrar el colegio como "Otros" o texto libre, perdiendo trazabilidad. Se necesita ampliar el catálogo a los 10 institutos de la imagen, con distrito/provincia correctos para que el autocompletado de `provincia` (fix previo) funcione.

## What Changes

- Añadir **10 instituciones educativas** al catálogo, extraídas de la imagen `WhatsApp Image 2026-09-15 at 3.07.57 PM.jpeg`:
  - I.E. 80055 Juan Ignacio Gutiérrez Fuente
  - I.E. José Andrés Rázuri – Pto. Chicama
  - I.E. 80085 Miguel Grau Seminario – Macabí Alto
  - I.E. Nuestra Señora de Lourdes
  - I.E. 80850 San Salvador
  - I.E. 80057 Inmaculada Concepción
  - I.E. Leoncio Prado
  - I.E. 80878 Alfonso Ugarte – Licapa
  - I.E. 80053 José Olaya Balandra – La Arenita
  - I.E. 80050 José Félix Black
- Para cada una, **investigar distrito y provincia** (MINEDU ESCALE / Identicole `identicole.minedu.gob.pe`, padrón, código modular) y fijar `region = La Libertad`, `tipo = "Público"` (o según padrón), `activo = true`.
- Implementar vía **migración Alembic + seed**: migración `insert` de las 10 filas (con `codigo_modular` cuando exista), y actualización de `app/utils/seed.py` para que instalaciones nuevas las incluyan. Usar `INSERT ... ON CONFLICT(codigo_modular) DO NOTHING` o `INSERT IGNORE` para idempotencia.
- El formulario `registro/index.html` y `editar.html` mostrará automáticamente las nuevas opciones (ya renderiza `colegios = InstitucionEducativa.query.filter_by(activo=True)`), sin cambio de template salvo verificar que `data-provincia` se expone.
- **BREAKING**: No hay — solo datos adicionales.

## Capabilities

### New Capabilities
- `instituciones-catalogo`: Catálogo ampliado de I.E. visitables con datos normalizados (nombre, código modular, distrito, provincia, región).

### Modified Capabilities
- `registro-form`: El `<select id="institucion_id">` SHALL listar las 16 I.E. (6 existentes + 10 nuevas) y el autocompletado de distrito/provincia SHALL funcionar para las nuevas.

## Impact

- **BD**: `instituciones_educativas` — 10 filas nuevas; migración `migrations/versions/*_add_nuevas_instituciones.py`.
- **Código**: `app/utils/seed.py` (añadir a lista `colegios`), `app/modules/registro/domain/institucion_educativa.py` si se requiere índice, `migrations/`.
- **Templates**: sin cambios lógicos (ya iteran `colegios`), solo verificación de `data-provincia`.
- **Tests**: `tests/test_registro.py` y `test_consulta.py` siguen pasando; se puede añadir test que verifica count >=16 y que `GET /registro/` contiene una de las nuevas con `data-provincia`.
- **Dependencias**: consulta a MINEDU/ESCALE para distrito/provincia (fuente externa, no código).
