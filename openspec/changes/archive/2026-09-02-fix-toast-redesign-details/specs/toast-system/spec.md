## Purpose

Centraliza el comportamiento del sistema de toasts/notificaciones internas (dashboard, registrar, consultar, usuarios, auditoría, reportes) para feedback consistente sin tapar contenido crítico ni depender de interacción manual.

## ADDED Requirements

### Requirement: Auto-cierre sin botón manual

El sistema de toasts internos SHALL cerrar cada toast únicamente por auto-cierre a los 6000ms y SHALL NOT renderizar ningún botón de cerrar manual (X). No SHALL existir elemento clickeable que descarte el toast antes de los 6s.

#### Scenario: Auto-cierre a los 6s
- **WHEN** se muestra un toast interno con `mostrarToast(tipo, titulo, mensaje)`
- **THEN** el toast permanece visible 6000ms y luego se remueve con animación de salida sin requerir interacción.

#### Scenario: Sin botón X en el DOM
- **WHEN** se inspecciona el DOM de un toast interno visible
- **THEN** no existe ningún elemento con clase `mc-toast-cerrar` ni botón con `aria-label` de cerrar.

#### Scenario: Click en toast no lo cierra
- **WHEN** el usuario hace click sobre el cuerpo del toast
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

En modo claro (tema blanco, `data-bs-theme="light"`), el toast interno SHALL distinguirse del fondo de la página mediante fondo ligeramente diferenciado y sombra más pronunciada, manteniendo el borde izquierdo de color de estado (rojo/verde/etc.) como diferenciador principal pero sin depender exclusivamente de él.

#### Scenario: Fondo y sombra en modo claro
- **WHEN** el tema es claro y se muestra un toast
- **THEN** el toast tiene fondo distinto al blanco puro de la página (ej. superficie elevada) y `box-shadow` más marcado que en modo oscuro, perceptible como elemento flotante.

#### Scenario: No regresión en modo oscuro
- **WHEN** el tema es oscuro
- **THEN** el toast mantiene legibilidad y contraste actuales sin cambio de fondo que lo degrade.

#### Scenario: Login no afectado
- **WHEN** se muestra un toast en páginas de auth (login, recuperar contraseña con `.login-card`)
- **THEN** mantiene su posición superior derecha y estilo previo, sin aplicar el fondo/sombra de toasts internos ni el cambio de posición inferior.
