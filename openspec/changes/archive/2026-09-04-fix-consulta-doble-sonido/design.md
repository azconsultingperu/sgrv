## Context

Ver proposal Why. El bug es carrera: `base.html` carga `main.js` antes que `consulta/index.html:152` (extra_js), así que `main.js` lee `flashData` y dispara `mostrarToast` + Audio antes de que el intercept lo vacíe y ponga `_consultaCargaTrigger`. El guard `main.js:487` nunca bloquea a tiempo → 2 sonidos.

## Goals / Non-Goals

**Goals:** Sonido 1:1 con toast visible, solo 1 sonido delayed tras overlay cuando vienes de registro/eliminar; resto de toasts normales sin regresión.

**Non-Goals:** No cambiar duración 4500ms, no cambiar flash ni redirect, no añadir query param, no tocar auditoría.

## Decisions

**Decisión 1: Mover intercept síncrono antes de main.js (base.html)**
- *Por qué:* Garantiza que `flashData` se vacíe antes de que `main.js` lo lea. El intercept actual en `consulta/index.html` corre después de `main.js` (script src antes que extra_js), así que llega tarde. Moviendo el IIFE que detecta `Registro creado|eliminado` a `base.html` justo después de `<div id="flashData">` y antes de `<script src="main.js">`, el trigger se setea primero y el guard `window._consultaCargaTrigger` sí bloquea el inmediato. Alternativa de hacer main.js esperar DOMContentLoaded también funciona pero cambia timing global de todos los toasts.
- *Alternativa descartada:* `setTimeout` en main.js → frágil, race sigue dependiendo de ms.
- *Alternativa descartada:* sessionStorage/query param → cambia contrato redirect innecesariamente.

**Decisión 2: Mantener guard en main.js + liberar antes del delayed**
- *Por qué:* `crearToast` ya bloquea si `window._consultaCargaTrigger && /Registro (creado|eliminado)/` (main.js:487). Con el nuevo orden, el inmediato será bloqueado (sin Audio). El delayed hace `window._consultaCargaTrigger=null` antes de `mostrarToast`, así que ese sí crea toast + Audio una vez.
- *Riesgo:* Si el usuario recarga durante overlay, el flash ya se consumió → segunda carga no tiene overlay ni sonido, que es lo deseado (flash de un solo uso).

**Decisión 3: No tocar duración ni overlay**
- *Por qué:* Fuera de alcance; el bug es solo doble sonido, no UX de tiempo.

## Risks / Trade-offs

- **Intercept en base.html corre en todas las páginas** → Mitigación: solo activa overlay si existe `#consultaCargaOverlay` y trigger coincide; en otras páginas es no-op.
- **Orden de scripts en base.html crítico** → Mitigación: documentar en design y testear que `flashData` intercept esté justo después del div y antes de main.js.

## Migration Plan

Solo frontend: mover IIFE a base.html + ajustar `consulta/index.html` para no duplicar lógica (dejar solo el DOMContentLoaded del overlay). Rollback: revert base.html + consulta. Verificación: registrar alumno → consultar debe mostrar 0 toasts inmediatos, 1 toast delayed con 1 Audio.

## Open Questions

- Ninguna.
