## Purpose

Evitar spam de notificaciones en el registro de visitas mostrando un solo cartel de error cuando faltan datos, en lugar de uno por cada campo.

## ADDED Requirements

### Requirement: Un solo toast para errores de validación

Cuando `registro_controller.registrar` detecta `errores` no vacío, SHALL hacer un solo `flash` en vez de uno por cada error, para que el frontend genere un solo `mc-toast`.

#### Scenario: Formulario vacío
- **WHEN** se envía `POST /registro/` sin completar ningún campo obligatorio
- **THEN** se genera exactamente 1 mensaje `danger` (ej. "Faltan datos por completar. Revisa los campos marcados.") y el JS muestra 1 toast, no 3.

#### Scenario: Un solo error
- **WHEN** solo el DNI es inválido y el resto es válido
- **THEN** se muestra 1 toast con el mensaje específico de ese error (ej. "El DNI debe tener 8 dígitos.").

#### Scenario: Múltiples errores colapsados
- **WHEN** hay 2 o más errores (ej. DNI + celular)
- **THEN** se muestra 1 toast con mensaje genérico colapsado y el detalle permanece en validación inline de cada campo si existe, sin spam.

### Requirement: Preservar validación específica

El colapso a un solo toast SHALL no ocultar la causa específica cuando hay un solo error; solo colapsa cuando hay varios.

#### Scenario: Error único preservado
- **WHEN** solo falta la institución
- **THEN** el toast dice "Debe seleccionar una institución educativa." (no genérico).
