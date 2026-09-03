## 1. Persistencia de selects y derivados

- [x] 1.1 Cambiar en `app/templates/registro/index.html` y `editar.html` los 3 selects (`institucion_id, carrera_id, promotor_id`) a `{% if form.xxx|string == c.id|string %}selected{% endif %}` y verificar que tras `POST` con error los 3 quedan seleccionados.
- [x] 1.2 Añadir en `index.html` JS que al `DOMContentLoaded` si `form.institucion_id` o `form.fecha_nacimiento` ya traen valor, dispare `change` de institucion y `calcularEdad()` para rellenar `distrito/provincia/edad`, y verificar que tras error esos readonly muestran el valor previo.
- [x] 1.3 Verificación E2E: llenar `institucion=3, carrera=2, promotor=5, fecha=2008-01-01` y enviar con `dni` inválido → la respuesta 200 muestra el form con los 3 selects y derivados intactos y solo `dni` marcado con error.
