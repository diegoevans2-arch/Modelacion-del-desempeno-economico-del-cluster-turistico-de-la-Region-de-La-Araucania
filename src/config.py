"""Configuración central del proyecto.

Rutas, catálogo comunal y definición del clúster turístico.
Ninguna ruta absoluta va hardcodeada en notebooks: todo pasa por aquí.
"""

import os
from pathlib import Path

# --------------------------------------------------------------------------
# Rutas
# --------------------------------------------------------------------------
# Los datos crudos viven fuera del repo (volumen y licencia de redistribución).
# Se puede sobreescribir con la variable de entorno TESIS_BBDD_DIR.

REPO_DIR = Path(__file__).resolve().parents[1]

BBDD_DIR = Path(
    os.environ.get(
        "TESIS_BBDD_DIR",
        Path.home() / "Documents" / "BBDD_tesis_doctorado_german",
    )
)

DATA_DIR = REPO_DIR / "BBDD"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
FINAL_DIR = DATA_DIR / "final"

for _d in (RAW_DIR, PROCESSED_DIR, FINAL_DIR):
    _d.mkdir(parents=True, exist_ok=True)

# Archivos fuente
BIP_CSV = BBDD_DIR / "inversiones_202503.csv"
SERNATUR_CSV = BBDD_DIR / "RegistroAlojamientosTuristicos.csv"
EMAT_XLSX = BBDD_DIR / "consolidado_ReporteDinamicoEMAT_2017_2026.xlsx"
PIB_XLSX = BBDD_DIR / "PIB REGIONAL.xlsx"
ENE_CSV = BBDD_DIR / "data (2) - PARA PILOTEAR_granularidad_final.csv"

# Pendientes de levantamiento (ver README de datos)
SII_DIR = BBDD_DIR / "SII"          # empresas por comuna y rubro
EMAT_MENSUAL_DIR = BBDD_DIR / "EMAT_MENSUAL"

# --------------------------------------------------------------------------
# Período de estudio
# --------------------------------------------------------------------------
ANIO_INICIO = 2013
ANIO_FIN = 2025          # 2026 se excluye: año parcial en EMAT

# --------------------------------------------------------------------------
# Catálogo comunal — Región de La Araucanía (código INE)
# --------------------------------------------------------------------------
# REG_CLAVE del BIP para La Araucanía. Verificado: el BIP codifica región como
# 168 + número de región (Biobío 8→176, Los Lagos 10→178, RM 13→181).
BIP_REG_CLAVE_ARAUCANIA = 177

COMUNAS_ARAUCANIA = {
    9101: "Temuco",          9102: "Carahue",        9103: "Cunco",
    9104: "Curarrehue",      9105: "Freire",         9106: "Galvarino",
    9107: "Gorbea",          9108: "Lautaro",        9109: "Loncoche",
    9110: "Melipeuco",       9111: "Nueva Imperial", 9112: "Padre Las Casas",
    9113: "Perquenco",       9114: "Pitrufquén",     9115: "Pucón",
    9116: "Saavedra",        9117: "Teodoro Schmidt",9118: "Toltén",
    9119: "Vilcún",          9120: "Villarrica",     9121: "Cholchol",
    9201: "Angol",           9202: "Collipulli",     9203: "Curacautín",
    9204: "Ercilla",         9205: "Lonquimay",      9206: "Los Sauces",
    9207: "Lumaco",          9208: "Purén",          9209: "Renaico",
    9210: "Traiguén",        9211: "Victoria",
}

# --------------------------------------------------------------------------
# Definición del clúster turístico
# --------------------------------------------------------------------------
# NÚCLEO: comunas que SERNATUR agrupa en Destinos Turísticos oficiales dentro
# del Registro Nacional de Prestadores. Criterio externo y citable — evita el
# umbral arbitrario. Concentra el 83% de la oferta formal regional.

DESTINOS_SERNATUR = {
    "Pucón y Villarrica":  [9115, 9120],
    "Araucanía Andina":    [9203, 9205, 9110],
    "Temuco y Lago Budi":  [9101, 9111, 9102],
}

CLUSTER_NUCLEO = sorted(c for comunas in DESTINOS_SERNATUR.values() for c in comunas)

# ANILLO: comunas sin destino oficial pero con oferta formal relevante (>=4
# alojamientos registrados). Se usan solo en el análisis de sensibilidad.
CLUSTER_ANILLO = [9103, 9211, 9201, 9116, 9119]  # Cunco, Victoria, Angol, Saavedra, Vilcún

CLUSTER_EXTENDIDO = sorted(CLUSTER_NUCLEO + CLUSTER_ANILLO)

COMUNA_A_DESTINO = {
    c: destino for destino, comunas in DESTINOS_SERNATUR.items() for c in comunas
}


def nombre_comuna(codigo: int) -> str:
    """Nombre oficial de la comuna a partir del código INE."""
    return COMUNAS_ARAUCANIA.get(int(codigo), f"<desconocida:{codigo}>")
