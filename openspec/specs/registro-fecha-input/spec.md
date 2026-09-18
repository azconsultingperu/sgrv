# registro-fecha-input Specification

## Purpose

Componente de entrada de fecha para el módulo registro que reemplaza el popup nativo de `type="date"` por una experiencia híbrida: escritura rápida con máscara DD/MM/AAAA y calendario ligero opcional, manteniendo envío YYYY-MM-DD al backend.

## Requirements

### Requirement: Entrada de fecha sin popup nativo obligatorio

El sistema SHALL proveer un componente de fecha que no dependa del popup nativo de `type="date"` como única forma de ingreso. SHALL permitir escribir directamente `DD/MM/AAAA` con máscara, con `inputmode="numeric"` y placeholder `DD/MM/AAAA`, y SHALL enviar al backend `YYYY-MM-DD` (vía conversión JS o campo hidden).

#### Scenario: Escritura directa con máscara
- **WHEN** el usuario enfoca `fecha_nacimiento` y teclea `15032008`
- **THEN** el input muestra `15/03/2008` con `/` insertados automáticamente y al hacer submit el valor enviado es `2008-03-15`

#### Scenario: Pegado con formato
- **WHEN** el usuario pega `15-03-2008` o `15/03/2008`
- **THEN** el componente normaliza a `15/03/2008` y valida correctamente

#### Scenario: Sin popup nativo impuesto
- **WHEN** el usuario hace click en el campo
- **THEN** no se abre obligatoriamente el calendario del SO; el calendario solo abre al presionar el botón calendario

### Requirement: Calendario ligero opcional

El componente SHALL ofrecer un botón con ícono Lucide `calendar` junto al input que abre un calendario ligero (overlay) solo a demanda. SHALL permitir navegación rápida por mes/año y selección con click/teclado, y SHALL respetar `min`/`max` si se definen (ej. nacimiento no futuro).

#### Scenario: Apertura a demanda
- **WHEN** el usuario hace click en el botón calendario de `fecha_nacimiento`
- **THEN** se abre un overlay con calendario del mes y puede cerrarse con Esc o click fuera, sin afectar el valor hasta seleccionar

#### Scenario: Navegación rápida por año
- **WHEN** el calendario está abierto y el usuario usa selector de año o flechas
- **THEN** puede saltar de 2026 a 2008 en ≤2 interacciones (sin scrollear año por año)

#### Scenario: Selección actualiza input
- **WHEN** el usuario selecciona `15 Mar 2008` en el calendario
- **THEN** el input muestra `15/03/2008` y dispara `change` para que `calcularEdad` actualice `edad`

### Requirement: Validación y accesibilidad

El componente SHALL validar formato `DD/MM/AAAA`, fechas reales (incluido 29/02 bisiesto), y rango (fecha_nacimiento no futura, no menor a 1900-01-01). SHALL marcar `is-invalid` y mostrar `invalid-feedback` con mensaje, SHALL ser accesible por teclado (Tab, Enter, Esc, flechas en calendario) y SHALL tener `aria-label` en botón y `role="dialog"` en overlay.

#### Scenario: Fecha inválida muestra error
- **WHEN** el usuario escribe `31/02/2008` y hace blur o submit
- **THEN** el input recibe `is-invalid` y se muestra "Fecha inválida"

#### Scenario: Teclado completo
- **WHEN** el usuario navega con Tab hasta el input, escribe `15/03/2008` y presiona Enter
- **THEN** el valor se acepta sin necesidad de mouse ni calendario

### Requirement: Compatibilidad con comportamiento existente

El componente SHALL preservar: cálculo de `edad` vía `change`/`blur`, auto-llenado de `fecha_visita` con `fecha_actual`, rehidratación tras error de validación (`form.fecha_nacimiento` muestra `15/03/2008` si vino `2008-03-15`), y `required`/`is-invalid` existentes.

#### Scenario: Edad se calcula igual
- **WHEN** el componente emite `change` con `15/03/2008`
- **THEN** `fetch /registro/calcular-edad?fecha_nacimiento=2008-03-15` se ejecuta y `#edad` se actualiza

#### Scenario: Rehidratación tras error
- **WHEN** `POST /registro/` falla y el template re-renderiza con `form.fecha_nacimiento="2008-03-15"`
- **THEN** el input muestra `15/03/2008` sin requerir interacción adicional

### Requirement: Degradación y no regresión

Si JS está deshabilitado, el componente SHALL degradar a `type="text"` con placeholder `DD/MM/AAAA` y validación server-side SHALL aceptar tanto `DD/MM/AAAA` como `YYYY-MM-DD`. El backend SHALL normalizar a `YYYY-MM-DD` antes de validar.

#### Scenario: Sin JS
- **WHEN** JS está deshabilitado y el usuario envía `15/03/2008`
- **THEN** el backend lo convierte a `2008-03-15` y el registro se crea correctamente
