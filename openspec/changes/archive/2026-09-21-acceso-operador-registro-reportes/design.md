## Context

Ver `proposal.md` (Why) y `specs/acceso-operador/spec.md` (requisitos). Estado actual verificado en código:

- `registro_controller.py:19-26` define un guard **local** `admin_or_supervisor_required` (`rol_id not in (1, 2)`) aplicado a `registrar` (:114) y `editar` (:239). No usa el de `app/utils/decorators.py`.
- `reportes_controller.py:30` define su propio `supervisor_required` local, aplicado a sus 10 rutas. El `supervisor_required` compartido de `app/utils/decorators.py` no lo usa ningún controller (solo `admin_required` se importa, en usuarios y auditoría).
- `sidebar.html:23` oculta "Registrar" con `{% if current_user.rol_id <= 2 %}`; `sidebar.html:37` muestra "Reportes" con `{% if rol_id <= 2 or rol_id == 4 %}`.
- Auditoría ya guarda `actor_id` en altas/ediciones, así que lo creado por operadores queda trazado sin cambios.

## Goals / Non-Goals

**Goals:**
- Operador (rol 3) registra, edita y ve reportes con el mismo comportamiento que Supervisor.
- Cero cambios de comportamiento para roles 1, 2 y 4.

**Non-Goals:**
- Unificar los guards duplicados (locales vs `app/utils/decorators.py`) — se documenta, no se toca.
- Activar el sistema `has_permission`/`permiso_requerido` (stub que solo deja pasar a admin) — fuera de alcance.
- El caso "Consultas ve Reportes en menú pero rebota" queda como está (decisión pendiente separada).

## Decisions

### 1. Extender los guards locales, no los compartidos
Cambiar la tupla `(1, 2)` → `(1, 2, 3)` solo en los dos guards locales (`registro_controller.admin_or_supervisor_required`, `reportes_controller.supervisor_required`). Alternativa descartada: tocar `app/utils/decorators.py` — innecesario porque ningún controller afectado lo importa, y evita blast radius sobre futuros usos compartidos.

### 2. Condiciones de sidebar por membresía explícita
`rol_id <= 2` → `rol_id in (1, 2, 3)` en el bloque Registrar; agregar `or rol_id == 3` en el bloque Reportes. Se prefiere membresía explícita sobre `<= 3` para que un futuro rol 5+ no herede acceso por accidente (el bug original nació de un `<=` que excluía al 3 sin que nadie lo notara).

### 3. Sin migración ni modelo nuevo
No hay cambio de esquema: `rol_id` ya existe, la auditoría ya traza actor. El despliegue es solo archivos (mismo procedimiento que el change anterior: 3 archivos por File Manager + `tmp/restart.txt`, FTP sigue con cuota llena).

### 4. Verificación por rol con cliente de pruebas
Cada ruta afectada se prueba con los 4 roles (operador pasa, consultas rebota donde debe, supervisor/admin intactos) antes de subir, más smoke en producción con cuenta operadora real.

## Risks / Trade-offs

- [Riesgo] Guard local duplicado: futuros cambios de permisos deben repetirse en 3 lugares (registro, reportes, decorators) → Mitigación: queda documentado aquí; unificar es un change futuro.
- [Riesgo] Operador ve todos los alumnos en Consultar (no solo los suyos) → Aceptado por decisión de usuario (evita duplicados en campo).
- [Riesgo] `has_permission` stub sigue existiendo y confunde → Mitigación: no se usa en ningún controller; no tocarlo en este change.

## Migration Plan

Sin migración de BD. Despliegue: subir `registro_controller.py`, `reportes_controller.py` y `sidebar.html` por cPanel File Manager (FTP bloqueado por cuota), tocar `tmp/restart.txt`, verificar con cuenta operadora en producción. Rollback: revertir los 3 archivos (git) y resubir.
