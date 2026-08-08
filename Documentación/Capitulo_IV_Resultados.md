---
capitulo: IV
titulo: Análisis de Resultados
proyecto: Tesis Doctoral — Barra Ávila
estado: borrador
fecha: 2026-07-20
---

# CAPÍTULO IV. ANÁLISIS DE RESULTADOS

## 4.1 Introducción

Este capítulo presenta los resultados obtenidos a partir del panel comunal integrado para el período 2013–2024 (156 observaciones correspondientes a 13 comunas). Se organiza en cinco secciones: la caracterización del panel y la validación de su condición no degenerada (§4.2), la construcción y validación del IDEC (§4.3), y el contraste de las tres hipótesis de investigación — relaciones entre variables (H1, §4.4), capacidad predictiva (H2, §4.5) y agrupamientos y desigualdad territorial (H3, §4.6). El capítulo cierra con una síntesis de hallazgos y sus limitaciones (§4.7).

## 4.2 El panel comunal y su validez

### 4.2.1 Descripción

El panel integra cinco fuentes administrativas a nivel comuna × año: actividad económica del rubro turístico (SII), inversión pública ejecutada (BIP), población (INE), capacidad de alojamiento (SERNATUR) y visitación a áreas silvestres protegidas (CONAF). El panel es **balanceado y completo** en las variables clave (156 de 156 observaciones), sin recurrir a imputación.

La incorporación de la visitación a áreas protegidas merece una nota. Es la única fuente del estudio que registra **flujos turísticos observados a escala sub-regional**, y su independencia respecto del SII —correlaciones de +0,30 con D2 y +0,31 con D3— permite emplearla como variable explicativa sin introducir circularidad. Su exploración se originó en la búsqueda de una vía para construir la dimensión D1; aunque no resultó válida para ese fin (§4.3.1), demostró ser el predictor más relevante del modelo (§4.4).

### 4.2.2 Validación de la no degeneración

Antes de cualquier modelación se verificó que el panel contiene información comunal genuina y no una réplica de series regionales. La descomposición de varianza (Tabla 4.1) reporta, para cada variable, la **idiosincrasia**: la fracción de la variación temporal atribuible a la dinámica propia de cada comuna.

**Tabla 4.1 — Diagnóstico de degeneración de las variables del panel**

| Variable | Idiosincrasia comuna×tiempo | Veredicto |
|---|---|---|
| Inversión pública ejecutada (BIP) | 0,918 | Válida |
| Renta neta p.c. (SII) | 0,785 | Válida |
| Trabajadores p.c. (SII) | 0,779 | Válida |
| Ventas p.c. (SII) | 0,297 | Válida |
| *EMAT regional × peso fijo (contraejemplo)* | *0,000* | *Degenerada (rango 1)* |

El contraejemplo —una serie regional desagregada mediante un peso comunal fijo— arroja idiosincrasia nula, matriz de rango 1 e índice de Theil constante en todos los años, confirmando la capacidad diagnóstica de la prueba. Las variables efectivamente empleadas superan el umbral con holgura, lo que acredita que el panel comunal es sustantivo.

### 4.2.3 El efecto de la normalización per cápita

La Tabla 4.2 ilustra por qué la normalización por población es una decisión metodológica sustantiva y no cosmética. Ordenar las comunas por ventas del rubro turístico en niveles frente a per cápita reordena por completo el ranking.

**Tabla 4.2 — Ranking comunal por ventas turísticas, 2024: niveles vs. per cápita**

| Comuna | Rango (niveles) | Rango (per cápita) | Salto | Alojamientos/1.000 hab. |
|---|---|---|---|---|
| Pucón | 2 | **1** | ▲1 | 3,06 |
| Curacautín | 4 | 2 | ▲2 | 1,92 |
| Villarrica | 3 | 3 | – | 1,45 |
| Temuco | **1** | **4** | ▼3 | 0,12 |
| Melipeuco | 11 | 5 | ▲6 | 1,42 |
| Nueva Imperial | 7 | 12 | ▼5 | 0,09 |

En niveles, Temuco encabeza por su sola escala demográfica (~310.000 habitantes). Al normalizar, desciende al cuarto lugar y las comunas de vocación turística ascienden. La coincidencia del ordenamiento per cápita con la intensidad de oferta formal (alojamientos por 1.000 habitantes), proveniente de una fuente independiente, valida externamente la normalización.

## 4.3 Construcción del IDEC

### 4.3.1 Composición

El IDEC vigente integra tres dimensiones observadas —empleo (D2), ingresos (D3) y capacidad (D4)— con igual ponderación, de modo que el índice mide, con precisión, el **desempeño económico estructural** del clúster.

La dimensión de actividad turística (D1) no se incorpora. Se evaluaron nueve esquemas de desagregación de la serie regional EMAT y se verificó adicionalmente la disponibilidad de aperturas sub-regionales en la fuente original; ninguna vía resultó válida. El resultado es concluyente y se documenta por separado en la nota metodológica correspondiente:

- Los ponderadores con dinámica turística genuina provienen del SII, la misma fuente de D2 y D3, con correlaciones de +0,54 a +0,83 que implicarían **doble conteo**.
- Los ponderadores independientes del índice —población, capacidad instalada— carecen de contenido turístico: en 2020 las llegadas regionales cayeron 57 % y ninguna población comunal lo hizo.
- La visitación a áreas protegidas (CONAF), pese a ser flujo turístico observado, tiene **cobertura estructuralmente incompleta**: Villarrica, segunda comuna en oferta hotelera con 88 establecimientos, carece de áreas protegidas y recibiría actividad nula.
- La EMAT sí contempla una apertura por destino turístico —con cuatro destinos para La Araucanía que coinciden en lo esencial con la delimitación del clúster—, pero la fuente declara que dicha apertura está **suspendida desde abril de 2020** por el cierre de más del 50 % de los establecimientos durante la pandemia, es decir, precisamente en el período que concentra la información de choque.

La ausencia de D1 no constituye, por tanto, una omisión, sino una **limitación de la información pública disponible identificada, cuantificada y declarada**.

### 4.3.2 Robustez al método de normalización

El ordenamiento comunal que produce el IDEC es estable ante la elección del método de normalización. La correlación de Spearman entre los índices construidos con Min-Max, Min-Max logarítmico, Z-score y rango percentil se sitúa entre **0,92 y 1,00**. Las conclusiones sobre qué comunas rinden mejor no dependen, por tanto, de la decisión metodológica.

### 4.3.3 El IDEC como panel válido

El propio IDEC supera el diagnóstico de degeneración (idiosincrasia 0,343), lo que confirma que hereda la variación comuna×tiempo de sus componentes y constituye una variable dependiente legítima para la modelación.

## 4.4 Contraste de H1 — Relaciones entre variables y el desempeño

> **H1.** Las variables económicas y territoriales de fuentes públicas presentan una relación estadísticamente significativa, potencialmente no lineal, con el IDEC.

La relación se estima mediante la importancia por permutación fuera de muestra de un modelo Random Forest, evaluada sobre particiones donde el modelo efectivamente predice (R² = 0,68). Los predictores son exógenos al IDEC (§3.10.2).

**Tabla 4.3 — Importancia de variables (permutación fuera de muestra)**

| Variable | Importancia | Desv. |
|---|---|---|
| **Visitación áreas protegidas p.c.** | **0,345** | 0,057 |
| Ventas construcción p.c. | 0,123 | 0,035 |
| Trabajadores recreativas p.c. | 0,070 | 0,031 |
| Ventas inmobiliarias p.c. | 0,067 | 0,014 |
| Ventas recreativas p.c. | 0,050 | 0,022 |
| Trabajadores comercio p.c. | 0,045 | 0,013 |
| Población | 0,043 | 0,006 |
| Población en edad laboral | 0,039 | 0,009 |
| Ventas comercio p.c. | 0,031 | 0,010 |
| Ventas transporte p.c. | 0,031 | 0,005 |

**Hallazgos.**

1. **La demanda turística observada domina.** La visitación a áreas silvestres protegidas es, con holgura, la variable de mayor capacidad explicativa: su importancia (0,345) casi triplica la de la segunda. El resultado es teóricamente esperable —es la única variable que mide directamente afluencia de visitantes, y no un proxy económico— y refuerza la validez del IDEC como medida de desempeño del clúster, puesto que un índice construido íntegramente con registros tributarios resulta predicho por un registro de flujos físicos completamente independiente.

2. **Construcción e inmobiliarias siguen siendo relevantes.** En conjunto suman 0,190 y ocupan el segundo bloque de importancia. Es coherente con la naturaleza del clúster: en Pucón y Villarrica el mercado de segunda vivienda y alojamiento turístico constituye un motor económico, y la actividad inmobiliaria y constructora es su rastro medible.

3. **La inversión pública no muestra señal predictiva detectable.** Su importancia es prácticamente nula. Este resultado debe leerse con cautela (§4.7): el BIP mide *toda* la inversión pública —vialidad, educación, saneamiento—, no la específicamente turística; la estructura de rezagos podría diferir; y con 13 comunas la potencia estadística es limitada. La lectura rigurosa es "no se detecta relación", no "no existe relación".

**Conclusión.** H1 se **sostiene**: se confirman relaciones significativas y no lineales entre el entorno económico y territorial comunal y el IDEC, con una jerarquía de variables interpretable en términos de la teoría de clústeres.

## 4.5 Contraste de H2 — Capacidad predictiva

> **H2.** Los modelos de aprendizaje supervisado estiman el IDEC con niveles de error predictivo aceptables, superiores a los enfoques tradicionales.

La Tabla 4.4 reporta el R² de cada modelo bajo los cuatro esquemas de validación.

**Tabla 4.4 — R² por modelo y esquema de validación**

| Modelo | Aleatorio* | Bloques | Temporal | Por comuna |
|---|---|---|---|---|
| Media (base) | −0,01 | −0,01 | −0,02 | −0,28 |
| Regresión lineal | 0,56 | 0,53 | 0,05 | −11,86 |
| Ridge (regularizada) | 0,48 | 0,32 | 0,24 | −2,94 |
| Árbol de decisión | 0,55 | 0,56 | 0,33 | −1,35 |
| **Random Forest** | **0,80** | **0,76** | **0,81** | **−0,36** |

\* Esquema aleatorio incluido sólo como control del sesgo por fuga temporal.

**Hallazgos.**

1. **Superioridad del Machine Learning ante una línea base competente.** Random Forest alcanza R² = 0,81 en validación temporal, frente a 0,24 de la regresión Ridge y 0,05 de la regresión lineal: más del triple del mejor contendiente econométrico. La comparación es exigente en dos sentidos. Primero, se incorporó una regresión Ridge con parámetro de regularización validado, precisamente para dotar al enfoque tradicional de su mejor versión ante predictores correlacionados. Segundo, y a diferencia de especificaciones preliminares en que los modelos lineales arrojaban ajustes negativos, aquí **alcanzan desempeños positivos y razonables** en los esquemas aleatorio y de bloques. La superioridad del ML se establece, por tanto, frente a alternativas que funcionan, y no frente a modelos mal especificados.

2. **La ventaja del ML se concentra donde la relación es no lineal.** La brecha entre Random Forest y los modelos lineales es moderada bajo validación aleatoria (0,80 frente a 0,56) y máxima bajo validación temporal (0,81 frente a 0,05). Es decir: cuando se exige extrapolar a años no observados —el uso efectivamente relevante para la decisión territorial—, los modelos lineales pierden casi toda su capacidad, mientras el bosque la conserva. Esto respalda directamente H1: la estructura del fenómeno es no lineal.

3. **La vulnerabilidad es espacial, no temporal.** El esquema aleatorio (0,80) y el de bloques temporales (0,76) arrojan resultados similares, lo que indica que la fuga temporal es modesta. En cambio, todos los modelos fallan al predecir una **comuna no vista** en entrenamiento (Random Forest: R² = −0,36). Con sólo 13 unidades y un IDEC dominado por efectos fijos comunales, no hay suficientes territorios para aprender una relación transferible entre comunas. Cabe notar que la incorporación de la visitación a áreas protegidas mejoró este esquema de −0,59 a −0,36, la mayor ganancia de las tres validaciones, lo que sugiere que el límite es de información territorial disponible antes que de método.

4. **Reformulación del alcance de H2.** En consecuencia, H2 se sostiene específicamente como hipótesis de **predicción temporal** (pronóstico del IDEC de años futuros), no de generalización espacial. Esta delimitación es coherente con el propósito declarado del estudio —anticipar la evolución del clúster para la toma de decisiones— y se declara explícitamente antes que ocultarse tras un ajuste inflado por fuga metodológica.

**Conclusión.** H2 se **sostiene con alcance acotado**: los modelos de ML estiman el IDEC con error bajo (MAE = 0,059) y superan netamente a los enfoques tradicionales en el horizonte temporal.

## 4.6 Contraste de H3 — Agrupamientos y desigualdad territorial

> **H3.** Las técnicas no supervisadas identifican agrupamientos territoriales diferenciados, y existe una estructura de desigualdad territorial dentro del clúster.

### 4.6.1 Desigualdad territorial: evidencia de convergencia

El índice de Theil del IDEC (Tabla 4.5) desciende de **0,537 en 2013 a 0,250 en 2024**, una caída del **53,5 %**, con tendencia estadísticamente significativa (pendiente −0,028 anual; *p* < 10⁻⁶; R² = 0,91). La caída es robusta: se mantiene entre −46 % y −67 % según el método de normalización, y persiste incluso sobre la variable económica cruda (*p* < 0,0001), descartando que sea un artefacto de la construcción del índice.

**Tabla 4.5 — Índice de Theil del IDEC (selección de años)**

| Año | 2013 | 2016 | 2019 | 2022 | 2024 |
|---|---|---|---|---|---|
| Theil | 0,537 | 0,432 | 0,306 | 0,265 | 0,250 |

Esta σ-convergencia se confirma mediante **β-convergencia**: la regresión de la tasa de crecimiento del IDEC sobre su nivel inicial arroja β = **−0,033** (*p* = 0,0002; R² = 0,73), equivalente a una velocidad de convergencia de ≈ 4 % anual (vida media ≈ 17 años). La coincidencia de ambas pruebas —dispersión decreciente y crecimiento más rápido de las rezagadas— descarta la falacia de Galton y hace del hallazgo un resultado defendible.

**Mecanismo.** La convergencia no obedece a un deterioro de Pucón, sino al **alcance de los destinos de la Araucanía Andina** (Tabla 4.6). Curacautín, Melipeuco y Lonquimay más que duplican su IDEC en el período, mientras Pucón es la única comuna que retrocede levemente.

**Tabla 4.6 — Variación del IDEC 2013–2024 (comunas seleccionadas)**

| Comuna | IDEC 2013 | IDEC 2024 | Variación |
|---|---|---|---|
| Curacautín | 0,196 | 0,459 | +134 % |
| Melipeuco | 0,162 | 0,342 | +111 % |
| Lonquimay | 0,104 | 0,216 | +108 % |
| Villarrica | 0,272 | 0,384 | +41 % |
| Temuco | 0,156 | 0,214 | +37 % |
| Pucón | 0,805 | 0,783 | −3 % |

### 4.6.2 Agrupamientos: regímenes de desempeño

La tipología puramente comunal (13 unidades) resultó **frágil**: todas las particiones aíslan a Pucón como conglomerado unitario y no concuerdan con los Destinos SERNATUR (ARI ≈ 0,03–0,21). Esta fragilidad es una limitación del número de unidades y se declara como tal.

El análisis a nivel **comuna × año** (156 observaciones) es, en cambio, robusto. Los criterios de selección convergen: el método del codo y el de silueta coinciden en **k = 4** (clustering jerárquico), y la partición es estable ante remuestreo (ARI = 0,79). Emergen cuatro regímenes de desempeño nítidamente diferenciados (Tabla 4.7).

**Tabla 4.7 — Regímenes de desempeño del clúster (k = 4)**

| Régimen | n | Perfil característico | Comunas representativas |
|---|---|---|---|
| **Enclave turístico** | 12 | Intensidad turística muy alta en todas las dimensiones | Pucón |
| **Centro urbano de servicios** | 12 | Población alta, intensidad turística baja (−0,86) | Temuco |
| **Turístico emergente** | 45 | Intensidad media-alta, en ascenso | Villarrica, Curacautín |
| **Periferia** | 83 | Bajo la media | resto |

El resultado sustantivo es que **k = 4 separa a Temuco de Pucón**, distinción que agrupamientos más gruesos confunden por escala. Temuco se revela como un centro urbano de servicios —mucha población, baja intensidad turística— y no como un destino, tal como sugería su composición sectorial. Esta es precisamente la clase de diferenciación cualitativa que H3 debía descubrir.

**Tránsitos entre regímenes.** Cuatro comunas cambian de régimen durante el período —Angol, Cunco, Curacautín y Victoria—, **todas en sentido ascendente**; ninguna desciende. Curacautín asciende en 2021, coincidiendo con el resultado de convergencia. El régimen de enclave (Pucón) se comporta como estado absorbente. El clúster exhibe así una estructura persistente con movilidad ascendente en los bordes, plenamente coherente con la convergencia documentada en §4.6.1.

**Conclusión.** H3 se **sostiene**: existe una estructura de desigualdad territorial significativa y decreciente, y las técnicas no supervisadas identifican regímenes de desempeño diferenciados y estables. La tipología estrictamente comunal es frágil por el bajo número de unidades, mientras que el análisis de regímenes comuna-año aporta la evidencia robusta.

## 4.7 Síntesis y limitaciones

### 4.7.1 Síntesis de hallazgos

| Hipótesis | Resultado | Estado |
|---|---|---|
| **H1** | Relaciones no lineales significativas; la visitación turística observada domina (0,345), seguida de construcción e inmobiliarias | Sostenida |
| **H2** | Random Forest R² = 0,81 en pronóstico temporal, frente a 0,24 de Ridge y 0,05 de regresión lineal | Sostenida (alcance temporal) |
| **H3** | Convergencia territorial (Theil −53,5 %; β = −0,033) y cuatro regímenes de desempeño estables | Sostenida |

Un patrón atraviesa los tres contrastes: el fenómeno central del período es la **desconcentración del clúster**, desde el enclave de Pucón hacia los destinos emergentes de la Araucanía Andina. Curacautín emerge de forma recurrente como el caso paradigmático de este proceso.

Este hallazgo cuenta con **validación externa independiente**. La Reserva Nacional Malalcahuello, situada en Curacautín y Lonquimay, pasó de 84.539 visitantes en 2013 a 297.623 en 2024, un incremento de 252 %, mientras el IDEC de Curacautín crecía 134 %. Se trata de dos registros administrativos sin relación entre sí —conteos físicos de visitantes de CONAF frente a declaraciones tributarias del SII— que convergen en la misma conclusión territorial. Que un fenómeno detectado mediante un índice construido con datos tributarios se corrobore con datos de visitación refuerza sustantivamente la validez del resultado.

### 4.7.2 Limitaciones

1. **Ausencia de la dimensión de actividad turística (D1).** El IDEC mide desempeño estructural (empleo, ingresos, capacidad) y no incorpora los flujos de visitantes. Como se expuso en §4.3.1, esta ausencia responde a una restricción de la información pública disponible —verificada sobre nueve esquemas de desagregación y sobre la propia fuente EMAT—, no a una decisión de conveniencia. Su superación requiere que el INE restituya la apertura por destino turístico suspendida en 2020, o que se acceda a registros de alojamiento con desagregación comunal.

2. **Número de unidades.** Con 13 comunas, la generalización espacial de los modelos y la tipología estrictamente comunal están intrínsecamente limitadas. El análisis a nivel comuna-año mitiga parcialmente esta restricción.

3. **Inversión pública agregada.** El BIP no distingue la inversión de vocación turística, lo que probablemente atenúa su señal en los modelos.

4. **Georreferencia tributaria y proyecciones de población.** Las cifras del SII se ubican por casa matriz y las poblaciones recientes son proyecciones anteriores al Censo 2024; ambas fuentes deberán actualizarse cuando se disponga de mejores registros.

Ninguna de estas limitaciones invalida los hallazgos: todas se declaran explícitamente y varias tienen una vía de resolución identificada, lo que refuerza —antes que debilita— la validez del estudio.
