# CONTEXTO DEL PROYECTO — Documento de traspaso

> **Propósito de este documento.** Contexto autocontenido para que un asistente de IA (o un colaborador) comprenda el estado actual del proyecto sin acceso a la conversación que lo generó. Todas las cifras provienen de corridas reproducibles del código en `src/` y están verificadas contra los CSV de `BBDD/final/`.
>
> **Fecha del estado:** julio 2026. **Período del panel:** 2013–2024.

---

## 1. Qué es el proyecto

**Tesis doctoral** (Germán Barra Ávila, TECH Universidad Tecnológica). Modela el **desempeño económico del clúster turístico de la Región de La Araucanía, Chile**, con Machine Learning sobre datos públicos, a nivel **comuna × año**.

**Variable dependiente:** IDEC (Índice de Desempeño Económico del Clúster), un indicador compuesto construido en este proyecto.

**Pregunta:** ¿en qué medida el ML modela con mayor precisión predictiva que los enfoques tradicionales el desempeño del clúster, para apoyar decisiones territoriales?

**Hipótesis:**
- **H1** — variables económicas/territoriales tienen relación significativa, potencialmente no lineal, con el IDEC.
- **H2** — modelos supervisados estiman el IDEC con error aceptable, superiores a los tradicionales.
- **H3** — técnicas no supervisadas identifican agrupamientos territoriales; existe desigualdad territorial medible.

---

## 2. La decisión de diseño central (NO re-litigar)

La unidad de análisis es la **comuna**. El problema metodológico dominante fue que la mayoría de las fuentes turísticas oficiales (EMAT, ENE, PIB) se publican **a nivel regional**, no comunal. Se resolvió así:

1. **Se priorizó dato comunal OBSERVADO sobre desagregación.** Se levantaron fuentes administrativas que sí tienen granularidad comunal (SII, BIP, INE población, SERNATUR), en vez de desagregar series regionales.

2. **Se descartó explícitamente la desagregación ingenua.** Multiplicar una serie regional `X_t` por un peso comunal fijo `w_i` produce un panel de **rango 1** (`x_it = X_t · w_i`) que no aporta información comunal: el clustering sólo recupera el ranking de pesos y el índice de Theil queda constante. Esto se demostró numéricamente (ver §6, contraejemplo).

3. **Todo dato desagregado pasa un diagnóstico de degeneración** antes de entrar a un modelo (`src/features/diagnostics.py`). Métrica: *idiosincrasia* = fracción de la variación temporal que es propia de cada comuna. Es invariante a escala y vale 0 exacto bajo rango 1. Umbral: <2% = degenerada, no se usa.

**Implicación clave para quien continúe:** no proponer desagregar EMAT/ENE/PIB por pesos fijos. Si se desagrega, debe ser con pesos dinámicos (dependientes del tiempo) y validarse con el diagnóstico.

---

## 3. Definición del clúster (criterio externo)

Se usa un criterio institucional verificable, no un umbral arbitrario: los **Destinos Turísticos oficiales de SERNATUR**.

- **Núcleo (8 comunas):** Pucón, Villarrica (Destino "Pucón y Villarrica"); Curacautín, Lonquimay, Melipeuco ("Araucanía Andina"); Temuco, Nueva Imperial, Carahue ("Temuco y Lago Budi"). Concentra 83% de la oferta formal regional.
- **Anillo (5 comunas):** Cunco, Victoria, Angol, Saavedra, Vilcún (≥4 alojamientos). Solo para sensibilidad.
- **Extendido (13):** núcleo + anillo. Es el panel principal (156 obs).

Código comunal = estándar INE (9101–9121, 9201–9211), coincide con `CMN_CLAVE` del BIP. Las fuentes enlazan sin tabla de equivalencia.

---

## 4. Fuentes de datos — estado real

| Fuente | Aporta | Granularidad | Ventana | Estado |
|---|---|---|---|---|
| **SII** — empresas por comuna y rubro (`PUB_COMU_RUBR.xlsb`) | Rubro I (alojamiento y comidas): ventas UF, trabajadores, renta, nº empresas | **comuna × año** | 2005–2024 | ✅ Integrada |
| **BIP** — inversión pública (`inversiones_202503.csv`, 1.2 GB) | Inversión ejecutada, parseada de `EBI_EJECUCION_PRESUPUESTARIA` (65.664 filas proyecto-año) | **comuna × año** | 2013–2022* | ✅ Integrada |
| **INE** — proyecciones población (base 2017) | Población total y en edad laboral | **comuna × año** | 2002–2035 | ✅ Integrada |
| **SERNATUR** — registro alojamientos | Nº y clase de alojamientos (335 en la región) | comuna (corte transversal) | snapshot | ✅ Integrada |
| **EMAT** — alojamiento turístico | Llegadas, pernoctaciones, ADR, RevPAR | región | 2017–2025 | ⚠️ **Pendiente versión comunal/mensual** |

\* BIP reporta ejecución con rezago de 2–3 años. Se usan variables rezagadas (`lag2`) y stock de capital que cubren hasta 2024. Los datos crudos viven fuera del repo en `~/Documents/BBDD_tesis_doctorado_german/` (variable `TESIS_BBDD_DIR`).

**Limitaciones declaradas de las fuentes** (importantes, ya documentadas):
- SII: georreferencia por **casa matriz** (no establecimiento); rubro 2015–2017 replicado de 2014; reserva tributaria Art. 35 (celdas ≤10 informantes enmascaradas). **En las 13 comunas del clúster no hubo enmascaramiento** en rubro turístico.
- INE: no existe proyección **comunal** base Censo 2024; las cifras recientes son proyecciones base 2017.
- SERNATUR: sin fecha de inscripción → capacidad es corte transversal, no serie temporal.

---

## 5. Arquitectura de código

Todo reproducible con `python -m src.build_panel`. Rutas centralizadas en `src/config.py` (no hardcodeadas).

```
src/
├── config.py              # catálogo 32 comunas, clúster, rutas, TESIS_BBDD_DIR
├── build_panel.py         # ensambla el panel Nivel A + normalización per cápita
├── data/
│   ├── sii.py             # rubro turístico + sectores conexos; maneja '*' enmascarado
│   ├── bip.py             # lee 1.2GB por chunks; parsea ejecución; corte por cobertura
│   ├── poblacion.py       # población comunal (formato ancho INE, latin-1)
│   └── sernatur.py        # capacidad de alojamiento por comuna
├── features/
│   ├── diagnostics.py     # descomposición de varianza, idiosincrasia, rango, Theil
│   ├── inversion.py       # rezagos, ventanas móviles, stock por inventario perpetuo
│   └── idec.py            # normalización, agregación, sensibilidad, Theil temporal
└── models/
    ├── supervisado.py     # H1 (importancia permutación) + H2 (4 esquemas validación)
    └── clustering.py      # H3 (codo Kneedle + silueta + estabilidad + regímenes)
```

**Salidas** en `BBDD/final/`: `panel_nivelA_comunal.csv` (156×~30), `panel_idec_comunal.csv`, `resultados_h1_importancia.csv`, `resultados_h2_validacion.csv`, `resultados_h3_seleccion_k.csv`, `resultados_h3_regimenes.csv`.

---

## 6. El IDEC

$$Z_{kjit} = \frac{\ln(1+X_{kjit}) - \min}{\max - \min}, \quad D_{kit} = \frac{1}{m_k}\sum_j Z_{kjit}, \quad IDEC_{it} = \frac{1}{K}\sum_k D_{kit}$$

- Normalización **per cápita** (crítico: en niveles el índice ordena por población; Temuco pasa de #1 en niveles a #4 per cápita).
- Método por defecto **Min-Max logarítmico**, pool sobre todo el panel.
- **Robusto:** Spearman 0,92–1,00 entre 4 métodos de normalización.

**Dimensiones — estado:**

| Dim | Indicadores | Fuente | Estado |
|---|---|---|---|
| D2 Empleo | trabajadores p.c. | SII | ✅ Observada |
| D3 Ingresos | ventas p.c., renta p.c. | SII | ✅ Observada |
| D4 Capacidad | alojamientos/1000 hab, empresas p.c. | SERNATUR+SII | ✅ Observada |
| **D1 Actividad turística** | llegadas, pernoctaciones, ocupación | EMAT | ⏳ **Pendiente** |

**El IDEC vigente integra 3 de 4 dimensiones.** Mide desempeño económico *estructural* (empleo/ingresos/capacidad), no *flujos* turísticos. D1 espera el levantamiento de EMAT comunal.

**Validación del diagnóstico de degeneración** (prueba de que el panel es real):

| Variable | Idiosincrasia | Veredicto |
|---|---|---|
| Inversión BIP (observada) | 0,918 | Válida |
| Renta p.c. / Trabajadores p.c. | ~0,78 | Válida |
| IDEC (agregado) | 0,343 | Válida |
| *EMAT × peso fijo (contraejemplo)* | **0,000** | *Rango 1 — degenerada* |

---

## 7. Resultados (cifras verificadas)

### H1 — Relaciones no lineales — SOSTENIDA
Importancia por permutación fuera de muestra (RF, R²=0,68). Predictores **exógenos** al IDEC (control de circularidad activo).

| Variable | Importancia |
|---|---|
| Ventas construcción p.c. | 0,189 |
| Ventas inmobiliarias p.c. | 0,106 |
| Población | 0,102 |
| Trabajadores/ventas recreativas p.c. | ~0,09 |
| **Inversión pública (BIP, lag2)** | **−0,003 (nula)** |

Construcción e inmobiliarias dominan (rastro de inversión turística privada). **Inversión pública sin señal predictiva detectable** — leer como "no se detecta", no "no existe" (BIP mide toda la inversión, no la turística; 13 comunas = baja potencia).

### H2 — Precisión predictiva — SOSTENIDA (alcance temporal)
R² por modelo y esquema de validación:

| Modelo | Aleatorio* | Bloques | Temporal | Por comuna |
|---|---|---|---|---|
| Regresión lineal | −0,33 | −0,05 | −0,18 | −25,7 |
| Ridge | −0,30 | −0,06 | −0,03 | −5,8 |
| Árbol | 0,40 | 0,21 | 0,21 | −2,6 |
| **Random Forest** | **0,69** | **0,64** | **0,76** | **−0,60** |

\* control de fuga temporal. RF temporal: MAE=0,067, R²=0,755.

**Dos hallazgos:** (1) ML supera netamente a lineales (comparación justa — Ridge incluido a propósito). (2) La vulnerabilidad es **espacial, no temporal**: todos los modelos fallan al predecir una comuna no vista (R²<0), por sólo 13 unidades. H2 se reformula como **pronóstico temporal**, no generalización espacial.

### H3 — Desigualdad y agrupamientos — SOSTENIDA

**Convergencia territorial (robusta):**
- Índice de Theil del IDEC cae **53,5%** (0,537 en 2013 → 0,250 en 2024); pendiente −0,028/año, *p*<10⁻⁶, R²=0,91.
- Robusto: −46% a −67% según método; −48% sobre variable cruda (*p*<0,0001).
- **β-convergencia:** β=−0,033, *p*=0,0002, R²=0,73; velocidad ≈4%/año, vida media ≈17 años.
- σ + β convergencia juntas → descarta falacia de Galton.
- **Mecanismo:** alcance de la Araucanía Andina (Curacautín +134%, Melipeuco +111%, Lonquimay +108%). Pucón única que cae (−3%).

**Regímenes de desempeño (comuna × año):**
- Selección de k: **codo (Kneedle) + silueta coinciden en k=4** (jerárquico). Estabilidad ARI=0,79.
- 4 regímenes: **Enclave turístico** (Pucón), **Centro urbano de servicios** (Temuco: población alta, intensidad turística −0,86), **Turístico emergente** (45 obs), **Periferia** (83 obs).
- k=4 **separa Temuco de Pucón** — distinción cualitativa clave.
- 4 comunas transitan de régimen (Angol, Cunco, Curacautín, Victoria), **todas al alza**. Pucón = estado absorbente.
- **Nota:** tipología puramente comunal (13 unidades) es FRÁGIL (Pucón queda como cluster de 1; ARI vs SERNATUR ≈0). El nivel comuna-año es el robusto.

**Patrón transversal a las 3 hipótesis:** desconcentración del clúster desde Pucón hacia la Araucanía Andina. Curacautín es el caso paradigmático.

---

## 8. Limitaciones declaradas (ya en los capítulos)

1. **Falta D1** (actividad turística / EMAT) — el IDEC mide desempeño estructural, no flujos.
2. **13 unidades** — limita generalización espacial (H2) y tipología comunal (H3).
3. **BIP agregado** — no distingue inversión turística de otras.
4. **SII por casa matriz** y **población pre-Censo 2024** — actualizar cuando haya mejores registros.

Ninguna invalida los hallazgos; todas están declaradas con vía de resolución.

---

## 9. Pendientes (prioridad)

1. **EMAT mensual/comunal** → habilita D1 y multiplica observaciones temporales. *Máxima prioridad.*
2. **SERNATUR con fecha de inscripción** → convierte D4 en serie temporal.
3. **Población comunal base Censo 2024** → cuando el INE la publique.
4. **Redacción:** Capítulos III y IV en borrador Markdown (`Documentación/Capitulo_III_*.md`, `Capitulo_IV_*.md`); falta integrarlos al `.docx` maestro.

---

## 10. Estado de documentos

- `README.md` — actualizado al diseño real (antes sobredeclaraba avance).
- `Documentación/Capitulo_III_Metodologia.md` — borrador completo.
- `Documentación/Capitulo_IV_Resultados.md` — borrador completo (antes vacío).
- `BBDD/README.md` — especificación de levantamiento de datos pendientes.
- `.docx` maestro (`Tesis_Doctoral_Barra_Avila.docx`) — **no modificado**; Caps I–III previos describen el diseño antiguo (comunal sin las fuentes actuales) y Cap I–V estaban vacíos.

---

## 11. Notas para quien continúe el trabajo

- **No re-litigar** la decisión de no desagregar por pesos fijos (§2). Está demostrado numéricamente.
- **Control de circularidad:** los predictores de H1/H2 NO pueden incluir componentes del IDEC (`supervisado.py` aborta si ocurre).
- **Validación de panel:** nunca usar K-fold aleatorio como resultado principal (fuga temporal). Usar temporal/bloques/comuna.
- **Entorno:** Python 3.12 (Anaconda), Windows. `.xlsb` requiere `pyxlsb`; el CSV del INE es **latin-1**; el BIP se lee **por chunks** (1.2 GB).
- Si se agrega D1, recalcular IDEC, sensibilidad y las tres hipótesis: los números de §7 cambiarán.
