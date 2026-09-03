## Purpose

Mejorar la jerarquía visual, la guía de placeholders y la consistencia de checkboxes del formulario de registro/edición de visitas sin afectar validación ni envío.

## ADDED Requirements

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
