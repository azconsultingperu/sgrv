# consulta-listado Specification

## Purpose
Añade una señal visual rápida al listado de consulta (`consulta/index.html`) mostrando el avatar del alumno en la tabla para identificar registros a golpe de vista, manteniendo el rendimiento y la privacidad del serving de fotos.

## Requirements

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

### Requirement: Estado de carga al aterrizar desde registro o eliminación

Cuando `consultar/index.html` se carga inmediatamente después de un `POST /registro/` exitoso (flash `success` "Registro creado exitosamente") o `POST /registro/eliminar` (flash "Registro eliminado"), el sistema SHALL mostrar un overlay de carga grande centrado sobre la tabla (`spinner-border` 48px + texto "Cargando estudiantes...") durante 4500ms, luego ocultar el overlay y disparar el toast `mostrarToast` correspondiente. En visitas normales a `consultar` (sin flash de registro/eliminación) SHALL no mostrar el overlay y cargar la tabla inmediatamente.

#### Scenario: Aterrizaje desde registro muestra carga y luego toast
- **WHEN** el usuario completa `POST /registro/` con datos válidos y es redirigido a `GET /consulta/` con flash `success`
- **THEN** durante ~1s se ve el spinner grande sobre la tabla y al terminar aparece un único toast `success` "Registro creado exitosamente" y la tabla ya contiene el nuevo alumno

#### Scenario: Visita normal sin carga
- **WHEN** el usuario entra a `GET /consulta/` directamente o via sidebar sin flash previo de registro/eliminación
- **THEN** la tabla se renderiza inmediatamente sin spinner y sin delay

#### Scenario: Aterrizaje desde eliminación
- **WHEN** el usuario hace `POST /registro/eliminar/<id>` y es redirigido a `/consulta/` con flash de eliminación
- **THEN** se muestra el mismo overlay 4500ms y luego el toast de eliminación, sin mostrar el registro eliminado

#### Scenario: Duración no es 3 segundos
- **WHEN** se mide el tiempo del overlay en el aterrizaje desde registro
- **THEN** la duración es entre 4500ms (no 3000ms) para no frustrar; el spinner es decorativo con función de feedback, no espera real de datos

#### Scenario: No bloquea interacción permanente
- **WHEN** el overlay termina
- **THEN** la tabla queda interactiva y el spinner no vuelve a aparecer al recargar manualmente sin flash
