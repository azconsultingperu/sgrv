/* =============================================================
   main.js  —  SGRV
   ============================================================= */

document.addEventListener('DOMContentLoaded', function () {

    /* --- Reloj en navbar ------------------------------------ */
    try {
        var relojEl = document.getElementById('relojNavbar');
        var relojHora = document.getElementById('relojHora');
        var relojAmPm = document.getElementById('relojAmPm');
        var relojFecha = document.getElementById('relojFecha');
        if (relojEl) {
            function actualizarReloj() {
                var d = new Date();
                var horaStr = '';
                var ampm = '';
                var fechaCorta = '';
                var fechaLarga = '';
                try {
                    var t = d.toLocaleTimeString('es-PE', {hour:'2-digit', minute:'2-digit', second:'2-digit', hour12:true});
                    // Normalizar "02:05:22 p. m." -> "02:05:22 PM"
                    t = t.replace(/\./g, '').replace(/\s+/g, ' ').trim().toUpperCase().replace('P M','PM').replace('A M','AM');
                    var m = t.match(/(.*)\s(AM|PM)$/);
                    if (m) { horaStr = m[1]; ampm = m[2]; } else { horaStr = t; }
                    fechaCorta = d.toLocaleDateString('es-PE', {day:'2-digit', month:'short'}).replace('.','').toLowerCase();
                    fechaLarga = d.toLocaleDateString('es-PE', {weekday:'long', day:'2-digit', month:'long', year:'numeric'});
                    fechaLarga = fechaLarga.charAt(0).toUpperCase() + fechaLarga.slice(1);
                } catch(e) {
                    var pad = function(n){ return String(n).padStart(2,'0'); };
                    var h = d.getHours(); var isPM = h >= 12;
                    var h12 = h % 12 || 12;
                    horaStr = pad(h12) + ':' + pad(d.getMinutes()) + ':' + pad(d.getSeconds());
                    ampm = isPM ? 'PM' : 'AM';
                    var meses = ['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic'];
                    fechaCorta = pad(d.getDate()) + ' ' + meses[d.getMonth()];
                    fechaLarga = pad(d.getDate()) + '/' + pad(d.getMonth()+1) + '/' + d.getFullYear();
                }
                if (relojHora) relojHora.textContent = horaStr;
                if (relojAmPm) relojAmPm.textContent = ampm;
                if (relojFecha) relojFecha.textContent = fechaCorta;
                var title = fechaLarga + ' — ' + horaStr + ' ' + ampm + ' (hora local)';
                relojEl.setAttribute('title', title);
                relojEl.setAttribute('aria-label', title);
            }
            actualizarReloj();
            setInterval(actualizarReloj, 1000);
        }
    } catch (e) {}

    /* --- Tema oscuro/claro ---------------------------------- */
    var themeToggle = document.getElementById('themeToggle');
    var themeIcon   = document.getElementById('themeIcon');
    var html        = document.documentElement;
    var esPaginaAuth = !themeToggle;
    var savedTheme  = esPaginaAuth ? 'light' : (localStorage.getItem('theme') || 'light');
    html.setAttribute('data-bs-theme', savedTheme);
    function updateThemeIcon(theme) {
        var icon = document.getElementById('themeIcon');
        // Lucide reemplaza <i> por <svg>, así que re-query cada vez y maneja ambos casos
        if (!icon) {
            // Si ya fue reemplazado por SVG, buscar el SVG dentro del botón
            var btn = document.getElementById('themeToggle');
            if (btn) icon = btn.querySelector('[data-lucide], svg.lucide');
        }
        var target = document.getElementById('themeIcon') || document.querySelector('#themeToggle [data-lucide], #themeToggle svg');
        if (target) {
            // Si es <i> con data-lucide, actualizar atributo; si es <svg>, reemplazar
            if (target.tagName.toLowerCase() === 'i') {
                target.setAttribute('data-lucide', theme === 'dark' ? 'sun' : 'moon');
            } else {
                // SVG ya renderizado: reemplazar por nuevo <i> y re-crear
                var newIcon = document.createElement('i');
                newIcon.id = 'themeIcon';
                newIcon.setAttribute('data-lucide', theme === 'dark' ? 'sun' : 'moon');
                target.parentNode.replaceChild(newIcon, target);
            }
            if (typeof lucide !== 'undefined' && lucide.createIcons) {
                try { lucide.createIcons(); } catch(e) {}
            }
        }
    }
    updateThemeIcon(savedTheme);
    if (themeToggle) {
        themeToggle.addEventListener('click', function () {
            var cur = html.getAttribute('data-bs-theme');
            var nxt = cur === 'dark' ? 'light' : 'dark';
            html.setAttribute('data-bs-theme', nxt);
            localStorage.setItem('theme', nxt);
            updateThemeIcon(nxt);
            document.dispatchEvent(new CustomEvent('sgrv:themechange', { detail: { theme: nxt } }));
        });
    }

    /* --- Sidebar -------------------------------------------- */
    var sidebar         = document.getElementById('sidebar');
    var sidebarToggle   = document.getElementById('sidebarToggle');
    var sidebarBackdrop = document.getElementById('sidebarBackdrop');
    var movilQuery      = window.matchMedia('(max-width: 991.98px)');

    function lockMainScroll(locked) {
        var mc = document.querySelector('.main-content');
        if (!mc) return;
        if (locked) {
            if (mc._lockWheel) return;
            mc._lockWheel = function (e) { e.preventDefault(); };
            mc._lockTouch = function (e) { e.preventDefault(); };
            mc.addEventListener('wheel', mc._lockWheel, { passive: false });
            mc.addEventListener('touchmove', mc._lockTouch, { passive: false });
        } else {
            if (mc._lockWheel) {
                mc.removeEventListener('wheel', mc._lockWheel);
                mc.removeEventListener('touchmove', mc._lockTouch);
                mc._lockWheel = null;
                mc._lockTouch = null;
            }
        }
    }

    function closeSidebar() {
        if (sidebar)         sidebar.classList.remove('show');
        if (sidebarBackdrop) sidebarBackdrop.classList.remove('show');
        document.body.classList.remove('sidebar-open');
        lockMainScroll(false);
    }
    function toggleSidebar() {
        if (movilQuery.matches) {
            if (sidebar && sidebar.classList.contains('show')) {
                closeSidebar();
            } else {
                // El menú se abre ENCIMA de las notificaciones (z-index en
                // CSS): las notis siguen vivas con su tiempo normal; si
                // vencen mientras el menú está abierto, simplemente
                // desaparecen solas debajo de él.
                if (sidebar)         sidebar.classList.add('show');
                if (sidebarBackdrop) sidebarBackdrop.classList.add('show');
                document.body.classList.add('sidebar-open');
                lockMainScroll(true);
            }
        } else {
            if (sidebar) sidebar.classList.toggle('collapsed');
            var mc = document.querySelector('.main-content');
            if (mc) mc.classList.toggle('expanded');
        }
    }
    if (sidebarToggle)   sidebarToggle.addEventListener('click', toggleSidebar);
    if (sidebarBackdrop) sidebarBackdrop.addEventListener('click', closeSidebar);
    if (sidebar) {
        sidebar.querySelectorAll('.nav-link').forEach(function (link) {
            link.addEventListener('click', function () {
                if (movilQuery.matches) closeSidebar();
            });
        });
    }
    window.addEventListener('resize', function () {
        if (!movilQuery.matches) {
            if (sidebarBackdrop) sidebarBackdrop.classList.remove('show');
            closeSidebar();
        }
    });

    /* --- Avatares: actualización global sin recargar --------- */
    document.addEventListener('avatar-updated', function (e) {
        var d = e.detail || {};
        var buster = '?_=' + Date.now();
        var def = (document.querySelector('meta[name="avatar-default"]') || {}).content || '/static/img/avatar-default.svg';
        var thumbSrc = d.thumbSrc ? d.thumbSrc + buster : null;
        var fullSrc  = d.src ? d.src + buster : null;

        function imgFoto(src, cls, el) {
            var i = document.createElement('img');
            i.src = src;
            i.alt = 'Foto de perfil';
            i.className = cls || 'rounded-circle';
            i.style.cssText = 'object-fit:cover;';
            if (el) {
                i.style.width = el.style.width;
                i.style.height = el.style.height;
                i.setAttribute('data-avatar', '');
                if (el.getAttribute('data-avatar-user')) {
                    i.setAttribute('data-avatar-user', el.getAttribute('data-avatar-user'));
                }
            }
            return i;
        }

        document.querySelectorAll('[data-avatar]').forEach(function (el) {
            if (d.usuarioId && el.getAttribute('data-avatar-user') &&
                String(el.getAttribute('data-avatar-user')) !== String(d.usuarioId)) {
                return;
            }
            var nuevoSrc = thumbSrc || def;
            if (el.tagName === 'IMG') {
                el.src = nuevoSrc;
            } else {
                var n = imgFoto(nuevoSrc, el.className.replace(/d-inline-flex|align-items-center|justify-content-center/g, ''), el);
                el.parentNode.replaceChild(n, el);
            }
        });

        var pv = document.querySelectorAll('[data-avatar-preview]');
        if (pv.length) {
            var nuevoPreview = fullSrc || def;
            pv.forEach(function (p) { p.src = nuevoPreview; });
        }
    });


    /* --- Validación de inputs ------------------------------ */
    document.querySelectorAll('input[pattern]').forEach(function (input) {
        input.addEventListener('input', function () {
            if (this.value.length === parseInt(this.getAttribute('maxlength'))) {
                this.classList.remove('is-invalid');
            }
        });
    });

    document.querySelectorAll('form:not([style*="display:none"])').forEach(function (form) {
        form.addEventListener('submit', function (e) {
            var hasInvalid = form.querySelector('.is-invalid');
            var checkValid = typeof form.checkValidity === 'function' ? form.checkValidity() : true;
            if (hasInvalid || !checkValid) {
                return;
            }
            var btn = this.querySelector('button[type="submit"]');
            if (btn && !btn.disabled) {
                // Guardar HTML original solo si aún no está en estado procesando
                if (btn.dataset.originalHtml === undefined) {
                    btn.dataset.originalHtml = btn.innerHTML;
                }
                console.log('[SGRV] spinner: validación pasó, cambiando botón a Procesando...', form.id || form.action);
                btn.disabled = true;
                btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Procesando...';
                setTimeout(function () {
                    if (btn.disabled) {
                        btn.disabled = false;
                        btn.innerHTML = btn.dataset.originalHtml || original;
                        delete btn.dataset.originalHtml;
                    }
                }, 15000);
            }
        });
    });

    /* --- Tooltips ------------------------------------------ */
    try {
        document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(function (el) {
            new bootstrap.Tooltip(el);
        });
    } catch (e) {}
});


/* =============================================================
   CONFIRM MODAL — motor global
   Uso en cualquier elemento:
     data-confirm
     data-confirm-type="danger|warning|info"
     data-confirm-title="Título"
     data-confirm-message="Mensaje de cuerpo"
     data-confirm-ok="Texto botón confirmar"
     data-confirm-cancel="Texto botón cancelar"
     data-confirm-form="id-del-form-oculto"   ← para enviar POST
   ============================================================= */
(function () {
    /* Inyectar keyframe de sacudida */
    var ks = document.createElement('style');
    ks.textContent =
        '@keyframes confirmShake{' +
        '0%,100%{transform:scale(1) translateX(0)}' +
        '20%{transform:scale(1) translateX(-8px)}' +
        '40%{transform:scale(1) translateX(8px)}' +
        '60%{transform:scale(1) translateX(-5px)}' +
        '80%{transform:scale(1) translateX(5px)}' +
        '}';
    document.head.appendChild(ks);

    /* Construir overlay */
    var overlay = document.createElement('div');
    overlay.id = 'confirmOverlay';
    overlay.className = 'confirm-overlay';
    overlay.innerHTML =
        '<div class="confirm-modal" id="confirmModal" role="dialog" aria-modal="true">' +
            '<div class="confirm-modal-header">' +
                '<div class="confirm-modal-icon danger" id="cIcon"><i data-lucide="triangle-alert" id="cIconI"></i></div>' +
                '<div>' +
                    '<p class="confirm-modal-title" id="cTitle">¿Confirmar acción?</p>' +
                    '<p class="confirm-modal-subtitle" id="cSubtitle">Esta acción requiere confirmación</p>' +
                '</div>' +
            '</div>' +
            '<div class="confirm-modal-body" id="cMessage">¿Estás seguro de que deseas continuar?</div>' +
            '<div class="confirm-modal-footer">' +
                '<button type="button" class="btn btn-confirm-cancel" id="cCancel">Cancelar</button>' +
                '<button type="button" class="btn btn-confirm-ok danger" id="cOk">Confirmar</button>' +
            '</div>' +
        '</div>';
    document.body.appendChild(overlay);
    if (typeof lucide !== 'undefined' && lucide.createIcons) lucide.createIcons();

    var ICONS = {
        danger:  { i: 'triangle-alert', sub: 'Esta acción no se puede deshacer' },
        warning: { i: 'circle-alert',   sub: 'Revisa antes de continuar' },
        info:    { i: 'info',           sub: 'Confirma para continuar' },
        success: { i: 'circle-check',          sub: 'Se ejecutará de inmediato' }
    };

    /* Estado pendiente */
    var _form = null;
    var _href = null;
    var _cb   = null;

    function shake() {
        var m = document.getElementById('confirmModal');
        m.style.animation = 'none';
        m.offsetHeight; // reflow
        m.style.animation = 'confirmShake 0.35s ease';
    }

    function open(opts) {
        var type = opts.type || 'danger';
        var cfg  = ICONS[type] || ICONS.danger;
        document.getElementById('cIcon').className      = 'confirm-modal-icon ' + type;
        var iconEl = document.getElementById('cIconI');
        iconEl.setAttribute('data-lucide', cfg.i);
        if (typeof lucide !== 'undefined' && lucide.createIcons) lucide.createIcons();
        document.getElementById('cTitle').textContent   = opts.title   || '¿Confirmar acción?';
        document.getElementById('cSubtitle').textContent = cfg.sub;
        document.getElementById('cMessage').textContent = opts.message || '¿Estás seguro?';
        document.getElementById('cOk').textContent      = opts.ok     || 'Confirmar';
        document.getElementById('cOk').className        = 'btn btn-confirm-ok ' + type;
        document.getElementById('cCancel').textContent  = opts.cancel  || 'Cancelar';
        _cb = opts.onConfirm || null;
        overlay.classList.add('active');
        document.getElementById('cCancel').focus();
    }

    function close() {
        overlay.classList.remove('active');
        _form = null;
        _href = null;
        _cb = null;
    }

    function execute() {
        overlay.classList.remove('active');
        var f = _form, h = _href, cb = _cb;
        _form = null; _href = null; _cb = null;
        setTimeout(function () {
            if (cb) { cb(); }
            else if (f) { f.submit(); }
            else if (h) { window.location.href = h; }
        }, 150);
    }

    document.getElementById('cCancel').addEventListener('click', close);
    document.getElementById('cOk').addEventListener('click', execute);

    /* Clic fuera → sacudir, no cerrar */
    overlay.addEventListener('click', function (e) {
        if (e.target === overlay) shake();
    });

    /* ESC → sacudir, Enter → confirmar */
    document.addEventListener('keydown', function (e) {
        if (!overlay.classList.contains('active')) return;
        if (e.key === 'Escape') { e.preventDefault(); shake(); }
        if (e.key === 'Enter')  { e.preventDefault(); execute(); }
    });

    /* Delegación global — fase de captura para interceptar antes que Bootstrap */
    document.addEventListener('click', function (e) {
        var trigger = e.target.closest('[data-confirm]');
        if (!trigger) return;
        e.preventDefault();
        e.stopImmediatePropagation();

        _form = null;
        _href = null;

        /* 1. form por ID (data-confirm-form) */
        var fid = trigger.dataset.confirmForm;
        if (fid) _form = document.getElementById(fid);

        /* 2. href del enlace */
        if (!_form) {
            var h = trigger.getAttribute('href');
            if (h && h !== '#') _href = h;
        }

        /* 3. form ancestro (fallback) */
        if (!_form && !_href) {
            var pf = trigger.closest('form');
            if (pf) _form = pf;
        }

        open({
            type:    trigger.dataset.confirmType    || 'danger',
            title:   trigger.dataset.confirmTitle   || '¿Confirmar acción?',
            message: trigger.dataset.confirmMessage || '¿Estás seguro de que deseas continuar?',
            ok:      trigger.dataset.confirmOk      || 'Confirmar',
            cancel:  trigger.dataset.confirmCancel  || 'Cancelar'
        });
    }, true);

    window.showConfirm  = open;
    window.closeConfirm = close;
})();

/* =============================================================
   Sistema de notificaciones estilo "logro desbloqueado"
   (fuera del DOMContentLoaded: el script va al final del body,
   así el contenedor ya existe y la cola es una única instancia)
   ============================================================= */
(function () {
    'use strict';

    var toastContainer = document.getElementById('toastContainer');
    var flashData      = document.getElementById('flashData');

    var TOAST_ICONOS = { success: 'circle-check', error: 'triangle-alert', warning: 'triangle-alert', info: 'info' };
    var TOAST_TITULOS = { success: 'Éxito', error: 'Error', warning: 'Advertencia', info: 'Aviso' };
    var TOAST_DURACION_POR_DEFECTO = { warning: 15000, error: 9000, success: 7000, info: 7000 };
    var TOAST_MAX_VISIBLES = 3;
    // Las categorías de Flask son 'danger' (Bootstrap), no 'error'
    var MAPA_CATEGORIAS = { danger: 'error', error: 'error' };
    var colaToasts = [];
    var toastsVisiblesActuales = 0;

    // Detección de dispositivo: se evalúa UNA sola vez al cargar. Un PC
    // con la ventana encogida NO pasa a modo móvil (y un móvil no vuelve
    // a modo PC al rotar). Combinamos táctil + puntero grueso + user-agent.
    function detectarDispositivoMovil() {
        var tactil = ('ontouchstart' in window) || (navigator.maxTouchPoints || 0) > 0;
        var pointerFino = window.matchMedia && window.matchMedia('(pointer: fine)').matches;
        var agente = /Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent || '');
        return agente || (tactil && !pointerFino);
    }
    document.body.classList.add(detectarDispositivoMovil() ? 'es-movil' : 'es-pc');

    // Alinear toast con la card en páginas de auth (login/recuperar) para que compartan línea superior o centro
    function alinearToastConCard() {
        var card = document.querySelector('.login-card');
        if (!card || !toastContainer) return;
        // Solo en auth (cuando existe .login-card y estamos en esa página)
        var rect = card.getBoundingClientRect();
        // Alinear top del toast con top de la card, con pequeño offset, o centrar verticalmente si el toast es más pequeño
        // Usamos top de la card + 12px de offset para que quede alineado visualmente
        var top = Math.max(12, rect.top + 12);
        // Si el toast es más pequeño que la card, centrar verticalmente puede verse mejor cuando la card es alta
        // Pero para no complicar, alineamos top con card top + 12px
        toastContainer.style.top = top + 'px';
        // Para centrar, alternativa: toastContainer.style.top = (rect.top + rect.height/2 - 40) + 'px';
    }
    // Intentar alinear en carga y en resize, y antes de mostrar cada toast
    if (document.querySelector('.login-card')) {
        alinearToastConCard();
        window.addEventListener('resize', alinearToastConCard);
        // Observar cambios de tamaño de la card (cuando aparecen errores, la card cambia de altura)
        try {
            var ro = new ResizeObserver(alinearToastConCard);
            var cardEl = document.querySelector('.login-card');
            if (cardEl) ro.observe(cardEl);
        } catch (e) {}
    }

    function mostrarToast(tipo, titulo, descripcion, duracionMs) {
        if (!toastContainer || !document.body.contains(toastContainer)) return;
        // Asegurar alineación con la card antes de mostrar
        if (document.querySelector('.login-card')) {
            try { alinearToastConCard(); } catch(e) {}
        }
        tipo = MAPA_CATEGORIAS[tipo] || tipo;
        if (!TOAST_DURACION_POR_DEFECTO[tipo]) tipo = 'info';
        colaToasts.push({ tipo: tipo, titulo: titulo, descripcion: descripcion || '', duracionMs: duracionMs });
        procesarColaToasts();
    }
    window.mostrarToast = mostrarToast;

    function procesarColaToasts() {
        while (toastsVisiblesActuales < TOAST_MAX_VISIBLES && colaToasts.length > 0) {
            crearToast(colaToasts.shift());
        }
    }

    function crearToast(entry) {
        toastsVisiblesActuales++;
        // Sonido según tipo: error para danger/error, éxito para success
        if (entry.tipo === 'error' || entry.tipo === 'success') {
            try {
                var soundFile = entry.tipo === 'success' ? '/static/sounds/success.mp3' : '/static/sounds/error.mp3';
                var audio = new Audio(soundFile);
                audio.volume = entry.tipo === 'success' ? 0.30 : 0.35;
                audio.preload = 'auto';
                if (!window.matchMedia || !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
                    audio.play().catch(function() {});
                }
            } catch (e) {}
        }
        var duracionTotal = entry.duracionMs || TOAST_DURACION_POR_DEFECTO[entry.tipo] || 5000;

        var toast = document.createElement('div');
        toast.className = 'mc-toast ' + entry.tipo;

        var icono = document.createElement('div');
        icono.className = 'mc-toast-icono';
        var iconoI = document.createElement('i');
        iconoI.setAttribute('data-lucide', TOAST_ICONOS[entry.tipo] || 'info');
        icono.appendChild(iconoI);

        var cuerpo = document.createElement('div');
        cuerpo.className = 'mc-toast-cuerpo';
        var titulo = document.createElement('div');
        titulo.className = 'mc-toast-titulo';
        titulo.textContent = entry.titulo;
        cuerpo.appendChild(titulo);
        if (entry.descripcion) {
            var desc = document.createElement('div');
            desc.className = 'mc-toast-descripcion';
            if (entry.descripcion.indexOf('<strong>') !== -1 || entry.descripcion.indexOf('<b>') !== -1) {
                desc.innerHTML = entry.descripcion;
            } else {
                desc.textContent = entry.descripcion;
            }
            cuerpo.appendChild(desc);
        }

        var cerrar = document.createElement('button');
        cerrar.type = 'button';
        cerrar.className = 'mc-toast-cerrar';
        cerrar.setAttribute('aria-label', 'Cerrar notificación');
        cerrar.textContent = '✕';

        var progreso = document.createElement('div');
        progreso.className = 'mc-toast-progreso';
        progreso.style.animationDuration = duracionTotal + 'ms';

        toast.appendChild(icono);
        toast.appendChild(cuerpo);
        toast.appendChild(cerrar);
        toast.appendChild(progreso);

        var temporizador = null;
        var restante = duracionTotal;
        var inicio = 0;
        var cerrado = false;
        var pausado = false;
        var corriendo = false;

        function eliminar() {
            toast.removeEventListener('animationend', onAnimEnd);
            if (!toast.isConnected) return;
            toast.remove();
            toastsVisiblesActuales = Math.max(0, toastsVisiblesActuales - 1);
            procesarColaToasts();
        }

        function onAnimEnd(e) {
            if (e.animationName === 'mcToastOut' || e.animationName === 'mcIslandOut') eliminar();
        }

        function cerrarToast() {
            if (cerrado) return;
            cerrado = true;
            corriendo = false;
            clearTimeout(temporizador);
            toast.classList.add('saliendo');
            setTimeout(eliminar, 350);
            toast.addEventListener('animationend', onAnimEnd);
        }

        function iniciarTemporizador() {
            if (corriendo) return;
            corriendo = true;
            pausado = false;
            inicio = Date.now();
            temporizador = setTimeout(cerrarToast, restante);
            progreso.style.animationPlayState = 'running';
        }

        // Pausa al pasar el cursor (o con el menú abierto): se descuenta el
        // tiempo ya transcurrido, así al reanudar el cierre ocurre
        // exactamente cuando debía. Los flags evitan pausas/reanudaciones
        // duplicadas (p. ej. el cursor cruzando el toast durante su
        // animación de entrada).
        function pausarTemporizador() {
            if (!corriendo || pausado) return;
            pausado = true;
            corriendo = false;
            clearTimeout(temporizador);
            restante -= Date.now() - inicio;
            progreso.style.animationPlayState = 'paused';
        }

        cerrar.addEventListener('click', cerrarToast);
        toast.addEventListener('mouseenter', pausarTemporizador);
        toast.addEventListener('mouseleave', iniciarTemporizador);
        toast._cerrar = cerrarToast;
        toast._pausar = pausarTemporizador;
        toast._reanudar = iniciarTemporizador;

        toastContainer.appendChild(toast);
        // Renderizar ícono Lucide dentro del toast
        if (typeof lucide !== 'undefined' && lucide.createIcons) {
            try { lucide.createIcons({ nodes: [icono] }); } catch(e) { try { lucide.createIcons(); } catch(e2) {} }
        }
        iniciarTemporizador();
    }

    if (flashData) {
        try {
            var messages = JSON.parse(flashData.getAttribute('data-messages') || '[]');
            messages.forEach(function (msg) {
                var category = Array.isArray(msg) ? msg[0] : msg.category;
                var text     = Array.isArray(msg) ? msg[1] : msg.message;
                if (!text) return;
                mostrarToast(category, TOAST_TITULOS[category] || 'Aviso', text);
            });
        } catch (e) {}
    }

    // Pausa/reanuda TODAS las notificaciones. Se usan con el menú lateral:
    // mientras el menú está abierto las notis quedan debajo (z-index menor
    // en CSS) y su tiempo de vida congelado; al cerrar, reanudan donde iban.
    window.pausarToasts = function () {
        Array.prototype.forEach.call(toastContainer.querySelectorAll('.mc-toast'), function (t) {
            if (t._pausar) t._pausar();
        });
    };
    window.reanudarToasts = function () {
        Array.prototype.forEach.call(toastContainer.querySelectorAll('.mc-toast'), function (t) {
            if (t._reanudar) t._reanudar();
        });
    };

    // Inicializar Lucide icons - asegurar que el DOM esté listo
    function initLucide() {
        if (typeof lucide !== 'undefined' && lucide.createIcons) {
            try { lucide.createIcons(); } catch(e) {}
        }
    }
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initLucide);
    } else {
        initLucide();
    }
    // Re-crear al cambiar dinámicamente (htmx, etc.)
    document.addEventListener('DOMContentLoaded', initLucide);
})();
