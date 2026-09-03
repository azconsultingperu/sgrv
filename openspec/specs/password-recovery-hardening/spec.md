# password-recovery-hardening Specification

## Purpose
Endurecer el flujo de recuperación de contraseña con garantías de seguridad verificables: token de corta vida, un solo uso y throttling, sin exponer existencia de cuentas.

## Requirements

### Requirement: Token de recuperación single-use con TTL de 15 minutos

El sistema SHALL generar tokens de recuperación con expiración de 15 minutos y SHALL invalidarlos tras un uso exitoso, de modo que un enlace no pueda reutilizarse.

#### Scenario: Token expira a los 15 minutos
- **WHEN** se solicita recuperación y luego se abre `/auth/reset_password/<token>` pasados 15 minutos
- **THEN** el sistema rechaza el token y redirige a login con mensaje "El enlace de recuperación es inválido o ha expirado."

#### Scenario: Token no reutilizable tras éxito
- **WHEN** un usuario restablece su contraseña con un token válido y luego reintenta el mismo enlace
- **THEN** el sistema lo rechaza como inválido/ya utilizado y muestra el mismo mensaje genérico de expiración, sin revelar si el usuario existe.

#### Scenario: Token no predecible
- **WHEN** se generan dos tokens para el mismo usuario
- **THEN** ambos son distintos y no derivables entre sí (firmados con `SECRET_KEY` y salt `password-reset`).

### Requirement: Rate limit en solicitud de recuperación

El endpoint `POST /auth/recuperar` SHALL limitar a 3 intentos cada 15 minutos por IP y por DNI, retornando respuesta genérica sin revelar si el límite fue por IP o por cuenta.

#### Scenario: Bloqueo por IP tras 3 intentos
- **WHEN** una misma IP hace 4 solicitudes a `/auth/recuperar` dentro de 15 minutos
- **THEN** la cuarta recibe respuesta con mensaje genérico de throttling (ej. "Has superado el límite de intentos. Intenta en 15 minutos.") y no se envía correo ni se genera token, con código HTTP 429 o 200 genérico según decisión de diseño pero sin filtrar existencia.

#### Scenario: Bloqueo por DNI tras 3 intentos
- **WHEN** se solicita recuperación 4 veces para el mismo DNI dentro de 15 minutos (incluso desde IPs distintas)
- **THEN** el sistema aplica el mismo límite y no envía correo adicional.

#### Scenario: Ventana deslizante se resetea
- **WHEN** pasan 15 minutos desde el primer intento del bloque
- **THEN** un nuevo intento es aceptado nuevamente.

### Requirement: Respuesta siempre genérica ante fallo de SMTP

El sistema SHALL nunca exponer errores técnicos de SMTP al usuario final; SHALL loguear el error en servidor y SHALL responder con el mismo mensaje genérico de éxito aparente.

#### Scenario: SMTP caído no filtra error
- **WHEN** `enviar_correo_recuperacion` falla (timeout, auth, red) durante `POST /auth/recuperar`
- **THEN** el usuario ve "Si los datos son correctos, recibirás un correo con las instrucciones" (mismo que en caso de cuenta inexistente), no un 500 ni "Error al enviar correo", y el servidor registra el fallo en logs.

#### Scenario: Usuario inexistente indistinguible de éxito
- **WHEN** se envía DNI/correo que no coincide con ningún usuario
- **THEN** la respuesta (flash/toast/alert y código HTTP) es idéntica a la de un envío exitoso, sin indicar qué campo falló.
