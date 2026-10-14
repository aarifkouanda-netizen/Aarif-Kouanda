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
- Carte : fond satellite gardé à 6000 px (3,5 m/px) pour zoomer jusqu'à ×2,3 sans flou ; caméra en
  segments adoucis, zoom interpolé en échelle logarithmique ; flou de mouvement par sous-images sur les
  mouvements rapides seulement.
- Raccord carte → rue : coupe au pic de vitesse, même sens de mouvement des deux côtés.
- Rythme du jour : nouveaux points d'entrée dans les rushes choisis sur la planche, coupes sur la grille.
- Contrôles à chaque étape : planche une image par temps, mesure du mouvement (aucune seconde figée hors
  noir voulu et extinction finale), contrôle des sauts d'image, critique notée.
