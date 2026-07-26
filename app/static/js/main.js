document.addEventListener('DOMContentLoaded', function() {

    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');
    const html = document.documentElement;

    const savedTheme = localStorage.getItem('theme') || 'light';
    html.setAttribute('data-bs-theme', savedTheme);
    if (themeIcon) {
        themeIcon.className = savedTheme === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-fill';
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = html.getAttribute('data-bs-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            html.setAttribute('data-bs-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            themeIcon.className = newTheme === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-fill';
        });
    }

    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebarBackdrop = document.getElementById('sidebarBackdrop');

    function closeSidebar() {
        if (sidebar) sidebar.classList.remove('show');
        if (sidebarBackdrop) sidebarBackdrop.classList.remove('show');
    }

    function toggleSidebar() {
        if (window.innerWidth < 992) {
            if (sidebar && sidebar.classList.contains('show')) {
                closeSidebar();
            } else {
                if (sidebar) sidebar.classList.add('show');
                if (sidebarBackdrop) sidebarBackdrop.classList.add('show');
            }
        } else {
            sidebar.classList.toggle('collapsed');
            document.querySelector('.main-content').classList.toggle('expanded');
        }
    }

    if (sidebarToggle) { sidebarToggle.addEventListener('click', toggleSidebar); }
    if (sidebarBackdrop) { sidebarBackdrop.addEventListener('click', closeSidebar); }

    if (sidebar) {
        sidebar.querySelectorAll('.nav-link').forEach(function(link) {
            link.addEventListener('click', function() {
                if (window.innerWidth < 992) { closeSidebar(); }
            });
        });
    }

    window.addEventListener('resize', function() {
        if (window.innerWidth >= 992 && sidebarBackdrop) { sidebarBackdrop.classList.remove('show'); }
    });

    const toastContainer = document.getElementById('toastContainer');
    const flashData = document.getElementById('flashData');

    if (flashData && toastContainer) {
        try {
            const messages = JSON.parse(flashData.getAttribute('data-messages'));
            const icons = {
                success: 'bi-check-circle-fill',
                danger: 'bi-exclamation-triangle-fill',
                warning: 'bi-exclamation-circle-fill',
                info: 'bi-info-circle-fill'
            };

            messages.forEach(function(msg) {
                const iconClass = icons[msg.category] || 'bi-bell-fill';
                const toast = document.createElement('div');
                toast.className = 'toast toast-custom show toast-' + msg.category;
                toast.setAttribute('role', 'alert');
                toast.innerHTML = '<div class="toast-body">' +
                    '<span class="toast-icon"><i class="bi ' + iconClass + '"></i></span>' +
                    '<span class="toast-text">' + msg.message + '</span>' +
                    '<button type="button" class="btn-close" data-bs-dismiss="toast"></button>' +
                    '</div>';
                toastContainer.appendChild(toast);

                setTimeout(function() {
                    toast.classList.remove('show');
                    setTimeout(function() { toast.remove(); }, 300);
                }, 5000);
            });
        } catch(e) {}
    }

    document.querySelectorAll('input[pattern]').forEach(function(input) {
        input.addEventListener('input', function() {
            if (this.value.length === parseInt(this.getAttribute('maxlength'))) {
                this.classList.remove('is-invalid');
            }
        });
    });

    document.querySelectorAll('form').forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.disabled) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Procesando...';
            }
        });
    });

    document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(function(el) {
        new bootstrap.Tooltip(el);
    });
});

function confirmDelete(message) {
    return confirm(message || '¿Está seguro de eliminar este registro?');
}
