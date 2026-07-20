"""Estadísticas de empresas por comuna y rubro económico (SII).

Fuente: https://www.sii.cl/sobre_el_sii/empresas/PUB_COMU_RUBR.xlsb
Cobertura: años comerciales 2005–2024.

Es la única fuente del proyecto con actividad económica del sector turístico
observada a nivel comuna × año. De ella dependen D2 (empleo sectorial) y D3
(generación de ingresos) del IDEC, y los pesos de desagregación de EMAT.

LIMITACIONES DE LA FUENTE (declaradas por el SII, deben ir en Capítulo III):

1. Reserva tributaria (Art. 35 Código Tributario): las celdas construidas con
   <=10 informantes se publican como '*'. Son FALTANTES ESTRUCTURALES, no
   ceros. Tratarlas como cero subestima sistemáticamente a las comunas
   pequeñas, que es justo donde la tesis necesita precisión.

2. La georreferencia es el domicilio / casa matriz ante el SII, no el
   establecimiento. Una cadena con casa matriz en Santiago y hotel en Pucón se
   contabiliza en Santiago. Sesgo a la baja en comunas turísticas pequeñas con
   operadores externos.

3. El rubro económico de los años 2015–2017 replica el declarado en 2014; los
   cambios de rubro en esa ventana no son observables.
"""

import numpy as np
import pandas as pd

from src import config

FILA_ENCABEZADO = 4

COLUMNAS = {
    "Año Comercial": "anio",
    "Comuna del domicilio o casa matriz": "comuna_nombre_sii",
    "Provincia del domicilio o casa matriz": "provincia",
    "Región del domicilio o casa matriz": "region",
    "Rubro económico": "rubro",
    "Número de empresas": "n_empresas",
    "Número de trabajadores dependientes informados": "n_trabajadores",
    "Ventas anuales en UF": "ventas_uf",
    "Renta neta informada en UF": "renta_uf",
}

# Rubro CIIU del sector turístico. Los otros dos se usan como covariables del
# clúster (comercio y actividades recreativas acompañan a la actividad
# turística en el sentido de Porter).
RUBRO_TURISMO = "I"
RUBROS_CLUSTER = ["I", "G", "R"]

CACHE = config.PROCESSED_DIR / "sii_araucania_rubros.csv"


def _norm(s):
    import unicodedata

    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.upper().strip()


def cargar_crudo(ruta=None):
    """Lee la hoja Datos completa. Lento (~1,4M filas en formato binario)."""
    ruta = ruta or (config.SII_DIR / "PUB_COMU_RUBR.xlsb")
    df = pd.read_excel(ruta, sheet_name="Datos", engine="pyxlsb",
                       header=FILA_ENCABEZADO)
    df.columns = [str(c).strip() for c in df.columns]
    faltantes = set(COLUMNAS) - set(df.columns)
    if faltantes:
        raise ValueError(f"Columnas ausentes en la fuente: {faltantes}")
    return df.rename(columns=COLUMNAS)[list(COLUMNAS.values())]


def cargar_araucania(ruta=None, usar_cache=True):
    """Extrae La Araucanía, mapea comunas a código INE y marca enmascarados.

    Las celdas '*' quedan como NaN, con una columna `enmascarado_<var>` que
    permite distinguirlas de un faltante ordinario.
    """
    if usar_cache and CACHE.exists():
        return pd.read_csv(CACHE, encoding="utf-8")

    df = cargar_crudo(ruta)
    df = df[df["region"].astype(str).str.contains("rauca", case=False, na=False)].copy()

    mapa = {_norm(v): k for k, v in config.COMUNAS_ARAUCANIA.items()}
    df["comuna"] = df["comuna_nombre_sii"].map(lambda s: mapa.get(_norm(s)))

    # El SII incluye filas agregadas ("Sin Información") que no son comunas.
    df = df.dropna(subset=["comuna"]).copy()
    df["comuna"] = df["comuna"].astype(int)

    df["rubro_letra"] = df["rubro"].astype(str).str.strip().str[0]
    df["anio"] = pd.to_numeric(df["anio"], errors="coerce").astype("Int64")

    for var in ["n_empresas", "n_trabajadores", "ventas_uf", "renta_uf"]:
        crudo = df[var].astype(str).str.strip()
        df[f"enmascarado_{var}"] = crudo.eq("*")
        df[var] = pd.to_numeric(crudo.replace("*", np.nan), errors="coerce")

    df["comuna_nombre"] = df["comuna"].map(config.nombre_comuna)
    df["destino_sernatur"] = df["comuna"].map(config.COMUNA_A_DESTINO)

    df = df.drop(columns=["comuna_nombre_sii", "region"])
    df.to_csv(CACHE, index=False, encoding="utf-8")
    return df


def panel_turismo(df=None, comunas=None, rubro=RUBRO_TURISMO,
                  anio_inicio=None, anio_fin=None):
    """Panel comuna × año del rubro turístico.

    Returns
    -------
    DataFrame: comuna, comuna_nombre, destino_sernatur, anio, n_empresas,
    n_trabajadores, ventas_uf, renta_uf, y los indicadores de enmascaramiento.
    """
    df = cargar_araucania() if df is None else df
    anio_inicio = anio_inicio or config.ANIO_INICIO
    anio_fin = anio_fin or config.ANIO_FIN

    p = df[df["rubro_letra"] == rubro].copy()
    p = p[(p["anio"] >= anio_inicio) & (p["anio"] <= anio_fin)]
    if comunas is not None:
        p = p[p["comuna"].isin(comunas)]

    cols = [
        "comuna", "comuna_nombre", "destino_sernatur", "anio",
        "n_empresas", "n_trabajadores", "ventas_uf", "renta_uf",
        "enmascarado_ventas_uf", "enmascarado_renta_uf",
    ]
    return p[cols].sort_values(["comuna", "anio"]).reset_index(drop=True)


# Sectores conexos al clúster turístico. En el sentido de Porter, un clúster
# es la concentración geográfica de industrias relacionadas y de apoyo: estas
# acompañan a la actividad turística sin formar parte del IDEC, de modo que
# son predictores legítimos y no introducen circularidad.
SECTORES_CONEXOS = {
    "G": "comercio",
    "H": "transporte",
    "R": "recreativas",
    "L": "inmobiliarias",
    "F": "construccion",
}


def panel_sectores_conexos(df=None, comunas=None, sectores=None,
                           anio_inicio=None, anio_fin=None):
    """Panel comuna × año con ventas y trabajadores de los sectores conexos.

    Devuelve formato ancho: ventas_uf_<sector>, n_trabajadores_<sector>.
    """
    df = cargar_araucania() if df is None else df
    sectores = sectores or SECTORES_CONEXOS
    anio_inicio = anio_inicio or config.ANIO_INICIO
    anio_fin = anio_fin or config.ANIO_FIN

    p = df[df["rubro_letra"].isin(sectores)].copy()
    p = p[(p["anio"] >= anio_inicio) & (p["anio"] <= anio_fin)]
    if comunas is not None:
        p = p[p["comuna"].isin(comunas)]

    p["sector"] = p["rubro_letra"].map(sectores)
    ancho = p.pivot_table(
        index=["comuna", "anio"],
        columns="sector",
        values=["ventas_uf", "n_trabajadores"],
        aggfunc="sum",
    )
    ancho.columns = [f"{val}_{sec}" for val, sec in ancho.columns]
    return ancho.reset_index()


def reporte_enmascaramiento(panel):
    """Tasa de enmascaramiento por comuna. Insumo de la sección de limitaciones."""
    filas = []
    for comuna, g in panel.groupby("comuna"):
        filas.append(
            {
                "comuna": comuna,
                "comuna_nombre": g["comuna_nombre"].iloc[0],
                "n_anios": len(g),
                "ventas_enmascaradas": int(g["enmascarado_ventas_uf"].sum()),
                "pct_ventas_enmascaradas": round(
                    100 * g["enmascarado_ventas_uf"].mean(), 1
                ),
                "empresas_promedio": round(g["n_empresas"].mean(), 1),
            }
        )
    return pd.DataFrame(filas).sort_values("pct_ventas_enmascaradas", ascending=False)
