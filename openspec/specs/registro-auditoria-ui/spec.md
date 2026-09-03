# registro-auditoria-ui Specification

## Purpose
Corrige tres fricciones de UI en registro y consultar sin afectar validación real ni envío de formularios.

## Requirements

### Requirement: Panel no reaparece al validar

Al validar el formulario de registro con campos faltantes (ocultando previamente el panel con la hamburguesa), el panel lateral SHALL permanecer oculto y no reaparecer por el scroll/validación.

#### Scenario: Validación con panel oculto
- **WHEN** el usuario oculta el panel (hamburguesa) y hace submit con campos vacíos en `registro/index.html`
- **THEN** el panel sigue oculto (`sidebar` sin `show`, `body` sin `sidebar-open`) mientras se muestra el scroll al primer campo inválido.

### Requirement: Sin bordes rojos genéricos en validación

Al fallar validación por campos vacíos en `registro`, el sistema SHALL NOT añadir `is-invalid` ni `input-glow` (bordes rojos) de forma genérica; solo muestra `invalid-feedback` y toast, reservando `is-invalid` para validaciones con lógica custom (ej. DNI duplicado).

#### Scenario: Campos vacíos sin borde rojo
- **WHEN** se hace submit con varios `required` vacíos
- **THEN** no aparece `border-color: var(--danger-color)` ni `box-shadow` rojo en los inputs; solo se ve el mensaje debajo y el toast.

#### Scenario: DNI duplicado sí marca
- **WHEN** el `fetch` de `consulta.verificar_dni` detecta DNI existente
- **THEN** sí se añade `is-invalid` y `dniFeedback` con borde rojo en ese campo.

### Requirement: Filtro de carrera con ancho suficiente

El filtro `carrera_id` en `consulta/index.html` SHALL mostrar nombres completos sin corte por ancho corto del select.

#### Scenario: Carrera desplegada sin corte
- **WHEN** se abre el desplegable de carrera en consultar (con `custom-select`)
- **THEN** cada `carrera.nombre` se ve completo (sin `[:20]`) con `min-width:240px` y `max-width:320px` en el menú, sin ser recortado por `col-md-2`.

### Requirement: Consistencia de filtros y selects

Los selects de filtros SHALL seguir enviando `name`/`value` correctos por `GET` y respetar `selected` inicial.

#### Scenario: Filtro GET intacto
- **WHEN** se elige carrera y se hace submit en consultar
- **THEN** la URL contiene `?carrera_id=<id>` y el backend filtra igual.
