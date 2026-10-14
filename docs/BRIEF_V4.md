# Brief V4 — « L'allumage », version dynamique

Base : `rendus/film_eclairage_v3.mp4` (60 s, 26 coupes). Charte, chiffres et structure de CLAUDE.md inchangés :
pas de fondu, de halo, de particule, de rebond ni de tremblement ; mots qui glissent de 24 px en 4 images ;
tout événement sur un multiple de 12 images (120 BPM) ; le point or porte les transitions.

## Diagnostic de la V3 (mesures sur le master)
| Moment | Défaut | Mesure |
|---|---|---|
| 0–1 s | Globe petit, presque immobile : l'accroche tarde | mouvement 0,0–0,7 |
| 6,5–15 s | Carte figée 8,5 s, circuits petits dans le cadre | mouvement 0,0–0,1 |
| 15,0 s | Saut brutal carte sombre immobile → rushes de jour clairs et agités, sans lien | 0,0 → 12,2 |
| 30–34 s, 36–38 s | Produit en images fixes agrandies (flou), textes posés sur le sujet | 0,5–1,1 |
| 40–55 s | Compteur « KM ÉCLAIRÉS » trop petit pour un téléphone | 24 px |
| 55–58,5 s | Fin sur image fixe, titre petit près d'un coin | 0,3–0,4 |

## Carte des temps V4
| Temps | Séquence | Ce qui change |
|---|---|---|
| 0–6 s | Globe | Le globe tourne déjà à la première image (plus de seconde morte). |
| 6,0–6,5 s | Fenêtre | Inchangé : la fenêtre s'ouvre autour du point or. |
| 6,5–9,5 s | Circuit 1 | **La caméra suit la lumière** : plongée sur le circuit 1 (zoom ×2 environ), le cadre accompagne la tête du tracé ; « CIRCUIT 1 » à 6,5 s, « · 7,2 km » à 9,5 s. |
| 9,5–10,0 s | Bascule vers le sud | Glissé rapide vers le circuit 2, flou de mouvement. |
| 10,0–12,5 s | Circuit 2 | Zoom sur le rond-point, avenue nord puis anneau dans les deux sens ; « CIRCUIT 2 » à 10 s, « · 4,2 km » à 12,5 s. |
| 12,5–13,0 s | Recul | La caméra recule sur les deux circuits. |
| 13,0–14,5 s | Total | « 11,4 km D'AVENUES ÉCLAIRÉES » arrive sur le temps ; lente poussée vers l'avenue du circuit 1. |
| 14,5–15,0 s | Plongée | Plongée accélérée sur l'avenue du circuit 1 jusqu'au niveau de la rue. |
| 15,0 s | **Raccord** | Coupe à pleine vitesse dans le rush de jour roulant sur cette même avenue : la plongée devient la marche avant. |
| 15–23 s | Le jour | **Rafale qui accélère** : plans de 2 · 1,5 · 1,5 · 1 · 1 · 0,5 · 0,5 s (×2, désaturés à 50 %), jusqu'au silence. |
| 23–30 s | Bascule | Inchangée (noir, clac, point → tête LED, volet avant/après), avec une lente poussée pendant le volet. |
| 30–40 s | Le produit | Chaque détail sur image **qui bouge** : 0,5 s à vitesse réelle puis ralenti à 15 % avec poussée vers le détail ; le mot arrive sur le temps, du côté opposé au sujet. (En attendant les gros plans Magnific.) |
| 40–55 s | La ville | Mêmes coupes ; compteur agrandi, chiffres qui défilent à chaque palier. |
| 55–58,5 s | La fin | Sur image qui bouge (C1-S1, lente poussée), titre en grand sur deux lignes, les mots montent sur les temps. |
| 58,5–60 s | Extinction | Inchangée : tout s'éteint sauf une lampe. |

## Technique
- Carte : fond satellite en pleine résolution (8104 px, 2,6 m/px) pour zoomer jusqu'à ×3,5 sans flou ; caméra en
  segments adoucis, zoom interpolé en échelle logarithmique ; flou de mouvement par sous-images sur les
  mouvements rapides seulement.
- Raccord carte → rue : coupe au pic de vitesse, même sens de mouvement des deux côtés.
- Rythme du jour : nouveaux points d'entrée dans les rushes choisis sur la planche, coupes sur la grille.
- Contrôles à chaque étape : planche une image par temps, mesure du mouvement (aucune seconde figée hors
  noir voulu et extinction finale), contrôle des sauts d'image, critique notée.

## Réalisé (V4 rendue le 14 octobre 2026)
Écarts au plan, pour que chaque chiffre reste lisible avant que la caméra reparte : « · 7,2 km » à 9,0 s,
glissé 9,5–10,0 s, « CIRCUIT 2 » à 10,0 s, « · 4,2 km » à 12,0 s, recul 12,5–13,0 s. Produit : couronne puis
crosses en un seul mouvement de 4 s (plus de coupe à 32 s), mât remonté du pied au sommet, socle suivi, acier
révélé en reculant. 27 coupes.

Mesure du mouvement (même méthode que la V3) : plus aucune seconde figée hors extinction finale (V3 : 17) ;
carte 0,2–8,2 (V3 : 0,0–0,1) ; raccord à 15 s 5,5 → 12,2 (V3 : 0 → 12) ; produit 1,2–13,9 (V3 : 0,5–1,1) ;
fin 0,9–1,4 (V3 : 0,3–0,4).

Pistes pour une V5 : accroche des 3 premières secondes (globe encore petit) ; étiquettes de la carte à
agrandir pour le téléphone ; plan de jour de 17 s très agité ; musique définitive et ambiance de rue ;
gros plans produit Magnific à la place des recadrages.

## V5 : l'existant en noir et blanc (demande d'Amar, 14 octobre 2026)
Amar valide la V4 et demande d'améliorer les images de l'existant (« un peu floues ou trop exposées ») et de les
passer en gris. Seules changent les images de jour : rafale de 15 à 23 s et côté « AVANT » du volet (26–29 s).
Coupes, durées, textes et son inchangés.

Traitement (`scripts/existant.py`), un réglage par plan calculé sur quelques images (pas de scintillement) :
débruitage léger avant l'agrandissement, noir et blanc façon filtre orange (le voile bleuté du ciel s'assombrit),
noir au 0,5e centile relevé à 7 % (anthracite), blanc au 99,7e centile plafonné à 92 %, gamma qui ramène la valeur
moyenne vers 45 %, courbe en S douce, netteté adaptée à l'agrandissement ×1,85, grain fin déterministe.

Plan remplacé : C2 à 72 s → C2 à 13 s (approche du monument, motos). De 17 s à la fin, le rush du circuit 2 porte
un reflet fixe du tableau de bord sur la chaussée, que le contraste rend visible ; un retrait par médiane temporelle
n'en enlève qu'une partie (le reflet change de forme avec le soleil).
