---
tipo: veredicto técnico y protocolo obligatorio de revisión
asunto: Dictamen sobre el "Plan ML para llevar la tesis a 98/100" y regla para
        toda revisión futura del componente cuantitativo
elaborado por: Diego Evans Pérez Paz — componente de Machine Learning
fecha: 2026-11-09
---

# Veredicto sobre el Plan de Robustez, y la regla que evita repetirlo

## Parte I — Veredicto

### 1. Dictamen

**El plan no debe ejecutarse tal como está escrito.** Su principio rector —no
inventar observaciones ni resultados— es correcto y debe conservarse. Su
protocolo técnico es inaplicable, y si se ejecuta produce un daño mayor que la
carencia que pretende corregir.

| Sección del plan | Dictamen |
|---|---|
| §1 Principio de no fabricar | ✅ Correcto, conservar |
| §2 Evidencia disponible | ⚠️ Fuente equivocada (export del simulador) |
| §3 Brechas y puntaje | ❌ Tres de seis ya cerradas; puntaje fabricado |
| §5 Auditoría inicial | ⚠️ Válida pero sobre el archivo equivocado |
| §6 Reproducción de métricas | ❌ **Circular. No ejecutar** |
| §7 Validación temporal | ❌ **Circular. No ejecutar** |
| §8 Clustering | ❌ Variables equivocadas; ya existe algo más completo |
| §9 Sensibilidad de las 4 asignaciones | ❌ Parte de un malentendido |
| §10 Anillo territorial | ❌ Inventa un bloqueo que no existe |
| §11 COVID-19 | ⚠️ Encuadre correcto, método inferior al ya ejecutado |
| §12 Manifiesto | ⚠️ Mejora marginal; ya existe con hashes |
| §13 Pruebas de coherencia | ✅ **Vale la pena. No existe** |
| §4 `requirements-lock.txt` | ✅ **Brecha real. Ya cerrada** |

### 2. El defecto fatal: el modelo propuesto es circular

El plan fija, en §6.2 y lo arrastra a §7, §8 y §11:

```python
FEATURES = ["d2", "d3", "d4"]
TARGET = "idec"
```

Esas tres variables **son las dimensiones del IDEC**, y el índice es su promedio
simple. Verificado sobre el propio `datos.json`:

| Comprobación | Resultado |
|---|---|
| máx \|promedio(d2,d3,d4) − idec\| | 0,000067 |
| media \|promedio(d2,d3,d4) − idec\| | 0,000025 |
| correlación | 0,99999999 |
| **R² de usar el promedio simple como predicción** | **0,99999998** |

La diferencia residual es únicamente el redondeo a cuatro decimales con que se
exportó el archivo del simulador. El plan propone predecir una variable a partir
de sus propios componentes.

**El repositorio lo bloquea por diseño.** `src/models/supervisado.py` define
`COMPONENTES_IDEC` e implementa `verificar_circularidad()`, que **aborta la
ejecución**:

```
verificar_circularidad(["D2_empleo","D3_ingresos","D4_capacidad"])
  -> ValueError: Predictores circulares (son componentes del IDEC)
```

### 3. Por qué el daño es mayor que la carencia

Ejecutado el protocolo del plan tal como está escrito, con su propio
`GroupKFold` por comuna y sus propios hiperparámetros:

| Especificación | R² | MAE |
|---|---|---|
| Protocolo del plan (d2, d3, d4) | **+0,6337** | 0,0633 |
| Los 15 predictores reales del repositorio | **−0,3619** | 0,1699 |

El plan **convierte el −0,36 honesto en un +0,63 espurio**.

El −0,3619 es el resultado más incómodo de la tesis: el modelo no transfiere a
comunas que no vio. Está correctamente reportado y correctamente interpretado.
El protocolo del plan lo haría desaparecer, y el documento pasaría a exhibir
como logro lo que en realidad sería una fuga de información del índice hacia sus
predictores.

Esto no es un error de cálculo que se corrige en la revisión siguiente. Es la
clase de hallazgo que, detectado en la defensa, invalida el capítulo de
resultados.

### 4. La fuente de datos es la equivocada

El plan construye todo sobre `datos.json`, que es el **export del simulador**:
156 filas, valores redondeados a cuatro decimales, predicciones precomputadas y
once campos. No es la base del análisis.

El panel real es `BBDD/final/panel_idec_comunal.csv`: 156 filas y 61 columnas,
con los **quince predictores** efectivamente usados. El propio plan admite en
§6.1 que auditar `df["pred"]` "no demuestra que las predicciones sean fuera de
muestra" — y aun así lo convierte en su punto de partida.

### 5. Tres de las seis brechas ya estaban cerradas

| Brecha del plan | Estado real |
|---|---|
| Cuatro asignaciones de regímenes | ✅ Resuelta: Melipeuco y Lonquimay, 2013-2014 |
| Sensibilidad del anillo 3/4/5 | ✅ Resuelta: los tres universos reconstruidos |
| COVID-19 | ✅ Resuelta: dummy, importancia y MCO con efecto fijo |
| Particiones y trazabilidad | ✅ Resuelta: 2.605 predicciones por fila |
| Estabilidad de clustering | ✅ **Ya existía y va más lejos** |
| Auditoría de coherencia | ❌ Pendiente, y vale la pena |

Sobre la estabilidad de clustering: el plan pide k = 2 a 6 con K-Means y Ward,
silueta y Davies-Bouldin. `BBDD/final/resultados_h3_seleccion_k.csv` contiene
**k = 2 a 7, ambos algoritmos, en dos niveles de agregación, con silueta,
Davies-Bouldin y Calinski-Harabasz**. Es un superconjunto de lo pedido y
precede al plan.

Los cuatro esquemas de validación que pide §6.2 también están implementados
desde antes: aleatorio, bloques, temporal de origen móvil y por comuna.

### 6. Dos secciones parten de un malentendido

**§9 — los 256 escenarios combinatorios.** El plan supone que las cuatro
asignaciones faltantes son *etiquetas externas* ausentes, y propone enumerar
4⁴ = 256 escenarios de peor caso.

No son etiquetas. Son cuatro observaciones que el agrupamiento descarta por
exclusión según lista completa, porque **el Servicio de Impuestos Internos no
publica fila de rubro R** (actividades recreativas) para Melipeuco y Lonquimay
en 2013 y 2014. No hay una etiqueta oculta que enumerar: hay una actividad
económica que no existe en esas comunas y años. El ejercicio combinatorio no
tiene objeto.

**§10 — la matriz de distancias.** El plan afirma que el anillo territorial
"requiere una matriz de distancias o adyacencia con fuente verificable" y que
"no puede reconstruirse honestamente"; en §17 lo deja como pendiente.

La regla del anillo **no es de distancia**: es el número de alojamientos
formales registrados (≥ 4). El Registro Nacional de Prestadores cubre las 32
comunas de la región y `build_panel.construir()` está parametrizado por lista de
comunas. Los tres universos se reconstruyeron por completo:

| Umbral | Comunas | Obs. | β | p | Theil 2013→2024 | RF temporal |
|---|---|---|---|---|---|---|
| ≥ 3 | 15 | 180 | −0,032480 | 0,000109 | −52,1 % | 0,8207 |
| **≥ 4 (vigente)** | **13** | **156** | **−0,032880** | **0,000212** | **−53,5 %** | **0,8086** |
| ≥ 5 | 12 | 144 | −0,041465 | 0,000014 | −57,7 % | 0,8235 |

El plan declara irreconstruible algo que ya está reconstruido, y propone para
ello una fuente que la regla no necesita.

### 7. El puntaje está fabricado

El plan asigna "84/100 de partida" y "98/100 de potencial", con ganancias
desglosadas de "+4", "+3", "+2" y "+1" por brecha. No existe rúbrica, ni
ponderación, ni evaluador que haya emitido esos números.

Es una cuantificación inventada dentro de un documento cuyo principio rector
declarado es, literalmente, *"elevar la robustez sin inventar observaciones,
resultados, pruebas, hiperparámetros ni fuentes"*. Si esas cifras llegan al
texto de la tesis, son exactamente el tipo de número que un comité pide trazar y
que no se puede trazar.

### 8. Lo que sí debe tomarse

1. **`requirements-lock.txt`** — brecha real. `requirements.txt` declaraba
   rangos `>=`, de modo que un revisor con instalación limpia podía recibir otra
   versión menor de scikit-learn y no reproducir las métricas con la misma
   semilla. **Ya está cerrada.** De paso quedó documentado que `requirements.txt`
   declara `xlrd` y `pyreadr`, que no están instalados y no se importan en
   `src/`: la única lectura de Excel usa `engine="pyxlsb"`.
2. **Pruebas automáticas de coherencia** entre las cifras del texto y los
   archivos de resultados (§13). No existen y son la medida que habría evitado
   el 0,92 frente al 0,91 y el 0,762 frente al 0,788.
3. **Reportar el ARI como mediana con intervalo percentil 5-95** en lugar de
   media con percentil 10 (§8). Mejora menor pero correcta, sobre todo porque el
   remuestreo por comuna arroja p10 = 0,38.
4. **El encuadre de COVID-19 como sensibilidad y no como causalidad** (§11). Es
   correcto y coincide con el resultado obtenido.

---

## Parte II — La regla

### 9. El patrón que hay que cortar

Tres rondas consecutivas de revisión produjeron conclusiones erróneas o
inaplicables por la misma causa: **el revisor no tenía el repositorio**.

| Ronda | Consecuencia |
|---|---|
| Comité (V32) | Cuatro bloqueantes legítimos, todos respondibles con el código |
| Correcciones (07-10) | Seis controles marcados "pendiente de evidencia"; el documento **retrocedió** en cuatro puntos ya resueltos |
| Plan 98/100 | Protocolo circular, tres brechas ya cerradas, un bloqueo inventado |

El Anexo L de la V33 lo dice sin rodeos: *"Esta revisión no recibió el archivo
`BBDD/final/resultados_h3_asignacion_por_fila.csv`"*. Ese archivo existía en el
repositorio desde antes de esa revisión.

En ningún caso faltó análisis. Faltó entrega.

### 10. Regla de admisibilidad de observaciones

> **No se emite ninguna observación sobre el componente cuantitativo sin haber
> completado los cuatro pasos de acceso.** Si alguno no se completó, la
> observación se rotula **"no verificada por el revisor"** y no se incorpora al
> documento de la tesis como carencia del autor.

Los cuatro pasos:

```bash
git clone <repositorio> && cd <repositorio>
python -m venv .venv && .venv/Scripts/pip install -r requirements-lock.txt
python -m src.build_panel
```

4. Leer los cuatro archivos canónicos: `evidencia_entorno.txt`,
   `evidencia_metricas_por_particion.csv`,
   `evidencia_predicciones_por_fila.csv` y
   `resultados_h3_asignacion_por_fila.csv`.

**La asimetría que corrige esta regla:** marcar algo como "pendiente de
evidencia" cuando la evidencia estaba disponible y no se consultó atribuye al
autor una carencia que es del proceso de revisión. Las dos situaciones son
distintas y deben rotularse distinto:

| Situación | Rótulo correcto |
|---|---|
| La evidencia no existe | *pendiente de evidencia* |
| La evidencia existe y no se consultó | *no verificada por el revisor* |
| La evidencia existe y se consultó | *verificada* o *discrepante*, con la cifra |

### 11. Lectura obligatoria antes de observar sobre cada tema

Antes de escribir una observación sobre la columna izquierda, hay que haber
leído lo de la derecha.

| Si vas a observar sobre… | Antes lee obligatoriamente |
|---|---|
| Hiperparámetros, semillas, entorno | `BBDD/final/evidencia_entorno.txt`; `modelos()` en `src/models/supervisado.py` |
| Cualquier R², MAE o RMSE | `BBDD/final/evidencia_metricas_por_particion.csv` — **tiene las dos definiciones de R²** |
| Particiones, fuga de información, horizonte | `BBDD/final/evidencia_predicciones_por_fila.csv`; `particiones()` |
| Qué variables predicen el IDEC | `PREDICTORES` y `COMPONENTES_IDEC` en `src/models/supervisado.py` |
| El conteo 152 frente a 156 | `BBDD/final/resultados_h3_asignacion_por_fila.csv` |
| Clustering, regímenes, ARI | `resultados_h3_seleccion_k.csv`; `VARIABLES_PERFIL` y `estabilidad()` |
| Visitación CONAF y sus ceros | `BBDD/final/evidencia_conaf_correspondencia.csv` |
| El umbral del anillo | `BBDD/final/evidencia_sensibilidad_umbral_anillo.csv`; `CLUSTER_ANILLO` en `src/config.py` |
| Cobertura temporal de un predictor | `BBDD/final/evidencia_disponibilidad_predictores.csv` |
| Stock de inversión, depreciación | `DEPRECIACION_INFRAESTRUCTURA` y `ANIO_CALENTAMIENTO_STOCK` |
| Construcción del IDEC y normalización | `src/features/idec.py` |

### 12. Cuatro errores que esta regla habría evitado

1. **Proponer `d2, d3, d4` como predictores.** Una lectura de
   `COMPONENTES_IDEC` lo impide. Treinta segundos de trabajo.
2. **Declarar el anillo irreconstruible.** Una lectura de `CLUSTER_ANILLO`
   muestra que la regla es conteo de alojamientos, no distancia.
3. **Marcar el 152/156 como pendiente.** El archivo con las 152 asignaciones
   existía.
4. **Repetir el barrido de clustering.** `resultados_h3_seleccion_k.csv` ya
   contenía un superconjunto de lo propuesto.

### 13. Señales para rechazar un plan o una observación de entrada

Si un documento de revisión presenta cualquiera de estos rasgos, devolverlo
antes de incorporarlo:

- **Usa `datos.json` como fuente del análisis.** Es el export del simulador, con
  cuatro decimales y predicciones precomputadas. No es la base.
- **Propone como predictor cualquier elemento de `COMPONENTES_IDEC`**, es decir
  `trabajadores_pc`, `ventas_pc`, `renta_pc`, `empresas_pc`,
  `alojamientos_por_mil_hab`, `D2_empleo`, `D3_ingresos`, `D4_capacidad`
  o `IDEC`.
- **Asigna puntajes** sin rúbrica que los respalde.
- **Cita un archivo del repositorio sin haberlo abierto**, o cita rutas y
  objetos que no existen (`04_unsupervised_clustering.ipynb`, `rf_model`,
  `tscv`, `TimeSeriesSplit`).
- **Mezcla las dos definiciones de R²** sin nombrarlas.
- **Propone "reejecutar" sin haber instalado `requirements-lock.txt`.**

### 14. Cifras canónicas

Toda cifra del componente cuantitativo debe coincidir con esta tabla. Si una
cifra del texto difiere, el texto está equivocado.

**Configuración y entorno**

| | |
|---|---|
| Random Forest | `n_estimators=500`, `min_samples_leaf=3`, `max_features='sqrt'`, `random_state=42` |
| Por defecto de scikit-learn | `max_depth=None`, `min_samples_split=2`, `bootstrap=True`, `criterion='squared_error'` |
| Sintonización | **ninguna**: sin GridSearch ni RandomSearch |
| Entorno | Python 3.12.7, scikit-learn 1.9.0, numpy 1.26.4, pandas 2.2.2, scipy 1.13.1 |
| Predictores / objetivo | 15 / `IDEC` |

**H2 — capacidad predictiva (Random Forest)**

| Esquema | R² agrupado | R² medio de pliegues | MAE | n prueba |
|---|---|---|---|---|
| Aleatorio | 0,7989 | 0,8001 | 0,0582 | 152 |
| Bloques | **0,7621** | **0,7877** | 0,0651 | 152 |
| Temporal | **0,8087** | 0,8068 | 0,0585 | 65 |
| Por comuna | **−0,3619** | −18,677 | 0,1699 | 152 |

Especificación previa a CONAF: 0,6306 agrupado y **0,674** medio de pliegues.
El antiguo "0,68" es esta última celda.

**Validación temporal, por año de prueba** (horizonte de un año, cinco
iteraciones de origen móvil)

| Año | n entren. | R² | MAE | RMSE |
|---|---|---|---|---|
| 2020 | 87 | 0,8417 | 0,0476 | 0,0688 |
| 2021 | 100 | 0,7745 | 0,0679 | 0,0814 |
| 2022 | 113 | 0,7814 | 0,0642 | 0,0892 |
| 2023 | 126 | 0,8407 | 0,0565 | 0,0726 |
| 2024 | 139 | 0,7956 | 0,0562 | 0,0870 |

**H1 — importancia por permutación** (R², pliegue de prueba, 30 repeticiones,
esquema de bloques)

| Variable | Importancia |
|---|---|
| Visitación SNASPE p.c. | 0,345 |
| Ventas construcción p.c. | 0,123 |
| Trabajadores recreativas p.c. | 0,070 |
| Ventas inmobiliarias p.c. | 0,067 |
| Ventas recreativas p.c. | 0,050 |

Advertencia obligatoria: **población y población laboral son colineales en
r = 1,000**. Sus importancias individuales (0,0428 y 0,0388) no son
interpretables por separado.

**H3 — regímenes y convergencia**

| | |
|---|---|
| Algoritmo | **jerárquico**, nivel comuna-año, k = 4, sobre 7 `VARIABLES_PERFIL` con log1p y estandarización |
| Conteos | **83, 45, 12, 12** = 152 |
| Las 4 ausentes | Melipeuco y Lonquimay, 2013 y 2014 |
| ARI, remuestreo por fila | **0,7949** (p10 = 0,6177) |
| ARI, remuestreo por comuna | **0,7045** (p10 = 0,3817) |
| Theil | 0,537174 (2013) → 0,249523 (2024) = **−53,5 %** |
| Theil sin Pucón, misma escala | −35,5 % |
| Theil sin Pucón, Min-Max recalibrado | −32,4 % |
| β-convergencia | **−0,032880** (p = 0,000212; R² = 0,7272; n = 13) |
| Especificación de β | `g = (ln y_2024 − ln y_2013)/11` sobre `ln y_2013` |

**Robusteces ejecutadas**

| Prueba | Resultado |
|---|---|
| Dummy COVID 2020-2021 | importancia **0,0000** (puesto 15 de 16); MCO con efecto fijo de comuna: coef = −0,00391, **p = 0,703**; R² temporal 0,8087 → 0,8229 |
| IDEC sin D4 | Spearman 2024 = **0,8956**; β = **−0,055017**; R² temporal 0,8087 → 0,7624 |
| Escala no acotada | 5 de 6 especificaciones con β negativa y significativa; falla solo el índice z compuesto (p = 0,26) |
| Umbral del anillo | β entre −0,0325 y −0,0415, p < 0,001 en los tres universos |
| Normalización del IDEC | Spearman mínimo **0,914971** → el intervalo es **0,91 a 1,00** |
| Enmascaramiento tributario | rubro I **0 %**; recreativas 33 %; inmobiliarias 32 % |
| Stock de inversión | δ = **0,05**, acumulación desde **2000**; no parte de cero en 2013 |

### 15. Límites que no se cierran con evidencia

Estos son reales y deben permanecer declarados. Ninguna reejecución los resuelve.

1. **Ausencia de D1.** El índice no mide flujos turísticos. La EMAT por destino
   está suspendida desde abril de 2020.
2. **Trece unidades territoriales.** Las 156 filas no son 156 unidades
   independientes.
3. **R² por comuna negativo (−0,3619).** El modelo no transfiere a comunas no
   vistas. Debe decirse sin matizar — y **ninguna especificación que lo mejore
   sustancialmente debe aceptarse sin verificar antes que no sea circular.**
4. **El registro de alojamientos no tiene fecha de inscripción.** D4 aporta
   variación entre comunas, no a lo largo del tiempo. Un "registro fechado" no
   es obtenible de la fuente.
5. **Umbrales de las hipótesis no preregistrados.** Fijarlos ahora sería
   retrospectivo.
6. **La magnitud de la convergencia es sensible.** Sin Pucón la caída de Theil
   pasa de −53,5 % a cerca de −33 %. La dirección es sólida; la magnitud
   requiere cautela con n = 13.
