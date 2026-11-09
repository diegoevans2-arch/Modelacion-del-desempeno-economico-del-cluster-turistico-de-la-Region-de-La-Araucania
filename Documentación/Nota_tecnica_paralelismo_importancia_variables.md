---
tipo: nota técnica
tema: Paralelismo anidado y reproducibilidad en `importancia_variables()` (H1)
proyecto: Tesis Doctoral — Barra Ávila
estado: cerrado
fecha: 2026-10-22
---

# Nota técnica — Paralelismo anidado en `importancia_variables()`

## 1. El síntoma

`src/models/supervisado.py::importancia_variables()` —la función que produce
la tabla de importancias de H1— tardaba del orden de **4,6 minutos** por
corrida en Windows y vertía en `stderr` centenares de miles de bytes de
advertencias de joblib. El cálculo en sí es diminuto: 156 observaciones, 15
predictores, 5 pliegues.

## 2. La causa: dos niveles de joblib, uno dentro del otro

La función construía el bosque con `n_jobs=-1` y acto seguido se lo entregaba
a `permutation_importance`, también con `n_jobs=-1`:

```python
m = RandomForestRegressor(..., n_jobs=-1).fit(X[tr], y[tr])
r = permutation_importance(m, X[te], y[te], n_repeats=30, n_jobs=-1)
```

`permutation_importance` llama a `predict()` tantas veces como
`n_predictores × n_repeticiones`, es decir **15 × 30 = 450 por pliegue**
(2.250 en total), y cada llamada opera sobre un conjunto de prueba de
**decenas de filas**: con `esquema="bloques"`, cada bloque son dos o tres años
de 13 comunas.

Sobre piezas de ese tamaño, el reparto del trabajo cuesta más que el trabajo.
El `n_jobs=-1` externo levanta procesos de joblib —en Windows el arranque es
por **spawn**, no por `fork`, de modo que cada proceso reimporta el intérprete
y las bibliotecas— y el `n_jobs=-1` interno vuelve a repartir los 500 árboles
en cada uno de esos 2.250 `predict()`. El costo dominante pasa a ser el
arranque de procesos, no la aritmética.

## 3. Las cuatro configuraciones, medidas

Panel vigente (`BBDD/final/panel_idec_comunal.csv`), `esquema="bloques"`,
`n_repeticiones=30`, un proceso limpio por configuración. Python 3.12.7,
scikit-learn 1.9.0, joblib 1.4.2.

| bosque | `permutation_importance` | tiempo | `stderr` |
|---|---|---|---|
| `-1` | `-1` | 276,5 s / 278,5 s | hasta 765 KB |
| `1` | `-1` | 158,7 s / 153,2 s | 0 |
| `-1` | `None` | **520,9 s** | 0 |
| **`1`** | **`None`** | **73,8 s / 75,0 s** | **0** |

Dos lecturas importantes:

- **Hacía falta fijar los dos.** Corregir sólo el bosque dejaba la función en
  155 s; corregir sólo `permutation_importance` la empeoraba a 521 s, casi el
  doble del original, porque elimina el único paralelismo que sí rinde —el
  reparto de los 15 predictores, que son tareas gruesas.
- **A esta escala el pool de procesos no se amortiza nunca.** Son 75 tareas
  (15 predictores × 5 pliegues) sobre datos diminutos.

Sobre la función real ya corregida: **78,4 s y 70,3 s** en dos corridas
consecutivas, con `stderr` vacío. La mejora es de **3,7×**.

El volumen de advertencias en la versión antigua era errático: 0, 1.950 y
2.369 líneas en corridas de la misma configuración (hasta 765 KB; el reporte
original que motivó la revisión observó más de 9.000 líneas y 27 MB). Depende
de cuántos procesos nuevos se creen y de los filtros de advertencias activos,
porque el filtro por omisión de Python deduplica *por proceso*. Tras la
corrección es cero en todas las corridas.

## 4. Hallazgo colateral: la versión anterior no era reproducible

Al verificar que la corrección no alterara las cifras apareció algo que no se
buscaba: **el código anterior no reproducía sus propios resultados.**

| comparación | ¿idéntico? | distancia máxima |
|---|---|---|
| anterior vs. anterior (dos corridas) | **no** | 820 ULP (5,6e−17) |
| **corregido vs. corregido** | **sí, bit a bit** | **0 ULP** |
| anterior vs. corregido | no | 217 ULP (6,9e−17) |

La causa está en `sklearn/ensemble/_forest.py`. `ForestRegressor.predict()`
crea un `threading.Lock()` y acumula los 500 árboles sobre un arreglo
compartido:

```python
with lock:
    out[0] += prediction
```

El orden en que los hilos ganan el lock varía entre corridas, y la suma de
flotantes **no es asociativa**: los últimos dígitos cambian. Con `n_jobs=1` la
acumulación es secuencial y el resultado queda fijo.

Conviene subrayar la consecuencia: la diferencia entre la versión anterior y
la corregida (217 ULP) es **menor que la que la versión anterior tenía consigo
misma** (820 ULP). La corrección no introduce un sesgo; fija un punto
determinista dentro del ruido que ya existía. Dicho de otro modo, **crea** la
reproducibilidad que la verificación daba por supuesta.

En cambio el `n_jobs` de `permutation_importance` sí es numéricamente neutro,
y se comprobó: sortea una única semilla (`random_seed`) y la reparte idéntica
a todas las tareas, de modo que las permutaciones no dependen del número de
procesos. Las corridas con `-1` y con `None` son idénticas al bit. Está en
`None` nada más que por tiempo.

## 5. Efecto sobre las cifras de la tesis

Ninguno. De los 15 valores de `BBDD/final/resultados_h1_importancia.csv`, 4
quedan **idénticos** y los 11 restantes coinciden en 16 o 17 decimales; la
diferencia máxima es **2,8e−17**. El orden del ranking no se mueve.

| variable | CSV comprometido | tras la corrección |
|---|---|---|
| `visitas_snaspe_pc` | 0,3452442151519476 | **idéntico** |
| `ventas_uf_construccion_pc` | 0,12286405348828597 | 0,122864053488285**95** |

`r2_medio_folds` queda en 0,7877458268910897 (antes 0,7877458268910899, valor
que de por sí oscilaba entre corridas). Las cifras publicadas van a tres
decimales —0,345 / 0,123 / R² = 0,788—, muy por encima de donde ocurre la
diferencia.

Queda una consecuencia menor y conocida: `resultados_h1_importancia.csv` fue
generado por la versión antigua, de modo que **no es exactamente reproducible
ni por el código que lo produjo**. Regenerarlo lo volvería estable de aquí en
adelante. Se dejó como estaba por no alterar un resultado comprometido sin
necesidad.

## 6. La optimización que no sirve

Como el `fit` del bosque sí se beneficia del paralelismo —500 árboles es una
tarea gruesa—, se probó la variante aparentemente óptima: entrenar con
`n_jobs=-1` y bajar a `m.n_jobs = 1` antes de permutar.

Da **70,3 s**, exactamente lo mismo que la corrección simple (una de cuyas
corridas midió también 70,3 s), y es idéntica al bit. Con 5 ajustes sobre
120×15 datos, el entrenamiento no alcanza a pesar. **No se adoptó**: la línea
extra no compra nada medible.

## 7. Qué no hacer

`importancia_variables()` lleva los dos `n_jobs` fijados y una nota en el
docstring que explica por qué. Devolver cualquiera de los dos a `-1`
cuadruplica el tiempo, reinstala la inundación de `stderr` y —lo más
importante para una tesis— **vuelve la tabla no reproducible**.

Los bosques de `modelos()` y `entrenar()` conservan `n_jobs=-1`
deliberadamente: ahí sí rinde, porque entrenan una vez y no quedan anidados
dentro de cientos de `predict()`.

## 8. Cómo reproducir la medición

```python
import pandas as pd
from src import config
from src.models import supervisado as sup

panel = pd.read_csv(config.FINAL_DIR / "panel_idec_comunal.csv")
tabla = sup.importancia_variables(panel, esquema="bloques", n_repeticiones=30)
print(tabla.attrs["r2_medio_folds"])   # 0.7877458268910897, estable
```

Dos corridas deben dar resultados idénticos hasta el último bit. Si no lo
hacen, alguien devolvió un `n_jobs` a `-1`.
