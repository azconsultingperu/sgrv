## Context

Ver `proposal.md` (Why) para la motivación. Estado actual:

- `GET /registro/` y `GET /registro/editar/<id>` (`app/modules/registro/presentation/registro_controller.py:71-73,194-196`) cargan `promotores = Promotor.query.filter_by(activo=True).all()` y los templates (`registro/index.html:155-159`, `editar.html:121-124`) iteran solo esa lista en `#promotor_id`.
- `Visita.promotor_id` (`app/modules/registro/domain/visita.py:9`) es `FK → promotores.id, nullable=True`; `Visita.usuario_id` es quien registró, no el promotor responsable. No hay vínculo visita↔usuario-operador.
- Usuarios Operador viven en `usuarios` (`rol_id=3`, `estado`, `eliminado`) gestionados en `usuarios_controller.py:crear/editar/eliminar`. No existe sincronización con `promotores`.
- Consumidores del nombre: `consulta/detalle.html` (None-safe "No asignado"), `email/nuevo_registro.html:73` y `reporte_service.py:32,67` (acceso directo `v.promotor.nombres`, revienta con `NULL`).
- Restricción: migración Alembic existente `c7e1a92f4b30` hizo `promotor_id` nullable; no se quiere migración destructiva ni romper las 507 filas migradas / tests de regresión (`tests/test_registro.py`, `test_consulta.py`).

## Goals / Non-Goals

**Goals:**
- `#promotor_id` muestra unión en vivo `promotores activos + operadores activos`; crear un Operador lo hace aparecer sin pasos extra.
- Guardar visita con promotor Operador sin romper FK ni visitas históricas; detalle/reportes/email muestran el nombre correcto.
- Persistencia tras error de validación (`|string` + rehidratado JS) funciona también para opciones Operador.

**Non-Goals:**
- No se cambian permisos ni roles: Operador (rol 3) sigue sin acceso a `Registrar/Editar/Reportes`; solo su nombre es elegible.
- No se fusionan las tablas `usuarios` y `promotores` ni se reescriben visitas históricas.
- No se añade CRUD de promotores en UI ni gestión de catálogo en este change.

## Decisions

### Decisión 1: Fuente unión en vivo en el controller (no tabla espejo)

- **Qué:** en `registrar()` y `editar()` (GET y re-render tras error) construir `opciones_promotor = promotores_activos + operadores_activos` (query a `Usuario` con `rol_id==3, estado==True, eliminado==False`, ordenados por apellidos/nombres) y pasarla al template como hoy se pasa `promotores` (mantener nombre de variable o añadir `operadores`; el template itera ambas).
- **Por qué sobre alternativa espejo (auto-crear fila `Promotor` por cada Operador en `usuarios_controller.crear`):** la unión en vivo cumple "se actualiza la lista cada que haya un nuevo usuario operador" por construcción, sin jobs ni hooks de sync que se desfasen (cambio de rol, baja, reactivación). La alternativa espejo duplica nombres/DNI en dos tablas y exige sync en crear/editar/eliminar/reactivar — cuatro puntos de fallo.
- **Alternativa descartada:** snapshot de nombre en `visitas` (columna texto libre) — pierde integridad referencial y complica reportes.

### Decisión 2: Distinguir origen con valor prefijado + columna FK nueva nullable

- **Qué:** `<option value="promotor:<id>">` para clásicos y `<option value="operador:<id>">` para usuarios; vacío = sin promotor. Nueva columna nullable `visitas.operador_promotor_id FK → usuarios.id` (migración Alembic) con invariante "a lo sumo uno de (`promotor_id`, `operador_promotor_id`) no nulo". El POST parsea el prefijo; el template marca `selected` comparando el string completo (extiende el comparador `|string` existente). Helper de lectura `visita.promotor_nombre` resuelve: operador → `Usuario`, clásico → `Promotor`, ninguno → `None` ("No asignado").
- **Por qué sobre reutilizar `promotor_id` con IDs de usuario:** `promotor_id` es FK real a `promotores`; meter IDs de `usuarios` rompería integridad y colisionaría (ambas tablas empiezan en 1).
- **Por qué sobre una sola columna polimórfica sin FK:** se pierde la garantía referencial y el ORM; la columna extra mantiene ambas FK reales y es rollback-safe (columna nullable, código viejo la ignora).

### Decisión 3: Mostrar con `optgroup` / `data-origen`, sin cambiar estilos globales

- **Qué:** agrupar opciones en `optgroup label="Promotores"` y `optgroup label="Operadores"` (o sufijo "(Operador)" si se prefiere lista plana), con `data-origen` por opción para tests (`assert 'data-origen="operador"' in html`). Reutiliza `form-select` y persistencia existentes; sin nuevos CSS ni JS salvo el comparador de `selected` con prefijo.
- **Alternativa descartada:** dos selects separados — rompería el contrato "un solo Promotor Responsable" y el POST/validación actuales.

## Risks / Trade-offs

- [Riesgo] `reporte_service.py` y `email/nuevo_registro.html` acceden `v.promotor.nombres` directo → `AttributeError` con `NULL` u Operador → **Mitigación:** usar el helper `promotor_nombre` en los 3 consumidores (detalle ya es None-safe; reportes/email se hacen None-safe + resolución Operador) con test de regresión.
- [Riesgo] Invariante "solo uno de los dos FK" violable por edición manual → **Mitigación:** validación en service (`ValueError` si ambos vienen seteados) + `CHECK` en migración donde el motor lo soporte.
- [Riesgo] Operador dado de baja deja visita huérfana de nombre → **Mitigación:** resolución tolerante (si el `Usuario` está eliminado/inactivo, mostrar último nombre conocido o "No asignado (baja)"; nunca 500). Decisión fina de texto en implementación.
- [Trade-off] Una columna nueva exige migración Alembic en MySQL productivo (`azconsultingperu_sgrv_visitas`) — paso incluido en tasks con downgrade.

## Migration Plan

1. Deploy código + migración Alembic `add visitas.operador_promotor_id nullable FK usuarios` (online-safe, sin backfill: existentes quedan `NULL` = comportamiento actual).
2. Verificar: `GET /registro/` lista unión; crear Operador de prueba aparece; visita con Operador se guarda y se ve en detalle/reporte.
3. Rollback: revert código (el template viejo ignora la columna nueva); `alembic downgrade -1` solo si no hay visitas nuevas con Operador (si las hay, quedan con `operador_promotor_id` set pero código viejo muestra "No asignado" — pérdida solo visual, recuperable al re-aplicar).

## Open Questions

- Ninguna que bloquee specs o tasks. Detalle menor diferible a implementación: texto exacto para Operador dado de baja ("No asignado" vs "Nombre (inactivo)") y si el `optgroup` será agrupado o lista plana con sufijo — ambas cumplen los scenarios.
