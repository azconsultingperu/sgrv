/**
 * custom-select.js — Hand-made custom select para SGRV
 * Reutiliza el estilo del dropdown de navbar (dropdown-menu / dropdown-item)
 * Mantiene el <select> nativo oculto para compatibilidad con formularios, validación y filtros GET
 */
(function () {
    'use strict';

    function initCustomSelect() {
        var selects = document.querySelectorAll('select.form-select');
        if (!selects.length) return;

        selects.forEach(function (select) {
            if (select.dataset.customSelectInit === '1') return;
            select.dataset.customSelectInit = '1';

            // Crear contenedor
            var wrapper = document.createElement('div');
            wrapper.className = 'custom-select';
            if (select.classList.contains('form-select-sm')) wrapper.classList.add('custom-select-sm');

            // Botón visible que imita form-select
            var button = document.createElement('button');
            button.type = 'button';
            button.className = 'form-select custom-select-button';
            if (select.classList.contains('form-select-sm')) button.classList.add('form-select-sm');
            button.setAttribute('aria-haspopup', 'listbox');
            button.setAttribute('aria-expanded', 'false');
            button.setAttribute('aria-label', select.getAttribute('aria-label') || select.name || 'Seleccionar opción');

            // Ul dropdown-menu
            var menu = document.createElement('ul');
            menu.className = 'dropdown-menu custom-select-menu';
            menu.setAttribute('role', 'listbox');
            menu.style.maxHeight = '220px';
            menu.style.overflowY = 'auto';

            // Sincroniza el botón con el valor del select (selected inicial de Jinja)
            function syncFromSelect() {
                var idx = select.selectedIndex;
                var opt = select.options[idx];
                var text = opt ? opt.textContent.trim() : '';
                // Si no hay selección o es placeholder vacío, mostrar placeholder o primer option
                if (!opt || (opt.value === '' && select.selectedIndex === 0 && select.options.length > 1 && text === '')) {
                    text = opt ? opt.textContent.trim() : 'Seleccionar';
                }
                // Si el texto es vacío (ej. option value="" con texto "Sexo"), usar ese texto
                if (!text) {
                    text = opt ? opt.textContent.trim() : 'Seleccionar';
                }
                button.textContent = text;
                // Limpiar y marcar activo
                var items = menu.querySelectorAll('[role="option"]');
                items.forEach(function (it) {
                    it.classList.remove('active');
                    it.setAttribute('aria-selected', 'false');
                    if (it.dataset.value === select.value) {
                        it.classList.add('active');
                        it.setAttribute('aria-selected', 'true');
                    }
                });
                // Sincronizar is-invalid
                syncInvalid();
            }

            function syncInvalid() {
                var isInvalid = select.classList.contains('is-invalid');
                button.classList.toggle('is-invalid', isInvalid);
                // El invalid-feedback ya existe bajo el select (o su wrapper); no lo movemos, solo aseguramos que se muestre
                // Si el select tiene is-invalid, el feedback debe ser visible (auth-validation.js lo maneja)
            }

            // Construir items por cada option
            Array.prototype.forEach.call(select.options, function (opt) {
                var li = document.createElement('li');
                var a = document.createElement('a');
                a.className = 'dropdown-item';
                a.href = '#';
                a.setAttribute('role', 'option');
                a.setAttribute('data-value', opt.value);
                a.textContent = opt.textContent.trim();
                if (opt.disabled) a.classList.add('disabled');
                // Marcar activo inicial
                if (opt.value === select.value && opt.textContent.trim() === (select.options[select.selectedIndex] ? select.options[select.selectedIndex].textContent.trim() : '')) {
                    // Se marcará luego en syncFromSelect
                }
                a.addEventListener('click', function (e) {
                    e.preventDefault();
                    if (opt.disabled) return;
                    select.value = opt.value;
                    // Disparar change e input para listeners existentes (ej. institucion_id → distrito)
                    select.dispatchEvent(new Event('change', { bubbles: true }));
                    select.dispatchEvent(new Event('input', { bubbles: true }));
                    syncFromSelect();
                    closeMenu();
                    button.focus();
                });
                li.appendChild(a);
                menu.appendChild(li);
            });

            // Insertar wrapper después del select y ocultar select
            select.style.display = 'none';
            select.parentNode.insertBefore(wrapper, select.nextSibling);
            wrapper.appendChild(button);
            wrapper.appendChild(menu);

            // Abrir/cerrar
            var isOpen = false;
            function openMenu() {
                if (isOpen) return;
                // Cerrar otros customs abiertos
                document.querySelectorAll('.custom-select .custom-select-menu.show').forEach(function (m) {
                    m.classList.remove('show');
                    var b = m.previousElementSibling;
                    if (b) b.setAttribute('aria-expanded', 'false');
                });
                menu.classList.add('show');
                button.setAttribute('aria-expanded', 'true');
                isOpen = true;
            }
            function closeMenu() {
                if (!isOpen) return;
                menu.classList.remove('show');
                button.setAttribute('aria-expanded', 'false');
                isOpen = false;
            }
            function toggleMenu() {
                if (isOpen) closeMenu();
                else openMenu();
            }

            button.addEventListener('click', function (e) {
                e.preventDefault();
                toggleMenu();
            });

            // Cerrar al hacer click fuera
            document.addEventListener('click', function (e) {
                if (!wrapper.contains(e.target)) closeMenu();
            });

            // Teclado: Enter/Space abre, Arrow navega, Enter selecciona, Escape cierra
            var focusedIndex = -1;
            function focusItem(idx) {
                var items = Array.prototype.slice.call(menu.querySelectorAll('[role="option"]:not(.disabled)'));
                if (!items.length) return;
                if (idx < 0) idx = items.length - 1;
                if (idx >= items.length) idx = 0;
                focusedIndex = idx;
                items.forEach(function (it, i) {
                    if (i === idx) it.focus();
                    else it.blur();
                });
            }

            button.addEventListener('keydown', function (e) {
                var items = Array.prototype.slice.call(menu.querySelectorAll('[role="option"]:not(.disabled)'));
                if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
                    e.preventDefault();
                    if (!isOpen) openMenu();
                    var dir = e.key === 'ArrowDown' ? 1 : -1;
                    var next = focusedIndex + dir;
                    // Si no hay foco previo, empezar por el seleccionado
                    if (focusedIndex === -1) {
                        var selIdx = -1;
                        items.forEach(function (it, i) {
                            if (it.dataset.value === select.value) selIdx = i;
                        });
                        next = selIdx + dir;
                    }
                    focusItem(next);
                } else if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    if (!isOpen) {
                        openMenu();
                    } else if (focusedIndex >= 0) {
                        var it = menu.querySelectorAll('[role="option"]:not(.disabled)')[focusedIndex];
                        if (it) it.click();
                    }
                } else if (e.key === 'Escape') {
                    e.preventDefault();
                    closeMenu();
                    button.focus();
                }
            });

            // Añadir navegación con teclas dentro del menú
            menu.addEventListener('keydown', function (e) {
                if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
                    e.preventDefault();
                    var dir = e.key === 'ArrowDown' ? 1 : -1;
                    focusItem(focusedIndex + dir);
                } else if (e.key === 'Escape') {
                    e.preventDefault();
                    closeMenu();
                    button.focus();
                } else if (e.key === 'Enter') {
                    e.preventDefault();
                    var items = menu.querySelectorAll('[role="option"]:not(.disabled)');
                    var it = items[focusedIndex];
                    if (it) it.click();
                }
            });

            // Hacer cada item focuseable
            menu.querySelectorAll('[role="option"]').forEach(function (it) {
                it.setAttribute('tabindex', '-1');
            });

            // Sincronizar is-invalid cuando el select cambia de clase (auth-validation.js)
            var observer = new MutationObserver(function () {
                syncInvalid();
            });
            observer.observe(select, { attributes: true, attributeFilter: ['class'] });

            // También sincronizar en change/blur del select nativo
            select.addEventListener('change', syncInvalid);
            select.addEventListener('blur', syncInvalid);

            // Manejar form.reset()
            var form = select.closest('form');
            if (form) {
                form.addEventListener('reset', function () {
                    setTimeout(syncFromSelect, 0);
                });
            }

            // Inicializar texto y estado
            syncFromSelect();
        });
    }

    // Exponer global y auto-inicializar
    window.initCustomSelect = initCustomSelect;
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initCustomSelect);
    } else {
        initCustomSelect();
    }
    // Re-inicializar en caso de contenido dinámico (htmx, etc.)
    document.addEventListener('DOMContentLoaded', initCustomSelect);
})();
