## Purpose

Catálogo de instituciones educativas secundarias visitables por el IESTP Paiján, ampliado a las 10 I.E. de la imagen de dirección, con datos normalizados para que el formulario registre el colegio correcto sin texto libre.

## ADDED Requirements

### Requirement: Catálogo ampliado a 16 instituciones

El sistema SHALL tener al menos 16 filas activas en `instituciones_educativas` (`activo=true`), incluyendo las 6 existentes más las 10 nuevas de la imagen, cada una con `nombre`, `codigo_modular` (cuando aplique), `distrito`, `provincia`, `region` y `tipo`.

#### Scenario: Conteo tras migración
- **WHEN** se ejecuta `flask db upgrade` en una BD con los 6 seed previos
- **THEN** `SELECT COUNT(*) FROM instituciones_educativas WHERE activo=true` es 16 y `SELECT codigo_modular` incluye `80055`, `80085`, `80057`, `80850`, `80878`, `80053`, `80050`

#### Scenario: Datos normalizados para Licapa y La Arenita
- **WHEN** se consulta `Alfonso Ugarte - Licapa` y `José Olaya Balandra - La Arenita`
- **THEN** `distrito` es `Paiján` o el que indique ESCALE y `provincia` es `Ascope`, `region` es `La Libertad`

#### Scenario: Seed idempotente
- **WHEN** se recrea la BD con `seed_data()`
- **THEN** las 16 I.E. existen y una segunda ejecución de seed no duplica filas (mismo `codigo_modular` o `nombre+distrito` no se repite)

### Requirement: Distrito y provincia investigados por cada I.E.

Cada nueva I.E. SHALL tener `distrito` y `provincia` verificados contra MINEDU ESCALE/Identicole (padrón 2026) antes de insertar; si el padrón no resuelve, SHALL usar la ubigeo oficial de La Libertad y documentar la fuente en la migración/seed.

#### Scenario: Fuente documentada
- **WHEN** se revisa `migrations/*_add_nuevas_instituciones.py` y `app/utils/seed.py`
- **THEN** cada `INSERT` incluye comentario con URL o nota de fuente (ESCALE/Identicole) y `provincia` no queda vacía ni `NULL`

#### Scenario: Consulta por código modular
- **WHEN** se busca por `codigo_modular = 80055`
- **THEN** se retorna `Juan Ignacio Gutiérrez Fuente` con `distrito` y `provincia` no vacíos
