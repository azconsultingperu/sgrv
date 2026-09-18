## 1. Plantillas — exponer provincia en el select

- [x] 1.1 Añadir `data-distrito`, `data-provincia` y `data-region` a cada `<option>` de `institucion_id` en `app/templates/registro/index.html` — verificar `GET /registro/` contiene `data-provincia="Ascope"` (u otro valor seed)
- [x] 1.2 Replicar los `data-*` en `app/templates/registro/editar.html` — verificar `GET /registro/editar/<id>` también expone provincia

## 2. JS — autocompletar provincia y región

- [x] 2.1 Modificar listener `select[name="institucion_id"]` en `registro/index.html` para leer `selected.dataset.{distrito,provincia,region}` y rellenar `#distrito`, `#provincia` y `#region` (o `#provincia`/`#region` readonly), limpiando si `!selected.value` — verificar al cambiar a colegio con provincia "Ascope" los tres campos se actualizan
- [x] 2.2 Replicar el mismo listener en `registro/editar.html` — verificar edición con valor pre-cargado muestra provincia correcta tras `dispatchEvent('change')` de rehidratación
- [x] 2.3 Verificar rehidratación tras error: `POST /registro/` con `institucion_id=1` y `dni` inválido re-renderiza con `distrito` y `provincia` visibles sin tocar el select — verificar HTML/JS muestra valores derivados
- [x] 2.4 Pruebas `FLASK_ENV=testing pytest tests/test_registro.py tests/test_boundaries.py -q` y revisión manual con `custom-select` activo — verificar sin regresión y sin lecturas frágiles de `text.split`
