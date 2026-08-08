"""Exporta el modelo entrenado y los datos mínimos para el despliegue.

Genera en `deploy/`:
  - modelo_idec.joblib : Random Forest entrenado sobre el panel completo
  - panel_app.csv      : columnas estrictamente necesarias para la aplicación
  - metadatos.json     : versiones, métricas y límites del modelo

Ejecutar desde la raíz del repositorio:  python -m deploy.exportar_modelo
"""

import json
from pathlib import Path

import joblib
import pandas as pd
import sklearn

from src import config
from src.features import cet as fcet
from src.models import supervisado as S

DESTINO = Path(__file__).resolve().parent

# Columnas que la aplicación necesita además de los predictores
CONTEXTO = [
    "comuna", "comuna_nombre", "destino_sernatur", "anio", "IDEC",
    "D2_empleo", "D3_ingresos", "D4_capacidad",
    "poblacion", "n_alojamientos", "visitas_snaspe", "ventas_uf",
    "n_trabajadores", "alojamientos_por_mil_hab",
]


def main():
    panel = pd.read_csv(config.FINAL_DIR / "panel_idec_comunal.csv")

    modelo, predictores = S.entrenar(panel)

    cols = sorted(set(CONTEXTO) | set(predictores))
    faltantes = [c for c in cols if c not in panel.columns]
    if faltantes:
        raise ValueError(f"Faltan columnas en el panel: {faltantes}")

    app_df = panel[cols].copy()
    app_df.to_csv(DESTINO / "panel_app.csv", index=False, encoding="utf-8")
    joblib.dump({"modelo": modelo, "predictores": predictores},
                DESTINO / "modelo_idec.joblib")

    # Métricas honestas, recalculadas al momento de exportar
    ev = S.evaluar(panel)
    rf = ev[ev["modelo"] == "Random Forest"].set_index("esquema")

    meta = {
        "descripcion": "Modelo predictivo del IDEC — clúster turístico de La Araucanía",
        "objetivo": S.OBJETIVO,
        "predictores": predictores,
        "n_observaciones": int(len(panel)),
        "comunas": sorted(panel["comuna_nombre"].unique().tolist()),
        "anio_min": int(panel["anio"].min()),
        "anio_max": int(panel["anio"].max()),
        "metricas": {
            esquema: {
                "R2": float(rf.loc[esquema, "R2"]),
                "MAE": float(rf.loc[esquema, "MAE"]),
                "RMSE": float(rf.loc[esquema, "RMSE"]),
            }
            for esquema in rf.index
        },
        "cet": {
            "neutro": fcet.CET_NEUTRO,
            "elasticidad_default": fcet.ELASTICIDAD_DEFAULT,
        },
        "versiones": {
            "scikit_learn": sklearn.__version__,
            "pandas": pd.__version__,
        },
        "limitaciones": [
            "El IDEC integra tres dimensiones observadas (empleo, ingresos y "
            "capacidad). No incorpora flujos de visitantes: mide desempeño "
            "económico estructural.",
            "El modelo no generaliza a comunas ausentes del panel "
            f"(R² = {rf.loc['comuna', 'R2']:.2f} en validación por comuna). "
            "Sólo deben consultarse las 13 comunas incluidas.",
            "No es una herramienta de pronóstico: los predictores sólo existen "
            "para 2013–2024. Las proyecciones son simulaciones de escenario "
            "sobre años observados.",
            "La CET opera en modo estructural con elasticidad declarada; no es "
            "una elasticidad estimada de los datos.",
        ],
    }
    (DESTINO / "metadatos.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"modelo    -> {DESTINO / 'modelo_idec.joblib'}")
    print(f"panel     -> {DESTINO / 'panel_app.csv'}  {app_df.shape}")
    print(f"metadatos -> {DESTINO / 'metadatos.json'}")
    print("\nMétricas Random Forest:")
    for esquema in rf.index:
        print(f"  {esquema:10s} R2={rf.loc[esquema,'R2']:+.3f}  "
              f"MAE={rf.loc[esquema,'MAE']:.4f}")


if __name__ == "__main__":
    main()
