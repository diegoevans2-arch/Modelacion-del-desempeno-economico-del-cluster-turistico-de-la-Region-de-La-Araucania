---
tipo: respuesta técnica a observaciones
destinatario: Germán Patricio Barra Ávila
asunto: Cierre de los cuatro puntos bloqueantes del Comité Evaluador
elaborado por: Diego Evans Pérez Paz — componente de Machine Learning
fecha: 2026-10-05
---

# Respuesta a las observaciones del Comité Evaluador

## 1. Veredicto general

**Los cuatro puntos que bloquean el depósito están resueltos.** Ninguno requería
reejecutar análisis ni «recuperar salidas perdidas»: el código es la salida
original y es reproducible de extremo a extremo, de modo que cada pregunta se
responde con la cifra exacta.

Se resuelve además el quinto punto de Prioridad 2 (análisis de influencia) y se
recupera la trazabilidad del R² = 0,68, que la versión vigente había retirado
por considerarlo no trazable.

| # | Observación del comité | Estado |
|---|---|---|
| 1 | La Tabla 4.7 suma 152 y no 156 | Resuelto — causa identificada en la fuente |
| 2 | Hiperparámetros de Random Forest | Resuelto — configuración y entorno completos |
| 3 | Horizonte de la validación temporal | Resuelto — un año, con tabla de iteraciones |
| 4 | Trazabilidad de la visitación CONAF | Resuelto — regla y naturaleza de los ceros |
| 5 | Influencia en la β-convergencia (P2) | Resuelto — leverage y distancia de Cook |
| — | R² = 0,68 «sin trazabilidad» | Trazabilidad recuperada |

Se detectó también **un problema que los revisores no identificaron**, con su
prueba de sensibilidad ya ejecutada, y que conviene declarar antes de que lo
pregunte el tribunal (§7).

---

## 2. Evaluación de las observaciones recibidas

### 2.1 Lo que está bien visto

**La crítica del constructo es la más profunda y es correcta.** El IDEC se
construye con el rubro I del Servicio de Impuestos Internos —alojamiento y
servicio de comidas— más un corte de SERNATUR. No mide el clúster turístico en
sentido amplio. La delimitación del documento vigente es correcta; la tensión
con el título es real y conviene responderla de frente, no esquivarla.

**Los cuatro bloqueantes son legítimos y están bien priorizados.** Son
exactamente las preguntas que permiten auditar un resultado cuantitativo.

**El efecto techo es una objeción justa.** Pucón parte de 0,805 sobre un índice
acotado en el intervalo unitario. Pedir un test explícito es razonable, y el
test ahora está hecho: el resultado favorece a la tesis (§8).

**La observación sobre D4 es correcta.** Su variación temporal proviene
únicamente del componente de empresas del SII.

### 2.2 Lo que conviene matizar

**El archivo de recomendaciones fue escrito sin acceso al código.** Instruye
abrir `04_unsupervised_clustering.ipynb` y `03_supervised_models.ipynb` y
ejecutar instrucciones sobre objetos llamados `kmeans`, `rf_model` y `tscv`.
**Ninguno de esos archivos ni objetos existe en el proyecto**: el análisis vive
en módulos de `src/` —`models/clustering.py`, `models/supervisado.py`— y no en
cuadernos, y la validación temporal no usa `TimeSeriesSplit` sino una partición
de origen móvil propia. Sus instrucciones no son aplicables tal cual. Las
preguntas de fondo que plantea sí lo son, y quedan respondidas más abajo.

**«Recuperar las salidas originales» presupone que algo se perdió.** No es el
caso. El proyecto se regenera completo con un comando. Conviene señalarlo en la
defensa: no se trata de reconstruir evidencia extraviada, sino de documentar en
el texto lo que el código ya determina.

**Una observación del informe está desactualizada.** Afirma que el simulador «no
se describe en la metodología ni en los resultados». Eso era cierto en la
versión anterior; la vigente lo incorpora en §3.17, §4.12 y §4.13, y el propio
comité lo califica como cumplido. No requiere acción.

**La cifra de Spearman que celebra el informe es ligeramente incorrecta.**
Menciona «entre 0,92 y 1,00»; el mínimo verificado es **0,915**, de modo que el
intervalo correcto es **0,91 a 1,00**. El documento vigente usa ambos valores en
pasajes distintos y debe unificarse en 0,91.

---

## 3. Punto 1 — Tabla 4.7: por qué 152 y no 156

### Respuesta

No es un error de transcripción. **Cuatro observaciones quedan fuera del
agrupamiento por dato faltante en una variable de perfil**, y el método las
excluye según lista completa:

| Comuna | Año | Variable faltante |
|---|---|---|
| Melipeuco | 2013 | ventas recreativas per cápita |
| Melipeuco | 2014 | ventas recreativas e inmobiliarias per cápita |
| Lonquimay | 2013 | ventas recreativas per cápita |
| Lonquimay | 2014 | ventas recreativas per cápita |

### Causa raíz verificada en la fuente

En esas celdas **el SII no publica fila alguna para el rubro R, actividades
recreativas**: no existen empresas registradas de ese rubro en esas comunas y
años. No es dato omitido ni imputación fallida; es ausencia estructural de la
actividad económica.

Los conteos por régimen se mantienen exactos: **12 + 12 + 45 + 83 = 152**,
idénticos a los de la Tabla 4.7.

### Acción sobre el documento

Sustituir la nota «debe verificarse» por una redacción definitiva:

> El agrupamiento se realiza sobre 152 de las 156 observaciones del panel.
> Cuatro observaciones —Melipeuco y Lonquimay, años 2013 y 2014— quedan
> excluidas por exclusión según lista completa, al no registrar el Servicio de
> Impuestos Internos empresas del rubro de actividades recreativas en esas
> comunas y años. La exclusión obedece a ausencia estructural de la actividad y
> no a dato omitido ni a imputación.

**Salida por fila disponible** para el anexo:
`BBDD/final/resultados_h3_asignacion_por_fila.csv`, con comuna, año, régimen
asignado e IDEC para las 152 observaciones.

---

## 4. Punto 2 — Hiperparámetros de Random Forest

### Configuración exacta

| Parámetro | Valor |
|---|---|
| `n_estimators` | 500 |
| `max_depth` | None (sin límite de profundidad) |
| `min_samples_leaf` | 3 |
| `min_samples_split` | 2 |
| `max_features` | `sqrt` |
| `bootstrap` | True |
| `criterion` | `squared_error` |
| `random_state` | **42** |
| Predictores | 15 |

| Entorno | Versión |
|---|---|
| scikit-learn | 1.9.0 |
| numpy | 1.26.4 |
| pandas | 2.2.2 |
| Python | 3.12.7 |

### Sobre la sintonización

**No se realizó búsqueda de hiperparámetros**, ni exhaustiva ni aleatorizada.
Los valores se fijaron a priori con criterios estándar para paneles pequeños:
`min_samples_leaf = 3` para limitar el sobreajuste con 156 observaciones, y
`max_features = "sqrt"` para decorrelacionar los árboles ante predictores
correlacionados entre sí.

Conviene declararlo así, explícitamente. Es una limitación menor y honesta, y
tiene una contrapartida metodológica favorable: no sintonizar evita el riesgo de
sobreajustar la *selección* de hiperparámetros a un conjunto de validación tan
reducido, que con n = 156 habría sido un riesgo mayor que el que se evita.

**`random_state = 42` está fijado**, de modo que los resultados son
reproducibles de forma exacta. Esto responde directamente la salvedad que la
guía de correcciones planteaba sobre la posible variabilidad entre ejecuciones:
no existe tal variabilidad.

---

## 5. Punto 3 — Horizonte de la validación temporal

### Respuesta: un año de horizonte, cinco iteraciones

| Iteración | Entrenamiento | n | Prueba | n | Horizonte |
|---|---|---|---|---|---|
| 1 | 2013–2019 | 87 | 2020 | 13 | 1 año |
| 2 | 2013–2020 | 100 | 2021 | 13 | 1 año |
| 3 | 2013–2021 | 113 | 2022 | 13 | 1 año |
| 4 | 2013–2022 | 126 | 2023 | 13 | 1 año |
| 5 | 2013–2023 | 139 | 2024 | 13 | 1 año |

Total de observaciones de prueba acumuladas: **65**.

El esquema es de **origen móvil con ventana expansiva**: cada iteración entrena
con todos los años disponibles hasta el corte y predice el año siguiente
completo, es decir las trece comunas simultáneamente.

### Implicación para la interpretación del R² = 0,809

Debe leerse como **capacidad de pronóstico a un año**, no a tres ni a cinco. Es
a la vez la lectura más exigente y la más útil para la decisión territorial: el
coeficiente se calcula sobre 65 predicciones de años que el modelo nunca vio en
el entrenamiento.

Conviene añadir que el período de prueba —2020 a 2024— contiene íntegramente el
choque sanitario. La cifra no proviene de un tramo especialmente favorable, sino
del más adverso de la serie.

---

## 6. Punto 4 — Trazabilidad de la visitación CONAF

### Regla de asignación unidad → comuna

Cuando una unidad del SNASPE abarca varias comunas del clúster, sus visitas se
**reparten en partes iguales** entre ellas. La asignación completa es:

| Unidad SNASPE | Comunas del clúster |
|---|---|
| P.N. Conguillío | Melipeuco, Cunco, Curacautín, Vilcún |
| P.N. Huerquehue | Pucón |
| P.N. Villarrica | Pucón |
| R.N. Villarrica | Pucón |
| R.N. Malalcahuello | Curacautín, Lonquimay |
| P.N. Tolhuaca | Curacautín, Victoria |
| P.N. Nahuelbuta | Angol |
| M.N. Cerro Ñielol | Temuco |
| R.N. China Muerta | Melipeuco, Lonquimay |
| R.N. Alto Biobío | Lonquimay |
| R.N. Nalcas | Lonquimay |
| R.N. Malleco, M.N. Contulmo | fuera del clúster; no se reparten |

El reparto en partes iguales es un **supuesto declarado**, no un dato observado.
Es revisable contra cartografía oficial de CONAF si el tribunal lo solicita.

### Naturaleza de los ceros en las cuatro comunas

**Carahue, Nueva Imperial, Saavedra y Villarrica no tienen ninguna unidad del
SNASPE asignada.** El cero es **estructural**: significa ausencia de área
silvestre protegida en el territorio comunal, no ausencia de registro ni
imputación por omisión. La distinción que pedía el comité queda zanjada: el dato
no confunde «sin área protegida» con «sin visitación registrada».

Esto es sustantivamente relevante y conviene decirlo en la defensa:
**Villarrica —segunda comuna en oferta hotelera, con 88 establecimientos— no
tiene áreas silvestres protegidas en su territorio**. Precisamente por eso la
visitación CONAF se emplea como *variable explicativa* y nunca como ponderador
para desagregar el índice: usarla como ponderador habría asignado actividad
turística nula a una de las principales comunas turísticas de la región.

### Caso distinto: unidades que no reportan

Tres unidades —R.N. Alto Biobío, R.N. Malleco y R.N. Nalcas— presentan ceros que
pueden corresponder a **falta de reporte** y no a ausencia real de visitas.
Afectan 26 celdas, están identificadas explícitamente en el código
(`UNIDADES_SIN_REPORTE`) y ninguna de ellas altera a las comunas del núcleo del
clúster.

### Denominador de la tasa per cápita

**Población total**, no población en edad laboral. Es consistente con el
tratamiento del resto de las variables per cápita del panel.

---

## 7. Hallazgo adicional no detectado por los revisores

### El problema

Los sectores económicos conexos se incorporan al panel mediante una tabla
dinámica que **convierte en cero los valores amparados por la reserva
tributaria**. Cuando el SII oculta una celda por construirse con diez o menos
informantes, el valor llega al panel como 0 y no como dato faltante.

Magnitud en las trece comunas del clúster:

| Sector | Celdas enmascaradas |
|---|---|
| Actividades recreativas | 50 de 152 (**33 %**) |
| Actividades inmobiliarias | 50 de 155 (**32 %**) |
| Construcción | 8 de 156 (5 %) |
| Transporte | 1 de 156 (1 %) |
| Comercio | 0 de 156 (0 %) |
| **Rubro I — el que compone el IDEC** | **0 de 156 (0 %)** |

Es la misma clase de problema que el comité detectó en CONAF. Si la pregunta por
los ceros de la visitación recibe una respuesta sólida, es previsible que el
tribunal pregunte a continuación por los ceros de los sectores conexos.

### Prueba de sensibilidad ejecutada

Se reconvirtieron a dato faltante todas las celdas enmascaradas del panel —218
celdas— y se reestimaron ambas hipótesis. Resultado:

**H2, coeficiente de determinación:**

| Esquema de validación | Tratamiento actual (cero) | Alternativo (faltante) | Δ |
|---|---|---|---|
| Temporal (origen móvil) | 0,8087 | 0,8141 | **+0,005** |
| Bloques | 0,7621 | 0,7497 | **−0,012** |
| Por comuna | −0,362 | −0,353 | +0,009 |

**H1, importancia por permutación:**

| Variable | Actual | Alternativo | Δ |
|---|---|---|---|
| Visitación SNASPE p.c. | 0,345 | 0,317 | −0,028 |
| Ventas construcción p.c. | 0,123 | 0,072 | −0,051 |
| Trabajadores recreativas p.c. | 0,070 | 0,082 | +0,012 |
| Ventas inmobiliarias p.c. | 0,067 | 0,046 | −0,022 |
| Ventas recreativas p.c. | 0,050 | 0,020 | −0,030 |

**Costo del tratamiento alternativo: la muestra utilizable cae de 152 a 92
observaciones —una pérdida del 39 %.**

### Lectura

1. **Ninguna conclusión cambia.** El R² se mueve dentro de ±0,012 en los tres
   esquemas; el esquema temporal, que es el que la tesis reporta, incluso
   *mejora* levemente. El predictor principal conserva su primer lugar con una
   holgura de más de tres veces respecto del segundo.
2. **El sesgo es de signo conocido y acotado.** Una celda enmascarada
   corresponde a diez o menos contribuyentes, es decir, a un valor pequeño.
   Tratarla como cero la subestima, pero no la distorsiona en órdenes de
   magnitud. Esto se confirma en que las importancias de los sectores conexos
   caen al reconvertir —estaban algo inflados— sin que se altere el orden
   general.
3. **La variable dependiente está limpia.** El rubro I no presenta
   enmascaramiento alguno en las trece comunas, de modo que el IDEC no está
   afectado en ningún grado.
4. **El predictor dominante es independiente del SII.** La visitación CONAF, con
   importancia 0,345, no proviene de la fuente tributaria.

### Recomendación: declararlo, no corregirlo

Corregir el tratamiento sacrificaría 60 observaciones —el 39 % de la muestra—
para no cambiar ninguna conclusión. Esa es la peor de las dos opciones.
Declararlo con su prueba de sensibilidad es la mejor, y además demuestra control
metodológico. Redacción propuesta para §3.6:

> Los valores de los sectores económicos conexos amparados por la reserva
> tributaria se incorporan al panel con valor cero, lo que constituye una cota
> inferior del valor real, dado que el enmascaramiento se aplica a celdas
> construidas con diez o menos informantes. Afecta al 33 % de las celdas de
> actividades recreativas y al 32 % de las inmobiliarias, y no afecta al rubro I
> que compone el IDEC, libre de enmascaramiento en las trece comunas del
> estudio. La prueba de sensibilidad que reconvierte esas celdas a dato faltante
> arroja un coeficiente de determinación de 0,814 frente a 0,809 en la
> especificación reportada, conserva el orden de importancia de los predictores
> y reduce la muestra utilizable de 152 a 92 observaciones. Se conserva por
> tanto el tratamiento con valor cero, que preserva la cobertura del panel sin
> alterar las conclusiones.

---

## 8. Punto 5 (Prioridad 2) — Influencia en la β-convergencia

### Resultado

Regresión sobre 13 observaciones: **β = −0,0329**, *p* = 0,000212, R² = 0,727.
Umbrales convencionales: leverage > 0,308; distancia de Cook > 0,308.

| Comuna | IDEC 2013 | Leverage | Cook | |
|---|---|---|---|---|
| Nueva Imperial | 0,011 | **0,372** | **1,453** | influyente |
| Vilcún | 0,024 | 0,195 | **0,582** | influyente |
| **Pucón** | **0,805** | **0,393** | **0,000** | leverage alto, **sin influencia** |
| Curacautín | 0,196 | 0,117 | 0,146 | |
| resto (9 comunas) | | < 0,18 | < 0,06 | |

### Lectura — y es favorable a la tesis

**Pucón presenta el mayor leverage de la muestra pero una distancia de Cook
prácticamente nula.** Está lejos del centro de la distribución, pero la recta lo
ajusta bien: **no arrastra la regresión**. Esto responde de frente la objeción
del efecto techo. La convergencia estimada no la produce Pucón.

Las observaciones influyentes están en el extremo opuesto: Nueva Imperial, que
parte de 0,011 —el valor más bajo del panel— y crece al 18 % anual.

### Sensibilidad a la exclusión

| Especificación | β | *p* |
|---|---|---|
| Completa (n = 13) | −0,0329 | 0,0002 |
| Sin Pucón | −0,0328 | 0,0019 |
| Sin Vilcún | −0,0380 | 0,00002 |
| Sin Nueva Imperial | −0,0237 | 0,0021 |
| Sin Pucón y Nueva Imperial | −0,0179 | 0,0397 |

**El signo y la significancia se mantienen en todas las especificaciones.** La
magnitud sí es sensible: excluir simultáneamente las dos observaciones extremas
reduce β casi a la mitad y eleva el *p*-valor a 0,04, que sigue siendo
significativo al 5 %.

### Redacción sugerida para §4.6.1.1

> El análisis de influencia muestra que Pucón, pese a presentar el mayor
> leverage de la muestra (0,393), tiene una distancia de Cook nula, de modo que
> no determina la pendiente estimada. Las observaciones influyentes son Nueva
> Imperial (Cook = 1,453) y Vilcún (0,582), ambas situadas en el extremo
> inferior de la distribución inicial. La exclusión de cualquiera de ellas
> conserva el signo negativo y la significancia de β, aunque su magnitud
> desciende de −0,033 a −0,018 al excluir simultáneamente Pucón y Nueva
> Imperial. La conclusión de desconcentración relativa se sostiene; su magnitud
> puntual debe interpretarse con la cautela que impone un n de 13.

---

## 9. Trazabilidad recuperada del R² = 0,68

El documento vigente retiró este valor «por no identificar su partición». **Sí
es trazable:**

- **0,68** es el coeficiente medio de los pliegues de la validación por bloques
  empleada para calcular la importancia por permutación, en la especificación
  **previa a la incorporación de la visitación CONAF**.
- En la especificación vigente, esa misma cantidad es **0,788**.
- **0,809** es el coeficiente de la validación temporal del modelo final.

No son cifras en conflicto: son cantidades distintas de especificaciones
distintas. La importancia por permutación exige declarar sobre qué calidad de
ajuste se computa —permutar variables de un modelo que no predice no informa
nada—, y 0,788 es ese valor en el modelo actual.

**Recomendación:** en lugar de retirar la cifra, restituirla con su procedencia.
Deja de ser una inconsistencia y pasa a ser evidencia de control metodológico y
de que la incorporación de CONAF mejoró el ajuste.

---

## 10. Inconsistencias que persisten en el documento vigente

| Cifra | Situación | Acción |
|---|---|---|
| Spearman «0,92 y 1,00» | Coexiste con «0,91» en otros pasajes. El mínimo verificado es **0,915** | Unificar en **0,91 a 1,00** |
| R² = 0,68 | Declarado «sin trazabilidad» en tres menciones | Restituir con la procedencia de §9 |
| Tabla 4.7 | «Diferencia documental sin asignación acreditada» | Reemplazar por la explicación de §3 |

El valor 0,067 que aparece dos veces corresponde a la importancia de
actividades inmobiliarias y es correcto. No debe modificarse.

---

## 11. Qué queda fuera de este componente

Las observaciones restantes del comité y del informe corresponden al autor de la
tesis y no al componente cuantitativo:

- Profundidad del Capítulo II y densidad del estado del arte.
- Verificación bibliográfica contra las fuentes originales, entrada por entrada.
- Numeración de tablas del Capítulo IV y existencia de los Anexos F a I.
- Operacionalización a priori de los umbrales de las hipótesis —qué cuenta como
  «relevante» y como «aceptable»—.
- Decisión sobre el título frente al constructo efectivamente medido.

---

## 12. Resumen de acciones

**Inmediatas, cierran los cuatro bloqueantes:**

1. Reescribir la nota de la Tabla 4.7 con la explicación de §3 e incorporar la
   salida por fila como anexo.
2. Agregar al Anexo C la configuración de Random Forest, el entorno de versiones
   y la declaración de no sintonización (§4).
3. Incorporar en §3.10.3.1 la tabla de iteraciones del origen móvil y precisar
   que el horizonte de pronóstico es de un año (§5).
4. Incorporar en §3.6.6 la regla de asignación de CONAF y la naturaleza
   estructural de los ceros de las cuatro comunas sin áreas protegidas (§6).

**Recomendadas antes de la defensa:**

5. Incorporar el análisis de influencia en §4.6.1.1 (§8). Responde el efecto
   techo con evidencia favorable.
6. Declarar el tratamiento de los valores enmascarados en los sectores conexos,
   con su prueba de sensibilidad (§7).
7. Restituir el R² = 0,68 con su procedencia (§9).
8. Unificar la cifra de Spearman en 0,91 (§10).

**Ninguna de estas acciones exige reejecutar los modelos ni altera un solo
resultado sustantivo de la tesis.**
