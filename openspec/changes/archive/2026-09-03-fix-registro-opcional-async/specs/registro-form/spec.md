## ADDED Requirements

### Requirement: Marcado visual de campos requeridos y opcionales

El formulario `registro/index.html` y `registro/editar.html` SHALL distinguir visualmente campos requeridos de opcionales: cada label de campo requerido SHALL llevar `<span class="text-danger">*</span>` rojo junto al texto, cada label de campo opcional SHALL llevar `<small class="text-muted">(opcional)</small>` gris. Encima del form SHALL aparecer leyenda `<p class="text-muted small"><span class="text-danger">*</span> Campos obligatorios</p>`. Requeridos: apellidos, nombres, dni, fecha_nacimiento, sexo, celular, institucion_id. Opcionales: email, direccion, carrera_id, area_interes, modalidad_contacto, desea_estudiar, solicita_info, fecha_visita, hora_visita, promotor_id, observaciones, foto. El `required` HTML SHALL mantenerse en requeridos para accesibilidad.

#### Scenario: Requeridos con asterisco
- **WHEN** se abre `registro/index.html`
- **THEN** los labels de apellidos, nombres, dni, fecha_nacimiento, sexo, celular, institucion muestran `*` rojo

#### Scenario: Opcionales con etiqueta
- **WHEN** se abre el mismo form
- **THEN** los labels de email, direccion, carrera, area, modalidad, observaciones muestran `(opcional)` gris

#### Scenario: Leyenda visible
- **WHEN** se renderiza el form
- **THEN** existe texto `* Campos obligatorios` arriba del primer `h5`

### Requirement: Validación de sexo requerido

El backend `POST /registro/` SHALL validar que `sexo` sea uno de `M`, `F`, `O`; si falta o es otro valor, SHALL añadir error a `errores` ("Debe seleccionar sexo.") y el template SHALL marcar el `<select name="sexo">` con `is-invalid` y mostrar `invalid-feedback`. El frontend SHALL también marcar el `custom-select` correspondiente si existe.

#### Scenario: Sexo vacío bloquea
- **WHEN** se envía `POST /registro/` sin `sexo`
- **THEN** la respuesta es `200` re-render con `errores` incluyendo "Debe seleccionar sexo" y el select tiene `is-invalid`

#### Scenario: Sexo válido pasa
- **WHEN** se envía con `sexo=M`
- **THEN** no se añade error por sexo

### Requirement: Spinner y protección doble submit en Guardar

El botón `Guardar Registro` (`type="submit"`) en `registro/index.html` y `Actualizar` en `editar.html` SHALL deshabilitarse al hacer submit, cambiar su contenido a `<span class="spinner-border spinner-border-sm" role="status"></span> Guardando...` y prevenir doble submit. Si la validación HTML5 falla (`form.checkValidity() === false`), el botón SHALL rehabilitarse inmediatamente.

#### Scenario: Submit deshabilita botón
- **WHEN** el usuario hace click en Guardar con form válido
- **THEN** el botón queda `disabled` y muestra spinner

#### Scenario: Validación falla rehabilita
- **WHEN** el form tiene un campo `required` vacío y se hace click en Guardar
- **THEN** el submit se cancela por `checkValidity` y el botón vuelve a `enabled` sin spinner

#### Scenario: No doble POST
- **WHEN** el usuario hace doble click rápido en Guardar con form válido
- **THEN** solo se envía un `POST /registro/` (el segundo click es ignorado por `disabled`)
