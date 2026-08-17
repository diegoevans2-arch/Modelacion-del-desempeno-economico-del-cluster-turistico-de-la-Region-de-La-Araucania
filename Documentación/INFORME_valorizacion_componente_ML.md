---
tipo: informe de valorización profesional
proyecto: Componente de Machine Learning — Tesis Doctoral Barra Ávila
elaborado por: Diego Evans Pérez Paz
fecha: 2026-08-14
---

# Informe de valorización — Componente de Machine Learning

## 1. Resumen ejecutivo

Este informe describe el producto desarrollado, el trabajo realizado y los
entregables del componente de Machine Learning de la tesis doctoral
*Modelación del desempeño económico del clúster turístico de la Región de La
Araucanía*, y propone una valorización profesional del servicio.

| | |
|---|---|
| **Período de ejecución** | 3 de junio – 14 de agosto de 2026 (≈ 10 semanas) |
| **Esfuerzo estimado** | 220 horas profesionales (rango 190–250) |
| **Código entregado** | 2.983 líneas de Python en 18 módulos |
| **Documentación técnica y académica** | 19.202 palabras |
| **Producto adicional** | Aplicación web desplegada y operativa |
| **Valorización propuesta** | **CLP 8.800.000** (rango CLP 5,5 – 12,1 millones) |

La cifra propuesta corresponde a tarifa profesional estándar. Las secciones 6 y
7 desglosan los tres escenarios considerados y los factores que justifican
situarse en uno u otro.

---

## 2. El producto entregado

No se trata de un script de análisis, sino de un **sistema completo y
reproducible** compuesto por cinco elementos:

**Un índice compuesto original.** El IDEC —Índice de Desempeño Económico del
Clúster— operacionaliza el desempeño de un clúster turístico a escala comunal
usando exclusivamente registros administrativos públicos, sin encuestas ni
levantamiento primario. Incluye validación de robustez ante cuatro métodos de
normalización.

**Un panel de datos comunal.** 156 observaciones balanceadas, trece comunas,
período 2013–2024, integrando cinco fuentes administrativas heterogéneas. Sin
datos faltantes en las variables clave y sin imputación.

**Un aporte metodológico propio.** El diagnóstico de degeneración del panel
detecta cuándo una desagregación territorial produce información aparente en
lugar de información real. Es un procedimiento replicable, aplicable a
cualquier investigación que combine datos públicos de distinta escala
geográfica, y constituye una contribución original de este trabajo.

**Un conjunto de modelos validados.** Cinco algoritmos supervisados evaluados
bajo cuatro esquemas de validación distintos, más modelos no supervisados con
selección objetiva del número de conglomerados y verificación de estabilidad.

**Una aplicación pública en operación.** Simulador interactivo que permite
consultar el desempeño comunal y proyectar escenarios de choques exógenos,
desplegado y accesible sin costo de infraestructura.

---

## 3. Trabajo realizado

### 3.1 Diagnóstico y rediseño metodológico

El estado inicial presentaba un problema estructural: la unidad de análisis
declarada era la comuna, pero la totalidad de las fuentes levantadas estaba
agregada a nivel regional. El panel disponible tenía un N efectivo de nueve
observaciones anuales replicadas, con dos de las cuatro dimensiones del índice
constantes o vacías.

Se identificó el riesgo —modelos con ajuste artificialmente alto por filas
duplicadas— y se rediseñó la arquitectura de datos sobre el principio de no
imputar lo que puede observarse.

### 3.2 Levantamiento e integración de fuentes

Cinco fuentes con dificultades técnicas específicas:

| Fuente | Complejidad resuelta |
|---|---|
| **SII** | Formato `.xlsb` binario, 15 MB; identificación de la estructura y del rubro CIIU pertinente |
| **BIP** | 1,2 GB procesados por bloques; extracción de la ejecución anual mediante análisis del campo textual `EBI_EJECUCION_PRESUPUESTARIA`, obteniendo 65.664 registros proyecto-año |
| **INE** | Formato ancho, codificación `latin-1`, transformación a panel largo |
| **SERNATUR** | CSV con registros malformados; normalización de nomenclatura comunal a código INE |
| **CONAF** | Extracción desde un reporte dinámico sin exportación directa, mediante análisis del servicio subyacente |

Se detectó y corrigió además un problema de cobertura en el BIP: los años sin
reporte completo habrían generado una caída ficticia de la inversión pública
que los modelos habrían interpretado como un choque real.

### 3.3 Ingeniería de variables

Construcción de rezagos, ventanas móviles y stock de capital por el método de
inventario perpetuo; normalización per cápita; derivación de indicadores de
intensidad turística e incorporación de sectores económicos conexos como
predictores exógenos.

### 3.4 Diagnóstico de validez territorial

Desarrollo del procedimiento de descomposición de varianza y de la métrica de
idiosincrasia, con verificación contra un caso deliberadamente degenerado.
Aplicado sistemáticamente a toda variable candidata antes de su incorporación
al modelo.

### 3.5 Construcción y validación del índice

Definición formal, normalización, agregación, análisis de sensibilidad ante
cuatro métodos alternativos y cálculo del índice de Theil con su evolución
temporal.

### 3.6 Modelación supervisada

Cinco modelos con roles diferenciados, incluida una regresión Ridge con
regularización validada para asegurar una comparación exigente. Cuatro
esquemas de validación —aleatorio, bloques temporales, temporal de origen móvil
y por comuna— con control automático de circularidad. Importancia de variables
por permutación fuera de muestra.

### 3.7 Modelación no supervisada

K-Means y clustering jerárquico, selección del número de conglomerados
mediante criterios convergentes —codo con detección objetiva y silueta—,
verificación de estabilidad por remuestreo y validación externa contra la
clasificación institucional de destinos turísticos. Pruebas de convergencia β y
σ con control de la falacia de Galton.

### 3.8 Variable de choques exógenos territoriales

Diseño e implementación de la variable CET solicitada durante el desarrollo,
incluyendo la detección de un modo de fallo silencioso —una variable constante
en entrenamiento habría tenido efecto nulo sin señal de error— y la
construcción de un modo estructural con elasticidad declarada y auditable,
calibrado empíricamente.

### 3.9 Despliegue

Desarrollo de la aplicación, y ante el cambio en las condiciones del proveedor
de alojamiento, reconstrucción completa como aplicación estática autocontenida
sin pérdida de funcionalidad, evitando un costo recurrente de suscripción.

### 3.10 Documentación y redacción académica

Redacción e integración de tres capítulos de la tesis, más notas metodológicas
y documentación de traspaso, con verificación de cada cifra contra las salidas
reproducibles del código.

---

## 4. Entregables

### 4.1 Código y datos

| Entregable | Detalle |
|---|---|
| Módulos Python | 18 archivos, 2.983 líneas |
| Panel integrado y resultados | 15 archivos CSV |
| Reproducibilidad | Todo el análisis se regenera con un comando |
| Control de versiones | 29 commits documentados |

### 4.2 Documentación (19.202 palabras)

| Documento | Palabras |
|---|---|
| Capítulo III — Metodología | 2.644 |
| Capítulo IV — Análisis de Resultados | 3.237 |
| Capítulo V — Conclusiones | 2.816 |
| Nota metodológica sobre desagregación | 1.409 |
| Referencias metodológicas (29 obras) | 1.169 |
| Documento de contexto técnico | 3.073 |
| Documento de entrega al autor | 2.117 |
| Documentación del repositorio | 2.737 |

Los tres capítulos están integrados en el documento de tesis con formato
consistente y tabla de contenido coherente.

### 4.3 Producto desplegado

Aplicación web pública con simulador de escenarios, explorador del panel
comunal y declaración de limitaciones, sin costo de infraestructura y con
procedimiento de actualización documentado.

---

## 5. Estimación de esfuerzo

| Fase | Horas |
|---|---|
| Diagnóstico y rediseño metodológico | 14 |
| Levantamiento e integración de cinco fuentes | 40 |
| Ingeniería de variables | 14 |
| Diagnóstico de validez territorial | 18 |
| Construcción y validación del índice | 18 |
| Modelación supervisada (H1, H2) | 22 |
| Modelación no supervisada (H3) | 22 |
| Variable de choques exógenos | 14 |
| Despliegue de la aplicación | 18 |
| Documentación y redacción académica | 40 |
| **Total** | **220** |

La estimación es consistente con las métricas observables: 2.265 líneas de
código de producción con documentación y validación, y 19.202 palabras de
redacción técnica y académica verificada.

---

## 6. Detalle de costos

> **Nota necesaria.** Los valores de mercado que siguen son estimaciones de
> referencia para el mercado chileno de ciencia de datos y **deben validarse**
> con cotizaciones comparables antes de presentar una propuesta formal. Las
> equivalencias en UF y dólares dependen del valor vigente a la fecha de
> emisión.

### Escenario A — Tarifa académica

Reconoce que el cliente es una persona natural y no una empresa.

| | |
|---|---|
| Tarifa horaria | CLP 25.000 |
| Horas | 220 |
| **Total** | **CLP 5.500.000** |

### Escenario B — Tarifa profesional estándar *(recomendado)*

Corresponde a consultoría de ciencia de datos con perfil senior.

| | |
|---|---|
| Tarifa horaria | CLP 40.000 |
| Horas | 220 |
| **Total** | **CLP 8.800.000** |

### Escenario C — Tarifa especializada

Reconoce el aporte metodológico original, el producto desplegado y la redacción
académica de nivel doctoral.

| | |
|---|---|
| Tarifa horaria | CLP 55.000 |
| Horas | 220 |
| **Total** | **CLP 12.100.000** |

### Desglose por componente, según escenario recomendado

| Componente | Horas | Valor (CLP) |
|---|---|---|
| Arquitectura de datos e integración de fuentes | 54 | 2.160.000 |
| Construcción y validación del índice | 32 | 1.280.000 |
| Aporte metodológico (diagnóstico de validez) | 18 | 720.000 |
| Modelación supervisada y no supervisada | 44 | 1.760.000 |
| Variable de choques exógenos | 14 | 560.000 |
| Desarrollo y despliegue de la aplicación | 18 | 720.000 |
| Documentación y redacción académica | 40 | 1.600.000 |
| **Total** | **220** | **8.800.000** |

---

## 7. Consideraciones para la propuesta

### 7.1 Factores que justifican la parte alta del rango

- **Aporte metodológico original.** El diagnóstico de degeneración no es
  aplicación de técnica conocida sino desarrollo propio, y queda declarado como
  contribución de la tesis.
- **Producto desplegado.** La aplicación es un entregable adicional al análisis,
  con valor de transferencia y citable en la defensa.
- **Redacción académica.** Tres capítulos completos con verificación de cifras,
  no un informe técnico que el autor deba después convertir en texto.
- **Reproducibilidad total.** El trabajo puede auditarse y actualizarse sin
  intervención del desarrollador.
- **Resultados publicables.** Los hallazgos de convergencia territorial tienen
  potencial de artículo académico derivado.

### 7.2 Factores que podrían moderar la cifra

- El cliente es una persona natural financiando estudios de posgrado, no una
  organización con presupuesto de consultoría.
- Existe una relación profesional previa que puede justificar condiciones
  preferentes.
- Parte del alcance surgió durante la ejecución —la variable CET y el despliegue
  no estaban en el encargo inicial—, lo que conviene explicitar antes que
  absorber silenciosamente.

### 7.3 Estructura de pago sugerida

Si la cifra completa resulta elevada de una vez, una alternativa razonable es
fraccionarla en tres cuotas asociadas a hitos ya cumplidos: entrega del panel y
del índice, entrega de los modelos y capítulos, y entrega del despliegue y la
documentación final.

---

## 8. Alcance no incluido

Conviene dejarlo explícito en la propuesta para evitar expectativas
posteriores:

- Capítulo I (El Problema) y Capítulo II (Marco Teórico).
- Verificación bibliográfica de las referencias en la fuente.
- Anexos, índices de tablas y figuras, y formato final del documento.
- Acompañamiento durante la defensa.
- Actualización del panel cuando se publiquen datos posteriores a 2024.

Estos dos últimos pueden ofrecerse como servicios adicionales con valorización
independiente.

---

## 9. Notas tributarias

La emisión mediante boleta de honorarios está sujeta a la retención vigente
para trabajadores independientes, cuya tasa ha venido incrementándose por
etapas conforme a la normativa. **Verificar el porcentaje aplicable a la fecha
de emisión** para calcular correctamente el monto líquido a recibir.

Si el pago se realiza contra factura, corresponde agregar el IVA sobre el valor
neto.

Conviene acordar con el cliente si la cifra convenida es bruta o líquida antes
de emitir el documento.

---

## 10. Recomendación

Se sugiere presentar el **Escenario B (CLP 8.800.000)** como valor de la
propuesta, indicando el desglose por componente de la sección 6 y el alcance no
incluido de la sección 8.

El desglose cumple dos funciones: transparenta que la cifra corresponde a
trabajo verificable y no a una estimación global, y permite al cliente
identificar qué componentes tienen mayor peso si necesitara ajustar el alcance.

En caso de requerirse una rebaja, es preferible reducir el alcance —por
ejemplo, excluyendo el despliegue de la aplicación o la redacción de uno de los
capítulos— antes que disminuir la tarifa horaria, que constituye la referencia
para trabajos futuros.
