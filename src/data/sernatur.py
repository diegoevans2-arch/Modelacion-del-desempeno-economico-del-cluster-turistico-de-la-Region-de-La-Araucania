"""Capacidad de alojamiento comunal desde el Registro Nacional de Prestadores.

LIMITACIÓN IMPORTANTE: el archivo publicado NO incluye fecha de inscripción.
Es un corte transversal, no una serie. Por lo tanto entrega variación ENTRE
comunas pero no A LO LARGO del tiempo, y no puede usarse por sí solo como peso
de desagregación dinámica (produciría un panel de rango 1 — ver
src/features/diagnostics.py).

Para obtener la dimensión temporal hay dos vías:
  - solicitar a SERNATUR el registro con fecha de inscripción (Ley de
    Transparencia), o
  - recuperar cortes anuales archivados del registro.
"""

import pandas as pd

from src import config

# El CSV trae filas con separadores extra; se omiten (son <0,5% y no
# corresponden a La Araucanía).
_LECTURA = dict(sep=";", encoding="latin-1", engine="python", on_bad_lines="skip")


def cargar_registro(ruta=None):
    """Registro de alojamientos de La Araucanía, normalizado."""
    ruta = ruta or config.SERNATUR_CSV
    df = pd.read_csv(ruta, **_LECTURA)
    df.columns = [c.strip() for c in df.columns]

    df = df[df["Región"].astype(str).str.contains("rauca", case=False, na=False)].copy()
    df["Comuna"] = df["Comuna"].astype(str).str.strip().str.upper()
    df["CLASE"] = df["CLASE"].astype(str).str.strip().str.upper()
    df["Destino"] = df["Destino"].astype(str).str.strip().replace("-", pd.NA)
    return df


def _mapa_nombre_a_codigo():
    """Normaliza nombres del registro (sin tildes, mayúsculas) a código INE."""
    import unicodedata

    def norm(s):
        s = unicodedata.normalize("NFKD", str(s))
        s = "".join(c for c in s if not unicodedata.combining(c))
        return s.upper().strip()

    return {norm(nombre): codigo for codigo, nombre in config.COMUNAS_ARAUCANIA.items()}


def capacidad_comunal(df=None, comunas=None):
    """Corte transversal de capacidad por comuna.

    Returns
    -------
    DataFrame: comuna, comuna_nombre, destino_sernatur, n_alojamientos,
    n_clases, n_hoteles, share_regional.
    """
    df = cargar_registro() if df is None else df
    mapa = _mapa_nombre_a_codigo()
    df = df.copy()
    df["comuna"] = df["Comuna"].map(mapa)

    sin_match = df[df["comuna"].isna()]["Comuna"].unique()
    if len(sin_match):
        raise ValueError(f"Comunas sin código INE: {list(sin_match)}")

    cap = (
        df.groupby("comuna")
        .agg(
            n_alojamientos=("Nombre del Establecimiento", "count"),
            n_clases=("CLASE", "nunique"),
            n_hoteles=("CLASE", lambda s: (s == "HOTEL").sum()),
        )
        .reset_index()
    )

    # Comunas sin oferta registrada: cero real, no faltante.
    universo = comunas if comunas is not None else sorted(config.COMUNAS_ARAUCANIA)
    cap = (
        pd.DataFrame({"comuna": universo})
        .merge(cap, on="comuna", how="left")
        .fillna({"n_alojamientos": 0, "n_clases": 0, "n_hoteles": 0})
    )

    cap["comuna_nombre"] = cap["comuna"].map(config.nombre_comuna)
    cap["destino_sernatur"] = cap["comuna"].map(config.COMUNA_A_DESTINO)
    total = cap["n_alojamientos"].sum()
    cap["share_regional"] = cap["n_alojamientos"] / total if total else 0.0

    return cap[
        ["comuna", "comuna_nombre", "destino_sernatur", "n_alojamientos",
         "n_clases", "n_hoteles", "share_regional"]
    ].sort_values("n_alojamientos", ascending=False).reset_index(drop=True)
