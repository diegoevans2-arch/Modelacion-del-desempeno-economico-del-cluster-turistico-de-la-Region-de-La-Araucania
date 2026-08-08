"""Variable Proxy de Choques Exógenos Territoriales (CET).

Representa la intensidad de perturbaciones **ajenas al rubro turístico** que
condicionan su desempeño (crisis sanitarias, conflictividad territorial,
desastres naturales, cortes de conectividad).

    CET ∈ [0, 1]      1 = condiciones normales, sin choque (valor por defecto)
                      0 = choque máximo
                    0,7 = el territorio opera al 70 % de su normalidad

Es una variable **dinámica**: el usuario puede fijarla para simular escenarios.


═══════════════════════════════════════════════════════════════════════════
POR QUÉ ESTE MÓDULO CONSTRUYE UNA SERIE HISTÓRICA (y no sólo acepta un input)
═══════════════════════════════════════════════════════════════════════════

Si la CET entrara al entrenamiento valiendo siempre 1, tendría **varianza
cero**: los árboles nunca la usarían para partir y su importancia sería
exactamente 0. El usuario podría fijar CET = 0,2 y la predicción no cambiaría
en absoluto — verificado empíricamente: cambio 0,0000000000.

Sería un fallo silencioso: el código corre, devuelve números, y la perilla no
hace nada.

Para que la CET tenga efecto real, el modelo debe **aprender** la relación
entre choques y desempeño a partir de períodos en que efectivamente hubo
choques. Por eso se construye una serie histórica comuna × año a partir de
eventos exógenos documentados, y el modelo se entrena con ella. La CET que el
usuario ingresa después opera sobre esa relación aprendida.


═══════════════════════════════════════════════════════════════════════════
ADVERTENCIA SOBRE LAS INTENSIDADES POR DEFECTO
═══════════════════════════════════════════════════════════════════════════

Los valores de `EVENTOS_DEFAULT` son **supuestos declarados, no mediciones**.
Reflejan el orden de magnitud de eventos conocidos, pero DEBEN ser validados y
recalibrados por el investigador contra fuentes documentales (decretos,
índices de movilidad, registros de conectividad). El módulo los explicita
justamente para que sean auditables y modificables, no para que se asuman
como dato duro.

Para anclarlos empíricamente a una serie externa, ver `calibrar_desde_serie()`.


═══════════════════════════════════════════════════════════════════════════
ADVERTENCIA DE CIRCULARIDAD FUTURA
═══════════════════════════════════════════════════════════════════════════

La CET **no debe construirse a partir de indicadores turísticos** (llegadas,
pernoctaciones, ocupación). Sería endógena: se estaría explicando el turismo
con el turismo. Debe derivarse de los eventos, no de sus consecuencias.

Cuando la dimensión D1 (EMAT) se incorpore al IDEC, revisar que ninguna
componente de la CET provenga de esa fuente.
"""

import numpy as np
import pandas as pd

from src import config

CET_NEUTRO = 1.0

# Provincia de Malleco: comunas donde la conflictividad territorial ha tenido
# mayor presencia. Se separa de Cautín para permitir choques diferenciados.
COMUNAS_MALLECO = [9201, 9202, 9203, 9204, 9205, 9206, 9207, 9208, 9209, 9210, 9211]

# ---------------------------------------------------------------------------
# Tabla de eventos. SUPUESTOS DECLARADOS — recalibrar con fuentes documentales.
#
#   intensidad ∈ [0,1] : magnitud del choque (0 = sin efecto, 1 = paralización)
#   alcance            : "regional" (todas las comunas) o lista de códigos INE
# ---------------------------------------------------------------------------
EVENTOS_DEFAULT = [
    # Crisis sanitaria COVID-19: restricciones de movilidad y cierre de
    # fronteras. Alcance regional; intensidad decreciente con la reapertura.
    {"evento": "COVID-19", "anio": 2020, "intensidad": 0.55, "alcance": "regional"},
    {"evento": "COVID-19", "anio": 2021, "intensidad": 0.35, "alcance": "regional"},
    {"evento": "COVID-19", "anio": 2022, "intensidad": 0.10, "alcance": "regional"},

    # Conflictividad territorial y estado de excepción en la Macrozona Sur.
    # Afecta con mayor intensidad la provincia de Malleco. FECHAS E INTENSIDADES
    # A VALIDAR por el investigador contra los decretos correspondientes.
    {"evento": "Conflictividad territorial", "anio": 2021,
     "intensidad": 0.10, "alcance": COMUNAS_MALLECO},
    {"evento": "Conflictividad territorial", "anio": 2022,
     "intensidad": 0.15, "alcance": COMUNAS_MALLECO},
    {"evento": "Conflictividad territorial", "anio": 2023,
     "intensidad": 0.15, "alcance": COMUNAS_MALLECO},
    {"evento": "Conflictividad territorial", "anio": 2024,
     "intensidad": 0.12, "alcance": COMUNAS_MALLECO},
]


def validar_cet(valor, nombre="CET"):
    """Verifica que un valor de CET esté en [0,1]. Devuelve float."""
    try:
        v = float(valor)
    except (TypeError, ValueError):
        raise ValueError(f"{nombre} debe ser numérico; se recibió {valor!r}")
    if not np.isfinite(v) or not (0.0 <= v <= 1.0):
        raise ValueError(
            f"{nombre} debe estar en el rango [0, 1] "
            f"(1 = sin choque, 0 = choque máximo); se recibió {v}"
        )
    return v


def serie_historica(comunas=None, anios=None, eventos=None):
    """Construye la serie histórica de CET por comuna y año.

    Los choques simultáneos se combinan de forma **multiplicativa**:

        CET = Π (1 - intensidad_e)

    de modo que se acumulan sin poder salir del rango [0,1], y un año sin
    eventos registrados queda en el valor neutro 1.

    Returns
    -------
    DataFrame: comuna, anio, cet, eventos_activos.
    """
    comunas = comunas or config.CLUSTER_EXTENDIDO
    anios = anios or range(config.ANIO_INICIO, config.ANIO_FIN + 1)
    eventos = EVENTOS_DEFAULT if eventos is None else eventos

    filas = []
    for c in comunas:
        for a in anios:
            factor = 1.0
            activos = []
            for ev in eventos:
                if ev["anio"] != a:
                    continue
                alcance = ev["alcance"]
                if alcance != "regional" and c not in alcance:
                    continue
                intensidad = validar_cet(ev["intensidad"], "intensidad")
                factor *= (1.0 - intensidad)
                activos.append(ev["evento"])
            filas.append(
                {
                    "comuna": int(c),
                    "anio": int(a),
                    "cet": round(factor, 4),
                    "eventos_activos": "; ".join(activos) if activos else "",
                }
            )
    return pd.DataFrame(filas)


def agregar_cet(panel, eventos=None, col_comuna="comuna", col_anio="anio"):
    """Incorpora la columna `cet` (serie histórica) a un panel comuna × año."""
    serie = serie_historica(
        comunas=sorted(panel[col_comuna].unique()),
        anios=sorted(panel[col_anio].unique()),
        eventos=eventos,
    )
    return panel.merge(
        serie[["comuna", "anio", "cet"]],
        left_on=[col_comuna, col_anio],
        right_on=["comuna", "anio"],
        how="left",
    ).fillna({"cet": CET_NEUTRO})


def aplicar_escenario(panel, cet=None, col_comuna="comuna", col_anio="anio"):
    """Fija la CET para simular un escenario definido por el usuario.

    Parameters
    ----------
    cet : None | float | dict | DataFrame
        - None  → valor neutro 1,0 (sin choque). **Comportamiento por defecto.**
        - float → mismo valor para todas las comunas y años.
        - dict  → por comuna `{9115: 0.6}` o por par `{(9115, 2025): 0.6}`.
                  Las comunas no mencionadas quedan en 1,0.
        - DataFrame → columnas comuna, anio, cet.

    Returns
    -------
    Copia del panel con la columna `cet` fijada según el escenario.
    """
    d = panel.copy()

    if cet is None:
        d["cet"] = CET_NEUTRO
        return d

    if isinstance(cet, (int, float, np.floating)):
        d["cet"] = validar_cet(cet)
        return d

    if isinstance(cet, dict):
        d["cet"] = CET_NEUTRO
        for clave, valor in cet.items():
            v = validar_cet(valor, f"CET[{clave}]")
            if isinstance(clave, tuple):
                comuna, anio = clave
                mask = (d[col_comuna] == comuna) & (d[col_anio] == anio)
            else:
                mask = d[col_comuna] == clave
            if not mask.any():
                raise ValueError(f"El escenario refiere a {clave!r}, ausente del panel")
            d.loc[mask, "cet"] = v
        return d

    if isinstance(cet, pd.DataFrame):
        faltantes = {"comuna", "anio", "cet"} - set(cet.columns)
        if faltantes:
            raise ValueError(f"El DataFrame de escenario requiere columnas {faltantes}")
        cet = cet.copy()
        cet["cet"] = cet["cet"].map(lambda v: validar_cet(v))
        d = d.drop(columns=["cet"], errors="ignore").merge(
            cet[["comuna", "anio", "cet"]],
            left_on=[col_comuna, col_anio], right_on=["comuna", "anio"], how="left",
        )
        return d.fillna({"cet": CET_NEUTRO})

    raise TypeError(f"Tipo de escenario no soportado: {type(cet).__name__}")


ELASTICIDAD_DEFAULT = 0.6


def atenuar(idec, cet, elasticidad=ELASTICIDAD_DEFAULT, exposicion=None,
            forma="lineal"):
    """Aplica el choque al IDEC proyectado mediante atenuación estructural.

        forma="lineal" :  IDEC' = IDEC · [1 − λ·(1 − CET)]
        forma="potencia":  IDEC' = IDEC · CET^λ

    donde λ (`elasticidad`) es la sensibilidad del desempeño del clúster ante
    choques exógenos. λ = 1 implica traspaso total (CET = 0 anula el
    desempeño); λ = 0,6 implica que un choque del 30 % (CET = 0,7) reduce el
    IDEC en 18 %.

    POR QUÉ ESTE MODO EXISTE
    ------------------------
    El modo aprendido —dejar que el Random Forest infiera el efecto del choque
    desde la serie histórica— **no es confiable con el IDEC vigente**. La
    correlación empírica entre CET e IDEC es −0,004 (nula) y seis de trece
    comunas AUMENTARON su desempeño durante la pandemia: el IDEC integra
    dimensiones estructurales (empleo, ingresos, capacidad) que resultaron
    resilientes, mientras el colapso se produjo en los flujos de visitantes
    (−57 % de llegadas en 2020), que corresponden a la dimensión D1 aún no
    incorporada. Un modelo entrenado así aprende un signo espurio positivo.

    La atenuación estructural resuelve esto imponiendo la dirección teórica y
    haciendo explícito el parámetro λ, que queda sujeto a justificación y
    análisis de sensibilidad por parte del investigador, en lugar de ocultarse
    tras una elasticidad mal identificada.

    Parameters
    ----------
    exposicion : array-like, optional
        Exposición relativa de cada comuna al choque, en [0,1]. Si se entrega,
        λ se pondera por ella (λ_i = λ·e_i), de modo que las comunas más
        dependientes del turismo sufren más. Úsese para choques
        específicamente turísticos; omítase para choques territoriales
        generales, que afectan a todo el territorio por igual.
    """
    idec = np.asarray(idec, dtype=float)
    cet = np.asarray(cet, dtype=float)
    lam = float(elasticidad)
    if not (0.0 <= lam <= 1.0):
        raise ValueError(f"elasticidad debe estar en [0,1]; se recibió {lam}")

    if exposicion is not None:
        e = np.asarray(exposicion, dtype=float)
        rango = np.nanmax(e) - np.nanmin(e)
        e = (e - np.nanmin(e)) / rango if rango > 0 else np.ones_like(e)
        lam = np.clip(lam * e, 0.0, 1.0)

    if forma == "lineal":
        factor = 1.0 - lam * (1.0 - cet)
    elif forma == "potencia":
        factor = np.power(np.clip(cet, 1e-12, 1.0), lam)
    else:
        raise ValueError(f"forma no reconocida: {forma!r}")

    return idec * np.clip(factor, 0.0, 1.0)


def calibrar_desde_serie(serie_choque, invertir=True):
    """Deriva intensidades de CET a partir de una serie externa de choque.

    Permite anclar la CET a un indicador documentado y exógeno al turismo
    (días de restricción de movilidad, índice de conectividad interrumpida,
    eventos registrados), en lugar de usar los supuestos por defecto.

    La serie se reescala a [0,1]. Con `invertir=True` se asume que valores
    altos del indicador representan MAYOR choque, de modo que la CET resultante
    es baja (peor condición).

    IMPORTANTE: la serie no debe provenir de indicadores turísticos — sería
    endógena (ver advertencia del módulo).
    """
    s = pd.Series(serie_choque, dtype="float64")
    rango = s.max() - s.min()
    if rango == 0:
        return pd.Series(CET_NEUTRO, index=s.index)
    z = (s - s.min()) / rango
    return (1.0 - z) if invertir else z


def resumen_serie(serie=None):
    """Tabla legible de la CET histórica, para incluir en la tesis."""
    serie = serie_historica() if serie is None else serie
    piv = serie.pivot_table(index="comuna", columns="anio", values="cet")
    piv.index = [config.nombre_comuna(c) for c in piv.index]
    return piv
