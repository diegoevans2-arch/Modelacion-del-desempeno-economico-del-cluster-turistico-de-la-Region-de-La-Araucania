---
capitulo: V
titulo: Conclusiones
proyecto: Tesis Doctoral — Barra Ávila
estado: borrador
fecha: 2026-08-14
---

# CAPÍTULO V. CONCLUSIONES

## 5.1 Introducción

Este capítulo cierra la investigación a partir de los resultados consolidados en el Capítulo IV. Se organiza en seis secciones: el cumplimiento de los objetivos planteados (§5.2), la contrastación final de las hipótesis (§5.3), las contribuciones teóricas, metodológicas y empíricas del estudio (§5.4), las implicancias para la toma de decisiones territoriales (§5.5), las limitaciones que acotan el alcance de los hallazgos (§5.6) y las líneas de investigación que se abren a partir de ellos (§5.7). Una reflexión final (§5.8) sitúa el aporte del trabajo en el marco de la economía regional basada en evidencia.

## 5.2 Cumplimiento de los objetivos

### 5.2.1 Objetivo general

El objetivo general consistía en **desarrollar y validar un modelo integrado para la medición y predicción del desempeño económico estructural del clúster turístico de la Región de La Araucanía**, mediante un índice compuesto y técnicas de Machine Learning aplicadas a datos públicos oficiales.

El objetivo se cumple. Se construyó el **Índice de Desempeño Económico del Clúster (IDEC)** sobre un panel comunal balanceado de 156 observaciones —trece comunas entre 2013 y 2024—, integrado exclusivamente con registros administrativos de acceso público. El índice fue sometido a validación de robustez, con correlaciones de Spearman entre 0,91 y 1,00 según el método de normalización empleado, y a un diagnóstico de validez territorial desarrollado específicamente para este estudio. Sobre esa base se estimaron modelos supervisados que alcanzan un R² de 0,809 en validación temporal, y modelos no supervisados que identifican cuatro regímenes de desempeño estables.

El término *estructural* del objetivo no es accesorio: delimita con precisión lo que el modelo mide —empleo sectorial, generación de ingresos y capacidad productiva instalada— y lo que no mide, que son los flujos de visitantes. Esa delimitación, lejos de constituir una concesión, es resultado de una verificación sistemática documentada en §4.3.1.

### 5.2.2 Objetivos específicos

**Primer objetivo — identificar las variables económicas y territoriales relevantes a partir de fuentes públicas.** Se identificaron, levantaron e integraron cinco fuentes administrativas con desagregación comunal: el Servicio de Impuestos Internos, el Banco Integrado de Proyectos, el Instituto Nacional de Estadísticas, SERNATUR y la Corporación Nacional Forestal. La jerarquía de relevancia predictiva quedó establecida mediante importancia por permutación fuera de muestra, encabezada por la visitación a áreas silvestres protegidas (0,345) y seguida por las actividades de construcción e inmobiliarias (0,190 en conjunto). El objetivo se cumple, con el matiz de que el proceso también permitió establecer, con evidencia, qué variables **no** resultan aprovechables: la dimensión de actividad turística no pudo construirse porque ninguna fuente pública disponible admite su desagregación comunal válida.

**Segundo objetivo — aplicar técnicas de Machine Learning para estimar y predecir el desempeño del clúster.** Se estimaron cinco modelos con roles diferenciados —media, regresión lineal, regresión Ridge, árbol de decisión y Random Forest— bajo cuatro esquemas de validación. El objetivo se cumple con una precisión sobre su alcance: la capacidad predictiva es **temporal**, no espacial. El modelo estima con solvencia la trayectoria futura de comunas conocidas, pero no transfiere el aprendizaje hacia territorios no observados.

**Tercer objetivo — analizar los patrones y relaciones identificados por los modelos.** El análisis reveló tres patrones convergentes: la primacía predictiva de la demanda turística observada por sobre los indicadores económicos indirectos; la ausencia de señal detectable de la inversión pública agregada; y un proceso sostenido de convergencia territorial, con reducción del índice de Theil de 53,5 % entre 2013 y 2024. El objetivo se cumple.

**Cuarto objetivo — determinar el aporte de los modelos para la toma de decisiones territoriales.** Se desarrolló, además del análisis, un instrumento operativo de simulación de escenarios que permite estimar el efecto de choques exógenos sobre el desempeño comunal. El aporte para la decisión territorial se detalla en §5.5 y se caracteriza, con precisión, como capacidad de **monitoreo y anticipación** antes que de prescripción causal.

## 5.3 Contrastación final de las hipótesis

### 5.3.1 Hipótesis específica H1

> *Las variables económicas y territoriales obtenidas de fuentes públicas presentan relaciones predictivas relevantes, potencialmente no lineales, con el IDEC.*

**Se sostiene.** La importancia por permutación fuera de muestra establece una jerarquía interpretable y estadísticamente consistente. La no linealidad queda acreditada por vía indirecta pero robusta: bajo validación temporal, Random Forest alcanza un R² de 0,809 mientras la regresión lineal desciende a 0,051. Un fenómeno gobernado por relaciones lineales no produciría esa brecha.

Dos hallazgos merecen destacarse. Primero, que la variable de mayor capacidad explicativa sea la visitación a áreas protegidas —un registro de conteos físicos completamente independiente de los registros tributarios que componen el índice— constituye una validación cruzada de la construcción del IDEC. Segundo, que la inversión pública agregada no presente señal predictiva detectable es un resultado que debe leerse con la cautela expuesta en §4.4: la fuente no distingue la inversión de vocación turística, la estructura de rezagos podría diferir y la potencia estadística es limitada. La formulación rigurosa es que no se detecta relación, no que la relación no exista.

### 5.3.2 Hipótesis específica H2

> *Los modelos de aprendizaje supervisado permiten estimar el IDEC con niveles de error predictivo aceptables, medidos mediante RMSE, MAE y R².*

**Se sostiene, con alcance temporal explícito.** Random Forest estima el IDEC con un error absoluto medio de 0,059 sobre un índice acotado en el intervalo unitario, y explica el 80,9 % de la varianza en validación temporal.

La comparación con los enfoques tradicionales es exigente por construcción. Se incorporó deliberadamente una regresión Ridge con parámetro de regularización validado, a fin de que el contendiente econométrico compitiera en su mejor versión frente a predictores correlacionados. El resultado no es que los modelos lineales fracasen —alcanzan desempeños positivos y razonables bajo validación aleatoria y de bloques—, sino que **pierden casi toda su capacidad cuando se exige extrapolar a años no observados**, que es precisamente el uso relevante para la decisión territorial.

La delimitación del alcance es parte del resultado, no una salvedad menor. Bajo validación por comuna todos los modelos fallan, incluido Random Forest. Con trece unidades territoriales y un índice fuertemente asociado a características comunales persistentes, no existe base suficiente para aprender una relación transferible entre territorios. Declararlo explícitamente resulta metodológicamente preferible a exhibir un ajuste inflado por validación aleatoria, que en datos panel filtra información entre años contiguos de una misma comuna.

### 5.3.3 Hipótesis específica H3

> *Las técnicas de aprendizaje no supervisado permiten identificar patrones y agrupamientos diferenciados dentro del sistema turístico regional, evaluados mediante indicadores de cohesión y separación.*

**Se sostiene, con una precisión sobre el nivel de análisis.** La tipología construida estrictamente sobre las trece comunas resultó frágil: todas las particiones aíslan a Pucón como conglomerado unitario y ninguna concuerda con los Destinos Turísticos de SERNATUR. Es una limitación del número de unidades, no del método, y se declara como tal.

El análisis a nivel comuna-año, en cambio, es robusto. Los criterios de selección convergen —el método del codo y el coeficiente de silueta coinciden en cuatro conglomerados— y la partición resiste el remuestreo con un índice de Rand ajustado de 0,79. Emergen cuatro regímenes de desempeño nítidamente diferenciados, entre los cuales resulta particularmente significativa la separación entre el **enclave turístico** (Pucón) y el **centro urbano de servicios** (Temuco): dos territorios que agrupamientos más gruesos confunden por escala demográfica, y que el análisis distingue por composición.

La dimensión de desigualdad territorial aporta el resultado más sólido del capítulo. El índice de Theil desciende de 0,537 a 0,250 entre 2013 y 2024 —una reducción de 53,5 %— con tendencia significativa al 1 ‰. La convergencia se confirma mediante la prueba complementaria de β-convergencia (β = −0,033; *p* = 0,0002), lo que descarta que se trate de una regresión a la media espuria.

### 5.3.4 Hipótesis general

> *La integración de un índice compuesto construido con datos públicos oficiales con técnicas de Machine Learning permite explicar y predecir temporalmente el comportamiento del clúster turístico con mayor capacidad analítica que los enfoques descriptivos y lineales tradicionales.*

**Se sostiene.** Las tres hipótesis específicas se verifican, y la superioridad analítica frente a los enfoques tradicionales queda establecida frente a alternativas competentes y no frente a especificaciones deficientes. El calificativo *temporalmente*, presente en la formulación, resulta corroborado en su sentido estricto: la ventaja del aprendizaje automático se concentra en la extrapolación a períodos no observados y no se extiende a territorios no observados.

## 5.4 Contribuciones de la investigación

### 5.4.1 Contribución metodológica

El aporte metodológico principal es el **diagnóstico de degeneración del panel**. Buena parte de la información turística oficial se publica a escala regional, mientras que las decisiones territoriales se adoptan a escala comunal. La tentación metodológica evidente consiste en desagregar la serie regional mediante ponderadores comunales, procedimiento que produce una matriz de rango unitario: el agrupamiento resultante sólo recupera el orden de los ponderadores y el índice de desigualdad permanece constante, de modo que las hipótesis territoriales se vuelven formalmente incontrastables.

El procedimiento desarrollado descompone la varianza de cada variable en efectos de comuna, de tiempo y de interacción, y adopta como criterio de decisión la **idiosincrasia**: la fracción de la variación temporal que es propia de cada territorio y no un movimiento regional común. La métrica es invariante a las diferencias de escala entre comunas y exactamente nula bajo una desagregación de rango unitario. Aplicada a un contraejemplo deliberado, arroja cero; aplicada a las variables efectivamente empleadas, valores entre 0,30 y 0,92.

Su valor excede el caso analizado: constituye un protocolo replicable para cualquier investigación que integre datos públicos con niveles heterogéneos de desagregación, situación habitual en la estadística territorial latinoamericana.

Un segundo aporte metodológico, de orden práctico, es la **arquitectura de validación para datos panel**. La comparación sistemática de cuatro esquemas —aleatorio, por bloques temporales, temporal de origen móvil y por comuna— permitió distinguir la capacidad de pronóstico de la capacidad de generalización espacial, distinción que un esquema único habría ocultado.

### 5.4.2 Contribución teórica

La investigación operacionaliza el desempeño de un clúster turístico como **construcción multidimensional medible con registros administrativos**, sin recurrir a encuestas ni a instrumentos de levantamiento propio. El IDEC traduce a métrica territorial la noción portereana de clúster como concentración geográfica de actividades relacionadas, e incorpora esa relación al modelo mediante los sectores conexos —comercio, transporte, actividades recreativas, inmobiliarias y construcción— como variables explicativas exógenas al índice.

Los resultados aportan además evidencia empírica al debate sobre **convergencia regional** aplicado a un sistema turístico subnacional. La coincidencia de σ-convergencia y β-convergencia en un clúster históricamente polarizado sugiere que los procesos de difusión territorial de la actividad turística pueden operar en horizontes de una década, y no solamente en escalas generacionales.

### 5.4.3 Contribución empírica

El hallazgo sustantivo es la **desconcentración del clúster turístico de La Araucanía** durante el período analizado, desde el enclave consolidado de Pucón hacia los destinos emergentes de la Araucanía Andina. Curacautín constituye el caso paradigmático, con un incremento del IDEC de 134 % entre 2013 y 2024, seguido de Melipeuco (111 %) y Lonquimay (108 %), mientras Pucón es la única comuna que retrocede levemente.

Este resultado cuenta con **validación externa independiente**. La Reserva Nacional Malalcahuello, situada en Curacautín y Lonquimay, pasó de 84.539 visitantes en 2013 a 297.623 en 2024, un incremento de 252 %. Se trata de dos registros administrativos sin relación entre sí —conteos físicos de visitantes frente a declaraciones tributarias— que convergen en la misma conclusión territorial.

## 5.5 Implicancias para la toma de decisiones territoriales

El aporte del instrumento desarrollado no reside en entregar una predicción universal aplicable a cualquier territorio, sino en cuatro capacidades concretas.

**Monitoreo de trayectorias.** El IDEC permite seguir la evolución del desempeño comunal con una periodicidad anual y un rezago determinado por la publicación de las fuentes, sin necesidad de levantamiento primario. Para un gobierno regional, esto significa disponer de un indicador comparable entre comunas y en el tiempo a costo marginal nulo.

**Identificación temprana de territorios emergentes.** El análisis de regímenes detectó cuatro comunas en tránsito ascendente —Angol, Cunco, Curacautín y Victoria—, todas en la misma dirección y ninguna en sentido inverso. Reconocer esos tránsitos cuando ocurren, y no retrospectivamente, permite orientar el acompañamiento institucional hacia territorios en fase de consolidación.

**Anticipación ante choques exógenos.** El simulador de escenarios permite estimar el efecto de perturbaciones ajenas al rubro sobre el desempeño comunal, con una elasticidad declarada y auditable. Su utilidad es la de un instrumento de planificación de contingencia, no la de un pronóstico.

**Orientación del levantamiento de información.** El estudio identifica con precisión dónde la información pública disponible es insuficiente. La imposibilidad de construir la dimensión de actividad turística a escala comunal, y la suspensión de la apertura por destino turístico en la fuente sectorial desde 2020, constituyen un diagnóstico accionable para los organismos productores de estadística.

Corresponde advertir con igual claridad **qué no permite el instrumento**. No establece relaciones causales: la ausencia de señal predictiva de la inversión pública no autoriza a concluir que la inversión pública sea ineficaz. No admite extrapolación a comunas ajenas al panel. Y no sustituye el juicio experto ni el conocimiento territorial situado, sino que aporta una base cuantitativa comparable sobre la cual ejercerlos.

## 5.6 Limitaciones

Las limitaciones se detallan en §4.7.2 y se sintetizan aquí en cuatro órdenes.

La **ausencia de la dimensión de actividad turística** implica que el índice mide desempeño estructural y no flujos de visitantes. La restricción fue verificada sistemáticamente y no obedece a una decisión de conveniencia.

El **número de unidades territoriales** limita de manera intrínseca la generalización espacial de los modelos y la construcción de una tipología estrictamente comunal.

La **naturaleza de las fuentes** introduce sesgos declarados: la georreferenciación tributaria por casa matriz, el carácter agregado de la inversión pública registrada y el uso de proyecciones de población anteriores al Censo 2024.

El **rezago de publicación** determina que el panel cierre en 2024, restricción común a toda investigación que emplee registros tributarios comunales en Chile.

Ninguna de estas limitaciones invalida los hallazgos. Todas fueron identificadas, cuantificadas y declaradas, y varias cuentan con una vía de resolución explícita.

## 5.7 Líneas futuras de investigación

**Incorporación de la dimensión de actividad turística.** La vía natural es la restitución, por parte del organismo productor, de la apertura por destino turístico suspendida en 2020, o el acceso a registros de alojamiento con desagregación comunal. Alternativamente, el estudio identificó fuentes de flujo turístico observado aún no explotadas —en particular los registros de ingreso por pasos fronterizos, con presencia en Curarrehue y Lonquimay— que podrían aportar señal comunal adicional.

**Ampliación de la base territorial.** La limitación de generalización espacial es de información, no de método. Replicar el diseño sobre las regiones turísticas del sur de Chile multiplicaría las unidades disponibles y permitiría evaluar si las relaciones aprendidas son transferibles entre territorios comparables.

**Identificación causal.** Los resultados de esta investigación son predictivos. Establecer el efecto causal de la inversión pública sobre el desempeño del clúster requiere diseños específicos —variables instrumentales, discontinuidades en la asignación presupuestaria o diferencias en diferencias sobre programas focalizados— que exceden el alcance del presente trabajo pero cuya pertinencia queda establecida por él.

**Desagregación temporal.** La disponibilidad de la EMAT mensual y de la visitación de áreas protegidas con periodicidad mensual abre la posibilidad de analizar la **estacionalidad** del clúster, dimensión central en economía del turismo que un panel anual no captura.

**Extensión del marco de choques exógenos.** La variable de choques territoriales opera actualmente con elasticidad declarada. Al incorporarse la dimensión de flujos, la elasticidad podría estimarse de los datos, lo que convertiría el simulador en un instrumento con fundamento empírico completo.

## 5.8 Reflexión final

Esta investigación se propuso modelar el desempeño económico de un clúster turístico regional con técnicas de Machine Learning aplicadas exclusivamente a datos públicos. El resultado confirma que ello es posible, pero la contribución más duradera podría no residir en el modelo sino en el procedimiento que lo hizo defendible.

La disponibilidad creciente de datos abiertos convive con una asimetría persistente: la información se publica en la escala en que se produce, no en aquella en que se decide. Frente a esa asimetría, la tentación metodológica es desagregar. El trabajo muestra, con evidencia numérica, que hacerlo mediante ponderadores fijos genera una apariencia de información territorial donde no la hay, y que las conclusiones derivadas de tal procedimiento serían indistinguibles de un artefacto aritmético.

Preferir un índice de tres dimensiones observadas antes que uno de cuatro con una dimensión imputada implicó renunciar a la completitud formal del diseño original. Esa renuncia es, a juicio de esta investigación, el resultado metodológicamente más significativo: en el análisis territorial con datos públicos, la validez de la escala precede a la sofisticación del algoritmo.

El clúster turístico de La Araucanía se desconcentra. Ese hallazgo, sostenido por dos registros administrativos independientes entre sí, ofrece a la política pública regional algo más útil que una predicción: la constatación verificable de que el territorio se transforma, y la indicación de dónde está ocurriendo.
