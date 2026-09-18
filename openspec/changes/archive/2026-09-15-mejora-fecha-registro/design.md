## Context

Actualmente `registro/index.html:34` y `:133` y `editar.html:92` usan `input type="date"` nativo. El popup es inconsistente (Chrome/Edge desktop vs Safari/Firefox vs Android/iOS), obliga a navegar año por año para 2008-2010, y no permite escribir `15032008` rápido. El proyecto ya usa `inputmode="numeric"` para DNI/celular, Lucide para íconos, y `fetch` para `calcularEdad`. No hay dependencia de calendario externa. Backend espera `YYYY-MM-DD` (`registro_controller`, `registro_service`).

Ver `proposal.md` para motivación y alternativas evaluadas.

## Goals / Non-Goals

**Goals:**
- Eliminar dependencia del popup nativo como única vía.
- Permitir escritura rápida enmascarada `DD/MM/AAAA` + calendario ligero a demanda.
- Preservar contrato backend `YYYY-MM-DD`, validación, edad, rehidratación y a11y.
- Añadir ≤10KB JS/CSS, sin jQuery, sin romper `lint-boundaries`.

**Non-Goals:**
- Cambiar modelo de datos ni `registro_service` (solo normalización de formato si se acepta DD/MM/AAAA server-side).
- Unificar filtros de `auditoria/consulta` en esta primera iteración (quedan como follow-up).
- Introducir date-fns/moment pesado; usar `Date` nativo o lib <3KB.

## Decisions

**Decisión 1: Híbrido máscara + calendario ligero (flatpickr 4.x o litepicker vanilla) sobre solo máscara o solo selects.**
- *Por qué híbrido*: cubre power users (teclado) y usuarios visuales (calendario). Solo máscara deja sin ayuda visual; solo selects son verbosos (3 campos) y rompen copy/paste.
- *Alternativas consideradas*: 
  - A Máscara sola → descartada por falta de descubrimiento.
  - B 3 selects → descartado por fricción y 3x validación.
  - C Calendario siempre visible → descartado por peso y sin escritura rápida.
- *Rationale de librería*: flatpickr es vanilla, 7KB gz, sin dependencias, soporta `dateFormat`, `altInput`, `locale es`, `yearSelector`, y `allowInput`. Litepicker similar. Evaluar ambas en tareas; elegir la que no requiera CSS global invasivo.

**Decisión 2: Input visible `type="text"` con `inputmode="numeric"` + campo hidden o conversión en submit para `YYYY-MM-DD`.**
- *Por qué*: evita `type="date"` nativo y su popup, permite placeholder `DD/MM/AAAA`. Hidden `name="fecha_nacimiento"` con ISO simplifica backend sin cambios. Alternativa de convertir en submit con JS es frágil si JS falla → hidden + normalización server-side como fallback.
- *Implementación*: `<input type="text" data-fecha-input>` visible + `<input type="hidden" name="fecha_nacimiento">` sincronizado en `input`/`change`. En degradación sin JS, el visible es el que se envía y el backend acepta ambos formatos.

**Decisión 3: Máscara con separadores automáticos y validación en blur/submit, no en cada keystroke bloqueante.**
- *Por qué*: insertar `/` tras 2 y 5 dígitos es familiar, no bloquea borrado. Validación agresiva en cada tecla frustra.
- *Alternativa*: inputmask library → descartada por peso; implementar 30 líneas vanilla.

**Decisión 4: No tocar `registro_controller` salvo normalizador opcional `DD/MM/AAAA` → `YYYY-MM-DD`.**
- *Por qué*: minimiza riesgo y mantiene tests existentes. Normalizador es 1 función `parse_fecha_ddmmyyyy` en `registro_service` o `helpers`.

## Risks / Trade-offs

- **Divergencia de formato visible vs enviado** → Mitigación: sincronización bidireccional y tests de rehidratación.
- **Calendario ligero añade CSS/JS y z-index** → Mitigación: scope CSS bajo `.fecha-input`, lazy-load solo en registro, test en dark mode.
- **Usuarios acostumbrados a date nativo en móvil** → Mitigación: `inputmode=numeric` muestra teclado numérico; calendario sigue disponible vía botón.
- **Validación bisiesto y rangos** → Mitigación: usar `new Date(yyyy, mm-1, dd)` y verificar round-trip.

## Migration Plan

1. Crear `app/static/js/fecha-input.js` y `fecha-input.css`, incluir en `base.html` o bloque `extra_js` de registro.
2. Reemplazar inputs en `index.html` y `editar.html`, añadir hidden y botón Lucide, inicializar con `data-` attrs.
3. Ajustar `calcularEdad` para escuchar `change` del hidden/visible y rehidratar desde `form.fecha_*`.
4. Añadir normalizador server-side si se decide aceptar `DD/MM/AAAA` sin JS.
5. Tests: `tests/test_registro.py` para submit con `DD/MM/AAAA` y rehidratación.
6. Rollback: revertir templates a `type="date"`; el hidden es ignorado.

## Open Questions

- ¿Unificar también `auditoria/index.html` filtros `fecha_desde/hasta` en este mismo cambio o dejar para follow-up? Propuesta: follow-up.
- ¿Locale del calendario `es-PE` con `Lunes` como primer día? Confirmar con producto (asumimos sí).
