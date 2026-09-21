## Purpose

Define qué puede y qué no puede hacer el rol Operador (rol 3, promotores de campo) en el sistema: registrar y editar alumnos, consultar todos los registros, ver reportes y usar dashboard y perfil propio, manteniendo el resto de módulos restringidos.

## ADDED Requirements

### Requirement: Operador registra alumnos

Un usuario con rol Operador SHALL poder abrir el formulario de registro (`/registro/`) y crear alumnos con las mismas validaciones y comportamiento que un Supervisor (incluye foto, select de Promotor Responsable, fecha DD/MM/AAAA y toasts de éxito/error).

#### Scenario: Formulario visible para operador
- **WHEN** un Operador autenticado abre `/registro/` por GET
- **THEN** ve el formulario completo y el enlace "Registrar" en el menú lateral

#### Scenario: Alta exitosa por operador
- **WHEN** un Operador envía un POST válido a `/registro/`
- **THEN** el alumno y su visita quedan creados y la auditoría registra su `actor_id`

#### Scenario: Validación igual que supervisor
- **WHEN** un Operador envía un POST inválido (DNI duplicado, fecha mala, campos vacíos)
- **THEN** recibe los mismos mensajes y rehidratación de formulario que un Supervisor

### Requirement: Operador edita registros

Un usuario con rol Operador SHALL poder abrir `/registro/editar/<id>` y actualizar datos del alumno y su visita, con las mismas validaciones que un Supervisor.

#### Scenario: Edición exitosa por operador
- **WHEN** un Operador envía un POST válido a `/registro/editar/<id>`
- **THEN** los cambios quedan guardados y la auditoría registra su `actor_id`

### Requirement: Operador ve reportes

Un usuario con rol Operador SHALL poder abrir el módulo Reportes, ver el índice y generar/descargar los reportes disponibles, igual que un Supervisor.

#### Scenario: Acceso a reportes por operador
- **WHEN** un Operador autenticado abre `/reportes/` o cualquiera de sus rutas de generación/descarga
- **THEN** accede sin mensaje de permisos y ve el enlace "Reportes" en el menú lateral

### Requirement: Prohibiciones del operador intactas

El Operador SHALL seguir sin acceso a Eliminar registros, Gestión de Usuarios y Auditoría: cualquier intento directo por URL SHALL redirigirlo al dashboard con el mensaje "No tiene permisos...".

#### Scenario: Eliminar sigue bloqueado
- **WHEN** un Operador hace POST a `/registro/eliminar/<id>`
- **THEN** es redirigido al dashboard con flash de error y el registro queda intacto

#### Scenario: Usuarios y auditoría siguen bloqueados
- **WHEN** un Operador abre `/usuarios/` o `/auditoria/`
- **THEN** es redirigido al dashboard con flash de error

#### Scenario: Menú no muestra módulos prohibidos
- **WHEN** un Operador ve el menú lateral
- **THEN** no aparecen los enlaces "Usuarios" ni "Auditoría"

### Requirement: Otros roles sin cambios

Los permisos de Administrador (todo), Supervisor (todo menos usuarios/auditoría/eliminar) y Consultas (solo lectura: dashboard, consultar, reportes según guard actual) SHALL permanecer idénticos.

#### Scenario: Supervisor conserva su acceso
- **WHEN** un Supervisor usa registro, edición o reportes
- **THEN** todo funciona igual que antes del cambio
