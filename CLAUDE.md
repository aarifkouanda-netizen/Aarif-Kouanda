# Film « L'allumage » — éclairage public, Ouagadougou

Contexte du projet pour Claude Code. Lis ce fichier en entier avant toute action.

## Qui, quoi
- Amar, architecte et artiste 3D à Ouagadougou. Échanges en français ; prompts de génération d'images et de vidéos en anglais.
- Objet : un film de présentation (≈ 60 s, 16:9, 1920×1080, 24 i/s) du remplacement des lampadaires sur **deux circuits** de Ouagadougou, par un lampadaire décoratif à double crosse et couronne découpée au laser rétroéclairée LED.
- Thèse : **« Deux circuits, une nuit rendue à la ville. »** Concept de montage : **chaque coupe est un interrupteur.**

## État au 14 octobre 2026
| Élément | État | Fichier |
|---|---|---|
| Plans de nuit (IA, Seedance via Magnific, 1080p, 5 s) | ✅ validés | `nuit/C1-S1…C2-S1_nuit_seedance_v1.mov` |
| Plaques de jour correspondantes (16:9, 720p, 24 i/s, 5 s, pixels carrés) | ✅ | `plaques/` |
| Carte de synthèse des deux circuits (fond satellite, 10 s) | ✅ validée | `cartes/plan7_synthese_v3.mp4` |
| Montage V2 (53 s, 27 coupes sur 120 BPM) | ✅ livré | `film_eclairage_v2.mp4` (racine du dossier), script `scripts/montage_v2.py` |
| Piste son provisoire générée par code | ✅ | `son/v2_son.wav`, script `scripts/son_v2.py` |
| Ouverture globe → Ouagadougou → circuits | ⏳ à faire | prompt : `docs/PROMPT_claude_code_globe.md` |
| 5 gros plans produit à caméra fixe + 1 plan de vie | ⏳ à générer dans Magnific | voir « À produire » |
| Montage V3 (nouvelle structure ci-dessous) | ⏳ à faire | — |

Correspondance des segments :
- **C1-S1** : avenue aux drapeaux (grands arbres, haie sur le terre-plein, panneau OMS). Les drapeaux et la haie ont disparu dans la version IA.
- **C1-S2** : boulevard Capitaine Thomas Sankara, carrefour avec feux.
- **C1-S3** : boulevard Capitaine Thomas Sankara, ligne droite, palmiers sur le terre-plein.
- **C2-S1** : Ouaga 2000, avenue vers le Monument des Héros nationaux (monument dans l'axe).

Rushes d'origine (de jour, tournés au téléphone en voiture) à placer dans `sources/` sous ces noms exacts, car `montage_v2.py` les lit :
- `Ensemble_1_-_2_minutes_-_version_nettoyee.mp4` (circuit 1, 1920×584, 30 i/s, sans son)
- `Circuit_complet_-_1_min_30_-_variations_de_vitesse.mp4` (circuit 2, 1396×584, 30 i/s, avec des rampes de vitesse)
Recadrage 16:9 utilisé : circuit 1 `crop=1038:584:371:0`, circuit 2 `crop=1038:584:180:0`.

## Chiffres (ne jamais en inventer)
- Circuit 1 : **7,2 km**. Circuit 2 : **4,2 km**, dont environ 1,9 km d'anneau autour du monument. Total : **11,4 km**.
- ⚠️ **Question ouverte** : y a-t-il des lampadaires sur l'anneau du rond-point ? Si non, le circuit 2 fait environ 2,3 km et le total environ 9,5 km : mettre à jour `chiffres_circuits.json` et tous les textes.
- Nombre de lampadaires : **inconnu**. Ne jamais l'afficher tant qu'il n'est pas fourni.
- Fiche produit (catalogue fournisseur) : mât acier galvanisé 10 à 12 m, portée totale des crosses 4,5 m, socle ajouré éclairé 1,3 m, motif découpé au laser et rétroéclairé LED, pose sur terre-plein central. La page du catalogue ne doit jamais apparaître à l'écran.

## Charte
- Couleurs : anthracite RAL 7016 `#383E42` (fonds de carte), gris aluminium RAL 9006 `#A5A5A5` (contexte), or RAL 1003 `#F9A800` (circuits, points, accents), blanc cassé `#F0F0EC` (texte). Fond des plans graphiques `#1B2023`.
- Police : **Inter** (Bold et SemiBold pour les titres, Regular pour le texte). Les mots arrivent par un glissement de 24 px en 4 images, sans fondu, et partent net.
- Étalonnage commun des plans vidéo : noirs relevés vers l'anthracite, vignettage léger ; sur les plans Seedance, `deband` + grain léger (le ciel a des bandes de compression).
- **Interdits** (retenus de prompt-motion.com) : fondus enchaînés, halos et lueurs, particules, anneaux qui s'étendent, dégradés décoratifs, rebonds, tremblement de caméra, texte dans les coins, temps mort de plus d'1 s sans texte à lire, et tout ce qui ressemble à un modèle tout fait.
- **Fil conducteur** : un point or qui porte les transitions. Ouagadougou sur le globe devient la fenêtre de la carte, puis une tête LED, puis la dernière lampe allumée.

## Grille de temps
Musique à **120 BPM** : 1 temps = 0,5 s = **12 images**, 1 mesure = 2 s. Toute coupe et tout événement visible tombent sur un multiple de 12 images. Le son provisoire est généré sur la même grille (`son_v2.py` lit la liste des coupes).

## Structure V3 validée par Amar (≈ 60 s)
| Temps | Séquence | Matière |
|---|---|---|
| 0–6 s | **Le globe** : rotation vers l'Afrique, le Burkina passe en or, plongée, point or sur Ouagadougou | à produire, voir `docs/PROMPT_claude_code_globe.md` |
| 6–15 s | **Les circuits** : le point s'ouvre sur la vue satellite, circuit 1 puis circuit 2, total | idem (une seule vue satellite couvrant les deux circuits) |
| 15–23 s | **Le jour** : rafale de 4 à 6 plans de jour de 1,5 s, accélérés ×2, désaturés à 50 %, sans texte | `sources/` |
| 23–30 s | **La bascule** : 0,5 s de noir et de silence, clac, le point or devient une tête LED (C2-S1 de nuit, 2 s), puis le **volet unique** avant/après sur C1-S1, ralenti à 50 % (4 s), avec « AVANT »/« APRÈS » portés par le trait | `nuit/`, `plaques/` |
| 30–40 s | **Le produit** : 5 détails de 2 s (couronne, crosse, mât, socle, mât entier) avec un mot sur le temps | aujourd'hui des recadrages de plans de nuit ; à remplacer par les gros plans à caméra fixe |
| 40–55 s | **La ville la nuit** : coupes quand un mât passe au même endroit du cadre, ralenti à 40 % au passage d'une couronne, compteur « KM ÉCLAIRÉS » qui monte par paliers, « CIRCUIT 1 » / « CIRCUIT 2 » | `nuit/` |
| 55–60 s | **La fin** : « DEUX CIRCUITS, UNE NUIT RENDUE À LA VILLE », puis tout s'éteint sauf une lampe | `nuit/` |

Plus de carte de synthèse à la fin : les circuits sont présentés au début.

Points de coupe repérés dans les clips de nuit (temps dans la source) :
- C1-S3 : 0,0–2,0 et 2,5–4,5 (mât proche à 2,0 s et 4,25 s) ; gros socle éclairé à 2,0 s ; couronne nette à 0,75 s.
- C1-S2 : 1,0–3,0 et 3,25–4,75.
- C1-S1 : 1,9–3,05 à vitesse normale, puis 3,05–3,59 ralenti à 40 % (la couronne passe en grand) ; mât entier net à 2,5 s ; couronne et crosses nettes à 3,25 s.
- C2-S1 : 2,0–4,0 (monument dans l'axe) ; 0,0–1,0. Éviter 1,0–1,25 (saut dans la source).

## À produire (côté Amar, dans Magnific, modèle Seedance)
- **5 gros plans produit de nuit, caméra fixe**, image vers vidéo à partir d'images clés Nano Banana tirées de `refs/REF_lampadaire.png` et `refs/REF_couronne.png` : couronne qui s'allume, crosse et tête LED, contre-plongée sur le fût, socle ajouré, mât entier sur le ciel à l'heure bleue.
- **1 plan de vie** : motos et piétons sous la lumière, sur une des avenues.
- Règles apprises : plaque, images clés et sortie **au même format (16:9) et à la même durée** ; pixels carrés ; prompt Kling/Seedance de 2 500 caractères maximum ; **Seedance** tient le dessin du produit, pas Kling.

## Encore attendu d'Amar
- La réponse sur l'anneau du rond-point (voir Chiffres).
- Le nom du maître d'ouvrage et les logos (le carton de fin affiche aujourd'hui un emplacement entre crochets).
- La musique définitive, libre de droits, et environ 3 min d'ambiance de rue de nuit enregistrées au téléphone.
- Les rushes du circuit 2 à vitesse normale, sans rampes.

## Méthode de travail
- Avant tout rendu complet : une planche d'aperçu avec une image par temps (toutes les 12 images), à montrer à Amar.
- Ne jamais présenter un défaut comme réglé sans l'avoir vu sur une image extraite.
- Garder les rendus dans `rendus/`, versionnés (`film_eclairage_v3.mp4`, …).
