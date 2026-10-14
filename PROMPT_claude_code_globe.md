# Prompt Claude Code — ouverture du film : globe → Ouagadougou → circuits

À lancer dans **le même dossier que les cartes** (celui qui contient déjà `circuits/`, `fonds/`, `chiffres_circuits.json` et ton script de rendu des cartes), pour que Claude Code réutilise tes tracés, tes fonds satellite et ton style.

---

```
Tu vas produire les deux premières séquences d'un film de présentation : le remplacement des lampadaires sur deux circuits à Ouagadougou (Burkina Faso). Ce dossier contient déjà le travail sur les cartes : tracés KMZ dans circuits/, fonds satellite dans fonds/, longueurs dans chiffres_circuits.json et le script qui a produit plan7_synthese.mp4. Lis-les d'abord : la charte, les tracés et les chiffres viennent de là. N'invente aucun nombre.

## Livrables
1. ouverture_globe.mp4 — 6,0 s exactement (144 images)
2. ouverture_circuits.mp4 — 9,0 s exactement (216 images)
La dernière image de la séquence 1 et la première de la séquence 2 doivent être identiques : les deux plans se raccordent sans coupe visible.
Format : 1920×1080, 24 i/s, H.264 CRF 14, yuv420p, pixels carrés (setsar=1), sans son.
Exporte aussi pour chaque séquence une planche d'aperçu : une image tous les 12 images (un temps), en mosaïque. Montre-la-moi avant le rendu définitif.

## Grille de temps
Le film est monté sur une musique à 120 BPM : 1 temps = 0,5 s = 12 images. Chaque événement visible (apparition d'un mot, allumage, début d'un tracé) tombe exactement sur un multiple de 12 images.

## Charte (identique aux cartes existantes)
Fond anthracite #383E42 (océan et espace), terres en anthracite légèrement plus clair, frontières en gris aluminium #A5A5A5, le Burkina Faso et les circuits en or #F9A800, texte blanc cassé #F0F0EC. Police Inter (SemiBold pour les titres en capitales, Regular pour le reste).
Interdits : halos et lueurs, particules, anneaux qui s'étendent, fondus enchaînés, dégradés décoratifs, rebonds, tremblement de caméra, texte dans les coins, temps mort de plus d'1 s sans rien à lire, Math.random, et tout ce qui ressemble à un modèle tout fait.

## Séquence 1 — le globe (0–6 s)
Méthode : un fichier HTML avec une fonction seek(t) qui calcule chaque image à partir du temps (aucune animation CSS, aucun minuteur), rendu image par image avec Playwright puis ffmpeg. Globe en projection orthographique avec d3-geo, contours des pays tirés du paquet npm world-atlas (110m pour la vue lointaine, 50m quand on approche), via topojson-client. Graticule très discret (opacité 8 %).
- 0–3 s : le globe, petit (rayon 320 px), tourne pour amener le Burkina Faso au centre (centre final : latitude 12,37, longitude -1,52) pendant que le rayon grandit jusqu'à 950 px. Zoom exponentiel, accélération et décélération douces.
- 3,0 s (image 72) : le Burkina Faso passe en or (contour or plein, remplissage or à 18 %), net, sur le temps. Le mot « BURKINA FASO » apparaît à côté du pays (glissement de 12 px en 4 images, sans fondu).
- 3–5 s : la caméra plonge vers Ouagadougou ; le globe déborde du cadre, les frontières voisines défilent. « BURKINA FASO » disparaît net à 4,5 s.
- 5,0 s (image 120) : un point or plein de 18 px s'allume sur Ouagadougou (12,3714 ; -1,5197), et « OUAGADOUGOU » apparaît sous lui. Aucune lueur autour du point.
- 5–6 s : la descente continue doucement ; le point reste exactement au centre de l'écran (960, 540) jusqu'à la dernière image.

## Séquence 2 — les circuits (6–15 s du film, 0–9 s du fichier)
- Image 0 : identique à la dernière image de la séquence 1 (même point, même place).
- 0–0,5 s : le point or s'agrandit en cercle et devient la fenêtre qui révèle la vue satellite assombrie de Ouagadougou (même traitement que dans plan7). Le cercle s'ouvre jusqu'à remplir l'écran ; pas de fondu.
- La vue satellite doit montrer LES DEUX circuits dans un seul cadre, à leur vraie position l'un par rapport à l'autre. Si aucun fond de fonds/ ne couvre les deux circuits ensemble, ARRÊTE-TOI et demande-moi une capture couvrant toute la zone, avec son fichier .json d'emprise (nord, sud, est, ouest). Ne fabrique pas de fond.
- 0,5–3,5 s : le circuit 1 se dessine à vitesse constante avec la tête lumineuse (comme dans plan7). À 3,5 s : « CIRCUIT 1 · 7,2 km » apparaît près du tracé (valeur lue dans chiffres_circuits.json).
- 3,5–6,5 s : le circuit 2 se dessine de la même façon. À 6,5 s : « CIRCUIT 2 · 4,2 km ».
- 7,0 s : le total « 11,4 km » apparaît en grand, avec le libellé « D'AVENUES ÉCLAIRÉES », et reste en pleine lumière jusqu'à la fin (2 s).
- Mention « Imagery © Google, Airbus » en bas à droite, 14 px, 60 % d'opacité, pendant toute la séquence.

## Contrôles avant de livrer
- Compte les images : 144 et 216 exactement.
- Vérifie que la dernière image de ouverture_globe.mp4 et la première de ouverture_circuits.mp4 sont identiques (différence de pixels nulle ou quasi nulle).
- Vérifie que chaque événement tombe sur un multiple de 12 images.
- Montre-moi les deux planches d'aperçu, puis livre les fichiers et liste ce que tu n'as pas pu vérifier.
```
