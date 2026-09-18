## 1. Componente base fecha-input

- [x] 1.1 Crear `app/static/js/fecha-input.js` con máscara `DD/MM/AAAA` (auto `/` tras 2 y 5, `inputmode=numeric`, paste normalizado, validación fecha real) y sincronización a hidden `YYYY-MM-DD` — verificar escribiendo `15032008` muestra `15/03/2008` y hidden vale `2008-03-15`
- [x] 1.2 Crear `app/static/css/fecha-input.css` (scope `.fecha-input`, botón calendario Lucide, overlay calendario, dark mode) — verificar sin regresión visual en registro
- [x] 1.3 Integrar calendario ligero (flatpickr o litepicker vanilla) con botón `calendar` a demanda, navegación rápida año, locale es-PE — verificar abrir con botón, seleccionar fecha actualiza input y dispara `change`, cerrar con Esc/click fuera

## 2. Integración en templates registro

- [x] 2.1 Reemplazar `type="date"` por componente en `app/templates/registro/index.html` para `fecha_nacimiento` y `fecha_visita` (visible `text` + hidden ISO + botón) — verificar `registro/index.html` renderiza placeholder `DD/MM/AAAA` y submit envía `YYYY-MM-DD`
- [x] 2.2 Reemplazar en `app/templates/registro/editar.html` con conversión `YYYY-MM-DD` → `DD/MM/AAAA` en render — verificar editar muestra `15/03/2008` si `form.fecha_visita="2008-03-15"`
- [x] 2.3 Adaptar JS existente (`calcularEdad`, auto `fecha_visita/hora`, rehidratación tras error) para escuchar `data-fecha-input`/`hidden` — verificar `edad` se calcula al seleccionar fecha vía calendario y tras re-render con `form.fecha_nacimiento` previo

## 3. Validación y backend

- [x] 3.1 Añadir validación frontend `is-invalid` + `invalid-feedback` para formato y rango (no futuro, ≥1900) en blur/submit — verificar `31/02/2008` marca error y `15/03/2008` pasa
- [x] 3.2 Añadir normalizador server-side `DD/MM/AAAA` → `YYYY-MM-DD` en `registro_controller`/`registro_service` como fallback sin JS — verificar `POST` con `15/03/2008` crea registro correctamente
- [x] 3.3 Verificar persistencia tras error: `POST /registro/` con `dni` inválido mantiene `fecha_nacimiento` y `fecha_visita` visibles — verificar re-render muestra valores previos

## 4. Accesibilidad y QA

- [x] 4.1 Añadir a11y: `aria-label` en botón calendario, `role="dialog"` en overlay, navegación teclado (Tab, flechas, Enter, Esc) — verificar con teclado solo se opera completo
- [x] 4.2 Pruebas manuales desktop/móvil (Chrome, Firefox, Safari, Android) y verificación `FLASK_ENV=testing pytest tests/test_registro.py -v` — verificar sin regresión, `test_boundaries` pasa, y `calcularEdad` sigue funcionando

