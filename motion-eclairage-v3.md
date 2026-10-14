# MOTION — ÉCLAIRAGE PUBLIC, DEUX CIRCUITS
### motion-eclairage-v3 — 13 octobre 2026 (dérushage circuit 1 §11, circuit 2 §12)

---

## 0. HYPOTHÈSES À CORRIGER

| # | Hypothèse | Si elle est fausse |
|---|---|---|
| H1 | Les nouveaux mâts remplacent les anciens **sur le terre-plein central**, aux mêmes emplacements (la fiche indique une pose sur refuge central). | Si les anciens sont en rive et les nouveaux au centre, il faut retirer puis ajouter : c'est plus risqué, et on découpe des segments plus courts. |
| H2 | Montage final dans **DaVinci Resolve** (gratuit). Magnific sert à la génération, à l'upscale et à l'audio ; son éditeur sert au dérushage. | Si tu as After Effects, la carte et la typographie s'y font, et Resolve sert au montage. |
| H3 | Usage : présentation au maître d'ouvrage, 16:9, 1080p, 24 i/s, environ 90 s. | Pour un appel d'offres, ajouter un carton de chiffres ; pour les réseaux, prévoir un dérivé en 9:16 de 30 s. |
| H4 | Têtes LED en blanc neutre, environ 4000 K ; décor doré rétroéclairé en blanc chaud. | À vérifier sur la fiche photométrique : cela change les prompts de nuit. |

---

## 1. THÈSE

**Le même trajet, la nuit rendue à la ville.**

On ne vend pas un poteau, on montre une avenue qui devient praticable et lisible après 19 h. Le lampadaire est un personnage secondaire, présenté une fois, clairement. Ensuite, c'est la route qui parle.

**Fil graphique :** l'or du décor découpé au laser (RAL 1003) devient la couleur des circuits sur la carte. Le produit et le territoire partagent une seule couleur.

---

## 2. DIAGNOSTIC DE PRODUCTION

1. **Tournage de jour, rendu voulu de nuit.** On demande donc au modèle deux transformations à la fois : remplacer les mâts et changer l'heure. Chacune est faisable ; les deux ensemble multiplient la fonte. Méthode : **image clé jour validée, puis image clé nuit validée, puis vidéo**. On ne saute jamais une étape.
2. **Heure bleue plutôt que pleine nuit.** Environ 20 minutes après le coucher du soleil, le ciel garde un dégradé, les façades restent lisibles et le bruit de capteur reste supportable. En pleine nuit, la vidéo d'un téléphone convertie par l'IA produit une bouillie noire avec des halos. L'heure bleue est aussi l'image la plus vendeuse d'un projet d'éclairage.
3. **Téléphone en voiture.** Il faut s'attendre à des secousses, du rolling shutter et des reflets de pare-brise. Il faut **stabiliser avant l'IA**, car le modèle amplifie le tremblement. Retenir les lignes droites et éviter les virages, en particulier le tour du rond-point des Héros, où la parallaxe fera glisser les mâts.
4. **Kling O1 Edit (dans Magnific)** prend une vidéo source avec du texte et jusqu'à 4 images de référence. Il conserve le mouvement et la caméra de la source, ce qui rend possible l'avant/après synchronisé. Il fonctionne par **segments de 3 à 10 s**. Le modèle rend en 60 i/s : il faudra conformer en 24 i/s au montage.
5. **Coût.** La grille affichée sur Magnific donne environ 150 crédits par seconde en 1080p avec vidéo de référence. Pour 40 s de route conservées dans le film, avec trois essais par segment, on arrive à environ **18 000 crédits** pour la seule étape vidéo. C'est le poste qui pèse : on ne génère que les segments retenus au découpage.
6. **Marques tierces.** La fiche fournisseur ne doit jamais apparaître à l'écran : ni la page, ni son titre, ni sa mise en page. Le produit est remodélisé dans 3ds Max et présenté avec notre typographie.

---

## 3. PIPELINE

| Étape | Outil | Sortie |
|---|---|---|
| 1. Dérushage, sélection des lignes droites de 5 à 10 s | Resolve ou éditeur Magnific | Liste de segments (voir §4) |
| 2. Stabilisation, correction du rolling shutter, recadrage léger | Resolve (Stabilizer) | Plaques propres en 1080p |
| 3. Extraction de la **première image** de chaque segment | Resolve | PNG |
| 4. Image clé **jour** : remplacement des mâts | Nano Banana Pro (Magnific), mode Transformation, créativité basse | Validée par comptage |
| 5. Image clé **heure bleue** à partir de l'image validée en 4 | Nano Banana Pro | Validée |
| 6. Vidéo : plaque + image clé nuit + fiche produit | Kling O1 Edit (Magnific), 1080p | Segment nuit |
| 7. Vérification image par image (première, médiane, dernière ; comptage des mâts) | Resolve | Prise retenue ou rejetée |
| 8. Upscale éventuel | Magnific Upscaler vidéo | 4K si nécessaire |
| 9. Produit : modélisation et animation | 3ds Max + Corona | Plans 3D (§4, plans 4a à 4d) |
| 10. Carte vectorielle et tracés | Illustrator, puis Resolve Fusion ou AE | Plans de carte |
| 11. Montage, étalonnage, son, typographie | Resolve | Master |

---

## 4. DÉCOUPAGE (≈ 92 s, 30 i/s — cadence de la source)

| # | Rôle | Durée | Caméra | key_motion | Source | Son |
|---|---|---|---|---|---|---|
| 1 | Ouvrir | 3 s | Fixe | Noir, puis un seul point doré s'allume | Fusion/AE | Ville de nuit au loin, contacteur sec |
| 2 | Situer | 8 s | Zoom lent | Ouaga en satellite étalonné nuit ; les deux circuits se tracent en or | Capture satellite + AE | Ambiance nocturne |
| 3 | Constat | 7 s | Plaque route (avance) | Les vieux mâts défilent, image désaturée | Rush original stabilisé | Moteurs deux-temps |
| 4a | Révéler le produit | 6 s | Fixe | Allumage séquencé : socle, fût, palmes, puis têtes | 3ds Max | Un clac par allumage |
| 4b | Montrer | 6 s | Orbite lente à 30° | Rotation de la caméra autour du mât allumé | 3ds Max | Grave sourd |
| 4c | Détail matière | 3 s | Travelling latéral lent | La lumière traverse le motif découpé | 3ds Max | — |
| 4d | Spécifier | 3 s | Fixe | Cotes animées : 10–12 m, 4,5 m, RAL | 3ds Max + typo | — |
| 5a | Situer le circuit 1 | 4 s | Fixe sur carte | Le tracé en L se dessine ; nom, longueur, nombre de points | Carte vectorielle | — |
| 5b | Avant/après | 8 s | Plaque route | **Volet** jour → nuit synchronisé | Rush + Kling O1 Edit | Bascule d'ambiance : jour puis nuit |
| 5c | Habiter | 6 s | Plaque route | Motos et piétons dans les flaques de lumière | Kling O1 Edit | Motos, radio d'un kiosque |
| 6a | Situer le circuit 2 | 4 s | Fixe sur carte | La croix centrée sur le Monument des Héros se dessine | Carte vectorielle | — |
| 6b | Approcher | 7 s | Plaque route | Ligne droite vers le rond-point, mâts allumés | Kling O1 Edit | Ambiance large |
| 6c | Avant/après | 7 s | Plaque route | Volet sur l'axe Kossyam | Rush + Kling O1 Edit | — |
| 7 | Conclure | 10 s | Dézoom lent | Les deux cartes ; les points s'allument un par un ; chiffres clés | Carte vectorielle | Contacteurs en rythme, puis silence |
| 8 | Signer | 5 s | Fixe | Maître d'ouvrage, logos, date | Typo | Ambiance qui s'éteint |

**Tempo :** coupe sur le mouvement de la plaque, jamais au milieu d'un mât qui passe. Les cartes respirent, les routes avancent. L'alternance carte, puis route, puis carte est la ponctuation du film.

**Segments à extraire de tes rushs :** 1 ligne droite « avant » par circuit, 3 segments circuit 1 (branche ouest-sud vers l'aéroport, branche est vers le CHU), 3 segments circuit 2 (approche nord, approche sud vers Kossyam, une branche est ou ouest). Huit segments de 5 à 10 s au total.

---

## 5. CHARTE

- **Couleurs tirées du produit :** RAL 7016 anthracite `#383E42` pour les fonds de carte, RAL 9006 aluminium `#A5A5A5` pour les routes secondaires, RAL 1003 jaune signal `#F9A800` pour les circuits, les points lumineux et les chiffres. Le blanc sert uniquement au texte courant.
- **Typographie :** une seule famille sans empattement technique, au choix Inter ou IBM Plex Sans (je tranche pour Inter), en deux graisses. Titres en capitales espacées +80, chiffres en tabulaires.
- **Carte :** routes principales redessinées en vectoriel dans Illustrator à partir de tes captures. Sans aucune étiquette Google : on ne garde que les repères utiles (Monument des Héros nationaux, Kossyam, aéroport, CHU). Si on garde l'image satellite au plan 2, la mention « Imagery © Google » reste visible.
- **Points lumineux :** un point par mât, placé selon le **plan d'implantation**. On ne pose jamais un nombre « à peu près ».

---

## 6. PROMPTS

### 6.1 Image clé jour — remplacement (Nano Banana Pro, Transformation, créativité basse)

Entrées : première image du segment + fiche produit recadrée sur le mât (sans texte).

```
You are retouching a real photograph of an existing road in Ouagadougou,
taken from a car. The road, kerbs, central median, buildings, trees,
vehicles and sky are already correct and must not change.

Count the existing street-light poles on the central median in the
photograph. Replace each one, at exactly the same position, with the
decorative street light shown in the reference image: a single
light-grey galvanised steel pole 10 to 12 metres tall, with a square
gold-coloured laser-cut lattice base about 1.3 metres high, a thin
vertical gold lattice strip running up the shaft, and at the top two
long curved arms sweeping left and right like palm fronds, each ending
in a flat rectangular LED road luminaire, with four pointed gold
laser-cut lattice leaves set between the arms. Total arm span 4.5
metres, arms perpendicular to the road. New poles are new: clean
edges, no rust, no dust.

Same daylight, same shadows direction as the photograph; each new pole
casts a shadow consistent with the existing ones.

KEEP EXACTLY:
- number of poles counted on the median
- spacing and position of every pole
- road geometry, lane markings, kerbs, median width
- every vehicle, person, building, tree, sign

AVOID:
- additional poles, poles in the carriageway or on the pavement
- text, logos, banners, brand names
- changing the sky, the season or the time of day
- extra decoration, flags, flowers on the poles
```

**Validation :** compter les mâts sur l'original et sur le résultat. Vérifier qu'aucun mât n'apparaît au bord du cadre et que l'orientation des bras est cohérente d'un mât à l'autre.

### 6.2 Image clé heure bleue (Nano Banana Pro, à partir de 6.1 validée)

```
You are relighting a real photograph of an existing road in
Ouagadougou. Nothing in the scene moves or changes shape: only the time
of day changes.

Make it the blue hour, about twenty minutes after sunset in the dry
season: deep cobalt sky fading to a thin warm orange band at the
horizon, a few flat-bottomed clouds still faintly lit from below. All
decorative street lights on the median are switched on: each flat LED
luminaire casts a neutral-white pool of light onto the asphalt below,
the pools overlapping slightly between poles; the gold laser-cut
lattice leaves, shaft strip and base glow softly from within in warm
white, their pattern readable. Vehicles have headlights and red tail
lights on. Building facades fall into soft shadow, a few windows and a
kiosk lit warm.

KEEP EXACTLY:
- every pole, its position and shape, as in the photograph
- road geometry, vehicles, buildings, trees

AVOID:
- wet road, rain, reflections on dry asphalt
- lens flares, starbursts, bloom haze over the whole image
- full black night, moon, stars
- text, logos
- changing the number or position of any pole
```

### 6.3 Segment vidéo (Kling O1 Edit dans Magnific, 1080p)

Entrées : **@Video** = plaque stabilisée (5–10 s) · **@Image1** = image clé 6.2 validée · **@Image2** = mât de la fiche, recadré sans texte.

```
You are editing real footage of an existing road in Ouagadougou, filmed
from a car moving slowly forward. The camera motion, the road, the
buildings, the trees and every vehicle keep exactly the motion and
position they have in @Video. The poles are rigid, heavy, perfectly
still objects anchored in the median.

THE EDIT: replace every street-light pole on the central median with
the decorative street light shown in @Image2, at exactly the same
position as each original pole, and turn the scene into the blue hour,
matching @Image1 in sky, light and colour.

THE LIGHT: deep cobalt sky, thin warm band at the horizon. Each LED
luminaire casts a stable neutral-white pool on the asphalt; the gold
lattice leaves, shaft strip and base glow softly and steadily. Car and
motorbike lights on. The light does not flicker and does not change
during the clip.

KEEP EXACTLY:
- the number of poles visible at every moment, as in @Video
- pole spacing, which stays constant as the car advances
- camera path and speed
- road geometry, lane markings, vehicles and their motion

AVOID:
- poles sliding, bending, melting, multiplying or appearing at the
  edge of frame
- arms changing shape from one pole to the next
- flickering lattice pattern
- wet road, flares, haze
- text, logos, signs changing
```

**Vérification :** première, médiane et dernière image ; comptage des mâts sur les trois ; lecture à 25 % de vitesse en surveillant les bords de cadre et le motif doré. Une prise belle où un mât glisse est rejetée.

### 6.4 Produit — 3ds Max (pas d'IA)

- Modélisation depuis la fiche : fût conique, deux bras en courbe (spline + sweep), quatre feuilles en plaque. Le motif découpé au laser se fait en carte d'opacité + émissive sur un plan, pas en géométrie : c'est plus léger et sans scintillement.
- **4a Allumage :** fond noir, sol réfléchissant mat, keyframes d'émissive à 0,5 s d'intervalle : socle, fût, feuilles, têtes. Caméra fixe en contre-plongée légère.
- **4b Orbite :** 30° en 6 s, ease in/out, focale 50 mm.
- **4c Détail :** travelling latéral de 40 cm devant une feuille, focale 85 mm, faible profondeur de champ.
- **4d Cotes :** plan fixe de face, cotes et RAL posés au montage (pas dans le rendu).

---

## 7. CARTE ANIMÉE

1. Dans Illustrator, sur tes deux captures : redessiner les avenues principales (trait 9006), les deux circuits (trait 1003, plus épais) et les repères. Supprimer tout le reste.
2. **Circuit 1** : point de départ au carré rouge, branche ouest puis sud jusqu'à l'aéroport, branche est jusqu'au CHU. **Circuit 2** : croix centrée sur le rond-point du Monument des Héros nationaux, nord jusqu'au boulevard des Tensoba, sud jusqu'au Palais de Kossyam, branches est et ouest.
3. Exporter les tracés en SVG, puis les animer en Trim Paths (AE) ou avec un tracé animé dans Fusion. Le tracé avance à vitesse constante, pas en ease : il raconte un parcours.
4. Points lumineux : un calque par mât, allumage décalé le long du tracé (0,08 s entre deux points).
5. **Je peux écrire le script** qui place automatiquement les points sur le tracé à partir du nombre de mâts et de l'interdistance (Python vers SVG, ou expression AE).

---

## 8. MONTAGE, ÉTALONNAGE, SON

- **Conformation :** timeline en 30 i/s (cadence des rushs) ; les segments Kling sont convertis de 60 en 30 i/s *avant* étalonnage. Les plaques jour et nuit doivent rester image par image alignées pour le volet.
- **Volet avant/après :** ligne verticale fine en 1003, vitesse constante, de gauche à droite en 2 s, au milieu du segment.
- **Étalonnage :** une seule courbe pour toute la pièce. Les noirs sont relevés vers le bleu-anthracite (7016) et non vers le noir pur. Les hautes lumières des têtes LED restent neutres et ne virent pas à l'orange.
- **Son :** enregistre 3 minutes d'ambiance au téléphone, de nuit, sur chacun des circuits. Retiens trois couches au maximum : moteurs deux-temps lointains, grillons, radio d'un kiosque. Un contacteur sec synchronisé sur chaque allumage. Pas de musique de banque ; si tu tiens à un fond, un drone grave de Magnific Audio, très bas.
- **Typo :** titres et chiffres en fondu + glissement de 12 px, 8 images. Aucun texte ne passe sur un mât.

---

## 9. CORRECTIONS PRÊTES

```
[Poles sliding / multiplying]
The poles are fixed to the ground and do not move relative to the road.
Keep exactly the number of poles of the source video at every frame.
No pole appears or disappears except by entering or leaving the frame
as the car advances.
```
```
[Melting arms / inconsistent shape]
Every pole is an identical copy of @Image2: same arm curve, same four
lattice leaves, same luminaires. The arms are rigid steel and never
bend or ripple.
```
```
[Flickering lattice]
The gold lattice glows with constant intensity. Its pattern is fine
and stable; no shimmer, no change between frames.
```
```
[Light changes during clip]
The time of day is fixed: blue hour, constant for the whole clip. Sky
brightness, colour and light pools do not change.
```
```
[Too dark / mush]
Raise the sky to a clear medium cobalt; facades remain readable in
soft shadow; keep detail in the asphalt between light pools.
```
```
[Wet road / glare]
The asphalt is dry and matte; light pools are soft-edged on a dry
surface, no specular reflections, no lens flares.
```
```
[Vehicles morphing]
Vehicles keep the exact shape, colour and motion of @Video; only their
lights are switched on.
```
```
[Text / signs appearing]
No new text, sign or logo anywhere. Existing road signs keep their
shape; their text is not altered.
```
**Fallback si la double transformation fond :** deux passes Kling O1 Edit. Passe 1, le remplacement en jour (prompt 6.3 sans THE LIGHT) ; validation ; passe 2, passage à l'heure bleue sur la vidéo validée.

---

## 10. AUTOCRITIQUE (référence : série image SAHA pour les critères communs)

| Critère | Note | Commentaire |
|---|---|---|
| Thèse formulée | 8 | Claire ; le fil couleur produit-territoire la sert bien. |
| Rôle par plan | 8 | 5c et 6b sont proches : à arbitrer au montage selon les rushs. |
| key_motion nommé | 9 | Chaque plan a le sien. |
| Un mouvement par plan | 9 | Les plaques imposent le travelling avant ; rien d'autre n'est ajouté. |
| Verrouillage architecture | 7 | Comptage et vérification prévus, mais la parallaxe d'une voiture reste un terrain dur. |
| Lumière spécifiée | 8 | Heure bleue décrite ; la température des LED reste à confirmer (H4). |
| Contexte en items concrets | 6 | Peu de contexte urbain nommé dans les prompts : à enrichir une fois les rushs vus. |
| Rythme chiffré | 9 | Toutes les durées sont données. |
| Son pensé | 8 | Dépend d'un enregistrement de nuit sur place. |
| Faisabilité avec les outils | 6 | Coût en crédits élevé, et rushs de téléphone non encore vus. |

**Faiblesse principale :** la conversion jour → nuit sur des rushs de téléphone en mouvement. Tout le film repose sur 5b et 6c. **Premier test à faire avant toute autre production :** un seul segment de 5 s, passé par les étapes 6.1 → 6.2 → 6.3. S'il tient, on lance le reste ; s'il fond, on passe au compositing 3D sur tracking pour les deux plans d'avant/après uniquement.

---

## 11. DÉRUSHAGE — CIRCUIT 1 (`Ensemble_1_-_2_minutes_-_version_nettoyee.mp4`)

### 11.1 Fiche technique de la source

| Paramètre | Valeur | Conséquence |
|---|---|---|
| Définition | **1920 × 584** (≈ 3,29:1) | Trop large pour un modèle vidéo. On recadre en **2,39:1** (1396 × 584, remis à 1920 × 804) ; le film adopte un cadre cinémascope dans le 16:9. |
| Cadence | 30 i/s, 117 s, 3518 images | Timeline en 30 i/s. |
| Son | Aucune piste | L'ambiance de nuit est à enregistrer (§8). |
| Traitement | Image déjà « nettoyée » : lissage type peinture à l'huile sur les arbres, halos d'accentuation, saturation forte | Le modèle va amplifier ces artefacts. **Les rushs originaux non traités sont préférables.** |
| Pare-brise | Bande irisée dans le ciel (moitié gauche, de 1:00 à 1:40), traces d'essuie-glace en bas de l'image, reflets du tableau de bord (0:40–0:52) | Le ciel sera remplacé à la nuit, donc l'irisation disparaît. Les traces du bas restent : on recadre légèrement le bas. |
| Fondus internes | 26,6 s · 33,4 s · 54,7 s · 61,8 s · 103,6 s | Aucun segment ne doit chevaucher un fondu. |

### 11.2 Lecture des tronçons

| Temps | Tronçon | Éclairage existant | Usage |
|---|---|---|---|
| 0:00–0:26 | Avenue Kwame Nkrumah (centre, terre-plein planté de palmiers) | Luminaires surtout sur poteaux bois du réseau, pas de mâts réguliers au centre | **Constat (plan 3)** uniquement. H1 n'y est pas vérifiée : il faudrait *ajouter* des mâts, pas les remplacer. |
| 0:26–0:34 | Carrefour giratoire, arrêt au feu avec motos au premier plan | — | Écarté. |
| 0:34–0:54 | Avenue aux drapeaux (terre-plein avec haie, passages piétons) | Mâts à deux têtes **sur le terre-plein**, drapeaux nationaux accrochés | Segment S1. H1 vérifiée. Décision à prendre : garder les drapeaux sur les nouveaux mâts ou non. |
| 0:55–1:44 | Boulevard Capitaine Thomas Sankara (panneau vu à 1:06), large, rectiligne | Mâts en Y à deux crosses **sur le terre-plein central**, interdistance régulière | **Meilleur tronçon du circuit.** Segments S2, S3, S4. H1 vérifiée. |
| 1:44–1:57 | Échangeur et virage, puis avenue avec glissière | — | Écarté (virage = parallaxe). |

### 11.3 Segments retenus

| Code | In → Out | Durée | Plan du découpage | Remarque |
|---|---|---|---|---|
| C1-S0 | 0:08 → 0:14 | 6 s | 3 Constat | Avenue vivante, voiture devant : garder tel quel, désaturé. |
| C1-S1 | 0:38 → 0:46 | 8 s | 5c Habiter | Motos dans l'axe, drapeaux ; reflets du tableau de bord en bas à recadrer. |
| C1-S2 | 1:17 → 1:24 | 7 s | 5b Avant/après (variante) | Palmier au premier plan à 1:25 : couper avant. Panneau tordu par le rolling shutter à 1:26. |
| **C1-S3** | **1:28 → 1:36** | **8 s** | **5b Avant/après — SEGMENT TEST** | Rectiligne, trafic faible, mât proche avec panneau d'affichage qui sort du cadre : c'est le cas le plus dur, donc le bon test. |
| C1-S4 | 1:39 → 1:43 | 4 s | Réserve | Court, mais propre. |

### 11.4 Plaque test livrée

- `C1-S3_plaque_239x1.mp4` : 1:28 → 1:36, stabilisée (vidstab, lissage 30, zoom 4 %), recadrée en 2,39:1, 1920 × 804, 30 i/s, 240 images. **À utiliser en priorité.**
- `C1-S3_image1_239x1.png` : première image, entrée de l'étape 6.1.
- `C1-S3_plaque_16x9_1080p.mp4` + `C1-S3_image1_16x9.png` : variante 16:9 si Magnific refuse le 2,39:1. Agrandissement ×1,85, donc plus molle.

### 11.5 Ajouts aux prompts pour le circuit 1

À insérer dans le paragraphe de remplacement des prompts 6.1 et 6.3 :

```
The existing poles are tall grey steel poles with a Y-shaped double
arm, standing in the centre of the planted median at a regular
interval. Some carry a rectangular advertising panel bolted to the
shaft; the new poles carry no panel at all.
```

À ajouter à AVOID (6.1, 6.2, 6.3) :

```
- advertising panels, posters or faces on the new poles
- rainbow-coloured streaks in the sky
```

Pour le segment S1 (avenue aux drapeaux), si on garde les drapeaux :

```
Each new pole keeps the two national flags hanging from a short
bracket at mid-height on the shaft, as on the original pole.
```

---

## 12. DÉRUSHAGE — CIRCUIT 2 (`Circuit_complet_-_1_min_30_-_variations_de_vitesse.mp4`)

### 12.1 Fiche technique de la source

| Paramètre | Valeur | Conséquence |
|---|---|---|
| Définition | 1396 × 584 (2,39:1) | Déjà au bon cadre. Les plaques sont remises à 1920 × 804. |
| Cadence | 30 i/s, 90 s, 2700 images, pas de son | Identique au circuit 1. |
| Rampes de vitesse | Accélérations et ralentis dans tout le montage | **Problème pour l'IA** : un ralenti par interpolation crée des images fantômes que Kling va figer en artefacts, et une rampe dans un segment rend le comptage des mâts imprévisible. |
| Image | Surexposée, laiteuse, dominante jaune, ciel brûlé | Plaque test légèrement corrigée (contraste +12 %, gamma 0,88) pour que le modèle lise mieux la géométrie. Le ciel brûlé n'est pas un problème : il sera remplacé. |
| Pare-brise | Reflets du tableau de bord en bas (0:16–1:16), fines rayures | Recadrer le bas de 5 à 8 % si le reflet gêne. |
| Fondus internes | 16,8 s · 23,4 s · 39,6 s · 44,9 s · 48,8 s · 59,1 s · 70,1 s | Aucun segment ne chevauche un fondu. |

**Règle de production :** générer les plaques IA à **vitesse réelle** et appliquer les rampes **au montage**, sur la plaque jour et la plaque nuit à la fois. L'avant/après reste ainsi synchronisé.

### 12.2 Lecture des tronçons

| Temps | Tronçon | Éclairage existant | Usage |
|---|---|---|---|
| 0:00–0:16 | Axe à 2 × 2 voies vers le Monument des Héros nationaux, trafic moyen | Mâts hauts à petite tête double **sur le terre-plein central pavé**, alignés dans l'axe du monument | **Meilleur tronçon du circuit.** Plan 6b (Approcher) : le monument dans l'axe est le point de fuite du film. H1 vérifiée. |
| 0:16–0:46 | Voies périphériques, terrains vides, tours en chantier, un carrefour non revêtu à 0:24 | Rares, en rive | **À confirmer** : ne semble pas faire partie de la croix tracée en vert. Écarté pour l'instant. |
| 0:48–0:52 | Approche du rond-point, monument au fond | Mâts sur terre-plein | Réserve (plan court) ; le virage d'entrée dans le rond-point commence à 0:52. |
| 0:52–0:59 | Rond-point | — | Écarté (virage). |
| 0:59–1:09 | Voie à 2 × 1 voies **sans terre-plein**, monument dans l'axe, bâtiments à toitures rouges | Mâts simples **en rive gauche** | H1 **non vérifiée** : pas de refuge central, alors que la fiche du produit indique une pose sur refuge. À clarifier avec le projet. |
| 1:10–1:28 | Axe nord vers le boulevard des Tensoba, trafic, échangeur à 1:28 | Mâts sur terre-plein | Constat (avant) ou plan d'habiter ; trafic dense, minibus au premier plan à 1:20. |

### 12.3 Segments retenus

| Code | In → Out | Durée | Plan du découpage | Remarque |
|---|---|---|---|---|
| **C2-S1** | **0:05 → 0:13** | **8 s** | **6b Approcher — SEGMENT TEST** | Monument dans l'axe, mâts alignés sur le terre-plein. Un piéton se tient au pied d'un mât vers 0:08 : point de vigilance (morphing). |
| C2-S2 | 0:48 → 0:52 | 4 s | Réserve | Approche finale du rond-point. |
| C2-S3 | 1:00 → 1:05 | 5 s | 6c Avant/après, si H1 est confirmée ici | Sans terre-plein : à ne générer qu'après décision. |
| C2-S4 | 1:12 → 1:18 | 6 s | 3 Constat ou 5c | Trafic modéré. |

### 12.4 Plaque test livrée

- `C2-S1_plaque_239x1.mp4` : 0:05 → 0:13, stabilisée, contraste corrigé, 1920 × 804, 30 i/s, 240 images.
- `C2-S1_image1_239x1.png` : première image, entrée de l'étape 6.1.

Note : la plaque a été coupée dans le montage avec rampes. Si une rampe tombe dans cette fenêtre, refaire la plaque depuis le rush original à vitesse réelle.

### 12.5 Ajouts aux prompts pour le circuit 2

À insérer dans le paragraphe de remplacement des prompts 6.1 et 6.3 :

```
The existing poles are tall plain grey steel poles with a small
double-headed luminaire at the top, standing in a single row in the
centre of the paved median. The road leads straight toward a tall
pale monument on a roundabout at the end of the avenue: the monument
stays exactly as it is, the same size and shape, and is not lit
differently from the rest of the city.
```

À ajouter à KEEP EXACTLY :

```
- the monument at the end of the avenue, its silhouette and position
- the pedestrian standing on the median, with the same posture and
  position
```

À ajouter à AVOID :

```
- billboards changing text or image
- the monument glowing, floodlit, or changing shape
```
