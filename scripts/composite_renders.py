#!/usr/bin/env python3
"""Lay the real Nanhe labels onto the blank-label AI product shots.

AI image models garble label text, so the product shots were generated with
blank packs. This script overlays the actual vector label and character from
scripts/build_packaging.py, using a multiply blend so the photo's own light
and shadow show through the print, then renders each composite with headless
Chrome.

Inputs:  assets/renders/ai-0X-*-plain.jpg
Outputs: assets/renders/ai-0X-*-labelled.jpg
Needs:   Google Chrome installed at the default macOS path, and `sips` (macOS).
Run:     python3 scripts/composite_renders.py
"""
import pathlib
import subprocess
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_packaging as bp  # noqa: E402

ROOT = bp.ROOT
RENDERS = ROOT / "assets/renders"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FONTS = ("https://fonts.googleapis.com/css2?family=Baloo+2:wght@600&family=Figtree:wght@500;700"
         "&family=Fraunces:opsz,wght,SOFT@9..144,500,100&display=swap")

# Placement measured on each base photo, in image pixels.
# kind: which label layout; (x, y) top-left of the label box; s: scale from label units to pixels.
SHOTS = [
    {"base": "ai-06-lotion-plain.jpg", "out": "ai-06-lotion-labelled.jpg", "slug": "daily-lotion",
     "w": 1024, "h": 1536, "kind": "tall", "x": 330, "y": 545, "s": 3.4},
    {"base": "ai-07-rash-cream-plain.jpg", "out": "ai-07-rash-cream-labelled.jpg", "slug": "diaper-rash-cream",
     "w": 1024, "h": 1536, "kind": "tall", "x": 362, "y": 262, "s": 2.98},
    {"base": "ai-08-wipes-plain.jpg", "out": "ai-08-wipes-labelled.jpg", "slug": "water-wipes",
     "w": 1536, "h": 1024, "kind": "wide", "x": 345, "y": 372, "s": 2.4,
     # Susu goes on the lid, centred on it
     "extra": {"cx": 942, "cy": 488, "size": 250}},
    {"base": "ai-09-diapers-plain.jpg", "out": "ai-09-diapers-labelled.jpg", "slug": "taped-diapers-nb",
     "w": 1536, "h": 1024, "kind": "bag", "x": 385, "y": 300, "s": 1.65,
     "more": [{"slug": "diaper-pants-m", "kind": "bag", "x": 830, "y": 300, "s": 1.65}]},
]

SIZES = {"tall": (100, 150), "wide": (160, 90), "bag": (200, 250)}


def overlay(pr, p, kind, x, y, s):
    label = {"tall": bp.label_tall, "wide": bp.label_wide, "bag": bp.label_bag}[kind](pr, p)
    lw, lh = SIZES[kind]
    return (f'<svg class="ov" style="left:{x}px;top:{y}px;width:{lw * s}px;height:{lh * s}px" '
            f'viewBox="0 0 {lw} {lh}">{label}</svg>')


def page(shot):
    pr = bp.BY_SLUG[shot["slug"]]
    p = "c-"
    labels = overlay(pr, p, shot["kind"], shot["x"], shot["y"], shot["s"]) + "".join(
        overlay(bp.BY_SLUG[m["slug"]], p, m["kind"], m["x"], m["y"], m["s"]) for m in shot.get("more", []))
    extra = ""
    if "extra" in shot:
        e = shot["extra"]
        extra = (f'<svg class="ov" style="left:{e["cx"] - e["size"] / 2}px;top:{e["cy"] - e["size"] / 2}px;'
                 f'width:{e["size"]}px;height:{e["size"]}px" viewBox="0 0 60 60"><use href="#{p}ch-{shot["slug"]}"/></svg>')
    base = (RENDERS / shot["base"]).as_uri()
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="{FONTS}">
<style>html,body{{margin:0;width:{shot['w']}px;height:{shot['h']}px;overflow:hidden}}
.wrap{{position:relative;width:{shot['w']}px;height:{shot['h']}px}}
.wrap img{{position:absolute;inset:0;width:100%;height:100%}}
.ov{{position:absolute;mix-blend-mode:multiply;opacity:.96}}</style></head>
<body><div class="wrap"><img src="{base}">
<svg width="0" height="0" style="position:absolute"><defs>{bp.defs(p)}</defs></svg>
{labels}
{extra}</div></body></html>"""


def main():
    with tempfile.TemporaryDirectory() as tmp:
        for shot in SHOTS:
            html = pathlib.Path(tmp) / (shot["out"] + ".html")
            png = pathlib.Path(tmp) / (shot["out"] + ".png")
            html.write_text(page(shot))
            subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                            "--force-device-scale-factor=1", "--allow-file-access-from-files",
                            "--virtual-time-budget=6000", f"--window-size={shot['w']},{shot['h']}",
                            f"--screenshot={png}", html.as_uri()],
                           check=True, capture_output=True)
            subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "90", str(png),
                            "--out", str(RENDERS / shot["out"])], check=True, capture_output=True)
            print("wrote", shot["out"])


if __name__ == "__main__":
    main()
