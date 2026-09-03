## Purpose

Unificar los íconos de toda la interfaz del SGRV con Lucide para lograr trazos más finos, consistentes y modernos, reemplazando los actuales de Bootstrap Icons.

## Requirements

### Requirement: Íconos Lucide en toda la UI

La interfaz SHALL renderizar íconos Lucide en lugar de Bootstrap Icons en todas las vistas (base, sidebar, navbar, dashboard, registro, consulta, usuarios, auditoría, perfil y auth), manteniendo el mismo significado semántico y tamaño relativo.

#### Scenario: Dashboard con Lucide
- **WHEN** se carga `/dashboard` tras el cambio
- **THEN** los íconos de `stat-icon` y `kpi-band` son Lucide (ej. `gauge`, `school`, `users`) y no `bi-*`, visibles con el mismo color y tamaño que antes.

#### Scenario: Formularios y navegación con Lucide
- **WHEN** se navega a `/registro`, `/consulta` o `/usuarios`
- **THEN** los íconos de títulos, botones y sidebar son Lucide y conservan el alineamiento y spacing previo.

### Requirement: Carga y fallback de íconos

El sistema SHALL cargar Lucide vía CDN o bundle y SHALL inicializar los íconos con `createIcons` tras cada render, sin dejar `bi-*` huérfanos.

#### Scenario: Sin Bootstrap Icons
- **WHEN** se inspecciona el HTML renderizado tras el cambio
- **THEN** no existe ningún `link` a `bootstrap-icons@1.11.2` ni clase `bi-*` en el DOM.

#### Scenario: Inicialización automática
- **WHEN** se cambia de página sin recarga completa (navegación interna)
- **THEN** los nuevos `data-lucide` se convierten a SVG sin necesidad de recargar manualmente.
