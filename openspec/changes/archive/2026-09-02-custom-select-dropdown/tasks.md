## 1. Componente base

- [x] 1.1 Crear `app/static/js/custom-select.js` que inicialice `querySelectorAll('select.form-select')`, oculte cada `select` y renderice `div.custom-select > button.form-select` + `ul.dropdown-menu` con `li a.dropdown-item` por `option`, leyendo `select.options[select.selectedIndex].text` al inicio para respetar `selected` de Jinja (edición) y mostrando placeholder si `value=""`; verificar con `grep -n "custom-select" app/static/js/custom-select.js` y abriendo `registro/editar.html` que el botón muestra la institución/carrera precargada.

- [x] 1.2 Añadir estilos en `app/static/css/style.css` para `.custom-select`, `.custom-select-button` (reusa `form-select` vars, `border`, `radius`, `focus` con `box-shadow`) y `.custom-select .dropdown-menu` (reusa `dropdown-menu` existente, `max-height` con scroll); verificar en DevTools que el desplegable se ve con bordes redondeados y sombra del sistema en light/dark.

## 2. Integración con formularios

- [x] 2.1 Implementar puente de validación: sincronizar `is-invalid` del `<select>` oculto al botón visible (`classList.toggle('is-invalid', select.classList.contains('is-invalid'))` tras `change`/`blur`) y asegurar que `.custom-select-button.is-invalid` pinte `border-color: var(--danger-color)` igual que `form-select.is-invalid`; verificar forzando `select.classList.add('is-invalid')` y viendo el botón con borde rojo y el `invalid-feedback` debajo.

- [x] 2.2 Asegurar propagación de `change`: al elegir opción en el custom, actualizar `select.value` y disparar `select.dispatchEvent(new Event('change', {bubbles:true}))` y `input`; verificar en `registro/index.html` que cambiar `institucion_id` autocompleta `distrito` vía el listener existente `select[name="institucion_id"].addEventListener('change', ...)`.

- [x] 2.3 Verificar filtros GET: en `auditoria/index.html` y `consulta/index.html`, elegir valores en los customs y hacer submit, confirmando que la URL contiene `?usuario_id=...&modulo=...` y `?sexo=...&carrera_id=...` y el backend filtra igual que con nativo; verificar con `curl` o inspección de `FormData` que `select.name`/`value` ocultos se envían.

## 3. Estado inicial y accesibilidad

- [x] 3.1 Manejar `selected` inicial y `form.reset()`: en init leer `selectedIndex` y en `form.addEventListener('reset', () => setTimeout(syncFromSelect,0))` sincronizar botón al valor restaurado; verificar abriendo `registro/editar.html` con institucion precargada y haciendo `form.reset()` que el botón vuelve al placeholder/valor inicial.

- [x] 3.2 Añadir a11y y teclado: `aria-haspopup="listbox"`, `aria-expanded`, roles `option`, navegación `ArrowUp`/`ArrowDown`/`Enter`/`Escape` y foco; verificar con teclado que se puede abrir, navegar y seleccionar sin mouse.

## 4. Integración y verificación final

- [x] 4.1 Incluir `custom-select.js` en `app/templates/base.html` y bump `?v=` para `style.css`/`custom-select.js`; probar en `registro` (5 selects), `usuarios` (rol), `auditoria` y `consulta` que los 15 selects muestran el desplegable custom con hover de la paleta, validación, `change` y `selected` correctos, sin regresión en `auth-validation.js`.
