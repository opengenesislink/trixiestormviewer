#!/usr/bin/env python3
"""Generate platform application icons from the project-supplied TrixieStorm logo."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "branding/source/trixiestorm-logo.png"
TARGET = ROOT / "branding/generated"
SIZES = (16, 32, 48, 64, 128, 256, 512)

def main():
    if not SOURCE.is_file():
        raise SystemExit(f"Missing original graphic: {SOURCE}\nPlace the supplied project image there first.")
    TARGET.mkdir(parents=True, exist_ok=True)
    with Image.open(SOURCE) as src:
        src = src.convert("RGBA")
        for size in SIZES:
            icon = src.resize((size, size), Image.Resampling.LANCZOS)
            path = TARGET / f"trixiestormviewer-{size}.png"
            icon.save(path, optimize=True)
            print(path.relative_to(ROOT))
        # Windows ICO contains multiple native resolutions, including 256px PNG.
        ico_path = TARGET / "trixiestormviewer.ico"
        src.resize((256, 256), Image.Resampling.LANCZOS).save(
            ico_path, format="ICO", sizes=[(16,16), (24,24), (32,32), (48,48), (64,64), (128,128), (256,256)]
        )
        print(ico_path.relative_to(ROOT))

if __name__ == "__main__":
    main()
