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

## 6. Verificación de la EMAT sub-regional

La vía de solución más limpia habría sido obtener la EMAT con desagregación
inferior a la región. Se verificó directamente en el Sistema de Información de
Estadísticas en Turismo (SIET) de SERNATUR, que aloja el Reporte Dinámico EMAT.

**La plataforma sí contempla la dimensión “destino turístico”**, con cuatro
destinos para La Araucanía —Araucanía Andina, Araucanía Lacustre, Temuco y
alrededores, y Resto Región— que coinciden en lo esencial con la delimitación
del clúster adoptada en §3.5.2 de la tesis.

Sin embargo, **el propio reporte declara que esa apertura está suspendida**:

> «Desde abril a la fecha existe información que no se puede mostrar debido a
> que la estimación del porcentaje de establecimientos de alojamiento turístico
> que cerró de manera total o parcial alcanzó más del 50 %, por el impacto de
> la crisis sanitaria ocasionada por COVID-19, por lo que se publican los datos
> a nivel nacional y total regional cuando corresponda, **sin incluir apertura
> por clase, residencia y destino turístico**.»
> — Notas del Reporte Dinámico EMAT, SIET/SERNATUR

Esto es consistente con lo observado en los datos: desde 2020 las columnas de
residencia (chilenos/extranjeros) figuran como *N/A*, y la consulta por
cualquiera de los cuatro destinos devuelve la cifra regional agregada.

**Consecuencia:** la apertura por destino existió hasta marzo de 2020, pero
desaparece justo en el período que concentra la información de choque. Incluso
en el mejor escenario se dispondría de tres años y cuatro destinos, frente a
las doce anualidades y trece comunas que requiere el panel. La vía queda
descartada.

*Nota de cautela:* se intentó además extraer los años previos a 2020 mediante
consultas directas al servicio del SIET, pero los resultados fueron
internamente inconsistentes (el agregado regional coincidía exactamente con uno
de los destinos, y la suma de destinos excedía el total). Esas cifras **no se
consideran válidas** y no se emplean en la investigación.

## 7. Aprovechamiento de las fuentes exploradas

El levantamiento realizado para resolver D1 produjo, aunque no la dimensión
buscada, una incorporación de valor: los registros de **visitantes a Áreas
Silvestres Protegidas (SNASPE) de CONAF**, publicados por SIET con cobertura
2012–2024, mensual y por unidad.

Esta fuente **no es válida como ponderador** —Villarrica, segunda comuna en
oferta hotelera, carece de áreas protegidas y recibiría cero actividad, mientras
R.N. Malalcahuello concentra cerca del 60 % de la visitación regional por su
condición de centro de esquí de visitantes de día—, pero **sí cumple los cuatro
criterios de §2 como variable explicativa**: es flujo turístico observado,
comunal, dinámico e independiente del SII (correlaciones de +0,30 con D2 y
+0,31 con D3).

Incorporada al panel como predictor (`visitas_snaspe_pc`), mejora
sustantivamente la capacidad predictiva del modelo:

| Esquema de validación | R² sin CONAF | R² con CONAF | Δ |
|---|---|---|---|
| Temporal | 0,751 | **0,809** | +0,057 |
| Bloques temporales | 0,631 | **0,762** | +0,132 |
| Por comuna | −0,591 | **−0,362** | +0,229 |

Pasa además a ser **la variable de mayor importancia predictiva del modelo**
(0,345 por permutación fuera de muestra, casi el triple de la segunda).

Adicionalmente, permite **calibrar empíricamente la variable CET** de choques
exógenos: la visitación regional cayó a 0,475 de su nivel de 2019 durante 2020,
frente al supuesto declarado de 0,45. La coincidencia respalda ese supuesto,
si bien la recuperación de 2021 diverge (0,948 en CONAF frente a 0,50 en EMAT),
porque el turismo de día al aire libre se normalizó antes que el alojamiento.

## 8. Reproducción

Los ensayos de ponderación son reproducibles con `src/features/diagnostics.py`
sobre el panel `BBDD/final/panel_idec_comunal.csv`, aplicando cada ponderador a
la serie regional EMAT 2017–2024 y evaluando `descomposicion_varianza()` y
`rango_efectivo()`.

Los datos de CONAF se encuentran en `BBDD/processed/conaf_snaspe_araucania.csv`
y su tratamiento en `src/data/conaf.py`, que documenta el mapeo unidad→comuna
y las limitaciones de la fuente.
