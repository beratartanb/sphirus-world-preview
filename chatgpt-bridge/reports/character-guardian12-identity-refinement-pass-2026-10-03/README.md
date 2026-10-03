# GUARDIAN-12: identity refinement pass (eye/brow/orbit, midface, lower-face rhythm, nose, lips, skin)

Date: 2026-10-03. Status: **STOPPED FOR USER REVIEW.** Nothing was promoted.

- **Candidate:** `/Game/Sphirus/CharacterLab/CharacterGuardian12_20261003/`.
- **Protected folders were not modified:** production and GUARDIAN 1–11. All 23 protected groups are byte-identical to the checkpoint (`data/preservation_check.json`).
- **Starting point:** GD11 face E, skin k9, hair h23.
- **Locked items, not reopened:** C8 cranium, balanced jaw/chin, chin centre, lower-face centreline, h23 hair, the new-DNA/RigLogic/LOD/restart pipeline, and the restrained age level.
- **No new wrinkles:** the normal and roughness maps are the k9 maps, unchanged.

## Final GD12 candidate

| Part | Asset |
|---|---|
| Face | `Face/SKM_GD12_Face_f`. One fresh auto-rig on the sculpted neutral r2 (`MHC/MHC_GD12_F`, DNA `MHC_GD12_F_Head`): RigLogic, 858 morphs, 8 LODs. RIGFIT mean 0.016, max 0.35; eyes 0.000. |
| Skin | `MI_LK_Face_*_VT_g12k11` + `MI_GD12_Body_k11`, textures `T_LK_Head_{BC,N,SRMF}_k11b` (`data/skin_k11_params.txt`). |
| Hair | h23, unchanged and rebound (`GB_GD12_*_f12`). |
| Eyes, body, garments | Unchanged. |

## What was done

### Sculpt

Sculpting started from GD11 E (`data/strokes/r2.json`, 14 strokes, all mirrored). The work was judged in front, 33° 3/4 and profile every round. The Tier A front and 3/4 photos are the authority; the Tier B profile is a low-weight aid.

| Region | Stroke | Peak displacement |
|---|---|---|
| Upper lid | Hood weight down / forward | 0.9 mm |
| Upper lid | Extra lateral hood | 0.62 mm |
| Brow | Brow shelter moved forward | 0.67 mm |
| Lower orbit | Rim support (clay) | 0.3 mm |
| Midface | Malar / mid-cheek support | 0.4 mm |
| Midface | Nasolabial-side support | 0.35 mm |
| Midface | Lower-cheek / prejowl support | 0.4 mm |
| Lower face | Philtrum lengthened, lower lip lowered, chin pad lowered (symmetric) | −0.4 / −0.5 / −0.6 mm |
| Nose | Radix continuity | 0.3 mm |
| Nose | Lobule fullness slightly restored (no further de-bulbing) | 0.24 mm |

Round r1 (`data/strokes/r1.json`) was too weak to see and was superseded.

### Safety checks

| Check | Result |
|---|---|
| Lid-tracker curves | Moved ≤ 0.56 mm |
| Eye joints / IPD | Unchanged: 5.903 → 5.904 cm (`data/joint_comparison.json`) |
| Facial joints moved > 1 mm vs GD11 | 0 of 843 |
| Jaw contour half-widths | Identical at three heights (8.263, 8.385, 9.895 cm) |
| Mouth-corner width | 4.659 → 4.666 cm (not widened) |
| Cranium | Unchanged |
| Hollows | None created |

### Skin k11

- **Base:** the k9 maps.
- **Redness:** the low-frequency redness excess in the BC was lowered (`tools/blender_gd12_redness.py`). This shows mostly on the nose tip, cheeks, ears and blotchy patches; `data/_redness_k11.png` shows where on the UV.
- **Lips:** capped so they keep most of their colour.
- **Colour factor:** moved to a neutral olive-beige [0.78, 0.83, 0.935], down from k9's [0.84, 0.85, 0.93].
- **Variants tried and rejected:** k10 and k10n, colour factor only. Both were barely different from k9.
- **Lines:** no new lines. Pores, roughness and grain are the k9 microstructure.

## Verification

| Check | Result |
|---|---|
| Rig, board 17 | 21 rig cases: neutral, blink, single-eye blinks, gaze in four directions, brow raise / lower, visemes, jaw, extreme. Plus 6 eyelid-expression cases, including the new half squint and full squint. Lids close fully, with no poke-through, no excess sclera and no bags. |
| LOD, board 18 | Passed. |
| Fresh-editor reopen | Face (DNA user data, 858 morphs, 8 LODs), MHC, DNA, h23 and the four bindings load; nothing dirty (`data/reopen_check.json`). |
| After restart, board 19 | Passed. |
| Capture files | 0 zero-byte files. Disk ended with 24 GB free; nothing was deleted. |

## Gates

| Gate | Result |
|---|---|
| EYE / BROW / ORBIT CHARACTER | PARTIAL |
| UPPER-LID CHARACTER | PARTIAL |
| LOWER-LID / LOWER-ORBIT CHARACTER | PARTIAL |
| MIDFACE TISSUE SUPPORT | PARTIAL |
| MALAR / CHEEK CHARACTER | PARTIAL |
| LOWER-FACE TISSUE | PARTIAL |
| LOWER-FACE RHYTHM | PARTIAL |
| PROFILE NOSE | PARTIAL |
| PROFILE RADIX / BRIDGE | PARTIAL |
| PROFILE TIP / ALA / COLUMELLA | PARTIAL |
| LIP VOLUME | PARTIAL |
| LIP PROJECTION | PARTIAL |
| MOUTH-CHIN RELATION | PARTIAL |
| SKIN TONE | PARTIAL |
| SKIN REGIONAL VARIATION | PARTIAL |
| SKIN MICROSTRUCTURE | PARTIAL |
| SKIN MATERIAL RESPONSE | PARTIAL |
| AGE CHARACTER | PARTIAL |
| AGE RESTRAINT | PASS |
| FULL PROFILE SILHOUETTE | FAIL |
| FRONT IDENTITY | PARTIAL |
| 3/4 IDENTITY | PARTIAL |
| PROFILE IDENTITY | FAIL |
| CRANIUM PRESERVATION | PASS |
| JAW / CHIN BALANCE PRESERVATION | PASS |
| HAIR ARCHITECTURE PRESERVATION | PASS |
| RIG | PASS |
| LOD | PASS |
| RESTART | PASS |
| OVERALL FACE GATE | FAIL |
| OVERALL CHARACTER LIKENESS GATE | FAIL |

### Honest read

**Better than GD11:**
- **Upper lid and brow:** the upper lid is heavier and more hooded laterally, and the brow sits slightly more forward over the eye. In the clay views (board 04) the eye reads a little more sheltered and calmer, with no bags or dark sockets.
- **Skin:** less red on the nose, cheeks and ears, and a more neutral olive-beige overall without going grey (boards 10–11).
- **Midface:** a light, even support on the malar, nasolabial-side and prejowl areas, with no inflation and no hollows (board 05).
- **Lower face:** the extra length is spread across philtrum, lips and chin pad instead of only dropping the chin, and the chin stays centred.

**Still not the same woman:**
- **Eyes:** they still read more open and less deep-set than the reference. The lid stroke is below 1 mm because larger amplitudes made lumps in earlier passes.
- **Profile:** the profile is still a different person. The forehead-radix line, nose length and tip, and lower-lip/chin fullness all differ (board 09). The profile overlay (board 15) has low reliability, because the generated profile sheets disagree with each other.
- **Lips:** the lower lip is still rounder and more "rolled" in front than in the reference.
- **Skin:** in studio light the skin still shows some warm peach in the 3/4 view. The age character still comes mostly from structure, with the age cues kept deliberately restrained.
- **Size of the change:** each change in this pass is sub-millimetre. Together they move the face in the right direction but do not close the identity gap.

**Recommended next step:** a hands-on freehand sculpt session on F, rebuilt with `blender_gd10_session.py`, for the eyes, profile and lower lip, followed by one more auto-rig. More scripted micro-strokes alone are unlikely to make it the same woman.

## Boards

| Board | Content |
|---|---|
| 01 | FRONT_CLAY |
| 02 | 3Q_CLAY |
| 03 | PROFILE_CLAY |
| 04 | EYE_BROW_ORBIT |
| 05 | MIDFACE_SOFT_TISSUE |
| 06 | LOWER_FACE_RHYTHM |
| 07 | PROFILE_NOSE |
| 08 | PROFILE_LIPS_MOUTH |
| 09 | FULL_PROFILE_RHYTHM |
| 10 | SKIN_TONE |
| 11 | SKIN_REGIONAL_VARIATION |
| 12 | SKIN_MICRO_MATERIAL |
| 13 | FRONT_OVERLAY |
| 14 | 3Q_OVERLAY |
| 15 | PROFILE_OVERLAY_IF_RELIABLE (low reliability) |
| 16 | HAIR_PRESERVATION |
| 17 | RIG_TEST |
| 18 | LOD |
| 19 | AFTER_RESTART |

Comparisons are REFERENCE | GD11 | GD12 with identical cameras and lights.
