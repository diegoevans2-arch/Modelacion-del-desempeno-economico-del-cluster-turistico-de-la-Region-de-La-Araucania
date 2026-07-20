"""Modelos supervisados para estimar el IDEC (H2).

DOS RIESGOS QUE ESTE MÓDULO EXISTE PARA EVITAR

1. **Circularidad.** El IDEC se construye a partir de `trabajadores_pc`,
   `ventas_pc`, `renta_pc`, `empresas_pc` y `alojamientos_por_mil_hab`. Usar
   cualquiera de ellas como predictor no mide capacidad predictiva: mide la
   fórmula del índice. `PREDICTORES` excluye explícitamente los componentes y
   `verificar_circularidad()` aborta si alguno se cuela.

2. **Fuga temporal en la validación.** Con datos panel, un K-fold aleatorio
   pone observaciones de la misma comuna en años contiguos a ambos lados de la
   partición. Como el IDEC de Pucón en 2016 es casi el de 2015, el modelo
   "predice" algo que ya vio. El R² resultante está inflado y no dice nada
   sobre capacidad predictiva real.

   Se implementan tres esquemas honestos y, deliberadamente, también el
   K-fold aleatorio — no para usarlo, sino para exhibir la magnitud del sesgo
   en la tesis:

   - `comuna`  : GroupKFold por comuna → generalizar a territorios no vistos
   - `temporal`: entrenar en t<=T, predecir t>T → capacidad de pronóstico
   - `bloques` : K-fold sobre bloques temporales contiguos
   - `aleatorio`: K-fold estándar (CONTROL, con fuga)
"""

import numpy as np
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, RidgeCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GroupKFold, KFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor

# Componentes del IDEC: prohibidos como predictores.
COMPONENTES_IDEC = {
    "trabajadores_pc", "ventas_pc", "renta_pc", "empresas_pc",
    "alojamientos_por_mil_hab", "n_trabajadores", "ventas_uf", "renta_uf",
    "n_empresas", "n_alojamientos", "alojamientos_pc",
    "D2_empleo", "D3_ingresos", "D4_capacidad", "IDEC",
}

PREDICTORES = [
    # Inversión pública (BIP) — exógena al IDEC
    "inversion_pc_lag2",
    "stock_capital_pc_lag1",
    # Sectores conexos del clúster (SII, rubros distintos del turístico)
    "ventas_uf_comercio_pc",
    "ventas_uf_transporte_pc",
    "ventas_uf_recreativas_pc",
    "ventas_uf_inmobiliarias_pc",
    "ventas_uf_construccion_pc",
    "n_trabajadores_comercio_pc",
    "n_trabajadores_transporte_pc",
    "n_trabajadores_recreativas_pc",
    # Demografía
    "poblacion",
    "poblacion_laboral",
    # Tendencia
    "anio",
]

OBJETIVO = "IDEC"


def verificar_circularidad(predictores, objetivo=OBJETIVO):
    """Aborta si algún predictor es componente del índice."""
    contaminados = set(predictores) & COMPONENTES_IDEC
    if contaminados:
        raise ValueError(
            "Predictores circulares (son componentes del IDEC): "
            f"{sorted(contaminados)}"
        )


def modelos():
    """Los modelos del protocolo, más líneas base honestas.

    Se incluye Ridge además del OLS: los predictores están fuertemente
    correlacionados entre sí (población y población laboral, las ventas de los
    distintos sectores conexos), y un OLS sin regularizar extrapola de forma
    errática en esas condiciones. Comparar Random Forest sólo contra el OLS
    crudo sería construir un hombre de paja — la hipótesis central de la tesis
    exige que el contendiente econométrico esté en su mejor versión.
    """
    return {
        "Media (base)": DummyRegressor(strategy="mean"),
        "Regresión lineal": Pipeline(
            [("esc", StandardScaler()), ("m", LinearRegression())]
        ),
        "Ridge (regularizada)": Pipeline(
            [("esc", StandardScaler()),
             ("m", RidgeCV(alphas=np.logspace(-3, 3, 25)))]
        ),
        "Árbol de decisión": DecisionTreeRegressor(
            max_depth=4, min_samples_leaf=8, random_state=42
        ),
        "Random Forest": RandomForestRegressor(
            n_estimators=500, min_samples_leaf=3, max_features="sqrt",
            random_state=42, n_jobs=-1
        ),
    }


def particiones(df, esquema, n_splits=5, col_comuna="comuna", col_anio="anio"):
    """Genera pares (train_idx, test_idx) según el esquema de validación."""
    n = len(df)
    idx = np.arange(n)

    if esquema == "comuna":
        grupos = df[col_comuna].to_numpy()
        k = min(n_splits, len(np.unique(grupos)))
        yield from GroupKFold(n_splits=k).split(idx, groups=grupos)

    elif esquema == "temporal":
        anios = np.sort(df[col_anio].unique())
        # Origen móvil: cada corte entrena con el pasado y prueba el año siguiente.
        for corte in anios[-n_splits:]:
            tr = idx[df[col_anio].to_numpy() < corte]
            te = idx[df[col_anio].to_numpy() == corte]
            if len(tr) and len(te):
                yield tr, te

    elif esquema == "bloques":
        anios = np.sort(df[col_anio].unique())
        bloques = np.array_split(anios, n_splits)
        for b in bloques:
            te = idx[np.isin(df[col_anio].to_numpy(), b)]
            tr = idx[~np.isin(df[col_anio].to_numpy(), b)]
            if len(tr) and len(te):
                yield tr, te

    elif esquema == "aleatorio":
        yield from KFold(n_splits=n_splits, shuffle=True, random_state=42).split(idx)

    else:
        raise ValueError(f"esquema no reconocido: {esquema!r}")


def evaluar(df, predictores=None, objetivo=OBJETIVO,
            esquemas=("comuna", "temporal", "bloques", "aleatorio"),
            n_splits=5):
    """Evalúa cada modelo bajo cada esquema de validación.

    Returns
    -------
    DataFrame con MAE, RMSE y R² por modelo y esquema.
    """
    predictores = predictores or PREDICTORES
    verificar_circularidad(predictores, objetivo)

    d = df.dropna(subset=predictores + [objetivo]).reset_index(drop=True)
    X = d[predictores].to_numpy(dtype=float)
    y = d[objetivo].to_numpy(dtype=float)

    filas = []
    for esquema in esquemas:
        cortes = list(particiones(d, esquema, n_splits=n_splits))
        for nombre, modelo in modelos().items():
            obs, pred = [], []
            for tr, te in cortes:
                m = _clonar(modelo)
                m.fit(X[tr], y[tr])
                obs.append(y[te])
                pred.append(m.predict(X[te]))
            obs = np.concatenate(obs)
            pred = np.concatenate(pred)
            filas.append(
                {
                    "esquema": esquema,
                    "modelo": nombre,
                    "n_test": len(obs),
                    "MAE": round(mean_absolute_error(obs, pred), 4),
                    "RMSE": round(np.sqrt(mean_squared_error(obs, pred)), 4),
                    "R2": round(r2_score(obs, pred), 4),
                }
            )
    return pd.DataFrame(filas)


def importancia_variables(df, predictores=None, objetivo=OBJETIVO,
                          n_repeticiones=30, esquema="bloques", n_splits=5):
    """Importancia por permutación, evaluada fuera de muestra.

    La importancia interna de Random Forest (`feature_importances_`) se calcula
    sobre los datos de entrenamiento y premia a las variables de alta
    cardinalidad. La permutación sobre el conjunto de prueba mide lo que
    realmente interesa: cuánto se degrada la predicción al romper la variable.

    El esquema por defecto es temporal/bloques, NO por comuna: bajo validación
    por comuna el modelo tiene R² negativo, y permutar variables de un modelo
    que ya predice peor que la media no informa sobre relevancia. La
    importancia sólo es interpretable donde el modelo efectivamente predice.
    """
    from sklearn.inspection import permutation_importance

    predictores = predictores or PREDICTORES
    verificar_circularidad(predictores, objetivo)

    d = df.dropna(subset=predictores + [objetivo]).reset_index(drop=True)
    X = d[predictores].to_numpy(dtype=float)
    y = d[objetivo].to_numpy(dtype=float)

    acum = {p: [] for p in predictores}
    r2_folds = []
    for tr, te in particiones(d, esquema, n_splits=n_splits):
        m = RandomForestRegressor(
            n_estimators=500, min_samples_leaf=3, max_features="sqrt",
            random_state=42, n_jobs=-1
        ).fit(X[tr], y[tr])
        r2_folds.append(r2_score(y[te], m.predict(X[te])))
        r = permutation_importance(
            m, X[te], y[te], n_repeats=n_repeticiones, random_state=42, n_jobs=-1
        )
        for i, p in enumerate(predictores):
            acum[p].append(r.importances_mean[i])

    tabla = (
        pd.DataFrame(
            [{"variable": p, "importancia": np.mean(v), "desv": np.std(v)}
             for p, v in acum.items()]
        )
        .sort_values("importancia", ascending=False)
        .reset_index(drop=True)
    )
    tabla.attrs["r2_medio_folds"] = float(np.mean(r2_folds))
    tabla.attrs["esquema"] = esquema
    return tabla


def _clonar(modelo):
    from sklearn.base import clone

    return clone(modelo)
