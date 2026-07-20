"""Extracción de inversión pública comunal desde el Banco Integrado de Proyectos.

El archivo fuente tiene ~481.000 proyectos nacionales (1,2 GB en CSV). Se lee
por chunks filtrando La Araucanía, de modo que nunca se carga completo en
memoria y no se materializa la copia nacional.

Dos formas de construir el panel anual:

1. Por cohorte (`agregacion="cohorte"`): asigna EBI_GASTO_VIGENTE al año de
   postulación. Simple, pero el gasto de un proyecto plurianual se concentra en
   un solo año.

2. Por ejecución (`agregacion="ejecucion"`): parsea EBI_EJECUCION_PRESUPUESTARIA,
   que contiene el desglose real año a año. Produce flujos anuales efectivos y
   es la opción metodológicamente correcta para un panel.
"""

import re

import pandas as pd

from src import config

COLS_BASE = [
    "REG_CLAVE", "CMN_CLAVE", "SEC_CLAVE",
    "EBI_CODIGO", "EBI_NOMBRE", "EBI_ETAPA_POSTULA",
    "EBI_ANO_POSTULA", "EBI_ULT_ANO_INV",
    "EBI_GASTO_VIGENTE", "EBI_EJECUCION_PRESUPUESTARIA",
]

# "2012: Asignado 396000, Gastado 600 - 2011: Asignado 0, Gastado 0"
_RE_EJECUCION = re.compile(
    r"(\d{4})\s*:\s*Asignado\s*([-\d]+)\s*,\s*Gastado\s*([-\d]+)",
    re.IGNORECASE,
)


def cargar_bip_araucania(ruta=None, chunksize=200_000):
    """Lee el BIP filtrando la Región de La Araucanía."""
    ruta = ruta or config.BIP_CSV
    trozos = []
    for chunk in pd.read_csv(ruta, usecols=COLS_BASE, chunksize=chunksize,
                             low_memory=False):
        trozos.append(chunk[chunk["REG_CLAVE"] == config.BIP_REG_CLAVE_ARAUCANIA])
    df = pd.concat(trozos, ignore_index=True)
    df["CMN_CLAVE"] = pd.to_numeric(df["CMN_CLAVE"], errors="coerce").astype("Int64")
    return df


def parsear_ejecucion_presupuestaria(df):
    """Expande EBI_EJECUCION_PRESUPUESTARIA a filas proyecto-año.

    Devuelve columnas: EBI_CODIGO, CMN_CLAVE, anio, asignado, gastado.
    """
    filas = []
    sub = df[["EBI_CODIGO", "CMN_CLAVE", "EBI_EJECUCION_PRESUPUESTARIA"]].dropna(
        subset=["EBI_EJECUCION_PRESUPUESTARIA"]
    )
    for codigo, comuna, texto in sub.itertuples(index=False):
        for anio, asignado, gastado in _RE_EJECUCION.findall(str(texto)):
            filas.append(
                {
                    "EBI_CODIGO": codigo,
                    "CMN_CLAVE": comuna,
                    "anio": int(anio),
                    "asignado": float(asignado),
                    "gastado": float(gastado),
                }
            )
    return pd.DataFrame(filas)


def anio_corte_cobertura(base, cobertura_minima=0.5):
    """Último año con cobertura completa en la fuente.

    El BIP es un extracto con fecha de corte (vintage): los años más recientes
    aparecen con ejecución presupuestaria parcial o ausente porque todavía no
    se informa. Rellenar esos años con cero introduce una caída ficticia de la
    inversión pública, que un modelo leería como shock real.

    Se marca como truncado el primer año cuyo volumen de registros cae por
    debajo de `cobertura_minima` respecto de la mediana de los años previos.
    """
    conteo = base.groupby("anio").size().sort_index()
    if len(conteo) < 3:
        return int(conteo.index.max())
    for anio in conteo.index[2:]:
        previos = conteo.loc[: anio - 1]
        if conteo.loc[anio] < cobertura_minima * previos.median():
            return int(anio) - 1
    return int(conteo.index.max())


def panel_inversion_comunal(df=None, agregacion="ejecucion",
                            anio_inicio=None, anio_fin=None, comunas=None,
                            truncar_por_cobertura=True):
    """Panel comuna x año de inversión pública.

    Parameters
    ----------
    agregacion : {"ejecucion", "cohorte"}
    comunas : lista de códigos INE. Por defecto, todas las de la región.
    truncar_por_cobertura : bool
        Si True, los años posteriores al corte de cobertura de la fuente quedan
        como NaN (dato ausente) en vez de 0 (ausencia de inversión). Ver
        `anio_corte_cobertura`.

    Returns
    -------
    DataFrame con columnas: comuna, comuna_nombre, anio, inversion_publica,
    n_proyectos.
    """
    df = cargar_bip_araucania() if df is None else df
    anio_inicio = anio_inicio or config.ANIO_INICIO
    anio_fin = anio_fin or config.ANIO_FIN

    if agregacion == "ejecucion":
        ejec = parsear_ejecucion_presupuestaria(df)
        base = ejec.rename(columns={"gastado": "inversion_publica"})
        base = base[["CMN_CLAVE", "anio", "inversion_publica", "EBI_CODIGO"]]
    elif agregacion == "cohorte":
        base = df.rename(
            columns={
                "EBI_ANO_POSTULA": "anio",
                "EBI_GASTO_VIGENTE": "inversion_publica",
            }
        )[["CMN_CLAVE", "anio", "inversion_publica", "EBI_CODIGO"]]
        base = base.dropna(subset=["inversion_publica"])
        base["anio"] = pd.to_numeric(base["anio"], errors="coerce")
    else:
        raise ValueError(f"agregacion no reconocida: {agregacion!r}")

    base = base.dropna(subset=["CMN_CLAVE", "anio"])
    base["anio"] = base["anio"].astype(int)

    # El corte se calcula sobre la serie regional completa, antes de filtrar
    # comunas: así no depende del subconjunto analizado.
    corte = anio_corte_cobertura(base) if truncar_por_cobertura else anio_fin
    anio_fin_efectivo = min(anio_fin, corte)

    base = base[(base["anio"] >= anio_inicio) & (base["anio"] <= anio_fin)]

    if comunas is not None:
        base = base[base["CMN_CLAVE"].isin(comunas)]

    panel = (
        base.groupby(["CMN_CLAVE", "anio"])
        .agg(inversion_publica=("inversion_publica", "sum"),
             n_proyectos=("EBI_CODIGO", "nunique"))
        .reset_index()
        .rename(columns={"CMN_CLAVE": "comuna"})
    )

    # Rejilla completa: las celdas sin proyectos son ceros reales, no faltantes.
    universo = comunas if comunas is not None else sorted(config.COMUNAS_ARAUCANIA)
    rejilla = pd.MultiIndex.from_product(
        [universo, range(anio_inicio, anio_fin + 1)], names=["comuna", "anio"]
    ).to_frame(index=False)

    panel = rejilla.merge(panel, on=["comuna", "anio"], how="left")

    # Dentro de la ventana con cobertura, una celda vacía sí es un cero real:
    # la comuna no ejecutó inversión ese año. Fuera de la ventana es un dato
    # que la fuente aún no informa, y debe quedar como faltante.
    en_cobertura = panel["anio"] <= anio_fin_efectivo
    panel.loc[en_cobertura, ["inversion_publica", "n_proyectos"]] = (
        panel.loc[en_cobertura, ["inversion_publica", "n_proyectos"]].fillna(0.0)
    )
    panel.loc[~en_cobertura, ["inversion_publica", "n_proyectos"]] = pd.NA
    panel["cobertura_fuente"] = en_cobertura

    panel["comuna_nombre"] = panel["comuna"].map(config.nombre_comuna)
    panel["destino_sernatur"] = panel["comuna"].map(config.COMUNA_A_DESTINO)

    return panel[
        ["comuna", "comuna_nombre", "destino_sernatur", "anio",
         "inversion_publica", "n_proyectos", "cobertura_fuente"]
    ].sort_values(["comuna", "anio"]).reset_index(drop=True)
