## 1. Scroll de página + zona segura en móvil

- [x] 1.1 Mover el scroll al `body` en `<=991px` (retirar scroller interno de `.main-content`) con `padding-bottom` de área segura (`env(safe-area-inset-bottom)` + fallback) y verificar en emulación 360×640 que `body.scrollHeight > viewport` y el botón Guardar de `/registro/` es visible y clicable al fondo.
- [x] 1.2 Re-anclar `sticky` al nuevo scroller (navbar `top:0`, barra de progreso de registro, headers de tabla) y verificar con screenshots que siguen fijos al scrollear en móvil y que desktop `>991px` queda idéntico (comparar screenshots antes/después).

## 2. Acciones de tabla visibles

- [x] 2.1 Columna de acciones fija visible en `<=767px` (o tarjetas donde aplique) en consulta, usuarios, reportes y auditoría, manteniendo permisos por rol, y verificar en cada una que sus acciones se ven sin swipe horizontal.
- [x] 2.2 Matriz sticky por página (dashboard, consulta, registro, editar, detalle, usuarios, reportes, perfil) y verificar que ningún `sticky`/`fixed` tapa botones en 360×640.

## 3. Drawer cerrable

- [x] 3.1 Botón ✕ visible en el sidebar solo en móvil + cierre con Escape (reutilizando `closeSidebar()`), conservando backdrop y auto-cierre al navegar, y verificar abriendo/cerrando por las 3 vías en emulación táctil sin que la página quede congelada (scroll responde tras cerrar).

## 4. Verificación integral

- [x] 4.1 Batería emulada 360×640 con screenshots (login, registro arriba/abajo, drawer abierto/cerrado, consulta, usuarios, editar con botones al fondo) y verificar cada scenario de `specs/responsive-movil/spec.md`.
- [x] 4.2 Aceptación en dispositivo físico del usuario (admin y operador): botones finales alcanzables y acciones visibles; si algo falla, reportar modelo de teléfono y zona exacta.
  - Fallo reportado 2026-09-19 (físico, servidor local por red): drawer navega OK, pero Guardar/Cancelar (registro) y equivalentes no se ven; filas de usuarios cortadas a la mitad con un "espacio" bloqueante; sin scroll en ningún módulo. Emulación 360×640 pasa 11/11.
  - Protocolo: captura del estado, navegador exacto (Chrome vs Samsung Internet vs otro), verificar CSS servido `style.css?v=70`, probar rotación, probar cerrar drawer con ✕ y reintentar scroll.
  - Resuelto 2026-09-21: causa raíz `body { overflow: hidden }` + sidebar sin flex; fix `html,body overflow-y:auto` + `overflow-x:clip` + `100dvh` + safe-area (`?v=71`); verificado en teléfono físico del usuario en producción — drawer, scroll y botones OK.
