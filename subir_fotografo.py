"""Sube las fotos del fotógrafo a la carpeta "oficial" del álbum (Supabase Storage).

Reduce cada foto a 2400 px por lado (JPEG calidad 85) para que el plan gratis de
Supabase (1 GB) alcance, y las sube en orden de nombre.

Uso:
    pip install pillow requests
    set SUPABASE_URL=https://xxxx.supabase.co          (Windows; en Mac/Linux: export ...)
    set SUPABASE_SECRET_KEY=sb_secret_...               (clave SECRETA: no la compartas ni la pongas en la invitación)
    python subir_fotografo.py "C:/ruta/a/fotos_fotografo"
"""
import io
import os
import sys
from pathlib import Path

import requests
from PIL import Image, ImageOps

URL = os.environ["SUPABASE_URL"].rstrip("/")
KEY = os.environ["SUPABASE_SECRET_KEY"]
BUCKET, CARPETA, LADO_MAX, CALIDAD = "album", "oficial", 2400, 85
EXT = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"}

headers = {"apikey": KEY}
if not KEY.startswith("sb_"):  # claves antiguas (JWT service_role)
    headers["Authorization"] = f"Bearer {KEY}"


def preparar(ruta: Path) -> bytes:
    with Image.open(ruta) as im:
        im = ImageOps.exif_transpose(im).convert("RGB")
        im.thumbnail((LADO_MAX, LADO_MAX), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=CALIDAD, optimize=True, progressive=True)
        return buf.getvalue()


def main(carpeta: str) -> None:
    fotos = sorted(p for p in Path(carpeta).iterdir() if p.suffix.lower() in EXT)
    if not fotos:
        sys.exit("No encontré fotos en esa carpeta.")
    total_mb = 0.0
    for i, p in enumerate(fotos, 1):
        data = preparar(p)
        destino = f"{CARPETA}/{i:04d}-{p.stem}.jpg"
        r = requests.post(
            f"{URL}/storage/v1/object/{BUCKET}/{destino}",
            headers={**headers, "Content-Type": "image/jpeg", "x-upsert": "true"},
            data=data,
            timeout=120,
        )
        estado = "ok" if r.ok else f"ERROR {r.status_code}: {r.text[:120]}"
        total_mb += len(data) / 1e6
        print(f"[{i}/{len(fotos)}] {p.name} -> {destino} ({len(data) / 1e6:.1f} MB) {estado}")
    print(f"Listo. Subidos ~{total_mb:.0f} MB.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
