# GUARDIAN-13c: localized sculpt of the nose base and perioral region (clay, before rig)

Date: 2026-10-03. Status: **STOPPED FOR USER REVIEW.** No auto-rig was run, the hair is paused, and nothing was promoted.

- **Protected folders were not modified:** all 25 protected groups are byte-identical (`data/preservation_check.json`).
- **Rollback baseline:** F3 (`hs/head_F3_baseline.npy`). The result is **HS3**.

## Method change

As instructed, there were no further normal-offset or height-fill iterations.

**New tool:** `tools/blender_gd13_hand.py`. It is the scripted equivalent of Blender sculpt-mode **mask + grab/move + smooth** with *connected / topology* falloff.

**How a stroke works:**
- **Mask:** seeds are chosen by region plus surface-normal direction, for example "the medially-facing inner wall of the ala".
- **Move:** the seeds move by a drag vector, mirrored on both sides.
- **Falloff:** influence spreads only along the connected surface, using geodesic distance over mesh edges (Dijkstra). A grab on the alar rim therefore can't drag the columella or nostril interior across the opening, which is what crumpled F1 and F2.

**Protected:**
- The global zone limits all edits to the nose base and perioral region.
- Jaw/chin (z < 153.2), nose dorsum (z > 159.7), eyes, teeth and the mouth interior.
- In the mouth zone every back-facing surface: the lip seam and inner lips.

**Verified movement:** eyes 0 mm, jaw 0 mm, teeth/inner mouth 0 mm, dorsum 0 mm. Mouth half-width is unchanged at 3.836 cm.

**Review views per stroke:** front, verified 33° 3/4 and profile, plus new close-up renders (`tools/blender_gd13_closeup.py`) from below, front, 3/4 and side.

## Nose base (`data/N4.json`)

**Diagnosis from the close-ups:**
- From below, the nostrils were narrow diagonal slits.
- The alar lobule curled in toward the columella.
- From the front, the nose base read as an "M": a notch where tip and ala meet, with the lobule hanging as a separate loop.

**Strokes:**
- Unroll the alar rim: lower rim only, the medial-facing inner wall moved 1.5 mm outward and 0.5 mm down. A first version (N2/N3) also moved the upper nostril arc and left a visible pit on the upper ala in 3/4, so that version was rejected.
- Hold the upper nostril arc in place.
- Lower the lower alar edge by 0.8 mm toward the tip line.
- Lower the soft triangle by 0.6 mm.
- Reduce the lateral alar bulge by 0.8 mm.
- Smooth the rim and the upper lobule, and round the rim edge.

**Result:**
- **From below:** the nostrils are now open teardrops instead of slits.
- **Front:** the alar lower edge now forms one continuous arch with the tip, and the "M" notch is mostly gone.
- **3/4:** a light shadow remains on the upper lobule.
- **Profile:** unchanged.

## Perioral (`data/L3.json`)

- Lower lip tapered laterally into the corners: back 1.2 mm, up 0.4 mm.
- Lateral lower border trimmed.
- Modiolus mound built forward by 0.8 mm, so the corner sits embedded in the face.
- Upper lip tapered laterally.
- Sublabial continuity improved.
- Perioral ring smoothed, plus a local smooth of a notch at the end of the lower lip.

**Result:** in front and 3/4 the lower lip no longer ends as a separate pill-shaped volume; it dissolves into the corners. The lip seam, mouth width and lip-to-teeth clearance are unchanged.

## Gates

| Gate | Result |
|---|---|
| NOSTRIL FORM | PARTIAL |
| ALAR UPPER FORM | PARTIAL |
| NOSE BASE INTEGRATION | PARTIAL |
| PHILTRUM-TO-UPPER-LIP | PARTIAL |
| UPPER-LIP FORM | PARTIAL |
| LOWER-LIP FORM | PARTIAL |
| PERIORAL INTEGRATION | PARTIAL |
| MOUTH NATURALNESS | PARTIAL |

### Honest read

**Clearly better than F3:**
- **Nose base:** open nostrils and a continuous alar-tip arch in front.
- **Lips:** the lower lip no longer ends abruptly, and the mouth corners are embedded.

**Not yet at the reference:**
- **Alar lobule:** it still reads as a defined, rounded loop compared with the reference's soft, flat ala, and a light shadow remains on the upper lobule in 3/4.
- **Lips:** still more sharply drawn at the vermilion border than the reference.

## Boards (`boards/`)

| Board | Content |
|---|---|
| A | NOSTRIL CLOSE-UP: REFERENCE (front photo) + F3 / HAND-SCULPT from below and front |
| B | NOSE BASE FRONT: REFERENCE / F3 / HAND-SCULPT |
| C | NOSE BASE 3/4: REFERENCE / F3 / HAND-SCULPT, plus close-ups 3/4 and profile |
| D | LIP CORNER / MODIOLUS: front + 3/4 |
| E | FULL PERIORAL REGION: front + 3/4 + profile |
