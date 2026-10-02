# GUARDIAN-5: soft-tissue age, nose, lips, skin and hair refinement

Date: 2026-10-02. Status: **STOPPED FOR USER REVIEW.** Nothing was promoted.

- **Starting point:** GUARDIAN-4 E1 (report commit 8914968), used as a read-only baseline.
- **Candidate:** `/Game/Sphirus/CharacterLab/CharacterGuardian5_20261002/`.
- **Protected folders were not modified:** `MH_MainCharacter`, GUARDIAN 1–4 and `MetaHumans/Common`. All 16 protected groups are byte-identical to the checkpoint (`data/preservation_check.json`).

## Final GD5 candidate

| Part | Asset |
|---|---|
| Face | `Face/SKM_GD5_Face_f5`. Fresh Epic auto-rig on the corrected neutral F5 (`MHC/MHC_GD5_F5`, `MHC/DNA/MHC_GD5_F5_Head`): RigLogic, 858 morphs, 8 LODs. |
| Skin | `Skin/MI_LK_Face_*_VT_g5k7` and `Skin/MI_GD5_Body_k7`. Textures `T_LK_Head_{BC,N,SRMF}_k7b` and the body seam SRMF `T_LK_Body_SRMF_k7b`. |
| Hair | `Hair/GR_LK_Hair_{Main,Loose}_h6`, the h2 hierarchy refined. Bindings `Face/Bindings/GB_GD5_*_f5h6`. |
| Reference expression | `Face/Diagnostics/AS_GD5_RefExpression`, a separate QA pose. |
| Eyes, body, garments | Unchanged: GUARDIAN-3 e2 eye MIs (read-only), B2 body, Henley g17e, Chaos shorts m1. |

## Jaw / chin reference correction (user, mid-pass)

The user supplied a photo-space guide showing the Tier A front jaw/chin is **balanced**: Δ 0–1 px at three jaw levels against a fitted landmark midline.

- The old contour picks (jaw L 0.543 / R 0.641 IPD) were therefore wrong and are retired.
- A read-only check with the same method (`blender_gd5_jawbalance.py`) found residual asymmetry inherited from N7 and the old pick-based edits:

  | Candidate | Upper lower-face Δ (px) | Mid jaw Δ (px) | Lower jaw / chin Δ (px) |
  |---|---|---|---|
  | E1 | 5.3 | −9.4 | 11.0 |
  | F3 | 3.8 | −11.6 | 7.6 |

- One corrective, `blender_gd5_symjaw.py`, applies a surface-mirror average below the mouth line, fades out toward the cheeks, mouth corners and lips, and is guarded at the collar. Result:

  | Candidate | Upper lower-face Δ (px) | Mid jaw Δ (px) | Lower jaw / chin Δ (px) | Menton offset |
  |---|---|---|---|---|
  | F4 / F5 | 0.6 | 4.9 | 0.7 | 0.5 mm from midline |

  The remaining mid-jaw 4.9 px comes from the solved camera's axis tilt; the 3D jaw is mirror-balanced.
- The jaw/chin is now **locked**. Board `00_JAW_CHIN_BALANCE_LOCK` shows REFERENCE FRONT | CURRENT | MIRRORED-JAW DIAGNOSTIC | FINAL BALANCED JAW.

## What changed, in the requested priority order

1. **Soft-tissue age (form, no wrinkles; `data/ops/opsF5.json`).**
   - Submalar plane −3 mm (normal).
   - Malar fat descended 2 mm.
   - Lid–cheek junction −1 mm.
   - Nasolabial plane: cheek side +0.75 mm, perioral side −0.65 mm.
   - Prejowl −1 mm; jowl weight lowered 1.7 mm.
   - Lateral brow hood lowered 0.6 mm, placed above the lid crease.
2. **Nose.**
   - Tip de-bulbed: lateral scale 0.82; alar width at 158 cm went from 3.46 to 3.36 cm.
   - Supratip and alar crease defined.
   - Nose roughness up (+0.03 instead of −0.05) and specular down (−0.05 instead of +0.02).
3. **Lips.**
   - Lower lip volume −1.2 mm and moved back 0.75 mm; front lower-lip thickness went from 0.153 to 0.143 IPD.
   - Upper vermilion −0.6 mm.
   - Mouth corners embedded with a 0.45 mm drop.
   - Width unchanged: 1.00 of Tier A.
4. **Skin k7.**
   - Distance-surviving base colour: pore-cavity tone, a fine low-contrast freckle layer, stronger mid-scale mottling, under-eye tonality, and lid–cheek and nasolabial plane tone.
   - 4K normal with larger, deeper regional pores and skin grain; softer forehead mid-bump for grazing-top.
   - Roughness breakup.
   - Colour direction kept: olive-beige, same tint factor on face and body.
   - k6 was rejected because its pores read as dark pepper noise.
5. **Head/body seam.**
   - Body SRMF blended toward the head collar values (`T_LK_Body_SRMF_k7b`).
   - Head collar albedo matched to the body base colour.
   - Body specular multiply and concavity response set equal to the face material (body specular 0.95 → 1.0, concavity 0.7/1.3 → 0.6/1.4).
6. **Hair, h2 → h6** (h3–h5 were intermediates).
   - Loose locks straightened and weighted: wave × 0.4, wavelength × 1.5, tighter tips.
   - Asymmetric framing: different face-frame and side locks dropped on each side.
   - Stronger clumping and less frizz.
   - Softer temple edge: wider density ramp, more fine edge hairs.
   - Smaller, less spherical bun: radius 3.0 → 2.45 cm, 7 loop groups, fewer turns.
   - Flyaways 1200 → 450 and shorter.
   - Matte material with less highlight.
   - The part band is limited to the front: the h4/h5 crown gap is fixed.

**Auto-rig:** rerun because the neutral geometry changed; joints were compared against E1 (`data/joint_comparison.json`).
- Eye-joint distance is 5.899 cm, unchanged.
- Mouth-corner joints are 4.604 cm apart (E1: 4.598).
- 37 of 843 facial joints moved more than 1 mm, consistent with the refinement scale.

## Measurements (`data/`)

| Measure | Tier A | GD4 E1 | GD5 F5 |
|---|---|---|---|
| Eye joint distance (cm) | – | 5.899 | 5.899 |
| Eye fissure width (IPD, front) | 0.460 | 0.460 | 0.460 |
| Mouth width (IPD, front) | 0.844 | 0.852 | 0.846 |
| Lower lip thickness (IPD, front) | 0.153 | 0.153 | 0.143 |
| Upper / lower lip thickness (IPD, 3/4) | 0.167 / 0.227 | 0.111 / 0.206 | 0.106 / 0.204 |
| Nose width at 158 / 159 / 160.5 cm (cm) | – | 3.46 / 3.28 / 2.55 | 3.36 / 3.28 / 2.55 |
| Lower-lip / upper-lip / labiomental projection, y (cm) | – | 13.68 / 13.79 / 12.87 | 13.59 / 13.79 / 12.87 |
| Jaw balance Δ upper / mid / lower (px) | 0 / 1 / 0 (user guide) | 5.3 / −9.4 / 11.0 | 0.6 / 4.9 / 0.7 |
| Menton offset from nose midline (cm) | ≈ 0 | −0.25 | 0.05 |
| Jaw-border path L / R (cm) | – | 16.39 / 16.32 | 17.02 / 16.84 |

Upper, mid and lower cheek per side: `data/sidecontour_y4.txt`. The cranium is unchanged from GD4 (`data/cranium.txt`).

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
| SOFT-TISSUE AGE CHARACTER | FAIL |
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

- **Soft-tissue age: FAIL.** The plane changes (≤3 mm) and the tonal work are real in clay and texture. At portrait distance the face still reads younger and fuller than Tier A (boards 01, 04, 05). The adult, lived-in character is not achieved without stronger form changes.
- **Nose / lips: PARTIAL.** They are drier and less plush, but the nose tip is still rounder and more upturned than Tier A in 3/4.
- **Seam: PARTIAL.** It is reduced in grazing and interior light, but a faint chest arc remains in studio light (board 12).
- **Hair: PARTIAL.**
  - Better: framing is straighter, stringier and asymmetric; the bun is smaller; there is less sparkle.
  - Still open: the front still reads more groomed than the damp, weighted reference, and the front part shows dark scalp patches in the high view.
- **Overall: FAIL.** Clear technical and form progress, and the jaw is balanced, but the result does not yet read as the same adult, lived-in woman.

## Boards

| Group | Boards |
|---|---|
| Jaw lock | 00 jaw/chin balance lock |
| Neutral face | 01 front, 02 3/4, 03 profile |
| Age and features | 04 soft-tissue age front, 05 soft-tissue age 3/4, 06 eye-area character, 07 nose, 08 lips |
| Skin | 09 macro, 10 micro, 11 lighting A–E, 12 head/body seam |
| Hair | 13 front/3/4, 14 hairline/temple, 15 bun |
| Expression and character | 16 reference expression, 17 full character |
| Verification | 18 rig test, 19 LOD test, 20 after restart |

Each board compares REFERENCE | GD4 | GD5 with identical cameras and lights.

## Recommended next step

The remaining gap is soft-tissue form at a scale the parametric ops can't reach without risking folds. Options:
- **(a)** A targeted sculpt pass on the F5 neutral in Blender: cheek fat-pad volume loss, a tear-trough transition, a nasolabial plane step and nose-tip length, guided by Tier A 3/4 overlays. Then one auto-rig.
- **(b)** Accept a slightly stronger, explicitly approved plane amplitude (3–5 mm).

Hair: a damp clump-and-weight pass on the front and side locks, plus a part-edge density fix.
