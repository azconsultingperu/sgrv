## Purpose

Añade una señal visual rápida al listado de consulta (`consulta/index.html`) mostrando el avatar del alumno en la tabla para identificar registros a golpe de vista, manteniendo el rendimiento y la privacidad del serving de fotos.

## ADDED Requirements

### Requirement: Columna thumb 32px en tabla de consulta

El sistema SHALL añadir como primera columna de `consulta/index.html` (antes de DNI) un thumb circular 32px (`avatar-sm` con `width 32px height 32px border-radius 50% object-fit cover`) que muestre la foto del alumno si `tiene_foto()` es True vía `foto_url(thumb=True)` (`/registro/foto/<id>?t=1`), o iniciales con color hash si no tiene foto. La columna SHALL tener header vacío o con icono `image` y `width` fija ~48px para no desplazar el resto. En `tbody` el thumb SHALL estar centrado en `td`. Si la tabla está vacía (empty-state), no se muestra thumb.

#### Scenario: Alumno con foto muestra thumb
- **WHEN** se carga `/consulta/` y hay un alumno con `foto="3_abc.webp"`
- **THEN** en su fila la primera celda contiene `<img src="/registro/foto/3?t=1" class="avatar-sm">` circular 32px

#### Scenario: Alumno sin foto muestra iniciales
- **WHEN** se lista alumno sin foto
- **THEN** la primera celda contiene `<span class="avatar-sm d-inline-grid place-items-center">JL</span>` con fondo `var(--surface-2)` y color hash

#### Scenario: Header no rompe layout
- **WHEN** se inspecciona el `<thead>` tras el cambio
- **THEN** tiene 9 columnas (foto + 8 existentes) y la tabla no hace overflow horizontal en desktop 1024px

### Requirement: Serving rápido y privado del thumb

El thumb SHALL servirse vía la misma ruta privada `GET /registro/foto/<id>?t=1` con `@login_required`, retornando el archivo `*_min.webp` 90px con `image/webp` y `Cache-Control private, max-age=0, must-revalidate`. Si no existe thumb pero existe full, SHALL hacer fallback al full. El listado SHALL NOT hacer N+1 queries: la carga de alumnos ya trae `foto` en la query principal sin join extra.

#### Scenario: Thumb requiere login
- **WHEN** sin sesión se pide `/registro/foto/1?t=1`
- **THEN** redirige a login y no expone thumb

#### Scenario: Sin thumb hace fallback a full
- **WHEN** existe `1_abc.webp` pero no `1_abc_min.webp`
- **THEN** `/registro/foto/1?t=1` retorna el full webp sin 404

### Requirement: Responsive y accesibilidad del thumb

En móvil el thumb SHALL mantenerse 32px y la tabla SHALL seguir en `table-responsive` con scroll horizontal; el thumb SHALL tener `alt="Foto de {{ alumno.nombres }} {{ alumno.apellidos }}"` y `loading="lazy"` para no bloquear render. El color de iniciales SHALL tener contraste ≥ 4.5:1 sobre `var(--surface-2)` reutilizando la paleta `AVATAR_COLORS` de usuario.

#### Scenario: Móvil mantiene tamaño
- **WHEN** se abre `/consulta/` en 375px
- **THEN** los thumbs siguen 32px y la tabla hace scroll horizontal sin romper círculos

#### Scenario: Thumb tiene alt y lazy
- **WHEN** se inspecciona un thumb en listado
- **THEN** tiene `alt` con nombre del alumno y `loading="lazy"`
