## Context

Ver `proposal.md - Why`. Estado actual: `login.html:14` hace `{% raw %}{% set _ = get_flashed_messages(...) %}{% endraw %}` que vacía la cola antes de `base.html:44`, por eso el `mc-toast` nunca aparece en login inválido. El sonido `vadim...mp3` está en `~/Descargas` (33KB) sin ruta estática; no hay `app/static/sounds/`. `main.js:347` ya gestiona `mc-toast` danger pero sin audio.

## Goals / Non-Goals

**Goals:**
- Que el error de login se vea como toast y suene una vez con volumen bajo.
- Asset renombrado y reutilizable para registrar/recuperar.

**Non-Goals:**
- Cambiar lógica de autenticación ni validación de DNI+correo.
- Añadir librería de audio.

## Decisions

### 1. Quitar consumo prematuro en login.html
- **Decisión:** Eliminar `{% raw %}{% set _ = get_flashed_messages(...) %}{% endraw %}` de `login.html` (línea 14) y dejar que `base.html` lo lea. Si login necesita mostrar algo inline, usar `#flashData` como hace el resto de la app.
- **Rationale:** `base.html` es el único lector canónico; duplicar lectura genera condición de carrera.
- **Alternativa:** Dejar el `set` y duplicar lectura en base — rechazada: consume dos veces.

### 2. Mover y renombrar mp3
- **Decisión:** `mkdir -p app/static/sounds && cp ~/Descargas/vadim...mp3 app/static/sounds/error.mp3` con `preload="auto"` en JS. Nombre `error.mp3` es indicativo, corto y cacheable.
- **Alternativa:** Mantener nombre original — rechazada: largo y con espacios, rompe URL.

### 3. Hook de audio en `main.js`
- **Decisión:** En `main.js` donde se crea `mc-toast` (`mostrarToast`), si `entry.tipo === 'danger'`, hacer:
  ```js
  try { const a = new Audio('/static/sounds/error.mp3'); a.volume = 0.35; a.preload='auto'; a.play().catch(()=>{}); } catch(e) {}
  ```
  Respetar `prefers-reduced-motion` como señal para no sonar si el usuario prefiere menos animación (opcional), y envolver en `try/catch`.
- **Rationale:** Reutiliza gesto del click que disparó el toast, cumple autoplay; volumen bajo no invasivo; no duplica código si se centraliza en `mostrarToast`.
- **Alternativa:** `<audio>` tag en base — rechazada: requiere DOM extra y no respeta gesto.

## Risks / Trade-offs

- **Navegador bloquea audio sin gesto** → Mitigación: `play().catch(()=>{})` silencia el error; el toast igual aparece.
- **Sonido repetido si hay 2 toasts danger seguidos** → Mitigación: cada toast dispara su propio `play`, pero el intervalo de toasts (cola) evita solapamiento; si hay spam, el segundo se encola y suena al mostrarse, no al crearse.
- **Quitar `set _` rompe si login esperaba usar `_` en plantilla** → Mitigación: `login.html` no usa `_` después; era solo para consumir.

## Migration Plan

1. Mover mp3, crear `app/static/sounds/`, quitar `set _` de `login.html`, añadir hook en `main.js`.
2. Probar login inválido en 360/1024: 1 toast danger visible + sonido una vez; recargar recuperar con error genérico también suena si es danger.
3. `make lint-boundaries` y `pytest tests/test_auth.py -q` verdes.
4. Rollback: restaurar `login.html` con `set _` y borrar `error.mp3` (un commit).

## Open Questions

- ¿Sonido también para `success` (ej. recuperar enviado) o solo `danger`? Default: solo `danger`.
