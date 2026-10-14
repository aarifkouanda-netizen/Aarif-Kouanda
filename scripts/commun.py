"""Fonctions de montage partagées, reprises telles quelles de montage_v2.py.

montage_v2.py reste inchangé (il produit la V2 livrée) ; les versions suivantes importent
ce module au lieu de recopier le code.
"""
import os, subprocess
from functools import lru_cache
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1920, 1080, 24; BEAT = 0.5            # 120 BPM : 1 temps = 12 images
GOLD = (249, 168, 0); WHITE = (240, 240, 236); BG = (27, 32, 35)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
N = ROOT + "nuit/"; U = ROOT + "sources/"; P = ROOT + "plaques/"; R = ROOT + "rendus/"
C1 = U + "Ensemble_1_-_2_minutes_-_version_nettoyee.mp4"; C2 = U + "Circuit_complet_-_1_min_30_-_variations_de_vitesse.mp4"
NIGHT = "deband=1thr=0.03:2thr=0.03:3thr=0.03:range=24:blur=1,noise=alls=4:allf=t"
F = os.environ.get("INTER_DIR", "C:/Windows/Fonts/")  # dossier contenant Inter-Bold.otf, Inter-SemiBold.otf…


@lru_cache(maxsize=None)
def font(w, s):
    # Inter statique (Inter-Bold.otf…) si INTER_DIR la fournit, sinon la police variable du projet
    p = F + f"Inter-{w}.otf"
    if os.path.exists(p): return ImageFont.truetype(p, s)
    f = ImageFont.truetype(ROOT + "fonts/InterVariable.ttf", s); f.set_variation_by_name(w); return f


def ease(t): return 0 if t <= 0 else 1 if t >= 1 else 1 - (1 - t) ** 3


def frames(src, ss=0, dur=None, vf=""):
    cmd = ["ffmpeg", "-v", "error"] + (["-ss", str(ss)] if ss else []) + ["-i", src]
    f = (vf + "," if vf else "") + f"scale={W}:{H}:flags=lanczos,fps={FPS},format=rgb24"
    cmd += ["-vf", f] + (["-t", str(dur)] if dur else []) + ["-f", "rawvideo", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE); n = 0; last = None
    while True:
        b = p.stdout.read(W * H * 3)
        if len(b) < W * H * 3: break
        last = Image.frombytes("RGB", (W, H), b); n += 1; yield last
    # complète si la source est un peu courte
    if dur and last is not None:
        for _ in range(int(round(dur * FPS)) - n): yield last


y, x = np.ogrid[:H, :W]; VIG = np.clip(1 - 0.22 * np.clip(np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2) - 0.6, 0, 1) ** 1.5, 0, 1)[..., None]


def grade(im, sat=1.0):
    a = np.asarray(im).astype(np.float32) / 255
    if sat != 1.0:
        g = a.mean(axis=2, keepdims=True); a = g + (a - g) * sat
    a = 0.03 + a * VIG * 0.97
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).convert("RGBA")


def txt(img, xy, s, f, col, a=1.0, anchor="la"):
    o = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(o).text(xy, s, font=f, fill=col + (int(255 * max(0, min(1, a))),), anchor=anchor)
    img.alpha_composite(o)


def word(img, t, t0, t1, s, size=150, col=WHITE, y=540):
    # mot posé sur le temps : arrive en 4 images, part net à t1 (pas de fondu)
    if not (t0 <= t < t1): return
    k = ease((t - t0) / (4 / FPS)); f = font("Bold", size)
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).text((W / 2, y + 3), s, font=f, fill=(0, 0, 0, int(150 * k)), anchor="mm")
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
    txt(img, (W / 2, y + (1 - k) * 24), s, f, col, k, "mm")


def rect(cx, cy, w):
    h = w * 9 / 16; x0 = min(max(cx - w / 2, 0), W - w); y0 = min(max(cy - h / 2, 0), H - h); return (x0, y0, w)


def brightest(im, top_frac):
    """Position du point le plus lumineux dans la partie haute de l'image (tête LED)."""
    L = np.asarray(im.convert("L").filter(ImageFilter.GaussianBlur(6))).astype(float); L[int(H * top_frac):] = 0
    hy, hx = np.unravel_index(L.argmax(), L.shape); return (int(hx), int(hy))
