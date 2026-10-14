"""Montage V5 du film « L'allumage » (60 s, 1440 images, 120 BPM) : la V4 validée, avec l'existant en noir et blanc.

Seules changent les images de la situation actuelle (le jour) : rafale de 15 à 23 s et côté « AVANT » du volet.
Elles passent par scripts/existant.py (noir et blanc dense et net, un réglage par plan). Le 5e plan de la rafale
(C2 à 72 s) est remplacé par C2 à 13 s : de 17 à 89 s, le rush du circuit 2 porte un reflet fixe du tableau de bord
sur la chaussée, que le contraste rend visible. Les coupes sont celles de la V4 : le son de la V4 reste valable.

   0– 6 s  le globe              rendus/ouverture_globe.mp4 (démarre déjà en rotation)
   6–15 s  les circuits          rendus/ouverture_circuits.mp4 (la caméra suit la lumière, plongée finale)
  15–23 s  le jour               rafale qui accélère : 2 · 1,5 · 1,5 · 1 · 1 · 0,5 · 0,5 s (×2, noir et blanc)
  23–30 s  la bascule            noir, clac, point or -> tête LED (C2-S1), volet avant (noir et blanc) / après
  30–40 s  le produit            images qui bougent : vitesse réelle puis ralenti en allant chercher le détail
                                 (couronne puis crosses en un seul mouvement, mât remonté, acier révélé en reculant)
  40–55 s  la ville la nuit      coupes mât à mât, ralenti au passage d'une couronne, compteur agrandi
  55–60 s  la fin                titre en grand sur image qui bouge, puis tout s'éteint sauf une lampe

usage :
  python scripts/montage_v5.py --planche   une image par temps -> rendus/v5_planche.jpg et v5_planche_grande.jpg,
                                           liste des coupes rendus/v5_cuts.txt ; aucune vidéo encodée
  python scripts/montage_v5.py             rendu complet -> rendus/v5_video.mp4 (son : rendus/v4_son.wav)
"""
import os, sys, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from commun import (W, H, FPS, GOLD, WHITE, BG, ROOT, N, P, R, C1, C2, NIGHT,
                    font, ease, frames, grade, txt, rect, brightest)
import existant as ex

PLANCHE = "--planche" in sys.argv
GLOBE, CIRCUITS = R + "ouverture_globe.mp4", R + "ouverture_circuits.mp4"
for f in (GLOBE, CIRCUITS):
    if not os.path.exists(f): sys.exit(f"{f} manquant : lancer ouverture/render_globe.py puis ouverture/render_circuits.py")

out = None if PLANCHE else subprocess.Popen(
    ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
     "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-pix_fmt", "yuv420p", R + "v5_video.mp4"], stdin=subprocess.PIPE)
T = [0]; CUTS = []; BOARD = []
def now(): return T[0] / FPS
def emit(im):
    im = im.convert("RGB")
    if out: out.stdin.write(im.tobytes())
    if T[0] % 12 == 0: BOARD.append((T[0], im.resize((320, 180), Image.LANCZOS)))
    T[0] += 1
def cut():
    assert T[0] % 12 == 0, f"coupe hors grille à l'image {T[0]}"
    CUTS.append(now())


def frames_hi(src, ss, dur, vf, fps_out):
    """Images à cadence élevée (pour les ralentis interpolés), sans retour à 24 i/s."""
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{ss:.3f}", "-i", src, "-t", f"{dur:.3f}",
           "-vf", f"{vf},scale={W}:{H}:flags=lanczos,format=rgb24", "-f", "rawvideo", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    return [Image.frombytes("RGB", (W, H), raw[i:i + W * H * 3]) for i in range(0, len(raw) - W * H * 3 + 1, W * H * 3)]


def push(im, s, cx=W / 2, cy=H / 2):
    """Poussée de caméra : agrandit l'image d'un facteur s autour de (cx, cy)."""
    if s <= 1.0001: return im
    w, h = W / s, H / s; x0 = min(max(cx - w / 2, 0), W - w); y0 = min(max(cy - h / 2, 0), H - h)
    return im.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((W, H), Image.BICUBIC)


def word_at(img, t, t0, t1, s, size, col, x, y, weight="Bold", anchor="mm"):
    """Mot posé sur le temps : glisse de 24 px en 4 images, sans fondu, part net à t1."""
    if not (t0 <= t < t1): return
    k = ease((t - t0) / (4 / FPS)); f = font(weight, size)
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).text((x, y + 3), s, font=f, fill=(0, 0, 0, int(150 * k)), anchor=anchor)
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
    txt(img, (x, y + (1 - k) * 24), s, f, col, 1.0 if k > 0 else 0, anchor)


COUNTER = [None]  # (valeur_affichée, cible, t_debut)
def counter(img, t):
    c = COUNTER[0]
    if c is None: return
    v0, v1, ts = c; k = ease((t - ts) / 0.3); v = v0 + (v1 - v0) * k
    s = f"{v:.1f}".replace(".", ",")
    f1 = font("Bold", 110); f2 = font("SemiBold", 38)
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle([W/2-330, 920, W/2+330, 1050], fill=(0, 0, 0, 110))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(34)))
    txt(img, (W/2 - 16, 990), s, f1, GOLD, 1, "rs"); txt(img, (W/2 + 8, 990), "KM ÉCLAIRÉS", f2, WHITE, 1, "ls")
def set_counter(v):
    c = COUNTER[0]; cur = c[1] if c else 0.0; COUNTER[0] = (cur, v, now())


# ---------- 0–6 s · le globe (144 images) ; 6–15 s · les circuits (216 images, finit sur la plongée)
cut()
for fr in frames(GLOBE, 0, 6.0): emit(fr.convert("RGBA"))
cut()
for fr in frames(CIRCUITS, 0, 9.0): emit(fr.convert("RGBA"))

# ---------- 15–23 s · le jour : une rafale qui accélère jusqu'au silence. Le premier plan prolonge la plongée
# (départ du circuit 1, avenue Kwame Nkrumah, en marche avant). L'existant en noir et blanc, un réglage par plan.
day = [(C1, 1.0, 371, 2.0), (C1, 14.0, 371, 1.5), (C2, 5.2, 180, 1.5), (C1, 38.5, 371, 1.0),
       (C2, 13.0, 180, 1.0), (C1, 84.0, 371, 0.5), (C1, 90.5, 371, 0.5)]
for src, ss, cx, dur in day:
    cut()
    shot = list(frames(src, ss, dur, f"crop=1038:584:{cx}:0,{ex.DENOISE},setpts=0.5*PTS"))
    lut = ex.curve_for(shot[::4])
    for fr in shot: emit(grade(ex.apply(fr, lut, T[0])))

# ---------- 23–30 s · la bascule
first = next(frames(N + "C2-S1_nuit_seedance_v1.mov", 2.0, 0.05))
DOT = brightest(first, 0.55)                                                  # la tête LED que le point va devenir
cut()
for i in range(int(0.5 * FPS)): emit(Image.new("RGB", (W, H), (6, 7, 8)))     # noir et silence
cut()
for i in range(int(0.5 * FPS)):                                               # clac : le point s'allume
    t = i / FPS; k = ease(t / 0.25); im = Image.new("RGBA", (W, H), (6, 7, 8, 255)); d = ImageDraw.Draw(im); r = 4 + 10 * k
    d.ellipse([DOT[0]-r, DOT[1]-r, DOT[0]+r, DOT[1]+r], fill=GOLD + (255,)); emit(im)
cut()
for fr in frames(N + "C2-S1_nuit_seedance_v1.mov", 2.0, 2.0, NIGHT): emit(grade(fr))   # le point devient la tête LED
cut()                                                                          # volet unique, ralenti 50 %, lente poussée
dayg = list(frames(P + "C1-S1_plaque_16x9_720p_5s.mp4", 0, 4.0, f"{ex.DENOISE},setpts=2.0*PTS,minterpolate=fps=24:mi_mode=mci"))
lut = ex.curve_for(dayg[::8])                                                 # avant en noir et blanc, après en couleur
nig = frames(N + "C1-S1_nuit_seedance_v1.mov", 0, 4.0, NIGHT + ",setpts=2.0*PTS,minterpolate=fps=24:mi_mode=mci")
t0 = now()
for fd, fn in zip(dayg, nig):
    t = now() - t0; x = int(W * (1 - ease((t - 0.5) / 2.5))) if t < 3.0 else 0
    im = grade(fn)
    if x > 0: a = grade(ex.apply(fd, lut, T[0])); im.paste(a.crop((0, 0, x, H)), (0, 0))   # le jour recule vers la gauche : la nuit gagne
    d = ImageDraw.Draw(im)
    if 0 < x < W:
        d.line([(x, 0), (x, H)], fill=GOLD + (255,), width=4)
        txt(im, (x-24, 880), "AVANT", font("SemiBold", 30), WHITE, 1, "rm"); txt(im, (x+24, 880), "APRÈS", font("SemiBold", 30), GOLD, 1, "lm")
    emit(push(im, 1 + 0.05 * t / 4.0))

# ---------- 30–40 s · le produit sur images qui bougent : vitesse réelle 0,5 s, puis ralenti (jusqu'à 25 % ou 15 %)
# pendant que le cadre va chercher le détail. Couronne puis crosses : un seul mouvement continu de 4 s ; le mât
# se remonte du pied au sommet ; l'acier se révèle en reculant sur le lampadaire entier. Un mot par temps fort.
def src_time(tau, vmin):
    """Temps source écoulé après tau secondes de plan : vitesse 1 jusqu'à 0,5 s, descente douce à vmin à 1 s."""
    if tau <= 0.5: return tau
    u = min(1.0, (tau - 0.5) / 0.5)
    base = 0.5 + 0.5 * (u - (1 - vmin) * (u ** 3 - u ** 4 / 2))              # intégrale de 1 - (1 - vmin) * smoothstep
    return base + vmin * max(0.0, tau - 1.0)
FULL = (0.0, 0.0, float(W))
def crop_at(keys, tau):
    """Cadre (x0, y0, largeur) interpolé entre des clés (temps, cadre), courbe douce dans chaque segment."""
    if tau <= keys[0][0]: return keys[0][1]
    for (t0, r0), (t1, r1) in zip(keys[:-1], keys[1:]):
        if tau <= t1:
            k = (tau - t0) / (t1 - t0); k = k * k * (3 - 2 * k)
            return tuple(r0[j] + (r1[j] - r0[j]) * k for j in range(3))
    return keys[-1][1]
def tighter(r, f):                                                           # même centre, cadre plus serré
    cx, cy = r[0] + r[2] / 2, r[1] + r[2] * 9 / 32; return rect(cx, cy, r[2] * f)
COUR, CROS = rect(610, 230, 760), rect(905, 150, 460)
MAT_A, MAT_B = rect(880, 760, 760), rect(880, 214, 760)
SOCLE, ACIER_A = rect(520, 820, 760), rect(700, 600, 1100)
product = [  # (clip, temps du détail, instant du plan où il tombe, durée, vitesse mini, clés de cadre, mots)
    ("C1-S1", 3.25, 2.0, 4.0, 0.15, [(0, FULL), (1.2, COUR), (2.0, COUR), (2.8, CROS), (4.0, tighter(CROS, 0.96))],
     [(0.5, 2.0, "COURONNE EN DENTELLE LED", (W / 2, 930)), (2.5, 4.0, "DOUBLE CROSSE · 4,5 M", (W / 2, 930))]),
    ("C1-S3", 0.75, 1.0, 2.0, 0.25, [(0, MAT_A), (1.6, MAT_B), (2.0, MAT_B)],
     [(0.5, 2.0, "MÂT DE 10 À 12 M", (W * 0.74, 930))]),
    ("C1-S3", 1.85, 1.0, 2.0, 0.15, [(0, FULL), (1.0, SOCLE), (2.0, rect(365, 830, 730))],   # le cadre suit le socle qui file à gauche
     [(0.5, 2.0, "SOCLE ÉCLAIRÉ · 1,3 M", (W / 2, 150))]),
    ("C1-S1", 2.5, 1.0, 2.0, 0.25, [(0, ACIER_A), (1.6, FULL), (2.0, FULL)],
     [(0.5, 2.0, "ACIER GALVANISÉ", (W / 2, 930))]),
]
for clip, t_detail, t_land, dur, vmin, keys, words in product:
    cut()
    hi_fps = int(round(24 / vmin / 24)) * 24                                  # assez d'images pour le ralenti le plus lent
    start = max(0.0, t_detail - src_time(t_land, vmin))
    hi = frames_hi(N + f"{clip}_nuit_seedance_v1.mov", start, src_time(dur, vmin) + 0.1,
                   NIGHT + f",minterpolate=fps={hi_fps}:mi_mode=mci", hi_fps)
    for i in range(int(dur * FPS)):
        tau = i / FPS; src = grade(hi[min(len(hi) - 1, int(round(src_time(tau, vmin) * hi_fps)))])
        x0, y0, w = crop_at(keys, tau); h = w * 9 / 16; x0 = min(max(x0, 0), W - w); y0 = min(max(y0, 0), H - h)
        im = src.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((W, H), Image.BICUBIC)
        for w0, w1, label, (lx, ly) in words: word_at(im, tau, w0, w1, label, 84, GOLD, lx, ly)
        emit(im)

# ---------- 40–55 s · la ville la nuit, mât à mât (inchangé, compteur agrandi)
pieces = [
    ("C1-S1", [(0.0, 1.0, 1.0)], [(0.0, 0.0)], "CIRCUIT 1"),
    ("C1-S3", [(0.0, 2.0, 1.0)], [(0.0, 1.2)], None),
    ("C1-S2", [(1.0, 2.0, 1.0)], [(0.0, 2.4)], None),
    ("C1-S1", [(1.9, 1.15, 1.0), (3.05, 0.54, 0.4), (3.59, 1.0, 1.0)], [(0.0, 3.6), (2.5, 4.8)], None),
    ("C1-S3", [(2.5, 2.0, 1.0)], [(0.0, 6.0)], None),
    ("C1-S2", [(3.25, 1.5, 1.0)], [(0.0, 7.2)], None),
    ("C2-S1", [(0.0, 1.0, 1.0)], [(0.0, 9.3)], "CIRCUIT 2"),
    ("C2-S1", [(2.0, 2.0, 1.0)], [(0.0, 11.4)], None),
]
for clip, spans, steps, label in pieces:
    cut(); t0 = now(); steps = list(steps)
    for ss, dur, speed in spans:
        vf = NIGHT if speed == 1.0 else NIGHT + f",setpts={1/speed}*PTS,minterpolate=fps=24:mi_mode=mci"
        for fr in frames(N + f"{clip}_nuit_seedance_v1.mov", ss, dur / speed, vf):
            t = now()
            while steps and t - t0 >= steps[0][0] - 1e-9:
                assert T[0] % 12 == 0, f"palier du compteur hors grille à l'image {T[0]}"
                set_counter(steps.pop(0)[1])
            im = grade(fr)
            if label: word_at(im, t, t0, t0 + 1.5, label, 110, WHITE, W / 2, 470)
            counter(im, t); emit(im)
COUNTER[0] = None

# ---------- 55–60 s · la fin : titre en grand sur image qui bouge (C1-S1 ralenti 50 %, lente poussée),
# puis tout s'éteint sauf une lampe
cut(); t0 = now()
endf = list(frames(N + "C1-S1_nuit_seedance_v1.mov", 2.0, 3.5, NIGHT + ",setpts=2.0*PTS,minterpolate=fps=24:mi_mode=mci"))
last = None
for i, fr in enumerate(endf):
    t = i / FPS; im = push(grade(fr), 1 + 0.05 * t / 3.5)
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle([60, 660, 1760, 1010], fill=(0, 0, 0, 120))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(60)))
    word_at(im, t, 0.0, 9.0, "DEUX CIRCUITS,", 92, WHITE, 140, 770, "Bold", "ls")
    word_at(im, t, 0.5, 9.0, "UNE NUIT RENDUE À LA VILLE", 92, WHITE, 140, 880, "Bold", "ls")
    word_at(im, t, 1.0, 9.0, "Ouagadougou · octobre 2026 · [maître d'ouvrage]", 34, GOLD, 144, 950, "Regular", "ls")
    emit(im); last = im
END = brightest(last.convert("RGB"), 0.4)                                     # la dernière lampe : celle de la dernière image
cut()
for i in range(int(1.5 * FPS)):                                               # tout s'éteint sauf une lampe
    t = i / FPS; im = Image.new("RGBA", (W, H), (6, 7, 8, 255)); r = 14 * (1 - ease((t - 0.5) / 0.5))
    if r > 0.5: ImageDraw.Draw(im).ellipse([END[0]-r, END[1]-r, END[0]+r, END[1]+r], fill=GOLD + (255,))
    emit(im)

if out: out.stdin.close(); out.wait()
open(R + "v5_cuts.txt", "w").write("\n".join(f"{c:.4f}" for c in CUTS) + f"\nEND {now():.4f}\n")
cols = 12; tw, th = 160, 90; rows = (len(BOARD) + cols - 1) // cols
sheet = Image.new("RGB", (cols * tw, rows * th), (14, 14, 14))
for i, (n, im) in enumerate(BOARD):
    v = im.resize((tw, th), Image.LANCZOS); ImageDraw.Draw(v).text((4, 3), f"{n / FPS:.1f}", fill=(255, 220, 0))
    sheet.paste(v, ((i % cols) * tw, (i // cols) * th))
sheet.save(R + "v5_planche.jpg", quality=90)
big = Image.new("RGB", (6 * 320, ((len(BOARD) + 5) // 6) * 180), (14, 14, 14))
for i, (n, im) in enumerate(BOARD):
    v = im.copy(); ImageDraw.Draw(v).text((6, 4), f"{n / FPS:.1f} s", fill=(255, 220, 0)); big.paste(v, ((i % 6) * 320, (i // 6) * 180))
big.save(R + "v5_planche_grande.jpg", quality=88)
print("durée", now(), "s ; images", T[0], "; coupes", len(CUTS), "; DOT", DOT, "END", END, "; planche", len(BOARD), "vignettes")
