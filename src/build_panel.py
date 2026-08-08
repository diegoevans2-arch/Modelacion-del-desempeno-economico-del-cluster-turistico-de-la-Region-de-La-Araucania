"""Ensambla el panel comunal Nivel A (datos observados, sin desagregación).

Ejecutar desde la raíz del repo:

    python -m src.build_panel

Integra SII (actividad económica del rubro turístico), BIP (inversión pública
con rezago y stock), SERNATUR (capacidad de alojamiento) e INE (población), y
deriva las versiones normalizadas per cápita.

La normalización no es cosmética: en niveles, Temuco tiene ~49 veces la
población de Melipeuco, de modo que cualquier índice sin normalizar ordena las
comunas por tamaño demográfico en vez de por intensidad de desempeño.
"""

import pandas as pd

from src import config
from src.data import bip, poblacion, sernatur, sii
from src.features import cet as fcet
from src.features import diagnostics as dg
from src.features import inversion as finv

ANIO_INICIO = 2013
ANIO_FIN = 2024
ANIO_CALENTAMIENTO_STOCK = 2000


def construir(comunas=None, anio_inicio=ANIO_INICIO, anio_fin=ANIO_FIN):
    comunas = comunas or config.CLUSTER_EXTENDIDO

    # --- Fuentes -------------------------------------------------------------
    act = sii.panel_turismo(comunas=comunas, anio_inicio=anio_inicio, anio_fin=anio_fin)

    bip_raw = bip.cargar_bip_araucania()
    bip_base = bip.panel_inversion_comunal(
        bip_raw, comunas=comunas,
        anio_inicio=ANIO_CALENTAMIENTO_STOCK, anio_fin=anio_fin,
    )
    inv = finv.construir_variables_inversion(bip_base, anio_inicio_reporte=anio_inicio)

    cap = sernatur.capacidad_comunal(comunas=comunas)
    pob = poblacion.panel_poblacion(
        comunas=comunas, anio_inicio=anio_inicio, anio_fin=anio_fin
    )
    conexos = sii.panel_sectores_conexos(
        comunas=comunas, anio_inicio=anio_inicio, anio_fin=anio_fin
    )

    # --- Integración ---------------------------------------------------------
    cols_inv = [
        "comuna", "anio", "inversion_lag2", "inversion_ventana3",
        "stock_capital_lag1",
    ]
    panel = (
        act.merge(inv[cols_inv], on=["comuna", "anio"], how="left")
        .merge(pob[["comuna", "anio", "poblacion", "poblacion_laboral"]],
               on=["comuna", "anio"], how="left")
        .merge(cap[["comuna", "n_alojamientos", "n_clases", "share_regional"]],
               on="comuna", how="left")
        .merge(conexos, on=["comuna", "anio"], how="left")
    )

    # --- Normalización -------------------------------------------------------
    per_capita = {
        "ventas_uf": "ventas_pc",
        "renta_uf": "renta_pc",
        "n_trabajadores": "trabajadores_pc",
        "n_empresas": "empresas_pc",
        "inversion_lag2": "inversion_pc_lag2",
        "stock_capital_lag1": "stock_capital_pc_lag1",
        "n_alojamientos": "alojamientos_pc",
    }
    for origen, destino in per_capita.items():
        panel[destino] = panel[origen] / panel["poblacion"]

    # Intensidad turística: alojamientos formales por cada 1.000 habitantes.
    # Es el indicador que separa una comuna turística de una que simplemente
    # tiene muchos restaurantes por tener mucha población.
    panel["alojamientos_por_mil_hab"] = 1000 * panel["alojamientos_pc"]
    panel["ventas_por_empresa"] = panel["ventas_uf"] / panel["n_empresas"]
    panel["trabajadores_por_empresa"] = panel["n_trabajadores"] / panel["n_empresas"]

    # Sectores conexos, también per cápita para que sean comparables entre
    # comunas de tamaño muy distinto.
    for col in [c for c in panel.columns if c.startswith(("ventas_uf_", "n_trabajadores_"))]:
        panel[f"{col}_pc"] = panel[col] / panel["poblacion"]

    # Choques exógenos territoriales: serie histórica documentada. El usuario
    # puede sobrescribirla para simular escenarios (features/cet.py).
    panel = fcet.agregar_cet(panel)

    return panel.sort_values(["comuna", "anio"]).reset_index(drop=True)


def main():
    panel = construir()
    salida = config.FINAL_DIR / "panel_nivelA_comunal.csv"
    panel.to_csv(salida, index=False, encoding="utf-8")

    print(f"Panel Nivel A -> {salida}")
    print(f"  {panel.shape[0]} observaciones | {panel.comuna.nunique()} comunas "
          f"| {int(panel.anio.min())}-{int(panel.anio.max())}")

    clave = ["ventas_pc", "trabajadores_pc", "renta_pc",
             "inversion_pc_lag2", "stock_capital_pc_lag1"]
    completas = panel[clave].notna().all(axis=1).sum()
    print(f"  celdas completas en variables clave: {completas}/{len(panel)}")

    print("\nDiagnóstico de degeneración:")
    d = panel.rename(columns={"anio": "periodo"})
    cols = ["variable", "share_comuna", "idiosincrasia_within",
            "domina_escala", "veredicto"]
    print(dg.tabla_diagnostico(d, clave)[cols].to_string(index=False))
    return panel


if __name__ == "__main__":
    main()
