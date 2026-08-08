"""Visitantes a Áreas Silvestres Protegidas del Estado (SNASPE) — CONAF.

Fuente: CONAF, publicada en el Sistema de Información de Estadísticas en
Turismo (SIET) de SERNATUR, Reporte Dinámico SNASPE.
    https://datosturismo.sernatur.cl/siet/reporteDinamicoSNASPE
Cobertura del reporte: 2012–2024, mensual, por unidad SNASPE.
Extracto vigente: 2013–2024 anual, 13 unidades de La Araucanía.

QUÉ APORTA
----------
Es la única fuente del proyecto con **flujo turístico observado a escala
sub-regional** que además es independiente del SII. Por eso cumple los cuatro
criterios que ninguna otra variable satisfacía simultáneamente:

  1. Direccionalidad turística — son conteos de visitantes, no un proxy.
  2. Dinámica temporal turística — capta el choque de 2020 (−53 % regional,
     frente a −57 % de la EMAT: magnitudes casi idénticas).
  3. Independencia del IDEC — correlaciones bajas con D2 (+0,30) y D3 (+0,31),
     de modo que no introduce doble conteo.
  4. Exogeneidad — no deriva de ninguna variable del índice.

PARA QUÉ **NO** SIRVE
---------------------
No es un ponderador válido para desagregar la EMAT y construir la dimensión D1.
Mide visitación a áreas protegidas, que es un fenómeno distinto del turismo de
alojamiento: Villarrica —segunda comuna en oferta hotelera, con 88
establecimientos— **no tiene ninguna unidad SNASPE** y recibiría cero actividad
turística. En sentido inverso, R.N. Malalcahuello (centro de esquí, con
visitantes de día) concentra cerca del 60 % de la visitación regional. Ver
`Documentación/Nota_metodologica_D1_desagregacion.md`.

Se emplea, por tanto, como **variable explicativa exógena** y como base de
calibración empírica de la CET.

LIMITACIONES DE LA FUENTE
-------------------------
1. **Ceros ambiguos.** CONAF advierte que un cero puede significar que la
   unidad no informó, no que no hubo visitas. Afecta de forma persistente a
   R.N. Alto Biobío, R.N. Malleco y R.N. Nalcas. `marcar_ceros_dudosos()` los
   identifica.
2. **Unidades que abarcan varias comunas.** El reparto entre ellas es un
   supuesto declarado (`MAPA_UNIDAD_COMUNA`), no un dato. Por defecto se divide
   en partes iguales.
3. **Cobertura desigual.** Las comunas sin áreas protegidas registran cero
   legítimo: no es un faltante, sino ausencia real de este tipo de atractivo.
"""

import pandas as pd

from src import config

ARCHIVO = "conaf_snaspe_araucania.csv"

# Unidades cuyo cero es persistente y probablemente refleja falta de reporte
# más que ausencia de visitantes.
UNIDADES_SIN_REPORTE = ["MALLECO", "NALCAS", "ALTO_BIO_BIO"]

# Asignación de cada unidad a las comunas del clúster que la contienen o le dan
# acceso principal. SUPUESTO DECLARADO — revisable contra cartografía CONAF.
# Las comunas fuera del clúster analizado (Curarrehue 9104, Purén 9208,
# Collipulli 9202) se omiten deliberadamente: la unidad reparte sólo entre las
# comunas del panel.
MAPA_UNIDAD_COMUNA = {
    "CONGUILLIO":     [9110, 9103, 9203, 9119],   # Melipeuco, Cunco, Curacautín, Vilcún
    "HUERQUEHUE":     [9115],                     # Pucón
    "PN_VILLARRICA":  [9115],                     # Pucón
    "RN_VILLARRICA":  [9115],                     # Pucón
    "MALALCAHUELLO":  [9203, 9205],               # Curacautín, Lonquimay
    "TOLHUACA":       [9203, 9211],               # Curacautín, Victoria
    "NAHUELBUTA":     [9201],                     # Angol
    "CERRO_NIELOL":   [9101],                     # Temuco
    "CHINA_MUERTA":   [9110, 9205],               # Melipeuco, Lonquimay
    "ALTO_BIO_BIO":   [9205],                     # Lonquimay
    "NALCAS":         [9205],                     # Lonquimay
    "MALLECO":        [],                         # Collipulli — fuera del clúster
    "CONTULMO":       [],                         # Purén — fuera del clúster
}


def cargar_snaspe(ruta=None):
    """Serie unidad × año de visitas registradas."""
    ruta = ruta or (config.PROCESSED_DIR / ARCHIVO)
    df = pd.read_csv(ruta, encoding="utf-8")
    df["anio"] = pd.to_numeric(df["anio"], errors="coerce").astype(int)
    df["visitas"] = pd.to_numeric(df["visitas"], errors="coerce")
    return df


def marcar_ceros_dudosos(df=None):
    """Identifica ceros que probablemente sean falta de reporte."""
    df = cargar_snaspe() if df is None else df.copy()
    df["cero_dudoso"] = (df["visitas"] == 0) & df["unidad"].isin(UNIDADES_SIN_REPORTE)
    return df


def panel_visitas_comunal(df=None, comunas=None, mapa=None,
                          anio_inicio=None, anio_fin=None):
    """Panel comuna × año de visitas a áreas protegidas.

    Las unidades que abarcan varias comunas reparten sus visitas en partes
    iguales entre ellas. Las comunas sin unidades registran cero, que en este
    caso es un valor legítimo (ausencia de áreas protegidas), no un faltante.

    Returns
    -------
    DataFrame: comuna, comuna_nombre, anio, visitas_snaspe, n_unidades.
    """
    df = cargar_snaspe() if df is None else df
    mapa = mapa or MAPA_UNIDAD_COMUNA
    comunas = comunas or config.CLUSTER_EXTENDIDO
    anio_inicio = anio_inicio or config.ANIO_INICIO
    anio_fin = anio_fin or config.ANIO_FIN

    filas = []
    for r in df.itertuples(index=False):
        destinos = [c for c in mapa.get(r.unidad, []) if c in comunas]
        if not destinos:
            continue
        cuota = r.visitas / len(destinos)
        for c in destinos:
            filas.append({"comuna": c, "anio": r.anio, "visitas_snaspe": cuota,
                          "unidad": r.unidad})

    if filas:
        agr = (
            pd.DataFrame(filas)
            .groupby(["comuna", "anio"])
            .agg(visitas_snaspe=("visitas_snaspe", "sum"),
                 n_unidades=("unidad", "nunique"))
            .reset_index()
        )
    else:
        agr = pd.DataFrame(columns=["comuna", "anio", "visitas_snaspe", "n_unidades"])

    rejilla = pd.MultiIndex.from_product(
        [comunas, range(anio_inicio, anio_fin + 1)], names=["comuna", "anio"]
    ).to_frame(index=False)

    panel = rejilla.merge(agr, on=["comuna", "anio"], how="left").fillna(
        {"visitas_snaspe": 0.0, "n_unidades": 0}
    )
    panel["comuna_nombre"] = panel["comuna"].map(config.nombre_comuna)
    panel["tiene_snaspe"] = panel["n_unidades"] > 0
    return panel.sort_values(["comuna", "anio"]).reset_index(drop=True)


def serie_regional(df=None):
    """Total regional de visitas por año."""
    df = cargar_snaspe() if df is None else df
    return df.groupby("anio")["visitas"].sum()


def calibrar_cet(df=None, anio_base=2019):
    """Deriva una serie de CET a partir de la visitación observada.

    Índice de normalidad = visitas_t / visitas_base, acotado a [0,1]. Sustituye
    los supuestos declarados de `features/cet.py` por un ancla empírica.

    ADVERTENCIA INTERPRETATIVA: la visitación a áreas protegidas es turismo
    mayoritariamente de día y al aire libre, que se recuperó antes que el
    alojamiento. En 2021 CONAF ya estaba a −5 % de su nivel prepandemia,
    mientras la EMAT seguía a −50 %. Una CET calibrada con CONAF describe la
    normalización de la movilidad recreativa, no la del sector de alojamiento
    que mide el IDEC. Úsese declarando el criterio, o combínese con la EMAT
    regional según qué choque se quiera representar.
    """
    s = serie_regional(df)
    base = s.get(anio_base)
    if not base:
        raise ValueError(f"El año base {anio_base} no está en la serie")
    return (s / base).clip(upper=1.0).round(4)
