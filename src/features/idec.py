"""Construcción del IDEC — Índice de Desempeño Económico del Clúster.

Indicador compuesto que agrega indicadores normalizados en dimensiones, y las
dimensiones en un índice único:

    Z_kjit = normalización de X_kjit
    D_kit  = (1/m_k) · Σ_j Z_kjit
    IDEC_it = Σ_k w_k · D_kit          (w iguales por defecto)

DECISIONES METODOLÓGICAS QUE HAY QUE DEFENDER

1. **Pool de normalización.** Por defecto se normaliza sobre TODO el panel
   (todas las comunas y años juntos). La alternativa —normalizar dentro de
   cada año— parece inocua pero destruye la señal temporal: si cada año se
   reescala a [0,1], todos los años tienen la misma distribución por
   construcción, el IDEC agregado no puede tener tendencia y el índice de
   Theil queda casi constante. Es la misma degeneración que produce una
   desagregación con pesos fijos. Usar `pool="anio"` sólo para análisis de
   posición relativa, nunca para contrastar evolución temporal.

2. **Transformación previa.** Las variables económicas comunales están muy
   sesgadas a la derecha (Pucón factura ~48 veces más por habitante que
   Vilcún). Un Min-Max sobre valores crudos manda al líder a 1,0 y comprime
   al resto cerca de 0, de modo que el índice se vuelve un detector de
   outliers. Por eso el método por defecto es `minmax_log`.

3. **Dimensiones estáticas.** Un indicador sin variación temporal (por
   ejemplo, el conteo de alojamientos de SERNATUR, que es un corte
   transversal) amortigua la señal temporal del IDEC en proporción a su peso.
   `reporte_dimensiones()` lo hace explícito.
"""

import numpy as np
import pandas as pd

from src.features.diagnostics import theil

# Dimensiones construibles con dato comunal observado (sin desagregación).
# D1 (actividad turística) requiere EMAT comunal y se añade cuando exista.
DIMENSIONES_OBSERVADAS = {
    "D2_empleo": ["trabajadores_pc"],
    "D3_ingresos": ["ventas_pc", "renta_pc"],
    "D4_capacidad": ["alojamientos_por_mil_hab", "empresas_pc"],
}

METODOS = ("minmax_log", "minmax", "zscore", "rank")


def normalizar(serie, metodo="minmax_log"):
    """Lleva una serie a [0,1]. Todos los métodos devuelven escala acotada
    para que las dimensiones sean agregables entre sí."""
    x = pd.Series(serie, dtype="float64")

    if metodo == "minmax_log":
        x = np.log1p(x.clip(lower=0))
        metodo_final = "minmax"
    elif metodo == "zscore":
        sd = x.std(ddof=0)
        z = (x - x.mean()) / sd if sd > 0 else x * 0.0
        # Reescalado a [0,1]: el z-score no está acotado y no es agregable tal cual.
        rango = z.max() - z.min()
        return (z - z.min()) / rango if rango > 0 else pd.Series(0.5, index=x.index)
    elif metodo == "rank":
        return x.rank(pct=True)
    else:
        metodo_final = metodo

    if metodo_final == "minmax":
        rango = x.max() - x.min()
        return (x - x.min()) / rango if rango > 0 else pd.Series(0.5, index=x.index)

    raise ValueError(f"método no reconocido: {metodo!r}")


def construir_idec(panel, dimensiones=None, metodo="minmax_log", pesos=None,
                   pool="panel", col_anio="anio"):
    """Calcula el IDEC y sus dimensiones.

    Parameters
    ----------
    pool : {"panel", "anio"}
        "panel" normaliza sobre todas las observaciones (recomendado).
        "anio" normaliza dentro de cada año — ver advertencia del módulo.
    pesos : dict, optional
        Peso por dimensión. Por defecto, iguales.

    Returns
    -------
    DataFrame con las columnas originales más z_<indicador>, las dimensiones
    y la columna IDEC.
    """
    dimensiones = dimensiones or DIMENSIONES_OBSERVADAS
    df = panel.copy()

    indicadores = [v for vs in dimensiones.values() for v in vs]
    faltantes = [v for v in indicadores if v not in df.columns]
    if faltantes:
        raise ValueError(f"Indicadores ausentes en el panel: {faltantes}")

    for var in indicadores:
        if pool == "panel":
            df[f"z_{var}"] = normalizar(df[var], metodo)
        elif pool == "anio":
            df[f"z_{var}"] = df.groupby(col_anio)[var].transform(
                lambda s: normalizar(s, metodo)
            )
        else:
            raise ValueError(f"pool no reconocido: {pool!r}")

    for dim, vs in dimensiones.items():
        df[dim] = df[[f"z_{v}" for v in vs]].mean(axis=1)

    nombres = list(dimensiones)
    if pesos is None:
        pesos = {d: 1.0 / len(nombres) for d in nombres}
    total = sum(pesos[d] for d in nombres)

    df["IDEC"] = sum(df[d] * pesos[d] for d in nombres) / total
    return df


def reporte_dimensiones(idec_df, dimensiones=None, col_comuna="comuna",
                        col_anio="anio"):
    """Cuánta variación temporal aporta cada dimensión.

    Una dimensión construida sobre indicadores estáticos tiene variación
    temporal nula y sólo diluye la señal del índice.
    """
    dimensiones = dimensiones or DIMENSIONES_OBSERVADAS
    filas = []
    for dim in list(dimensiones) + ["IDEC"]:
        if dim not in idec_df.columns:
            continue
        g = idec_df.groupby(col_comuna)[dim]
        var_within = g.transform(lambda s: s - s.mean()).var(ddof=0)
        filas.append(
            {
                "dimension": dim,
                "media": round(idec_df[dim].mean(), 4),
                "desv": round(idec_df[dim].std(ddof=0), 4),
                "var_temporal_within": round(var_within, 6),
                "estatica": bool(var_within < 1e-10),
            }
        )
    return pd.DataFrame(filas)


def sensibilidad(panel, dimensiones=None, metodos=METODOS, col_comuna="comuna",
                 col_anio="anio"):
    """Compara el IDEC bajo distintos métodos de normalización.

    El protocolo exige análisis de sensibilidad. La métrica relevante es la
    correlación de Spearman entre ordenamientos: si las conclusiones sobre
    qué comunas rinden mejor cambian según el método, el índice no es robusto.
    """
    dimensiones = dimensiones or DIMENSIONES_OBSERVADAS
    series = {}
    for m in metodos:
        d = construir_idec(panel, dimensiones=dimensiones, metodo=m)
        series[m] = d.set_index([col_comuna, col_anio])["IDEC"]

    tabla = pd.DataFrame(series)
    return tabla, tabla.corr(method="spearman")


def theil_temporal(idec_df, col_idec="IDEC", col_anio="anio"):
    """Índice de Theil del IDEC por año — desigualdad territorial (H3).

    Si el resultado es constante en el tiempo, la construcción del índice
    introdujo pesos fijos en alguna parte y H3 no es contrastable.
    """
    filas = []
    for anio, g in idec_df.groupby(col_anio):
        filas.append({"anio": int(anio), "theil": theil(g[col_idec]),
                      "n_comunas": g[col_idec].notna().sum()})
    return pd.DataFrame(filas)
