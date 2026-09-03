## MODIFIED Requirements

### Requirement: Contraste en modo claro

El toast interno SHALL tener fondo sólido del color de estado (error=rojo, éxito=verde, advertencia=ámbar, info=azul) usando la paleta existente de `--danger-color`, `--success-color`, `--warning-color`, `--info-color`, con texto (título + mensaje), ícono y botón X en blanco/casi blanco para contraste, y SHALL verse idéntico en modo claro y en modo oscuro sin depender del tema.

#### Scenario: Fondo sólido por tipo
- **WHEN** se muestra un toast de tipo `error`, `success`, `warning` o `info`
- **THEN** su fondo es sólido del color de estado correspondiente (rojo/verde/ámbar/azul) y no el fondo neutro `var(--surface-1)` anterior.

#### Scenario: Texto e ícono en blanco
- **WHEN** el toast tiene fondo sólido de color
- **THEN** el título, la descripción y el ícono (triángulo/circle-check/info) se renderizan en blanco (`#ffffff` o `rgba(255,255,255,0.92)`) con contraste suficiente sobre el fondo.

#### Scenario: Botón X en blanco
- **WHEN** el toast muestra el botón X suelto sin caja
- **THEN** la X es blanca, sin fondo ni borde, visible sobre el fondo sólido y clickeable para cierre inmediato.

#### Scenario: Hover con borde blanco sobre fondo sólido
- **WHEN** el mouse pasa sobre un toast con fondo sólido
- **THEN** aparece un borde sólido blanco de 1.2px sin blur con transición suave, igual que antes pero sobre el nuevo fondo de color.

#### Scenario: Independiente del tema
- **WHEN** se alterna entre modo claro (`data-bs-theme="light"`) y modo oscuro (`data-bs-theme="dark"`) con un toast visible
- **THEN** el toast mantiene el mismo fondo sólido, texto e ícono blancos y sombra, sin variación por tema; la lógica condicional de sombra reforzada solo para light ya no es necesaria y puede simplificarse/eliminarse.

#### Scenario: Todos los tipos
- **WHEN** se disparan toasts de los 4 tipos en el mismo tema
- **THEN** cada uno usa su color sólido correspondiente y todos son claramente distinguibles del fondo de la página (no mimetizados).
