"""Diagnósticos de validez del panel comunal.

El riesgo central de desagregar una serie regional a comunas es producir un
panel degenerado: si x_it = X_t * w_i con peso w fijo, la matriz resultante es
de rango 1 y no contiene información comunal nueva. En ese caso el clustering
sólo recupera el ranking de w, y el índice de Theil queda constante.

Este módulo cuantifica esa degeneración antes de que la variable entre a
cualquier modelo.
"""

import numpy as np
import pandas as pd


def descomposicion_varianza(df, var, id_comuna="comuna", id_tiempo="periodo",
                            en_logs=True):
    """Descompone la varianza de un panel en efecto comuna, tiempo e interacción.

    Modelo de dos vías: x_it = mu + alpha_i + gamma_t + e_it

    La interacción es la única fuente de variación que un panel regional
    replicado NO puede generar. Es la métrica que decide si la variable aporta
    información comunal genuina.

    Parameters
    ----------
    en_logs : bool
        Una desagregación multiplicativa (x_it = X_t * w_i) tiene interacción
        exactamente cero **en logaritmos**. Ejecutar en logs es la prueba
        estricta; en niveles la degeneración puede quedar enmascarada.

    Returns
    -------
    dict con las participaciones (suman 1.0) y el veredicto.
    """
    d = df[[id_comuna, id_tiempo, var]].dropna().copy()
    if d.empty:
        return {"variable": var, "error": "sin observaciones"}

    x = d[var].astype(float)
    if en_logs:
        if (x <= 0).any():
            # desplazamiento mínimo para admitir ceros estructurales
            x = x - x.min() + 1e-6
        x = np.log(x)
    d["_x"] = x

    gran_mean = d["_x"].mean()
    media_comuna = d.groupby(id_comuna)["_x"].transform("mean")
    media_tiempo = d.groupby(id_tiempo)["_x"].transform("mean")

    ss_total = ((d["_x"] - gran_mean) ** 2).sum()
    if ss_total == 0:
        return {"variable": var, "error": "varianza nula (constante)"}

    ss_comuna = ((media_comuna - gran_mean) ** 2).sum()
    ss_tiempo = ((media_tiempo - gran_mean) ** 2).sum()
    resid = d["_x"] - media_comuna - media_tiempo + gran_mean
    ss_inter = (resid ** 2).sum()

    share_comuna = ss_comuna / ss_total
    share_tiempo = ss_tiempo / ss_total
    share_inter = ss_inter / ss_total

    # `share_interaccion` sobre la varianza TOTAL es engañoso cuando las
    # comunas difieren mucho en escala: Temuco factura ~64 veces más que
    # Melipeuco, así que el efecto comuna absorbe >90% de la varianza y deja
    # la interacción artificialmente pequeña aunque la dinámica temporal sea
    # rica y diferenciada.
    #
    # La métrica correcta condiciona en la comuna: de la variación que ocurre
    # A LO LARGO DEL TIEMPO, ¿qué fracción es propia de cada comuna y no un
    # movimiento regional común? Es invariante a la brecha de escala, y sigue
    # valiendo exactamente 0 en una desagregación de rango 1.
    denom = ss_inter + ss_tiempo
    idiosincrasia = (ss_inter / denom) if denom > 0 else 0.0

    if idiosincrasia < 0.02:
        veredicto = "DEGENERADA — replica la serie regional"
    elif idiosincrasia < 0.10:
        veredicto = "DÉBIL — sólo como control"
    else:
        veredicto = "OK"

    return {
        "variable": var,
        "escala": "log" if en_logs else "nivel",
        "n_obs": len(d),
        "n_comunas": d[id_comuna].nunique(),
        "n_periodos": d[id_tiempo].nunique(),
        "share_comuna": round(share_comuna, 4),
        "share_tiempo": round(share_tiempo, 4),
        "share_interaccion": round(share_inter, 4),
        "idiosincrasia_within": round(idiosincrasia, 4),
        "domina_escala": bool(share_comuna > 0.80),
        "veredicto": veredicto,
    }


def tabla_diagnostico(df, variables, **kwargs):
    """Aplica la descomposición a varias variables y devuelve una tabla.

    Esta tabla va como anexo metodológico del Capítulo IV: es la evidencia de
    que el panel comunal no es una réplica del dato regional.
    """
    filas = [descomposicion_varianza(df, v, **kwargs) for v in variables]
    return pd.DataFrame(filas)


def rango_efectivo(df, var, id_comuna="comuna", id_tiempo="periodo", tol=1e-8):
    """Rango numérico de la matriz comuna x tiempo.

    Rango 1 == la variable es exactamente el producto de un perfil comunal por
    una serie temporal. Es la comprobación más directa de degeneración.
    """
    m = df.pivot_table(index=id_comuna, columns=id_tiempo, values=var)
    m = m.dropna(axis=0, how="any").dropna(axis=1, how="any")
    if m.empty:
        return {"variable": var, "error": "panel no balanceado"}

    vals = np.linalg.svd(m.values, compute_uv=False)
    rango = int((vals > tol * vals[0]).sum())
    # proporción de la energía capturada por el primer componente
    energia_pc1 = float(vals[0] ** 2 / (vals ** 2).sum())

    return {
        "variable": var,
        "dim": m.shape,
        "rango_numerico": rango,
        "energia_componente_1": round(energia_pc1, 4),
        "alerta": "rango 1: panel degenerado" if rango == 1 else "",
    }


def theil(valores):
    """Índice de Theil sobre un vector de valores comunales.

    T = (1/N) * sum( (x_i / x_bar) * ln(x_i / x_bar) )

    Se reporta junto con la descomposición: si T es constante en el tiempo, la
    desagregación usó pesos fijos y la hipótesis H3 no es contrastable.
    """
    x = np.asarray(valores, dtype=float)
    x = x[~np.isnan(x)]
    x = x[x > 0]
    if len(x) < 2:
        return np.nan
    r = x / x.mean()
    return float(np.mean(r * np.log(r)))
