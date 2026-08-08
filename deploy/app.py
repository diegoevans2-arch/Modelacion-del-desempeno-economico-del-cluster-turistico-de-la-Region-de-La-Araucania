"""Simulador del Índice de Desempeño Económico del Clúster (IDEC).

Aplicación de apoyo a la investigación doctoral sobre el clúster turístico de
la Región de La Araucanía. Permite consultar el IDEC comunal estimado y simular
escenarios de choques exógenos territoriales (CET).

Autocontenida: no depende del repositorio de investigación. Carga el modelo
entrenado, el panel y los metadatos desde archivos locales.
"""

import json
from pathlib import Path

import gradio as gr
import joblib
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent

PAQUETE = joblib.load(BASE / "modelo_idec.joblib")
MODELO = PAQUETE["modelo"]
PREDICTORES = PAQUETE["predictores"]
PANEL = pd.read_csv(BASE / "panel_app.csv")
META = json.loads((BASE / "metadatos.json").read_text(encoding="utf-8"))

# Tipos nativos de Python: los escalares de numpy no son serializables a JSON
# y Gradio falla al construir la configuración de la interfaz.
COMUNAS = sorted(str(c) for c in PANEL["comuna_nombre"].unique())
ANIOS = sorted(int(a) for a in PANEL["anio"].unique())
CET_NEUTRO = 1.0
ELASTICIDAD_DEFAULT = META["cet"]["elasticidad_default"]


# --------------------------------------------------------------------------
# Lógica del choque exógeno
# --------------------------------------------------------------------------
def atenuar(idec, cet, elasticidad):
    """IDEC' = IDEC · [1 − λ·(1 − CET)]

    La dirección del efecto se impone por construcción y λ es un parámetro
    declarado, no estimado. La elasticidad aprendida de los datos históricos
    no está identificada con el IDEC vigente: el índice mide desempeño
    estructural, que resultó resiliente al choque de 2020, mientras el
    colapso se produjo en los flujos de visitantes.
    """
    factor = 1.0 - float(elasticidad) * (1.0 - float(cet))
    return float(idec) * float(np.clip(factor, 0.0, 1.0))


def _fila(comuna_nombre, anio):
    f = PANEL[(PANEL["comuna_nombre"] == comuna_nombre) & (PANEL["anio"] == anio)]
    return f.iloc[0] if len(f) else None


def _predecir(fila, cet=CET_NEUTRO):
    x = fila[PREDICTORES].to_frame().T.copy()
    x["cet"] = cet
    return float(MODELO.predict(x[PREDICTORES].to_numpy(dtype=float))[0])


# --------------------------------------------------------------------------
# Simulador
# --------------------------------------------------------------------------
def simular(comuna_nombre, anio, cet, elasticidad):
    fila = _fila(comuna_nombre, int(anio))
    if fila is None:
        return "### Sin datos para esa combinación de comuna y año.", None

    # La simulación se ancla en el valor OBSERVADO, no en la predicción del
    # modelo. Para los años del panel el IDEC es un dato conocido, y el bosque
    # aleatorio comprime los valores extremos hacia la media (correlación entre
    # IDEC y residuo: −0,79), de modo que subestima a las comunas de mayor
    # desempeño. Anclar en lo observado evita arrastrar ese sesgo al escenario.
    observado = float(fila["IDEC"])
    estimado = _predecir(fila, CET_NEUTRO)
    escenario = atenuar(observado, cet, elasticidad)
    delta = escenario - observado
    delta_pct = 100 * delta / observado if observado else float("nan")
    intensidad = round(100 * (1 - cet))
    brecha_pct = 100 * (estimado - observado) / observado if observado else float("nan")

    if cet >= 0.999:
        cabecera = "**Escenario sin choque** — condiciones normales (CET = 1,00)"
    else:
        cabecera = (f"**Escenario con choque de intensidad {intensidad} %** "
                    f"(CET = {cet:.2f})")

    md = f"""
### {comuna_nombre} — {int(anio)}

{cabecera}

| | IDEC |
|---|---|
| Observado | **{observado:.3f}** |
| Bajo el escenario | **{escenario:.3f}** |
| Variación | {delta:+.3f} ({delta_pct:+.1f} %) |

*Elasticidad aplicada: λ = {elasticidad:.2f}. Un choque que reduce la normalidad
territorial en {intensidad} % se traduce en una caída de {abs(delta_pct):.1f} %
del desempeño.*

---

**Contraste con el modelo.** Para este caso el Random Forest estima un IDEC de
{estimado:.3f}, un {brecha_pct:+.1f} % respecto del valor observado. El modelo
tiende a comprimir los valores extremos hacia la media, por lo que subestima a
las comunas de mayor desempeño y sobreestima a las de menor. Por esa razón la
simulación se ancla en el dato observado y no en la predicción.
"""

    valores = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]
    curva = pd.DataFrame({
        "CET": valores,
        "IDEC": [atenuar(observado, v, elasticidad) for v in valores],
    })
    return md, curva


# --------------------------------------------------------------------------
# Explorador
# --------------------------------------------------------------------------
def serie_comuna(comuna_nombre):
    d = PANEL[PANEL["comuna_nombre"] == comuna_nombre].sort_values("anio")
    return d[["anio", "IDEC"]].rename(columns={"anio": "Año"})


def ranking(anio):
    d = PANEL[PANEL["anio"] == int(anio)].copy()
    d = d.sort_values("IDEC", ascending=False)
    salida = d[["comuna_nombre", "IDEC", "destino_sernatur",
                "alojamientos_por_mil_hab", "poblacion"]].copy()
    salida.columns = ["Comuna", "IDEC", "Destino SERNATUR",
                      "Alojamientos/1.000 hab.", "Población"]
    salida["IDEC"] = salida["IDEC"].round(3)
    salida["Alojamientos/1.000 hab."] = salida["Alojamientos/1.000 hab."].round(2)
    salida["Destino SERNATUR"] = salida["Destino SERNATUR"].fillna("—")
    salida["Población"] = salida["Población"].astype(int)
    grafico = d[["comuna_nombre", "IDEC"]].rename(columns={"comuna_nombre": "Comuna"})
    return salida, grafico


# --------------------------------------------------------------------------
# Interfaz
# --------------------------------------------------------------------------
AVISO = """
> ⚠️ **Herramienta de investigación, no de pronóstico.** El IDEC mide desempeño
> económico *estructural* (empleo, ingresos y capacidad instalada); no incorpora
> flujos de visitantes. Los resultados son simulaciones sobre años observados
> (2013–2024) para las 13 comunas del estudio, y **no deben extrapolarse a otros
> territorios ni a años futuros**. Ver la pestaña *Metodología y limitaciones*.
"""

LIMITACIONES = f"""
## Qué es el IDEC

Índice compuesto que mide el desempeño económico del clúster turístico a nivel
comunal, construido con registros administrativos públicos. Integra tres
dimensiones observadas, con igual ponderación:

| Dimensión | Indicadores | Fuente |
|---|---|---|
| Empleo sectorial | trabajadores del rubro por habitante | SII |
| Generación de ingresos | ventas y renta por habitante | SII |
| Capacidad productiva | alojamientos por 1.000 hab., empresas p.c. | SERNATUR + SII |

## Desempeño del modelo

Random Forest sobre {META['n_observaciones']} observaciones
({META['anio_min']}–{META['anio_max']}, {len(META['comunas'])} comunas).

| Esquema de validación | R² | MAE |
|---|---|---|
| Temporal (pronóstico de años futuros) | **{META['metricas']['temporal']['R2']:.3f}** | {META['metricas']['temporal']['MAE']:.4f} |
| Bloques temporales | {META['metricas']['bloques']['R2']:.3f} | {META['metricas']['bloques']['MAE']:.4f} |
| Por comuna (territorios no vistos) | **{META['metricas']['comuna']['R2']:.3f}** | {META['metricas']['comuna']['MAE']:.4f} |

## Limitaciones declaradas

{chr(10).join('- ' + l for l in META['limitaciones'])}
- El bosque aleatorio **comprime los valores extremos hacia la media**
  (correlación entre IDEC observado y residuo: −0,79): subestima a las comunas
  de mayor desempeño —Pucón en torno a un 10 %— y sobreestima a las de menor.
  Por eso el simulador ancla los escenarios en el valor observado y muestra la
  estimación del modelo únicamente como contraste.

## Sobre la variable CET

La **Variable Proxy de Choques Exógenos Territoriales** representa perturbaciones
ajenas al rubro turístico (crisis sanitarias, conflictividad, desastres).

- Rango **[0, 1]**: **1 = condiciones normales** (valor por defecto), 0 = choque máximo.
- Opera en **modo estructural**: el efecto se aplica como atenuación con
  elasticidad λ **declarada**, no estimada de los datos.
- Motivo: la elasticidad histórica no está identificada. Durante 2020 el IDEC
  estructural resultó resiliente —seis de trece comunas incluso aumentaron su
  desempeño— mientras el colapso ocurría en los flujos de visitantes (−57 % de
  llegadas), dimensión no incorporada al índice.
- Como referencia empírica, la visitación a áreas protegidas cayó en 2020 a
  **0,475** de su nivel de 2019.

## Fuentes de datos

Servicio de Impuestos Internos · Banco Integrado de Proyectos · Instituto
Nacional de Estadísticas · SERNATUR · CONAF. Todas de acceso público.

---

*Investigación doctoral — Germán Patricio Barra Ávila, TECH Universidad
Tecnológica. Modelación del desempeño económico del clúster turístico de la
Región de La Araucanía mediante técnicas de Machine Learning aplicadas a datos
públicos.*
"""

with gr.Blocks(title="Simulador IDEC — Clúster Turístico de La Araucanía") as demo:
    gr.Markdown("# Simulador IDEC — Clúster Turístico de La Araucanía")
    gr.Markdown(AVISO)

    with gr.Tab("Simulador de escenarios"):
        gr.Markdown(
            "Seleccione una comuna y un año, y ajuste la variable de choque "
            "exógeno para estimar su efecto sobre el desempeño del clúster."
        )
        with gr.Row():
            with gr.Column(scale=1):
                in_comuna = gr.Dropdown(COMUNAS, value="Pucón", label="Comuna")
                in_anio = gr.Dropdown(ANIOS, value=ANIOS[-1], label="Año")
                in_cet = gr.Slider(
                    0.0, 1.0, value=CET_NEUTRO, step=0.05,
                    label="CET — Choques Exógenos Territoriales",
                    info="1 = sin choque (por defecto) · 0 = choque máximo",
                )
                in_lambda = gr.Slider(
                    0.0, 1.0, value=ELASTICIDAD_DEFAULT, step=0.05,
                    label="λ — elasticidad ante el choque",
                    info="Parámetro declarado: cuánto del choque se traslada al desempeño",
                )
                btn = gr.Button("Simular", variant="primary")
            with gr.Column(scale=2):
                out_md = gr.Markdown()
                out_curva = gr.LinePlot(
                    x="CET", y="IDEC", title="Respuesta del IDEC ante el choque",
                    x_title="CET (1 = sin choque)", y_title="IDEC estimado",
                    height=280,
                )

        entradas = [in_comuna, in_anio, in_cet, in_lambda]
        salidas = [out_md, out_curva]
        btn.click(simular, entradas, salidas)
        for componente in entradas:
            componente.change(simular, entradas, salidas)
        demo.load(simular, entradas, salidas)

    with gr.Tab("Explorador del panel"):
        gr.Markdown("Evolución del IDEC observado y comparación entre comunas.")
        with gr.Row():
            with gr.Column():
                ex_comuna = gr.Dropdown(COMUNAS, value="Curacautín",
                                        label="Comuna — evolución temporal")
                ex_serie = gr.LinePlot(
                    x="Año", y="IDEC", title="IDEC observado por año",
                    height=280,
                )
            with gr.Column():
                ex_anio = gr.Dropdown(ANIOS, value=ANIOS[-1],
                                      label="Año — comparación entre comunas")
                ex_barras = gr.BarPlot(
                    x="Comuna", y="IDEC", title="IDEC por comuna",
                    height=280,
                )
        ex_tabla = gr.Dataframe(label="Detalle por comuna", wrap=True)

        ex_comuna.change(serie_comuna, ex_comuna, ex_serie)
        ex_anio.change(ranking, ex_anio, [ex_tabla, ex_barras])
        demo.load(serie_comuna, ex_comuna, ex_serie)
        demo.load(ranking, ex_anio, [ex_tabla, ex_barras])

    with gr.Tab("Metodología y limitaciones"):
        gr.Markdown(LIMITACIONES)


if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft())
