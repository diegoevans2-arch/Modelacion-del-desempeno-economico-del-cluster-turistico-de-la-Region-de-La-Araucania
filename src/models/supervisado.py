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
    # Flujo turístico observado (CONAF/SNASPE) — exógeno al IDEC
    "visitas_snaspe_pc",
    # Demografía
    "poblacion",
    "poblacion_laboral",
    # Choques exógenos al rubro turístico (ver src/features/cet.py).
    # Entra al entrenamiento con su serie histórica —no como constante—, para
    # que el modelo aprenda una elasticidad real y la simulación de escenarios
    # tenga efecto. Con la variable constante en 1 su importancia sería 0.
    "cet",
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

    Los dos `n_jobs` están fijados a propósito: NO devolver ninguno a -1.
    Cada pliegue hace `n_predictores × n_repeticiones` llamadas a `predict()`
    (15 × 30 = 450) sobre conjuntos de prueba de decenas de filas, de modo
    que cualquier nivel de joblib cuesta más en arrancar procesos —en Windows
    el arranque es por spawn— que lo que tarda el cálculo. Medido sobre este
    panel con `esquema="bloques"` y `n_repeticiones=30`: ambos en -1, 277 s;
    sólo el bosque en 1, 155 s; los dos como están ahora, 74 s. Volver a -1
    además inunda stderr con `UserWarning` de joblib, miles de líneas por
    corrida.

    Hay una segunda razón, menos visible. Con `n_jobs=-1` el `predict()` del
    bosque suma los 500 árboles bajo un lock, en el orden en que los hilos lo
    van ganando, y la suma de flotantes no es asociativa: los últimos dígitos
    de la tabla cambian de una corrida a otra. Así, el CSV de
    `BBDD/final/resultados_h1_importancia.csv` no es exactamente reproducible
    ni por el código que lo generó. Con `n_jobs=1` la función es reproducible
    bit a bit. El `n_jobs` de `permutation_importance`, en cambio, sí es
    numéricamente neutro —sortea una sola semilla y la reparte a todas las
    tareas—, y está en `None` nada más que por tiempo.
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
        # n_jobs fijado a propósito; leer la nota del docstring antes de tocarlo.
        m = RandomForestRegressor(
            n_estimators=500, min_samples_leaf=3, max_features="sqrt",
            random_state=42, n_jobs=1
        ).fit(X[tr], y[tr])
        r2_folds.append(r2_score(y[te], m.predict(X[te])))
        r = permutation_importance(
            m, X[te], y[te], n_repeats=n_repeticiones, random_state=42,
            n_jobs=None
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


def entrenar(df, predictores=None, objetivo=OBJETIVO, modelo=None):
    """Entrena el modelo final sobre todo el panel, para simulación.

    Devuelve `(modelo_ajustado, predictores)`. A diferencia de `evaluar()`,
    que estima el desempeño fuera de muestra, aquí se usa toda la información
    disponible porque el objetivo es proyectar escenarios, no medir error.
    """
    predictores = predictores or PREDICTORES
    verificar_circularidad(predictores, objetivo)

    d = df.dropna(subset=predictores + [objetivo])
    X = d[predictores].to_numpy(dtype=float)
    y = d[objetivo].to_numpy(dtype=float)

    modelo = modelo or RandomForestRegressor(
        n_estimators=500, min_samples_leaf=3, max_features="sqrt",
        random_state=42, n_jobs=-1
    )
    return modelo.fit(X, y), predictores


def simular_cet(df, cet=None, modelo=None, predictores=None, objetivo=OBJETIVO,
                comunas=None, anio=None, modo="estructural",
                elasticidad=None, ponderar_exposicion=False):
    """Proyecta el IDEC bajo un escenario de Choques Exógenos Territoriales.

    Parameters
    ----------
    cet : None | float | dict | DataFrame
        Escenario a simular. **Si es None se usa el valor neutro 1,0**
        (condiciones normales, sin choque). Ver `features.cet.aplicar_escenario`.
    modo : {"estructural", "aprendido"}
        - "estructural" (por defecto): el modelo proyecta el IDEC y el choque
          se aplica como atenuación con elasticidad declarada. Dirección
          garantizada y parámetro auditable. **Modo recomendado.**
        - "aprendido": la CET entra como predictor y el bosque infiere su
          efecto. Con el IDEC vigente esta elasticidad está mal identificada
          (ver `features.cet.atenuar`); se conserva para el análisis de
          sensibilidad y para cuando D1 esté disponible.
    elasticidad : float, optional
        λ ∈ [0,1] del modo estructural. Por defecto `cet.ELASTICIDAD_DEFAULT`.
    ponderar_exposicion : bool
        Si True, pondera λ por la intensidad turística de cada comuna
        (choques específicos del rubro). Si False —por defecto— el choque
        afecta por igual a todo el territorio.

    Returns
    -------
    DataFrame: comuna, comuna_nombre, anio, cet, IDEC_observado,
    IDEC_base (CET=1), IDEC_escenario, delta, delta_pct.
    """
    from src.features import cet as mcet

    if modo not in ("estructural", "aprendido"):
        raise ValueError(f"modo no reconocido: {modo!r}")

    predictores = predictores or PREDICTORES
    if modelo is None:
        modelo, predictores = entrenar(df, predictores, objetivo)

    d = df.dropna(subset=[c for c in predictores if c != "cet"] + [objetivo]).copy()
    if comunas is not None:
        d = d[d["comuna"].isin(comunas)]
    if anio is not None:
        d = d[d["anio"] == anio]
    if d.empty:
        raise ValueError("El filtro comunas/anio no dejó observaciones que proyectar")

    base = mcet.aplicar_escenario(d, mcet.CET_NEUTRO)
    esc = mcet.aplicar_escenario(d, cet)

    pred_base = modelo.predict(base[predictores].to_numpy(dtype=float))

    if modo == "aprendido":
        pred_esc = modelo.predict(esc[predictores].to_numpy(dtype=float))
    else:
        exposicion = (
            d["alojamientos_por_mil_hab"].to_numpy()
            if ponderar_exposicion and "alojamientos_por_mil_hab" in d.columns
            else None
        )
        pred_esc = mcet.atenuar(
            pred_base,
            esc["cet"].to_numpy(),
            elasticidad=(mcet.ELASTICIDAD_DEFAULT if elasticidad is None
                         else elasticidad),
            exposicion=exposicion,
        )

    out = pd.DataFrame(
        {
            "comuna": d["comuna"].to_numpy(),
            "comuna_nombre": d.get("comuna_nombre", pd.Series(index=d.index)).to_numpy(),
            "anio": d["anio"].to_numpy(),
            "cet": esc["cet"].to_numpy(),
            "IDEC_observado": d[objetivo].to_numpy(),
            "IDEC_base": pred_base,
            "IDEC_escenario": pred_esc,
        }
    )
    out["delta"] = out["IDEC_escenario"] - out["IDEC_base"]
    out["delta_pct"] = np.where(
        out["IDEC_base"] > 0, 100 * out["delta"] / out["IDEC_base"], np.nan
    )
    out.attrs["modo"] = modo
    return out


def curva_respuesta_cet(df, valores=None, modelo=None, predictores=None,
                        objetivo=OBJETIVO, **kwargs):
    """Respuesta media del IDEC ante distintos niveles de CET.

    Es la verificación de que la variable **efectivamente opera**: si el IDEC
    proyectado no varía al mover la CET, la variable entró como constante y el
    modelo la está ignorando (ver advertencia en `features/cet.py`).
    """
    valores = valores if valores is not None else [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.3, 0.0]
    filas = []
    for v in valores:
        r = simular_cet(df, cet=v, modelo=modelo, predictores=predictores,
                        objetivo=objetivo, **kwargs)
        filas.append(
            {
                "cet": v,
                "IDEC_medio": round(r["IDEC_escenario"].mean(), 4),
                "delta_medio": round(r["delta"].mean(), 4),
                "delta_pct_medio": round(r["delta_pct"].mean(), 2),
            }
        )
    t = pd.DataFrame(filas)
    if t["delta_medio"].abs().max() < 1e-9:
        t.attrs["alerta"] = (
            "La CET no produce ningún efecto: entró al entrenamiento como "
            "constante y el modelo la ignora."
        )
    return t


def _clonar(modelo):
    from sklearn.base import clone

    return clone(modelo)
