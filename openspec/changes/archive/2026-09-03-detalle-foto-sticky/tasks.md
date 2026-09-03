## 1. Sticky foto en detalle

- [x] 1.1 Añadir regla `.detalle-foto-sticky` en `app/static/css/style.css` con `position:sticky; top:80px; align-self:flex-start; z-index:1` dentro de `@media (min-width:768px)` y verificar que en desktop la card no se solapa con navbar.
- [x] 1.2 Aplicar `class="detalle-foto-sticky"` a la card de foto en `app/templates/consulta/detalle.html` (`col-md-4 > .card`) y verificar que al hacer scroll 400px en 1024px la foto permanece a 80px del top mientras la tabla scrollea, y que en 375px no hace sticky.
