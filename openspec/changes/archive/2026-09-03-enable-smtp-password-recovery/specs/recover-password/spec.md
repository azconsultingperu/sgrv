## ADDED Requirements

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

## MODIFIED Requirements

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
