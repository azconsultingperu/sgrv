/* =============================================================
   main.js  —  SGRV
   ============================================================= */

document.addEventListener('DOMContentLoaded', function () {

    /* --- Reloj en navbar ------------------------------------ */
    try {
        var relojEl = document.getElementById('relojNavbar');
        if (relojEl) {
            function actualizarReloj() {
                var d = new Date();
                var pad = function (n) { return String(n).padStart(2, '0'); };
                relojEl.textContent =
                    pad(d.getDate()) + '/' + pad(d.getMonth() + 1) + '/' + d.getFullYear() +
                    ' ' + pad(d.getHours()) + ':' + pad(d.getMinutes()) + ':' + pad(d.getSeconds());
            }
            actualizarReloj();
            setInterval(actualizarReloj, 1000);
        }
    } catch (e) {}

    /* --- Tema oscuro/claro ---------------------------------- */
    var themeToggle = document.getElementById('themeToggle');
    var themeIcon   = document.getElementById('themeIcon');
    var html        = document.documentElement;
    var savedTheme  = localStorage.getItem('theme') || 'light';
    html.setAttribute('data-bs-theme', savedTheme);
    if (themeIcon) {
        themeIcon.className = savedTheme === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-fill';
    }
    if (themeToggle) {
        themeToggle.addEventListener('click', function () {
            var cur = html.getAttribute('data-bs-theme');
            var nxt = cur === 'dark' ? 'light' : 'dark';
            html.setAttribute('data-bs-theme', nxt);
            localStorage.setItem('theme', nxt);
            if (themeIcon) themeIcon.className = nxt === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-fill';
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

    /* --- Toasts (flash messages) ---------------------------- */
    var toastContainer = document.getElementById('toastContainer');
    var flashData      = document.getElementById('flashData');
    if (flashData && toastContainer) {
        try {
            var messages = JSON.parse(flashData.getAttribute('data-messages') || '[]');
            var ICONS = {
                success: 'bi-check-circle-fill',
                danger:  'bi-exclamation-triangle-fill',
                warning: 'bi-exclamation-circle-fill',
                info:    'bi-info-circle-fill'
            };
            messages.forEach(function (msg) {
                var category = Array.isArray(msg) ? msg[0] : msg.category;
                var text     = Array.isArray(msg) ? msg[1] : msg.message;
                if (!text) return;
                var iconClass = ICONS[category] || 'bi-bell-fill';
                var toast = document.createElement('div');
                toast.className = 'toast toast-custom show toast-' + category;
                toast.setAttribute('role', 'alert');
                toast.style.pointerEvents = 'auto';
                toast.innerHTML =
                    '<div class="toast-body">' +
                        '<span class="toast-icon"><i class="bi ' + iconClass + '"></i></span>' +
                        '<span class="toast-text">' + text + '</span>' +
                        '<button type="button" class="btn-close" aria-label="Cerrar"></button>' +
                    '</div>';
                toast.querySelector('.btn-close').addEventListener('click', function () {
                    toast.classList.remove('show');
                    setTimeout(function () { toast.remove(); }, 300);
                });
                toastContainer.appendChild(toast);
                setTimeout(function () {
                    toast.classList.remove('show');
                    setTimeout(function () { toast.remove(); }, 300);
                }, 5000);
            });
        } catch (e) {}
    }

    /* --- Validación de inputs ------------------------------ */
    document.querySelectorAll('input[pattern]').forEach(function (input) {
        input.addEventListener('input', function () {
            if (this.value.length === parseInt(this.getAttribute('maxlength'))) {
                this.classList.remove('is-invalid');
            }
        });
    });

    /* --- Spinner en submit de forms (excluye forms ocultos) - */
    document.querySelectorAll('form:not([style*="display:none"])').forEach(function (form) {
        form.addEventListener('submit', function () {
            var btn = this.querySelector('button[type="submit"]');
            if (btn && !btn.disabled) {
                btn.disabled = true;
                btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Procesando...';
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
                '<div class="confirm-modal-icon danger" id="cIcon"><i class="bi bi-exclamation-triangle-fill" id="cIconI"></i></div>' +
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

    var ICONS = {
        danger:  { i: 'bi-exclamation-triangle-fill', sub: 'Esta acción no se puede deshacer' },
        warning: { i: 'bi-exclamation-circle-fill',   sub: 'Revisa antes de continuar' },
        info:    { i: 'bi-info-circle-fill',           sub: 'Confirma para continuar' }
    };

    /* Estado pendiente */
    var _form = null;
    var _href = null;

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
        document.getElementById('cIconI').className     = 'bi ' + cfg.i;
        document.getElementById('cTitle').textContent   = opts.title   || '¿Confirmar acción?';
        document.getElementById('cSubtitle').textContent = cfg.sub;
        document.getElementById('cMessage').textContent = opts.message || '¿Estás seguro?';
        document.getElementById('cOk').textContent      = opts.ok     || 'Confirmar';
        document.getElementById('cOk').className        = 'btn btn-confirm-ok ' + type;
        document.getElementById('cCancel').textContent  = opts.cancel  || 'Cancelar';
        overlay.classList.add('active');
        document.getElementById('cCancel').focus();
    }

    function close() {
        overlay.classList.remove('active');
        _form = null;
        _href = null;
    }

    function execute() {
        overlay.classList.remove('active');
        var f = _form, h = _href;
        _form = null; _href = null;
        setTimeout(function () {
            if (f) { f.submit(); }
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

function confirmDelete(msg) {
    return confirm(msg || '¿Está seguro de eliminar este registro?');
}
