"""Séquence 1 de l'ouverture : globe -> Burkina Faso -> Ouagadougou (6,0 s, 144 images).

globe.html calcule chaque image à partir du temps (seek(t)) ; Playwright la photographie,
ffmpeg encode. Sorties dans rendus/ : ouverture_globe.mp4 et la planche d'aperçu (une image
par temps, toutes les 12 images).

usage: python ouverture/render_globe.py [--apercu]   (--apercu : seulement la planche)
"""
import base64
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
NM = HERE / "node_modules"
OUT = ROOT / "rendus"
W, H, FPS, N = 1920, 1080, 24, 144
apercu_only = "--apercu" in sys.argv

OUT.mkdir(exist_ok=True)
font_b64 = base64.b64encode((ROOT / "fonts" / "InterVariable.ttf").read_bytes()).decode()
w110 = json.loads((NM / "world-atlas" / "countries-110m.json").read_text(encoding="utf-8"))
w50 = json.loads((NM / "world-atlas" / "countries-50m.json").read_text(encoding="utf-8"))

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
    page.goto((HERE / "globe.html").as_uri())
    for lib in ("d3-array/dist/d3-array.min.js", "d3-geo/dist/d3-geo.min.js", "topojson-client/dist/topojson-client.min.js"):
        page.add_script_tag(path=str(NM / lib))
    page.add_style_tag(content="@font-face{font-family:Inter;font-weight:100 900;"
                               f"src:url(data:font/ttf;base64,{font_b64}) format('truetype');}}")
    ok = page.evaluate("""async () => { await document.fonts.load('600 44px Inter');
                                         return document.fonts.check('600 44px Inter'); }""")
    if not ok:
        raise SystemExit("Inter ne s'est pas chargée : rendu arrêté (sinon le texte sortirait dans une autre police)")
    page.evaluate("([a, b]) => init(a, b)", [w110, w50])

    enc = None
    if not apercu_only:
        enc = subprocess.Popen(
            ["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "png", "-i", "-",
             "-vf", "format=yuv420p,setsar=1", "-c:v", "libx264", "-crf", "14", "-preset", "slow",
             "-pix_fmt", "yuv420p", "-frames:v", str(N), str(OUT / "ouverture_globe.mp4")],
            stdin=subprocess.PIPE)
    board, dots = [], {}
    for n in range(N):
        if apercu_only and n % 12 and n != N - 1:
            continue
        info = page.evaluate(f"seek({n}/{FPS})")
        png = page.screenshot(type="png")
        if enc:
            enc.stdin.write(png)
        if n % 12 == 0 or n == N - 1:
            (OUT / "apercus").mkdir(exist_ok=True)
            p = OUT / "apercus" / f"globe_{n:03d}.png"
            p.write_bytes(png)
            board.append((n, p))
        if n >= 120:
            dots[n] = info["dot"]
        if n == N - 1:
            (OUT / "ouverture_globe_derniere.png").write_bytes(png)    # for the seam with sequence 2
    if enc:
        enc.stdin.close()
        enc.wait()
    browser.close()

# planche : une vignette par temps
cols, tw, th = 4, 480, 270
rows = (len(board) + cols - 1) // cols
sheet = Image.new("RGB", (cols * tw, rows * th), (20, 20, 20))
from PIL import ImageDraw
for i, (n, p) in enumerate(board):
    im = Image.open(p).convert("RGB").resize((tw, th), Image.LANCZOS)
    ImageDraw.Draw(im).text((8, 6), f"image {n} · {n / FPS:.2f} s", fill=(255, 220, 0))
    sheet.paste(im, ((i % cols) * tw, (i // cols) * th))
sheet.save(OUT / "ouverture_globe_planche.jpg", quality=90)
off = max(max(abs(x - 960), abs(y - 540)) for x, y in dots.values()) if dots else None
print(f"planche : {OUT / 'ouverture_globe_planche.jpg'}  ({len(board)} vignettes)")
print(f"point sur Ouagadougou, écart max au centre (960,540) entre les images 120 et 143 : {off:.3f} px")
