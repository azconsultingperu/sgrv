## 1. Controller - flashes únicos

- [x] 1.1 Modificar `app/modules/registro/presentation/registro_controller.py` en `registrar()` para emitir un solo flash por POST (si foto falla → solo `danger` sin `success`; si ok o sin foto → solo `success`), eliminar `db.session.rollback()` tras UoW y verificar que `POST /registro/` sin foto redirige 302 con flash success visible y `POST` con foto inválida muestra solo danger sin crear duplicado.
- [x] 1.2 Ajustar `editar()` con misma regla de flash único para foto y verificar que reemplazar/eliminar foto mantiene un solo flash.

## 2. Templates - placeholder, botón y centrado móvil

- [x] 2.1 Reemplazar placeholder "--" por `<img src="avatar-default.svg">` dentro de `#alumnoFotoWrap` en `app/templates/registro/index.html` y `editar.html` y verificar que sin foto se ve el svg tenue centrado.
- [x] 2.2 Hacer botón dinámico en `index.html`: inicial "Añadir foto" (cambia a "Cambiar foto" tras seleccionar) y "Eliminar" aparece solo con preview, y en `editar.html` respeta estado existente, y verificar que el texto cambia sin recargar.
- [x] 2.3 Centrar en móvil foto, botones y texto de ayuda con `justify-content-center` / `text-center` y `justify-content-md-start` en desktop en ambos templates y verificar en viewport 375px que todo queda centrado y en 1024px alineado a la izquierda.
- [x] 2.4 Verificación E2E: llenar formulario sin foto y con foto válida, comprobar que el registro aparece en `/consulta/` y que el toast `success` brinca una sola vez; repetir con foto inválida y comprobar que solo aparece `danger`.
