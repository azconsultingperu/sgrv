## Context

Ver `proposal.md`. Hay 15 `select.form-select` en 6 templates, todos con estilo cerrado pulido pero desplegable nativo. El navbar ya usa `div.dropdown` + `button[data-bs-toggle="dropdown"]` + `ul.dropdown-menu` con `dropdown-item` (ver `navbar.html:16-27`) con vars de `style.css` (border, radius, shadow). `auth-validation.js` valida inputs y añade `is-invalid` + `invalid-feedback`; los selects de filtros son `GET` y el de `registro` tiene listener `change` para distrito.

## Goals / Non-Goals

**Goals:** Desplegable custom con misma identidad que el navbar, puente de validación `is-invalid`, propagación de `change` para `institucion_id→distrito`, compatibilidad `name`/`value` en `GET`, respeto de `selected` inicial de Jinja y `form.reset()`, sin dependencia externa.
**Non-Goals:** Búsqueda dentro del select, multi-select, virtualización, cambiar `auth-validation.js` más allá de integración, tocar backend o `auth.css`, añadir Choices.js/TomSelect.

## Decisions

**1. Hand-made reutilizando dropdown de navbar (no librería)**
- Nuevo `app/static/js/custom-select.js` que hace `querySelectorAll('select.form-select')` al `DOMContentLoaded`, oculta cada `select` (`style.display='none'`), inserta `div.custom-select > button.form-select` + `ul.dropdown-menu` y genera `li a.dropdown-item` por `option`. Click en item → `select.value = option.value; select.dispatchEvent(new Event('change',{bubbles:true})); select.dispatchEvent(new Event('input',{bubbles:true}));` + actualiza `button.textContent` y cierra.
- Alternativa Choices.js/TomSelect descartada: añade 15-40KB, tema light/dark hay que mapear, y trae UI distinta al dropdown del sistema.
- CSS puro `appearance:none` descartado: no estiliza el popup en Chrome/Win y Firefox.

**2. Puente de validación**
- Observar `select` con `MutationObserver` para clase `is-invalid` o hacer `customButton.classList.toggle('is-invalid', select.classList.contains('is-invalid'))` tras cada `change` y en `blur`. El `invalid-feedback` ya existe bajo el `select` (o se crea); el CSS de `.form-select.is-invalid` también debe aplicarse al botón: `.custom-select-button.is-invalid { border-color: var(--danger-color); box-shadow: 0 0 0 3px rgba(220,53,69,0.12); }`.
- Alternativa modificar `auth-validation.js` para que valide `select` directamente descartada: el módulo actual solo conoce `input` por `name`; mejor que el custom emule el input.

**3. Selected inicial y reset**
- En `init`, `const idx = select.selectedIndex; const opt = select.options[idx]; button.textContent = opt ? opt.text : ''` — respeta `{% if ... %}selected{% endif %}` de Jinja. Para `form.reset()`, escuchar `form.addEventListener('reset', () => setTimeout(syncFromSelect, 0))` donde `syncFromSelect` relee `selectedIndex`.
- Alternativa re-render tras `reset` sin `setTimeout` falla porque el `selected` aún no se ha restaurado.

**4. Sin tocar markup de templates**
- No se modifica `registro/*.html` etc.; el `select` sigue con `name`/`id`/`required`. El custom se inserta como hermano; el `form` envía el `select` oculto, por lo que `GET` de auditoría/consulta no cambia.

## Risks / Trade-offs

- **A11y incompleta (listbox vs native select)** → Mitigación: `aria-haspopup="listbox"`, `aria-expanded`, roles `option`, navegación con `ArrowUp`/`ArrowDown`/`Enter`/`Escape` y `focus` management; probar con teclado y lector básico.
- **Listener de distrito depende de `select` oculto** → Mitigación: disparar `change` burbujeante garantiza que el handler existente en `registro/index.html:188` se ejecute sin re-registrar.
- **`MutationObserver` puede ser overkill** → Mitigación: en lugar de observer, cada `change` y cada `blur` del custom sincroniza `is-invalid`; suficiente para `auth-validation.js` que valida en `blur`/`input`/`submit`.
- **`body:has()` para toasts no afecta selects** → No aplica.

## Migration Plan

1. Crear `custom-select.js` y estilos en `style.css` (reusa `dropdown-menu` existente).
2. Incluir `custom-select.js` en `base.html` y bump `?v=`.
3. Probar en `registro` (5 selects, con `institucion→distrito`), `usuarios` (rol), `auditoria` y `consulta` (filtros GET) que el valor se envía y la validación pinta el botón.
4. Verificar edición con `selected` precargado y `form.reset()`.
5. Rollback: quitar `custom-select.js` y su `link` en `base.html`; los `select` nativos vuelven al mostrarse (`display:block`).

## Open Questions

- Ninguna.
