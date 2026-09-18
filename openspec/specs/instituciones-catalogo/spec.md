# instituciones-catalogo Specification

## Purpose

Catálogo de instituciones educativas: exactamente las 10 I.E. de la imagen de dirección 2026-09-18, con datos normalizados para que el formulario registre el colegio correcto sin texto libre. Las 6 seed originales salieron del catálogo (desactivadas si tenían historial, eliminadas si no).

## Requirements

### Requirement: Catálogo de 10 instituciones

El sistema SHALL tener exactamente 10 filas activas en `instituciones_educativas` (`activo=true`): las 10 I.E. de la imagen (80055, José Andrés Rázuri, 80085, Lourdes, 80850, 80057, Leoncio Prado, 80878, 80053, 80050), cada una con `nombre`, `codigo_modular` (cuando aplique), `distrito`, `provincia`, `region` y `tipo`. Las 6 seed originales SHALL eliminarse junto con sus alumnos y visitas (dato de prueba autorizado 2026-09-18), y el seed SHALL crear solo las 10.

#### Scenario: Conteo tras migración
- **WHEN** se ejecuta `flask db upgrade` a head
- **THEN** `SELECT COUNT(*) FROM instituciones_educativas WHERE activo=true` es 10 y `SELECT codigo_modular` incluye `80055`, `80085`, `80057`, `80850`, `80878`, `80053`, `80050`

#### Scenario: Sin rastro de las viejas
- **WHEN** se ejecuta `flask db upgrade` a head
- **THEN** ningún `nombre` fuera de las 10 existe en la tabla y ningún alumno referencia una I.E. inexistente

#### Scenario: Datos normalizados para Licapa y La Arenita
- **WHEN** se consulta `Alfonso Ugarte - Licapa` y `José Olaya Balandra - La Arenita`
- **THEN** `distrito` es `Paiján` o el que indique ESCALE y `provincia` es `Ascope`, `region` es `La Libertad`

#### Scenario: Seed idempotente
- **WHEN** se recrea la BD con `seed_data()`
- **THEN** las 10 I.E. existen y una segunda ejecución de seed no duplica filas (mismo `codigo_modular` o `nombre+distrito` no se repite)

### Requirement: Distrito y provincia investigados por cada I.E.

Cada nueva I.E. SHALL tener `distrito` y `provincia` verificados contra MINEDU ESCALE/Identicole (padrón 2026) antes de insertar; si el padrón no resuelve, SHALL usar la ubigeo oficial de La Libertad y documentar la fuente en la migración/seed.

#### Scenario: Fuente documentada
- **WHEN** se revisa `migrations/*_add_nuevas_instituciones.py` y `app/utils/seed.py`
- **THEN** cada `INSERT` incluye comentario con URL o nota de fuente (ESCALE/Identicole) y `provincia` no queda vacía ni `NULL`

#### Scenario: Consulta por código modular
- **WHEN** se busca por `codigo_modular = 80055`
- **THEN** se retorna `Juan Ignacio Gutiérrez Fuente` con `distrito` y `provincia` no vacíos
