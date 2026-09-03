## ADDED Requirements

### Requirement: Foto anclada al hacer scroll en desktop

En `consulta/detalle.html` la card de foto (`col-md-4`) SHALL permanecer visible al hacer scroll vertical en viewport `>=768px` mediante `position:sticky` con `top:80px`, `align-self:flex-start` y `z-index:1`. En viewport `<768px` SHALL no aplicar sticky y la foto SHALL quedar arriba apilada con la tabla debajo.

#### Scenario: Desktop mantiene foto visible
- **WHEN** se abre `/consulta/detalle/<id>` en desktop 1024px y se hace scroll 400px hacia abajo
- **THEN** la card de foto permanece anclada a 80px del top del viewport (justo debajo del navbar) mientras la tabla derecha sigue scrolleando

#### Scenario: Móvil no hace sticky
- **WHEN** se abre el mismo detalle en 375px y se hace scroll
- **THEN** la foto no queda fija sino que scrollea normal junto con el contenido (no tapa la tabla)

#### Scenario: Sin solape con navbar
- **WHEN** la foto está en estado sticky
- **THEN** su borde superior queda a 80px del top, sin solaparse con el navbar de 60px

#### Scenario: Sin JS
- **WHEN** se inspecciona el CSS de la card de foto
- **THEN** la regla usa solo `position:sticky` y `@media`, sin listeners de scroll
