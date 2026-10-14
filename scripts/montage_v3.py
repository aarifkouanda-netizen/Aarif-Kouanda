"""Montage V3 du film « L'allumage » (60 s, 1440 images, 120 BPM : une coupe tous les multiples de 12 images).

Structure validée (CLAUDE.md) :
   0– 6 s  le globe              rendus/ouverture_globe.mp4
   6–15 s  les circuits          rendus/ouverture_circuits.mp4 (en attente de la vue satellite)
  15–23 s  le jour               5 plans de jour accélérés ×2, désaturés à 50 %, sans texte
  23–30 s  la bascule            noir, clac, point or -> tête LED (C2-S1), volet avant/après ralenti (C1-S1)
  30–40 s  le produit            5 détails de 2 s, un mot par détail
  40–55 s  la ville la nuit      coupes mât à mât, ralenti 40 % au passage d'une couronne, compteur
  55–60 s  la fin                titre, puis tout s'éteint sauf une lampe

usage :
  python scripts/montage_v3.py --planche   une image par temps (toutes les 12 images) -> rendus/v3_planche.jpg,
                                           et la liste des coupes rendus/v3_cuts.txt ; aucune vidéo encodée
  python scripts/montage_v3.py             rendu complet -> rendus/v3_video.mp4 (exige ouverture_circuits.mp4)
"""
import os, sys
from PIL import Image, ImageDraw, ImageFilter
from commun import (W, H, FPS, GOLD, WHITE, BG, ROOT, N, P, R, C1, C2, NIGHT,
                    font, ease, frames, grade, txt, word, rect, brightest)
import subprocess

PLANCHE = "--planche" in sys.argv
GLOBE, CIRCUITS = R + "ouverture_globe.mp4", R + "ouverture_circuits.mp4"
if not os.path.exists(GLOBE):
    sys.exit("rendus/ouverture_globe.mp4 manquant : lancer ouverture/render_globe.py")
if not os.path.exists(CIRCUITS) and not PLANCHE:
    sys.exit("rendus/ouverture_circuits.mp4 manquant (vue satellite des deux circuits) : seule la planche est possible")

os.makedirs(R + "apercus", exist_ok=True)
out = None if PLANCHE else subprocess.Popen(
    ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
     "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-pix_fmt", "yuv420p", R + "v3_video.mp4"], stdin=subprocess.PIPE)
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

COUNTER = [None]  # (valeur_affichée, cible, t_debut)
def counter(img, t):
    c = COUNTER[0]
    if c is None: return
    v0, v1, ts = c; k = ease((t - ts) / 0.3); v = v0 + (v1 - v0) * k
    s = f"{v:.1f}".replace(".", ",")
    f1 = font("Bold", 64); f2 = font("Medium", 24)
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(sh); d.rectangle([W/2-260, 950, W/2+260, 1050], fill=(0, 0, 0, 110))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(30)))
    txt(img, (W/2-14, 1000), s, f1, GOLD, 1, "rm"); txt(img, (W/2+4, 1006), "KM ÉCLAIRÉS", f2, WHITE, 1, "lm")
def set_counter(v):
    c = COUNTER[0]; cur = c[1] if c else 0.0; COUNTER[0] = (cur, v, now())

# ---------- 0–6 s · le globe (144 images) ; 6–15 s · les circuits (216 images)
cut()
for fr in frames(GLOBE, 0, 6.0): emit(fr.convert("RGBA"))
cut()
if os.path.exists(CIRCUITS):
    for fr in frames(CIRCUITS, 0, 9.0): emit(fr.convert("RGBA"))
else:   # planche seulement : emplacement réservé, signalé comme tel
    for i in range(9 * FPS):
        im = Image.new("RGBA", (W, H), BG + (255,))
        txt(im, (W/2, 520), "LES CIRCUITS", font("SemiBold", 54), WHITE, 1, "mm")
        txt(im, (W/2, 590), "en attente de la vue satellite des deux circuits", font("Regular", 30), GOLD, 1, "mm")
        emit(im)

# ---------- 15–23 s · le jour : 4 plans de 1,5 s et un de 2 s, accélérés ×2, désaturés à 50 %, sans texte
day = [(C1, 1, 371, 1.5), (C1, 38.5, 371, 1.5), (C1, 84, 371, 1.5), (C2, 5.2, 180, 1.5), (C2, 72, 180, 2.0)]
for src, ss, cx, dur in day:
    cut()
    for fr in frames(src, ss, dur, f"crop=1038:584:{cx}:0,setpts=0.5*PTS"): emit(grade(fr, 0.5))

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
cut()                                                                          # volet unique, ralenti 50 %
dayg = frames(P + "C1-S1_plaque_16x9_720p_5s.mp4", 0, 4.0, "setpts=2.0*PTS,minterpolate=fps=24:mi_mode=mci")
nig = frames(N + "C1-S1_nuit_seedance_v1.mov", 0, 4.0, NIGHT + ",setpts=2.0*PTS,minterpolate=fps=24:mi_mode=mci")
t0 = now()
for fd, fn in zip(dayg, nig):
    t = now() - t0; x = int(W * (1 - ease((t - 0.5) / 2.5))) if t < 3.0 else 0
    a = grade(fd); im = grade(fn); im.paste(a.crop((0, 0, x, H)), (0, 0))     # le jour recule vers la gauche : la nuit gagne
    d = ImageDraw.Draw(im)
    if 0 < x < W:
        d.line([(x, 0), (x, H)], fill=GOLD + (255,), width=4)
        txt(im, (x-24, 880), "AVANT", font("SemiBold", 30), WHITE, 1, "rm"); txt(im, (x+24, 880), "APRÈS", font("SemiBold", 30), GOLD, 1, "lm")
    emit(im)

# ---------- 30–40 s · le produit : 5 détails de 2 s (recadrages des plans de nuit, en attendant les gros plans fixes)
def still(clip, t):
    return grade(list(frames(N + f"{clip}_nuit_seedance_v1.mov", t, 0.05, NIGHT))[0])
shots = [("C1-S1", 3.25, rect(610, 260, 900), rect(610, 230, 760), "COURONNE EN DENTELLE LED"),
         ("C1-S1", 3.25, rect(900, 170, 560), rect(905, 150, 460), "DOUBLE CROSSE · 4,5 M"),
         ("C1-S3", 0.75, rect(880, 760, 760), rect(880, 214, 760), "MÂT DE 10 À 12 M"),
         ("C1-S3", 2.0, rect(520, 800, 900), rect(520, 820, 760), "SOCLE ÉCLAIRÉ · 1,3 M"),
         ("C1-S1", 2.5, rect(700, 600, 1100), rect(960, 540, 1920), "ACIER GALVANISÉ")]
for clip, ts, a, b, label in shots:
    cut(); src = still(clip, ts)
    for i in range(int(2.0 * FPS)):
        t = i / FPS; k = t / 2.0; k = k * k * (3 - 2 * k)
        x0, y0, w = [a[j] + (b[j] - a[j]) * k for j in range(3)]; h = w * 9 / 16
        im = src.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((W, H), Image.BICUBIC)
        word(im, t, 0.5, 2.0, label, 84, GOLD, 930); emit(im)

# ---------- 40–55 s · la ville la nuit, mât à mât
# Chaque morceau : (clip, [(début source, durée source, vitesse)], [(décalage, valeur du compteur)], titre)
# Le compteur monte par paliers réguliers jusqu'aux longueurs réelles : 7,2 km (circuit 1) puis 11,4 km au total.
pieces = [
    ("C1-S1", [(0.0, 1.0, 1.0)], [(0.0, 0.0)], "CIRCUIT 1"),                     # 40,0 s  l'avenue s'allume au loin
    ("C1-S3", [(0.0, 2.0, 1.0)], [(0.0, 1.2)], None),                            # 41,0 s  mât proche à 2,0 s
    ("C1-S2", [(1.0, 2.0, 1.0)], [(0.0, 2.4)], None),                            # 43,0 s
    ("C1-S1", [(1.9, 1.15, 1.0), (3.05, 0.54, 0.4), (3.59, 1.0, 1.0)],          # 45,0 s  la couronne passe en grand
              [(0.0, 3.6), (2.5, 4.8)], None),                                   #         au ralenti, puis reprend
    ("C1-S3", [(2.5, 2.0, 1.0)], [(0.0, 6.0)], None),                            # 48,5 s  mât proche à 4,25 s
    ("C1-S2", [(3.25, 1.5, 1.0)], [(0.0, 7.2)], None),                           # 50,5 s  circuit 1 : 7,2 km
    ("C2-S1", [(0.0, 1.0, 1.0)], [(0.0, 9.3)], "CIRCUIT 2"),                     # 52,0 s
    ("C2-S1", [(2.0, 2.0, 1.0)], [(0.0, 11.4)], None),                           # 53,0 s  monument dans l'axe : 11,4 km
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
            if label: word(im, t, t0, t0 + 1.5, label, 110, WHITE, 470)
            counter(im, t); emit(im)
COUNTER[0] = None

# ---------- 55–60 s · la fin : le titre (3,5 s), puis tout s'éteint sauf une lampe (1,5 s)
cut(); st = grade(list(frames(N + "C1-S1_nuit_seedance_v1.mov", 3.5, 0.05, NIGHT))[0])
END = brightest(st, 0.4)
for i in range(int(3.5 * FPS)):
    t = i / FPS; s = 1 + 0.05 * t / 3.5; w = W / s; h = H / s; x0 = END[0] - END[0] / s; y0 = END[1] - END[1] / s
    im = st.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((W, H), Image.BICUBIC)
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle([60, 760, 1500, 1010], fill=(0, 0, 0, 120)); im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(50)))
    k = ease((t - 0.0) / (4 / FPS)); txt(im, (110, 830 + (1 - k) * 24), "DEUX CIRCUITS, UNE NUIT RENDUE À LA VILLE", font("Bold", 54), WHITE, 1 if k > 0 else 0)
    k2 = ease((t - 0.5) / (4 / FPS)); txt(im, (110, 910 + (1 - k2) * 24), "Ouagadougou · octobre 2026 · [maître d'ouvrage]", font("Regular", 30), GOLD, 1 if t >= 0.5 else 0)
    emit(im)
cut()
for i in range(int(1.5 * FPS)):                                               # tout s'éteint sauf une lampe
    t = i / FPS; im = Image.new("RGBA", (W, H), (6, 7, 8, 255)); r = 14 * (1 - ease((t - 0.5) / 0.5))
    if r > 0.5: ImageDraw.Draw(im).ellipse([END[0]-r, END[1]-r, END[0]+r, END[1]+r], fill=GOLD + (255,))
    emit(im)

if out: out.stdin.close(); out.wait()
open(R + "v3_cuts.txt", "w").write("\n".join(f"{c:.4f}" for c in CUTS) + f"\nEND {now():.4f}\n")
# planche : une vignette par temps, 12 par ligne (6 s par ligne)
cols = 12; tw, th = 160, 90; rows = (len(BOARD) + cols - 1) // cols
sheet = Image.new("RGB", (cols * tw, rows * th), (14, 14, 14))
for i, (n, im) in enumerate(BOARD):
    v = im.resize((tw, th), Image.LANCZOS); ImageDraw.Draw(v).text((4, 3), f"{n / FPS:.1f}", fill=(255, 220, 0))
    sheet.paste(v, ((i % cols) * tw, (i // cols) * th))
sheet.save(R + "v3_planche.jpg", quality=90)
big = Image.new("RGB", (6 * 320, ((len(BOARD) + 5) // 6) * 180), (14, 14, 14))   # la même, en grand, pour la lecture
for i, (n, im) in enumerate(BOARD):
    v = im.copy(); ImageDraw.Draw(v).text((6, 4), f"{n / FPS:.1f} s", fill=(255, 220, 0)); big.paste(v, ((i % 6) * 320, (i // 6) * 180))
big.save(R + "v3_planche_grande.jpg", quality=88)
print("durée", now(), "s ; images", T[0], "; coupes", len(CUTS), "; DOT", DOT, "END", END, "; planche", len(BOARD), "vignettes")
