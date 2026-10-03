# GUARDIAN-12C: nose, lips, upper temple and hair correction

Date: 2026-10-03. Status: **STOPPED FOR USER REVIEW.** Nothing was promoted.

- **Candidate:** `/Game/Sphirus/CharacterLab/CharacterGuardian12C_20261003/`.
- **Protected folders were not modified:** production, GUARDIAN 1–11 and GUARDIAN-12 F. All 24 protected groups are byte-identical to the checkpoint (`data/preservation_check.json`).
- **Starting point:** GD12 F (k11 skin, h23 hair).
- **Locked items, not reopened:** C8 skull, jaw/chin balance, eyes, the non-hollow face, the restrained age level and the skin.

## Final GD12C candidate

| Part | Asset |
|---|---|
| Face | `Face/SKM_GD12C_Face_g`. One fresh auto-rig on sculpt G (`MHC/MHC_GD12C_G`): RigLogic, 858 morphs, 8 LODs. RIGFIT mean 0.017, max 0.35; eyes 0.000. |
| Skin | k11, the same textures and colour factor as GD12 (`MI_LK_Face_*_VT_g12ck11`). |
| Hair | **h24** (`Hair/GR_LK_Hair_{Main,Loose}_h24`), built on the corrected head G. |

## 1. Nose: rebuilt as one structure

Tool: `tools/blender_gd12c_nose_temple.py` with `data/ops/n3.json`; then `tools/blender_gd12c_ops.py` with `data/ops/L5.json`.

**Diagnosis on F (midline, x = −0.25):**
- **Radix:** almost no depth (0.8 mm).
- **Upper bridge:** almost vertical (about 9°), with a flat "pinch" plateau around z 161–162.
- **Lobule:** below the pinch it jumps forward at about 42° into a ball.

**Correction:** the midline profile was retargeted as one curve.
- **Radix:** 1.4 mm deep.
- **Bridge:** a single 21° line from radix to supratip.
- **Supratip and tip:** a smooth supratip, then a rounded tip, 2 mm less projected.
- **How it was applied:** the per-height difference is applied across the whole nose cross-section with a lateral gaussian falloff. The bridge sidewalls follow the ridge and the alar base stays in place.
- **Not a blanket edit:** this is not an inflate/deflate pass, and the nose was not made smaller.

**Local nasal-base corrections:**
- The alar bulb was flattened by 1.2 mm along its normal.
- The groove between the alar lobule and the tip, and the crease between ala and cheek, were filled.
- The columella was lifted by 0.7 mm.
- The region was given a soft local relax.

## 2. Lips

The lips were corrected on the outer ~4.5 mm shell only, so the inner lips stay clear of the teeth (7.7 mm clearance). The mouth width was not changed.

**Diagnosis on F:**
- **Lower lip:** it projected as far as the upper lip, then fell off 5.7 mm within 2 mm of height. This reads as a padded tube.
- **Labiomental fold:** it sat only 1.3 mm behind the chin.

**Correction:**
- **Lower lip:**
  - It goes back about 2 mm, with a softer roll-off.
  - Its lateral ends now taper into the corners instead of ending in round "sausage" ends.
  - Its lower border is softened, and the area beneath it is filled by 0.5 mm.
- **Upper lip:** it comes forward about 1 mm, so it now sits slightly ahead of the lower lip. The white-roll ridge is softened.
- **Labiomental fold:** filled by about 1 mm, so lower lip, fold and chin read as one soft S.
- **Corners:** embedded by 0.5 mm and the sharp pit is relaxed.

**Rejected round:** L1 used front-facing (normal) weighting. It produced a seam on the upper vermilion and a notch under the lower lip, so it was replaced by the depth-shell mask.

## 3. Upper temple / side width

- **Change:** a small inward push on the lateral wall only, at most 1.8 mm per side at z 166–168.
- **Preserved:** the top arc and crown above z 171, the ears, the brow and everything below z 164 are untouched.
- **Head half-width:** 7.58 → 7.41 cm at z 167.

## 4. Hair h24

Built with the same hierarchical builder as h23, on head G (`data/hair_h24_build_env.txt`).

| Area | Change from h23 |
|---|---|
| Breakup | Messy 0.45 → 0.6, frizz 0.6 → 0.85, wave 1.0 → 1.25, flyaways 450 → 850, more depth separation |
| Bun | Jitter 0.2 → 0.35, more escaping strands, a less regular loop turn |
| Rear | Density 0.68 → 0.6, more variation, slightly more lift |
| Side lift | 2.2 → 1.85, which also helps the temple width |
| Kept | The higher bun (centroid z 160.8, h23 160.6) and the side-hair start |

**Colour, brown-first auburn:**

| Parameter | h23 | h24 |
|---|---|---|
| Melanin | 0.50 | 0.53 |
| Redness | 0.50 | 0.45 |
| Red variation | 0.18 | 0.12 |
| Highlights redness | 0.52 | 0.47 |
| Highlights intensity | 0.02 | 0.015 |
| Loose-strand melanin | 0.56 | 0.62 |

- **Rejected round:** a first colour round at 0.57 / 0.40 read too dark brown.

## Verification

| Check | Result |
|---|---|
| Regions outside the targets | Jaw/chin, ears, top arc and non-head parts moved 0 mm; cheeks moved ≤ 0.03 mm. The eye area moved ≤ 0.55 mm, which is the nasal sidewall at the edge of the nose field. |
| Joints vs GD12 F | Eye-joint distance unchanged (5.904 cm); 26 of 843 joints moved > 1 mm (nose and lips). |
| Mouth-corner joint width | 4.666 → 4.698 cm (+0.3 mm). This is a small side-effect of the corner relax. It is noted here because the brief says the mouth must not be widened. |
| Rig, board 09 | 21 rig cases plus eyelid expressions including half squint and full squint. Lids close, no poke-through. |
| LOD, board 10 | Passed. |
| Fresh-editor reopen | Face (DNA, 858 morphs, 8 LODs), MHC, DNA, h24 and the four bindings load; nothing dirty. |
| After restart, board 11 | Passed. |
| Capture files | 0 zero-byte files. Disk ended with 21 GB free; nothing was deleted. |

## Gates

| Gate | Result |
|---|---|
| NOSE FORM | PARTIAL |
| NOSE CURVE FLOW | PASS |
| NOSE CONSISTENCY FRONT/3Q/PROFILE | PARTIAL |
| LIP FORM | PARTIAL |
| LIP PROJECTION | PARTIAL |
| LIP-TO-CHIN RELATION | PARTIAL |
| MOUTH NATURALNESS | PARTIAL |
| HAIR COLOUR | PARTIAL |
| HAIR FORM | PARTIAL |
| BUN INTEGRATION | PARTIAL |
| HAIR OVERALL NATURALNESS | PARTIAL |
| UPPER TEMPLE WIDTH | PASS |
| TOP ARC PRESERVATION | PASS |

### Honest read

**Clearly better:**
- **Nose profile:** it is now one coherent radix → bridge → tip line, with no pinch and no ball tip (boards 01, 02). In real-skin profile the dorsum and tip read much closer to the Tier B profile.
- **Lower lip:** it no longer reads as an overhanging tube in profile or 3/4.
- **Lip-chin:** the transition is a soft S.
- **Hair colour:** less orange-red and browner, while staying warm.

**Not yet resolved:**
- **Nose, front and 3/4:** the alae still read slightly as separate rounded wings with a dark alar curl. This is MetaHuman base topology, and only part of it could be corrected with these local ops.
- **Lips:** in profile the reference upper lip is still fuller and more projected than ours. The lips are now natural but still on the thin side of the target.
- **Hair:** h24 is looser and browner, but at board scale the form change from h23 is modest. The top still shows regular combed waves and the bun still reads somewhat constructed. A larger change needs a new top-flow / bun construction, not more parameter tuning.
- **Mouth width:** the mouth-corner joint width grew by 0.3 mm (see Verification).

## Boards

| Board | Content |
|---|---|
| 01 | NOSE FORM: REFERENCE / CURRENT / CORRECTED |
| 02 | NOSE FRONT / 3Q / PROFILE CONSISTENCY (real skin) |
| 03 | LIP FORM: REFERENCE / CURRENT / CORRECTED |
| 04 | LIP PROFILE / 3Q RELATION |
| 05 | HAIR COLOUR: REFERENCE / h23 / h24 |
| 06 | HAIR FORM / BUN / REAR MASS |
| 07 | UPPER TEMPLE / SIDE WIDTH: CURRENT / NEW |
| 08 | OVERALL front / 3/4 |
| 09 | RIG TEST |
| 10 | LOD |
| 11 | AFTER RESTART |

CURRENT means GD12 F; NEW / CORRECTED means GD12C G. All views use identical cameras and lights.
