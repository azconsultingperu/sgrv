## 1. Tokens, lint y base responsive

- [ ] 1.1 Normalizar tokens y jerarquía en `style.css` y verificar que `h5.text-success/warning/info` ya no existe en `registro/index.html` y que `getComputedStyle` devuelve `var(--text-primary)` para `h5.section-title`
- [ ] 1.2 Subir `control-height-sm` a 36px y forzar 44px en móvil para `pagination .page-link`, `btn-group-sm` y `navbar avatar`, y verificar en 360px que cada `page-link` mide ≥44px con `getBoundingClientRect`
- [ ] 1.3 Añadir `make lint-design` (o `stylelint`) que falle si encuentra `color: #` hardcodeado fuera de `auth.css`, `h5.text-*` semántico o `min-height:34px` en móvil, y verificar que `make lint-design` falla ante un `color: #fff` de prueba y pasa sin él
- [ ] 1.4 Corregir `100dvh` y safe-area en `style.css` (`main-content` `min-height` + `padding-bottom: calc(1.5rem + env(safe-area-inset-bottom))` para `#toastContainer` y drawers), y verificar en iPhone notch que el último botón no queda bajo el home indicator

## 2. Toast-island móvil dirección B

- [ ] 2.1 Migrar `main.js`/`style.css` a isla superior en `es-movil` (`top: calc(env(safe-area-inset-top,0)+12px)`, `translateX(-50%)`, `width: min(92vw,400px)`, entrada `translateY(-20px) scale(.96)` 0.32s `cubic-bezier(.16,1,.3,1)`), y verificar en 360px que `mostrarToast('success',...)` aparece centrado arriba sin tapar navbar
- [ ] 2.2 Añadir gesto táctil a isla (touchstart pausa, swipe horizontal con velocity cierra, `navigator.vibrate(10)` en danger) y verificar que un swipe de 70px descarta el toast con `mcIslandOut` y que `mouseenter` ya no es requerido en móvil
- [ ] 2.3 Respetar `prefers-reduced-motion` y coexistencia con sidebar (`body.sidebar-open` baja isla a `top:70px` o `z-index` 1020), y verificar que con `prefers-reduced-motion: reduce` no hay `mcToastIn` y con sidebar abierto la isla no queda debajo del backdrop

## 3. Tablas responsive y filter drawer

- [ ] 3.1 Implementar patrón `table[data-responsive="cards"]` (thead oculto en <768px, `tr` como card con `td::before` desde `data-label` generado desde `th`) y verificar en 360px que `consulta/index.html` no tiene scroll horizontal y muestra 3 cards con acciones 44px
- [ ] 3.2 Aplicar `table--cards` a `consulta`, `auditoria`, `usuarios` y `reportes`, y verificar en 360/768/1024 que la tabla es `table` en desktop y `cards` en móvil sin duplicar markup
- [ ] 3.3 Implementar `filter-drawer` bottom sheet (reuse `.confirm-overlay`, `max-height:80dvh`, backdrop, `Aplicar`/`Cancelar`/`Limpiar`) y teleport del `form` en <768px, y verificar que en 360px solo se ve botón `Filtros (n)` y `Aplicar` cierra drawer y actualiza URL con `search_params`
- [ ] 3.4 Verificar que `filter-drawer` preserva `pagination` (reset a 1) y que `…` de paginación sigue siendo clicable a 44px en móvil con `pytest tests/test_consulta.py` verde

## 4. Formularios y confirmaciones

- [ ] 4.1 Envolver formularios largos (`registro/index.html`, `registro/editar.html`) en `form-section` acordeón (desktop siempre abierto, móvil solo primero abierto, `aria-expanded`, animación `max-height`), y verificar en 360px que solo Datos Personales está expandido y que un submit fallido expande la sección con el primer campo inválido enfocado
- [ ] 4.2 Corregir `inputmode`/`autocomplete` en formularios (DNI `inputmode="numeric" pattern="[0-9]*"`, `tel`, `email`) y verificar que en Android/iOS el teclado mostrado es numérico/tel/email según campo
- [ ] 4.3 Migrar `confirm-modal` a `confirm-sheet` en móvil (bottom `border-radius 16px 16px 0 0`, handle, swipe-down, haptic) y verificar en 360px que `Eliminar` en `usuarios` muestra sheet y un swipe-down lo cierra sin ejecutar y `Esc` hace shake

## 5. Navegación, dashboard y polish

- [ ] 5.1 Añadir swipe-from-edge (0-30px) para abrir sidebar y `overscroll-behavior: contain` + `Esc` para cerrar, y verificar que en iOS el `lockMainScroll` no deja el body congelado al cerrar
- [ ] 5.2 Adaptar dashboard a móvil (`chart-frame` 240px, `stat-card` 84px/`stat-icon` 40px, lazy render del 2º chart vía `IntersectionObserver` + skeleton pulse), y verificar que el primer paint en 360px muestra 5 cards + 1 chart sin scroll horizontal y el segundo chart carga al hacer scroll
- [ ] 5.3 Implementar estados globales (`empty-state` ya existe, añadir `skeleton` pulse y `alert` + Reintentar) y verificar que `consulta` sin filtros muestra `empty-state` con CTA y que un chart en carga muestra 3 skeletons
- [ ] 5.4 Auditoría visual integral en 360/768/1024 + `prefers-reduced-motion` y `make lint-design` verde, y verificar que `pytest` y `lint-imports` siguen verdes y que un nuevo módulo `seguimiento` de prueba hereda los 7 componentes sin CSS ad-hoc
