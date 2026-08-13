---
tipo: material de apoyo
tema: Referencias canónicas de los métodos empleados en el Capítulo III
proyecto: Tesis Doctoral — Barra Ávila
fecha: 2026-08-14
---

# Referencias metodológicas — Capítulo III

> ⚠️ **ADVERTENCIA NECESARIA.** Esta lista reúne las referencias canónicas de los
> métodos efectivamente empleados en la investigación. Son obras ampliamente
> conocidas, pero **cada entrada debe ser verificada por el autor** —volumen,
> número, páginas y DOI— antes de incorporarse a la versión definitiva. Ninguna
> bibliografía doctoral debe darse por buena sin comprobación en la fuente.
>
> Se indica, para cada método, el apartado del Capítulo III que lo emplea, de
> modo que la verificación pueda hacerse en orden y sin omisiones.

---

## 1. Modelación supervisada (§3.10.1)

**Random Forest** — *ya citado en la tesis.*
- Breiman, L. (2001). Random forests. *Machine Learning, 45*(1), 5–32.

**Regresión Ridge.** Se emplea como línea base econométrica regularizada ante predictores correlacionados.
- Hoerl, A. E., y Kennard, R. W. (1970). Ridge regression: Biased estimation for nonorthogonal problems. *Technometrics, 12*(1), 55–67.

**Árboles de decisión.**
- Breiman, L., Friedman, J. H., Olshen, R. A., y Stone, C. J. (1984). *Classification and Regression Trees*. Wadsworth.

---

## 2. Importancia de variables (§3.10.1, H1)

**Importancia por permutación.** El estudio la evalúa fuera de muestra, no sobre el conjunto de entrenamiento.
- Strobl, C., Boulesteix, A.-L., Zeileis, A., y Hothorn, T. (2007). Bias in random forest variable importance measures: Illustrations, sources and a solution. *BMC Bioinformatics, 8*, 25.
- Molnar, C. (2022). *Interpretable Machine Learning: A Guide for Making Black Box Models Explainable* (2.ª ed.). Publicación independiente.

---

## 3. Esquemas de validación cruzada (§3.10.3)

Justifican la decisión de no emplear K-fold aleatorio como resultado principal en datos panel.

- Bergmeir, C., y Benítez, J. M. (2012). On the use of cross-validation for time series predictor evaluation. *Information Sciences, 191*, 192–213.
- Roberts, D. R., Bahn, V., Ciuti, S., Boyce, M. S., Elith, J., Guillera-Arroita, G., … Dormann, C. F. (2017). Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. *Ecography, 40*(8), 913–929.
- Hastie, T., Tibshirani, R., y Friedman, J. (2009). *The Elements of Statistical Learning* (2.ª ed.). Springer. *— ya citado.*

---

## 4. Aprendizaje no supervisado (§3.10.4)

**K-Means** — *ya citado (MacQueen, 1967).*
- Lloyd, S. P. (1982). Least squares quantization in PCM. *IEEE Transactions on Information Theory, 28*(2), 129–137.

**Clustering jerárquico con enlace de Ward.**
- Ward, J. H., Jr. (1963). Hierarchical grouping to optimize an objective function. *Journal of the American Statistical Association, 58*(301), 236–244.

**Índices de validación de conglomerados.**
- Rousseeuw, P. J. (1987). Silhouettes: A graphical aid to the interpretation and validation of cluster analysis. *Journal of Computational and Applied Mathematics, 20*, 53–65.
- Davies, D. L., y Bouldin, D. W. (1979). A cluster separation measure. *IEEE Transactions on Pattern Analysis and Machine Intelligence, PAMI-1*(2), 224–227.
- Caliński, T., y Harabasz, J. (1974). A dendrite method for cluster analysis. *Communications in Statistics, 3*(1), 1–27.

**Método del codo y su detección objetiva.** El estudio localiza el codo mediante el criterio de máxima distancia a la cuerda, sin inspección visual.
- Thorndike, R. L. (1953). Who belongs in the family? *Psychometrika, 18*(4), 267–276.
- Satopää, V., Albrecht, J., Irwin, D., y Raghavan, B. (2011). Finding a "kneedle" in a haystack: Detecting knee points in system behavior. *31st International Conference on Distributed Computing Systems Workshops*, 166–171.

**Estabilidad de la partición ante remuestreo.**
- Hubert, L., y Arabie, P. (1985). Comparing partitions. *Journal of Classification, 2*(1), 193–218. *(índice de Rand ajustado)*
- Hennig, C. (2007). Cluster-wise assessment of cluster stability. *Computational Statistics & Data Analysis, 52*(1), 258–271.

---

## 5. Desigualdad y convergencia territorial (§3.10.5)

**Índice de Theil** — *ya citado (Theil, 1967).*
- Shorrocks, A. F. (1980). The class of additively decomposable inequality measures. *Econometrica, 48*(3), 613–625.

**Convergencia β y σ.**
- Barro, R. J., y Sala-i-Martin, X. (1992). Convergence. *Journal of Political Economy, 100*(2), 223–251.
- Sala-i-Martin, X. (1996). The classical approach to convergence analysis. *The Economic Journal, 106*(437), 1019–1036.

**Falacia de Galton.** Sustenta la decisión de contrastar σ-convergencia y β-convergencia de forma conjunta, y no aisladamente.
- Quah, D. T. (1993). Galton's fallacy and tests of the convergence hypothesis. *The Scandinavian Journal of Economics, 95*(4), 427–443.

---

## 6. Construcción de indicadores compuestos (§3.8)

Respaldan las decisiones de normalización, ponderación y análisis de sensibilidad del IDEC.

- OCDE y Centro Común de Investigación. (2008). *Handbook on Constructing Composite Indicators: Methodology and User Guide*. OECD Publishing.
- Saisana, M., Saltelli, A., y Tarantola, S. (2005). Uncertainty and sensitivity analysis techniques as tools for the quality assessment of composite indicators. *Journal of the Royal Statistical Society: Series A, 168*(2), 307–323.
- Nardo, M., Saisana, M., Saltelli, A., y Tarantola, S. (2005). *Tools for Composite Indicators Building*. Comisión Europea, Centro Común de Investigación.

---

## 7. Panel comunal y descomposición de varianza (§3.11.1)

Sustentan el diagnóstico de degeneración, que descompone la varianza en efectos de comuna, de tiempo e interacción.

- Wooldridge, J. M. (2010). *Econometric Analysis of Cross Section and Panel Data* (2.ª ed.). MIT Press.
- Baltagi, B. H. (2021). *Econometric Analysis of Panel Data* (6.ª ed.). Springer.

---

## 8. Estimación en áreas pequeñas (§3.6.5 y §4.3.1)

Marco de referencia del procedimiento de desagregación que se evaluó y finalmente se descartó. Su cita es pertinente precisamente porque el estudio documenta por qué no resultó aplicable.

- Fay, R. E., y Herriot, R. A. (1979). Estimates of income for small places: An application of James-Stein procedures to census data. *Journal of the American Statistical Association, 74*(366), 269–277.
- Rao, J. N. K., y Molina, I. (2015). *Small Area Estimation* (2.ª ed.). Wiley.
- Pfeffermann, D. (2013). New important developments in small area estimation. *Statistical Science, 28*(1), 40–68.

---

## 9. Stock de capital público (§3.6.2)

Respalda el método de inventario perpetuo empleado para construir el stock a partir de los flujos de inversión ejecutada.

- OCDE. (2009). *Measuring Capital: OECD Manual* (2.ª ed.). OECD Publishing.
- Goldsmith, R. W. (1951). A perpetual inventory of national wealth. En *Studies in Income and Wealth* (Vol. 14, pp. 5–73). National Bureau of Economic Research.

---

## 10. Líneas futuras (§5.7)

Sólo si se desarrolla la propuesta de modelo de gravedad para la desagregación de flujos turísticos.

- Morley, C., Rosselló, J., y Santana-Gallego, M. (2014). Gravity models for tourism demand: Theory and use. *Annals of Tourism Research, 48*, 1–10.

---

## Resumen de cobertura

| Apartado del Capítulo III | Referencias nuevas |
|---|---|
| 3.6.2 — Inversión pública (stock de capital) | 2 |
| 3.6.5 / 4.3.1 — Estimación en áreas pequeñas | 3 |
| 3.8 — Construcción del IDEC | 3 |
| 3.10.1 — Modelos supervisados e importancia | 4 |
| 3.10.3 — Esquemas de validación | 2 |
| 3.10.4 — Aprendizaje no supervisado | 8 |
| 3.10.5 — Desigualdad y convergencia | 4 |
| 3.11.1 — Descomposición de varianza en panel | 2 |
| 5.7 — Líneas futuras | 1 |
| **Total** | **29** |
