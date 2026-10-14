"""Géométrie des deux circuits, lue dans circuits/*.kmz (coordonnées WGS84 : lon, lat).

- Circuit 1 : la polyligne de « tracé 1.kmz », dans l'ordre du fichier (de l'aéroport vers le CHU).
- Circuit 2 : « 2ème trajet.kmz » parcourt chaque avenue dans les deux sens et coupe l'anneau en
  lignes droites. On en tire l'axe de chaque avenue (une seule fois) et l'anneau du Monument des
  Héros nationaux comme un cercle, dont le centre et le rayon viennent des points du fichier.
"""
import math
import re
import zipfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
KMZ1 = ROOT / "circuits" / "tracé 1.kmz"
KMZ2 = ROOT / "circuits" / "2ème trajet.kmz"
LAT0 = 12.34          # latitude de référence pour la projection locale en mètres
KX = 111320.0 * math.cos(math.radians(LAT0)); KY = 110574.0


def read_kmz(path):
    kml = zipfile.ZipFile(path).read("doc.kml").decode("utf-8")
    raw = re.search(r"<coordinates>(.*?)</coordinates>", kml, re.S).group(1).split()
    return np.array([[float(v) for v in c.split(",")[:2]] for c in raw])


def to_m(ll): return np.c_[ll[:, 0] * KX, ll[:, 1] * KY]
def to_ll(m): return np.c_[m[:, 0] / KX, m[:, 1] / KY]


def length_m(line):
    """Longueur d'une ligne (lon, lat) en mètres, par haversine."""
    R = 6371008.8; lo, la = np.radians(line[:, 0]), np.radians(line[:, 1])
    h = np.sin(np.diff(la) / 2) ** 2 + np.cos(la[:-1]) * np.cos(la[1:]) * np.sin(np.diff(lo) / 2) ** 2
    return float((2 * R * np.arcsin(np.sqrt(h))).sum())


def densify(line, step_m):
    """Points le long de la ligne, espacés d'environ step_m mètres (lon, lat)."""
    m = to_m(line); out = [m[:1]]
    for a, b in zip(m[:-1], m[1:]):
        n = max(1, int(np.ceil(np.hypot(*(b - a)) / step_m)))
        out.append(a + (b - a) * (np.arange(1, n + 1) / n)[:, None])
    return to_ll(np.concatenate(out))


def circuit1():
    return [read_kmz(KMZ1)]


def circuit2_parts():
    pts = to_m(read_kmz(KMZ2)[:-1])                      # boucle fermée : dernier point = premier
    ends = {"N": pts[:, 1].argmax(), "S": pts[:, 1].argmin(), "O": pts[:, 0].argmin(), "E": pts[:, 0].argmax()}
    # chaque extrémité d'avenue est tracée deux fois (une par chaussée) : on prend le milieu des deux
    def end_point(i):
        d = np.hypot(*(pts - pts[i]).T); near = pts[d < 40]
        return near.mean(axis=0)
    E = {k: end_point(i) for k, i in ends.items()}
    # centre : croisement de l'axe nord-sud et de l'axe ouest-est
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = E["N"], E["S"], E["O"], E["E"]
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    a, b = x1 * y2 - y1 * x2, x3 * y4 - y3 * x4
    c = np.array([(a * (x3 - x4) - (x1 - x2) * b) / den, (a * (y3 - y4) - (y1 - y2) * b) / den])
    # rayon : distance médiane au centre des points de l'anneau (ni extrémités, à moins de 500 m)
    d = np.hypot(*(pts - c).T)
    far = np.zeros(len(pts), bool)
    for p in E.values(): far |= np.hypot(*(pts - p).T) < 40
    r = float(np.median(d[(~far) & (d < 500)]))
    spokes = {}
    for k, p in E.items():                                 # de l'extrémité jusqu'à l'anneau
        u = (p - c) / np.hypot(*(p - c)); spokes[k] = to_ll(np.array([p, c + u * r]))
    return {"centre": to_ll(c[None])[0], "rayon_m": r, "avenues": spokes}


def ring(parts, start_deg=90.0, n=360, clockwise=True):
    """L'anneau en polyligne fermée, à partir de l'angle start_deg (90 = nord)."""
    c = to_m(parts["centre"][None])[0]; s = -1 if clockwise else 1
    t = np.radians(start_deg + s * np.arange(n + 1) * 360.0 / n)
    return to_ll(np.c_[c[0] + parts["rayon_m"] * np.cos(t), c[1] + parts["rayon_m"] * np.sin(t)])


def circuit2():
    p = circuit2_parts()
    return list(p["avenues"].values()) + [ring(p)]


if __name__ == "__main__":
    c1 = length_m(circuit1()[0]); p = circuit2_parts()
    av = {k: length_m(v) for k, v in p["avenues"].items()}; an = length_m(ring(p))
    print(f"circuit 1 : {c1 / 1000:.2f} km")
    print("circuit 2 : avenues " + ", ".join(f"{k} {v:.0f} m" for k, v in av.items())
          + f" ; anneau {an:.0f} m (rayon {p['rayon_m']:.0f} m) ; total {(sum(av.values()) + an) / 1000:.2f} km")
