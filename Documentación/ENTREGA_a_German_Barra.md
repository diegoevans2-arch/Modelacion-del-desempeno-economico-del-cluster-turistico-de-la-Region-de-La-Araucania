---
tipo: documento de entrega
destinatario: Germán Patricio Barra Ávila
asunto: Componente de Machine Learning de la tesis doctoral
fecha: 2026-08-14
---

# Entrega del componente de Machine Learning

Germán:

Este documento resume lo que queda entregado del componente cuantitativo de tu
tesis, qué significa cada resultado, qué decisiones metodológicas conviene que
puedas explicar en la defensa, y qué queda pendiente de tu lado.

Está escrito para leerse completo en unos veinte minutos. Al final hay un mapa
de dónde está cada archivo.

---

## 1. Qué queda entregado

| Componente | Estado |
|---|---|
| Panel comunal 2013–2024, cinco fuentes públicas | 156 observaciones, 13 comunas, sin datos faltantes |
| IDEC — Índice de Desempeño Económico del Clúster | Construido y validado |
| Diagnóstico de validez territorial del panel | Desarrollado para esta investigación |
| Hipótesis H1, H2 y H3 | Contrastadas |
| Variable CET — choques exógenos territoriales | Implementada y calibrada |
| Capítulos III, IV y V | Redactados e integrados en la tesis |
| Referencias metodológicas | 29 incorporadas (total: 61) |
| Simulador público | En línea |
| Código reproducible | Todo el análisis se regenera con un comando |

El simulador está disponible en
`https://huggingface.co/spaces/diegoevans2-arch/idec-araucania`
y puede citarse en la defensa como producto de transferencia.

---

## 2. Los tres hallazgos, en una página

**Primero: existe una jerarquía clara de variables asociadas al desempeño.**
La visitación a áreas silvestres protegidas es, con distancia, la variable de
mayor capacidad explicativa (importancia 0,345), seguida de las actividades de
construcción e inmobiliarias (0,190 en conjunto). La inversión pública agregada
no muestra señal detectable.

**Segundo: el Machine Learning predice mejor que los enfoques tradicionales,
pero sólo en el tiempo.** Random Forest alcanza un R² de 0,809 pronosticando
años futuros de comunas conocidas, frente a 0,24 de la regresión Ridge y 0,05
de la regresión lineal. En cambio, ningún modelo logra predecir una comuna que
no vio en el entrenamiento.

**Tercero: el clúster se está desconcentrando.** El índice de Theil cae 53,5 %
entre 2013 y 2024, con una prueba de β-convergencia que lo confirma
(β = −0,033; *p* = 0,0002). El motor no es el deterioro de Pucón sino el
crecimiento de la Araucanía Andina: Curacautín +134 %, Melipeuco +111 %,
Lonquimay +108 %.

Este tercer hallazgo es el más fuerte de la tesis y tiene **validación
externa**: la Reserva Nacional Malalcahuello pasó de 84.539 visitantes en 2013
a 297.623 en 2024 (+252 %). Son conteos físicos de guardaparques, sin ninguna
relación con las declaraciones tributarias que componen el IDEC, y apuntan al
mismo fenómeno. Cuando dos registros independientes coinciden, el hallazgo deja
de ser un artefacto del método.

---

## 3. Cinco decisiones que conviene poder explicar

### 3.1 Por qué el IDEC tiene tres dimensiones y no cuatro

El diseño original contemplaba cuatro: actividad turística, empleo, ingresos y
capacidad. Las tres últimas se construyeron con datos comunales observados. La
primera no.

No fue una omisión. Se evaluaron **nueve esquemas** distintos para desagregar
la serie regional de la EMAT a nivel comunal, y ninguno resultó válido. Los
ponderadores con dinámica turística real provienen del SII —la misma fuente de
las dimensiones de empleo e ingresos—, con correlaciones de +0,54 a +0,83: el
índice habría contado dos veces la misma información. Los ponderadores
independientes, como la población, no contienen información turística: en 2020
las llegadas cayeron 57 % y ninguna población comunal cayó en esa magnitud.

Se verificó además directamente en la fuente que la EMAT **sí tiene** apertura
por destino turístico —con cuatro destinos para La Araucanía que casi calcan la
definición del clúster—, pero el propio reporte declara que esa apertura está
**suspendida desde abril de 2020** por el cierre de más del 50 % de los
establecimientos durante la pandemia. Desaparece justo en el período que
concentra la información de choque.

Todo esto está documentado en `Nota_metodologica_D1_desagregacion.md`, con las
cifras de cada ensayo. Es el respaldo si alguien pregunta.

### 3.2 Por qué el modelo no predice comunas nuevas

Con trece unidades territoriales no hay base suficiente para aprender una
relación transferible entre comunas. El modelo aprende el nivel característico
de cada territorio, no una regla general.

Esto se declara explícitamente en lugar de ocultarlo. La alternativa habría
sido mostrar sólo la validación cruzada aleatoria, que en datos panel arroja un
R² de 0,80 porque mezcla años contiguos de la misma comuna —información que el
modelo ya vio—. Presentar ese número como capacidad predictiva habría sido
engañoso.

### 3.3 Por qué la comparación con los modelos lineales es justa

Se incorporó deliberadamente una regresión Ridge con parámetro de
regularización validado, para que el enfoque econométrico compitiera en su
mejor versión. Los modelos lineales **no fracasan**: alcanzan R² de 0,48 a 0,56
bajo validación aleatoria y de bloques. Pierden capacidad específicamente
cuando se les exige extrapolar a años no observados, que es el uso relevante.

Esto importa: demostrar que Random Forest supera a un contendiente que funciona
es un argumento mucho más sólido que superarlo cuando está mal especificado.

### 3.4 Por qué la convergencia no es un artefacto estadístico

La crítica clásica a las pruebas de convergencia es la falacia de Galton: una
regresión a la media puede simular convergencia sin que la dispersión
disminuya realmente.

Por eso se contrastan **las dos formas de manera conjunta**: la σ-convergencia
(caída del índice de Theil, 53,5 %, *p* < 10⁻⁶) y la β-convergencia (las
comunas rezagadas crecen más rápido, *p* = 0,0002). Que ambas coincidan es lo
que descarta la falacia. La referencia es Quah (1993), ya incorporada a la
bibliografía.

Adicionalmente, la caída del Theil se mantiene entre 46 % y 67 % según el
método de normalización, y persiste incluso sobre las ventas comunales sin
normalizar. No depende de cómo se construyó el índice.

### 3.5 Qué significa que la inversión pública no muestre señal

Significa **que no se detecta relación**, no que la relación no exista. Tres
razones justifican esa cautela, y conviene enunciarlas antes de que las
pregunten:

1. El Banco Integrado de Proyectos registra *toda* la inversión pública
   —vialidad, educación, saneamiento—, no la de vocación turística.
2. La estructura de rezagos podría ser distinta de la supuesta.
3. Con trece comunas la potencia estadística es limitada.

Establecer causalidad requeriría un diseño específico —variables
instrumentales, discontinuidades presupuestarias— que excede el alcance de esta
tesis. Así queda planteado en las líneas futuras.

---

## 4. Preguntas probables del tribunal

**«¿Por qué el panel llega sólo hasta 2024?»**
Porque es la última anualidad publicada. El SII difunde por año comercial con
unos dieciocho meses de rezago: el año 2024 quedó disponible en noviembre de
2025. Se verificó contra el servidor que no existe versión más reciente. Es una
restricción común a toda investigación con registros tributarios comunales en
Chile, y está declarada en las limitaciones.

**«¿Por qué trece comunas y no las treinta y dos de la región?»**
El clúster se delimitó con un criterio institucional externo: los Destinos
Turísticos oficiales que SERNATUR reconoce en su Registro Nacional de
Prestadores. El núcleo son ocho comunas y concentra el 83 % de la oferta formal
regional; las cinco restantes conforman un anillo con oferta relevante y se
emplean en el análisis de sensibilidad. No es un umbral elegido por el
investigador.

**«¿Cómo se evita que el modelo se explique a sí mismo?»**
Ningún componente del IDEC puede usarse como predictor. El código verifica esa
condición automáticamente y aborta la estimación si algún componente se filtra.
Los predictores son la visitación a áreas protegidas, la inversión pública, los
sectores económicos conexos y la demografía, todos exógenos al índice.

**«¿Por qué normalizar per cápita?»**
Porque en niveles el índice ordenaría las comunas por tamaño demográfico. Con
la normalización, Temuco pasa del primer al cuarto lugar y las comunas de
vocación turística ascienden. El ordenamiento resultante coincide con la
intensidad de oferta hotelera medida por SERNATUR, que es una fuente
independiente: eso valida la decisión.

**«¿El índice depende del método de normalización elegido?»**
No. Se probaron cuatro métodos —Min-Max, Min-Max logarítmico, Z-score y rango
percentil— y las correlaciones de Spearman entre los ordenamientos resultantes
se sitúan entre 0,91 y 1,00.

**«¿Cuál es el aporte metodológico original?»**
El diagnóstico de degeneración del panel. Buena parte de la información
turística oficial se publica a escala regional mientras las decisiones se toman
a escala comunal, y la tentación es desagregar. El procedimiento desarrollado
demuestra numéricamente cuándo esa desagregación produce información aparente:
descompone la varianza en efectos de comuna, tiempo e interacción, y mide qué
fracción de la variación temporal es propia de cada territorio. Aplicado a un
caso deliberadamente degenerado da cero exacto. Es un protocolo replicable para
cualquier investigación que combine datos públicos de distinta escala.

---

## 5. Qué queda pendiente de tu lado

Esto no fue abordado en el componente de Machine Learning:

| Componente | Estado actual | Comentario |
|---|---|---|
| **Capítulo II — Marco Teórico** | 1.426 palabras | Es el punto más débil del documento: catorce secciones, incluidos tres estados del arte, en poco más de mil cuatrocientas palabras. Un tribunal doctoral lo mirará con atención. |
| **Capítulo I — El Problema** | 1.690 palabras | Cumple, pero está ajustado. |
| **Verificación de referencias** | 61 entradas | Las 29 metodológicas nuevas deben comprobarse en la fuente: volumen, número, páginas y DOI. Ver §6. |
| **Anexos** | Ausentes | Hay material disponible: salidas del diagnóstico, tablas de sensibilidad, código. |
| **Índices de tablas y figuras** | Ausentes | — |
| **Tabla de contenido** | Desactualizada | En Word: clic derecho sobre el índice → *Actualizar toda la tabla*, para que aparezcan las secciones 5.1 a 5.8. |

---

## 6. Lo que debes verificar antes de la defensa

**Las referencias metodológicas.** Se incorporaron 29 obras canónicas de los
métodos empleados, organizadas por método en
`Referencias_metodologicas.md` con indicación del apartado que las usa. Son
obras ampliamente conocidas, pero **cada entrada debe comprobarse en la
fuente**. Un dato equivocado en una cita es exactamente el tipo de detalle que
un tribunal detecta. Revisa con especial cuidado Nardo et al. (2005) y
Goldsmith (1951), que son informes técnicos y capítulos de libro cuyos datos de
publicación varían entre ediciones.

**El documento en Word.** Abre la tesis y comprueba que las tablas 4.3 y 4.4 se
vean correctamente, que la numeración de las limitaciones vaya del 1 al 5, y
que los títulos del Capítulo V tengan el formato de los capítulos anteriores.

**Las cifras.** Todas las que aparecen en los Capítulos III, IV y V fueron
verificadas contra las salidas del código. Si modificas algún número, conviene
recalcularlo en lugar de ajustarlo a mano: basta ejecutar `python -m
src.build_panel` y volver a mirar los archivos de `BBDD/final/`.

---

## 7. Cómo actualizar el trabajo en el futuro

Cuando el SII publique el año comercial 2025 —previsiblemente a fines de
2026— extender el panel es mecánico:

```bash
# 1. Descargar el archivo actualizado del SII a la carpeta de datos
# 2. Regenerar el panel y todos los resultados
python -m src.build_panel

# 3. Actualizar el simulador público
python -m deploy_static.generar_datos
python deploy_static/publicar.py --publicar
```

Los resultados de las tres hipótesis se recalculan solos. Lo único que hay que
hacer a mano es actualizar las cifras en el documento.

---

## 8. Dónde está cada cosa

```
Documentación/
├── ENTREGA_a_German_Barra.md            ← este documento
├── Capitulo_III_Metodologia.md          borrador fuente del capítulo
├── Capitulo_IV_Resultados.md            borrador fuente del capítulo
├── Capitulo_V_Conclusiones.md           borrador fuente del capítulo
├── Referencias_metodologicas.md         las 29 referencias, por método
├── Nota_metodologica_D1_desagregacion.md respaldo del cierre de D1
├── CONTEXTO_PROYECTO_handoff.md         contexto técnico detallado
└── Tesis_Doctoral_Barra_Avila_Version_29.07.2026.docx

BBDD/final/          resultados de las tres hipótesis
src/                 código reproducible
deploy_static/       aplicación publicada
```

Los datos crudos no están en el repositorio por su volumen; viven en la carpeta
externa indicada en `src/config.py`.

---

## 9. Una observación final

El resultado del que más conviene apropiarse no es el R² ni el índice de Theil,
sino la decisión de haber preferido un índice de tres dimensiones observadas
antes que uno de cuatro con una dimensión imputada.

La disponibilidad creciente de datos abiertos convive con una asimetría
persistente: la información se publica en la escala en que se produce, no en
aquella en que se decide. Frente a esa asimetría lo fácil es desagregar. Esta
investigación muestra, con evidencia numérica, que hacerlo mediante
ponderadores fijos genera una apariencia de información territorial donde no la
hay.

Renunciar a la cuarta dimensión costó completitud formal. A cambio, ninguna
conclusión de esta tesis descansa sobre un dato inventado. Eso es defendible
ante cualquier tribunal, y es más de lo que puede decir buena parte de la
literatura que trabaja con datos públicos desagregados.

Éxito en la defensa.
