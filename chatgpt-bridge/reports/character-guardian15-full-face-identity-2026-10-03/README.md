# GUARDIAN-15: full-face identity rebuild (clay, before rig)

Date: 2026-10-03. Status: **STOP FOR USER REVIEW.**

- **Not done in this pass:** no auto-rig, no hair, no skin, no body or clothing changes, nothing promoted.
- **Protected folders:** all 27 protected groups are byte-identical (`data/preservation_check.json`), including GD14.
- **Sculpt:** baseline GD14b **K5**, new sculpt **N1** (`Saved/Codex/CharacterGuardian15_20261003/head_N1.npy`).

## What still read as "another woman" (diagnosed before sculpting)

Measured in the same Tier A camera frame with MetaHuman tracker curves, plus silhouette overlays (`data/image_ratios.json`, boards 04/05):

| Ratio (front) | Tier A | K5 | N1 |
|---|---|---|---|
| Eye→stomion / IPD | **1.153** | 1.073 | 1.115 |
| Eye→alar base / IPD | 0.520 | 0.500 | **0.520** |
| Inner canthal / IPD | 0.538 | 0.545 | 0.527 |
| Mouth / IPD (clay) | 0.855 | 0.853 | 0.899 |

1. **The eyes are set wider than Tier A.** In the identical camera framing the vertical eye→mouth distance matches Tier A (199 vs 203 px), but our IPD is 9 % wider (189 vs 173 px) and the inner-canthal gap 11 % wider. That makes the face read narrower and more central. It is also why "mouth too narrow" appeared: the mouth was being measured against a too-wide IPD. This was the single largest generic-MetaHuman trait left.
2. The cheek architecture is concentrated near the nose; the zygoma doesn't carry toward the ear.
3. The lower face tapers into a V: lean lower cheek, prejowl/marionette groove, pointed chin.
4. The brow band sits slightly high and straight.
5. The midface is flat in profile.

## N1 edits (`data/ops/P1-P3.json`; tools `blender_gd15_ops.py`, `blender_gd15_ipd.py`)

The K5 nose was frozen with an explicit nose mask: max change on the nose is 0.4 mm, from the general softening only. Tip, nostrils, alae, columella and sill are unchanged.

| Pass | Edit |
|---|---|
| **A** lower cheek | Lower-cheek tissue widened up to +1.5 mm per side with wide ramps; the jaw border at the angle is unchanged |
| **B** zygoma / malar | Zygoma reach +2.0 mm outward and +0.8 mm up toward the ear; malar apex moved lateral, forward and up (+1.0 / +0.6 / +0.5 mm) |
| **C** midface | Anterior midface +1.2 mm forward; lateral maxilla / lip support +0.7 mm |
| **D** chin / lower face | Prejowl / marionette grooves filled (≤1.2 mm); chin point −0.7 mm; lateral chin-pad fullness; chin-pad and labiomental softening; lower-jaw soft tissue around the chin widened (chin pad 7.62 → 7.99 cm) |
| **E** mouth | Corners +0.5 mm per side and relaxed |
| **F** brow | Brow skin band −1.2 mm with the arch peak kept and the tail −0.5 mm (less straight); brow shelter +0.5 mm forward |
| **G** softness | Remaining sculpt high-frequency reduced 25 % (eyelids, lip seam and nose kept) |
| **Eye set** | Evidence-based, not a random move: each eye assembly (eyeball, shell, lashes, edge) plus the orbit tissue moved **1.2 mm medially**, with a smooth radial field around each orbit. The midline is fixed. IPD 5.95 → 5.71 cm. |

**3D measurements** (`data/face_measurements.txt`):

| Measure | K5 | N1 |
|---|---|---|
| Bizygomatic | 14.34 | 14.74 |
| Width at z 156 | 13.29 | 13.58 |
| Mouth-level face width | 12.99 | 13.29 |
| Width / height | 1.305 | 1.341 |
| Mouth width | 5.31 | 5.39 |
| Mouth / IPD | 0.893 | 0.943 |

- The real-render lip-colour ratio was 0.818 at K2. Scaled by the new mouth width and IPD it should land around **0.86** (Tier A 0.855). This is to be confirmed after the rig.
- Unchanged: cranium (≤0.8 mm at the low forehead from the brow band), jaw lower border (≤0.05 mm), teeth and mouth interior.

## Gates

| Gate | Result |
|---|---|
| FACE WIDTH / HEIGHT | PARTIAL |
| FRONT SILHOUETTE | PARTIAL |
| 3Q SILHOUETTE | PARTIAL |
| ZYGOMATIC ARCH | PARTIAL |
| ZYGOMATIC LATERAL REACH | PARTIAL |
| MALAR POSITION | PARTIAL |
| MALAR PROJECTION | PARTIAL |
| MIDFACE DEPTH | PARTIAL |
| MAXILLA SUPPORT | PARTIAL |
| LOWER-CHEEK TISSUE | PARTIAL |
| CHIN-PAD FULLNESS | PARTIAL |
| MOUTH WIDTH | PARTIAL |
| MOUTH CORNERS | PARTIAL |
| UPPER LIP | PARTIAL |
| LOWER LIP | PARTIAL |
| PERIORAL INTEGRATION | PARTIAL |
| BROW POSITION | PARTIAL |
| BROW SHAPE | PARTIAL |
| EYE / ORBIT CHARACTER | PARTIAL |
| UPPER-LID CHARACTER | PARTIAL |
| LOWER-LID CHARACTER | PARTIAL |
| JAW / CHIN PRESERVATION | PASS |
| CRANIUM PRESERVATION | PASS |
| K5 NOSE PRESERVATION | PASS |
| IDENTITY FRONT | PARTIAL |
| IDENTITY 3/4 | PARTIAL |
| IDENTITY PROFILE | FAIL |
| OVERALL FACE GATE | FAIL |

### Honest read

**Better than K5 (boards 01, 02, 04, 10, 11):**
- The face reads broader and softer.
- The lower face is no longer a V: the chin pad is wider and the groove beside the mouth is gone.
- The cheeks carry further toward the ears.
- The closer-set eyes remove some of the generic MetaHuman spacing.
- The front and 3/4 silhouettes sit closer to the Tier A outline at cheek and mouth level.

**Still not the same woman:**
- **Vertical proportion:** Tier A's eye→mouth distance relative to IPD is still longer (1.153 vs 1.115). Her lower face, philtrum and mouth sit lower relative to the eyes.
- **Brows:** they can't be judged in clay. Brow hair only shows after the rig with the groom, so BROW stays PARTIAL until a real render.
- **Eyes:** the Tier A eye is smaller and more sheltered. Our fissures still read long in clay.
- **Profile:** the midface is still flatter than Tier A suggests.

**Open decisions for you:**
1. **Eye set:** keep the 1.2 mm medial eye move (recommended: it is the biggest identity lever measured), or return to the K5 IPD.
2. **Vertical proportion:** lower the mouth/chin rhythm by about 1.5–2 mm to close the remaining eye→mouth gap.

After approval: one fresh auto-rig, then a real-render check of brows, mouth width and eyes, then the rig test.

## Boards (`boards/`)

| Board | Content |
|---|---|
| 01 | FRONT_FULL_FACE |
| 02 | 3Q_FULL_FACE |
| 03 | PROFILE_FACE |
| 04 | FRONT_SILHOUETTE_OVERLAY |
| 05 | FACE_WIDTH_HEIGHT |
| 06 | ZYGOMATIC_FRONT |
| 07 | ZYGOMATIC_3Q |
| 08 | MALAR_POSITION |
| 09 | MIDFACE_DEPTH |
| 10 | LOWER_CHEEK_TISSUE |
| 11 | CHIN_PAD |
| 12 | MOUTH_WIDTH |
| 13 | FULL_PERIORAL |
| 14 | BROW_POSITION |
| 15 | EYE_BROW_ORBIT |
| 16 | FULL_CLAY_FRONT |
| 17 | FULL_CLAY_3Q |
| 18 | FULL_CLAY_PROFILE |

Comparisons are REFERENCE (Tier A) | BASELINE (GD14b K5) | NEW (GD15 N1); boards 16–18 have no labels.
