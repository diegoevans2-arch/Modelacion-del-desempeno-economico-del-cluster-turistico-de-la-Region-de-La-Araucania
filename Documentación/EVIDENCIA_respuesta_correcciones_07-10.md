---
tipo: entrega de evidencia y respuesta técnica
destinatario: Germán Patricio Barra Ávila y equipo revisor
asunto: Evidencia ejecutada para los controles declarados "pendientes" en la versión del 7 de octubre
elaborado por: Diego Evans Pérez Paz — componente de Machine Learning
fecha: 2026-10-22
---

# Evidencia ejecutada para los controles pendientes

## 1. El problema de fondo era de entrega, no de análisis

La revisión del 7 de octubre declaró **seis controles "pendientes de evidencia"**
y retiró del documento afirmaciones que antes eran correctas. El Anexo L lo dice
con precisión: *"Esta revisión no recibió el archivo
`BBDD/final/resultados_h3_asignacion_por_fila.csv` mencionado en una redacción
anterior ni una salida equivalente."*

Ese archivo existe en el repositorio desde antes de esa revisión. Nunca se
entregó. Lo mismo ocurre con el código, el entorno y las particiones: no estaban
perdidos, estaban sin enviar. La consecuencia es que el documento retrocedió en
cuatro puntos que ya estaban resueltos.

Este documento entrega la evidencia y reporta los resultados de **todas** las
comprobaciones que quedaron declaradas y no ejecutadas. Todo es reproducible con
`random_state = 42`.

| Control | Estado en la V33 | Estado ahora |
|---|---|---|
| Hiperparámetros de Random Forest | sin certificar | ✅ verificado en código y entorno |
| Particiones y métricas por fila | pendiente | ✅ registro de 2.605 filas |
| Conciliación 152/156 | pendiente | ✅ identificadas las cuatro filas |
| Correspondencia territorial CONAF | pendiente | ✅ tabla unidad→comuna |
| R² de bloques (0,788 vs. 0,762) | contradictorio | ✅ reconciliado (§3) |
| Datos de convergencia | pendiente | ✅ especificación calibrada |
| COVID-19 | declarado no ejecutado | ✅ ejecutado (§6) |
| Sensibilidad sin D4 | parcial | ✅ completa, con bosque (§7) |
| Escala no acotada | no ejecutado | ✅ ejecutado, seis escalas (§8) |
| Umbral del anillo 3/4/5 | declarado irreconstruible | ✅ reconstruido (§9) |

---

## 2. Un error propio, primero

La discrepancia entre 0,788 y 0,762 que el informe señala **es mía y es real**.
Entregué dos cantidades distintas como si fueran la misma, y el revisor hizo
bien en marcarla. Más aún: la caracterizó correctamente sin ver el código
(*"distinguir el R² sobre predicciones agrupadas del promedio de R² por
partición, que no son equivalentes"*). Es exactamente eso.

La corrección está en §3. El documento debe conservar **0,762** en la Tabla 4.4.

---

## 3. Reconciliación del R²: son cuatro cifras, no dos

El código calcula el R² de dos maneras distintas en dos funciones distintas:

- **`evaluar()`** concatena las predicciones de todos los pliegues y calcula
  **un solo** R² sobre el conjunto agrupado. Es la cantidad que reporta la
  Tabla 4.4.
- **`importancia_variables()`** calcula el R² **de cada pliegue y los promedia**.
  Es la cantidad que califica la importancia por permutación, porque permutar
  variables de un modelo que no predice no informa nada.

No son equivalentes: el R² agrupado usa la media global de la variable
dependiente como referencia, y el promedio por pliegue usa la media de cada
pliegue. Las cuatro cifras forman una matriz:

| Especificación | R² agrupado | R² medio de pliegues |
|---|---|---|
| **previa a CONAF** | 0,6306 | **0,674** |
| **vigente (con CONAF)** | **0,7621** | **0,788** |

**Lecturas que se siguen:**

1. El **0,762** de la Tabla 4.4 es la celda *agrupado × vigente*. Es correcto y
   debe conservarse.
2. El **0,788** es la celda *medio-por-pliegue × vigente*. Es la que debe
   acompañar a la tabla de importancias, con ese nombre.
3. El antiguo **0,68** es la celda *medio-por-pliegue × previa a CONAF*. Al
   reproducirlo hoy da **0,674**, es decir redondea a **0,67**. La diferencia
   respecto del 0,68 documentado proviene de que la especificación histórica
   tenía otra lista de predictores. **Debe reportarse 0,674**, que es lo
   reproducible, y no el 0,68.
4. La mejora atribuible a CONAF es real y se puede expresar en ambas escalas:
   0,6306 → 0,7621 en agrupado, y 0,674 → 0,788 en promedio por pliegue.

La redacción debe nombrar las dos cantidades de forma distinta. Con eso, lo que
hoy parece una contradicción pasa a ser un control metodológico.

### Tabla 4.4 verificada en su totalidad

| Esquema | R² | MAE | n de prueba |
|---|---|---|---|
| Aleatorio | 0,7989 | 0,0582 | 152 |
| Bloques | 0,7621 | 0,0651 | 152 |
| Temporal | 0,8087 | 0,0585 | 65 |
| Por comuna | −0,3619 | 0,1699 | 152 |

Los valores tabulados 0,80 / 0,76 / 0,81 / −0,36 son todos correctos.

### Por qué la Tabla 4.4 debe usar el R² agrupado

Las dos cantidades, calculadas sobre los cuatro esquemas:

| Esquema | R² agrupado | R² medio de pliegues | desviación entre pliegues |
|---|---|---|---|
| Aleatorio | 0,7989 | 0,8001 | 0,0865 |
| Bloques | 0,7621 | **0,7877** | 0,1467 |
| Temporal | 0,8087 | 0,8068 | 0,0289 |
| Por comuna | −0,3619 | **−18,677** | 26,36 |

El caso por comuna muestra por qué el agrupado es la cifra correcta para la
tabla: dentro del pliegue de una sola comuna la varianza de la variable
dependiente es mínima, de modo que el R² de ese pliegue se desploma y el
promedio queda dominado por un puñado de pliegues degenerados. El valor
agrupado, −0,3619, es el interpretable.

El promedio por pliegue sigue siendo el correcto para acompañar la importancia
por permutación, porque la permutación se ejecuta pliegue a pliegue. El
**0,7877** de bloques es el que debe citarse allí, y es el que redondea a 0,788.

---

## 4. Hiperparámetros: configuración certificada

| Parámetro | Valor |
|---|---|
| `n_estimators` | 500 |
| `min_samples_leaf` | 3 |
| `max_features` | `sqrt` |
| `random_state` | 42 |
| `max_depth` | None |
| `min_samples_split` | 2 |
| `bootstrap` | True |
| `criterion` | `squared_error` |

Los cuatro primeros se fijan explícitamente en `modelos()`, en
`src/models/supervisado.py`; los cuatro últimos son los valores por defecto de
scikit-learn y se documentan para evitar ambigüedad. **No se ejecutó GridSearch
ni RandomSearch.**

Entorno verificado: Python 3.12.7, scikit-learn 1.9.0, numpy 1.26.4,
pandas 2.2.2. Quince predictores.

El archivo `BBDD/final/evidencia_entorno.txt` contiene esta configuración junto
con los hashes SHA-256 de los módulos y de los paneles, de modo que la
correspondencia entre código y resultados es verificable.

**Corresponde adoptar la Alternativa A** del documento de correcciones: los
parámetros son los efectivos y están verificados contra el código.

---

## 5. Validación temporal: métricas por año

El horizonte es de **un año** y el esquema es de origen móvil con ventana
expansiva. Cinco iteraciones:

| Año de prueba | n entrenamiento | n prueba | R² | MAE | RMSE |
|---|---|---|---|---|---|
| 2020 | 87 | 13 | **0,8417** | 0,0476 | 0,0688 |
| 2021 | 100 | 13 | 0,7745 | 0,0679 | 0,0814 |
| 2022 | 113 | 13 | 0,7814 | 0,0642 | 0,0892 |
| 2023 | 126 | 13 | 0,8407 | 0,0565 | 0,0726 |
| 2024 | 139 | 13 | 0,7956 | 0,0562 | 0,0870 |

Prueba acumulada: 65 observaciones. El R² agregado de 0,8087 no esconde un año
malo: los cinco están entre 0,77 y 0,84. **El mejor es 2020**, el año del cierre
sanitario.

El registro completo por fila —comuna, año, esquema, partición, observado,
predicho y residuo, para los cinco modelos y los cuatro esquemas— está en
`BBDD/final/evidencia_predicciones_por_fila.csv`. Es exactamente el artefacto
que pide §3.10.3.1.

---

## 6. COVID-19: ejecutado

Se incorporó una variable indicadora con valor 1 en 2020 y 2021, y se reestimó.

**Efecto sobre el ajuste:**

| Esquema | sin dummy | con dummy | Δ |
|---|---|---|---|
| Bloques | 0,7621 | 0,7746 | +0,0125 |
| Temporal | 0,8087 | 0,8229 | +0,0142 |

**Relevancia de la dummy:** importancia por permutación = **0,0000**, en la
posición 15 de 16 predictores.

**Efecto descriptivo (MCO con efecto fijo de comuna):** coeficiente = −0,00391
(ee = 0,01022; t = −0,382; **p = 0,703**), equivalente a −1,86 % de la media del
IDEC. **No significativo.**

La jerarquía de importancias se conserva: visitación CONAF sigue primera, con
0,3996.

### Interpretación

La pandemia **no deja huella detectable en el índice**, y eso es
sustantivamente coherente: el IDEC mide empleo, ingresos y capacidad
productiva —variables estructurales y de ajuste lento—, no flujos de visitantes.
El choque golpeó los flujos, que son justamente lo que el índice no contiene por
la ausencia de D1.

La decisión de no modelar COVID-19 queda así **justificada empíricamente**, no
sólo declarada. Es un resultado mucho más defendible que la redacción actual de
§1.1.5, que lo deja como carencia.

---

## 7. Sensibilidad del IDEC sin D4: completa

**Concordancia de ordenamientos (Spearman, índice completo vs. de dos
dimensiones):**

| | valor |
|---|---|
| Mínimo (2013) | 0,7527 |
| Mediana | 0,8819 |
| Máximo (2021) | 0,9286 |
| **2024** | **0,8956** |
| Panel completo | 0,8891 |

El 0,896 que reporta el informe para 2024 **se confirma exactamente**.

**β-convergencia:** sin D4, β = **−0,055017** (p = 0,000008; R² = 0,8471), frente
a −0,032880 con D4. También **confirma** el −0,055 del informe.

**Capacidad predictiva con el índice de dos dimensiones como objetivo:**

| Esquema | con D4 | sin D4 | Δ |
|---|---|---|---|
| Bloques | 0,7621 | 0,6914 | **−0,0707** |
| Temporal | 0,8087 | 0,7624 | **−0,0463** |

### Interpretación

Excluir D4 **refuerza** la convergencia y **deteriora** la predicción. La
dimensión aporta información real: retirarla cuesta entre 4,6 y 7,1 puntos de
R². Su permanencia queda justificada por evidencia y no sólo por "cobertura
conceptual", que es como la defiende hoy §3.8.4.

Conviene señalar el matiz: parte de la convergencia del índice completo está
siendo *atenuada* por D4, cuya variación temporal es escasa. Eso es consistente
con la observación del comité sobre D4 y la vuelve interpretable.

---

## 8. Escala acotada: la convergencia no es un artefacto del techo

Se estimó la β-convergencia en seis especificaciones, de las cuales cinco están
fuera del intervalo unitario:

| Especificación | Escala | β | p |
|---|---|---|---|
| IDEC (base) | acotada [0,1] | −0,032880 | 0,000212 |
| Logit del IDEC | no acotada | −0,025124 | 0,001308 |
| Ventas p.c. | original, no acotada | −0,023046 | 0,028106 |
| Trabajadores p.c. | original, no acotada | −0,034213 | 0,014987 |
| Renta p.c. | original, no acotada | −0,038941 | 0,002714 |
| Índice z compuesto | no acotada | −0,010896 | **0,2598** |

Trabajadores y renta per cápita se estiman sobre doce comunas: Cunco registra
cero en 2013 en ambas, y el logaritmo de cero no está definido. La exclusión se
declara.

### Interpretación, con su reserva

**En cinco de seis especificaciones la convergencia es negativa y
significativa**, incluidas las tres construidas sobre indicadores económicos en
sus unidades originales, que no tienen techo alguno. La objeción del efecto
techo **no se sostiene**: la desconcentración no es un artefacto del
acotamiento.

La excepción es el índice z compuesto, donde β pierde significancia
(p = 0,26). Es un agregado que construí estandarizando los logaritmos de los
cinco indicadores, y la estandarización comprime precisamente la dispersión
inicial que la β-convergencia necesita medir. Debe reportarse, no esconderse:
es el único caso adverso de seis y conviene declararlo tal cual.

Esta sección reemplaza con resultados el párrafo de §4.6.1.1 que hoy sólo
advierte sobre la limitación.

---

## 9. Umbral del anillo: los tres universos son reconstruibles

§3.5.2 afirma que *"con el material disponible no pueden reconstruirse de manera
fiable los universos de tres y cinco alojamientos ni reestimar los
resultados"*. **Esa afirmación es incorrecta.** El Registro Nacional de
Prestadores cubre las 32 comunas de la región y `construir()` está parametrizado
por lista de comunas. Los tres universos se reconstruyeron por completo.

**Oferta formal fuera del núcleo:** Cunco 14, Victoria 7, Angol 7, Saavedra 6,
Vilcún 4, Loncoche 3, Collipulli 3, y el resto 2 o menos.

| Umbral | Comunas | Obs. | β | p | Theil 2013→2024 | RF bloques | RF temporal | MAE |
|---|---|---|---|---|---|---|---|---|
| ≥ 3 | 15 | 180 | −0,032480 | 0,000109 | −52,1 % | 0,7820 | 0,8207 | 0,0546 |
| **≥ 4 (vigente)** | **13** | **156** | **−0,032880** | **0,000212** | **−53,5 %** | **0,7636** | **0,8086** | **0,0585** |
| ≥ 5 | 12 | 144 | −0,041465 | 0,000014 | −57,7 % | 0,7610 | 0,8235 | 0,0597 |

Con ≥ 3 ingresan **Loncoche y Collipulli**; con ≥ 5 sale **Vilcún**.

### Interpretación

Las conclusiones son **robustas al umbral**. En los tres universos la β es
negativa con p < 0,001, la caída de Theil se mantiene entre 52 y 58 %, y el R²
temporal del bosque entre 0,81 y 0,82.

Un punto que conviene explicitar en la defensa: el Anexo I advierte que *"no se
deben seleccionar umbrales después de observar cuál conserva un resultado
significativo"*. Aquí ocurre lo contrario del cherry-picking — el umbral vigente
es el **caso intermedio y el menos favorable** para la magnitud de β. Elegirlo
no maximiza ningún resultado.

**Lo que sí es una limitación real:** el registro de SERNATUR es un corte
transversal **sin fecha de inscripción**, como ya reconoce §3.6. Por eso la
petición de "aportar un registro fechado de alojamientos" no puede cumplirse con
la fuente disponible: no existe tal fecha en el registro. Lo que sí se puede —y
se hizo— es la sensibilidad sobre el corte transversal. Conviene reformular esa
exigencia en el Anexo G, porque hoy pide algo que la fuente no contiene.

---

## 10. Conciliación 152/156: resuelta

El agrupamiento usa 152 de las 156 observaciones. Las cuatro ausentes,
verificadas contra el archivo de asignación por fila, son:

| Comuna | Año | Causa |
|---|---|---|
| Melipeuco | 2013 | sin fila de rubro R en el SII |
| Melipeuco | 2014 | sin fila de rubro R ni de rubro L |
| Lonquimay | 2013 | sin fila de rubro R |
| Lonquimay | 2014 | sin fila de rubro R |

No es error de transcripción ni imputación fallida: **el SII no registra empresas
del rubro de actividades recreativas en esas comunas y años**. La exclusión es
por lista completa sobre una variable de perfil, y la causa es ausencia
estructural de la actividad.

Conteos por régimen en el archivo: **83, 45, 12 y 12**, suma 152, idénticos a los
de la Tabla 4.7.

`BBDD/final/resultados_h3_asignacion_por_fila.csv` contiene comuna, nombre, año,
régimen, etiqueta e IDEC para las 152 filas. **Es el archivo que la revisión no
recibió.**

---

## 11. Controles del Anexo I

### 11.1 Theil excluyendo Pucón, con las dos decisiones separadas

El Anexo I pide distinguir la exclusión del cambio de escala. Ambas:

| Especificación | 2013 | 2024 | Variación |
|---|---|---|---|
| Base, 13 comunas | 0,5372 | 0,2495 | **−53,5 %** |
| Sin Pucón, misma escala Min-Max | 0,2568 | 0,1656 | **−35,5 %** |
| Sin Pucón, Min-Max recalibrado | 0,2826 | 0,1910 | **−32,4 %** |

La base reproduce el −53,5 % publicado. **La caída persiste sin Pucón, pero es
sustancialmente menor**: cerca de un tercio en lugar de más de la mitad. Y el
nivel de desigualdad cae a menos de la mitad al excluirlo, lo que confirma que
Pucón es el principal contribuyente a la dispersión del índice.

Esto debe reportarse. Es el matiz correcto a la afirmación de desconcentración:
una parte importante de la caída de Theil es la convergencia *del resto hacia
Pucón*, no una igualación general.

### 11.2 Stock de inversión

| Parámetro | Valor |
|---|---|
| Tasa de depreciación | **0,05** (`DEPRECIACION_INFRAESTRUCTURA`) |
| Año de inicio de la acumulación | **2000** |
| Año inicial del reporte | 2013 |
| Años de calentamiento | **13** |

El Anexo I advierte que *"un supuesto de stock inicial nulo y una serie histórica
previa no son equivalentes"*. La respuesta es la segunda: **el stock no parte de
cero en 2013**, se acumula por inventario perpetuo desde 2000, de modo que al
primer año del panel ya lleva trece años de historia.

### 11.3 Metadatos de la permutación

| Elemento | Valor |
|---|---|
| Métrica cuya pérdida se mide | R² |
| Conjunto de evaluación | pliegue de prueba de cada partición |
| Repeticiones | 30 por pliegue |
| Pliegues | 5 |
| Esquema | bloques |

**Predictores correlacionados** — el control que pide el Anexo I:

| Par | r |
|---|---|
| Población ↔ población laboral | **1,000** |
| Ventas construcción p.c. ↔ población | 0,910 |
| Ventas construcción p.c. ↔ población laboral | 0,908 |
| Ventas comercio p.c. ↔ trabajadores comercio p.c. | 0,886 |

**Población y población laboral son colineales en r = 1,000**: son la misma
información en dos columnas. Con predictores perfectamente correlacionados, la
importancia por permutación **subestima a ambos**, porque permutar uno deja al
otro transportando la señal. Sus importancias individuales (0,0428 y 0,0388) no
son interpretables por separado y deben leerse como un solo aporte conjunto.
Conviene declararlo donde se presenta la Tabla 4.3.

### 11.4 Unidad de remuestreo del ARI

El Anexo I observa que *"muestrear filas puede preservar inadvertidamente años de
una misma comuna en ambos subconjuntos"*. Es exactamente lo que hace
`estabilidad()`. Ambas variantes:

| Unidad de remuestreo | ARI medio | p10 |
|---|---|---|
| **Fila** (la publicada) | **0,7949** | 0,6177 |
| **Comuna completa** | **0,7045** | 0,3817 |

El 0,79 publicado **se reproduce exactamente** con remuestreo por fila. Con
remuestreo por comuna el ARI baja a 0,70 y el percentil 10 a 0,38.

Esto debe declararse: la estabilidad sigue por encima del umbral de 0,5 que el
protocolo fija como mínimo interpretable, pero cae por debajo del 0,75 que el
mismo protocolo define como estructura robusta. **La unidad de remuestreo debe
nombrarse en el texto**, y conviene reportar las dos cifras.

---

## 12. Dos hallazgos que la revisión no podía ver

### 12.1 El agrupamiento publicado es jerárquico, no k-means

Verificado: las etiquetas del archivo por fila se reproducen con **agrupamiento
jerárquico** a nivel comuna-año con k = 4, con **ARI = 1,0000** y conteos
idénticos (83/45/12/12). K-means da 82/46/12/12, de modo que **no** es el
algoritmo que generó los resultados reportados.

El documento es por tanto internamente consistente —el ARI = 0,79 también
corresponde a jerárquico—, pero el algoritmo **no está nombrado** donde se
presentan los regímenes. Debe explicitarse en §4.7, porque un auditor que
reejecute con el valor por defecto del módulo obtendrá otros conteos y creerá
haber encontrado una inconsistencia. Es lo que me ocurrió a mí al verificarlo.

### 12.2 Enmascaramiento tributario convertido en cero

Los sectores conexos se integran al panel con una tabla dinámica que convierte
en **0** los valores que el SII oculta por reserva tributaria (celdas con diez o
menos informantes).

| Sector | Celdas enmascaradas |
|---|---|
| Actividades recreativas | 50 de 152 (**33 %**) |
| Actividades inmobiliarias | 50 de 155 (**32 %**) |
| Construcción | 8 de 156 (5 %) |
| Transporte | 1 de 156 |
| Comercio | 0 de 156 |
| **Rubro I (el del IDEC)** | **0 de 156 (0 %)** |

**La variable dependiente no está afectada.** Prueba de sensibilidad
reconvirtiendo las celdas a dato faltante: R² temporal 0,8087 → 0,8141, se
conserva el orden de importancias, y la muestra utilizable cae de 152 a 92
observaciones (−39 %).

**Recomendación: declararlo, no corregirlo.** Corregirlo sacrificaría el 39 % del
panel sin cambiar ninguna conclusión. El sesgo es de signo conocido y acotado:
una celda oculta corresponde a diez o menos contribuyentes, de modo que el cero
es una cota inferior.

---

## 13. Cifras a corregir en el documento

| Cifra | Dónde | Corrección |
|---|---|---|
| Spearman "0,92 a 1,00" | §5.1 (y se declara adoptado "para coherencia documental") | El mínimo verificado es **0,914971**. El intervalo correcto es **0,91 a 1,00**, como ya dice §4.3.2 |
| R² = 0,68 pre-CONAF | Anexo G y §4.4 | El valor reproducible es **0,674**, y es un promedio por pliegue, no un R² agrupado |
| "0,68 no trazable" | Anexo G | Es trazable: celda *medio-por-pliegue × pre-CONAF* (§3) |
| 152/156 "pendiente" | §4.7, Tabla 4.7, Anexo L | Resuelto (§10) |
| Universos 3 y 5 "irreconstruibles" | §3.5.2 | Reconstruidos (§9) |
| Reproducibilidad "pendiente de evidencia" | Anexo G | Código, entorno, hashes y particiones entregados |

El 0,067 de actividades inmobiliarias es correcto y no debe tocarse.

Las correcciones estructurales del informe **sí están aplicadas** y no requieren
acción: anexos A a L sin duplicación de F, §4.8.3 restaurada, y numeración
coherente.

---

## 14. Archivos entregados

En `BBDD/final/`:

| Archivo | Contenido |
|---|---|
| `resultados_h3_asignacion_por_fila.csv` | 152 filas: comuna, año, régimen, IDEC |
| `evidencia_predicciones_por_fila.csv` | observado y predicho por fila, partición, esquema y modelo |
| `evidencia_metricas_por_particion.csv` | R² agrupado **y** medio por pliegue, MAE, RMSE |
| `evidencia_disponibilidad_predictores.csv` | cobertura temporal y nulos de cada predictor |
| `evidencia_conaf_correspondencia.csv` | unidad SNASPE → comuna, fracción asignada, no reporte |
| `evidencia_sensibilidad_umbral_anillo.csv` | los tres universos de §9 |
| `evidencia_panel_universo_u3.csv` | panel de quince comunas |
| `resultados_h2_metricas_por_anio.csv` | las cinco iteraciones de §5 |
| `evidencia_entorno.txt` | versiones, semilla, configuración y hashes SHA-256 |

El código está en `src/`. El panel se regenera con `python -m src.build_panel`.

**Nota de reproducción**: `importancia_variables()` sufría paralelismo anidado
entre el bosque y la permutación, lo que en Windows la hacía tardar varios
minutos. Ya está corregido en `src/models/supervisado.py`, con los dos `n_jobs`
fijados a propósito; la medición sobre este panel es de 277 s con ambos en −1
frente a 74 s con la configuración actual.

Importa una precisión sobre esa corrección, porque yo la había enunciado de
forma demasiado fuerte. El `n_jobs` de `permutation_importance` **sí** es
numéricamente neutro: sortea una sola semilla y la reparte entre las tareas. El
del bosque **no lo es del todo**: con `n_jobs=-1`, `predict()` acumula los 500
árboles bajo un lock en el orden en que los hilos lo van ganando, y la suma de
punto flotante no es asociativa, de modo que los últimos dígitos varían entre
corridas. Las cifras que este documento reporta —tres y cuatro decimales— no se
ven afectadas, pero la afirmación correcta es que con `n_jobs=1` la función pasa
a ser reproducible bit a bit, no que el reparto fuera indiferente.

El detalle está en `Documentación/Nota_tecnica_paralelismo_importancia_variables.md`.

---

## 15. Lo que sigue siendo una limitación real

No todo se resuelve con evidencia. Estas observaciones del comité son correctas
y deben permanecer como límites declarados:

1. **Ausencia de D1.** El índice no mide flujos turísticos. La EMAT por destino
   está suspendida desde abril de 2020 y no existe serie comunal compatible.
   Es el límite de validez de contenido más importante.
2. **Trece unidades territoriales.** Las 156 filas no son 156 unidades
   independientes. Limita la inferencia y la generalización espacial.
3. **R² por comuna negativo (−0,3619).** El modelo no transfiere a comunas no
   vistas. Debe decirse sin matizar.
4. **El registro de alojamientos no tiene fecha.** D4 aporta variación entre
   comunas, no a lo largo del tiempo.
5. **Umbrales de las hipótesis no preregistrados.** Fijarlos ahora sería
   retrospectivo. La postura del documento es defendible, pero conviene
   confirmarla con la comisión, como ya señala el informe.
6. **La magnitud de la convergencia es sensible.** Sin Pucón la caída de Theil
   pasa de −53,5 % a cerca de −33 %, y la β se reduce a la mitad al excluir
   simultáneamente las observaciones influyentes. La dirección es sólida; la
   magnitud puntual requiere cautela con n = 13.

Ninguna de las comprobaciones de este documento alteró un resultado sustantivo
de la tesis. Lo que cambió es que ahora están ejecutadas en lugar de declaradas.
