# Prompt Claude Code — cartes animées des circuits d'éclairage public

À coller dans Claude Code, lancé dans un dossier qui contient :
- `circuits/` : le ou les fichiers `.kmz` ou `.kml` exportés de Google Earth (chemins des circuits, repères des lampadaires si disponibles)
- `fonds/` (facultatif) : captures satellite **sans libellés**, chacune avec ses coordonnées d'emprise (voir §6)
- `render_cartes_v1_reference.py` : la version 1, tracée à la main, qui sert de référence de style

---

```
Tu vas produire les plans de carte animés d'un film de présentation : remplacement des lampadaires d'éclairage public sur deux circuits à Ouagadougou (Burkina Faso). Une version 1 existe dans render_cartes_v1_reference.py : tracés relevés à la main sur des captures. Lis-la d'abord ; elle fixe le style. Ta mission : refaire ces plans à partir des vrais fichiers KMZ/KML du dossier circuits/, avec la géométrie réelle et des chiffres calculés.

## 1. Lecture des données
- Ouvre chaque .kmz (c'est un zip contenant un .kml) ou .kml du dossier circuits/. Parse le XML (xml.etree ou fastkml), sans dépendance lourde.
- Extrais : les LineString (tracés, un par branche), avec leur nom et le nom du dossier parent ; les Point (repères : lampadaires ou lieux).
- Liste ce que tu as trouvé (noms, nombre de points par tracé, nombre de repères) et demande-moi de confirmer quel élément appartient au circuit 1 et lequel au circuit 2, et quels repères sont des lampadaires. Ne devine pas.

## 2. Calculs
- Projection : Web Mercator (EPSG:3857) ou équirectangulaire locale centrée sur chaque circuit. Les distances se calculent en haversine sur les coordonnées WGS84 d'origine, pas sur la projection.
- Pour chaque circuit : longueur totale en km (1 décimale), longueur par branche, nombre de lampadaires si les repères existent, interdistance moyenne.
- Écris ces chiffres dans chiffres_circuits.json et affiche-les-moi. Si les lampadaires ne sont pas pointés, ne fabrique AUCUN nombre : la carte n'affiche alors que la longueur.

## 3. Charte (identique à la v1)
- Fond RAL 7016 anthracite #383E42 ; routes de contexte RAL 9006 #A5A5A5 à faible opacité ; circuits RAL 1003 #F9A800 avec un halo flou (glow) ; texte blanc cassé #F0F0EC.
- Police Inter (SemiBold pour les titres en capitales, Regular pour le texte, Medium pour les étiquettes). Chiffres en tabulaires.
- 1920×1080, 24 i/s, H.264 CRF 14, yuv420p, pixels carrés (setsar=1). Rendu suréchantillonné ×2 puis réduit (anticrénelage).
- Aucune étiquette ne chevauche un tracé : vérifie-le sur l'aperçu et décale l'étiquette si besoin.

## 4. Plans à produire
1. plan5a_circuit1.mp4 — 4 s. Fond qui apparaît (0–0,5 s), tracé qui se dessine à VITESSE CONSTANTE (0,5–3 s), tête lumineuse blanche au bout du trait pendant le dessin, repères qui apparaissent (fondu + glissement de 12 px, décalés de 0,12 s), titre « CIRCUIT 1 » + sous-titre, puis longueur en km et nombre de lampadaires s'il est connu (compteur qui défile de 0 à la valeur).
2. plan6a_circuit2.mp4 — 4 s, même grammaire. Le rond-point du Monument des Héros nationaux est dessiné en cercle.
3. plan7_synthese.mp4 — 10 s. Les deux circuits côte à côte. Si les lampadaires sont pointés : chaque point s'allume dans l'ordre du parcours (0,08 s d'écart, petit flash puis lueur stable). Sinon : une lumière balaie les tracés. Titre « DEUX CIRCUITS, UNE NUIT RENDUE À LA VILLE », puis les chiffres totaux à 6,8 s. Fondu de sortie sur la dernière seconde.
4. minicarte_C1.mov et minicarte_C2.mov — vignettes 480×480 avec canal alpha (ProRes 4444), tracé du circuit, et un point qui avance le long du tracé, pour l'incrustation en coin des plans de route. Durée et position de départ et d'arrivée en paramètres (je les fixerai segment par segment).

## 5. Contexte géographique
Ajoute quelques repères fixes pour situer : pour le circuit 1, l'aéroport (piste) et le CHU ; pour le circuit 2, le Monument des Héros nationaux, le Palais de Kossyam et le boulevard des Tensoba. Si le KMZ ne contient pas les routes de contexte, dessine uniquement les repères ; n'invente pas de rues.

## 6. Fond satellite (facultatif, seulement si fonds/ contient des images)
Chaque image a un fichier .json de même nom avec son emprise {"nord":…, "sud":…, "est":…, "ouest":…} en degrés. Cale l'image par ces coordonnées, assombris-la vers la nuit (exposition −1,5 IL, teinte vers #383E42, désaturation 60 %), pose les tracés exactement dessus, ajoute un zoom lent de 3 % sur la durée du plan et la mention « Imagery © Google » en bas à droite, en 14 px, à 60 % d'opacité.

## 7. Méthode
- Un seul script Python paramétrable (render_cartes_v2.py), avec ffmpeg via subprocess. Pas de navigateur, pas d'After Effects.
- Avant le rendu complet : exporte une image d'aperçu par plan (à 85 % de la durée), regarde-la, corrige les chevauchements, puis seulement lance les vidéos.
- À la fin : liste des fichiers produits, chiffres_circuits.json, et les points que tu n'as pas pu vérifier.
```
