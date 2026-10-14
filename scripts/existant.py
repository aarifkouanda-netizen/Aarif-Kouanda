"""Traitement « existant » : les images de jour (la situation actuelle) en noir et blanc net et dense.

Les rushes de jour sont voilés (noirs trop clairs, contraste faible) et mous (bande de 1038 x 584 agrandie
près de 2 fois). Pour chaque plan, un seul réglage, calculé sur quelques images du plan (pas de scintillement) :
  1. noir et blanc par mélange de couches façon filtre orange (assombrit le voile bleuté du ciel) ;
  2. niveaux : noir au 0,5e centile relevé à 7 % (charte), blanc au 99,7e centile plafonné à 92 %, courbe en S douce,
     gamma qui ramène la valeur moyenne vers 45 % ;
  3. netteté (masque flou) adaptée à l'agrandissement ;
  4. grain fin déterministe (une graine par image), qui masque la mollesse de l'agrandissement.
Le débruitage léger (hqdn3d) se fait dans ffmpeg, avant l'agrandissement (voir DENOISE).
"""
import numpy as np
from PIL import Image, ImageFilter

DENOISE = "hqdn3d=2:1.5:3:3"
MIX = np.array([0.45, 0.45, 0.10], np.float32)          # filtre orange
WHITE_CAP, MID_TARGET, S_CURVE, BLACK = 0.92, 0.45, 0.15, 0.07
TINT = np.array([0.965, 0.985, 1.0], np.float32)          # très légère teinte anthracite dans les ombres


def luminance(im):
    return (np.asarray(im.convert("RGB"), np.float32) / 255) @ MIX


def curve_for(samples):
    """Réglage d'un plan à partir de quelques images : renvoie une table de 1024 valeurs (entrée 0-1 -> sortie 0-1)."""
    y = np.concatenate([luminance(s).ravel() for s in samples])
    lo, hi = np.percentile(y, 0.5), np.percentile(y, 99.7)
    x = np.linspace(0, 1, 1024)
    v = np.clip((x - lo) / max(hi - lo, 1e-3), 0, 1)
    mean = float(np.clip((y - lo) / max(hi - lo, 1e-3), 0, 1).mean())
    g = np.log(MID_TARGET) / np.log(max(min(mean, 0.95), 0.05))   # gamma qui amène la moyenne vers MID_TARGET
    v = v ** g
    v = v - S_CURVE * np.sin(2 * np.pi * v) / (2 * np.pi)    # courbe en S : pente 1 + S au milieu, 1 - S aux bouts
    return BLACK + np.clip(v, 0, 1) * (WHITE_CAP - BLACK)        # noirs relevés vers l'anthracite (charte)


def apply(im, lut, n):
    """Une image : noir et blanc, réglage du plan, netteté, grain, teinte ; renvoie une image RGB 8 bits."""
    y = luminance(im)
    y = lut[np.clip((y * 1023).astype(np.int32), 0, 1023)]
    L = Image.fromarray((y * 255).astype(np.uint8)).filter(ImageFilter.UnsharpMask(radius=1.4, percent=55, threshold=3))
    y = np.asarray(L, np.float32) / 255
    rng = np.random.default_rng(1000 + n)
    y = np.clip(y + rng.normal(0, 0.012, y.shape).astype(np.float32), 0, 1)
    tint = TINT + (1 - TINT) * y[..., None]                  # la teinte ne touche que les ombres
    return Image.fromarray((np.clip(y[..., None] * tint, 0, 1) * 255).astype(np.uint8))
