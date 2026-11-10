---
tipo: instrucción operativa
para: Germán Patricio Barra Ávila
de: Diego Evans Pérez Paz — componente de Machine Learning
fecha: 2026-11-09
---

# Instrucciones para gestionar las revisiones del componente cuantitativo

## 1. Qué está pasando, en corto

Las últimas tres revisiones llegaron a conclusiones equivocadas por la misma
razón: **quien revisó no tenía el repositorio a la vista**.

No faltaron análisis. Faltó entregarlos. La V33 llegó a decir que no recibió un
archivo que existía en el repositorio desde antes de esa revisión. Como
consecuencia, el documento **retrocedió**: cosas que ya estaban resueltas
volvieron a quedar escritas como "pendiente de evidencia".

El último documento, el *Plan ML para llevar la tesis a 98/100*, repite el
patrón y además propone un procedimiento que haría daño: usar como variables
predictoras las tres dimensiones que **componen** el IDEC. Eso equivale a
predecir un promedio a partir de sus propios términos. El detalle técnico está
en [VEREDICTO_plan_robustez_y_regla_de_revision.md](VEREDICTO_plan_robustez_y_regla_de_revision.md).

**No lo apliques.**

## 2. La regla, en una frase

> Antes de que alguien escriba una observación sobre la parte cuantitativa,
> tiene que haber abierto el repositorio. Si no lo abrió, su observación no
> entra al documento como carencia tuya.

Esto importa porque hay una diferencia que se ha estado confundiendo:

| Situación real | Cómo debe rotularse |
|---|---|
| La evidencia no existe | *pendiente de evidencia* |
| La evidencia existe y no se consultó | *no verificada por el revisor* |
| La evidencia existe y se consultó | *verificada*, o *discrepante* con la cifra |

Las tres últimas rondas usaron el primer rótulo cuando correspondía el segundo.
Eso te atribuye a ti una carencia que es del proceso de revisión, y es lo que
hizo retroceder al documento.

## 3. Qué entregar antes de pedir cualquier revisión

Copia y envía este mensaje a quien vaya a revisar:

---

> Antes de emitir observaciones sobre el componente de Machine Learning, por
> favor completa estos cuatro pasos. Si alguno no se puede completar, indícalo
> y la observación se rotulará "no verificada por el revisor".
>
> **1. Clonar el repositorio** (enlace: `________`)
>
> **2. Instalar el entorno exacto.** Usa `requirements-lock.txt`, no
> `requirements.txt`: el segundo declara rangos de versión y no reproduce las
> cifras.
>
> ```
> python -m venv .venv
> .venv\Scripts\pip install -r requirements-lock.txt
> ```
>
> **3. Regenerar el panel**
>
> ```
> python -m src.build_panel
> ```
>
> **4. Leer estos cuatro archivos antes de escribir nada**
>
> - `BBDD/final/evidencia_entorno.txt` — configuración, semilla, versiones y
>   hashes
> - `BBDD/final/evidencia_metricas_por_particion.csv` — **contiene las dos
>   definiciones de R²**, que no son equivalentes
> - `BBDD/final/evidencia_predicciones_por_fila.csv` — 2.605 predicciones con
>   su partición
> - `BBDD/final/resultados_h3_asignacion_por_fila.csv` — las 152 asignaciones
>   del agrupamiento
>
> Además, el documento `Documentación/VEREDICTO_plan_robustez_y_regla_de_revision.md`
> contiene en su §14 la tabla de **cifras canónicas**. Cualquier cifra que
> propongas debe coincidir con ella, o explicar la discrepancia.

---

## 4. Cómo verificar una observación sin saber programar

No necesitas ejecutar nada. Hazte tres preguntas:

**¿Qué archivo del repositorio miró?** Si la observación no nombra un archivo
concreto, pide que lo nombre. Las tres últimas rondas citaron archivos que no
existen: `04_unsupervised_clustering.ipynb`, objetos llamados `rf_model` y
`tscv`, y una función `TimeSeriesSplit`. Nada de eso está en el proyecto. El
análisis vive en la carpeta `src/`.

**¿La cifra coincide con la tabla canónica?** Está en §14 del documento de
veredicto. Si difiere y el revisor no explica por qué, la tabla manda.

**¿Dice "pendiente" sobre algo que ya está entregado?** Compáralo con la
lista de §6 de este documento.

## 5. Cuándo devolver una revisión sin incorporarla

Cualquiera de estas señales basta:

- **Usa `datos.json` como fuente del análisis.** Ese archivo es la exportación
  del simulador, con los valores redondeados a cuatro decimales y las
  predicciones ya calculadas. No es la base de datos del estudio.
- **Propone predecir el IDEC usando `d2`, `d3`, `d4`, ventas, empleo, renta,
  empresas o alojamientos per cápita.** Todas esas variables *forman* el índice.
  Es el error del último plan.
- **Asigna puntajes** del tipo "84/100" o "98/100" sin una rúbrica que los
  respalde. El último plan inventó esos números en un documento cuyo principio
  declarado era no inventar números.
- **Habla de R² sin decir cuál de los dos.** Hay dos definiciones en juego
  (ver §7).
- **Propone "reejecutar"** sin haber instalado `requirements-lock.txt`.

## 6. Qué está cerrado y qué sigue abierto

**Cerrado y entregado** — si una revisión lo marca pendiente, está equivocada:

| Control | Dónde está la evidencia |
|---|---|
| Hiperparámetros, semilla, entorno | `evidencia_entorno.txt` |
| Particiones y predicciones por fila | `evidencia_predicciones_por_fila.csv` |
| Las 152 asignaciones y las 4 exclusiones | `resultados_h3_asignacion_por_fila.csv` |
| Correspondencia CONAF unidad→comuna | `evidencia_conaf_correspondencia.csv` |
| Umbral del anillo 3 / 4 / 5 | `evidencia_sensibilidad_umbral_anillo.csv` |
| Cobertura temporal de cada predictor | `evidencia_disponibilidad_predictores.csv` |
| Métricas por año de prueba | `resultados_h2_metricas_por_anio.csv` |
| Barrido de clustering k = 2…7 | `resultados_h3_seleccion_k.csv` |
| COVID-19, sin D4, escala no acotada | §6, §7 y §8 de `EVIDENCIA_respuesta_correcciones_07-10.md` |

**Realmente abierto**, y conviene abordarlo:

1. **Pruebas automáticas de coherencia** entre las cifras del texto y los
   archivos de resultados. Es la única idea genuinamente nueva del último plan.
   Habría evitado los dos desajustes de cifras que aparecieron.
2. **Nombrar el algoritmo del agrupamiento en el texto.** Los regímenes se
   obtuvieron con agrupamiento **jerárquico**. No está dicho en §4.7, y quien
   reejecute con el valor por defecto obtendrá otros conteos y creerá haber
   encontrado un error. Me pasó a mí al verificarlo.
3. **Declarar la unidad de remuestreo del ARI.** El 0,79 publicado corresponde
   a remuestreo por fila. Por comuna completa baja a 0,70.

## 7. Las cuatro correcciones de cifras que faltan en el texto

| Cifra | Dónde | Corrección |
|---|---|---|
| Spearman "0,92 a 1,00" | donde se adopta "para coherencia documental" | El mínimo verificado es 0,914971 → **0,91 a 1,00**. La otra sección ya lo dice bien |
| R² = 0,68 pre-CONAF | Anexo G y §4.4 | El valor reproducible es **0,674**, y es un promedio por pliegue, no un R² agrupado |
| "0,68 sin trazabilidad" | Anexo G | Sí es trazable: es el promedio por pliegue de la especificación previa a CONAF |
| 152/156 "pendiente" | §4.7, Tabla 4.7, Anexo L | Resuelto: Melipeuco y Lonquimay, 2013 y 2014, porque el SII no registra empresas de actividades recreativas en esas comunas y años |

### Sobre los dos R², que es la confusión más persistente

El código calcula el R² de dos formas, para dos propósitos distintos:

- **R² agrupado**: junta todas las predicciones y calcula un solo valor. Es el
  de la **Tabla 4.4**. En el esquema de bloques vale **0,762**.
- **R² promedio de pliegues**: calcula uno por partición y los promedia. Es el
  que acompaña a la **tabla de importancias**. En bloques vale **0,788**.

Los dos son correctos. El error fue mío: te los entregué como si fueran la misma
cantidad. No deben mezclarse, y conviene nombrarlos distinto en el texto.

## 8. Lo que no se arregla con más revisiones

Estos límites son reales y deben quedar declarados. Si alguien ofrece cerrarlos,
desconfía — probablemente esté introduciendo circularidad:

1. **El índice no mide flujos turísticos.** Falta la dimensión D1 porque la EMAT
   por destino está suspendida desde abril de 2020.
2. **Son trece comunas.** Las 156 filas no equivalen a 156 unidades
   independientes.
3. **El modelo no transfiere a comunas nuevas**: R² = −0,3619. Hay que decirlo
   sin matizar. **Si una propuesta mejora mucho esta cifra, lo primero que hay
   que revisar es si introdujo circularidad.** El último plan la subía a +0,63
   exactamente así.
4. **El registro de alojamientos no tiene fecha de inscripción**, así que D4 no
   aporta variación en el tiempo. Un "registro fechado" no existe en la fuente:
   esa petición del Anexo G no se puede cumplir y conviene reformularla.
5. **Los umbrales de las hipótesis no están preregistrados.** Fijarlos ahora
   sería retrospectivo. Tu postura actual es defendible, pero conviene
   confirmarla con la comisión.
6. **La magnitud de la convergencia es sensible.** Sin Pucón, la caída de Theil
   pasa de −53,5 % a cerca de −33 %. La dirección se sostiene; la magnitud
   puntual requiere cautela con trece observaciones.

## 9. Resumen

- No apliques el plan de 98/100.
- Antes de pedir una revisión, entrega el repositorio con los cuatro pasos de §3.
- Si una revisión no nombra los archivos que miró, devuélvela.
- Corrige las cuatro cifras de §7.
- Agrega las tres cosas de §6 que sí están abiertas.
- Mantén declarados los seis límites de §8.
