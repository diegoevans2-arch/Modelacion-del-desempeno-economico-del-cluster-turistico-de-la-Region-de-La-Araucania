"""Agrupamiento territorial del clúster turístico (H3).

DOS NIVELES DE ANÁLISIS, PORQUE RESPONDEN PREGUNTAS DISTINTAS

- `nivel="comuna"`: una observación por comuna (perfil promedio del período).
  Es la tipología territorial que H3 pide literalmente. Con sólo 13 unidades
  la partición es frágil, así que `estabilidad()` es obligatorio antes de
  interpretar nada.

- `nivel="comuna_anio"`: una observación por comuna y año (156). Identifica
  *regímenes de desempeño* y permite observar el tránsito de una comuna entre
  regímenes — que es donde conecta con el resultado de convergencia.

ADVERTENCIA SOBRE LA ELECCIÓN DE VARIABLES

Agrupar directamente sobre los componentes del IDEC produce una partición por
nivel ("alto / medio / bajo"), no una tipología: los conglomerados serían
tramos del propio índice. Para que el agrupamiento aporte información nueva,
`VARIABLES_PERFIL` mezcla intensidad turística, escala, estructura productiva
y composición sectorial, de modo que dos comunas puedan diferenciarse por
*forma* del perfil y no sólo por magnitud.
"""

import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.metrics import (
    adjusted_rand_score,
    calinski_harabasz_score,
    davies_bouldin_score,
    silhouette_score,
)
from sklearn.preprocessing import StandardScaler

VARIABLES_PERFIL = [
    "alojamientos_por_mil_hab",     # intensidad de oferta turística formal
    "ventas_pc",                    # desempeño económico del rubro
    "trabajadores_por_empresa",     # tamaño medio de los establecimientos
    "ventas_por_empresa",           # productividad aparente
    "poblacion",                    # escala del territorio
    "ventas_uf_recreativas_pc",     # servicios turísticos complementarios
    "ventas_uf_inmobiliarias_pc",   # dinamismo inmobiliario
]

RANGO_K = range(2, 7)


def preparar_matriz(panel, variables=None, nivel="comuna", log=True):
    """Construye la matriz estandarizada para agrupar.

    Se aplica log1p antes de estandarizar: las variables económicas comunales
    están muy sesgadas y, sin transformar, la distancia euclídea queda
    dominada por Pucón y Temuco, con lo que el agrupamiento degenera en
    "outliers contra el resto".
    """
    variables = variables or VARIABLES_PERFIL
    d = panel.dropna(subset=variables).copy()

    if nivel == "comuna":
        d = d.groupby(["comuna", "comuna_nombre"], as_index=False)[variables].mean()
        etiquetas = d[["comuna", "comuna_nombre"]].copy()
    elif nivel == "comuna_anio":
        etiquetas = d[["comuna", "comuna_nombre", "anio"]].copy()
    else:
        raise ValueError(f"nivel no reconocido: {nivel!r}")

    X = d[variables].to_numpy(dtype=float)
    if log:
        X = np.log1p(np.clip(X, 0, None))
    X = StandardScaler().fit_transform(X)
    return X, etiquetas.reset_index(drop=True), variables


def evaluar_k(X, rango=RANGO_K, algoritmo="kmeans", random_state=42):
    """Métricas de selección de k, combinando dos familias de criterios.

    - Codo (inercia / WCSS): criterio de compacidad. Baja monótonamente con k,
      así que no tiene óptimo; el "codo" es el punto de rendimiento marginal
      decreciente. `codo_optimo()` lo localiza de forma objetiva.
    - Silueta y Davies-Bouldin: criterios de separación, con óptimo interno.
    - Calinski-Harabasz: razón varianza inter/intra.

    Se reportan juntos a propósito: cuando codo y silueta coinciden en un k, la
    elección es defendible; cuando discrepan, la estructura es ambigua y hay
    que decirlo.
    """
    filas = []
    for k in rango:
        if k >= len(X):
            continue
        etq = _ajustar(X, k, algoritmo, random_state)
        if len(np.unique(etq)) < 2:
            continue
        filas.append(
            {
                "k": k,
                "inercia_wcss": round(_wcss(X, etq), 3),
                "silueta": round(silhouette_score(X, etq), 4),
                "davies_bouldin": round(davies_bouldin_score(X, etq), 4),
                "calinski_harabasz": round(calinski_harabasz_score(X, etq), 2),
            }
        )
    t = pd.DataFrame(filas)
    if len(t):
        k_codo = codo_optimo(t["k"].tolist(), t["inercia_wcss"].tolist())
        t["codo"] = t["k"] == k_codo
        t["mejor_silueta"] = t["silueta"] == t["silueta"].max()
        t["mejor_db"] = t["davies_bouldin"] == t["davies_bouldin"].min()
    return t


def codo_optimo(ks, inercias):
    """Localiza el codo de la curva de inercia sin intervención visual.

    Método de la máxima distancia a la cuerda (base del algoritmo Kneedle):
    se traza la recta entre el primer y el último punto de la curva (k, WCSS) y
    se elige el k cuyo punto queda más lejos de esa recta. Es reproducible y no
    depende de inspeccionar el gráfico, requisito para que la elección de k sea
    auditable en la tesis.
    """
    ks = np.asarray(ks, dtype=float)
    y = np.asarray(inercias, dtype=float)
    if len(ks) < 3:
        return int(ks[0])
    x0, y0, x1, y1 = ks[0], y[0], ks[-1], y[-1]
    # distancia perpendicular de cada punto a la cuerda (x0,y0)-(x1,y1)
    num = np.abs((y1 - y0) * ks - (x1 - x0) * y + x1 * y0 - y1 * x0)
    den = np.hypot(y1 - y0, x1 - x0)
    return int(ks[np.argmax(num / den)])


def _wcss(X, labels):
    """Suma de cuadrados intra-clúster (idéntica a KMeans.inertia_).

    Se calcula desde las etiquetas para que sirva a cualquier algoritmo, no
    sólo a KMeans."""
    total = 0.0
    for c in np.unique(labels):
        pts = X[labels == c]
        total += ((pts - pts.mean(axis=0)) ** 2).sum()
    return float(total)


def clusterizar(X, k, algoritmo="kmeans", random_state=42):
    return _ajustar(X, k, algoritmo, random_state)


def estabilidad(X, k, algoritmo="kmeans", n_muestras=200, fraccion=0.8,
                random_state=42):
    """Estabilidad de la partición ante remuestreo.

    Con 13 comunas, una partición puede verse nítida y aun así depender de una
    o dos observaciones. Se remuestrea sin reemplazo y se mide el ARI entre la
    partición completa y la del submuestreo, restringido a los puntos comunes.

    ARI medio > 0,75 sugiere una estructura robusta; < 0,5 indica que la
    partición no debe interpretarse sustantivamente.
    """
    rng = np.random.default_rng(random_state)
    base = _ajustar(X, k, algoritmo, random_state)
    n = len(X)
    tam = max(k + 1, int(fraccion * n))

    aris = []
    for _ in range(n_muestras):
        idx = rng.choice(n, size=tam, replace=False)
        etq = _ajustar(X[idx], k, algoritmo, random_state)
        if len(np.unique(etq)) < 2:
            continue
        aris.append(adjusted_rand_score(base[idx], etq))

    return {
        "k": k,
        "ari_medio": round(float(np.mean(aris)), 4) if aris else np.nan,
        "ari_p10": round(float(np.percentile(aris, 10)), 4) if aris else np.nan,
        "n_muestras": len(aris),
        "veredicto": _veredicto_estabilidad(np.mean(aris) if aris else np.nan),
    }


def perfil_clusters(etiquetas, X, variables, asignacion):
    """Perfil medio de cada conglomerado, en unidades estandarizadas."""
    d = pd.DataFrame(X, columns=variables)
    d["cluster"] = asignacion
    perfil = d.groupby("cluster").mean().round(2)
    perfil["n"] = d.groupby("cluster").size()
    return perfil.reset_index()


def concordancia_externa(etiquetas, asignacion, col="destino_sernatur"):
    """Compara la partición hallada contra los Destinos Turísticos SERNATUR.

    Es validación externa: si el agrupamiento reproduce una clasificación
    construida por otra institución con otros criterios, la estructura no es
    un artefacto del algoritmo.
    """
    d = etiquetas.copy()
    d["cluster"] = asignacion
    d[col] = d[col].fillna("Sin destino")
    contingencia = pd.crosstab(d["cluster"], d[col])
    ari = adjusted_rand_score(d[col].astype("category").cat.codes, asignacion)
    return contingencia, round(ari, 4)


def _ajustar(X, k, algoritmo, random_state):
    if algoritmo == "kmeans":
        return KMeans(n_clusters=k, n_init=50, random_state=random_state).fit_predict(X)
    if algoritmo == "jerarquico":
        return AgglomerativeClustering(n_clusters=k, linkage="ward").fit_predict(X)
    raise ValueError(f"algoritmo no reconocido: {algoritmo!r}")


def _veredicto_estabilidad(ari):
    if np.isnan(ari):
        return "no evaluable"
    if ari > 0.75:
        return "ROBUSTA"
    if ari > 0.50:
        return "MODERADA — interpretar con cautela"
    return "FRÁGIL — no interpretar sustantivamente"
