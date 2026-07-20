---
capitulo: III
titulo: Metodología
proyecto: Tesis Doctoral — Barra Ávila
estado: borrador
fecha: 2026-07-20
---

# CAPÍTULO III. METODOLOGÍA

## 3.1 Introducción

Este capítulo describe el diseño metodológico empleado para modelar el desempeño económico del clúster turístico de la Región de La Araucanía mediante técnicas de Machine Learning aplicadas a datos públicos. Se detallan el paradigma y el enfoque de investigación, la unidad de análisis y la delimitación del clúster, las fuentes de información y su tratamiento, la construcción del Índice de Desempeño Económico del Clúster (IDEC) como variable dependiente, y las técnicas de análisis asociadas a cada hipótesis.

Una preocupación transversal organiza todo el capítulo: la **validez del panel comunal**. Buena parte de la información turística oficial se publica a nivel regional, mientras que la unidad de análisis de esta investigación es la comuna. El capítulo hace explícito el criterio metodológico adoptado para no confundir información comunal genuina con la mera réplica territorial de un dato regional, y documenta las pruebas diagnósticas que garantizan esa distinción.

## 3.2 Paradigma de investigación

La investigación se inscribe en el **paradigma positivista**. Se asume la existencia de regularidades empíricas en el comportamiento económico del clúster turístico, susceptibles de ser medidas, modeladas y contrastadas mediante evidencia cuantitativa. El conocimiento se construye a partir de la observación sistemática de registros administrativos oficiales y de la validación estadística de las relaciones postuladas.

## 3.3 Enfoque metodológico

El enfoque es **cuantitativo**, orientado a la medición y a la modelación predictiva. Se combinan técnicas de estadística inferencial con algoritmos de aprendizaje automático supervisado y no supervisado. La estrategia analítica es **explicativo-predictiva**: no sólo busca estimar el desempeño económico del clúster, sino identificar las variables que lo condicionan y los patrones territoriales que lo estructuran.

## 3.4 Diseño de investigación

El diseño es **no experimental, longitudinal y de análisis secundario**. No experimental porque las variables no se manipulan: se observan tal como fueron registradas por las fuentes oficiales. Longitudinal porque el dato se estructura como **panel comuna × año**, lo que permite analizar simultáneamente la variación entre territorios y su evolución en el tiempo. De análisis secundario porque la totalidad de la información proviene de registros administrativos públicos preexistentes.

## 3.5 Población y unidad de análisis

### 3.5.1 Unidad de análisis

La **unidad de análisis es la comuna**, observada anualmente. El panel resultante cubre el período **2013–2024**.

### 3.5.2 Delimitación del clúster turístico

La definición del clúster no se apoya en un umbral arbitrario, sino en un **criterio externo, institucional y verificable**: los **Destinos Turísticos oficiales** que el Servicio Nacional de Turismo (SERNATUR) reconoce en su Registro Nacional de Prestadores de Servicios Turísticos. Este anclaje refuerza la validez de constructo de la delimitación, al hacerla independiente de las decisiones del investigador.

**Núcleo del clúster (8 comunas):**

| Destino SERNATUR | Comunas |
|---|---|
| Pucón y Villarrica | Pucón, Villarrica |
| Araucanía Andina | Curacautín, Lonquimay, Melipeuco |
| Temuco y Lago Budi | Temuco, Nueva Imperial, Carahue |

El núcleo concentra el **83 % de la oferta formal de alojamiento** de la región.

**Anillo del clúster (5 comunas):** Cunco, Victoria, Angol, Saavedra y Vilcún, comunas sin destino oficial pero con oferta formal relevante (≥ 4 alojamientos registrados). El anillo se emplea únicamente en el **análisis de sensibilidad**, para verificar que las conclusiones no dependan de la frontera exacta del clúster.

La codificación comunal sigue el estándar del INE (códigos 9101–9121 y 9201–9211), coincidente con el campo `CMN_CLAVE` del Banco Integrado de Proyectos, lo que permite el enlace directo de las fuentes sin tablas de equivalencia.

## 3.6 Fuentes de información

El principio rector del levantamiento es **no imputar lo que puede observarse**. Cada dimensión del IDEC se construye, en la medida de lo posible, sobre registros comunales observados y no sobre desagregaciones de series regionales.

### 3.6.1 Servicio de Impuestos Internos (SII) — Estadísticas de empresas por comuna y rubro

Fuente central del estudio y única que aporta actividad económica del sector turístico **observada a nivel comuna × año**. Del archivo *Estadísticas de empresas por comuna y rubro económico* se extrae el rubro **I – Actividades de alojamiento y de servicio de comidas**, con cuatro variables por comuna y año: número de empresas, ventas anuales (UF), número de trabajadores dependientes y renta neta informada (UF). Cobertura 2005–2024.

De esta fuente se derivan las dimensiones **D2 (empleo)** y **D3 (ingresos)** del IDEC. Adicionalmente se extraen los rubros conexos al clúster (comercio, transporte, actividades recreativas, inmobiliarias y construcción) como variables explicativas exógenas.

**Limitaciones declaradas de la fuente** (relevantes para la interpretación):

1. **Reserva tributaria (Art. 35 del Código Tributario).** Las celdas construidas con ≤ 10 informantes se publican enmascaradas y se tratan como faltantes estructurales, nunca como ceros. En las 13 comunas del clúster, el rubro turístico no presentó enmascaramiento en el período analizado.
2. **Georreferencia por casa matriz.** La ubicación corresponde al domicilio tributario, no al establecimiento. Una empresa con casa matriz fuera de la región y operación local queda contabilizada en su domicilio. El sesgo se estima acotado, dado el predominio de operadores locales, pero se declara explícitamente.
3. **Rubro replicado 2015–2017.** El SII replica en esos años la actividad económica declarada en 2014; los cambios de rubro en esa ventana no son observables.

### 3.6.2 Banco Integrado de Proyectos (BIP) — Inversión pública

Se procesa el registro histórico nacional filtrando la Región de La Araucanía (`REG_CLAVE = 177`). La inversión anual efectiva por comuna se obtiene **parseando el campo `EBI_EJECUCION_PRESUPUESTARIA`**, que contiene el desglose de ejecución año a año, en lugar de asignar el gasto vigente al año de postulación. Este procedimiento convierte el registro en un flujo de ejecución real por comuna (65.664 registros proyecto-año).

El BIP reporta la ejecución con un **rezago estructural de 2–3 años**. Antes que corregirlo artificialmente, se aprovecha teóricamente: la inversión pública no incide sobre el desempeño turístico el mismo año en que se ejecuta, sino con retardo. Se construyen por tanto variables **rezagadas** (`inversión_lag2`) y de **stock de capital** por inventario perpetuo, $K_t = (1-\delta)K_{t-1} + I_t$ con $\delta = 0{,}05$, que cubren hasta 2024.

### 3.6.3 Instituto Nacional de Estadísticas (INE) — Población

Estimaciones y proyecciones de población comunal (base Censo 2017), 2002–2035, desagregadas por sexo y edad simple. Se emplean la población total y la población en edad laboral (15–64 años) como denominadores de normalización y como covariables de escala.

**Limitación declarada:** el INE ya publicó proyecciones base Censo 2024, pero **sólo a nivel país y región**; no existe aún desagregación comunal para esa base. Las cifras comunales recientes son por tanto proyecciones anteriores al Censo 2024 y deberán contrastarse con los resultados comunales definitivos cuando se publiquen.

### 3.6.4 SERNATUR — Registro de alojamientos

Registro Nacional de Prestadores, del que se obtiene el número y la clase de alojamientos formales por comuna (335 en la región). Aporta la dimensión **D4 (capacidad)**. El registro es un **corte transversal sin fecha de inscripción**, por lo que entrega variación entre comunas pero no a lo largo del tiempo; esta limitación se discute en §3.8.4.

### 3.6.5 Encuesta Mensual de Alojamiento Turístico (EMAT) — pendiente

La EMAT aportaría la dimensión **D1 (actividad turística)**: llegadas, pernoctaciones, tasa de ocupación, ADR y RevPAR. Los reportes actualmente disponibles son anuales y de cobertura regional. La incorporación de D1 requiere el levantamiento de la EMAT en su versión mensual y, de ser posible, comunal. En consecuencia, el IDEC presentado en esta versión integra **tres de las cuatro dimensiones** previstas (§3.8.5).

## 3.7 Variables de investigación

**Variable dependiente:** el IDEC (§3.8).

**Variables independientes** (exógenas al IDEC, para evitar circularidad — §3.10.2):

| Grupo | Variables | Fuente |
|---|---|---|
| Inversión pública | inversión ejecutada rezagada, stock de capital público | BIP |
| Sectores conexos | ventas y trabajadores p.c. de comercio, transporte, recreativas, inmobiliarias, construcción | SII |
| Demografía | población total, población en edad laboral | INE |
| Temporal | año | — |

Todas las variables económicas se expresan **per cápita**, para que sean comparables entre comunas de escala demográfica muy dispar.

## 3.8 Construcción del Índice de Desempeño Económico del Clúster (IDEC)

### 3.8.1 Definición formal

El IDEC agrega indicadores normalizados en dimensiones, y las dimensiones en un índice único de igual ponderación:

$$Z_{kjit} = \frac{f(X_{kjit}) - \min_{kj}}{\max_{kj} - \min_{kj}}, \qquad D_{kit} = \frac{1}{m_k}\sum_{j=1}^{m_k} Z_{kjit}, \qquad IDEC_{it} = \frac{1}{K}\sum_{k=1}^{K} D_{kit}$$

donde $i$ indexa comuna, $t$ año, $k$ dimensión y $j$ indicador dentro de la dimensión; $f(\cdot)$ es la transformación previa (por defecto $\ln(1+x)$).

### 3.8.2 Normalización per cápita

Las variables se normalizan por población **antes** de la agregación. La justificación es sustantiva: en niveles, la comuna de mayor población (Temuco, ~310.000 habitantes) domina cualquier agregado por su sola escala, y el índice mediría demografía en lugar de desempeño. La normalización per cápita convierte el IDEC en una medida de **intensidad** comparable entre territorios.

### 3.8.3 Transformación y método

Las variables económicas comunales presentan fuerte asimetría a la derecha. Un Min-Max sobre valores crudos comprimiría a la mayoría de las comunas cerca de cero y convertiría el índice en un detector de valores extremos. El método por defecto es por tanto **Min-Max logarítmico** ($f(x) = \ln(1+x)$ seguido de reescalado a [0,1]). La normalización se realiza sobre el conjunto completo del panel (*pool* comuna-año), y no dentro de cada año, para preservar la señal temporal del índice.

### 3.8.4 Dimensiones

| Dimensión | Indicadores | Fuente | Estado |
|---|---|---|---|
| **D2 — Empleo sectorial** | trabajadores turísticos p.c. | SII | ✅ Observada |
| **D3 — Generación de ingresos** | ventas p.c., renta p.c. | SII | ✅ Observada |
| **D4 — Capacidad productiva** | alojamientos por 1.000 hab., empresas p.c. | SERNATUR + SII | ✅ Observada |
| **D1 — Actividad turística** | llegadas, pernoctaciones, ocupación | EMAT | ⏳ Pendiente |

D4 es la dimensión más débil temporalmente: el conteo de alojamientos de SERNATUR es un corte transversal, de modo que su variación temporal proviene únicamente del componente de empresas del SII. Esta limitación se supera al obtener el registro SERNATUR con fecha de inscripción.

### 3.8.5 Alcance de la versión vigente

El IDEC presentado integra **D2, D3 y D4**. La ausencia de D1 implica que el índice mide, con rigor, el **desempeño económico estructural** del clúster (empleo, ingresos y capacidad instalada), a la espera de incorporar los **flujos turísticos** propiamente tales. Esta delimitación se declara explícitamente y constituye una línea de trabajo inmediata, no una omisión.

## 3.9 Procedimiento metodológico

El flujo reproducible de construcción del panel es:

1. **Extracción por fuente** — filtrado regional y comunal, normalización de códigos (`src/data/`).
2. **Ingeniería de variables** — rezagos y stock de inversión, per cápita, indicadores de intensidad turística (`src/features/`).
3. **Integración** — ensamblado del panel comuna × año (`src/build_panel.py`).
4. **Diagnóstico de validez** — descomposición de varianza sobre cada variable (§3.11.1).
5. **Construcción del IDEC** — normalización, agregación y análisis de sensibilidad.
6. **Modelación** — supervisada (H1, H2) y no supervisada (H3).

Todo el procesamiento es reproducible mediante `python -m src.build_panel`. Las rutas a los datos crudos se centralizan y no se codifican en los notebooks.

## 3.10 Técnicas de análisis

### 3.10.1 Aprendizaje supervisado (H1, H2)

Se estiman cuatro modelos con papeles diferenciados: **regresión lineal** (base econométrica), **Ridge** (base econométrica regularizada, para una comparación justa ante predictores correlacionados), **árbol de decisión** (relaciones no lineales) y **Random Forest** (interacciones complejas). Se añade una línea base trivial (media) para acotar el piso de desempeño. La importancia relativa de las variables (H1) se estima por **permutación fuera de muestra**, más honesta que la importancia interna del bosque.

### 3.10.2 Control de circularidad

Los predictores excluyen por construcción todos los componentes del IDEC. Utilizar como predictor una variable que forma parte del índice mediría la fórmula del índice, no capacidad predictiva. Un control automático aborta la estimación si algún componente se filtra entre los predictores.

### 3.10.3 Validación

Con datos panel, la validación cruzada aleatoria filtra información entre años contiguos de una misma comuna e infla artificialmente el ajuste. Se implementan y comparan cuatro esquemas:

- **Aleatorio** (K-fold estándar): incluido sólo como control, para exhibir la magnitud del sesgo.
- **Por bloques temporales**: particiones de años contiguos.
- **Temporal** (origen móvil): entrenar en $t \le T$, predecir $t > T$ — mide capacidad de **pronóstico**.
- **Por comuna** (GroupKFold): predecir comunas no vistas — mide **generalización espacial**.

Las métricas reportadas son MAE, RMSE y R².

### 3.10.4 Aprendizaje no supervisado (H3)

Se aplican **K-Means** y **clustering jerárquico** (enlace de Ward). La selección del número de conglomerados combina dos familias de criterios: el **método del codo** sobre la inercia intra-clúster —localizado de forma objetiva por el criterio de máxima distancia a la cuerda (Kneedle), sin lectura visual— y los **índices de silueta y Davies-Bouldin**, que penalizan la falta de separación. La convergencia de ambos criterios en un mismo $k$ se toma como evidencia de una partición defendible.

El análisis se realiza en dos niveles: **comuna** (tipología territorial) y **comuna × año** (regímenes de desempeño y tránsitos entre ellos). Dada la baja cantidad de comunas, la robustez de toda partición se evalúa mediante **remuestreo** (índice de Rand ajustado entre la partición completa y submuestras), y se valida externamente contra los Destinos SERNATUR.

### 3.10.5 Desigualdad territorial

La desigualdad del desempeño se mide con el **índice de Theil**:

$$T_t = \frac{1}{N} \sum_{i=1}^{N} \frac{IDEC_{it}}{\overline{IDEC}_t} \ln \frac{IDEC_{it}}{\overline{IDEC}_t}$$

Su evolución temporal contrasta la hipótesis de convergencia (σ-convergencia). Como prueba complementaria se estima la **β-convergencia**, regresando la tasa de crecimiento del IDEC sobre su nivel inicial.

## 3.11 Validación y robustez

### 3.11.1 Diagnóstico de degeneración del panel

Constituye el aporte metodológico central del capítulo. Desagregar una serie regional $X_t$ mediante un peso comunal fijo $w_i$, $x_{it} = X_t \cdot w_i$, produce una matriz de **rango 1**: no aporta información comunal nueva, y bajo ella el clustering sólo recupera el ranking de pesos y el índice de Theil resulta constante en el tiempo.

Para descartar esta degeneración, cada variable se somete a una **descomposición de varianza** de dos vías (comuna, tiempo e interacción). La métrica de decisión es la **idiosincrasia** —fracción de la variación temporal que es propia de cada comuna y no un movimiento regional común—, invariante a las diferencias de escala entre comunas y exactamente nula bajo una desagregación de rango 1. Una variable con idiosincrasia inferior al 2 % se considera degenerada y no se incorpora al modelo.

La prueba, aplicada a un contraejemplo deliberado (una serie regional de la EMAT multiplicada por un peso fijo), arroja idiosincrasia 0,000, rango 1 y un índice de Theil constante hasta el sexto decimal, confirmando su capacidad de detección. Las variables efectivamente utilizadas (inversión ejecutada, renta, trabajadores) superan holgadamente el umbral.

### 3.11.2 Robustez del IDEC

Se contrasta la sensibilidad del índice a cuatro métodos de normalización (Min-Max, Min-Max logarítmico, Z-score y rango percentil). La métrica es la correlación de Spearman entre los ordenamientos comunales resultantes: correlaciones altas indican que las conclusiones no dependen de la elección metodológica.

### 3.11.3 Robustez del clúster

El modelo principal se estima sobre el núcleo de 8 comunas y se replica sobre el conjunto extendido de 13, verificando la estabilidad de los hallazgos ante la frontera del clúster.

## 3.12 Consideraciones éticas

El estudio utiliza **exclusivamente datos públicos** provenientes de registros administrativos oficiales, sin información personal sensible. Se respeta la reserva tributaria establecida en el Artículo 35 del Código Tributario: las cifras del SII construidas con diez o menos informantes se publican agregadas o enmascaradas, y en este estudio se tratan como faltantes, nunca como valores nulos. La totalidad del procedimiento es reproducible a partir de código documentado y fuentes de acceso abierto, en línea con los principios de transparencia y datos abiertos del Estado de Chile.
