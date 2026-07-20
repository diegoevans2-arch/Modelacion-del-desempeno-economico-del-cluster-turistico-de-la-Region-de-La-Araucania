# Datos del proyecto

Los archivos crudos **no se versionan** (volumen y condiciones de
redistribución). Viven en una carpeta externa, apuntada por `src/config.py`:

```bash
# opcional, si la carpeta no está en la ruta por defecto
export TESIS_BBDD_DIR="/ruta/a/BBDD_tesis_doctorado_german"
```

---

## Estado por fuente

| Fuente | Granularidad | Ventana útil | Estado |
|---|---|---|---|
| BIP — inversión pública | **comuna × año** | 2013–2022 | ✅ Procesada |
| SERNATUR — alojamientos | comuna (corte transversal) | snapshot | ⚠️ Sin dimensión temporal |
| EMAT — actividad hotelera | región × año | 2017–2025 | ⚠️ Falta versión mensual |
| ENE — empleo turístico | región × trimestre móvil | 2013–2025 | ✅ Procesada |
| PIB — Banco Central | región × trimestre | 2013–2025 | ✅ Procesada |
| **SII — empresas por comuna y rubro** | **comuna × año** | 2013–2023 | 🔴 **Pendiente** |

---

## Pendiente 1 — SII, Estadísticas de empresas por comuna y rubro

Es el levantamiento crítico. Sin él, ninguna variable de actividad económica
turística tiene variación comunal genuina y la desagregación queda degenerada
(ver más abajo).

**Qué descargar:** serie anual de *Estadísticas de empresas por comuna y rubro
económico* del Servicio de Impuestos Internos, publicada en su portal de
estadísticas.

**Filtros:** Región de La Araucanía · rubro CIIU **I — Actividades de
alojamiento y de servicio de comidas** (conviene traer también *G — Comercio* y
*R — Actividades artísticas y recreativas* como covariables del clúster).

**Campos necesarios:** año · comuna · rubro · número de empresas · ventas
anuales (UF) · número de trabajadores dependientes informados · renta neta
informada.

**Destino:** `$TESIS_BBDD_DIR/SII/` — un archivo por año, sin renombrar.

**Verificar al descargar:** que el desglose sea efectivamente comunal (no
regional) y que el rubro I esté desagregado. Si el SII enmascara comunas con
pocos contribuyentes por secreto tributario, registrar cuáles: son faltantes
estructurales, no ceros.

## Pendiente 2 — EMAT mensual

El consolidado actual son reportes **anuales** (un `.xls` por año), lo que
deja 9 observaciones. El Reporte Dinámico del INE permite exportar la serie
**mensual**: 2017–2025 son ~108 observaciones reales.

**Destino:** `$TESIS_BBDD_DIR/EMAT_MENSUAL/`

No sustituir esto por desagregación temporal: es dato observado disponible.

## Pendiente 3 — SERNATUR con fecha de inscripción

`RegistroAlojamientosTuristicos.csv` no trae fecha de inscripción, así que la
capacidad comunal es un corte transversal fijo. Para convertirlo en serie:
solicitar a SERNATUR el registro con fecha de inscripción por Ley de
Transparencia, o recuperar cortes anuales archivados.

Mientras tanto, `n_alojamientos` **no puede usarse como peso de desagregación
dinámica** — es exactamente lo que genera el panel de rango 1.

---

## Por qué importa: el panel degenerado

Desagregar una serie regional multiplicándola por un peso comunal fijo,
`x_it = X_t · w_i`, produce una matriz de **rango 1**. Verificado sobre estos
datos con `src/features/diagnostics.py`:

| Variable | Interacción comuna×tiempo | Rango | Theil |
|---|---|---|---|
| Inversión BIP (dato comunal real) | **59,8 %** | 10 | varía |
| EMAT × share fijo SERNATUR | **0,0 %** | **1** | **0,639343 todos los años** |

El índice de Theil bajo desagregación ingenua es idéntico hasta el sexto
decimal en los nueve años. H3 y el análisis de desigualdad territorial serían
formalmente incontrastables.

Toda variable desagregada debe pasar por
`diagnostics.tabla_diagnostico()` antes de entrar a un modelo. Umbral: si la
interacción es menor al 5 %, la variable entra sólo como control; si es menor
al 1 %, no entra.
