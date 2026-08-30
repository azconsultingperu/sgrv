## Purpose

Estandariza la presentación visual de los gráficos de barras del dashboard para que las barras sean delgadas y espaciadas y el tooltip aparezca como burbuja flotante con caret visible, mejorando legibilidad sin cambiar datos.

## ADDED Requirements

### Requirement: Barras delgadas y espaciadas

Los datasets de `chartColegios` y `chartDistritos` SHALL configurar `barPercentage` en 0.5–0.6 y `categoryPercentage` en 0.6–0.7 para que cada barra deje aire lateral y no ocupe todo el ancho de la categoría.

#### Scenario: Barras con aire visible
- **WHEN** el dashboard renderiza "Alumnos por Colegio" con 6 categorías
- **THEN** cada barra mide ~50–60% del ancho de categoría y queda espacio visible entre barras adyacentes (gap ≥ 8px en desktop).

#### Scenario: Consistencia entre ambos gráficos
- **WHEN** se inspecciona `chartDistritos` tras el cambio
- **THEN** usa los mismos `barPercentage` y `categoryPercentage` que `chartColegios`.

### Requirement: Tooltip flotante con caret visible

El tooltip de ambos gráficos SHALL ser una burbuja flotante separada de la barra, con `enabled: true`, `position: 'nearest'`, `yAlign: 'bottom'`, `caretSize: 6–8`, `caretPadding: 8–10`, `padding: 8–10`, `cornerRadius: 6–8`, sombra y fondo con contraste, de modo que la flecha apunte hacia la barra sin taparla.

#### Scenario: Caret visible arriba de la barra
- **WHEN** el usuario hace hover sobre una barra de "Alumnos por Distrito"
- **THEN** el tooltip se dibuja arriba de la barra con caret apuntando hacia abajo hacia el dato, separado por ≥8px, y no superpuesto sobre la barra.

#### Scenario: Burbuja con estilo consistente
- **WHEN** se compara el tooltip de `chartColegios` y `chartDistritos`
- **THEN** ambos comparten mismos `padding`, `cornerRadius`, `caretSize`/`caretPadding` y tipografía alineada a `--text-*`.

### Requirement: Tooltip no cortado en el borde superior

El contenedor o la escala SHALL reservar margen superior para que el tooltip no se recorte cuando la barra está cerca del máximo, vía `layout.padding.top: 12–16` o `scales.y.suggestedMax` con 10–15% de margen extra, o `padding-top` en `.chart-frame`.

#### Scenario: Barra al máximo no recorta tooltip
- **WHEN** "Alumnos por Colegio" tiene una barra con valor igual al máximo de la escala
- **THEN** el tooltip flotante se ve completo dentro del card sin corte contra el borde superior.

#### Scenario: Sin impacto en datos
- **WHEN** se verifica `dashboard_get_alumnos_por_colegio` y `por_distrito`
- **THEN** los valores y labels son idénticos antes y después del cambio (solo config visual).
