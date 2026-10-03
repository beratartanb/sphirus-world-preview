# GUARDIAN-14b: nose-tip identity correction (clay, before rig)

Date: 2026-10-03. Status: **STOP FOR USER REVIEW.** No auto-rig was run, nothing was promoted, and the hair, outfit and skin were not touched.

- **Protected folders:** all 26 protected groups are byte-identical (`data/preservation_check.json`).
- **New sculpt:** `Saved/Codex/CharacterGuardian14_20261003/head_K5.npy`.
- **Rigged GD14 face:** K2 is unchanged.

## Diagnosis: history comparison

Midline profile and tip measurements (`data/tip_measurements.txt`):

| Sculpt | Tip projection from subnasale | Tip width 8 mm behind the tip | Columella base z |
|---|---|---|---|
| GD13c HS3 | 1.80 cm | 2.01 cm | 157.32 |
| GD14 K2 | **1.57 cm** | **2.34 cm** | 157.32 |
| **NEW K5** | 1.77 cm | 2.03 cm | 157.32 |

**What GD14's nose-base transfer changed at the tip:**
- Tip lost 2.3 mm of projection.
- Tip widened by 3.3 mm and flattened.
- Supratip dropped (159.5–159.75: 15.11 → 14.98).
- Lower lobule went in (158.5: 15.08 → 14.86).

**Compared with Tier A (front and verified 3/4, boards A, B, E):**
- **Old HS3 tip was closer on:** projection and the rounded, fleshy lobule. The Tier A tip is a full, rounded lobule that projects forward and slightly down in 3/4.
- **K2 was closer on:** nothing at the tip. The K2 tip reads flatter and more generic.

## Method

`tools/blender_gd14_tiprestore.py` computes `new = K2 + W · LP₁₀(HS3 − K2)`.

- **Low-frequency only:** only the low-frequency tip volume (10 umbrella iterations) comes from HS3, so none of the old crease or curl detail returns.
- **Mask W:**
  - Covers tip, lobule and supratip only.
  - Fades out at |x| 1.0 → 1.7 cm (alae excluded).
  - Height ramp z 157.95 → 158.9 at the bottom and 160.0 → 161.0 at the top.
  - Front of the nose only.
  - Down-facing surfaces fade out, so nostril roofs, sill and columella base stay K2.
- **Lobule shaping:** a small fleshy-lobule fullness of +0.46 mm, lobule widening of 0.6 mm per side, and the tip moved forward/down by 0.8 mm, followed by a light relax (`data/lobule_ops_L5.json`).

**Rejected variants:**

| Variant | Why rejected |
|---|---|
| k = 40 / 80 low-pass | Too smooth; only about 0.7 mm of projection came back |
| t2 (k = 10, short lower ramp) | Left a ridge across the lower lobule |
| t3 (included the infratip underside) | The lobule hung over the nostrils (hanging infratip) |
| K3 / K4 | Correct direction but too subtle |

**Movement checks:**
- Max movement 2.1 mm.
- 0 mm outside the nose (|x| > 2.2, z > 161 or z < 157.3).
- 0 mm on eyes, teeth and mouth.
- Nostril interior at most 0.17 mm.
- Columella base unchanged.

## Gates

| Gate | Result |
|---|---|
| NOSTRIL FORM | PASS |
| ALAR RIM | PASS |
| NOSE BASE PRESERVATION | PASS |
| TIP PROJECTION | PARTIAL |
| TIP WIDTH | PARTIAL |
| TIP ROTATION | PARTIAL |
| LOBULE FORM | PARTIAL |
| SUPRATIP | PARTIAL |
| INFRATIP | PARTIAL |
| COLUMELLA | PARTIAL |
| NOSE FRONT IDENTITY | PARTIAL |
| NOSE 3Q IDENTITY | PARTIAL |
| NOSE PROFILE COHERENCE | PASS |

### Honest read

**Better than K2:**
- The tip has a rounded, fleshy lobule again and projection is back near HS3 (1.77 vs 1.80 cm). The 3/4 view (boards B, E) is closer to Tier A.
- The tip, alae and nostrils still read as one structure, with no "M" notch.
- From below (board D) the GD14 nostrils are unchanged: open, unrolled rim, columella and sill intact.
- The profile (board C) is one continuous line, with a rounder tip and no step.

**Still another nose in front:**
- **Proportion:** in the Tier A front the tip lobule is broad relative to the alae, and the nostrils show only as two small dark dots under the tip. In ours the alae still flare wider than the tip, and the nostril openings/sills are visible as dark slits at the alar base.
- **Why it is not a tip fix:** that proportion is alar flare and nostril exposure, which this pass was told not to change.
- **Next step:** reduce the alar flare and nostril show slightly while keeping the base topology, then rig once.

## Boards (`boards/`)

| Board | Content |
|---|---|
| A | NOSE FRONT: REFERENCE / GD13c HS3 / GD14 K2 / NEW |
| B | NOSE 3/4: REFERENCE / HS3 / K2 / NEW |
| C | NOSE PROFILE: HS3 / K2 / NEW, plus close-ups (Tier B aid only) |
| D | NOSE BASE FROM BELOW: K2 / NEW |
| E | TIP / SUPRATIP CLOSE-UP: REFERENCE / K2 / NEW, front + 3/4 |
