"""Cale une capture Google Earth sur les tracés KMZ et écrit son emprise.

On enregistre deux fois la même vue dans Google Earth : une fois avec les tracés rouges des
circuits, une fois sans. Les pixels rouges de la première sont ajustés (transformation affine,
ICP) sur la géométrie des circuits lue dans circuits/ ; la seconde devient le fond, avec un .json
d'emprise {nord, sud, est, ouest} comme l'attend docs/PROMPT_claude_code_globe.md.

usage: python ouverture/caler_fond.py AVEC_TRACES.jpg SANS_TRACES.jpg fonds/NOM.jpg [--largeur PX]
  --largeur : réduit le fond redressé à cette largeur (une capture de 8192 px est plus fine que le cadre)
  --qualite : qualité JPEG du fond (95 par défaut)
"""
import json
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None          # captures « Maximum » de Google Earth : 8192 px et plus
sys.path.insert(0, str(Path(__file__).resolve().parent))
from circuits import KX, circuit1, circuit2, densify  # noqa: E402

avec, sans, sortie = map(Path, sys.argv[1:4])
A = np.asarray(Image.open(avec).convert("RGB")).astype(np.int16)
B = np.asarray(Image.open(sans).convert("RGB")).astype(np.int16)
if A.shape != B.shape:
    sys.exit(f"les deux captures n'ont pas la même taille : {A.shape[1]}x{A.shape[0]} et {B.shape[1]}x{B.shape[0]}")
h, w = A.shape[:2]

# pixels du tracé rouge : rouges sur la première capture, absents de la seconde
red = (A[..., 0] > 150) & (A[..., 1] < 100) & (A[..., 2] < 100) & (np.abs(A - B).sum(axis=2, dtype=np.int16) > 120)
del B
ry, rx = np.nonzero(red)
P = np.stack([rx, ry], 1).astype(float)
print(f"capture {w}x{h} ; {len(P)} pixels de tracé rouge")
if len(P) > 20000:                       # capture en pleine résolution : un pixel sur k suffit au calage
    P = P[::int(np.ceil(len(P) / 20000))]
if len(P) < 200:
    sys.exit("trop peu de pixels rouges : les tracés sont-ils bien affichés sur la première capture ?")

# géométrie des circuits en (lon, lat), échantillonnée tous les 10 m environ
G = np.concatenate([densify(line, 10) for line in circuit1() + circuit2()])

# première estimation : les extrémités du nuage rouge contre celles des tracés (axes nord et est)
def fit(src, dst):
    X = np.c_[src, np.ones(len(src))]
    M, *_ = np.linalg.lstsq(X, dst, rcond=None)
    return M  # (3, 2) : [lon, lat, 1] @ M = [x, y]

lon0, lon1, lat0, lat1 = G[:, 0].min(), G[:, 0].max(), G[:, 1].min(), G[:, 1].max()
x0, x1, y0, y1 = P[:, 0].min(), P[:, 0].max(), P[:, 1].min(), P[:, 1].max()
M = fit(np.array([[lon0, lat1], [lon1, lat0], [lon0, lat0], [lon1, lat1]]),
        np.array([[x0, y0], [x1, y1], [x0, y1], [x1, y0]]))

# ICP : chaque point des tracés vers le pixel rouge le plus proche, puis on réajuste l'affine.
# Le seuil de rejet se resserre peu à peu : un seuil serré d'emblée laisse le circuit 1, plus long,
# imposer son calage et écarter le circuit 2 comme aberrant. Chaque circuit pèse autant que l'autre.
weight = np.concatenate([np.full(len(densify(l, 10)), 1.0 / n) for n, lines in
                         ((sum(len(densify(l, 10)) for l in circuit1()), circuit1()),
                          (sum(len(densify(l, 10)) for l in circuit2()), circuit2())) for l in lines])
def nearest(M):
    Q = np.c_[G, np.ones(len(G))] @ M
    idx = np.empty(len(Q), int); dist = np.empty(len(Q))
    for k in range(0, len(Q), 128):
        d = ((Q[k:k + 128, None, :] - P[None, :, :]) ** 2).sum(-1)
        idx[k:k + 128] = d.argmin(1); dist[k:k + 128] = np.sqrt(d.min(1))
    return idx, dist
K = max(1.0, w / 1024)                   # seuils pensés pour une capture de 1024 px
for seuil in [v * K for v in (80, 50, 30, 20, 12, 8)] + [8, 5, 3]:
    for it in range(15):
        idx, dist = nearest(M); keep = dist < seuil
        sw = np.sqrt(weight[keep])[:, None]
        X = np.c_[G[keep], np.ones(keep.sum())] * sw
        M_new, *_ = np.linalg.lstsq(X, P[idx[keep]] * sw, rcond=None)
        done = np.abs(M_new - M).max() < 1e-7
        M = M_new
        if done:
            break
idx, dist = nearest(M)
MPP = KX / np.hypot(*M[0])              # mètres par pixel de la capture
print(f"calage : écart médian {np.median(dist):.2f} px, 95 % sous {np.percentile(dist, 95):.2f} px, max {dist.max():.1f} px "
      f"(capture à {MPP:.1f} m/px : max {dist.max() * MPP:.0f} m)")

# la vue de Google Earth peut être légèrement tournée : rotation lue sur chacun des deux axes
ax, ay = M[0], M[1]          # dérivées de (x, y) par rapport à lon et à lat
rot_lon = np.degrees(np.arctan2(ax[1], ax[0])); rot_lat = np.degrees(np.arctan2(ay[0], -ay[1]))
print(f"rotation de la vue : {rot_lon:.2f}° (axe est-ouest), {rot_lat:.2f}° (axe nord-sud)")
# Une vue inclinée déforme l'image en trapèze, ce qu'une affine ne rattrape pas : l'écart de calage
# grandit alors. Tant qu'il reste faible, l'affine corrige aussi le léger cisaillement.
if dist.max() > max(3, 40 / MPP):
    sys.exit("calage imprécis (écart > 3 px et > 40 m) : vue inclinée ? Remettre la vue à plat (touche U) et refaire les captures")

# On redresse la capture nord en haut : la plus grande emprise lon/lat contenue dans l'image,
# rééchantillonnée à la même résolution. Chaque pixel de sortie va chercher son pixel source par M.
Minv = np.linalg.inv(np.r_[M.T, [[0, 0, 1]]])
def lonlat(x, y): return (Minv @ [x, y, 1])[:2]
(lo_tl, la_tl), (lo_tr, la_tr), (lo_bl, la_bl), (lo_br, la_br) = (lonlat(0, 0), lonlat(w, 0), lonlat(0, h), lonlat(w, h))
ouest, est = max(lo_tl, lo_bl), min(lo_tr, lo_br)
nord, sud = min(la_tl, la_tr), max(la_bl, la_br)
ow = int(round((est - ouest) * np.hypot(*ax))); oh = int(round((nord - sud) * np.hypot(*ay)))
du, dv = (est - ouest) / ow, -(nord - sud) / oh
# (u, v) -> (lon, lat) = (ouest + u du, nord + v dv) -> (x, y) = [lon, lat, 1] @ M
a, d_ = M[0] * du; b, e_ = M[1] * dv; c, f = np.array([ouest, nord, 1.0]) @ M
img = Image.open(sans).convert("RGB").transform((ow, oh), Image.AFFINE, (a, b, c, d_, e_, f), resample=Image.BICUBIC)
if "--largeur" in sys.argv and ow > int(sys.argv[sys.argv.index("--largeur") + 1]):
    lw = int(sys.argv[sys.argv.index("--largeur") + 1])
    ow, oh = lw, int(round(oh * lw / ow)); img = img.resize((ow, oh), Image.LANCZOS)
emprise = {"nord": round(float(nord), 7), "sud": round(float(sud), 7),
           "est": round(float(est), 7), "ouest": round(float(ouest), 7),
           "largeur_px": ow, "hauteur_px": oh,
           "calage": {"ecart_median_px": round(float(np.median(dist)), 2), "ecart_max_px": round(float(dist.max()), 2),
                      "rotation_corrigee_deg": round(float(rot_lon), 3),
                      "source": f"{avec.name} (tracés rouges) ajusté sur circuits/*.kmz, {sans.name} redressée"}}
sortie.parent.mkdir(parents=True, exist_ok=True)
img.save(sortie, quality=int(sys.argv[sys.argv.index("--qualite") + 1]) if "--qualite" in sys.argv else 95)
sortie.with_suffix(".json").write_text(json.dumps(emprise, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps(emprise, ensure_ascii=False))
