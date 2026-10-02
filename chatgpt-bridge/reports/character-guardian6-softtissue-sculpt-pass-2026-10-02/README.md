# GUARDIAN-6: targeted soft-tissue sculpt pass (option A)

Date: 2026-10-02. Status: **STOPPED FOR USER REVIEW.** Nothing was promoted.

- **Starting point:** GUARDIAN-5 F5 (report commit 545d03d), used as a read-only baseline.
- **Candidate:** `/Game/Sphirus/CharacterLab/CharacterGuardian6_20261002/`.
- **Protected folders were not modified:** production and GUARDIAN 1–5. All 17 protected groups are byte-identical to the checkpoint (`data/preservation_check.json`).

The user chose option (a): a targeted Blender sculpt of the cheek fat pads, tear trough, nasolabial plane and nose tip, guided by Tier A overlays, followed by an auto-rig.

## Final GD6 candidate

| Part | Asset |
|---|---|
| Face | `Face/SKM_GD6_Face_s4`: fresh Epic auto-rig on the sculpted neutral S4 (`MHC/MHC_GD6_S4`, `MHC/DNA/MHC_GD6_S4_Head`). RigLogic, 858 morphs, 8 LODs. |
| Skin | GUARDIAN-5 k7, referenced read-only: `CharacterGuardian5_20261002/Skin/MI_LK_Face_*_VT_g5k7`, `MI_GD5_Body_k7`. |
| Hair | GUARDIAN-5 h6, referenced read-only. New bindings `Face/Bindings/GB_GD6_*_s4f`: hair, SlightArch brows, S_Thin lashes. |
| Expression, body, garments | `AS_GD6_RefExpression` QA pose. Body, Henley g17e and Chaos shorts m1 unchanged. |

## How the sculpt was done

"Hand-sculpt" here means art-directed sculpt brushes in Blender (`tools/blender_gd6_sculpt.py`), applied stroke by stroke and checked visually against the Tier A overlays at each step. It was not an interactive ZBrush-style session.

1. **Guide lines.** The Tier A front nasolabial tracker curves were back-projected through the solved camera onto the F5 surface (`data/ref_nasolabial_3d.json`). The far-side 3/4 line is occluded by the nose, so the front projection was used.
2. **Brushes**, in order (`data/ops/sculptS3.json` + `sculptS4lid.json`):

| Brush | Change |
|---|---|
| Nasolabial plane step along the reference lines | tanh profile, ±1.4 mm. The cheek side rises and the lip side drops, with no crease line. |
| Tear-trough transition | 1.1 mm soft trough with 0.5 mm of tissue above it; no bag |
| Malar fat pad deflation | −2.7 mm |
| Submalar plane | −1.7 mm |
| Lateral zygoma accent | +0.4 mm |
| Nose tip de-rotation | 1.4 mm down; columella lowered; lobule narrowed (scale 0.87); alae slimmed (width 3.36 → 3.11 cm) |
| Upper-lid weight above the lash line | L −0.7 mm, R −1.2 mm. Mid aperture L/R went from 1.07/1.23 to 1.00/1.11 cm. The heavier right side removes an asymmetry inherited from N7. |
| Local Taubin smoothing | over the cheek and nasolabial regions |

3. **Brush defect found and fixed.** The first strong pass showed a serrated nasolabial edge and a notch near the mouth corners: the per-vertex side sign flipped across polyline segments. Fixed by resampling and smoothing the guide line, using a continuous side direction, and fading the ends earlier.
4. **Jaw/chin lock kept.** Balance Δ is 0.9 / 5.1 / 0.8 px, menton 0 px from the midline (`data/jawbalance.txt`).

### Iterations

| Version | Result |
|---|---|
| S1 | First pass |
| S2 | Softer trough, nose slimmed. **Auto-rigged.** Barely visible in the real-skin studio render. |
| S3 | Stronger brushes plus the brush fix. **Auto-rigged** and compared with S2 under identical cameras and lights; better, so adopted. |
| S4 | S3 plus upper-lid weight. **Auto-rigged.** Final. |

That is **three** auto-rigs, not one. S2 alone was too weak to evaluate in real skin.

**Brows:** M_Natural brows were tried. They rendered thinner and lighter than SlightArch, while the reference brows are fuller and darker, so they were reverted.

## Verification

- **Rig (S4), 23 cases:** blink, single-eye blinks, gaze, brows, visemes and extremes. No cornea or lid penetration after the lid sculpt (board 18).
- **Joints vs F5:** eye-joint distance 5.898 cm (F5: 5.899). Mouth-corner joints 4.588 cm (F5: 4.604). 13 of 843 facial joints moved more than 1 mm.
- **Restart:** fresh-editor reopen (`data/reopen_check.json`). Face with DNA user data, 858 morphs, 8 LODs, MHC, expression, h6 grooms and four `s4f` bindings all load. Nothing was dirty before or after.
- **After-restart captures:** board 20.

## Measurements (`data/`)

| Measure | Tier A | GD5 F5 | GD6 S4 |
|---|---|---|---|
| Eye aperture (IPD, mesh curves) | 0.157 | 0.191 (1.21×) | 0.176 (1.12×) |
| Upper-lid mid aperture L / R (cm) | – | 1.073 / 1.227 | 1.004 / 1.110 |
| Alar width at 158 cm (cm) | – | 3.36 | 3.11 |
| Pronasale y / z (cm) | – | 15.02 / 159.26 | 15.04 / 159.19 |
| Mouth width (IPD) | 0.844 | 0.846 | 0.842 |
| Lower lip thickness (IPD) | 0.153 | 0.143 | 0.143 |
| Corner drop (IPD) | 0.039 | 0.032 | 0.024 |
| Jaw balance Δ upper / mid / lower (px) | 0 / 1 / 0 | 0.6 / 4.9 / 0.7 | 0.9 / 5.1 / 0.8 |
| Eye joint distance (cm) | – | 5.899 | 5.898 |

The nasolabial plane lifted the mouth corners slightly: corner drop went from 0.83 to 0.63 of Tier A. This is a known side effect for the next pass.

## Final gates

| Gate | Result |
|---|---|
| IDENTITY FRONT | PARTIAL |
| IDENTITY 3/4 | PARTIAL |
| IDENTITY PROFILE | PARTIAL |
| CRANIUM | PASS |
| EYE PLACEMENT | PASS |
| EYE AREA CHARACTER | PARTIAL |
| NOSE | PARTIAL |
| LIPS / MOUTH VOLUME | PARTIAL |
| JAW / CHIN BALANCE | PASS |
| SOFT-TISSUE AGE CHARACTER | PARTIAL |
| SKIN COLOUR | PARTIAL |
| SKIN TEXTURE | PARTIAL |
| SKIN MATERIAL RESPONSE | PARTIAL |
| HEAD / BODY SEAM | PARTIAL |
| HAIR FLOW | PARTIAL |
| HAIRLINE / TEMPLE | PARTIAL |
| BUN | PARTIAL |
| HAIR MATERIAL | PARTIAL |
| REFERENCE EXPRESSION | PARTIAL |
| RIG | PASS |
| LOD | PASS |
| RESTART | PASS |
| OVERALL FACE GATE | FAIL |
| OVERALL CHARACTER LIKENESS GATE | FAIL |

### Why

- **Soft-tissue age went from FAIL to PARTIAL.** The sculpted planes clearly change the clay read toward Tier A: flatter malar fat, a defined nasolabial plane, a tear-trough transition and a lower nose tip (boards 00a, 04, 05). Under gameplay and interior light they read in skin too (board 11). Under the soft, fill-heavy studio light with subsurface scattering, the real-skin difference from GD5 is still modest.
- **Eye area: PARTIAL.** The heavier upper lids reduce the wide-eyed, young read. The brows are still the SlightArch library groom, thinner than the reference's.
- **Overall: FAIL.** The face moved toward an adult, lived-in character, but it does not yet read as the same woman. The remaining gaps:
  - the brow groom;
  - nose-tip length and shape in 3/4;
  - the studio-light read of the planes;
  - skin micro-relief;
  - the seam arc;
  - hair dampness and weight.
- Skin, seam and hair are unchanged GD5 assets and keep the GD5 verdicts.

## Boards

| Group | Boards |
|---|---|
| Sculpt | 00a sculpt targets in clay (REF / F5 / S4, front and 3/4); 00b mesh-curve overlays and profile |
| Neutral face | 01 front, 02 3/4, 03 profile |
| Age and features | 04 age front, 05 age 3/4, 06 eye area, 07 nose, 08 lips |
| Skin | 09 macro, 10 micro, 11 lighting A–E, 12 seam |
| Hair | 13 front/3/4, 14 hairline, 15 bun |
| Expression and character | 16 reference expression, 17 full character |
| Verification | 18 rig, 19 LOD, 20 after restart |

Each board compares REFERENCE | GD5 | GD6 with identical cameras and lights.

## Suggested next pass

1. **Brows:** a custom brow groom or a re-grown library brow (fuller, darker, straighter, lower), which is a strong identity cue.
2. **Mouth corners:** restore the corner drop under the nasolabial plane.
3. **Nose:** tip length and definition in 3/4.
4. **Review lighting:** a reference-like key light (more directional, less fill) so planes read in lookdev, alongside the A–E set.
5. **Then** skin micro-relief, the seam arc, and hair dampness.
