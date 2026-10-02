# GUARDIAN-11: profile, eye/brow, age-character and skin-tone pass

Dates: 2026-10-02/03. Status: **STOPPED FOR USER REVIEW.** Nothing was promoted.

- **Candidate:** `/Game/Sphirus/CharacterLab/CharacterGuardian11_20261002/`.
- **Protected folders were not modified:** production and GUARDIAN 1–10. All 22 protected groups are byte-identical to the checkpoint (`data/preservation_check.json`).

## Final GD11 candidate

| Part | Asset |
|---|---|
| Face | `Face/SKM_GD11_Face_e`. One fresh auto-rig on the sculpted neutral E (`MHC/MHC_GD11_E`, `MHC/DNA/MHC_GD11_E_Head`): RigLogic, 858 morphs, 8 LODs. |
| Skin | `Skin/MI_LK_Face_*_VT_g11k9` + `MI_GD11_Body_k9`, textures `T_LK_Head_{BC,N,SRMF}_k9b` (`data/skin_k9_params.txt`). |
| Hair | h23, unchanged and rebound (`GB_GD11_*_e11`). |
| Eyes, body, garments | Unchanged. |

## What was done

Sculpting started from the GD10 r5 neutral, using the same mirrored stroke brushes judged against the Tier A front and 3/4 photos. Profile sheets were a low-weight aid only.

| Pass | Strokes |
|---|---|
| A — nose (`data/strokes/pA.json`) | Rounded "ball" of the tip flattened, slight tip de-projection, radix-to-bridge continuity. |
| A2 / C / D / E (`data/strokes/pCDE.json`) | Alar balls deflated and the alar crease filled, so the nostril wings blend into the tip instead of reading as three bulbs. Upper vermilion rolled in, upper and lower lip padding reduced (less "plush"); width unchanged. Chin pad 1.2 mm lower for a slightly longer lower face (symmetric). Brow shelter moved down and forward with more lateral-hood weight. Light lower-orbit support. |

Two weaker rounds (pC, pC2) were run first. They were visually indistinguishable, so they were superseded.

### Safety checks

| Check | Result |
|---|---|
| Upper / lower-lid tracker curves | Moved ≤ 0.4 mm |
| Blink | Closes fully |
| Jaw contour half-widths | Identical to GD10 at three heights |
| Cranium | Unchanged |
| Hollowing in nasolabial, submalar, malar, tear trough | None |
| Perioral zone | Min −1.25 mm. This is the intended lip-volume reduction at the lip edge, not a hollow (mean −0.08 mm). |

### Auto-rig and joints

One fresh auto-rig on E. Joints vs GD10 S5:

| Joint measure | GD10 S5 | GD11 E |
|---|---|---|
| Eye-joint distance (cm) | 5.903 | 5.903 |
| Mouth-corner joints (cm) | 4.671 | 4.659 |
| Facial joints moved > 1 mm | – | 28 of 843 |

### Skin k9

- Colour factor moved to a warmer-neutral olive-beige.
- Large baked blotches evened out at low frequency: the grimy dark patches of GD10 k7 are gone, and detail and fine freckles are kept.
- Mottling and sun spots reduced.
- Lips lighter and muted (rose-brown instead of dark red).
- Mild under-eye tone.

**Restrained early-adult age cues** in the normal map and, at 5 %, in the colour:
- three faint broken forehead lines;
- a soft glabella;
- delicate double creases under the lower lids;
- a soft nasolabial indication.

There are no deep folds, bags or crow's feet. Placement is verified on the UV (board 09, right).

## Verification

| Check | Result |
|---|---|
| Rig, board 16 | 23 cases, single-eye blinks, visemes, extreme; no lid issues. |
| LOD, board 17 | Passed. |
| Fresh-editor reopen | Face (DNA user data, 858 morphs, 8 LODs), MHC, DNA, h23 and the four bindings load; nothing dirty. |
| After restart, board 18 | Passed. |

**Interruption:** C: ran out of disk space during the final captures. Those captures were written as 0-byte files and the chain stalled.

- With the user's approval, 11,811 capture files older than 2026-10-02 (21.8 GB) were deleted from `Saved/Codex/CharacterLookdev_20260930/captures`.
- All affected GD11 captures were re-rendered; 0-byte files were found and replaced.
- The only data lost was the deleted older render captures; published reports keep their own boards.

## Gates

| Gate | Result |
|---|---|
| PROFILE NOSE | PARTIAL |
| PROFILE RADIX / BRIDGE | PARTIAL |
| PROFILE TIP / ALA / COLUMELLA | PARTIAL |
| PROFILE ZYGOMA | PARTIAL |
| PROFILE MALAR | PARTIAL |
| PROFILE MAXILLA | PARTIAL |
| PROFILE MIDFACE | PARTIAL |
| PROFILE UPPER LIP | PARTIAL |
| PROFILE LOWER LIP | PARTIAL |
| PROFILE LIP PROJECTION | PARTIAL |
| PROFILE MOUTH-CHIN RELATION | PARTIAL |
| EYE / BROW / ORBIT CHARACTER | PARTIAL |
| SOFT-TISSUE AGE CHARACTER | PARTIAL |
| SKIN TONE | PARTIAL |
| SKIN MACRO CHARACTER | PARTIAL |
| SKIN MICROSTRUCTURE | PARTIAL |
| SKIN MATERIAL RESPONSE | PARTIAL |
| FULL PROFILE SILHOUETTE | FAIL |
| 3/4 IDENTITY PRESERVATION | PASS |
| FRONT IDENTITY PRESERVATION | PASS |
| SOFT-TISSUE SUPPORT PRESERVATION | PASS |
| JAW / CHIN BALANCE PRESERVATION | PASS |
| CRANIUM PRESERVATION | PASS |
| HAIR ARCHITECTURE PRESERVATION | PASS |
| RIG | PASS |
| LOD | PASS |
| RESTART | PASS |
| IDENTITY FRONT | PARTIAL |
| IDENTITY 3/4 | PARTIAL |
| IDENTITY PROFILE | FAIL |
| OVERALL FACE GATE | FAIL |
| OVERALL CHARACTER LIKENESS GATE | FAIL |

### Honest read

**Clearly better than GD10:**
- **Skin:** even, natural, olive-beige, lighter lips, no grime. It is the biggest visible improvement of the pass (board 10).
- **Nose:** less "three-ball" in front.
- **Lips:** less padded.
- **Brow:** slightly heavier.

**Not yet the same woman:**
- In profile (board 12) the forehead-radix-nose line, nose size and lower-face fullness still differ.
- The eyes still sit more open and less deep under the brow than in the reference (board 08).
- The age cues are deliberately restrained, so at portrait distance the face still reads somewhat younger than Tier A. That is within the requested 28–32 range, but the reference itself reads older.
- The geometry strokes in this pass are sub-millimetre to about 1.4 mm. Larger stroke amplitudes produced lumps in GD10 (r2 / r4).

The remaining identity gap still needs freehand sculpting. The hands-on Blender session from GUARDIAN-10 (`CharacterGuardian10_20261002/sculpt_session`) can be rebuilt on E with `blender_gd10_session.py`.

## Boards

| Board | Content |
|---|---|
| 01–03 | Front / 3/4 / profile clay |
| 04 | Nose |
| 05 | Cheekbone / midface |
| 06 | Lips |
| 07 | Mouth–chin |
| 08 | Eye / brow / orbit |
| 09 | Soft-tissue age, plus age-cue UV placement |
| 10 | Skin tone |
| 11 | Skin macro / micro |
| 12 | Full profile rhythm |
| 13 | Front overlay |
| 14 | 3/4 overlay |
| 15 | Hair preservation |
| 16 | Rig test |
| 17 | LOD |
| 18 | After restart |

Comparisons are REFERENCE | GD10 | GD11 with identical cameras and lights.
