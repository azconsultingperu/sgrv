## 1. Panel y scroll

- [x] 1.1 Cambiar en `app/static/js/main.js` y `app/templates/registro/index.html`/`editar.html` el cálculo de progreso y `scrollToInvalid` para usar `mainContent.scrollTop` y `mainContent.scrollTo`/`scrollIntoView` dentro de `.main-content` en vez de `window`, evitando reflow del `sidebar`; verificar ocultando panel en móvil y validando vacío que el panel no reaparece.

## 2. Validación sin bordes rojos

- [x] 2.1 Quitar en `app/static/js/main.js` el bloque que añade `is-invalid`/`input-glow` genérico en `form.checkValidity()===false` (mantenerlo solo para `fetch` de DNI duplicado) y asegurar que solo se hace `scroll` al primer `:invalid` sin pintar borde rojo; verificar enviando vacío que no hay `border-color: var(--danger-color)` en inputs y solo aparece `invalid-feedback` y toast.

## 3. Carrera en consultar

- [x] 3.1 Cambiar en `app/templates/consulta/index.html` el filtro de carrera de `col-md-2` a `col-md-3` y quitar `[:20]` en `{{ c.nombre[:20] }}` para `{{ c.nombre }}`, y en `app/static/css/style.css` ajustar `.custom-select-menu` a `min-width:240px; width:max-content; max-width:320px` para que el desplegable no se corte por el ancho corto del select; verificar que nombres largos se ven completos.

## 4. Verificación y bump

- [x] 4.1 Hacer bump de `?v=` en `app/templates/base.html` para `style.css`/`main.js`/`custom-select.js` y probar en `registro` y `consultar` que los tres fixes funcionan juntos sin regresión.
