/* fecha-input.js — máscara DD/MM/AAAA + hidden YYYY-MM-DD + calendario ligero a demanda */
(function () {
  function pad(n) { return n < 10 ? '0' + n : '' + n; }
  function isoToDMY(iso) {
    if (!iso) return '';
    var p = iso.split('-');
    if (p.length !== 3) return iso;
    return pad(parseInt(p[2], 10)) + '/' + pad(parseInt(p[1], 10)) + '/' + p[0];
  }
  function dmyToISO(dmy) {
    var m = dmy.match(/^(\d{2})\/(\d{2})\/(\d{4})$/);
    if (!m) return '';
    return m[3] + '-' + m[2] + '-' + m[1];
  }
  function isValidDMY(dmy) {
    var m = dmy.match(/^(\d{2})\/(\d{2})\/(\d{4})$/);
    if (!m) return false;
    var d = parseInt(m[1], 10), mo = parseInt(m[2], 10), y = parseInt(m[3], 10);
    if (y < 1900 || y > 2100) return false;
    if (mo < 1 || mo > 12) return false;
    if (d < 1 || d > 31) return false;
    var dt = new Date(y, mo - 1, d);
    if (dt.getFullYear() !== y || dt.getMonth() !== mo - 1 || dt.getDate() !== d) return false;
    return true;
  }
  function formatMask(digits) {
    digits = digits.replace(/\D/g, '').slice(0, 8);
    var out = '';
    for (var i = 0; i < digits.length; i++) {
      if (i === 2 || i === 4) out += '/';
      out += digits[i];
    }
    return out;
  }
  function normalizePaste(text) {
    var digits = text.replace(/\D/g, '').slice(0, 8);
    return formatMask(digits);
  }

  function initOne(wrap) {
    var visible = wrap.querySelector('[data-fecha-visible]');
    var hidden = wrap.querySelector('[data-fecha-hidden]');
    var btn = wrap.querySelector('[data-fecha-btn]');
    var feedback = wrap.querySelector('[data-fecha-feedback]');
    if (!visible || !hidden) return;

    var maxAttr = visible.getAttribute('data-max') || '';
    var minAttr = visible.getAttribute('data-min') || '';

    function parseISO(iso) {
      if (!iso) return null;
      var p = iso.split('-');
      if (p.length !== 3) return null;
      var d = new Date(parseInt(p[0], 10), parseInt(p[1], 10) - 1, parseInt(p[2], 10));
      return isNaN(d) ? null : d;
    }
    var minDate = parseISO(minAttr);
    var maxDate = parseISO(maxAttr);

    function clampDate(d) {
      if (minDate && d < minDate) return minDate;
      if (maxDate && d > maxDate) return maxDate;
      return d;
    }

    function showError(msg) {
      visible.classList.add('is-invalid');
      if (feedback) { feedback.textContent = msg; feedback.style.display = 'block'; }
      if (btn) btn.classList.add('is-invalid');
    }
    function clearError() {
      visible.classList.remove('is-invalid');
      if (feedback) { feedback.textContent = ''; feedback.style.display = 'none'; }
      if (btn) btn.classList.remove('is-invalid');
    }
    function validateDMY(dmy) {
      if (!dmy) {
        if (visible.hasAttribute('required')) { showError('Fecha requerida.'); return false; }
        clearError(); return true;
      }
      if (!/^\d{2}\/\d{2}\/\d{4}$/.test(dmy)) { showError('Formato DD/MM/AAAA.'); return false; }
      if (!isValidDMY(dmy)) { showError('Fecha inválida.'); return false; }
      var iso = dmyToISO(dmy);
      var dt = parseISO(iso);
      if (dt) {
        if (minDate && dt < minDate) { showError('Fecha fuera de rango.'); return false; }
        if (maxDate && dt > maxDate) { showError('Fecha no puede ser futura.'); return false; }
      }
      clearError(); return true;
    }
    function syncHidden() {
      var v = visible.value.trim();
      if (!v) { hidden.value = ''; return; }
      if (isValidDMY(v) && validateDMY(v)) {
        hidden.value = dmyToISO(v);
      } else {
        // si no es válida aún, no sincronizar; hidden queda vacío hasta que sea válida
        if (/^\d{2}\/\d{2}\/\d{4}$/.test(v) && isValidDMY(v)) hidden.value = dmyToISO(v);
        else if (!v) hidden.value = '';
      }
      // disparar eventos para compatibilidad (edad, etc.)
      var ev = new Event('change', { bubbles: true });
      hidden.dispatchEvent(ev);
      visible.dispatchEvent(new Event('fecha-sync', { bubbles: true }));
    }

    // Inicializar visible desde hidden (rehidratación server-side) — soporta ISO y DD/MM
    if (hidden.value && !visible.value) {
      if (/^\d{4}-\d{2}-\d{2}$/.test(hidden.value)) visible.value = isoToDMY(hidden.value);
      else if (/^\d{2}\/\d{2}\/\d{4}$/.test(hidden.value)) { visible.value = hidden.value; hidden.value = dmyToISO(hidden.value); }
      else if (/^\d{2}-\d{2}-\d{4}$/.test(hidden.value)) { var p = hidden.value.split('-'); var dmy = p[0] + '/' + p[1] + '/' + p[2]; visible.value = dmy; hidden.value = dmyToISO(dmy); }
    } else if (visible.value && /^\d{4}-\d{2}-\d{2}$/.test(visible.value)) {
      var iso2 = visible.value;
      visible.value = isoToDMY(iso2);
      hidden.value = iso2;
    }

    // Máscara en input
    visible.addEventListener('input', function (e) {
      var start = visible.selectionStart;
      var raw = visible.value;
      var digits = raw.replace(/\D/g, '');
      var masked = formatMask(digits);
      if (masked !== raw) {
        visible.value = masked;
        // estimar cursor tras inserción de /
        var newPos = start;
        if (masked.length > raw.length) newPos = start + 1;
        try { visible.setSelectionRange(newPos, newPos); } catch (err) {}
      }
      syncHidden();
    });
    visible.addEventListener('paste', function (e) {
      e.preventDefault();
      var text = (e.clipboardData || window.clipboardData).getData('text') || '';
      var masked = normalizePaste(text);
      visible.value = masked;
      syncHidden();
      validateDMY(masked);
    });
    visible.addEventListener('blur', function () {
      if (visible.value) validateDMY(visible.value);
      else clearError();
      syncHidden();
    });
    // permitir que Enter valide
    visible.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') {
        // dejar submit handling, pero validar visual
        if (visible.value && !validateDMY(visible.value)) {
          // no prevenir submit aquí; validación de form lo hará
        }
      }
    });

    // Calendario ligero
    var overlay = null;
    var viewDate = new Date();
    if (hidden.value) {
      var pd = parseISO(hidden.value);
      if (pd) viewDate = pd;
    } else if (visible.value && isValidDMY(visible.value)) {
      var p2 = parseISO(dmyToISO(visible.value));
      if (p2) viewDate = p2;
    }
    // para max/min defaults: fecha_nacimiento max hoy
    function buildOverlay() {
      if (overlay) return overlay;
      overlay = document.createElement('div');
      overlay.className = 'fecha-overlay';
      overlay.setAttribute('role', 'dialog');
      overlay.setAttribute('aria-label', 'Calendario');
      overlay.style.display = 'none';
      overlay.innerHTML = ''
        + '<div class="fecha-cal-header">'
        + '  <button type="button" class="fecha-nav" data-dir="-1" aria-label="Mes anterior">&#8249;</button>'
        + '  <select class="form-select form-select-sm fecha-month" aria-label="Mes"></select>'
        + '  <select class="form-select form-select-sm fecha-year" aria-label="Año"></select>'
        + '  <button type="button" class="fecha-nav" data-dir="1" aria-label="Mes siguiente">&#8250;</button>'
        + '</div>'
        + '<div class="fecha-weekdays"><span>Lu</span><span>Ma</span><span>Mi</span><span>Ju</span><span>Vi</span><span>Sá</span><span>Do</span></div>'
        + '<div class="fecha-grid"></div>'
        + '<div class="fecha-cal-footer"><button type="button" class="btn btn-sm btn-outline-secondary fecha-today">Hoy</button><button type="button" class="btn btn-sm btn-primary fecha-close">Cerrar</button></div>';
      wrap.appendChild(overlay);

      var monthSel = overlay.querySelector('.fecha-month');
      var months = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'];
      months.forEach(function (m, i) {
        var o = document.createElement('option'); o.value = i; o.textContent = m; monthSel.appendChild(o);
      });
      var yearSel = overlay.querySelector('.fecha-year');
      var yMin = minDate ? minDate.getFullYear() : 1900;
      var yMax = maxDate ? maxDate.getFullYear() : (new Date().getFullYear() + 2);
      for (var y = yMax; y >= yMin; y--) {
        var o2 = document.createElement('option'); o2.value = y; o2.textContent = y; yearSel.appendChild(o2);
      }
      monthSel.addEventListener('change', function () { viewDate.setMonth(parseInt(monthSel.value, 10)); renderGrid(); });
      yearSel.addEventListener('change', function () { viewDate.setFullYear(parseInt(yearSel.value, 10)); renderGrid(); });
      overlay.querySelectorAll('.fecha-nav').forEach(function (b) {
        b.addEventListener('click', function () {
          var dir = parseInt(b.getAttribute('data-dir'), 10);
          viewDate.setMonth(viewDate.getMonth() + dir);
          renderGrid();
        });
      });
      overlay.querySelector('.fecha-today').addEventListener('click', function () {
        var t = new Date(); t = clampDate(t);
        viewDate = new Date(t);
        selectDate(t);
      });
      overlay.querySelector('.fecha-close').addEventListener('click', closeCal);
      overlay.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') { e.preventDefault(); closeCal(); btn.focus(); }
      });
      return overlay;
    }
    function renderGrid() {
      if (!overlay) return;
      var monthSel = overlay.querySelector('.fecha-month');
      var yearSel = overlay.querySelector('.fecha-year');
      // Evitar dispatch que causaba loop infinito: asignar directo sin evento
      monthSel.value = viewDate.getMonth();
      yearSel.value = viewDate.getFullYear();
      var grid = overlay.querySelector('.fecha-grid');
      grid.innerHTML = '';
      var y = viewDate.getFullYear(), m = viewDate.getMonth();
      var first = new Date(y, m, 1);
      var dow = (first.getDay() + 6) % 7; // Lu=0
      var daysInMonth = new Date(y, m + 1, 0).getDate();
      for (var i = 0; i < dow; i++) {
        var cell0 = document.createElement('span'); cell0.className = 'fecha-day muted'; grid.appendChild(cell0);
      }
      var selectedISO = hidden.value || (visible.value && isValidDMY(visible.value) ? dmyToISO(visible.value) : '');
      for (var d2 = 1; d2 <= daysInMonth; d2++) {
        var cell = document.createElement('button');
        cell.type = 'button';
        cell.className = 'fecha-day';
        cell.textContent = d2;
        var dt = new Date(y, m, d2);
        var iso = y + '-' + pad(m + 1) + '-' + pad(d2);
        if (iso === selectedISO) cell.classList.add('selected');
        var today = new Date();
        if (dt.getFullYear() === today.getFullYear() && dt.getMonth() === today.getMonth() && dt.getDate() === today.getDate()) cell.classList.add('today');
        if ((minDate && dt < minDate) || (maxDate && dt > maxDate)) { cell.disabled = true; cell.classList.add('disabled'); }
        (function (yy, mm, dd) {
          cell.addEventListener('click', function () { selectDate(new Date(yy, mm, dd)); });
        })(y, m, d2);
        grid.appendChild(cell);
      }
    }
    function selectDate(dt) {
      dt = clampDate(dt);
      var iso = dt.getFullYear() + '-' + pad(dt.getMonth() + 1) + '-' + pad(dt.getDate());
      visible.value = isoToDMY(iso);
      hidden.value = iso;
      clearError();
      closeCal();
      // disparar change para edad y demás
      hidden.dispatchEvent(new Event('change', { bubbles: true }));
      visible.dispatchEvent(new Event('change', { bubbles: true }));
      visible.dispatchEvent(new Event('input', { bubbles: true }));
    }
    function openCal() {
      buildOverlay();
      // actualizar viewDate desde valor actual
      if (hidden.value) {
        var pd2 = parseISO(hidden.value);
        if (pd2) viewDate = pd2;
      } else if (visible.value && isValidDMY(visible.value)) {
        var p3 = parseISO(dmyToISO(visible.value));
        if (p3) viewDate = p3;
      }
      renderGrid();
      overlay.style.display = 'block';
      // foco accesible
      var sel = overlay.querySelector('.fecha-day.selected') || overlay.querySelector('.fecha-day:not(.disabled)');
      if (sel) sel.focus();
    }
    function closeCal() {
      if (overlay) overlay.style.display = 'none';
    }
    if (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        if (overlay && overlay.style.display === 'block') closeCal(); else openCal();
      });
      btn.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openCal(); }
      });
    }
    document.addEventListener('click', function (e) {
      if (!wrap.contains(e.target) && overlay && overlay.style.display === 'block') closeCal();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && overlay && overlay.style.display === 'block') { closeCal(); }
    });
    // validación en submit del form padre
    var form = wrap.closest('form');
    if (form && !form._fechaBound) {
      form._fechaBound = true;
      form.addEventListener('submit', function (e) {
        var ok = true;
        form.querySelectorAll('[data-fecha-visible]').forEach(function (vis) {
          var w = vis.closest('[data-fecha-wrap]');
          var hid = w ? w.querySelector('[data-fecha-hidden]') : null;
          var v = vis.value.trim();
          if (!v && vis.hasAttribute('required')) {
            vis.classList.add('is-invalid');
            var fb = w ? w.querySelector('[data-fecha-feedback]') : null;
            if (fb) { fb.textContent = 'Fecha requerida.'; fb.style.display = 'block'; }
            ok = false;
          } else if (v && !isValidDMY(v)) {
            vis.classList.add('is-invalid');
            var fb2 = w ? w.querySelector('[data-fecha-feedback]') : null;
            if (fb2) { fb2.textContent = 'Fecha inválida.'; fb2.style.display = 'block'; }
            ok = false;
          } else if (v && isValidDMY(v)) {
            if (hid) hid.value = dmyToISO(v);
          }
        });
        if (!ok) { e.preventDefault(); e.stopPropagation(); }
      });
    }
    // exponer sync inicial
    syncHidden();
  }

  function initAll() {
    document.querySelectorAll('[data-fecha-wrap]').forEach(initOne);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initAll);
  else initAll();

  // API para tests y otros scripts
  window.FechaInput = { isoToDMY: isoToDMY, dmyToISO: dmyToISO, isValidDMY: isValidDMY, formatMask: formatMask };
})();
