## Context

Seed actual: 6 I.E. en `app/utils/seed.py` y en migración inicial, todas en Ascope/La Libertad. Template `registro/index.html` ya itera `colegios = InstitucionEducativa.query.filter_by(activo=True)` y expone `data-provincia` tras el fix previo. Ver `proposal.md` Why y lista de 10 códigos/nombres extraídos de la imagen. Fuente de verdad para distrito/provincia: MINEDU ESCALE/Identicole padrón 2026 (consulta por `codigo_modular`).

## Goals / Non-Goals

**Goals:**
- Insertar 10 I.E. con distrito/provincia verificados y exponerlas en el formulario sin cambiar lógica de autocompletado.
- Migración idempotente y seed consistente para nuevas instalaciones.

**Non-Goals:**
- Geocodificación lat/long en esta iteración (se deja `NULL` si no está en padrón).
- Endpoint de búsqueda de colegios (fuera de alcance).

## Decisions

**Decisión 1: Migración + seed, no solo seed**
- Migración Alembic `INSERT` para BDs existentes (prod) + actualización de `seed.py` para instalaciones nuevas. *Por qué*: `INIT_DB_ON_START=False` en prod, solo migraciones aplican. *Alternativa solo-seed* descartada por dejar prod desactualizado.

**Decisión 2: Búsqueda de distrito/provincia via ESCALE/Identicole por código modular**
- Para cada código (80055, 80085, etc.) consultar `identicole.minedu.gob.pe/colegio/<codigo>` o ESCALE. Si no hay código (ej. "Leoncio Prado"), buscar por nombre+UGEL Ascope. *Por qué*: fuente oficial, evita asumir distrito. *Alternativa LLM asumido* descartada: riesgo de provincia errónea. Registrar fuente en comentario de migración.

**Decisión 3: Idempotencia con `codigo_modular` único**
- Usar `codigo_modular` como clave natural cuando existe; para los sin código, usar `nombre+distrito` con `ON CONFLICT DO NOTHING` (Postgres) / `INSERT OR IGNORE` (SQLite) o check en seed con `query.filter_by(codigo_modular=...).first()`. *Por qué*: permite re-ejecutar migración/seed sin duplicar.

**Decisión 4: Mantener `activo=true`, `region=La Libertad`, `tipo` según padrón (mayoría "Pública")**
- No inferir tipo privado. *Por qué*: coherente con 6 existentes (tipo "Público").

## Risks / Trade-offs

- **Padrón sin distrito para "Licapa"/"La Arenita" (anexos)** → Mitigación: Licapa es centro poblado de Paiján, La Arenita de Paiján; si ESCALE lo lista como anexo, usar distrito Paiján, provincia Ascope, documentar. Si duda, dejar `distrito=Paiján` con nota.
- **Nombre duplicado con existente** → Mitigación: verificar `SELECT nombre FROM instituciones_educativas` antes de insertar; si colisiona, reutilizar existente.
- **Migración en MySQL prod (cPanel)** → Mitigación: usar `INSERT` estándar sin `ON CONFLICT` específico de Postgres; Alembic con `op.bulk_insert` que es portable, o `INSERT ...` con check previo en Python.

## Migration Plan

1. Crear migración `xxx_add_nuevas_instituciones.py` con `op.bulk_insert` de 10 filas.
2. Actualizar `app/utils/seed.py` lista `colegios_data` con mismas 10.
3. `flask db upgrade` local y verificar `GET /registro/` lista 16.
4. Tests: añadir `assert InstitucionEducativa.query.count() >=16` en `test_registro.py` (opcional).
5. Rollback: `flask db downgrade` elimina las 10 por `codigo_modular`.
