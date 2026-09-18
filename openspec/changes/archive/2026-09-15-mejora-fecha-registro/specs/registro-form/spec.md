## ADDED Requirements

### Requirement: Fecha con componente híbrido en registro y edición

Los templates `registro/index.html` y `registro/editar.html` SHALL usar el componente `registro-fecha-input` para `fecha_nacimiento` (requerida) y `fecha_visita` (opcional) en lugar de `input type="date"` nativo. SHALL mostrar placeholder `DD/MM/AAAA`, `inputmode="numeric"`, y botón calendario Lucide. El valor visible SHALL ser `DD/MM/AAAA` y el enviado SHALL ser `YYYY-MM-DD`.

#### Scenario: Registro muestra nuevo componente
- **WHEN** se abre `registro/index.html`
- **THEN** `fecha_nacimiento` y `fecha_visita` renderizan input texto con `placeholder="DD/MM/AAAA"` y botón `calendar`, no `type="date"`

#### Scenario: Editar muestra valor convertido
- **WHEN** se abre `registro/editar.html` con `form.fecha_visita="2026-03-15"`
- **THEN** el input muestra `15/03/2026`

#### Scenario: Submit envía ISO
- **WHEN** el usuario envía el form con `15/03/2008` visible
- **THEN** el payload contiene `fecha_nacimiento=2008-03-15`

### Requirement: Validación preservada con nuevo formato

La validación frontend y backend SHALL aceptar el nuevo formato. Si `fecha_nacimiento` está vacía o inválida, SHALL añadir error a `errores` y marcar el input con `is-invalid` igual que antes.

#### Scenario: Vacío bloquea
- **WHEN** se envía `POST /registro/` sin `fecha_nacimiento`
- **THEN** la respuesta es `200` re-render con error "Fecha de nacimiento requerida" y el input con `is-invalid`

