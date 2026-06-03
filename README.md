# Modelación del Desempeño Económico del Clúster Turístico de la Región de La Araucanía mediante Técnicas de Machine Learning

> **Investigación Doctoral** · Doctorado en Ciencias Económicas Empresariales  
> TECH Universidad Tecnológica · Santiago, 2026

---

## Resumen

Esta investigación aplica técnicas de Machine Learning supervisado y no supervisado para modelar y evaluar el desempeño económico del clúster turístico de la Región de La Araucanía (Chile), utilizando exclusivamente datos públicos oficiales. El estudio introduce el **IDEC** (*Índice de Desempeño Económico del Clúster*), un indicador compuesto que integra actividad turística, empleo sectorial, generación de ingresos y capacidad productiva a nivel comunal. La hipótesis central postula que los modelos de ML logran una precisión predictiva superior a los enfoques econométricos tradicionales, generando evidencia accionable para la toma de decisiones territoriales.

---

## Ficha del Estudio

| Atributo | Detalle |
|---|---|
| **Autor** | Germán Patricio Barra Ávila |
| **Director** | Dr. Alejandro Héctor Molina |
| **Institución** | TECH Universidad Tecnológica |
| **Programa** | Doctorado en Ciencias Económicas Empresariales |
| **Área de estudio** | Región de La Araucanía, Chile |
| **Unidad de análisis** | Comuna (datos panel: series temporales por comuna) |
| **Período cubierto** | 2013 – 2025 |
| **Fuentes de datos** | INE · SERNATUR · Banco Central · BIP · ENE |
| **Paradigma** | Positivista · Cuantitativo · Explicativo-Predictivo |
| **Entrega final** | 10 de diciembre de 2026 |

---

## Pregunta de Investigación

> *¿En qué medida la aplicación de técnicas de Machine Learning a datos públicos permite modelar con mayor precisión predictiva que enfoques tradicionales el desempeño económico del clúster turístico de la Región de La Araucanía, para apoyar la toma de decisiones territoriales?*

---

## Hipótesis

| # | Hipótesis | Métricas de validación |
|---|---|---|
| **H1** | Las variables económicas y territoriales de fuentes públicas presentan una relación estadísticamente significativa, potencialmente no lineal, con el IDEC | Análisis de correlación · Pruebas de no linealidad |
| **H2** | Los modelos de aprendizaje supervisado estiman el IDEC con niveles de error predictivo aceptables | MAE · RMSE · R² |
| **H3** | Las técnicas no supervisadas identifican agrupamientos territoriales diferenciados dentro del clúster | Coeficiente de silueta · Índice de Davies-Bouldin |

---

## Metodología

### Fase 1 — Construcción del IDEC

El IDEC integra cuatro dimensiones mediante normalización Min-Max y agregación de igual ponderación:

$$IDEC_{it} = \frac{1}{4}\left(D_{1it} + D_{2it} + D_{3it} + D_{4it}\right)$$

Donde cada dimensión $D_{k}$ agrega indicadores normalizados:

$$D_{kit} = \frac{1}{m_k} \sum_{j=1}^{m_k} Z_{kjit}, \quad Z_{kjit} = \frac{X_{kjit} - \min(X_{kj})}{\max(X_{kj}) - \min(X_{kj})}$$

**Dimensiones:** Actividad turística · Empleo sectorial · Generación de ingresos · Capacidad productiva

> Se realizará análisis de sensibilidad comparando normalización Min-Max vs Z-score y esquemas alternativos de ponderación.

---

### Fase 2 — Modelación Predictiva (Aprendizaje Supervisado)

| Modelo | Rol |
|---|---|
| Regresión Lineal Múltiple | Modelo base comparativo |
| Árboles de Decisión | Relaciones no lineales |
| Random Forest | Interacciones complejas entre variables |

**Validación:** K-fold cross-validation · Train/test split · MAE · RMSE · R²

---

### Fase 3 — Agrupamiento Territorial (Aprendizaje No Supervisado)

**Algoritmos:** K-Means · Clustering jerárquico (según pertinencia exploratoria)

**Evaluación:** Coeficiente de silueta · Índice de Davies-Bouldin · Cohesión intra-clúster · Separación inter-clúster

**Desigualdad territorial** medida con el Índice de Theil:

$$T = \frac{1}{N} \sum_{i=1}^{N} \frac{IDEC_{it}}{\overline{IDEC}_t} \ln \frac{IDEC_{it}}{\overline{IDEC}_t}$$

---

## Base de Datos Integrada

Se construyó una **Base Maestra Integrada** para el período 2013–2025, consolidando cinco fuentes oficiales de información pública con distintas periodicidades (mensual, trimestral y anual), homologadas a nivel comunal.

### Consolidado de Variables

| Dimensión IDEC | Variable | Fuente | Periodicidad |
|---|---|---|---|
| Actividad turística | Llegadas | EMAT – INE | Mensual |
| Actividad turística | Pernoctaciones | EMAT – INE | Mensual |
| Actividad turística | Tasa de ocupación | EMAT – INE | Mensual |
| Generación de ingresos | ADR *(Average Daily Rate)* | EMAT – INE | Mensual |
| Generación de ingresos | RevPAR *(Revenue per Available Room)* | EMAT – INE | Mensual |
| Empleo sectorial | Empleo turístico | ENE – INE | Trimestral |
| Capacidad productiva | Alojamientos registrados | SERNATUR | Anual |
| Contexto económico | PIB Regional | Banco Central | Anual |
| Inversión pública | Gasto vigente BIP | BIP – MDS | Anual |

### Logros Alcanzados en la Recopilación

- Se identificaron y procesaron **cinco fuentes oficiales** de información pública.
- Se construyó la **Base Maestra Integrada** para el período 2013–2025.
- Se definió y operacionalizó el **IDEC** con sus cuatro dimensiones componentes.
- Se homologaron fuentes con distintas periodicidades (mensual, trimestral y anual).
- Se integró la **inversión pública regional** proveniente del Banco Integrado de Proyectos (BIP).
- La base se encuentra en condiciones suficientes para iniciar el análisis estadístico y la aplicación de modelos de Machine Learning.

---

## Hoja de Ruta

```
Construcción definitiva del IDEC → Análisis descriptivo → Correlaciones →
Regresión múltiple → Random Forest → Clustering → Índice de Theil →
Redacción de Capítulos V, VI y VII
```

| Trimestre | Etapa | Estado |
|---|---|---|
| Q1 2026 | Protocolo de investigación | ✅ Completo |
| Q1–Q2 2026 | Capítulo I — El Problema | ✅ Completo |
| Q2 2026 | Capítulo II — Marco Teórico | ✅ Completo |
| Q2 2026 | Capítulo III — Marco Conceptual | ✅ Completo |
| Q2 2026 | Capítulo IV — Metodología | ✅ Completo |
| Q2–Q3 2026 | **Recopilación y preparación de datos** | 🔄 En progreso |
| Q3 2026 | Capítulo V — Análisis de Resultados | ⏳ Pendiente |
| Q4 2026 | Capítulo VI — Conclusiones | ⏳ Pendiente |

> **Fecha de entrega final: 10 de diciembre de 2026**

---

## Estructura del Repositorio

```
.
├── data/
│   ├── raw/                  # Datasets públicos originales (sin modificar)
│   │   ├── emat/             # Encuesta Mensual de Alojamiento Turístico (INE)
│   │   ├── ene/              # Encuesta Nacional de Empleo (INE)
│   │   ├── sernatur/         # Prestadores y alojamientos registrados
│   │   ├── banco_central/    # PIB regional
│   │   └── bip/              # Gasto vigente inversión pública
│   ├── processed/            # Datasets limpios y normalizados
│   └── final/                # Base Maestra Integrada lista para modelación
├── notebooks/
│   ├── 01_recopilacion_datos.ipynb
│   ├── 02_construccion_idec.ipynb
│   ├── 03_analisis_descriptivo.ipynb
│   ├── 04_modelos_supervisados.ipynb
│   ├── 05_clustering_territorial.ipynb
│   └── 06_analisis_resultados.ipynb
├── src/
│   ├── preprocessing/        # Limpieza y normalización
│   ├── features/             # Ingeniería de variables
│   ├── models/               # Entrenamiento y evaluación
│   └── visualization/        # Gráficos y mapas territoriales
├── reports/
│   └── figures/              # Gráficos y tablas generados
├── requirements.txt
└── README.md
```

---

## Stack Tecnológico

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=flat&logo=jupyter&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?style=flat&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?style=flat&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-1.x-013243?style=flat&logo=numpy&logoColor=white)

**Librerías principales:** `scikit-learn` · `pandas` · `numpy` · `matplotlib` · `seaborn` · `scipy` · `statsmodels`

---

## Consideraciones Éticas

Este estudio utiliza **exclusivamente datos públicos** sin información personal sensible, cumpliendo los principios éticos de la investigación científica y los estándares de datos abiertos del gobierno de Chile. La total reproducibilidad está garantizada mediante código documentado y fuentes de acceso público.

---

## Cita

```bibtex
@phdthesis{barra2026cluster,
  author    = {Barra Ávila, Germán Patricio},
  title     = {Modelación del desempeño económico del clúster turístico de la Región
               de La Araucanía mediante técnicas de machine learning aplicadas a datos
               públicos para la toma de decisiones territoriales},
  school    = {TECH Universidad Tecnológica},
  year      = {2026},
  type      = {Tesis Doctoral},
  address   = {Santiago, Chile}
}
```

---

## Referencias Seleccionadas

- Breiman, L. (2001). Random forests. *Machine Learning, 45*(1), 5–32.
- Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning* (2.ª ed.). Springer.
- INE. (2023). *Estadísticas regionales*. Instituto Nacional de Estadísticas.
- Ministerio de Economía. (2022). *Cuenta Satélite de Turismo de Chile*.
- OECD. (2020). *Machine Learning and Artificial Intelligence in Public Policy*.
- Porter, M. E. (1998). Clusters and the new economics of competition. *Harvard Business Review, 76*(6), 77–90.
- Russell, S. J., & Norvig, P. (2021). *Artificial Intelligence: A Modern Approach* (4.ª ed.). Pearson.
- Varian, H. R. (2019). Artificial intelligence, economics, and industrial organization. En Agrawal, Gans & Goldfarb (Eds.), *The Economics of Artificial Intelligence*. University of Chicago Press.

---

<p align="center">
  <sub>Investigación Doctoral · TECH Universidad Tecnológica · 2026</sub>
</p>
