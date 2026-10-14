# Prompt de démarrage pour Claude Code

Ouvre Claude Code dans le dossier `Eclairage_public` et colle :

```
Lis CLAUDE.md en entier : c'est l'état du projet et toutes les décisions prises. Puis :

1. Vérifie l'environnement : ffmpeg, Python 3 avec Pillow et numpy, la police Inter (dis-moi où elle est installée pour la variable INTER_DIR), Node et Playwright pour le globe. Installe ce qui manque en me demandant d'abord.
2. Vérifie que les rushes d'origine sont dans sources/ sous les noms attendus. S'ils manquent, demande-les-moi.
3. Relance scripts/montage_v2.py puis scripts/son_v2.py, pour t'assurer que tu reproduis la V2 à l'identique (53 s, 27 coupes). Montre-moi la planche d'aperçu.
4. Produis l'ouverture (globe puis circuits) en suivant docs/PROMPT_claude_code_globe.md.
5. Écris scripts/montage_v3.py selon la structure V3 de CLAUDE.md, en réutilisant les fonctions de montage_v2.py. Calcule la nouvelle liste de coupes et régénère le son sur cette grille. Montre-moi la planche (une image par temps) avant le rendu complet.

Pose-moi une question seulement si la réponse change le résultat. Ne fabrique aucun chiffre.
```
