"""Crea el Space en Hugging Face y sube la aplicación.

Requiere haber iniciado sesión previamente:

    huggingface-cli login

Uso:
    python deploy/publicar_space.py                 # simulacro, no publica nada
    python deploy/publicar_space.py --publicar      # crea el Space y sube
    python deploy/publicar_space.py --publicar --privado

El modo por defecto es un simulacro deliberado: crear un Space público es una
acción de publicación, y conviene que sea explícita.
"""

import argparse
import sys
from pathlib import Path

from huggingface_hub import HfApi, create_repo, get_token, upload_folder

BASE = Path(__file__).resolve().parent
USUARIO = "diegoevans2-arch"
NOMBRE = "idec-araucania"

# Sólo lo que el Space necesita para ejecutarse.
ARCHIVOS = [
    "app.py",
    "requirements.txt",
    "README.md",
    "modelo_idec.joblib",
    "panel_app.csv",
    "metadatos.json",
]

IGNORAR = ["__pycache__/*", "*.pyc", "__init__.py",
           "exportar_modelo.py", "publicar_space.py"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--publicar", action="store_true",
                    help="ejecuta realmente la creación y la subida")
    ap.add_argument("--privado", action="store_true",
                    help="crea el Space como privado")
    ap.add_argument("--nombre", default=NOMBRE)
    args = ap.parse_args()

    repo_id = f"{USUARIO}/{args.nombre}"
    url = f"https://huggingface.co/spaces/{repo_id}"

    # --- Comprobaciones previas -------------------------------------------
    faltan = [f for f in ARCHIVOS if not (BASE / f).exists()]
    if faltan:
        sys.exit(f"ERROR: faltan archivos en deploy/: {faltan}")

    peso = sum((BASE / f).stat().st_size for f in ARCHIVOS) / 1_048_576
    print(f"Space:      {repo_id}")
    print(f"Visibilidad:{' privado' if args.privado else ' PÚBLICO'}")
    print(f"Archivos:   {len(ARCHIVOS)}  ({peso:.1f} MB)")
    for f in ARCHIVOS:
        print(f"   - {f}  ({(BASE / f).stat().st_size / 1024:.0f} KB)")

    if not get_token():
        sys.exit("\nERROR: no hay sesión iniciada.\n"
                 "Ejecute primero:  huggingface-cli login")
    quien = HfApi().whoami().get("name")
    print(f"\nAutenticado como: {quien}")
    if quien != USUARIO:
        print(f"AVISO: la sesión no corresponde a {USUARIO}")

    if not args.publicar:
        print("\n--- SIMULACRO: no se creó ni subió nada ---")
        print("Para publicar de verdad, añada la opción --publicar")
        return

    # --- Publicación -------------------------------------------------------
    print(f"\nCreando el Space...")
    create_repo(repo_id=repo_id, repo_type="space", space_sdk="gradio",
                private=args.privado, exist_ok=True)

    print("Subiendo archivos...")
    upload_folder(repo_id=repo_id, repo_type="space", folder_path=str(BASE),
                  ignore_patterns=IGNORAR,
                  commit_message="Simulador IDEC — clúster turístico de La Araucanía")

    print(f"\nListo: {url}")
    print("La primera construcción del entorno tarda unos minutos.")


if __name__ == "__main__":
    main()
