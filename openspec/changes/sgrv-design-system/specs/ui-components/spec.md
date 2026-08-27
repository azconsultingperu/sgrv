## Purpose

Provee componentes reutilizables y reglas de interacción de SGRV para que tablas, filtros, formularios, modales y notificaciones mantengan la misma experiencia en todos los módulos y tamaños.

## ADDED Requirements

### Requirement: Botones y estados interactivos
Todo botón SHALL respetar `min-height` 44px base / 36px `sm` / 48px `lg` en móvil, con estados `hover` (`translateY(-1px)` + shadow), `active` (0), `disabled` (0.58) y `focus-visible` (outline 2px + shadow). Un botón icon-only SHALL ser ≥44×44px en <768px. Un botón `danger` SHALL exigir `data-confirm`.

#### Scenario: Botón icon-only en móvil
- **WHEN** se renderiza `consulta/index.html` en 360px con `btn-group-sm` de acciones
- **THEN** cada `a.btn` y `button.btn` mide ≥44px de alto y ancho y el `focus-visible` muestra outline de 2px

#### Scenario: Botón peligro exige confirmación
- **WHEN** un futuro módulo añade `<button class="btn-danger">Eliminar</button>` sin `data-confirm`
- **THEN** la revisión lo rechaza por regla de componente

### Requirement: Tablas transformadas en cards en móvil
Toda tabla con `data-responsive="cards"` SHALL renderizarse como `table` en ≥768px y como lista de cards apiladas en <768px, sin duplicar markup. El `thead` SHALL ocultarse en móvil y cada `td` SHALL mostrar su `data-label` como encabezado de card.

#### Scenario: Consulta en móvil muestra cards
- **WHEN** se abre `consulta/index.html` en 360px con 3 alumnos
- **THEN** no hay scroll horizontal, se ven 3 cards con DNI/Apellidos/Nombres/Edad/Sexo/Colegio y acciones de 44px, y el `thead` no es visible

#### Scenario: Tabla sin atributo no cambia
- **WHEN** una tabla sin `data-responsive` se ve en móvil
- **THEN** сохраняет comportamiento `table-responsive` legacy con scroll horizontal

### Requirement: Filter drawer / bottom sheet en móvil
En <768px los filtros de `consulta` y `auditoria` SHALL colapsar a un botón `Filtros (n)` + `Buscar`. Al pulsar SHALL abrir un drawer bottom sheet con todos los campos y acciones `Aplicar`/`Cancelar`/`Limpiar`, con `position: fixed`, `max-height: 80dvh`, scroll interno y backdrop.

#### Scenario: Filtros colapsados en móvil
- **WHEN** se abre `consulta/index.html` en 360px
- **THEN** solo se ven 1 input de búsqueda y un botón `Filtros` con contador, y el formulario completo solo aparece dentro del drawer

#### Scenario: Aplicar cierra y preserva estado
- **WHEN** se seleccionan filtros dentro del drawer y se pulsa `Aplicar`
- **THEN** el drawer se cierra con animación y la URL contiene los `search_params` y `pagination` se reinicia a 1

### Requirement: Form sections como acordeones en móvil
Formularios con ≥3 secciones (`h5.section-title`) SHALL mostrar todas las secciones expandidas en desktop y como acordeón en <768px con solo la primera abierta por defecto, animación `height` y `aria-expanded` correcto.

#### Scenario: Registro en móvil es acordeón
- **WHEN** se abre `registro/index.html` en 360px
- **THEN** se ven 5 `h5` como acordeones, solo Datos Personales expandido, y al pulsar Contacto se expande con `aria-expanded="true"` sin perder datos ya ingresados

#### Scenario: Validación preserva acordeón
- **WHEN** el submit falla por DNI inválido en una sección colapsada
- **THEN** esa sección se expande automáticamente y el foco va al primer campo inválido

### Requirement: Confirmaciones como bottom sheet en móvil
El motor `data-confirm` SHALL mostrar modal centrado `430px` en desktop y bottom sheet (`bottom:0`, `border-radius 16px 16px 0 0`, handle, swipe-down) en <768px, con haptic `navigator.vibrate(10)` en danger.

#### Scenario: Eliminar en móvil muestra sheet
- **WHEN** se pulsa `Eliminar` en `usuarios/index.html` en 360px
- **THEN** aparece sheet desde abajo con título, mensaje y botones `Cancelar`/`Sí, eliminar`, y un swipe-down lo cierra sin ejecutar

### Requirement: Toast-island móvil dirección B
En `body.es-movil` las notificaciones SHALL aparecer como isla superior centrada (`top: calc(env(safe-area-inset-top,0) + 12px)`, `left:50%`, `translateX(-50%)`, `width: min(92vw,400px)`), con entrada `translateY(-20px) scale(.96) → 0/1` 0.32s `cubic-bezier(.16,1,.3,1)`, salida `translateY + opacity` 0.22s, pausa por `touchstart`, cierre por swipe horizontal con velocity, y respeta `prefers-reduced-motion`.

#### Scenario: Éxito en móvil muestra isla
- **WHEN** se dispara `mostrarToast('success','Éxito','Registro creado')` en 360px con `es-movil`
- **THEN** la isla aparece arriba centrada, no tapa el navbar, y un swipe horizontal la descarta con `mcIslandOut`

#### Scenario: Sidebar no tapa isla
- **WHEN** el sidebar está abierto (`body.sidebar-open`) y llega un toast
- **THEN** la isla queda con `z-index` menor que el sidebar o se reubica a `top:70px` sin quedar debajo del backdrop

### Requirement: Estados globales únicos
Vacío SHALL usar `empty-state` (icono + título + texto + CTA), carga SHALL usar skeleton `pulse` de 3 líneas, error SHALL usar `alert-danger` + botón Reintentar, éxito SHALL usar solo `toast-island` nunca `alert-success` inline. Un módulo SHALL no inventar un empty propio.

#### Scenario: Consulta sin datos muestra empty-state correcto
- **WHEN** `consulta` no tiene alumnos y no hay filtros
- **THEN** se ve `empty-state` con `No hay registros` + botón `Registrar la primera visita` si `rol_id <=2`, y nunca un `table` vacío

#### Scenario: Carga muestra skeleton
- **WHEN** un chart o tabla está cargando
- **THEN** se ven 3 `skeleton` pulsantes en lugar de `no-data-overlay` blanco

### Requirement: Touch targets mínimos
Todo elemento interactivo SHALL medir ≥44×44px en <768px (`pagination .page-link`, `btn-group-sm`, `navbar avatar`, `nav-link`). Un validador SHALL fallar si un `a.btn` mide 34px en 360px.

#### Scenario: Paginación en móvil
- **WHEN** se renderiza `partials/paginacion.html` en 360px
- **THEN** cada `page-link` mide ≥44px y el `…` es clicable con `min-width` 44px
