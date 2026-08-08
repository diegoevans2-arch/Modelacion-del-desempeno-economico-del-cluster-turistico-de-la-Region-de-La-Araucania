"""Crea el Static Space en Hugging Face y sube la aplicación.

Requiere sesión iniciada:  hf auth login

Uso, desde la raíz del repositorio:
    python deploy_static/publicar.py               # simulacro
    python deploy_static/publicar.py --publicar    # crea y sube
"""

import argparse
import sys
from pathlib import Path

from huggingface_hub import HfApi, create_repo, get_token, upload_folder

BASE = Path(__file__).resolve().parent
USUARIO = "diegoevans2-arch"
NOMBRE = "idec-araucania"

ARCHIVOS = ["index.html", "datos.json", "README.md"]
IGNORAR = ["__pycache__/*", "*.pyc", "__init__.py", "generar_datos.py", "publicar.py"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--publicar", action="store_true")
    ap.add_argument("--privado", action="store_true")
    ap.add_argument("--nombre", default=NOMBRE)
    args = ap.parse_args()

    repo_id = f"{USUARIO}/{args.nombre}"
    url = f"https://huggingface.co/spaces/{repo_id}"

    faltan = [f for f in ARCHIVOS if not (BASE / f).exists()]
    if faltan:
        sys.exit(f"ERROR: faltan archivos: {faltan}")

    print(f"Space:       {repo_id}")
    print(f"SDK:         static")
    print(f"Visibilidad: {'privado' if args.privado else 'PÚBLICO'}")
    for f in ARCHIVOS:
        print(f"   - {f}  ({(BASE / f).stat().st_size / 1024:.1f} KB)")

    if not get_token():
        sys.exit("\nERROR: sin sesión. Ejecute:  hf auth login")
    quien = HfApi().whoami().get("name")
    print(f"\nAutenticado como: {quien}")

    if not args.publicar:
        print("\n--- SIMULACRO: no se creó ni subió nada ---")
        return

    print("\nCreando el Space...")
    create_repo(repo_id=repo_id, repo_type="space", space_sdk="static",
                private=args.privado, exist_ok=True)

    print("Subiendo archivos...")
    upload_folder(repo_id=repo_id, repo_type="space", folder_path=str(BASE),
                  ignore_patterns=IGNORAR,
                  commit_message="Simulador IDEC — clúster turístico de La Araucanía")

    print(f"\nListo: {url}")


if __name__ == "__main__":
    main()
