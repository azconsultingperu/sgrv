## Purpose

Aclarar en la creación de usuario que el DNI ingresado será el nombre de usuario para iniciar sesión, reduciendo confusión y logins fallidos.

## Requirements

### Requirement: Hint de DNI como usuario

El formulario `usuarios/crear.html` SHALL mostrar bajo el input DNI un texto de ayuda con el mismo estilo que `password-requirements` (ej. `Mínimo 8 caracteres...`) que diga "Este DNI será el usuario con el que la persona iniciará sesión".

#### Scenario: Hint visible al cargar
- **WHEN** se carga `/usuarios/crear` con usuario autenticado admin
- **THEN** bajo el input DNI se ve el texto de ayuda sin necesidad de interactuar, con color secundario y sin empujar el layout de forma superpuesta.

#### Scenario: Hint no interfiere con validación
- **WHEN** el DNI es inválido y aparece el `invalid-feedback` de error
- **THEN** el hint permanece visible arriba del error o se adapta sin tapar el mensaje de error.

### Requirement: Consistencia con login

El hint SHALL usar el mismo tono visual que el login cuando se indique que el usuario es DNI, sin cambiar la validación de 8 dígitos.

#### Scenario: Mensaje coherente entre crear y login
- **WHEN** se compara el hint de crear usuario con el placeholder/label de login que indica "Usuario (DNI)"
- **THEN** ambos comunican la misma idea sin contradicción.
