## MODIFIED Requirements

### Requirement: Persistencia de selects y derivados tras error de validación

Cuando `POST /registro/` falla por validación y el controller hace `render_template(..., form=request.form)`, el HTML SHALL repintar los 3 selects (`institucion_id, carrera_id, promotor_id`) con la opción previamente elegida marcada `selected` usando comparación `|string` (`form.xxx|string == c.id|string`), y SHALL re-disparar el JS que rellena `distrito`, `provincia`, `region` y `edad` para que los campos readonly también muestren el valor previo sin requerir nuevo `change`. El `input type=file` de foto SHALL permanecer vacío por seguridad del browser.

#### Scenario: Selects persisten
- **WHEN** el usuario elige `institucion_id=3, carrera_id=2, promotor_id=5` y envía con `dni` inválido
- **THEN** la respuesta `200` re-renderiza el form con los 3 selects mostrando `3,2,5` como `selected` y no "Seleccionar..."

#### Scenario: Derivados se re-hidratan
- **WHEN** la respuesta re-renderiza con `institucion_id=3` y `fecha_nacimiento=2008-01-01`
- **THEN** `distrito`, `provincia`, `region` muestran el distrito/provincia/región de la institución `3` y `edad` muestra la edad calculada sin que el usuario toque el select/fecha

#### Scenario: Foto no persiste
- **WHEN** se re-renderiza tras error con foto previamente seleccionada
- **THEN** el `input file` queda vacío (comportamiento estándar) y el usuario debe re-seleccionar la foto si desea

#### Scenario: Editar también persiste
- **WHEN** `POST /registro/editar/<id>` falla por validación
- **THEN** los mismos 3 selects y derivados se repintan igual que en `index`

#### Scenario: Provincia autocompletada al elegir colegio
- **WHEN** el usuario cambia `institucion_id` a un colegio con `provincia="Ascope"`
- **THEN** los inputs `distrito`, `provincia` y `region` se actualizan inmediatamente a los valores del colegio sin recargar

#### Scenario: Limpieza al deseleccionar
- **WHEN** el usuario vuelve a `Seleccionar institución...`
- **THEN** `distrito`, `provincia` y `region` quedan vacíos (o región vuelve a valor por defecto si aplica)
