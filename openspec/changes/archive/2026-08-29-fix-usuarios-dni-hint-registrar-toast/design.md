## Context

Ver `proposal.md - Why`. Estado actual: `app/templates/usuarios/crear.html:29` muestra hint `Mínimo 8 caracteres...` bajo contraseña pero no bajo DNI, aunque `usuarios_controller.py:30` hace `username = dni`. En `registro_controller.py:76` se acumulan `errores` y luego `for e in errores: flash(e, 'danger')` genera 3 toasts si se envía vacío (DNI + celular + nombres).

## Goals / Non-Goals

**Goals:**
- Hint de DNI visible sin tocar validación.
- Un solo toast en registrar cuando hay múltiples errores.

**Non-Goals:**
- Cambiar reglas de validación (8 dígitos DNI, 9 celular, etc.).
- Cambiar validación inline de DNI existente (`verificar_dni`).
- Tocar login/recuperar en este paso (va en Paso B).

## Decisions

### 1. Hint bajo DNI reutilizando `password-requirements`
- **Decisión:** En `crear.html:14` debajo del input DNI agregar `<div class="password-requirements">Este DNI será el usuario con el que la persona iniciará sesión</div>` (misma clase que_hint de contraseña) y opcionalmente `small` para consistencia.
- **Rationale:** Reusa estilo existente, no añade CSS nuevo, queda alineado visualmente con el hint de contraseña.
- **Alternativa:** Crear nueva clase `.dni-hint` — rechazada: duplica estilo.

### 2. Colapsar flashes en registrar a uno solo
- **Decisión:** En `registro_controller.py:90` reemplazar `for e in errores: flash(e, 'danger')` por:
  ```python
  if len(errores) == 1: flash(errores[0], 'danger')
  else: flash('Faltan datos por completar. Revisa los campos marcados.', 'danger')
  ```
  Mantener validación específica para `flash` de fecha inválida y otros errores puntuales (siguen con su mensaje único).
- **Rationale:** Genera 1 `mc-toast` en `main.js:347` en vez de 3, sin perder detalle cuando es un solo error; el detalle por campo puede verse luego con validación inline si se añade.
- **Alternativa:** Unir todos con `'; '.join(errores)` en un solo flash — rechazada: mensaje largo, poco legible en toast.

### 3. No tocar backend de correo ni roles
- **Decisión:** Solo cambios en presentación y agregación de mensajes.
- **Rationale:** Mantiene alcance de Paso A mínimo y desacoplado del sonido (Paso B).

## Risks / Trade-offs

- **Mensaje genérico "Faltan datos..." puede ocultar cuál falta** → Mitigación: solo se usa cuando hay ≥2 errores; con 1 error se muestra el específico.
- **Hint de DNI puede confundirse con error** → Mitigación: usar color `#666` como hint de contraseña, no rojo.

## Migration Plan

1. Editar `crear.html` (hint) y `registro_controller.py` (colapso flash).
2. Verificar en 360/1024: hint visible; registrar vacío → 1 toast.
3. `make lint-boundaries` y `pytest tests/test_registro.py tests/test_usuarios.py -q` verdes.
4. Rollback: revertir hint y `for` loop (un commit).

## Open Questions

- ¿El mensaje genérico debe listar los campos faltantes entre paréntesis? Default: no, solo genérico para no alargar toast.
