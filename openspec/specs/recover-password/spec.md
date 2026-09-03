## Purpose

Alinear la pantalla de recuperar contraseña con el login y mejorar su usabilidad mediante microcopy claro, feedback de carga y éxito, y validación inline reutilizable sin tooltips nativos.

## Requirements

### Requirement: Consistencia visual con login

La tarjeta de recuperar SHALL igualar al login en footer institucional, tamaño de ícono y padding inferior, usando la misma variable CSS para no hardcodear valores distintos.

#### Scenario: Footer institucional presente
- **WHEN** se carga `/auth/recuperar` tras el cambio
- **THEN** debajo de "Volver al Login" aparece el texto `¡Crea, Innova e Inspira!` en cursiva, centrado, con el mismo color y tamaño que en `login.html`.

#### Scenario: Ícono con misma proporción
- **WHEN** se compara el candado de recuperar con el logo del login en viewport 1024px
- **THEN** la altura renderizada del ícono es 55px (±2px) igual que `.auth-logo` y ambos están centrados en `.auth-brand`.

#### Scenario: Padding inferior unificado
- **WHEN** se inspecciona `auth.css` tras el cambio
- **THEN** `login.html` y `recuperar.html` comparten la misma variable/regla para `padding-bottom` del `.card-body` (ej. `0.7rem` o `var(--auth-card-padding-bottom)`) sin valores distintos hardcodeados.

### Requirement: Microcopy de ayuda

La pantalla SHALL explicar qué sucederá tras el envío y por qué se piden dos datos, sin revelar lógica interna de backend.

#### Scenario: Línea de ayuda bajo subtítulo
- **WHEN** se carga `/auth/recuperar`
- **THEN** debajo de "Ingrese sus credenciales para recuperar el acceso" se muestra "Te enviaremos un enlace de recuperación al correo registrado con este DNI." (o texto equivalente ajustado al flujo real).

#### Scenario: Hint bajo campo correo
- **WHEN** el campo correo está visible
- **THEN** debajo del input aparece un texto pequeño "Usamos ambos datos para verificar tu identidad" con color secundario y sin interferir con mensajes de error.

### Requirement: Feedback de estado de envío

El botón y el resultado del envío SHALL comunicar carga, éxito y error genérico sin exponer si el DNI existe.

#### Scenario: Estado de carga
- **WHEN** el usuario hace submit con datos válidos y la petición está en curso
- **THEN** el botón "Enviar Instrucciones" queda `disabled`, muestra spinner y texto "Enviando..." y no permite doble submit.

#### Scenario: Confirmación de éxito
- **WHEN** el backend responde OK (correo enviado o flujo completado)
- **THEN** se muestra mensaje claro "Si los datos son correctos, recibirás un correo con las instrucciones" ya sea como reemplazo del formulario o como alert/toast visible, y el formulario no queda sin cambios — incluso si el envío real falló por SMTP, el mensaje es el mismo.

#### Scenario: Error genérico por seguridad
- **WHEN** DNI o correo no coinciden con ningún usuario, o el correo no pudo enviarse por fallo SMTP
- **THEN** se muestra "Si los datos son correctos, recibirás un correo con las instrucciones" sin indicar cuál campo falló ni exponer error técnico, y la respuesta HTTP no permite distinguir el caso (mismo código y cuerpo genérico).

### Requirement: Validación inline reutilizable sin tooltips nativos

El formulario SHALL usar `novalidate` y validación JS personalizada por campo, con error visual que empuja layout (borde rojo + mensaje con badge "!" debajo), timing `blur`/`submit` para mostrar y `input` para limpiar, y SHALL ser reutilizable para login.

#### Scenario: Error sin overlay
- **WHEN** el usuario envía el formulario vacío o con DNI "123"
- **THEN** aparece borde rojo en el input y debajo un mensaje con badge circular "!" (ej. "● Este campo es requerido" / "El DNI debe tener 8 dígitos") que desplaza el siguiente campo hacia abajo, nunca superpuesto, y el tooltip nativo del navegador no aparece.

#### Scenario: Timing de validación
- **WHEN** el usuario escribe por primera vez en DNI sin haber hecho `blur` ni `submit`
- **THEN** no se muestra error hasta que pierde foco con valor inválido o intenta enviar; si corrige a 8 dígitos, el error desaparece inmediatamente en `input`.

#### Scenario: Reglas específicas
- **WHEN** se valida DNI con valor no vacío
- **THEN** debe tener exactamente 8 dígitos numéricos (`/^\d{8}$/`), de lo contrario mensaje "El DNI debe tener 8 dígitos"; correo requerido y con formato email válido (`type=email` + regex), de lo contrario "Ingresa un correo válido".

#### Scenario: Reutilización en login
- **WHEN** el componente JS se aplica a `login.html` (usuario/contraseña)
- **THEN** usa la misma función sin duplicar código (ej. `initAuthValidation(form, rules)`), manteniendo el mismo estilo de badge y timing.

### Requirement: Paridad visual de restablecer contraseña

La pantalla `reset_password.html` SHALL igualar a `login.html`/`recuperar.html` en identidad visual (mismo `login-card`, `auth.css` con variable `--auth-card-padding-bottom`, tipografía, iconografía Lucide y patrón de validación inline), sin modificar `recuperar.html` ni `auth.css` más allá del cableado mínimo.

#### Scenario: Card y estilos compartidos
- **WHEN** se carga `/auth/reset_password/<token>` tras el cambio
- **THEN** la tarjeta usa `login-card` con `max-width:480px`, mismo `auth.css?v=17`, footer `¡Crea, Innova e Inspira!` y variables CSS compartidas, sin valores hardcodeados distintos a login/recuperar.

#### Scenario: Validación inline reutilizable en reset
- **WHEN** el usuario envía `reset_password` con contraseñas vacías o que no coinciden
- **THEN** aparece borde rojo + badge `!` debajo del campo (mismo componente `initAuthValidation`), sin tooltip nativo, con timing `blur`/`submit` y limpieza en `input`.

#### Scenario: Fortaleza de contraseña visible
- **WHEN** el usuario escribe la nueva contraseña
- **THEN** se muestra indicador de fortaleza (débil/media/buena) con el mismo estilo que en gestión de usuarios, sin duplicar lógica.
