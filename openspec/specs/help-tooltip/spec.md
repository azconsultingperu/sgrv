# help-tooltip Specification

## Purpose
Provee ayuda contextual con iconos `?` y tooltips para campos y métricas con reglas no obvias, sin recargar la UI en campos autoexplicativos.

## Requirements

### Requirement: Iconos de ayuda en formulario de registro

El sistema SHALL mostrar icono `?` (`i[data-lucide="circle-help"]`) junto a los labels de `DNI`, `Celular` y `Área Profesional` en `registro/index.html` y `registro/editar.html`, con tooltip que explica la regla oculta.

#### Scenario: Tooltip de DNI
- **WHEN** el usuario hace hover o focus en el `?` junto a `DNI`
- **THEN** se muestra cartelito con texto "8 dígitos sin puntos. Al ingresarlo buscaremos tus datos en RENIEC y se autocompletarán nombres/apellidos."

#### Scenario: Tooltip de Celular
- **WHEN** el usuario hace hover en el `?` junto a `Celular`
- **THEN** se muestra "9 dígitos, empieza con 9. Solo para coordinar la visita."

#### Scenario: Tooltip de Área Profesional
- **WHEN** el usuario hace hover en el `?` junto a `Área Profesional de Interés`
- **THEN** se muestra "Escribe el área que te interesa (ej. Sistemas, Enfermería). No limita tu postulación."

### Requirement: Tooltips en dashboard

El sistema SHALL mostrar `?` junto a 2-3 stat-cards del dashboard (ej. Tasa de Conversión) con tooltip que explica el cálculo.

#### Scenario: Tooltip de métrica
- **WHEN** el usuario hace hover en el `?` junto a `Tasa de Conversión`
- **THEN** se muestra "Interesados / Total Registros en el periodo filtrado."

### Requirement: Comportamiento de tooltip

Cada `?` SHALL usar `data-bs-toggle="tooltip"` con `data-bs-title` y ser inicializado por `bootstrap.Tooltip` ya existente en `main.js`, con trigger `hover focus` para funcionar en desktop y móvil (tap).

#### Scenario: Desktop y móvil
- **WHEN** el usuario hace hover (desktop) o tap/focus (móvil) en el `?`
- **THEN** el tooltip aparece y desaparece al salir o hacer tap fuera, sin requerir librería nueva.

### Requirement: No saturar

El sistema SHALL NOT añadir `?` en filtros de `consulta`/`auditoria`, checkboxes (`Desea estudiar`, `Solicita info`) ni campos donde el `placeholder` ya es suficiente.

#### Scenario: Sin tooltips innecesarios
- **WHEN** se inspecciona `consulta/index.html` o `auditoria/index.html`
- **THEN** no existe ningún `circle-help` con tooltip.
