"""Séquence 2 de l'ouverture : les circuits (9,0 s, 216 images), dans la continuité du globe.

  0,0 s        image 0 = dernière image du globe (rendus/ouverture_globe_derniere.png)
  0,0–0,5 s    une fenêtre ronde s'ouvre sur Ouagadougou autour du point or ; la vue satellite
               glisse jusqu'au cadre qui montre les deux circuits
  0,5–3,5 s    circuit 1 dessiné à vitesse constante (« CIRCUIT 1 » dès 0,5 s, « · 7,2 km » à 3,5 s)
  3,5–6,5 s    circuit 2 : l'avenue nord, puis l'anneau dans les deux sens, les autres avenues partant
               de l'anneau quand il les atteint (« CIRCUIT 2 » dès 3,5 s, « · 4,2 km » à 6,5 s)
  7,0–9,0 s    le total « 11,4 km » et « D'AVENUES ÉCLAIRÉES »
Longueurs lues dans chiffres_circuits.json ; géométrie dans circuits/ (voir circuits.py) ; fond
satellite calé par caler_fond.py. Tous les événements tombent sur un multiple de 12 images.

usage: python ouverture/render_circuits.py [--apercu] [--fond fonds/NOM.jpg]
  --apercu : seulement la planche (une image par temps) et la dernière image, pas de vidéo
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from circuits import circuit1, circuit2_parts, to_ll, to_m  # noqa: E402

W, H, FPS, N = 1920, 1080, 24, 216
SS = 2                                           # tracés dessinés à 2x puis réduits (anticrénelage)
GOLD, WHITE, ANTH = (249, 168, 0), (240, 240, 236), (56, 62, 66)
OUAGA = np.array([-1.5197, 12.3714])             # le point du globe (globe.html)
MARGE_M = 450                                    # marge autour des deux circuits, en mètres
OUT = ROOT / "rendus"
apercu = "--apercu" in sys.argv
fond = ROOT / (sys.argv[sys.argv.index("--fond") + 1] if "--fond" in sys.argv else "fonds/ouaga_deux_circuits_1024.jpg")
emp = json.loads(fond.with_suffix(".json").read_text(encoding="utf-8"))
chiffres = json.loads((ROOT / "chiffres_circuits.json").read_text(encoding="utf-8"))
km = lambda v: f"{v:.1f}".replace(".", ",")


def frame_of(t): return round(t * FPS)
T_OPEN, T_C1, T_C2, T_END2, T_TOTAL = 0, frame_of(0.5), frame_of(3.5), frame_of(6.5), frame_of(7.0)
for f in (T_C1, T_C2, T_END2, T_TOTAL):
    assert f % 12 == 0, f"événement hors grille : image {f}"


def font(w, s):
    f = ImageFont.truetype(str(ROOT / "fonts" / "InterVariable.ttf"), s); f.set_variation_by_name(w); return f


# ---------- cadre : les deux circuits entiers, centrés, avec une marge
c1 = circuit1()[0]; p2 = circuit2_parts()
allm = to_m(np.concatenate([c1] + list(p2["avenues"].values())))
r_m = p2["rayon_m"]; cm2 = to_m(p2["centre"][None])[0]
lo = np.minimum(allm.min(0), cm2 - r_m) - MARGE_M; hi = np.maximum(allm.max(0), cm2 + r_m) + MARGE_M
S = min(W / (hi[0] - lo[0]), H / (hi[1] - lo[1]))     # pixels par mètre
CEN = (lo + hi) / 2


def scr(ll, off=(0.0, 0.0)):
    m = to_m(np.atleast_2d(ll))
    return np.c_[W / 2 + (m[:, 0] - CEN[0]) * S + off[0], H / 2 - (m[:, 1] - CEN[1]) * S + off[1]]


# ---------- fond satellite : traitement de plan7 (moyenne, contraste et saturation mesurés sur plan7)
raw = np.asarray(Image.open(fond).convert("RGB")).astype(np.float32)
g = raw.mean(axis=2, keepdims=True); a = g + (raw - g) * 0.48
a = np.array([74.0, 68.9, 60.4]) + (a - a.reshape(-1, 3).mean(0)) * (18.0 / max(g.std(), 1e-6))
sat = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
(x0, y0), (x1, y1) = scr([[emp["ouest"], emp["nord"]], [emp["est"], emp["sud"]]])
sat = sat.resize((int(round(x1 - x0)), int(round(y1 - y0))), Image.LANCZOS)
SAT_XY = np.array([x0, y0])


def map_layer(off):
    im = Image.new("RGB", (W, H), ANTH)
    im.paste(sat, (int(round(SAT_XY[0] + off[0])), int(round(SAT_XY[1] + off[1]))))
    return im


# ---------- traits : chaque trait est une polyligne avec un départ (en mètres, sur l'horloge du circuit)
def stroke(ll, s0=0.0):
    m = to_m(ll); cum = np.r_[0, np.cumsum(np.hypot(*np.diff(m, axis=0).T))]
    return {"px": scr(ll) * SS, "cum": cum, "s0": s0, "len": float(cum[-1])}


def arc(theta0, theta1, n=180):
    t = np.radians(np.linspace(theta0, theta1, n))
    return to_ll(np.c_[cm2[0] + r_m * np.cos(t), cm2[1] + r_m * np.sin(t)])


C1 = [stroke(c1)]
L1 = C1[0]["len"]
ang = {k: np.degrees(np.arctan2(*(to_m(v[-1:])[0] - cm2)[::-1])) % 360 for k, v in p2["avenues"].items()}
tN = ang["N"]; tO = ang["O"] if ang["O"] > tN else ang["O"] + 360; tS = ang["S"] if ang["S"] > tO else ang["S"] + 360
tE = ang["E"] if ang["E"] < tN else ang["E"] - 360; tS2 = tS - 360       # moitié est : on descend sous tN
LN = stroke(p2["avenues"]["N"])["len"]
C2 = [stroke(p2["avenues"]["N"], 0.0),
      stroke(arc(tN, tS), LN), stroke(arc(tN, tS2), LN),
      stroke(p2["avenues"]["O"][::-1], LN + np.radians(tO - tN) * r_m),
      stroke(p2["avenues"]["E"][::-1], LN + np.radians(tN - tE) * r_m),
      stroke(p2["avenues"]["S"][::-1], LN + np.radians(max(tS - tN, tN - tS2)) * r_m)]
L2 = max(s["s0"] + s["len"] for s in C2)
LW, HEAD = 6 * SS, 6 * SS


def draw_strokes(d, strokes, s, heads):
    for st in strokes:
        k = s - st["s0"]
        if k <= 0: continue
        k = min(k, st["len"]); px, cum = st["px"], st["cum"]
        i = int(np.searchsorted(cum, k, side="right"))
        pts = px[:i]
        if i < len(px):
            u = (k - cum[i - 1]) / (cum[i] - cum[i - 1]); pts = np.r_[pts, [px[i - 1] + (px[i] - px[i - 1]) * u]]
        d.line([tuple(p) for p in pts], fill=GOLD + (255,), width=LW, joint="curve")
        for p in (pts[0], pts[-1]):
            d.ellipse([p[0] - LW / 2, p[1] - LW / 2, p[0] + LW / 2, p[1] + LW / 2], fill=GOLD + (255,))
        if heads and k < st["len"]:
            p = pts[-1]; d.ellipse([p[0] - HEAD, p[1] - HEAD, p[0] + HEAD, p[1] + HEAD], fill=WHITE + (255,))


def traces(n):
    lay = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    if n >= T_C1: draw_strokes(d, C1, L1 * min(1, (n - T_C1) / (T_C2 - T_C1)), n < T_C2)
    if n >= T_C2: draw_strokes(d, C2, L2 * min(1, (n - T_C2) / (T_END2 - T_C2)), n < T_END2)
    return lay.resize((W, H), Image.LANCZOS)


# ---------- texte : capitales espacées (comme le globe), arrivée par glissement de 24 px en 4 images
def slide(n, n0): return 24 * (1 - (1 - min(1, (n - n0) / 4)) ** 3)


def tracked(d, x, y, s, f, fill, track=0.06):
    for ch in s:
        d.text((x, y), ch, font=f, fill=fill, anchor="ls"); x += f.getlength(ch) + track * f.size
    return x


def width_of(s, f, track=0.06): return sum(f.getlength(ch) + track * f.size for ch in s)


F_LAB, F_TOT, F_SUB, F_CRED = font("SemiBold", 40), font("Bold", 150), font("SemiBold", 40), font("Regular", 14)
full = traces(N - 1)                                          # tracés complets : pour placer les textes
end1 = scr(c1[-1])[0]; endE = scr(p2["avenues"]["E"][0])[0]
LAB1 = (end1[0] - width_of(f"CIRCUIT 1 · {km(chiffres['circuit_1']['longueur_km'])} km", F_LAB), end1[1] + 62)
LAB2 = (endE[0] + 34, endE[1] + 14)
TOT = (W * 0.62, H * 0.50)


def texts(im, n):
    d = ImageDraw.Draw(im)
    if n >= T_C1:
        x = tracked(d, LAB1[0], LAB1[1] - slide(n, T_C1) + 24, "CIRCUIT 1", F_LAB, WHITE)
        if n >= T_C2: tracked(d, x, LAB1[1] - slide(n, T_C2) + 24, f" · {km(chiffres['circuit_1']['longueur_km'])} km", F_LAB, GOLD)
    if n >= T_C2:
        x = tracked(d, LAB2[0], LAB2[1] - slide(n, T_C2) + 24, "CIRCUIT 2", F_LAB, WHITE)
        if n >= T_END2: tracked(d, x, LAB2[1] - slide(n, T_END2) + 24, f" · {km(chiffres['circuit_2']['longueur_km'])} km", F_LAB, GOLD)
    if n >= T_TOTAL:
        dy = -slide(n, T_TOTAL) + 24
        x = tracked(d, TOT[0], TOT[1] + dy, km(chiffres["total_km"]), F_TOT, GOLD, 0.0)
        tracked(d, x + 18, TOT[1] + dy, "km", font("SemiBold", 64), GOLD, 0.0)
        tracked(d, TOT[0] + 6, TOT[1] + 64 + dy, "D'AVENUES ÉCLAIRÉES", F_SUB, WHITE)
    if n >= 1:                                                # l'image 0 doit rester celle du globe
        o = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(o).text((W - 24, H - 20), "Imagery © Google, Airbus", font=F_CRED, fill=WHITE + (153,), anchor="rs")
        im.alpha_composite(o)


# ---------- ouverture de la fenêtre (images 0 à 11)
globe_last = Image.open(OUT / "ouverture_globe_derniere.png").convert("RGB")
assert globe_last.size == (W, H)
P_END = scr(OUAGA)[0]; OFF0 = np.array([W / 2, H / 2]) - P_END
R_COVER = max(np.hypot(*(P_END - c)) for c in [(0, 0), (W, 0), (0, H), (W, H)]) + 4
yy, xx = np.mgrid[0:H, 0:W]
ease_io = lambda k: 4 * k ** 3 if k < 0.5 else 1 - (-2 * k + 2) ** 3 / 2

STATIC = map_layer((0.0, 0.0)).convert("RGBA")


def frame(n):
    if n == 0:
        return globe_last.copy().convert("RGBA")
    if n < T_C1:
        k = n / T_C1; off = OFF0 * (1 - ease_io(k)); c = P_END + off
        r = 9 + (R_COVER - 9) * k ** 2.2
        alpha = np.clip(r - np.hypot(xx - c[0], yy - c[1]) + 0.5, 0, 1)
        mask = Image.fromarray((alpha * 255).astype(np.uint8))
        im = globe_last.copy(); im.paste(map_layer(off), (0, 0), mask); im = im.convert("RGBA")
        d = ImageDraw.Draw(im); d.ellipse([c[0] - 9, c[1] - 9, c[0] + 9, c[1] + 9], fill=GOLD)   # le point reste sur Ouagadougou
    else:
        im = STATIC.copy(); im.alpha_composite(traces(n))
    texts(im, n)
    return im


# ---------- contrôle : aucun texte ne chevauche un tracé (tracés élargis de 10 px)
last = frame(N - 1)
trace_mask = np.asarray(full.split()[3].filter(ImageFilter.MaxFilter(21))) > 0
txt_only = Image.new("RGBA", (W, H), (0, 0, 0, 0)); texts(txt_only, N - 1)
txt_mask = np.asarray(txt_only.split()[3]) > 0
txt_mask[H - 60:, W - 400:] = False                           # la mention Google est hors du cadre utile
inside = (0 <= LAB1[0]) and (LAB2[0] + width_of("CIRCUIT 2 · 4,2 km", F_LAB) < W)
print(f"cadre : {1 / S:.2f} m par pixel ; fenêtre ouverte sur le point ({P_END[0]:.0f}, {P_END[1]:.0f})")
print(f"longueurs : circuit 1 {L1 / 1000:.2f} km en 3 s ; circuit 2, chemin le plus long {L2 / 1000:.2f} km en 3 s")
print(f"chevauchement texte / tracé : {int((trace_mask & txt_mask).sum())} pixels ; textes dans le cadre : {inside}")
print(f"satellite à l'écran : x {SAT_XY[0]:.0f} à {SAT_XY[0] + sat.width:.0f}, y {SAT_XY[1]:.0f} à {SAT_XY[1] + sat.height:.0f} "
      f"(échelle x{sat.width / emp['largeur_px']:.2f} par rapport à la capture)")

OUT.mkdir(exist_ok=True)
enc = None if apercu else subprocess.Popen(
    ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
     "-vf", "setsar=1", "-c:v", "libx264", "-crf", "14", "-preset", "slow", "-pix_fmt", "yuv420p",
     "-frames:v", str(N), str(OUT / "ouverture_circuits.mp4")], stdin=subprocess.PIPE)
board = []
for n in range(N):
    if apercu and n % 12 and n != N - 1:
        continue
    im = (last if n == N - 1 else frame(n)).convert("RGB")
    if enc: enc.stdin.write(im.tobytes())
    if n % 12 == 0 or n == N - 1: board.append((n, im))
if enc:
    enc.stdin.close(); enc.wait()
last.convert("RGB").save(OUT / "ouverture_circuits_derniere.png")
diff = np.abs(np.asarray(board[0][1]).astype(int) - np.asarray(globe_last).astype(int)).max()
print(f"raccord : écart max entre l'image 0 et la dernière image du globe = {diff}")

cols, tw, th = 4, 480, 270
sheet = Image.new("RGB", (cols * tw, ((len(board) + cols - 1) // cols) * th), (20, 20, 20))
for i, (n, im) in enumerate(board):
    v = im.resize((tw, th), Image.LANCZOS); ImageDraw.Draw(v).text((8, 6), f"image {n} · {n / FPS:.2f} s", fill=(255, 220, 0))
    sheet.paste(v, ((i % cols) * tw, (i // cols) * th))
sheet.save(OUT / "ouverture_circuits_planche.jpg", quality=90)
print(f"planche : {OUT / 'ouverture_circuits_planche.jpg'} ({len(board)} vignettes)")

# la fenêtre s'ouvre entre deux temps : planche à part, une vignette par image de 0 à 12
strip = Image.new("RGB", (cols * tw, 4 * th), (20, 20, 20))
for i, n in enumerate(range(0, T_C1 + 1)):
    if i >= 16: break
    v = frame(n).convert("RGB").resize((tw, th), Image.LANCZOS)
    ImageDraw.Draw(v).text((8, 6), f"image {n} · {n / FPS:.2f} s", fill=(255, 220, 0))
    strip.paste(v, ((i % cols) * tw, (i // cols) * th))
strip.save(OUT / "ouverture_circuits_fenetre.jpg", quality=90)
print(f"planche de la fenêtre : {OUT / 'ouverture_circuits_fenetre.jpg'}")
