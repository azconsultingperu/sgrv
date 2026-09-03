# registro-form Specification

## Purpose
Mejorar la jerarquía visual, la guía de placeholders y la consistencia de checkboxes del formulario de registro/edición de visitas sin afectar validación ni envío.

## Requirements

### Requirement: Jerarquía visual entre secciones

El formulario SHALL mostrar headers de sección numerados (`01` con badge) + `border-bottom` separador y una barra de progreso fina (`height:3px`, `position:sticky`) que se llena con scroll, manteniendo las 5 secciones existentes sin convertir en wizard.

#### Scenario: Headers numerados y separador
- **WHEN** se renderiza `registro/index.html` o `editar.html`
- **THEN** cada `h5` de sección muestra número con badge y `border-bottom:1px solid var(--border-color)` con `padding-bottom`.

#### Scenario: Barra de progreso por scroll
- **WHEN** el usuario hace scroll dentro del formulario
- **THEN** una barra fina bajo el navbar se llena proporcionalmente al % de scroll del formulario.

### Requirement: Placeholders en campos sin guía

Los 8 campos identificados SHALL tener `placeholder` descriptivo en ambos templates (`index` y `editar`) para consistencia.

#### Scenario: Campos con placeholder en index
- **WHEN** se abre `registro/index.html` sin datos
- **THEN** `apellidos` muestra "Ej. García López", `nombres` "Ej. Juan Carlos", `dni` "Ej. 12345678", `celular` "Ej. 987654321", `email` "Ej. juan@ejemplo.com", `direccion` "Ej. Jr. Lima 123, Paiján", `area_interes` "Ej. Ingeniería de Sistemas", `observaciones` "Ej. Interesado en beca, visita con padres...".

#### Scenario: Consistencia en editar
- **WHEN** se abre `registro/editar.html`
- **THEN** los mismos 8 campos muestran los mismos placeholders cuando están vacíos.

### Requirement: Inputmode numérico

Los campos `dni` y `celular` SHALL tener `inputmode="numeric"` (y `pattern` ya existente) para mostrar teclado numérico en móvil.

#### Scenario: Teclado numérico en móvil
- **WHEN** el usuario hace focus en `dni` o `celular` en dispositivo móvil
- **THEN** el teclado mostrado es numérico.

### Requirement: Custom checkbox cuadrado

Los 6 checkboxes del sistema (registro/index 2, registro/editar 2, usuarios/editar 1, login "Recordar" 1) SHALL usar estilo custom cuadrado `appearance:none` de 18px con borde 1.2px, check blanco y focus con halo `primary-soft`, manteniendo `name`/`value`/`checked` originales.

#### Scenario: Checkbox custom visible
- **WHEN** se renderiza cualquier `form-check-input` de los 6 identificados
- **THEN** se ve cuadrado de 18px con borde `var(--border-color)` y al estar `checked` muestra fondo `var(--primary-color)` con check blanco y `focus` con `box-shadow:0 0 0 3px rgba(var(--bs-primary-rgb),0.16)`.

#### Scenario: Envío preservado
- **WHEN** se envía el formulario con un checkbox marcado
- **THEN** el backend recibe `name=on` (o valor correspondiente) igual que con el nativo; si no está marcado, no se envía.

### Requirement: Validación preservada

Cualquier cambio de placeholder, inputmode o estilo de checkbox SHALL preservar el comportamiento de `is-invalid` y `invalid-feedback` existente.

#### Scenario: Validación no rota
- **WHEN** un campo `required` con placeholder está vacío y se intenta enviar
- **THEN** se añade `is-invalid` y se muestra `invalid-feedback` debajo, igual que antes.

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
