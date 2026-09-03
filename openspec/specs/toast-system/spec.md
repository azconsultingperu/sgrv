# toast-system Specification

## Purpose
Centraliza el comportamiento del sistema de toasts/notificaciones internas (dashboard, registrar, consultar, usuarios, auditoría, reportes) para feedback consistente sin tapar contenido crítico ni depender de interacción manual.

## Requirements

### Requirement: Auto-cierre sin botón manual

El sistema de toasts internos SHALL cerrar cada toast por auto-cierre a los 6000ms y SHALL renderizar un botón de cerrar manual (X) como ícono suelto sin caja, fondo ni borde; un click en la X SHALL cerrar el toast de inmediato sin esperar los 6s, mientras que sin click el auto-cierre a los 6000ms SHALL seguir funcionando.

#### Scenario: Auto-cierre a los 6s
- **WHEN** se muestra un toast interno con `mostrarToast(tipo, titulo, mensaje)` y el usuario no hace click
- **THEN** el toast permanece visible 6000ms y luego se remueve con animación de salida.

#### Scenario: Botón X suelto en el DOM
- **WHEN** se inspecciona el DOM de un toast interno visible
- **THEN** existe un elemento con clase `mc-toast-cerrar` (botón con `aria-label` de cerrar) sin caja/fondo/borde visible, solo el ícono X.

#### Scenario: Click en X cierra inmediato
- **WHEN** el usuario hace click sobre el botón X del toast
- **THEN** el toast se cierra de inmediato con animación de salida y su `setTimeout` de 6s se cancela.

#### Scenario: Click en cuerpo no cierra
- **WHEN** el usuario hace click sobre el cuerpo del toast (fuera de la X)
- **THEN** el toast no se cierra y sigue su temporizador de 6s hasta auto-cierre.

### Requirement: Alineación vertical del ícono

El toast interno SHALL alinear verticalmente el ícono de alerta al centro respecto al bloque de texto (título + mensaje) usando flexbox con `align-items: center` en el contenedor principal del toast.

#### Scenario: Ícono centrado
- **WHEN** se renderiza un toast con título y descripción de 1-2 líneas
- **THEN** el triángulo de alerta queda centrado verticalmente respecto a la altura total del bloque de texto, no pegado al borde superior.

#### Scenario: Consistencia entre temas
- **WHEN** se cambia entre modo claro y modo oscuro
- **THEN** la alineación vertical del ícono se mantiene centrada en ambos temas.

### Requirement: Sin indicador de progreso

El toast interno SHALL NOT mostrar barra/línea indicadora de tiempo restante. El elemento `mc-toast-progreso` SHALL no existir en el DOM y su animación CSS SHALL ser removida, manteniendo el auto-cierre de 6s sin feedback visual de progreso.

#### Scenario: Sin barra en el DOM
- **WHEN** se muestra cualquier toast interno
- **THEN** no existe elemento con clase `mc-toast-progreso` dentro de `.mc-toast`.

#### Scenario: Auto-cierre silencioso
- **WHEN** un toast es visible
- **THEN** se cierra a los 6000ms sin animación de barra y sin requerir `animation` de progreso.

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
