## ADDED Requirements

### Requirement: Select de institución lista las nuevas I.E.

El `<select id="institucion_id">` en `registro/index.html` y `registro/editar.html` SHALL listar las 16 I.E. activas (6 + 10 nuevas) ordenadas por nombre, cada `<option>` con `value=c.id`, texto `c.nombre - c.distrito` y atributos `data-distrito`, `data-provincia`, `data-region`, y el autocompletado de `provincia` SHALL funcionar para las nuevas.

#### Scenario: Listado en registro
- **WHEN** un usuario autenticado abre `GET /registro/`
- **THEN** el HTML contiene al menos 16 `<option value="` dentro de `#institucion_id` y contiene `data-provincia="Ascope"` para una de las nuevas con `80055`

#### Scenario: Autocompletado para nueva I.E.
- **WHEN** el usuario selecciona `Alfonso Ugarte - Licapa` (80878)
- **THEN** `#provincia` muestra la provincia de Licapa y `#distrito` su distrito sin recargar

#### Scenario: Editar también lista
- **WHEN** se abre `GET /registro/editar/<id>` de un alumno existente
- **THEN** el select también contiene las 10 nuevas opciones
