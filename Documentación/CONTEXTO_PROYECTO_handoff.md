# CONTEXTO DEL PROYECTO — Documento de traspaso

> **Propósito de este documento.** Contexto autocontenido para que un asistente de IA (o un colaborador) comprenda el estado actual del proyecto sin acceso a la conversación que lo generó. Todas las cifras provienen de corridas reproducibles del código en `src/` y están verificadas contra los CSV de `BBDD/final/`.
>
> **Fecha del estado:** agosto 2026. **Período del panel:** 2013–2024.
>
> **Alcance de este trabajo.** Cubre exclusivamente el **componente de Machine Learning** de la investigación: levantamiento e integración de datos, construcción del IDEC, modelación supervisada y no supervisada, y la redacción de los Capítulos III, IV y V, que dependen de ese componente. Los Capítulos I y II, las referencias bibliográficas y los anexos corresponden al autor de la tesis y **quedan fuera de este alcance** (ver §10).
>
> **Estado:** los Capítulos III, IV y V **están integrados en la tesis** con las cifras verificadas. El modelo está desplegado y operativo.

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
- **Robusto:** Spearman 0,91–1,00 entre 4 métodos de normalización.

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

> Todas las cifras de esta sección corresponden al modelo vigente, que incorpora CONAF/SNASPE como predictor (§7-ter), y coinciden con `BBDD/final/resultados_h1_importancia.csv` y `resultados_h2_validacion.csv`.

### H1 — Relaciones no lineales — SOSTENIDA
Importancia por permutación fuera de muestra (RF, R² medio de los folds = 0,788). Predictores **exógenos** al IDEC (control de circularidad activo).

| Variable | Importancia |
|---|---|
| **Visitación áreas protegidas p.c.** | **0,345** |
| Ventas construcción p.c. | 0,123 |
| Trabajadores recreativas p.c. | 0,070 |
| Ventas inmobiliarias p.c. | 0,067 |
| Ventas recreativas p.c. | 0,050 |
| Población | 0,043 |
| Stock de capital público | 0,005 |
| **Inversión pública (BIP, lag2)** | **−0,002 (nula)** |

La visitación observada domina, con importancia casi triple de la segunda variable: es el único registro que mide afluencia directa y no un proxy económico. **Inversión pública sin señal predictiva detectable** — leer como "no se detecta", no "no existe" (BIP mide toda la inversión, no la turística; 13 comunas = baja potencia).

### H2 — Precisión predictiva — SOSTENIDA (alcance temporal)
R² por modelo y esquema de validación:

| Modelo | Aleatorio* | Bloques | Temporal | Por comuna |
|---|---|---|---|---|
| Regresión lineal | 0,56 | 0,53 | 0,05 | −11,86 |
| Ridge | 0,48 | 0,32 | 0,24 | −2,94 |
| Árbol | 0,55 | 0,56 | 0,33 | −1,35 |
| **Random Forest** | **0,80** | **0,76** | **0,81** | **−0,36** |

\* control de fuga temporal. RF temporal: MAE = 0,059, R² = 0,809.

**Tres hallazgos:** (1) El ML supera a los lineales frente a una **línea base competente** —con los predictores actuales los modelos lineales ya no arrojan ajustes negativos—, no frente a modelos mal especificados. (2) La brecha es moderada bajo validación aleatoria (0,80 vs 0,56) y **máxima bajo la temporal** (0,81 vs 0,05): al extrapolar a años no observados lo lineal se desploma, lo que respalda la no linealidad de H1. (3) La vulnerabilidad es **espacial, no temporal**: todos los modelos fallan al predecir una comuna no vista, por sólo 13 unidades. H2 se reformula como **pronóstico temporal**, no generalización espacial.

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

## 7-bis. Variable CET — Choques Exógenos Territoriales

Variable **dinámica ingresada por el usuario** para simular escenarios de choque exógeno al rubro turístico (crisis sanitarias, conflictividad, desastres). Implementada en `src/features/cet.py` + `models/supervisado.simular_cet()`.

- **Rango [0,1]**, donde **1 = sin choque (valor por defecto)** y 0 = choque máximo.
- Acepta escalar (`cet=0.7`), por comuna (`{9115: 0.5}`), por comuna-año (`{(9115,2025): 0.5}`) o DataFrame.
- Serie histórica comuna×año construida desde eventos documentados (COVID 2020–22; conflictividad en Malleco). **Las intensidades son supuestos declarados, no mediciones — recalibrar con fuentes.**

**Dos modos, y por qué:**

| Modo | Mecanismo | Estado |
|---|---|---|
| **`estructural`** (por defecto) | El modelo proyecta el IDEC y el choque se aplica como atenuación `IDEC·[1−λ(1−CET)]`, con λ declarado (default 0,6) | ✅ **Recomendado** |
| `aprendido` | La CET entra como predictor y el bosque infiere el efecto | ⚠️ Mal identificado hoy |

**Hallazgo que motivó el diseño (importante, verificado):** el modo aprendido produce un **signo espurio positivo** (un choque máximo *subiría* el IDEC +3,7 %). Causa: la correlación empírica CET↔IDEC es **−0,004 (nula)** y **6 de 13 comunas aumentaron** su IDEC durante la pandemia (Curacautín +37,9 %, Melipeuco +26,4 %). El IDEC vigente mide desempeño **estructural** —resiliente al choque—, mientras el colapso ocurrió en los **flujos** (llegadas −57 % en 2020), que corresponden a **D1, la dimensión ausente**.

**Trampa técnica documentada:** si la CET entrara al entrenamiento como constante = 1 tendría varianza cero, importancia exactamente 0, y mover la perilla no cambiaría nada (verificado: cambio 0,0000000000). Es un fallo silencioso. Por eso existe la serie histórica.

**Al incorporar D1:** reevaluar el modo aprendido —debería identificarse correctamente— y verificar que ninguna componente de la CET provenga de EMAT (sería endógena).

Salidas: `BBDD/processed/cet_serie_historica.csv`, `BBDD/final/resultados_cet_curva_respuesta.csv`.

---

## 7-ter. CONAF/SNASPE y el cierre de D1

**Fuente:** visitantes a Áreas Silvestres Protegidas (CONAF), vía SIET/SERNATUR. 2012–2024, mensual, por unidad. 13 unidades en La Araucanía. Módulo `src/data/conaf.py`; datos en `BBDD/processed/conaf_snaspe_araucania.csv`.

**Rol: predictor exógeno, NO componente del IDEC ni ponderador de D1.**

| Uso | Resultado |
|---|---|
| Predictor H1/H2 | R² temporal 0,751 → **0,809**; predictor más importante (**0,345**) |
| Calibración CET | 2020 observado **0,475** vs supuesto 0,45 → respalda el supuesto |
| Validación externa | Malalcahuello +252 % (2013→2024) corrobora la convergencia de la Araucanía Andina desde fuente independiente |

**Por qué NO como ponderador de D1:** Villarrica —2ª comuna en oferta hotelera, 88 alojamientos— **no tiene áreas protegidas** y recibiría cero actividad turística. Malalcahuello (centro de esquí, visitantes de día) concentra ~60 % de la visitación regional. Mide visitación a parques, no turismo de alojamiento.

**D1 queda cerrada.** Cuatro vías descartadas con evidencia: población (idiosincrasia 0,0008), SII (doble conteo r≈0,8), CONAF (cobertura estructural incompleta) y EMAT sub-regional. Sobre esta última: el SIET **sí tiene** dimensión “destino turístico” (4 destinos para La Araucanía, casi calcan el clúster), pero el reporte declara oficialmente que la apertura por destino está **suspendida desde abril de 2020** por el cierre de >50 % de establecimientos durante la pandemia. Desaparece justo donde vive la información de choque. Detalle completo en `Documentación/Nota_metodologica_D1_desagregacion.md`.

**Pista no explorada:** SIET ofrece también `repDinamicoPDI` — llegadas de extranjeros por paso fronterizo (Mamuil Malal/Curarrehue, Pino Hachado e Icalma/Lonquimay). Otra señal turística comuna×año exógena al SII, en la misma línea que CONAF.

---

## 8. Limitaciones declaradas (ya en los capítulos)

1. **Falta D1** (actividad turística / EMAT) — el IDEC mide desempeño estructural, no flujos.
2. **13 unidades** — limita generalización espacial (H2) y tipología comunal (H3).
3. **BIP agregado** — no distingue inversión turística de otras.
4. **SII por casa matriz** y **población pre-Censo 2024** — actualizar cuando haya mejores registros.

Ninguna invalida los hallazgos; todas están declaradas con vía de resolución.

---

## 9. Pendientes

### 9.1 Dentro del alcance de ML — todos completados

No queda trabajo analítico pendiente. Las tres hipótesis están contrastadas, el panel es reproducible y los Capítulos III–V están integrados en la tesis.

Mejoras posibles a futuro, ninguna bloqueante:

1. **Actualización anual del panel** → cuando el SII publique el año comercial 2025 (previsiblemente fines de 2026), extender el panel es mecánico: descargar `PUB_COMU_RUBR.xlsb`, ejecutar `python -m src.build_panel`, regenerar el Space. Igual para la visitación de CONAF.
2. **Pasos fronterizos (PDI)** → `repDinamicoPDI` en SIET ofrece llegadas de extranjeros por paso fronterizo (Mamuil Malal/Curarrehue, Pino Hachado e Icalma/Lonquimay). Señal turística comuna×año exógena al SII, sin explorar.
3. **SERNATUR con fecha de inscripción** → convertiría D4 en serie temporal.
4. **Población comunal base Censo 2024** → cuando el INE la publique con desagregación comunal.
5. **D1** → cerrada con evidencia (§7-ter). Sólo se reabre si el INE restituye la apertura por destino turístico de la EMAT. Si eso ocurre, recalcular IDEC, sensibilidad y las tres hipótesis: cambiarían los números de §7 y las Tablas 4.1–4.7.

### 9.2 Fuera del alcance de ML — corresponden al autor de la tesis

Estos puntos **no fueron abordados** en este trabajo y quedan pendientes:

| Componente | Estado | Observación |
|---|---|---|
| **Capítulo II — Marco Teórico** | 🔴 Esquemático | 1.426 palabras para 14 secciones (2.1–2.14, incluidos tres estados del arte): unas 100 palabras por sección. Es el hueco mayor del documento. |
| **Capítulo I — El Problema** | ⚠️ Delgado | 1.690 palabras para contexto, problema, justificación, objetivos e hipótesis. |
| **Referencias** | ⚠️ 32 entradas | No incluyen la literatura que sustenta lo incorporado en el Capítulo III: estimación en áreas pequeñas, convergencia β y σ, importancia por permutación, método del codo, índices compuestos territoriales. |
| **Anexos** | ❌ Ausentes | Material disponible para construirlos: salidas del diagnóstico, tablas de sensibilidad del IDEC, código. |
| **Índices de tablas y figuras** | ❌ Ausentes | — |
| **Tabla de contenido** | ⏳ Requiere actualización | En Word: clic derecho sobre el índice → *Actualizar toda la tabla*, para que aparezcan las secciones 5.1–5.8. |

---

## 10. Estado de documentos

**Tesis maestra:** `Documentación/Tesis_Doctoral_Barra_Avila_Version_29.07.2026.docx` — **15.008 palabras, 960 párrafos, 17 tablas**. Estructura completa I–V con tabla de contenido.

| Capítulo | Palabras | Estado |
|---|---|---|
| I — El Problema | 1.690 | ⚠️ Delgado — fuera del alcance de ML |
| II — Marco Teórico (§2.1–2.14) | 1.426 | 🔴 Esquemático — fuera del alcance de ML |
| **III — Metodología** | 3.371 | ✅ **Integrado** (12 secciones + Tablas 3.1–3.3, Figura 3.1). Incluye secciones propias del autor: 3.8.6 y 3.11.4 |
| **IV — Resultados** | 3.455 | ✅ **Integrado** (Tablas 4.1–4.7, Figura 4.1). Incluye 4.2.4 y 4.7.3 del autor |
| **V — Conclusiones** | 2.778 | ✅ **Integrado** (8 secciones, 9 subsecciones) |
| Referencias | 533 | ⚠️ 32 entradas — fuera del alcance de ML |

**Coherencia verificada:** las cifras de la tesis coinciden con las salidas del código — R² temporal **0,809**; MAE **0,059**; R² por comuna **−0,362**; importancia visitación **0,345**, construcción **0,123**; Theil **−53,5 %**; β **−0,033**; k = 4 con ARI **0,79**; idiosincrasia **0,918** (BIP) frente a **0,000** (contraejemplo); Spearman **0,91–1,00**.

**Documentos de apoyo en el repo:**
- `README.md` — actualizado al diseño real.
- `Documentación/Capitulo_III_Metodologia.md` y `Capitulo_IV_Resultados.md` — borradores fuente en Markdown (origen de lo integrado al `.docx`).
- `BBDD/README.md` — especificación de levantamiento de datos pendientes.
- `Documentación/documentacion_2026-05-26_protocolo-investigacion-barra.md` — protocolo original.
- `Documentación/Nota_tecnica_paralelismo_importancia_variables.md` — por qué los dos `n_jobs` de `importancia_variables()` están fijados: paralelismo anidado, 3,7× de tiempo y reproducibilidad bit a bit.

---

## 11. Notas para quien continúe el trabajo

- **No re-litigar** la decisión de no desagregar por pesos fijos (§2). Está demostrado numéricamente.
- **Control de circularidad:** los predictores de H1/H2 NO pueden incluir componentes del IDEC (`supervisado.py` aborta si ocurre).
- **Validación de panel:** nunca usar K-fold aleatorio como resultado principal (fuga temporal). Usar temporal/bloques/comuna.
- **Rendimiento de H1:** los dos `n_jobs` de `importancia_variables()` están fijados a propósito. Devolver cualquiera a `-1` cuadruplica el tiempo y vuelve la tabla no reproducible (ver la nota técnica).
- **Entorno:** Python 3.12 (Anaconda), Windows. `.xlsb` requiere `pyxlsb`; el CSV del INE es **latin-1**; el BIP se lee **por chunks** (1.2 GB).
- Si se agrega D1, recalcular IDEC, sensibilidad y las tres hipótesis: los números de §7 cambiarán.
