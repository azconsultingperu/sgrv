# custom-select Specification

## Purpose
Reemplaza visualmente los 15 `select` nativos del sistema por un desplegable custom coherente con el design system, manteniendo compatibilidad total con formularios, validación y filtros.

## Requirements

### Requirement: Reemplazo visual con desplegable custom

El sistema SHALL reemplazar visualmente cada `select.form-select` (15 en `registro`, `usuarios`, `auditoria`, `consulta`) por un componente hand-made que oculta el `<select>` nativo pero lo mantiene en el DOM, renderizando un botón con apariencia `form-select` y un `ul.dropdown-menu` con `li a.dropdown-item` por cada `option`, usando los mismos tokens de `border`, `radius`, `shadow` y `hover` del dropdown de navbar.

#### Scenario: Render inicial
- **WHEN** la página carga y `custom-select.js` inicializa `querySelectorAll('select.form-select')`
- **THEN** cada `select` queda `display:none` y a su lado aparece un botón que muestra el texto del `option` seleccionado y un `ul` oculto con un ítem por cada `option`.

#### Scenario: Apertura y selección
- **WHEN** el usuario hace click en el botón del custom-select
- **THEN** se muestra el `ul.dropdown-menu` con las opciones estilizadas; al elegir una, el `ul` se cierra y el botón muestra el nuevo texto.

### Requirement: Puente de validación

El estado `is-invalid` del `<select>` nativo SHALL propagarse al botón visible del custom-select, mostrando `border-color: var(--danger-color)` y el `invalid-feedback` existente, y SHALL limpiarse igual que en `auth-validation.js` para inputs.

#### Scenario: Select requerido vacío con error
- **WHEN** un `select` con `required` está vacío y la validación le añade `is-invalid` y un `.invalid-feedback`
- **THEN** el botón visible del custom-select muestra borde rojo y el mensaje de error debajo, idéntico al comportamiento de inputs.

#### Scenario: Corrección limpia el error
- **WHEN** el usuario elige una opción válida en el custom-select
- **THEN** se remueve `is-invalid` tanto del `<select>` oculto como del botón visible y se oculta el `invalid-feedback`.

### Requirement: Propagación de evento change

Al elegir una opción en el custom-select, el sistema SHALL actualizar `select.value` al `value` del `option` elegido y SHALL disparar `select.dispatchEvent(new Event('change', {bubbles:true}))` (y `input` si aplica) para que listeners existentes sigan funcionando.

#### Scenario: Autollenado de distrito
- **WHEN** en `registro/index.html` el usuario cambia `institucion_id` en el custom-select
- **THEN** el listener `select[name="institucion_id"].addEventListener('change', ...)` que hace `document.getElementById('distrito').value = selected.text.split(' - ')[1]` se ejecuta y el campo distrito se autocompleta.

#### Scenario: Filtros no se rompen
- **WHEN** se usa el custom-select en un cambio de valor
- **THEN** cualquier otro listener `change` registrado sobre el `<select>` nativo se dispara sin necesidad de re-registrarlo en el custom.

### Requirement: Envío de formulario y filtros GET

Los `<select>` de filtros en `auditoria/index.html` y `consulta/index.html` SHALL seguir enviando `name`/`value` correctos por `GET` al hacer submit, porque el `<select>` oculto conserva `name` y `value` sincronizados.

#### Scenario: Filtro de auditoría
- **WHEN** el usuario elige `usuario_id` y `modulo` en el custom-select de auditoría y hace submit del form `GET`
- **THEN** la URL generada contiene `?usuario_id=<id>&modulo=<valor>` igual que con el select nativo y el backend filtra correctamente.

#### Scenario: Filtro de consulta
- **WHEN** el usuario elige `sexo` y `carrera_id` en consulta y hace submit
- **THEN** los parámetros `sexo` y `carrera_id` se envían por `GET` sin cambios.

### Requirement: Selected inicial desde Jinja

Al inicializarse, el custom-select SHALL leer `select.options[select.selectedIndex]` (el `selected` renderizado por `{% if ... %}selected{% endif %}` en `registro/editar.html` y `usuarios/editar.html`) y SHALL mostrar ese `text` en el botón; si no hay `selected` (placeholder con `value=""`), muestra el texto del placeholder. También SHALL respetar `form.reset()` restaurando el botón al valor inicial.

#### Scenario: Edición con valor precargado
- **WHEN** se abre `registro/editar.html` con `institucion_id` ya seleccionado desde Jinja
- **THEN** el botón del custom-select muestra desde el inicio el nombre de esa institución (no el placeholder), y el `ul` marca ese ítem como activo.

#### Scenario: Reset de formulario
- **WHEN** se ejecuta `form.reset()`
- **THEN** el custom-select vuelve a mostrar el texto del `option` que quedó `selected` tras el reset y sincroniza `select.value`.

### Requirement: Accesibilidad y teclado

El botón del custom-select SHALL ser navegable por teclado (focus, `Enter`/`Space` abre, `ArrowUp`/`ArrowDown` navega, `Enter` selecciona, `Escape` cierra) y SHALL tener `aria-haspopup="listbox"` y `aria-expanded`.

#### Scenario: Navegación por teclado
- **WHEN** el botón tiene foco y el usuario presiona `ArrowDown`
- **THEN** el desplegable se abre y el primer ítem queda enfocado; `Enter` selecciona y cierra.
