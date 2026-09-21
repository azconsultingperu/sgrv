## Purpose

Garantiza que en teléfonos (viewport <=991px) toda acción del sistema se alcanza con scroll normal de página, sin botones tapados por el navegador ni columnas de acciones fuera de pantalla.

## Requirements

### Requirement: Scroll de página en móvil

En viewports `<=991px` el desplazamiento vertical SHALL pertenecer al `body` (scroll de página nativo), no a un contenedor interno, de modo que el navegador móvil esconda su barra inferior al scrollear y el final de cada página (botones Guardar/Actualizar/Volver) quede visible y tocable.

#### Scenario: Botón final alcanzable en registro
- **WHEN** un usuario con rol 1 abre `/registro/` en 360×640 y scrollea hasta el fondo
- **THEN** el botón Guardar Registro es visible y recibe el tap (sin quedar bajo la barra del navegador)

#### Scenario: Barra del navegador se esconde
- **WHEN** se scrollea hacia abajo cualquier página interna en móvil
- **THEN** el navegador esconde su barra inferior (comportamiento nativo de scroll de body)

#### Scenario: Desktop intacto
- **WHEN** se usa viewport `>991px`
- **THEN** el layout con sidebar fija y panel con scroll propio se comporta igual que antes

### Requirement: Zona segura inferior

El contenido móvil SHALL reservar al pie `padding-bottom` con el área segura del dispositivo, de modo que ningún botón quede bajo la barra de gestos de Android/iOS.

#### Scenario: Sin solape con gestos
- **WHEN** se llega al final de un formulario en un teléfono con navegación por gestos
- **THEN** entre el último botón y el borde inferior hay espacio libre equivalente al área segura

### Requirement: Acciones de tabla visibles en móvil

En `<=767px` cada fila de las tablas de gestión (consulta, usuarios, reportes, auditoría) SHALL exponer sus acciones (Ver/Editar/Eliminar según rol) sin exigir swipe horizontal no indicado: sea con columna de acciones fija visible, sea con tarjetas.

#### Scenario: Acciones sin swipe adivinable
- **WHEN** se abre `/usuarios/` en 360×640
- **THEN** cada fila muestra al menos un acceso visible a sus acciones sin scrollear horizontalmente

#### Scenario: Permisos por rol se mantienen
- **WHEN** un Operador abre las mismas tablas
- **THEN** ve solo las acciones que su rol autoriza (igual que en desktop)

### Requirement: Drawer cerrable en móvil

El menú lateral en `<=991px` SHALL poder cerrarse por botón ✕ visible, tecla Escape y toque en el fondo, además del comportamiento actual (cerrar al elegir opción).

#### Scenario: Cierre por ✕ y Escape
- **WHEN** el drawer está abierto en móvil
- **THEN** existe un botón ✕ visible que lo cierra, y pulsar Escape también lo cierra

#### Scenario: Sticky preservados
- **WHEN** se scrollea con el nuevo esquema en móvil
- **THEN** la navbar superior y la barra de progreso de registro siguen fijas y visibles como antes
