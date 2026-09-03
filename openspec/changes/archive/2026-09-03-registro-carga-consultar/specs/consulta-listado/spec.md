## ADDED Requirements

### Requirement: Estado de carga al aterrizar desde registro o eliminación

Cuando `consultar/index.html` se carga inmediatamente después de un `POST /registro/` exitoso (flash `success` "Registro creado exitosamente") o `POST /registro/eliminar` (flash "Registro eliminado"), el sistema SHALL mostrar un overlay de carga grande centrado sobre la tabla (`spinner-border` 48px + texto "Cargando estudiantes...") durante 4500ms, luego ocultar el overlay y disparar el toast `mostrarToast` correspondiente. En visitas normales a `consultar` (sin flash de registro/eliminación) SHALL no mostrar el overlay y cargar la tabla inmediatamente.

#### Scenario: Aterrizaje desde registro muestra carga y luego toast
- **WHEN** el usuario completa `POST /registro/` con datos válidos y es redirigido a `GET /consulta/` con flash `success`
- **THEN** durante ~1s se ve el spinner grande sobre la tabla y al terminar aparece un único toast `success` "Registro creado exitosamente" y la tabla ya contiene el nuevo alumno

#### Scenario: Visita normal sin carga
- **WHEN** el usuario entra a `GET /consulta/` directamente o via sidebar sin flash previo de registro/eliminación
- **THEN** la tabla se renderiza inmediatamente sin spinner y sin delay

#### Scenario: Aterrizaje desde eliminación
- **WHEN** el usuario hace `POST /registro/eliminar/<id>` y es redirigido a `/consulta/` con flash de eliminación
- **THEN** se muestra el mismo overlay 4500ms y luego el toast de eliminación, sin mostrar el registro eliminado

#### Scenario: Duración no es 3 segundos
- **WHEN** se mide el tiempo del overlay en el aterrizaje desde registro
- **THEN** la duración es entre 4500ms (no 3000ms) para no frustrar; el spinner es decorativo con función de feedback, no espera real de datos

#### Scenario: No bloquea interacción permanente
- **WHEN** el overlay termina
- **THEN** la tabla queda interactiva y el spinner no vuelve a aparecer al recargar manualmente sin flash
