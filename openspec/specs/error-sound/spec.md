## Purpose

Proveer feedback sonoro de error para notificaciones danger sin duplicar código y respetando políticas de autoplay y preferencias del usuario.

## Requirements

### Requirement: Sonido de error en toast danger

Cuando el sistema muestra un `mc-toast` con `tipo danger`, SHALL reproducir el asset `app/static/sounds/error.mp3` (ahora copiado desde `~/Descargas/creatorshome-error-002-337159.mp3`) con volumen bajo (~0.35) y `preload="auto"`, solo si el gesto de usuario permite `play()` y sin bloquear el toast si el navegador lo rechaza.

#### Scenario: Login fallido con sonido
- **WHEN** el usuario envía login con credenciales inválidas y el backend hace `flash('...incorrectos', 'danger')` y el JS crea `mc-toast danger`
- **THEN** se escucha el nuevo sonido de error una vez con volumen ~0.35 y el toast permanece visible el tiempo normal.

#### Scenario: Navegador bloquea autoplay
- **WHEN** el navegador rechaza `audio.play()` por falta de gesto
- **THEN** el toast se muestra igual sin sonido y sin error en consola.

#### Scenario: Reutilización en registrar y recuperar
- **WHEN** `registrar` muestra su único toast de error o `recuperar` muestra el cartel genérico de error
- **THEN** se usa el mismo asset y la misma función de reproducción sin duplicar código de audio.

### Requirement: Asset estático renombrado

El archivo original en `~/Descargas/creatorshome-error-002-337159.mp3` SHALL copiarse a `app/static/sounds/error.mp3` (sobrescribiendo el anterior) con nombre indicativo y ser servido como estático.

#### Scenario: Ruta accesible
- **WHEN** se carga `/static/sounds/error.mp3` en el navegador
- **THEN** responde 200 con `audio/mpeg` y es cacheable, y su contenido corresponde al nuevo archivo de Creators Home.
