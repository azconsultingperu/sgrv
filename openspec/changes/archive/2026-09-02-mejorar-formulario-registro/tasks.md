## 1. Estructura y jerarquía

- [x] 1.1 Añadir headers numerados + separador en `registro/index.html` y `editar.html` (badge `01`–`05` dentro de cada `h5` con `border-bottom:1px solid var(--border-color)` y `padding-bottom`) y barra fina `div#registroProgress` sticky bajo navbar que se llena con scroll (JS con `requestAnimationFrame` sin librería); verificar visualmente que las 5 secciones se distinguen al hacer scroll y el progreso se llena.

## 2. Placeholders e inputmode

- [x] 2.1 Añadir `placeholder` a 8 campos en `registro/index.html` (apellidos "Ej. García López", nombres "Ej. Juan Carlos", dni "Ej. 12345678", celular "Ej. 987654321", email "Ej. juan@ejemplo.com", direccion "Ej. Jr. Lima 123, Paiján", area_interes "Ej. Ingeniería de Sistemas", observaciones "Ej. Interesado en beca, visita con padres...") y replicar en `registro/editar.html`; verificar que los placeholders se muestran cuando el campo está vacío en ambos templates.

- [x] 2.2 Agregar `inputmode="numeric"` a `dni` y `celular` en ambos templates (index y editar); verificar en móvil que el teclado numérico aparece al hacer focus y que `pattern`/`maxlength` siguen funcionando.

## 3. Checkboxes custom

- [x] 3.1 Reemplazar estilo nativo de 6 checkboxes (`registro/index` 2, `registro/editar` 2, `usuarios/editar` 1, `login` 1) por custom cuadrado `appearance:none` de 18px con borde 1.2px, check blanco y focus con halo `primary-soft` en `app/static/css/style.css` (manteniendo `form-check-input` y `name`/`value`/`checked`); verificar que los 6 se ven uniformes y al estar `checked` muestran fondo `primary` con check.

## 4. Validación y entrega

- [x] 4.1 Confirmar que validación `is-invalid`/`invalid-feedback` sigue funcionando tras placeholders/checkboxes custom: probar enviar formulario con campo requerido vacío y verificar que se añade `is-invalid` y el mensaje debajo, igual que antes; hacer bump de `?v=` en `app/templates/base.html` para `style.css` si se editó y verificar recarga.

