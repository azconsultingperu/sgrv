/**
 * auth-validation.js - Validación inline reutilizable para auth
 * Uso: initAuthValidation(formElement, {
 *   'username': { required: true, pattern: /^\d{8}$/, messagePattern: '...' },
 *   'email': { required: true, type: 'email' }
 * })
 * - Añade novalidate si falta
 * - Crea .invalid-feedback con badge "!" + mensaje bajo el input (empuja layout, sin overlay)
 * - Muestra error en blur si inválido o en submit; limpia en input al corregir
 * - Borde rojo vía .is-invalid
 */
function initAuthValidation(form, rules) {
    if (!form) return null;
    form.setAttribute('novalidate', 'novalidate');

    const fields = {};
    const touched = {};

    function getInput(name) {
        return form.querySelector('[name="' + name + '"]');
    }

    function ensureErrorContainer(input) {
        // Para inputs dentro de .password-field-wrap/.input-group, el contenedor debe ir después del wrapper, no entre input y botón
        const passwordWrap = input.closest('.password-field-wrap');
        const inputGroup = input.closest('.input-group');
        const searchRoot = passwordWrap || inputGroup || input.parentElement;
        let container = searchRoot.querySelector('.invalid-feedback');
        if (!container) {
            const mb = input.closest('.mb-3');
            if (mb) {
                container = mb.querySelector('.invalid-feedback');
            }
        }
        if (!container) {
            container = document.createElement('div');
            container.className = 'invalid-feedback';
            container.style.display = 'none';
            container.style.maxHeight = '0';
            container.style.overflow = 'hidden';
            container.style.marginTop = '4px';
            container.style.fontSize = '0.8rem';
            container.style.color = '#dc3545';
            container.style.visibility = 'hidden';
            container.style.opacity = '0';
            container.style.transition = 'opacity 0.15s ease, visibility 0.15s ease, max-height 0.2s ease';
            container.style.width = '100%';
            container.style.maxWidth = '100%';
            container.style.boxSizing = 'border-box';
            container.style.lineHeight = '1.3';
            if (passwordWrap) {
                passwordWrap.insertAdjacentElement('afterend', container);
            } else if (inputGroup) {
                inputGroup.insertAdjacentElement('afterend', container);
            } else {
                const hint = input.parentElement.querySelector('small.form-text');
                if (hint) {
                    hint.insertAdjacentElement('afterend', container);
                } else if (input.nextSibling) {
                    input.insertAdjacentElement('afterend', container);
                } else {
                    input.parentElement.appendChild(container);
                }
            }
            const mb = input.closest('.mb-3');
            if (mb) {
                mb.style.transition = 'all 0.2s ease';
            }
        }
        return container;
    }

    function showError(input, message) {
        const container = ensureErrorContainer(input);
        container.innerHTML = '<span class="invalid-badge" style="display:inline-flex;align-items:center;justify-content:center;width:16px;height:16px;border-radius:50%;background:#dc3545;color:#fff;font-size:10px;font-weight:700;margin-right:6px;vertical-align:middle;">!</span>' + message;
        container.style.display = 'block';
        void container.offsetHeight;
        container.style.visibility = 'visible';
        container.style.opacity = '1';
        container.style.maxHeight = '40px';
        input.classList.add('is-invalid');
        input.style.borderColor = '#dc3545';
    }

    function clearError(input) {
        const container = ensureErrorContainer(input);
        container.style.visibility = 'hidden';
        container.style.opacity = '0';
        container.style.maxHeight = '0';
        setTimeout(function() {
            if (container.style.visibility === 'hidden') {
                container.innerHTML = '';
                container.style.display = 'none';
            }
        }, 200);
        input.classList.remove('is-invalid');
        input.style.borderColor = '';
    }

    function validateField(name) {
        const rule = rules[name];
        const input = getInput(name);
        if (!input || !rule) return true;
        const value = (input.value || '').trim();
        let message = '';
        if (rule.required && !value) {
            message = rule.messageRequired || 'Este campo es requerido';
        } else if (value && rule.pattern && !rule.pattern.test(value)) {
            message = rule.messagePattern || 'Formato inválido';
        } else if (value && rule.type === 'email') {
            // validación email simple
            const emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRe.test(value)) {
                message = rule.messageEmail || 'Ingresa un correo válido';
            }
        }
        if (message) {
            showError(input, message);
            return false;
        } else {
            clearError(input);
            return true;
        }
    }

    // preparar listeners y reservar espacio para errores desde el inicio
    let formSubmitted = false;
    // Marcar formulario como enviado cuando se hace submit (para validar vacíos en blur después)
    form.addEventListener('submit', function() {
        formSubmitted = true;
    });
    Object.keys(rules).forEach(function(name) {
        const input = getInput(name);
        if (!input) return;
        ensureErrorContainer(input);
        input.addEventListener('blur', function() {
            const value = (input.value || '').trim();
            // No mostrar error en el primer blur si el campo está vacío y aún no se ha intentado enviar
            // Solo validar en blur si hay valor (para patrón/email) o si ya se intentó enviar
            if (value === '' && !formSubmitted) {
                touched[name] = true;
                // No validar vacíos en blur inicial, dejar que el submit lo haga
                return;
            }
            touched[name] = true;
            validateField(name);
        });
        input.addEventListener('input', function() {
            if (touched[name] || input.classList.contains('is-invalid') || formSubmitted) {
                validateField(name);
            }
        });
        // Nunca validar en focus
        input.addEventListener('focus', function() {
            // No hacer nada en focus, solo preparar
        });
    });

    function validateAll() {
        let allValid = true;
        Object.keys(rules).forEach(function(name) {
            touched[name] = true;
            const ok = validateField(name);
            if (!ok) allValid = false;
        });
        return allValid;
    }

    // exponer para submit handler
    return {
        validateAll: validateAll,
        validateField: validateField,
        clearAll: function() {
            Object.keys(rules).forEach(function(name) {
                const input = getInput(name);
                if (input) clearError(input);
            });
        }
    };
}
// exponer global para uso sin módulo
if (typeof window !== 'undefined') {
    window.initAuthValidation = initAuthValidation;
}
