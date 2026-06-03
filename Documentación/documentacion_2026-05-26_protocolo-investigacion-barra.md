---
date: 2026-05-26
tags: [documentacion, machine-learning, investigacion, turismo, araucania, doctorado, cluster]
status: done
type: documentacion
project: Protocolo-Doctorado-Barra
author: El Egypcio
---

# 📄 Protocolo de Investigación — Doctorado en Ciencias Económicas Empresariales

> **Presenta:** Germán Patricio Barra Ávila  
> **Asesor:** Dr. Alejandro Héctor Molina  
> **Institución:** TECH Universidad Tecnológica  
> **Fecha:** Santiago, marzo 2026

---

## 🎯 Título

**Modelación del desempeño económico del clúster turístico de la Región de La Araucanía mediante técnicas de [[machine-learning]] aplicadas a datos públicos para la toma de decisiones territoriales.**

---

## 1. 📌 Introducción

El turismo constituye uno de los sectores estratégicos para el desarrollo económico regional, especialmente en territorios con alta dotación de recursos naturales y culturales, como la Región de La Araucanía. La conformación de **clústeres turísticos** permite articular actores públicos y privados, generar economías de aglomeración y potenciar el desempeño económico territorial.

A pesar de la creciente disponibilidad de datos públicos del sector turístico, su uso mediante metodologías analíticas avanzadas sigue siendo limitado. Las técnicas de [[machine-learning]] han adquirido relevancia al identificar patrones complejos, relaciones no lineales y comportamientos emergentes a partir de grandes volúmenes de datos.

**Concepto central:** El desempeño económico del clúster turístico se entiende como una construcción analítica basada en la combinación de indicadores de actividad turística, empleo, ingresos y dinamismo territorial, obtenidos a partir de fuentes públicas oficiales.

---

## 2. 🔍 Definición del Problema de Investigación

La evaluación del desempeño económico del clúster turístico regional se ha basado principalmente en **análisis descriptivos y enfoques tradicionales**, que no logran capturar la complejidad de las interacciones entre variables económicas, territoriales y productivas.

Existe una brecha metodológica: ausencia de modelos integrados que permitan analizar y modelar el desempeño económico del clúster turístico usando técnicas de ML aplicadas a datos públicos.

Para operacionalizar la variable dependiente se define el:

> 📊 **IDEC — Índice de Desempeño Económico del Clúster**  
> Indicador compuesto que integra: actividad turística, empleo sectorial, generación de ingresos y capacidad productiva. Obtenido de fuentes públicas oficiales.

### ❓ Pregunta de Investigación

> ¿En qué medida la aplicación de técnicas de Machine Learning a datos públicos permite modelar con mayor precisión predictiva que enfoques tradicionales el desempeño económico del clúster turístico de la Región de La Araucanía para apoyar la toma de decisiones territoriales?

---

## 3. ✅ Justificación

| Dimensión | Descripción |
|---|---|
| 🎓 **Académica** | Integra economía regional, análisis de clústeres y ML. Pertinente al Doctorado en Ciencias Económicas Empresariales. |
| 🌿 **Social y territorial** | Aporta evidencia para políticas públicas orientadas al desarrollo sostenible y cohesión territorial en La Araucanía. |
| 🔬 **Metodológica** | Datos públicos abiertos: replicabilidad, transparencia, alineación con gobierno abierto. |
| ⚙️ **Viabilidad** | Acceso a fuentes oficiales (INE, SERNATUR, Banco Central) y herramientas de código abierto. |

---

## 4. 🎯 Objetivos

### 4.1 Objetivo General

> Modelar y evaluar comparativamente el desempeño económico del clúster turístico de la Región de La Araucanía mediante técnicas de Machine Learning aplicadas a datos públicos, con el fin de apoyar la toma de decisiones territoriales.

### 4.2 Objetivos Específicos

1. Identificar las variables económicas y territoriales relevantes del clúster turístico de La Araucanía a partir de fuentes de datos públicos.
2. Aplicar técnicas de ML para estimar y predecir el desempeño económico del clúster.
3. Analizar los patrones y relaciones identificados por los modelos en el comportamiento del clúster.
4. Determinar el aporte de los modelos desarrollados para la toma de decisiones territoriales basadas en evidencia.

### 4.3 Meta del Estudio

Modelo capaz de **predecir tendencias económicas** y **clasificar el desempeño del clúster**, permitiendo a los tomadores de decisiones anticiparse a crisis de estacionalidad y optimizar la inversión pública.

---

## 5. 💡 Hipótesis

### Hipótesis General

> La aplicación de técnicas de ML a datos públicos permite modelar de manera significativa el desempeño económico del clúster turístico de La Araucanía, con mayor precisión predictiva que modelos econométricos tradicionales, generando evidencia empírica relevante para la toma de decisiones territoriales.

### Hipótesis Específicas

**H1:** Las variables económicas y territoriales obtenidas de fuentes públicas presentan una relación estadísticamente significativa, potencialmente no lineal, con el IDEC.

| Indicadores H1 |
|---|
| Llegadas y pernoctaciones turísticas |
| Empleo en alojamiento y servicios turísticos |
| Ingresos turísticos estimados (Cuenta Satélite de Turismo) |
| Capacidad y ocupación de alojamiento |

---

**H2:** Los modelos de aprendizaje supervisado permiten estimar el IDEC con niveles de error predictivo aceptables.

| Métricas H2 |
|---|
| MAE — Error Absoluto Medio |
| RMSE — Error Cuadrático Medio |
| R² — Coeficiente de Determinación |

---

**H3:** Las técnicas de aprendizaje no supervisado permiten identificar patrones y agrupamientos territoriales diferenciados dentro del clúster.

| Indicadores H3 |
|---|
| Número de clústeres identificados |
| Coeficiente de silueta |
| Homogeneidad intra-clúster y heterogeneidad inter-clúster |

---

## 6. 🔬 Metodología

### 6.1 Paradigma y Enfoque

- **Paradigma:** Positivista
- **Enfoque:** Cuantitativo, orientado al análisis empírico y modelación predictiva

### 6.2 Tipo de Investigación

Estudio aplicado, no experimental, de alcance **explicativo y predictivo**, basado en análisis secundario de datos públicos.

### 6.3 Población y Muestra

- **Población:** Comunas del clúster turístico de La Araucanía
- **Muestra:** Comunas con información pública disponible y consistente en el período de estudio

### 6.4 Fuentes de Datos

| Fuente | Datos |
|---|---|
| **INE** | Encuesta Mensual de Alojamiento Turístico (EMAT) |
| **SERNATUR** | Llegada de turistas, tasa de ocupabilidad, prestadores de servicios turísticos |
| **Banco Central / Hacienda** | PIB regional, inversión pública, gasto promedio por turista |
| **Datos Abiertos** | Infraestructura vial, datos meteorológicos, eventos culturales |

### 6.5 Variables

**Variable Dependiente:**  
→ `IDEC` — Índice de Desempeño Económico del Clúster

**Variables Independientes:**
- Oferta turística
- Demanda turística
- Empleo turístico
- Inversión pública
- Factores territoriales (conectividad, estacionalidad, infraestructura)

### 6.6 Unidad de Análisis

**Comuna** como unidad territorial básica. Datos estructurados en formato **panel** (series temporales por comuna).

---

## 7. 📐 Técnicas de Análisis

### Fase 1 — Construcción del IDEC

El IDEC integra 4 dimensiones: Actividad turística · Empleo sectorial · Generación de ingresos · Capacidad productiva

**Normalización Min-Max:**

$$Z_{kjit} = \frac{X_{kjit} - \min(X_{kj})}{\max(X_{kj}) - \min(X_{kj})}$$

**Agregación por dimensión:**

$$D_{kit} = \frac{1}{m_k} \sum_{j=1}^{m_k} Z_{kjit}$$

**Construcción del IDEC:**

$$IDEC_{it} = \frac{1}{4}(D_{1it} + D_{2it} + D_{3it} + D_{4it})$$

> 💡 Ponderaciones iguales → transparencia metodológica y replicabilidad. Se realizará análisis de sensibilidad: Min-Max vs Z-score y esquemas alternativos de ponderación.

---

### Fase 2 — Modelación Predictiva (Aprendizaje Supervisado)

Modelos a aplicar sobre el IDEC como variable dependiente (datos panel):

| Modelo | Rol |
|---|---|
| Regresión Lineal Múltiple | Modelo base comparativo |
| Árboles de Decisión | Relaciones no lineales |
| [[random-forest]] | Interacciones complejas |

**Evaluación predictiva:** MAE · RMSE · R²  
**Validación:** K-fold cross-validation · Partición train/test

---

### Fase 3 — Agrupamiento y Desigualdad Territorial (No Supervisado)

Algoritmos:
- [[k-means]]
- Clustering jerárquico (según pertinencia exploratoria)

**Evaluación del clustering:** Coeficiente de silueta · Índice de Davies-Bouldin · Cohesión intra-clúster · Separación inter-clúster

**Índice de Theil (desigualdad territorial):**

$$T = \frac{1}{N} \sum_{i=1}^{N} \frac{IDEC_{it}}{\bar{IDEC}_t} \ln \frac{IDEC_{it}}{\bar{IDEC}_t}$$

> Permite medir dispersión territorial y analizar desigualdad intra e interregional.

---

## 8. 🛡️ Validación y Robustez

| Dimensión | Estrategia |
|---|---|
| **Predictiva** | MAE, RMSE, R² + validación cruzada K-fold + train/test split |
| **Estructural** | Coeficiente de silueta + métricas de cohesión/separación del clustering |
| **Robustez del IDEC** | Análisis de sensibilidad: esquemas de ponderación, métodos de normalización, períodos temporales |

---

## 9. 📅 Cronograma

| Período | Capítulo | Descripción |
|---|---|---|
| I Trimestre | Protocolo | Formulación del anteproyecto de investigación |
| II Trimestre | Cap. I: El Problema | Contexto, justificación, objetivos, hipótesis |
| II Trimestre | Cap. II: Marco Teórico | Revisión exhaustiva de literatura |
| II Trimestre | Cap. III: Marco Conceptual | Variables, dimensiones, modelo conceptual |
| III Trimestre | Cap. IV: Metodología | Diseño detallado, herramientas y técnicas |
| III Trimestre | Cap. V: Análisis de Resultados | Implementación y análisis |
| IV Trimestre | Cap. VI: Conclusiones | Hallazgos, refutación/confirmación de hipótesis |

> ⏱ **Fecha de entrega final: 10 DIC 2026**

---

## 10. ⚖️ Consideraciones Éticas

El estudio utiliza exclusivamente **datos públicos**, sin información personal sensible, cumpliendo principios éticos de investigación científica.

---

## 📚 Referencias

- Aghion, P., Jones, B. F., & Jones, C. I. (2019). *Artificial intelligence and economic growth.* Journal of Economic Perspectives, 33(2), 163–190.
- Banco Mundial. (2021). *World Development Report 2021: Data for Better Lives.*
- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning.* Springer.
- Breiman, L. (2001). *Random forests.* Machine Learning, 45(1), 5–32.
- CEPAL. (2019). *Desarrollo territorial en América Latina y el Caribe.*
- Dolnicar, S., Grün, B., & Leisch, F. (2018). *Market Segmentation Analysis.* Springer.
- Fagerberg, J., & Srholec, M. (2008). *National innovation systems, capabilities and economic development.* Research Policy, 37(9), 1417–1435.
- Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning* (2nd ed.). Springer.
- INE. (2023). *Estadísticas regionales.* Instituto Nacional de Estadísticas.
- Li, X., Pan, B., Law, R., & Huang, X. (2017). *Forecasting tourism demand with composite search index.* Tourism Management, 59, 57–66.
- López, M., & Palomino, H. (2020). *Clústeres productivos y desarrollo regional: evidencia para Chile.* Revista CEPAL, 131, 87–106.
- Ministerio de Economía. (2022). *Cuenta Satélite de Turismo de Chile.*
- OECD. (2018). *OECD Regions and Cities at a Glance 2018.*
- OECD. (2020). *Machine Learning and Artificial Intelligence in Public Policy.*
- Porter, M. E. (1998). *Clusters and the new economics of competition.* Harvard Business Review, 76(6), 77–90.
- Russell, S. J., & Norvig, P. (2021). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.
- Varian, H. R. (2019). *Artificial intelligence, economics, and industrial organization.* En Agrawal, Gans & Goldfarb (Eds.), *The Economics of Artificial Intelligence.* University of Chicago Press.
