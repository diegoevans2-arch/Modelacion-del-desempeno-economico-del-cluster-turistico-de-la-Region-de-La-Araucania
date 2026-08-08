"""Precomputa las predicciones del modelo para la aplicación estática.

La aplicación estática no ejecuta Python: no lo necesita. Los escenarios se
anclan en el IDEC observado y la atenuación por CET es una fórmula cerrada, de
modo que basta con precomputar, para cada par comuna-año, el valor observado y
la estimación del modelo con CET neutro.

Ejecutar desde la raíz del repositorio:
    python -m deploy_static.generar_datos
"""

import json
from pathlib import Path

import pandas as pd

from src import config
from src.features import cet as fcet
from src.models import supervisado as S

DESTINO = Path(__file__).resolve().parent


def main():
    panel = pd.read_csv(config.FINAL_DIR / "panel_idec_comunal.csv")
    modelo, predictores = S.entrenar(panel)

    X = panel[predictores].copy()
    X["cet"] = fcet.CET_NEUTRO
    panel["pred"] = modelo.predict(X[predictores].to_numpy(dtype=float))

    registros = []
    for r in panel.itertuples(index=False):
        registros.append({
            "comuna": r.comuna_nombre,
            "anio": int(r.anio),
            "idec": round(float(r.IDEC), 4),
            "pred": round(float(r.pred), 4),
            "destino": (None if pd.isna(r.destino_sernatur)
                        else str(r.destino_sernatur)),
            "poblacion": int(r.poblacion),
            "alojMil": round(float(r.alojamientos_por_mil_hab), 2),
            "d2": round(float(r.D2_empleo), 4),
            "d3": round(float(r.D3_ingresos), 4),
            "d4": round(float(r.D4_capacidad), 4),
            "visitas": int(r.visitas_snaspe),
        })

    ev = S.evaluar(panel)
    rf = ev[ev["modelo"] == "Random Forest"].set_index("esquema")

    # Sesgo de compresión hacia la media, para declararlo en la interfaz
    resid = panel["pred"] - panel["IDEC"]
    corr_sesgo = float(panel["IDEC"].corr(resid))

    salida = {
        "meta": {
            "titulo": "Simulador IDEC — Clúster Turístico de La Araucanía",
            "nObs": int(len(panel)),
            "anioMin": int(panel["anio"].min()),
            "anioMax": int(panel["anio"].max()),
            "cetNeutro": fcet.CET_NEUTRO,
            "elasticidadDefault": fcet.ELASTICIDAD_DEFAULT,
            "corrSesgo": round(corr_sesgo, 3),
            "metricas": {
                e: {"r2": round(float(rf.loc[e, "R2"]), 3),
                    "mae": round(float(rf.loc[e, "MAE"]), 4)}
                for e in rf.index
            },
        },
        "comunas": sorted(panel["comuna_nombre"].unique().tolist()),
        "anios": sorted(int(a) for a in panel["anio"].unique()),
        "datos": registros,
    }

    ruta = DESTINO / "datos.json"
    ruta.write_text(json.dumps(salida, ensure_ascii=False, separators=(",", ":")),
                    encoding="utf-8")
    print(f"datos.json -> {ruta}  ({ruta.stat().st_size / 1024:.1f} KB)")
    print(f"  registros: {len(registros)}  comunas: {len(salida['comunas'])}")
    print(f"  R2 temporal: {salida['meta']['metricas']['temporal']['r2']}")
    print(f"  correlacion IDEC-residuo: {corr_sesgo:+.3f}")


if __name__ == "__main__":
    main()
