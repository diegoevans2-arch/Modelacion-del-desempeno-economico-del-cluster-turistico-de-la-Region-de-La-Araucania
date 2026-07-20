"""Población comunal — Estimaciones y proyecciones INE, base 2017.

Fuente: INE, "Estimaciones y proyecciones 2002-2035, comunas" (base Censo 2017).
El archivo viene en formato ancho: una fila por comuna × sexo × edad simple, y
una columna por año.

POR QUÉ IMPORTA: sin normalizar por población, cualquier índice construido en
niveles ordena las comunas por tamaño. Temuco tiene ~1.150 empresas del rubro
turístico y Melipeuco ~53; un IDEC en niveles mediría demografía, no
desempeño. La normalización per cápita es lo que convierte al índice en una
medida de intensidad comparable entre comunas.

LIMITACIÓN A DECLARAR: el INE ya publicó proyecciones base Censo 2024, pero
**sólo a nivel país y región** — no hay desagregación comunal para esa base.
Por tanto las cifras comunales de los años recientes son proyecciones
anteriores al Censo 2024 y se desviarán de lo observado. Es la mejor fuente
comunal disponible, pero conviene contrastar el último año contra los
resultados comunales del Censo 2024 cuando se publiquen.
"""

import pandas as pd

from src import config

ARCHIVO = "INE_proyecciones_comunas_2002_2035_base2017.csv"

# Tramo etario laboral, usado como covariable de oferta de trabajo local.
EDAD_LABORAL = (15, 64)


def cargar_crudo(ruta=None):
    ruta = ruta or (config.BBDD_DIR / "INE" / ARCHIVO)
    # El INE publica este CSV en latin-1, no en UTF-8.
    df = pd.read_csv(ruta, encoding="latin-1")
    df.columns = [str(c).strip() for c in df.columns]
    return df


def panel_poblacion(ruta=None, comunas=None, anio_inicio=None, anio_fin=None):
    """Panel comuna × año de población total y en edad laboral.

    Returns
    -------
    DataFrame: comuna, comuna_nombre, anio, poblacion, poblacion_laboral.
    """
    df = cargar_crudo(ruta)
    anio_inicio = anio_inicio or config.ANIO_INICIO
    anio_fin = anio_fin or config.ANIO_FIN

    cols_anio = {
        c: int(c.replace("Poblacion", "").strip())
        for c in df.columns
        if c.startswith("Poblacion")
    }
    cols_validos = [c for c, a in cols_anio.items() if anio_inicio <= a <= anio_fin]

    df = df.rename(columns={"Comuna": "comuna", "Edad": "edad"})
    df = df[df["comuna"].isin(comunas or config.COMUNAS_ARAUCANIA)]

    largo = df.melt(
        id_vars=["comuna", "edad"],
        value_vars=cols_validos,
        var_name="col_anio",
        value_name="personas",
    )
    largo["anio"] = largo["col_anio"].map(cols_anio)

    total = (
        largo.groupby(["comuna", "anio"])["personas"].sum().reset_index(name="poblacion")
    )

    lo, hi = EDAD_LABORAL
    laboral = (
        largo[largo["edad"].between(lo, hi)]
        .groupby(["comuna", "anio"])["personas"]
        .sum()
        .reset_index(name="poblacion_laboral")
    )

    panel = total.merge(laboral, on=["comuna", "anio"], how="left")
    panel["comuna_nombre"] = panel["comuna"].map(config.nombre_comuna)
    panel["destino_sernatur"] = panel["comuna"].map(config.COMUNA_A_DESTINO)

    return panel[
        ["comuna", "comuna_nombre", "destino_sernatur", "anio",
         "poblacion", "poblacion_laboral"]
    ].sort_values(["comuna", "anio"]).reset_index(drop=True)
