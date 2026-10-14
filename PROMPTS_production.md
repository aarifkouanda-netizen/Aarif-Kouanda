# PROMPTS DE PRODUCTION — standard validé sur le test C2-S1

## Réglages fixes (tous les segments)
- Plaque : `..._plaque_16x9_720p_5s.mp4` (16:9, 1280×720, pixels carrés, 24 i/s, 5 s)
- Nano Banana : format **16:9** (jamais carré)
- Kling O1 Edit : 16:9 · 5 s · Image 1 = clé nuit · Image 2 = `REF_lampadaire.png` · Image 3 = `REF_couronne.png`
- Prompt Kling : 2500 caractères maximum

## Ligne « mâts existants » à insérer, par segment

| Segment | À coller à la place de [EXISTING] |
|---|---|
| C1-S1 avenue aux drapeaux | `The existing poles are red-and-white striped poles with a double head, standing in the planted median; two national flags hang from each pole. Each new pole keeps the two flags at the same height.` |
| C1-S2 bd Thomas Sankara (carrefour) | `The existing poles are tall grey Y-shaped double-arm poles in the centre of the median. The traffic lights stay unchanged.` |
| C1-S3 bd Thomas Sankara | `The existing poles are tall grey Y-shaped double-arm poles in the centre of the median, some with an advertising panel; the new poles carry no panel.` |
| C2-S1 (fait) | `The existing poles are tall plain grey poles with a small double head in the centre of the paved median.` |

---

## Étape 1 — Nano Banana, clé JOUR (entrées : image1 du segment + REF_lampadaire)
```
You are retouching a real photograph of an existing avenue in Ouagadougou, taken from a car. Keep the exact framing, road, kerbs, median, buildings, trees, billboards, vehicles and sky.

[EXISTING] Count them. Replace each one, at exactly the same position and height, with the street light of the reference image: light-grey steel pole, square gold lattice base, thin gold strip up the shaft, two long thin grey arms curving far left and right to flat rectangular LED heads, and between them an open crown of thin grey ribs holding perforated gold lattice panels: a small diamond on top, two large blades crossing in an X, two smaller side blades. New, clean, no rust.

Same daylight as the photograph.

KEEP EXACTLY:
- number and position of poles
- road geometry, vehicles, buildings, signs

AVOID:
- extra poles, poles off the median
- text, logos on the poles
- changing the sky or time of day
- tulip, flower or palm shapes
```

## Étape 2 — Nano Banana, clé NUIT (entrées : clé jour validée + REF_lampadaire)
```
You are relighting a real photograph of an existing avenue in Ouagadougou. Nothing moves or changes shape; only the time of day changes.

Blue hour, twenty minutes after sunset, dry season: deep cobalt sky fading to a thin warm pink-orange band at the horizon. All decorative street lights on the median are on: each LED head throws a clear pool of neutral-white light on the asphalt, darker road between pools; the gold lattice glows softly from within, its holes readable. Vehicle lights on. Facades in soft shadow, a few windows lit warm.

KEEP EXACTLY:
- every pole, position and shape
- road geometry, vehicles, buildings, trees

AVOID:
- wet road, flares, haze, black night, moon
- text or billboards changing
```

## Étape 3 — Kling O1 Edit (Vidéo = plaque · @Image1 = clé nuit · @Image2 = REF_lampadaire · @Image3 = REF_couronne)
```
Edit real footage of an avenue in Ouagadougou filmed from a moving car. Keep the exact frame, camera motion, road, buildings, trees and vehicles of @Video. No car interior or windshield. Poles are rigid and anchored in the median.

[EXISTING]

EDIT: replace every street-light pole on the median, without exception, with the street light of @Image2, at the same position as each original pole. Turn the scene into the blue hour, matching @Image1. No original pole remains.

PRODUCT, exactly as @Image2 and @Image3: light-grey steel pole, square gold lattice base, thin gold strip up the shaft. Two long thin grey arms curve far left and right to flat rectangular LED heads; the span is much wider than the crown. Open airy crown of thin grey curved ribs: small gold diamond on top, two large gold blades crossing in an X, two smaller side blades, all perforated lattice glowing warm. Not a tulip, not palm leaves.

LIGHT: deep cobalt sky, thin warm band at the horizon. Each LED head throws a visible, stable pool of neutral-white light on the asphalt, darker road between poles. Vehicle lights on. No flicker.

KEEP EXACTLY:
- first frame matches @Image1
- number of poles at every moment, as in @Video
- camera path and speed

AVOID:
- tulip, flower or palm shapes, short arms
- any original pole left
- uniformly lit road without light pools
- poles sliding, bending or appearing at frame edges
- flickering lattice, wet road, flares
```
