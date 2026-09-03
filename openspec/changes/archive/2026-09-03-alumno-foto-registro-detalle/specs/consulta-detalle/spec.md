## Purpose

Rediseña la vista de detalle del alumno (`consulta/detalle.html`) de 4 cards fragmentadas a 2 cards estilo Mi Perfil para dar protagonismo a la foto, agrupar información por secciones y mejorar legibilidad en desktop y móvil sin cambiar datos ni permisos.

## ADDED Requirements

### Requirement: Layout 2 cards estilo perfil para detalle

El sistema SHALL renderizar `GET /consulta/detalle/<id>` con `row g-4` conteniendo `col-md-4` (izquierda) y `col-md-8` (derecha), espejo de `perfil/index.html`. La izquierda SHALL contener foto circular 110px (`#alumnoFotoWrap` con `width 110px height 110px border 2px solid var(--border-color) border-radius 50% overflow hidden`) centrada, nombre completo, DNI badge `bg-info`, carrera e institución resumidas y botones Editar/Volver. La derecha SHALL ser una sola card `border-0 shadow-sm` con `card-body p-4` y tabla `profile-table` subdividida en secciones con `<h6>` separadores: Datos Personales, Contacto, Colegio, Académicos y Visita. En móvil (`<768px`) las columnas SHALL apilarse a `col-12` con foto arriba centrada.

#### Scenario: Desktop muestra 2 columnas
- **WHEN** se abre `/consulta/detalle/1` en viewport ≥ 992px
- **THEN** se ven exactamente 2 cards principales en fila (izquierda foto, derecha datos) y no 4 cards 2x2

#### Scenario: Móvil apila foto arriba
- **WHEN** se abre el mismo detalle en viewport 375px
- **THEN** la foto queda arriba centrada y la tabla debajo a ancho completo sin overflow horizontal

#### Scenario: Foto usa mismo tamaño que perfil
- **WHEN** se inspecciona `#alumnoFotoWrap` en detalle
- **THEN** su `width` y `height` son 110px (±2px) iguales que `#avatarPreviewWrap` en perfil, con `border-radius 50%`

### Requirement: Foto en detalle con fallback a iniciales

El detalle SHALL mostrar la foto del alumno vía `alumno.foto_url()` si `tiene_foto()` es True; si no, SHALL mostrar fallback circular con iniciales (`alumno.nombres[0]+alumno.apellidos[0]`) sobre fondo `var(--surface-2)` y borde igual al wrap, con color de texto derivado de hash del nombre (reusa lógica `avatar_color()`). Si la foto existe pero el archivo falta en disco, la ruta de serving SHALL devolver `avatar-default.svg`.

#### Scenario: Alumno con foto muestra imagen
- **WHEN** `alumno.foto = "7_xyz.webp"` y se abre detalle
- **THEN** el `<img>` tiene `src="/registro/foto/7"` y se ve la foto

#### Scenario: Alumno sin foto muestra iniciales
- **WHEN** `alumno.foto IS NULL` y se abre detalle
- **THEN** se ve círculo con texto "JL" (iniciales) y no un `<img>` roto

#### Scenario: Foto 404 sirve default
- **WHEN** el archivo webp fue borrado manualmente pero `alumno.foto` aún apunta a él
- **THEN** `GET /registro/foto/7` retorna `avatar-default.svg` y el detalle lo muestra sin error

### Requirement: Tabla consolidada por secciones y paridad con datos actuales

La card derecha SHALL contener toda la información que hoy está repartida en 4 cards, sin pérdida: DNI, apellidos, nombres, fecha nacimiento, edad, sexo, celular, email, dirección, institución (nombre, distrito, provincia, región, tipo), carrera, área interés, desea_estudiar, solicita_info, modalidad_contacto, fecha_visita, hora_visita, promotor, observaciones. Cada sección SHALL tener header `text-primary` o `text-muted` con icono Lucide (`contact-2`, `phone`, `school`, `book-open`, `history`) igual a registro. Los valores `NULL` SHALL mostrar "No registrado" / "No especificada" / "Ninguna" como hoy.

#### Scenario: Paridad de datos con 4 cards viejas
- **WHEN** se compara detalle viejo (4 cards) con el nuevo (2 cards) para el mismo alumno
- **THEN** todos los campos visibles antes siguen visibles con el mismo texto y formato (fechas `dd/mm/YYYY`, horas `HH:MM`)

#### Scenario: Secciones con headers visibles
- **WHEN** se inspecciona la tabla consolidada
- **THEN** existen al menos 4 headers de sección (`Datos Personales`, `Contacto`, `Colegio`, `Académicos y Visita`) con icono Lucide

### Requirement: Acciones Editar y Volver preservadas

El detalle SHALL mantener los botones `Editar` (solo si `current_user.rol_id <= 2`) y `Volver` (`url_for('consulta.index')`) en el header `d-flex justify-content-between` igual que hoy, sin agregar nuevas acciones. El botón Editar SHALL seguir apuntando a `registro.editar`.

#### Scenario: Supervisor ve Editar
- **WHEN** un supervisor abre detalle
- **THEN** ve botón Editar amarillo con `pencil`

#### Scenario: Operador no ve Editar
- **WHEN** un operador (rol 3) abre detalle
- **THEN** no ve botón Editar, solo Volver
