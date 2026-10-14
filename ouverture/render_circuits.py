"""Séquence 2 de l'ouverture : les circuits (9,0 s, 216 images), dans la continuité du globe. Version V4 :
la caméra suit la lumière.

  0,0 s        image 0 = dernière image du globe (rendus/ouverture_globe_derniere.png)
  0,0–0,5 s    une fenêtre ronde s'ouvre autour du point or, qui reste au centre sur Ouagadougou (lente
               poussée) ; le départ du circuit 1 est déjà dans le cadre
  0,5–3,0 s    circuit 1 dessiné à vitesse constante, le cadre l'accompagne et recule pour le montrer
               en entier ; « CIRCUIT 1 » dès 0,5 s, « · 7,2 km » à 3,0 s
  3,5–4,0 s    glissé rapide vers le sud (léger recul en route), flou de mouvement
  4,0–6,0 s    circuit 2 sur le rond-point : avenue nord, anneau dans les deux sens, autres avenues ;
               « CIRCUIT 2 » à 4,0 s, « · 4,2 km » à 6,0 s
  6,5–7,0 s    recul sur les deux circuits ; 7,0 s : « 11,4 km D'AVENUES ÉCLAIRÉES » (jusqu'à 8,5 s)
  8,5–9,0 s    plongée qui accélère vers le départ du circuit 1, coupée à pleine vitesse sur le rush de jour
Longueurs lues dans chiffres_circuits.json ; géométrie dans circuits/ (voir circuits.py) ; fond
satellite calé par caler_fond.py. Tous les événements tombent sur un multiple de 12 images.

usage: python ouverture/render_circuits.py [--apercu] [--fond fonds/NOM.jpg]
  --apercu : seulement les planches (une image par temps, et l'ouverture image par image), pas de vidéo
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

Image.MAX_IMAGE_PIXELS = None
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from circuits import KX, KY, circuit1, circuit2_parts, to_ll, to_m  # noqa: E402

W, H, FPS, N = 1920, 1080, 24, 216
SS = 2                                           # tracés dessinés à 2x puis réduits (anticrénelage)
GOLD, WHITE, ANTH = (249, 168, 0), (240, 240, 236), (56, 62, 66)
OUAGA = np.array([-1.5197, 12.3714])             # le point du globe (globe.html)
MARGE_M = 450                                    # marge autour des deux circuits (cadre d'ensemble)
SHUTTER = 0.4                                    # flou de mouvement de la plongée (40 % de l'intervalle) ; 25 % ailleurs
OUT = ROOT / "rendus"
apercu = "--apercu" in sys.argv
fond = ROOT / (sys.argv[sys.argv.index("--fond") + 1] if "--fond" in sys.argv else "fonds/ouaga_large.jpg")
emp = json.loads(fond.with_suffix(".json").read_text(encoding="utf-8"))
chiffres = json.loads((ROOT / "chiffres_circuits.json").read_text(encoding="utf-8"))
km = lambda v: f"{v:.1f}".replace(".", ",")


def frame_of(t): return round(t * FPS)
T_C1, T_C1_END, T_GLIDE, T_C2, T_C2_END, T_BACK, T_TOTAL, T_DIVE = (
    frame_of(x) for x in (0.5, 3.0, 3.5, 4.0, 6.0, 6.5, 7.0, 8.5))
for f in (T_C1, T_C1_END, T_GLIDE, T_C2, T_C2_END, T_BACK, T_TOTAL, T_DIVE):
    assert f % 12 == 0, f"événement hors grille : image {f}"


def font(w, s):
    f = ImageFont.truetype(str(ROOT / "fonts" / "InterVariable.ttf"), s); f.set_variation_by_name(w); return f


# ---------- géométrie (mètres, projection locale de circuits.py)
c1 = circuit1()[0]; p2 = circuit2_parts()
M = lambda ll: to_m(np.atleast_2d(np.asarray(ll, float)))[0]
S1, K1, E1 = M(c1[0]), M(c1[1]), M(c1[-1])                  # départ (côté aéroport), angle, fin (côté CHU)
r_m = p2["rayon_m"]; C2 = to_m(p2["centre"][None])[0]
allm = to_m(np.concatenate([c1] + list(p2["avenues"].values())))
lo = np.minimum(allm.min(0), C2 - r_m) - MARGE_M; hi = np.maximum(allm.max(0), C2 + r_m) + MARGE_M
S0 = min(W / (hi[0] - lo[0]), H / (hi[1] - lo[1]))          # pixels par mètre du cadre d'ensemble (zoom 1)
CEN = (lo + hi) / 2
c1m = to_m(c1); C1C = (c1m.min(0) + c1m.max(0)) / 2         # centre du circuit 1
c2lo = np.minimum(to_m(np.concatenate(list(p2["avenues"].values()))).min(0), C2 - r_m)
c2hi = np.maximum(to_m(np.concatenate(list(p2["avenues"].values()))).max(0), C2 + r_m); C2C = (c2lo + c2hi) / 2
OUAGA_M = M(OUAGA)

# ---------- caméra : clés (temps, centre en mètres, zoom, courbe du segment qui finit à cette clé, creux de zoom)
io = lambda k: 4 * k ** 3 if k < 0.5 else 1 - (-2 * k + 2) ** 3 / 2
ein = lambda k: k ** 3
KEYS = [
    (0.0, OUAGA_M,                                 1.7, None, 0.0),
    (0.5, OUAGA_M,                                 1.9, io,   0.0),   # la fenêtre s'ouvre : le point reste au centre, lente poussée
    (3.0, C1C,                                     2.6, io,   0.0),   # le cadre accompagne le tracé et recule
    (3.5, C1C,                                     2.7, io,   0.0),   # lente poussée pendant « · 7,2 km »
    (4.0, C2C,                                     3.2, io,   0.9),   # glissé vers le sud, recul en route
    (6.5, C2C,                                     3.5, io,   0.0),   # lente poussée sur le rond-point
    (7.0, CEN,                                     1.0, io,   0.0),   # recul sur les deux circuits
    (8.5, CEN + 0.25 * (S1 - CEN),                 1.22, io,  0.0),   # lente poussée vers le départ
    (9.0, S1,                                      8.0, ein,  0.0),   # plongée qui accélère (pic de vitesse à la coupe)
]


def cam(t):
    for (t0, c0, z0, _, _), (t1, c1_, z1, ease, dip) in zip(KEYS[:-1], KEYS[1:]):
        if t <= t1:
            k = ease(min(1, max(0, (t - t0) / (t1 - t0))))
            lz = np.log(z0) + (np.log(z1) - np.log(z0)) * k - dip * np.sin(np.pi * k)
            return c0 + (c1_ - c0) * k, float(np.exp(lz))
    return KEYS[-1][1], KEYS[-1][2]


def proj(m, cm):
    (c, z) = cm; s = S0 * z; m = np.atleast_2d(m)
    return np.c_[W / 2 + (m[:, 0] - c[0]) * s, H / 2 - (m[:, 1] - c[1]) * s]


# ---------- fond satellite : jonctions corrigées, traitement de plan7, pyramide pour les zooms
raw = np.asarray(Image.open(fond).convert("RGB")).astype(np.float32)
for j in emp.get("jonctions", []):
    hh, ww = raw.shape[:2]
    for y0 in range(0, hh, 512):                                # par bandes : la pleine résolution est lourde
        y1 = min(hh, y0 + 512)
        xs = j["x_haut"] + (j["x_bas"] - j["x_haut"]) * np.arange(y0, y1)[:, None] / (hh - 1)
        k = np.clip((np.arange(ww)[None, :] - xs) / j["fondu_px"] + 0.5, 0, 1); k = (k * k * (3 - 2 * k))[..., None]
        mL, mR = np.array(j["moyenne_gauche"], np.float32), np.array(j["moyenne_droite"], np.float32)
        band = raw[y0:y1]
        raw[y0:y1] = band + k * ((band - mR) * np.array(j["contraste_droite"], np.float32) + mL - band)
g = raw.mean(axis=2, keepdims=True); gs = float(g.std())
raw = g + (raw - g) * 0.48; del g
raw = np.array([74.0, 68.9, 60.4], np.float32) + (raw - raw.reshape(-1, 3).mean(0)) * (18.0 / max(gs, 1e-6))
PYR = [Image.fromarray(np.clip(raw, 0, 255).astype(np.uint8))]; del raw
while PYR[-1].width > 1500: PYR.append(PYR[-1].resize((PYR[-1].width // 2, PYR[-1].height // 2), Image.LANCZOS))
FOND_MPP = (emp["est"] - emp["ouest"]) * KX / emp["largeur_px"]  # mètres par pixel du fond


def map_layer(cm):
    (c, z) = cm; s = S0 * z
    lvl = int(np.clip(np.floor(np.log2(max(1.0, (1 / s) / FOND_MPP))), 0, len(PYR) - 1)); im = PYR[lvl]
    kxx = im.width / ((emp["est"] - emp["ouest"]) * KX); kx0 = emp["ouest"] * im.width / (emp["est"] - emp["ouest"])
    kyy = im.height / ((emp["nord"] - emp["sud"]) * KY); ky0 = emp["nord"] * im.height / (emp["nord"] - emp["sud"])
    a = kxx / s; c0 = kxx * (c[0] - W / (2 * s)) - kx0
    e = kyy / s; f0 = ky0 - kyy * c[1] - kyy * H / (2 * s)
    return im.transform((W, H), Image.AFFINE, (a, 0, c0, 0, e, f0), resample=Image.BICUBIC, fillcolor=ANTH)


# ---------- traits : polylignes en mètres, avec un départ sur l'horloge du circuit (mètres parcourus)
def stroke(ll, s0=0.0):
    m = to_m(ll); cum = np.r_[0, np.cumsum(np.hypot(*np.diff(m, axis=0).T))]
    return {"m": m, "cum": cum, "s0": s0, "len": float(cum[-1])}


def arc(theta0, theta1, n=180):
    t = np.radians(np.linspace(theta0, theta1, n))
    return to_ll(np.c_[C2[0] + r_m * np.cos(t), C2[1] + r_m * np.sin(t)])


ST1 = [stroke(c1)]; L1 = ST1[0]["len"]
ang = {k: np.degrees(np.arctan2(*(to_m(v[-1:])[0] - C2)[::-1])) % 360 for k, v in p2["avenues"].items()}
tN = ang["N"]; tO = ang["O"] if ang["O"] > tN else ang["O"] + 360; tS = ang["S"] if ang["S"] > tO else ang["S"] + 360
tE = ang["E"] if ang["E"] < tN else ang["E"] - 360; tS2 = tS - 360
LN = stroke(p2["avenues"]["N"])["len"]
ST2 = [stroke(p2["avenues"]["N"], 0.0), stroke(arc(tN, tS), LN), stroke(arc(tN, tS2), LN),
       stroke(p2["avenues"]["O"][::-1], LN + np.radians(tO - tN) * r_m),
       stroke(p2["avenues"]["E"][::-1], LN + np.radians(tN - tE) * r_m),
       stroke(p2["avenues"]["S"][::-1], LN + np.radians(max(tS - tN, tN - tS2)) * r_m)]
L2 = max(s["s0"] + s["len"] for s in ST2)
LW, HEAD = 6 * SS, 6 * SS


def draw_strokes(d, strokes, s, heads, cm):
    for st in strokes:
        k = s - st["s0"]
        if k <= 0: continue
        k = min(k, st["len"]); cum = st["cum"]; px = proj(st["m"], cm) * SS
        i = int(np.searchsorted(cum, k, side="right")); pts = px[:i]
        if i < len(px):
            u = (k - cum[i - 1]) / (cum[i] - cum[i - 1]); pts = np.r_[pts, [px[i - 1] + (px[i] - px[i - 1]) * u]]
        d.line([tuple(p) for p in pts], fill=GOLD + (255,), width=LW, joint="curve")
        for p in (pts[0], pts[-1]):
            d.ellipse([p[0] - LW / 2, p[1] - LW / 2, p[0] + LW / 2, p[1] + LW / 2], fill=GOLD + (255,))
        if heads and k < st["len"]:
            p = pts[-1]; d.ellipse([p[0] - HEAD, p[1] - HEAD, p[0] + HEAD, p[1] + HEAD], fill=WHITE + (255,))


def progress(t):
    """(mètres parcourus sur le circuit 1, tête visible, idem circuit 2) au temps t de la séquence."""
    f1 = min(1, max(0, (t * FPS - T_C1) / (T_C1_END - T_C1))); f2 = min(1, max(0, (t * FPS - T_C2) / (T_C2_END - T_C2)))
    return L1 * f1, 0 < f1 < 1, L2 * f2, 0 < f2 < 1


def traces(t, cm):
    lay = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    s1, h1, s2, h2 = progress(t)
    if s1 > 0: draw_strokes(d, ST1, s1, h1, cm)
    if s2 > 0: draw_strokes(d, ST2, s2, h2, cm)
    return lay.resize((W, H), Image.LANCZOS)


# ---------- textes : capitales espacées, arrivée par glissement de 24 px en 4 images, sans fondu
def slide(n, n0): return 24 * (1 - (1 - min(1, (n - n0) / 4)) ** 3)


def tracked(d, x, y, s, f, fill, track=0.06):
    for ch in s:
        d.text((x, y), ch, font=f, fill=fill, anchor="ls"); x += f.getlength(ch) + track * f.size
    return x


def width_of(s, f, track=0.06): return sum(f.getlength(ch) + track * f.size for ch in s)


F_LAB, F_TOT, F_SUB, F_CRED = font("SemiBold", 40), font("Bold", 150), font("SemiBold", 40), font("Regular", 14)
V1 = f" · {km(chiffres['circuit_1']['longueur_km'])} km"; V2 = f" · {km(chiffres['circuit_2']['longueur_km'])} km"
EAST2 = M(p2["avenues"]["E"][0])                            # bout de l'avenue est du circuit 2
TOT = (W * 0.62, H * 0.50)


def map_texts(im, n, cm):
    """Étiquettes accrochées à la carte : elles suivent la caméra."""
    d = ImageDraw.Draw(im)
    if n >= T_C1:
        e = proj(K1, cm)[0]                                    # accroché à l'angle du circuit : là où était le point or
        x = tracked(d, e[0] + 40, e[1] + 62 - slide(n, T_C1) + 24, "CIRCUIT 1", F_LAB, WHITE)
        if n >= T_C1_END: tracked(d, x, e[1] + 62 - slide(n, T_C1_END) + 24, V1, F_LAB, GOLD)
    if n >= T_C2:
        e = proj(EAST2, cm)[0]; x = tracked(d, e[0] + 34, e[1] + 14 - slide(n, T_C2) + 24, "CIRCUIT 2", F_LAB, WHITE)
        if n >= T_C2_END: tracked(d, x, e[1] + 14 - slide(n, T_C2_END) + 24, V2, F_LAB, GOLD)


def screen_texts(im, n):
    """Textes accrochés à l'écran : le total, et la mention des images (dès l'image 1)."""
    d = ImageDraw.Draw(im)
    if T_TOTAL <= n < T_DIVE:
        dy = -slide(n, T_TOTAL) + 24
        x = tracked(d, TOT[0], TOT[1] + dy, km(chiffres["total_km"]), F_TOT, GOLD, 0.0)
        tracked(d, x + 18, TOT[1] + dy, "km", font("SemiBold", 64), GOLD, 0.0)
        tracked(d, TOT[0] + 6, TOT[1] + 64 + dy, "D'AVENUES ÉCLAIRÉES", F_SUB, WHITE)
    if n >= 1:
        o = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(o).text((W - 24, H - 20), "Imagery © Google, Airbus", font=F_CRED, fill=WHITE + (153,), anchor="rs")
        im.alpha_composite(o)


# ---------- une image (avec flou de mouvement quand la caméra va vite)
globe_last = Image.open(OUT / "ouverture_globe_derniere.png").convert("RGB")
assert globe_last.size == (W, H)
yy, xx = np.mgrid[0:H, 0:W]
REF = np.array([[0, 0], [W, 0], [0, H], [W, H], [W / 2, H / 2]], float)


def speed_px(t):
    """Déplacement maximal à l'écran d'un point de la carte entre t et t + 1 image."""
    a, b = cam(t), cam(min(9.0, t + 1 / FPS))
    m = np.c_[a[0][0] + (REF[:, 0] - W / 2) / (S0 * a[1]), a[0][1] - (REF[:, 1] - H / 2) / (S0 * a[1])]
    return float(np.abs(proj(m, b) - REF).max())


def window_mask(t):
    cm = cam(t); c = proj(OUAGA_M, cm)[0]; k = t / 0.5
    far = max(np.hypot(*(c - q)) for q in [(0, 0), (W, 0), (0, H), (W, H)]) + 4
    r = 9 + (far - 9) * k ** 2.2
    return Image.fromarray((np.clip(r - np.hypot(xx - c[0], yy - c[1]) + 0.5, 0, 1) * 255).astype(np.uint8)), c


def sample(t, n):
    """Carte + tracés + étiquettes de carte au temps t (une sous-image)."""
    cm = cam(t)
    im = map_layer(cm).convert("RGBA"); im.alpha_composite(traces(t, cm)); map_texts(im, n, cm)
    return im


def frame(n):
    if n == 0:
        return globe_last.copy().convert("RGBA")
    t = n / FPS
    v = speed_px(t); sub = 1 if v < 4 else int(min(10, np.ceil(v / 5)))
    sh = SHUTTER if t >= T_DIVE / FPS else 0.25                # flou fort réservé à la plongée finale
    times = [min(8.999, t + ((i + 0.5) / sub - 0.5) * sh / FPS) for i in range(sub)] if sub > 1 else [t]
    acc = None
    for ts in times:
        a = np.asarray(sample(ts, n).convert("RGB"), np.float32); acc = a if acc is None else acc + a
    im = Image.fromarray(np.clip(acc / len(times), 0, 255).astype(np.uint8)).convert("RGBA")
    if n < T_C1:                                               # la fenêtre s'ouvre sur la carte, le point reste sur Ouagadougou
        mask, c = window_mask(t)
        base = globe_last.copy(); base.paste(im.convert("RGB"), (0, 0), mask); im = base.convert("RGBA")
        ImageDraw.Draw(im).ellipse([c[0] - 9, c[1] - 9, c[0] + 9, c[1] + 9], fill=GOLD)
    screen_texts(im, n)
    return im


# ---------- contrôles : textes hors des tracés et dans le cadre, aux instants où ils sont tous posés
problems = []
for n in (T_C1_END + 11, T_C2_END + 11, T_DIVE - 1):
    t = n / FPS; cm = cam(t)
    tr = np.asarray(traces(t, cm).split()[3].filter(ImageFilter.MaxFilter(21))) > 0
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); map_texts(lay, n, cm); screen_texts(lay, n)
    tx = np.asarray(lay.split()[3]) > 0; tx[H - 60:, W - 400:] = False
    over = int((tr & tx).sum()); ys, xs = np.nonzero(tx)
    inside = bool(len(xs) == 0 or (xs.min() >= 40 and xs.max() <= W - 40 and ys.min() >= 30 and ys.max() <= H - 30))
    problems.append((n, over, inside))
print("caméra : zoom de", min(k[2] for k in KEYS), "à", max(k[2] for k in KEYS),
      f"; fond à {FOND_MPP:.2f} m/px, cadre d'ensemble à {1 / S0:.2f} m/px")
print(f"longueurs : circuit 1 {L1 / 1000:.2f} km en {(T_C1_END - T_C1) / FPS:.1f} s ; circuit 2, chemin le plus long {L2 / 1000:.2f} km en {(T_C2_END - T_C2) / FPS:.1f} s")
for n, over, inside in problems:
    print(f"image {n} ({n / FPS:.2f} s) : chevauchement texte / tracé {over} px ; textes dans le cadre : {inside}")
print("flou de mouvement (sous-images) :", {n: int(min(10, np.ceil(speed_px(n / FPS) / 5))) for n in range(1, N) if speed_px(n / FPS) >= 4})

OUT.mkdir(exist_ok=True)
enc = None if apercu else subprocess.Popen(
    ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
     "-vf", "setsar=1", "-c:v", "libx264", "-crf", "14", "-preset", "slow", "-pix_fmt", "yuv420p",
     "-frames:v", str(N), str(OUT / "ouverture_circuits.mp4")], stdin=subprocess.PIPE)
board, last = [], None
for n in range(N):
    if apercu and n % 12 and n != N - 1:
        continue
    im = frame(n).convert("RGB")
    if enc: enc.stdin.write(im.tobytes())
    if n % 12 == 0 or n == N - 1: board.append((n, im))
    last = im
if enc:
    enc.stdin.close(); enc.wait()
last.save(OUT / "ouverture_circuits_derniere.png")
diff = np.abs(np.asarray(board[0][1]).astype(int) - np.asarray(globe_last).astype(int)).max()
print(f"raccord : écart max entre l'image 0 et la dernière image du globe = {diff}")

cols, tw, th = 4, 480, 270
sheet = Image.new("RGB", (cols * tw, ((len(board) + cols - 1) // cols) * th), (20, 20, 20))
for i, (n, im) in enumerate(board):
    v = im.resize((tw, th), Image.LANCZOS); ImageDraw.Draw(v).text((8, 6), f"image {n} · {n / FPS:.2f} s", fill=(255, 220, 0))
    sheet.paste(v, ((i % cols) * tw, (i // cols) * th))
sheet.save(OUT / "ouverture_circuits_planche.jpg", quality=90)
print(f"planche : {OUT / 'ouverture_circuits_planche.jpg'} ({len(board)} vignettes)")

# les moments rapides, image par image : l'ouverture de la fenêtre, le glissé, le recul, la plongée
strip = Image.new("RGB", (8 * 240, 4 * 135), (20, 20, 20))
for row, (a, b) in enumerate(((1, 12), (84, 96), (156, 168), (204, 215))):
    for i, n in enumerate(np.linspace(a, b, 8).round().astype(int)):
        v = frame(int(n)).convert("RGB").resize((240, 135), Image.LANCZOS)
        ImageDraw.Draw(v).text((4, 3), f"{n / FPS:.2f}", fill=(255, 220, 0)); strip.paste(v, (i * 240, row * 135))
strip.save(OUT / "ouverture_circuits_fenetre.jpg", quality=90)
print(f"planche des mouvements rapides : {OUT / 'ouverture_circuits_fenetre.jpg'}")
