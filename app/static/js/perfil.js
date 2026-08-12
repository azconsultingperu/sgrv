(function () {
    'use strict';

    var btnCambiar = document.getElementById('btnCambiarFoto');
    var btnBorrar  = document.getElementById('btnBorrarFoto');
    var fileInput  = document.getElementById('fileAvatar');
    var wrap       = document.getElementById('avatarPreviewWrap');
    var csrfToken  = document.querySelector('meta[name="csrf-token"]');
    var token      = csrfToken ? csrfToken.getAttribute('content') : '';
    var avatarUrl  = document.querySelector('meta[name="avatar-url"]');
    var avatarEndpoint = avatarUrl ? avatarUrl.getAttribute('content') : '/perfil/avatar';
    var userIdMeta = document.querySelector('meta[name="avatar-user-id"]');
    var userId     = userIdMeta ? userIdMeta.getAttribute('content') : null;
    var defaultMeta = document.querySelector('meta[name="avatar-default"]');
    var defaultAvatar = defaultMeta ? defaultMeta.getAttribute('content') : '/static/img/avatar-default.svg';

    function notificarGlobal(src, thumbSrc) {
        var metaInic = document.querySelector('meta[name="user-iniciales"]');
        var metaColor = document.querySelector('meta[name="user-color"]');
        document.dispatchEvent(new CustomEvent('avatar-updated', {
            detail: {
                usuarioId: userId,
                src: src,
                thumbSrc: thumbSrc,
                iniciales: metaInic ? metaInic.getAttribute('content') : '?',
                color: metaColor ? metaColor.getAttribute('content') : '#2d8a4e'
            }
        }));
    }

    // Notificaciones globales (toast estilo Minecraft); si main.js no
    // cargó, fallback mínimo para que el usuario nunca pierda el feedback.
    function notificar(tipo, texto) {
        if (window.mostrarToast) {
            window.mostrarToast(tipo, tipo === 'success' ? 'Éxito' : 'Error', texto);
        } else if (tipo === 'danger') {
            window.alert('Error: ' + texto);
        }
    }

    function actualizarAvatar(src, thumbSrc) {
        var i = document.createElement('img');
        i.id = 'avatarImg';
        i.src = (src || defaultAvatar) + (src ? '?_=' + Date.now() : '');
        i.alt = 'Foto de perfil';
        wrap.innerHTML = '';
        wrap.appendChild(i);
    }

    if (btnCambiar) {
        btnCambiar.addEventListener('click', function () {
            fileInput.click();
        });
    }

    if (fileInput) {
        fileInput.addEventListener('change', function () {
            var archivo = fileInput.files[0];
            if (!archivo) return;

            if (archivo.size > 10 * 1024 * 1024) {
                notificar('danger', 'La imagen supera los 10 MB de tamaño máximo.');
                fileInput.value = '';
                return;
            }

            var lector = new FileReader();
            lector.onload = function (e) {
                var img = document.createElement('img');
                img.src = e.target.result;
                img.alt = 'Vista previa';
                wrap.innerHTML = '';
                wrap.appendChild(img);
            };
            lector.readAsDataURL(archivo);

            var fd = new FormData();
            fd.append('file', archivo);
            fd.append('csrf_token', token);

            fetch(avatarEndpoint, { method: 'POST', body: fd })
                .then(function (r) { return r.json().then(function (d) { return { ok: r.ok, d: d }; }); })
                .then(function (res) {
                    if (res.ok && res.d.ok) {
                        actualizarAvatar(res.d.src, res.d.thumbSrc);
                        btnBorrar.style.display = '';
                        notificarGlobal(res.d.src, res.d.thumbSrc || null);
                        notificar('success', 'Foto de perfil actualizada correctamente.');
                    } else {
                        notificar('danger', res.d.error || 'Error al subir la imagen.');
                    }
                })
                .catch(function () {
                    notificar('danger', 'Error de conexión al subir la imagen.');
                })
                .finally(function () { fileInput.value = ''; });
        });
    }

    if (btnBorrar) {
        btnBorrar.addEventListener('click', function () {
            fetch(avatarEndpoint, {
                method: 'DELETE',
                headers: { 'X-CSRFToken': token }
            })
                .then(function (r) { return r.json(); })
                .then(function (d) {
                    if (d.ok) {
                        actualizarAvatar(null);
                        btnBorrar.style.display = 'none';
                        notificarGlobal(null, null);
                        notificar('success', 'Foto de perfil eliminada.');
                    }
                });
        });
    }
})();
