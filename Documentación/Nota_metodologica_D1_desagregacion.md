---
tipo: nota metodológica
tema: Dimensión D1 (actividad turística) — intentos de desagregación comunal
proyecto: Tesis Doctoral — Barra Ávila
estado: cerrado con resultado negativo
fecha: 2026-08-08
---

# Nota metodológica — Por qué D1 no se incorporó por desagregación

## 1. El problema

El IDEC contempla cuatro dimensiones. Tres de ellas (D2 empleo, D3 ingresos,
D4 capacidad) se construyen con registros **observados a nivel comunal**. La
cuarta, **D1 — actividad turística** (llegadas, pernoctaciones, ocupación),
depende de la EMAT, que el INE publica únicamente a **nivel regional**.

Los archivos disponibles (`ReporteDinamicoEMAT_2017–2026`) contienen una sola
fila por año: `AGRUPACIÓN = "La Araucanía"`. No existe desglose comunal.

Se evaluó por tanto estimar D1 mediante desagregación:

$$D1_{it} = EMAT_t \times \frac{w_{it}}{\sum_j w_{jt}}$$

La pregunta operativa es **de dónde sale el ponderador $w_{it}$**.

## 2. Criterios que debe cumplir un ponderador válido

| # | Criterio | Razón |
|---|---|---|
| 1 | **Direccionalidad turística** | Debe asignar los flujos a las comunas turísticas, no a las más pobladas |
| 2 | **Variación temporal turística** | Si $w$ es fijo, $D1$ es de rango 1 y el panel degenera (idiosincrasia = 0) |
| 3 | **Independencia del IDEC** | Si $w$ proviene de D2/D3/D4, el índice contaría dos veces la misma información |
| 4 | **Exogeneidad respecto de H1/H2** | Si $w$ proviene de los predictores, los modelos quedan circulares |

## 3. Esquemas evaluados

Se probaron nueve ponderadores sobre el panel 2017–2024 (8 años × 13 comunas),
midiendo la **idiosincrasia** (fracción de la variación temporal propia de cada
comuna; ver `src/features/diagnostics.py`) y la correlación de la D1 resultante
con las dimensiones existentes.

| Ponderador | Idiosincrasia | Rango | corr D3 | Veredicto |
|---|---|---|---|---|
| A — Población | 0,0008 | 8 | +0,19 | ❌ Degenerada |
| B — Capacidad (alojamientos) | 0,0000 | **1** | +0,80 | ❌ Degenerada |
| C — Capacidad × población | 0,0008 | 8 | +0,41 | ❌ Degenerada |
| D — Capacidad × ventas | 0,3967 | 8 | **+0,82** | ⚠️ Doble conteo |
| E — Nº empresas (capacidad dinámica) | 0,0359 | — | +0,54 | ❌ Débil |
| F — Yield (ventas / alojamiento) | 0,2810 | — | **+0,07** | ⚠️ Ver §4 |
| G — Trabajadores | 0,6050 | — | +0,68 | ⚠️ Doble conteo |
| H — Capacidad × trabajadores | 0,5729 | — | +0,83 | ⚠️ Doble conteo |
| I — Capacidad × yield | 0,3744 | — | +0,59 | ⚠️ Redundante* |

\* El esquema I es algebraicamente idéntico a ponderar por ventas:
$n_{aloj} \times (ventas / n_{aloj}) = ventas$. Se conserva en la tabla como
verificación de consistencia del procedimiento.

## 4. El dilema estructural

Los resultados revelan una **tensión que no se resuelve con ingeniería de
variables sobre los datos disponibles**:

- Los ponderadores que satisfacen el criterio 2 (variación turística real)
  provienen todos de la actividad económica registrada por el SII —ventas,
  trabajadores, empresas—, que es exactamente la fuente de D2 y D3. Su
  correlación con D3 oscila entre **+0,54 y +0,83**: la D1 resultante sería, en
  lo esencial, una réplica de la dimensión de ingresos.

- El único esquema con baja correlación (**F**, yield: corr D3 = +0,07) logra su
  ortogonalidad **precisamente porque descarta la información de volumen**. Al
  ser un cociente (ingreso por establecimiento), pondera igual a una comuna con
  un establecimiento muy productivo que a una con noventa. Para repartir un
  agregado de volumen —491.448 llegadas en 2024— eso es sustantivamente
  incorrecto: sobreasigna a comunas pequeñas de alto rendimiento unitario.

- Los ponderadores independientes del IDEC (población, capacidad estática) no
  contienen dinámica turística. La prueba intuitiva: en 2020 las llegadas
  regionales cayeron **−57 %**, pero ninguna población comunal cayó en esa
  magnitud. Un ponderador demográfico no puede distribuir un choque turístico.

**Conclusión:** dentro del conjunto de datos actual, la ortogonalidad respecto
del IDEC y la validez para repartir volumen son **mutuamente excluyentes**. No
es una limitación del método de estimación, sino de la información disponible.

## 5. Decisión adoptada

**No se incorpora D1 por desagregación.** El IDEC mantiene tres dimensiones
observadas y se declara explícitamente como indicador de **desempeño económico
estructural** (§3.8.5 de la tesis).

Esta decisión es coherente con el principio metodológico que rige el estudio
—no imputar lo que puede observarse— y evita introducir en la variable
dependiente una dimensión estimada que, o bien duplicaría información ya
contenida en el índice, o bien carecería de contenido turístico genuino.

El registro de estos ensayos constituye evidencia de que la limitación fue
identificada, cuantificada y resuelta de forma deliberada.

## 6. Vías de resolución (requieren nuevo levantamiento)

Ordenadas por calidad de la solución:

1. **EMAT sub-regional.** Verificar si el Reporte Dinámico del INE permite
   extracción por provincia, comuna o destino turístico. Elimina el problema en
   su origen.
2. **Flujos turísticos observados de fuentes independientes** —visitantes a
   áreas silvestres protegidas, pasos fronterizos, patentes municipales—, que
   cumplen simultáneamente los cuatro criterios de §2 por no provenir del SII.
3. **Reformulación de D1 con indicadores de precio** (ADR, RevPAR) en lugar de
   volumen, lo que atenúa la redundancia con D3 aunque no elimina la necesidad
   de desagregar.

## 7. Reproducción

Los ensayos son reproducibles con `src/features/diagnostics.py` sobre el panel
`BBDD/final/panel_idec_comunal.csv`, aplicando cada ponderador a la serie
regional EMAT 2017–2024 y evaluando `descomposicion_varianza()` y
`rango_efectivo()`.
