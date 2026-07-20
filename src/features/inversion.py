"""Variables de inversión pública a partir del panel comunal del BIP.

El BIP reporta la ejecución presupuestaria con 2-3 años de rezago, así que la
inversión contemporánea no está disponible para los años más recientes. Eso
no es un obstáculo: la inversión pública no afecta el desempeño turístico el
mismo año en que se ejecuta, sino con retardo. Una obra terminada en 2020
incide sobre la actividad de 2022.

Este módulo construye tres familias de variables:

1. **Flujo rezagado** — `inversion_lag{k}`. La especificación directa del
   efecto retardado.

2. **Flujo acumulado en ventana móvil** — `inversion_ventana{n}`. Suaviza la
   volatilidad interanual de los proyectos grandes, que en comunas pequeñas
   puede ser extrema (un solo proyecto multiplica el flujo del año).

3. **Stock de capital por inventario perpetuo** — `stock_capital`. Sigue
   K_t = (1-δ)·K_{t-1} + I_t, la formulación estándar en economía regional.
   Mide capital público instalado, que es lo que teóricamente sostiene la
   capacidad productiva del clúster.

Para que el stock no arranque artificialmente en cero conviene alimentar la
serie desde varios años antes del período de análisis (el BIP tiene registros
desde 1986) y recortar después.
"""

import numpy as np
import pandas as pd

DEPRECIACION_INFRAESTRUCTURA = 0.05


def construir_variables_inversion(
    panel,
    rezagos=(1, 2),
    ventanas=(3, 5),
    depreciacion=DEPRECIACION_INFRAESTRUCTURA,
    anio_inicio_reporte=None,
    col_valor="inversion_publica",
    col_comuna="comuna",
    col_anio="anio",
):
    """Genera variables de inversión rezagadas, acumuladas y de stock.

    Parameters
    ----------
    panel : DataFrame
        Panel comuna × año completo (rejilla sin huecos). Conviene que empiece
        varios años antes del período de análisis para calentar el stock.
    anio_inicio_reporte : int, optional
        Año desde el cual devolver resultados. Los años previos se usan sólo
        como calentamiento del stock y de las ventanas móviles.

    Returns
    -------
    DataFrame con las variables originales más las derivadas. Las versiones en
    log usan log1p porque hay ceros reales (comunas sin inversión ese año).
    """
    df = panel.sort_values([col_comuna, col_anio]).copy()
    g = df.groupby(col_comuna, sort=False)

    # --- 1. Flujos rezagados -------------------------------------------------
    for k in rezagos:
        df[f"inversion_lag{k}"] = g[col_valor].shift(k)

    # --- 2. Ventanas móviles -------------------------------------------------
    # Se desplaza 1 año para que la ventana sea estrictamente pasada: la
    # inversión del propio año t no debe entrar a explicar el desempeño de t.
    for n in ventanas:
        df[f"inversion_ventana{n}"] = (
            g[col_valor]
            .shift(1)
            .groupby(df[col_comuna], sort=False)
            .rolling(n, min_periods=n)
            .sum()
            .reset_index(level=0, drop=True)
        )

    # --- 3. Stock por inventario perpetuo ------------------------------------
    df["stock_capital"] = _inventario_perpetuo(
        df, depreciacion, col_valor, col_comuna
    )
    # Rezagado en 1: el stock relevante para el desempeño de t es el instalado
    # al cierre de t-1.
    df["stock_capital_lag1"] = g["stock_capital"].shift(1)

    # --- Transformaciones ----------------------------------------------------
    derivadas = (
        [f"inversion_lag{k}" for k in rezagos]
        + [f"inversion_ventana{n}" for n in ventanas]
        + ["stock_capital", "stock_capital_lag1"]
    )
    for col in derivadas:
        df[f"log_{col}"] = np.log1p(df[col].clip(lower=0))

    if anio_inicio_reporte is not None:
        df = df[df[col_anio] >= anio_inicio_reporte]

    return df.reset_index(drop=True)


def _inventario_perpetuo(df, depreciacion, col_valor, col_comuna):
    """K_t = (1-δ)·K_{t-1} + I_t, por comuna.

    Los años sin dato (fuera de la cobertura de la fuente) interrumpen la
    acumulación: se propaga el último stock depreciado en vez de suponer
    inversión cero, que sesgaría el stock a la baja.
    """
    salida = np.full(len(df), np.nan)
    pos = 0
    for _, g in df.groupby(col_comuna, sort=False):
        k = 0.0
        visto = False
        for inv in g[col_valor].to_numpy():
            if np.isnan(inv):
                if visto:
                    k = (1 - depreciacion) * k
                    salida[pos] = k
                # sin ningún dato previo el stock no es estimable: queda NaN
            else:
                k = (1 - depreciacion) * k + float(inv)
                salida[pos] = k
                visto = True
            pos += 1
    return salida


def cobertura_por_variable(df, variables, col_anio="anio"):
    """Años con dato completo por variable. Define la ventana de cada modelo."""
    filas = []
    for v in variables:
        d = df[[col_anio, v]].dropna()
        filas.append(
            {
                "variable": v,
                "n_obs": len(d),
                "anio_min": int(d[col_anio].min()) if len(d) else None,
                "anio_max": int(d[col_anio].max()) if len(d) else None,
            }
        )
    return pd.DataFrame(filas)
