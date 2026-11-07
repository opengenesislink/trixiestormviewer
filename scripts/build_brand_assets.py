#!/usr/bin/env python3
"""Generate TrixieStorm viewer runtime icons from the project-supplied logo.

Keep the exact artwork (when PNG provided); use WebP as a compact tracked
copy when the full-resolution master cannot be stored in Git. Never generate
Firestorm/Second Life branding. Requires Pillow.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "branding/source/trixiestorm-logo.png"
COMPACT = ROOT / "branding/source/trixiestorm-logo.webp"
SIZES = (16, 32, 48, 64, 128, 256, 512)

def output(image, path, size, fmt="PNG"):
    path.parent.mkdir(parents=True, exist_ok=True)
    img = image.resize((size, size), Image.Resampling.LANCZOS)
    if fmt == "BMP":
        img.convert("RGB").save(path, format="BMP")
    else:
        img.save(path, format="PNG", optimize=True)
    print(path.relative_to(ROOT))

def main():
    src = MASTER if MASTER.exists() else COMPACT
    if not src.exists():
        raise SystemExit("Missing branding/source/trixiestorm-logo.png or .webp")
    with Image.open(src) as opened:
        image = opened.convert("RGBA")
        dest = ROOT / "branding/generated"
        for size in SIZES:
            output(image, dest / f"trixiestormviewer-{size}.png", size)
        ico = ROOT / "indra/newview/res/trixiestormviewer.ico"
        ico.parent.mkdir(parents=True, exist_ok=True)
        image.resize((256,256), Image.Resampling.LANCZOS).save(
            ico, "ICO", sizes=[(16,16),(24,24),(32,32),(48,48),
                              (64,64),(128,128),(256,256)])
        print(ico.relative_to(ROOT))
        output(image, ROOT / "indra/newview/res/trixiestormviewer.png", 256)
        output(image, ROOT / "indra/newview/res-sdl/trixiestormviewer.BMP", 256, "BMP")
        output(image, ROOT / "indra/newview/skins/default/textures/windows/trixiestorm_login.png", 256)
        # Login/UI use texture IDs but these are our actual pixels.
        for flavor in ("release-os", "beta-os", "private-os"):
            output(image, ROOT / f"indra/newview/icons/{flavor}/trixiestorm_256.png", 256)
        mac_icon = ROOT / "indra/newview/trixiestormviewer.icns"
        try:
            image.resize((512,512), Image.Resampling.LANCZOS).save(mac_icon, format="ICNS")
            print(mac_icon.relative_to(ROOT))
        except Exception as exc:
            print("Optional macOS ICNS generation unavailable:", exc)

if __name__ == "__main__":
    main()
