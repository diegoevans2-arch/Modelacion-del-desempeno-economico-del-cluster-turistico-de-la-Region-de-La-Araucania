# Modelación del Desempeño Económico del Clúster Turístico de la Región de La Araucanía mediante Técnicas de Machine Learning

> **Investigación Doctoral** · Doctorado en Ciencias Económicas Empresariales
> TECH Universidad Tecnológica · Santiago, 2026

---

## Resumen

Esta investigación aplica técnicas de Machine Learning supervisado y no supervisado para modelar y evaluar el desempeño económico del clúster turístico de la Región de La Araucanía (Chile), utilizando exclusivamente datos públicos oficiales. El estudio introduce el **IDEC** (*Índice de Desempeño Económico del Clúster*), un indicador compuesto construido **a nivel comunal** a partir de registros administrativos observados. La hipótesis central postula que los modelos de ML logran una precisión predictiva superior a los enfoques econométricos tradicionales, generando evidencia accionable para la toma de decisiones territoriales.

---

## Ficha del Estudio

| Atributo | Detalle |
|---|---|
| **Autor** | Germán Patricio Barra Ávila |
| **Director** | Dr. Alejandro Héctor Molina |
| **Institución** | TECH Universidad Tecnológica |
| **Programa** | Doctorado en Ciencias Económicas Empresariales |
| **Área de estudio** | Región de La Araucanía, Chile |
| **Unidad de análisis** | Comuna × año (panel) |
| **Comunas del clúster** | 13 (núcleo de 8 + anillo de 5) |
| **Período del panel** | 2013 – 2024 |
| **Fuentes de datos** | SII · BIP · INE · SERNATUR · Banco Central |
| **Paradigma** | Positivista · Cuantitativo · Explicativo-Predictivo |
| **Entrega final** | 10 de diciembre de 2026 |

---

## Pregunta de Investigación

> *¿En qué medida la aplicación de técnicas de Machine Learning a datos públicos permite modelar con mayor precisión predictiva que enfoques tradicionales el desempeño económico del clúster turístico de la Región de La Araucanía, para apoyar la toma de decisiones territoriales?*

---

## Definición del clúster

La unidad de análisis es la **comuna**. El clúster turístico se define con un criterio externo y verificable: los **Destinos Turísticos oficiales que SERNATUR** reconoce en su Registro Nacional de Prestadores.

| Grupo | Comunas | Criterio |
|---|---|---|
| **Núcleo** (8) | Pucón, Villarrica · Curacautín, Lonquimay, Melipeuco · Temuco, Nueva Imperial, Carahue | Destino SERNATUR |
| **Anillo** (5) | Cunco, Victoria, Angol, Saavedra, Vilcún | Oferta formal ≥ 4 alojamientos (análisis de sensibilidad) |

El núcleo concentra el 83 % de la oferta formal de alojamiento de la región.

---

## Arquitectura de datos

El principio rector es **no imputar lo que puede observarse**. Las dimensiones del IDEC se construyen sobre registros administrativos comunales observados, no sobre desagregaciones de series regionales.

### Fuentes integradas

| Fuente | Variable | Granularidad | Ventana | Estado |
|---|---|---|---|---|
| **SII** — Estadísticas de empresas por comuna y rubro | Ventas (UF), trabajadores, renta, nº empresas del rubro *I – Alojamiento y servicio de comidas* | **comuna × año** | 2005–2024 | ✅ Integrada |
| **BIP** — Banco Integrado de Proyectos | Inversión pública ejecutada (`EBI_EJECUCION_PRESUPUESTARIA`) | **comuna × año** | 2013–2022* | ✅ Integrada |
| **INE** — Proyecciones de población (base 2017) | Población total y en edad laboral | **comuna × año** | 2002–2035 | ✅ Integrada |
| **SERNATUR** — Registro de alojamientos | Nº y clase de alojamientos | comuna (corte) | snapshot | ✅ Integrada |
| **EMAT** — Encuesta Mensual de Alojamiento | Llegadas, pernoctaciones, ADR, RevPAR | región | 2017–2025 | ⚠️ Pendiente versión mensual |

\* El BIP reporta la ejecución con 2–3 años de rezago; se emplean versiones rezagadas (`lag2`) y de stock de capital, que cubren hasta 2024.

### El riesgo evitado: el panel degenerado

Desagregar una serie regional multiplicándola por un peso comunal fijo produce un panel de **rango 1** que no contiene información comunal nueva: el clustering sólo recupera el ranking de pesos y el índice de Theil queda constante. Toda variable pasa por un **diagnóstico de degeneración** antes de entrar a un modelo (`src/features/diagnostics.py`).

| Variable | Interacción comuna×tiempo | Veredicto |
|---|---|---|
| Inversión pública (BIP, observada) | 0,918 | ✅ OK |
| Renta / trabajadores (SII, observadas) | 0,78 | ✅ OK |
| *EMAT × peso fijo (contraejemplo)* | *0,000 — rango 1* | ❌ Degenerada |

---

## El IDEC

Índice compuesto que agrega indicadores normalizados en dimensiones, y las dimensiones en un índice único de igual ponderación:

$$Z_{kjit} = \frac{\ln(1+X_{kjit}) - \min}{\max - \min}, \qquad D_{kit} = \frac{1}{m_k}\sum_{j} Z_{kjit}, \qquad IDEC_{it} = \frac{1}{K}\sum_k D_{kit}$$

Las variables se normalizan **per cápita** antes de agregar: en niveles, el índice ordenaría las comunas por tamaño demográfico en vez de por intensidad de desempeño.

| Dimensión | Indicadores | Fuente | Estado |
|---|---|---|---|
| **D2 — Empleo sectorial** | trabajadores turísticos p.c. | SII | ✅ Observada |
| **D3 — Generación de ingresos** | ventas p.c., renta p.c. | SII | ✅ Observada |
| **D4 — Capacidad productiva** | alojamientos/1.000 hab., empresas p.c. | SERNATUR + SII | ✅ Observada |
| **D1 — Actividad turística** | llegadas, pernoctaciones, ocupación | EMAT | ⏳ Pendiente (requiere EMAT comunal/mensual) |

> El IDEC vigente integra **tres de las cuatro dimensiones**. D1 se incorporará al levantar EMAT. El índice es robusto al método de normalización (correlación de Spearman 0,91–1,00 entre Min-Max, Z-score, rank y Min-Max logarítmico).

---

## Principales resultados

Los tres hallazgos se sostienen sobre el panel comunal observado 2013–2024 (156 observaciones, 13 comunas).

### H1 — Relaciones no lineales
Random Forest estima el IDEC con predictores **exógenos** al índice (visitación a áreas protegidas, inversión pública, sectores conexos, demografía). La variable más relevante por importancia de permutación es la **visitación a áreas silvestres protegidas** (0,345), seguida de **construcción** (0,123) e **inmobiliarias** (0,067). La inversión pública (BIP) no muestra señal predictiva detectable.

### H2 — Precisión predictiva
| Modelo | R² (validación temporal) |
|---|---|
| **Random Forest** | **0,809** |
| Árbol de decisión | 0,334 |
| Ridge (regularizada) | 0,243 |
| Regresión lineal | 0,051 |

El ML supera netamente a los modelos lineales en **pronóstico temporal** — y lo hace frente a una línea base competente, no frente a modelos mal especificados. La generalización espacial (predecir una comuna no vista) es intrínsecamente limitada por el bajo número de unidades (13 comunas) y se declara como tal.

### H3 — Desigualdad y agrupamientos territoriales
- **Convergencia del clúster.** El índice de Theil del IDEC cae **53,5 %** entre 2013 y 2024 (σ-convergencia, *p* < 10⁻⁶), confirmada por β-convergencia (β = −0,033, *p* = 0,0002; velocidad ≈ 4 % anual). El motor es el alcance de los destinos de la **Araucanía Andina** (Curacautín +134 %, Melipeuco +111 %), no el deterioro de Pucón.
- **Regímenes de desempeño.** El agrupamiento (selección de *k* por método del codo + silueta convergentes en *k* = 4) identifica cuatro regímenes estables (ARI de remuestreo 0,79), separando el **enclave turístico** (Pucón) del **centro urbano de servicios** (Temuco). Cuatro comunas transitan al alza; ninguna a la baja.

---

## Estructura del repositorio

```
.
├── BBDD/
│   ├── processed/            # paneles intermedios por fuente
│   ├── final/                # panel Nivel A, IDEC y resultados H1–H3
│   └── README.md             # estado y especificación de levantamiento de datos
├── src/
│   ├── config.py             # catálogo comunal, definición del clúster, rutas
│   ├── build_panel.py        # ensamblado reproducible del panel Nivel A
│   ├── data/                 # loaders: sii, bip, poblacion, sernatur
│   ├── features/             # diagnostics, inversion, idec
│   └── models/               # supervisado (H1–H2), clustering (H3)
├── Notebooks/                # exploración y transformaciones
├── Documentación/            # protocolo, capítulos, tesis
├── requirements.txt
└── README.md
```

Los datos crudos **no se versionan** (volumen y licencia). Viven en una carpeta externa apuntada por `src/config.py`; puede redefinirse con la variable de entorno `TESIS_BBDD_DIR`.

### Reproducir el panel

```bash
pip install -r requirements.txt
python -m src.build_panel        # genera BBDD/final/panel_nivelA_comunal.csv
```

---

## Estado de avance

| Componente | Avance |
|---|---|
| Levantamiento de fuentes comunales (SII, BIP, INE, SERNATUR) | 100 % |
| Panel comunal integrado 2013–2024 | 100 % |
| Diagnóstico de validez del panel | 100 % |
| IDEC (3 de 4 dimensiones) | 85 % |
| Dimensión D1 — actividad turística (EMAT) | 0 % *(pendiente levantamiento)* |
| Modelos supervisados (H1, H2) | 100 % |
| Clustering y desigualdad territorial (H3) | 100 % |
| Redacción Capítulos I–IV (integrados en la tesis) | 100 % |
| Redacción Capítulo V (Conclusiones) | Pendiente *(placeholder en la tesis)* |

### Pendientes de datos

Detallados en [`BBDD/README.md`](BBDD/README.md):
1. **EMAT mensual/comunal** — habilita D1 y multiplica las observaciones temporales.
2. **SERNATUR con fecha de inscripción** — convierte D4 en serie temporal.
3. **Población comunal base Censo 2024** — el INE aún no la publica desagregada.

---

## Stack tecnológico

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?style=flat&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?style=flat&logo=pandas&logoColor=white)

**Librerías principales:** `scikit-learn` · `pandas` · `numpy` · `scipy` · `statsmodels` · `pyxlsb` · `pyreadr`

---

## Consideraciones éticas

Este estudio utiliza **exclusivamente datos públicos** sin información personal sensible. Las cifras del SII respetan la reserva tributaria (Art. 35 del Código Tributario): los valores construidos con ≤10 informantes se publican enmascarados y se tratan como faltantes estructurales. La reproducibilidad está garantizada mediante código documentado y fuentes de acceso público.

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

<p align="center">
  <sub>Investigación Doctoral · TECH Universidad Tecnológica · 2026</sub>
</p>
