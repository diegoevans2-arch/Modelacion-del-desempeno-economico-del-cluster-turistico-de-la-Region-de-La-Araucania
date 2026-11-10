---
tipo: respuesta técnica
destinatario: asistente de IA de Germán Patricio Barra Ávila
asunto: Paralelismo anidado en `importancia_variables()` — corrección aplicada
elaborado por: Diego Evans Pérez Paz — componente de Machine Learning
fecha: 2026-10-22
commits: aeed847 y f3c208f, en `main`
---

# Respuesta — Paralelismo anidado en `importancia_variables()`

## 0. Antes de leer: hay que actualizar el repositorio

`main` avanzó de `dee060a` a `f3c208f` (dos commits). Nada de lo que sigue está
en una copia que no se haya actualizado:

```bash
git fetch origin
git checkout main
git pull --ff-only origin main
```

Debe quedar `f3c208f Documentar el paralelismo anidado de importancia_variables`
como último commit. Si se trabaja en otra rama, la que se movió es `main`.

---

## 1. Veredicto general

**El diagnóstico enviado era correcto en la causa y acertó el mecanismo con
precisión.** La corrección está aplicada y medida. Hay, sin embargo, **dos
puntos del reporte que no se sostuvieron al verificarlos**, y uno de ellos
afecta la verificación que se declaraba obligatoria. Van en §4, con evidencia.

| # | Lo planteado en el reporte | Veredicto |
|---|---|---|
| 1 | La función es patológicamente lenta en Windows | **Confirmado** — 277 s por corrida |
| 2 | Causa: paralelismo anidado; `permutation_importance` llama a `predict()` del orden de `n_predictores × n_repeticiones` por pliegue (15 × 30 = 450) sobre conjuntos de decenas de filas | **Confirmado, y exacto** |
| 3 | En Windows el arranque es por *spawn*, de modo que domina el arranque de procesos y no el cálculo | **Confirmado** |
| 4 | Inundación de `UserWarning` de `sklearn.utils.parallel.delayed` | **Confirmado** (volumen variable, ver §3) |
| 5 | Los valores de referencia son ≈ 0,345 y ≈ 0,123 con `esquema="bloques"` | **Confirmados** |
| 6 | Bastaba fijar **o bien** el `n_jobs` del bosque **o bien** el de `permutation_importance` | **Incorrecto — hacían falta los dos** (§4.1) |
| 7 | La corrección es «sin efecto numérico alguno»; `n_jobs` sólo reparte el trabajo | **Inexacto** — cierto para `permutation_importance`, falso para el `predict()` del bosque (§4.2) |
| 8 | Verificación obligatoria: la tabla debe coincidir antes y después «hasta el último decimal» | **Inalcanzable tal como estaba especificada**, y no por la corrección (§4.2) |

Se usó el intérprete indicado: Python 3.12.7 (Anaconda), scikit-learn 1.9.0,
joblib 1.4.2, numpy 1.26.4, pandas 2.2.2.

---

## 2. Qué se hizo

En `src/models/supervisado.py::importancia_variables()` quedaron fijados **los
dos** `n_jobs`:

```python
m = RandomForestRegressor(..., random_state=42, n_jobs=1).fit(X[tr], y[tr])
r = permutation_importance(m, X[te], y[te], n_repeats=n_repeticiones,
                           random_state=42, n_jobs=None)
```

Se agregó al docstring una nota que explica por qué están fijados, con las
cifras medidas, para que nadie los «optimice» de vuelta a `-1`.

**No se tocaron** los bosques de `modelos()` ni de `entrenar()`, que conservan
`n_jobs=-1`: ahí el paralelismo sí rinde, porque entrenan una vez y no quedan
anidados dentro de cientos de `predict()`.

---

## 3. Resultados medidos

Panel vigente (`BBDD/final/panel_idec_comunal.csv`), `esquema="bloques"`,
`n_repeticiones=30`, un proceso limpio por configuración:

| bosque | `permutation_importance` | tiempo | `stderr` |
|---|---|---|---|
| `-1` | `-1` | 276,5 s / 278,5 s | hasta 765 KB |
| `1` | `-1` | 158,7 s / 153,2 s | 0 |
| `-1` | `None` | **520,9 s** | 0 |
| **`1`** | **`None`** | **73,8 s / 75,0 s** | **0** |

Sobre la función real ya corregida: **78,4 s y 70,3 s** en dos corridas
consecutivas, contra **297,4 s** antes. **Mejora de 3,7×, y `stderr` vacío.**

Sobre las advertencias: el volumen era errático —0, 1.950 y 2.369 líneas en
corridas de la *misma* configuración, hasta 765 KB—, porque depende de cuántos
procesos nuevos se creen y de los filtros activos, ya que el filtro por omisión
de Python deduplica *por proceso*. Las 9.000 líneas y 27 MB reportadas son
perfectamente compatibles con esto: en la configuración `bosque -1 + perm None`
se contaron **79.870** advertencias dentro del proceso. Tras la corrección es
**cero en todas las corridas**.

---

## 4. Las dos correcciones al diagnóstico

### 4.1. Las dos opciones propuestas no eran equivalentes

El reporte las ofrecía como alternativas («o bien… o bien»). No lo son:

- Fijar **sólo el bosque** deja la función en 155 s. Mejora, pero a medias.
- Fijar **sólo `permutation_importance`** la lleva a **521 s**, casi el doble
  del original. Elimina el único paralelismo que sí rinde —el reparto de los 15
  predictores, que son tareas gruesas— y deja intacto el anidamiento fino.

La razón de fondo es que **a esta escala el pool de procesos no se amortiza
nunca**: son 75 tareas (15 predictores × 5 pliegues) sobre datos diminutos. Por
eso la configuración ganadora es la que no usa procesos en absoluto.

### 4.2. El `n_jobs` del bosque sí tiene efecto numérico

Esto es lo más importante del documento.

El razonamiento enviado —«con `random_state=42` el resultado es determinista;
`n_jobs` sólo reparte el trabajo»— **es correcto para `permutation_importance`**,
y se comprobó: sortea una única semilla (`random_seed`, en
`sklearn/inspection/_permutation_importance.py:278`) y la entrega idéntica a
todas las tareas, de modo que las permutaciones no dependen del número de
procesos. Las corridas con `-1` y con `None` son idénticas al bit.

**Pero no se extiende al `predict()` del bosque.** En
`sklearn/ensemble/_forest.py:1077`, `ForestRegressor.predict()` crea un
`threading.Lock()` y acumula los 500 árboles sobre un arreglo compartido:

```python
with lock:
    out[0] += prediction
```

El orden en que los hilos ganan el lock varía entre corridas, y **la suma de
flotantes no es asociativa**. Con `n_jobs=-1` los últimos dígitos cambian de
una corrida a otra.

La consecuencia es que la verificación declarada obligatoria no podía
cumplirse, y no por la corrección:

| comparación | ¿idéntico? | distancia máxima |
|---|---|---|
| versión antigua vs. versión antigua (dos corridas) | **no** | 820 ULP (5,6e−17) |
| **versión corregida vs. versión corregida** | **sí, bit a bit** | **0 ULP** |
| antigua vs. corregida | no | 217 ULP (6,9e−17) |

Nótese el orden de magnitud: **la diferencia entre la versión antigua y la
corregida es menor que la que la versión antigua tenía consigo misma.** La
corrección no introduce sesgo alguno; fija un punto determinista dentro del
ruido que ya existía. Dicho de otro modo, **la corrección crea la
reproducibilidad que la verificación daba por supuesta**.

Un corolario que conviene tener presente:
`BBDD/final/resultados_h1_importancia.csv` fue generado por la versión antigua
y por lo tanto **no es exactamente reproducible ni por el código que lo
produjo**. Se dejó como estaba, para no alterar un resultado comprometido sin
necesidad. Regenerarlo lo volvería estable de aquí en adelante y no movería
ninguna cifra publicada.

---

## 5. Efecto sobre las cifras de la tesis: ninguno

De los 15 valores de la tabla, **4 quedan idénticos** y los 11 restantes
coinciden en 16 o 17 decimales. La diferencia máxima es **2,8e−17**. **El orden
del ranking no se mueve.**

| variable | CSV comprometido | tras la corrección |
|---|---|---|
| `visitas_snaspe_pc` | 0,3452442151519476 | **idéntico** |
| `ventas_uf_construccion_pc` | 0,12286405348828597 | 0,122864053488285**95** |

`r2_medio_folds` queda en 0,7877458268910897, ahora estable (antes
0,7877458268910899, valor que de por sí oscilaba entre corridas).

Las cifras publicadas van a tres decimales —**0,345 / 0,123 / R² = 0,788**—, muy
por encima de donde ocurre la diferencia. **No hay nada que corregir en los
capítulos, las tablas ni el simulador.**

---

## 6. Una optimización que se probó y se descartó

Como el `fit` del bosque sí se beneficia del paralelismo —500 árboles es tarea
gruesa—, se midió la variante aparentemente óptima: entrenar con `n_jobs=-1` y
bajar a `m.n_jobs = 1` antes de permutar.

Da **70,3 s**, exactamente lo mismo que la corrección simple, y es idéntica al
bit. Con 5 ajustes sobre 120×15 datos el entrenamiento no alcanza a pesar. **No
se adoptó:** la línea extra no compra nada medible. Queda documentada para que
no se vuelva a intentar.

---

## 7. Qué no hacer de aquí en adelante

- **No devolver ninguno de los dos `n_jobs` a `-1`.** Cuadruplica el tiempo,
  reinstala la inundación de `stderr` y —lo más importante para una tesis—
  vuelve la tabla no reproducible.
- **No «homogeneizar»** los `n_jobs` del módulo: los de `modelos()` y
  `entrenar()` deben seguir en `-1`. La asimetría es deliberada.
- **Criterio de verificación, de ahora en adelante:** dos corridas consecutivas
  de `importancia_variables()` deben dar resultados **idénticos hasta el último
  bit**. Si no lo hacen, alguien devolvió un `n_jobs` a `-1`.

```python
import pandas as pd
from src import config
from src.models import supervisado as sup

panel = pd.read_csv(config.FINAL_DIR / "panel_idec_comunal.csv")
tabla = sup.importancia_variables(panel, esquema="bloques", n_repeticiones=30)
print(tabla.attrs["r2_medio_folds"])   # 0.7877458268910897, estable
```

---

## 8. Dónde quedó cada cosa

| Qué | Dónde |
|---|---|
| La corrección | `src/models/supervisado.py::importancia_variables()`, commit `aeed847` |
| La nota técnica completa, con todas las mediciones | `Documentación/Nota_tecnica_paralelismo_importancia_variables.md`, commit `f3c208f` |
| Advertencia para quien continúe | `Documentación/CONTEXTO_PROYECTO_handoff.md`, §10 y §11 |
| Este documento | Enviado por separado; **no** está en el repositorio, así que el `pull` no lo trae |

Ambos commits están en `origin/main`. **Recordar el `git pull` de §0.**
