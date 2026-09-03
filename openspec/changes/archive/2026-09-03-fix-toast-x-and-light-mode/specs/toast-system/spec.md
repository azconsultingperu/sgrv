## MODIFIED Requirements

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
