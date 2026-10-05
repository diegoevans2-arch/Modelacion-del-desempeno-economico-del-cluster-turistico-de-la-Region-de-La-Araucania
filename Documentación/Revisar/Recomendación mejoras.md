
**Punto 1 — Tabla 4.7 suma 152 vs. 156**

La acción más rápida es abrir el notebook `04_unsupervised_clustering.ipynb` y ejecutar esta línea después del K-Means:

python

Plain Text

```
df_regimenes = pd.DataFrame({'comuna': X.index.get_level_values('comuna'),                              'anio': X.index.get_level_values('anio'),                              'regimen': kmeans.labels_})print(df_regimenes.shape[0])  # debe dar 156df_regimenes['regimen'].value_counts()  # debe sumar 156
```

Si el conteo da 152, probablemente hay 4 observaciones con NaN en algún predictor que K-Means excluyó silenciosamente. La solución es identificarlas con `X[X.isna().any(axis=1)]`, imputar o documentar la exclusión, y actualizar la tabla con los conteos reales. Si da 156, el error es solo de transcripción en la tabla y se corrige directamente.

---

**Punto 2 — Hiperparámetros de Random Forest**

Ejecuta esto sobre el modelo ya entrenado en `03_supervised_models.ipynb`:

python

Plain Text

```
print(rf_model.get_params())import sklearn; print(sklearn.__version__)import sys; print(sys.version)
```

Eso imprime todos los parámetros. Cópialos al Anexo C con este formato mínimo exigible por el tribunal: n_estimators, max_depth (None = sin límite), min_samples_leaf, max_features, random_state y la versión de scikit-learn. Si no fijaste random_state en su momento, debes declararlo como no fijado y señalar que los resultados pueden variar entre ejecuciones, lo cual es una limitación honesta y aceptable.

---

**Punto 3 — Horizonte de validación temporal**

En el mismo notebook busca el bloque de `TimeSeriesSplit` o el loop de origen móvil y agrega:

python

Plain Text

```
for fold, (train_idx, test_idx) in enumerate(tscv.split(X)):    anios_train = sorted(X.iloc[train_idx].index.get_level_values('anio').unique())    anios_test  = sorted(X.iloc[test_idx].index.get_level_values('anio').unique())    print(f"Fold {fold+1}: entrenamiento {anios_train[0]}–{anios_train[-1]}, prueba {anios_test}")
```

Con eso generas una tabla de 4–5 filas que va directo al §3.10.3.1. El tribunal necesita saber si estás prediciendo 1 año adelante o 3 — eso cambia completamente la interpretación del R²=0,809.

---

**Punto 4 — Trazabilidad CONAF**

Este es el más delicado porque puede requerir revisar el script de integración. Ve a `src/data/` y busca cómo se cargó CONAF. Las preguntas a responder son tres:

- ¿Se usó el código de comuna del área protegida o se asignó al centroide? Si un área abarca Pucón y Curarrehue, ¿qué pasó?
- Para las 4 comunas con cero en todos los años (Carahue, Nueva Imperial, Saavedra, Villarrica): ¿no tienen área protegida registrada por CONAF, o tienen área pero con cero visitas, o el dato estaba faltante y se imputó como cero?
- ¿Cuál es el denominador de la tasa per cápita — población total o población en edad laboral?

Con esa información escribes un párrafo de 4–5 líneas en §3.6.6 que cierra la observación. Si descubres que los ceros son genuinamente "sin área protegida", eso es perfectamente defendible. Si son imputaciones, hay que declararlo.

---

**Orden de prioridad recomendado**

Empieza por el Punto 2 porque toma 5 minutos y lo cierra completamente. Luego el Punto 3 que también es una corrida de código. El Punto 1 depende de si es error de transcripción (rápido) o NaN estructural (requiere decisión metodológica). El Punto 4 es el que puede tomar más tiempo si el script de integración no está bien documentado, pero su resolución fortalece significativamente la defensa del hallazgo más importante de la tesis.