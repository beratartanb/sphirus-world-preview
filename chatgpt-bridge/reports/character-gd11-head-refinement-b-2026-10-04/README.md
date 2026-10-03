# GD11 head refinement B: nose dorsum, natural top / forehead roots, groom LOD, whole-head verification

Date: 2026-10-04. Status: **STOP FOR USER REVIEW.** Nothing promoted; the playable character was not changed.

**Starting point:** report `character-gd11-head-refinement-2026-10-04` (commit `b44c08a`): R3 face, h32 hair, k9 skin, e2 eyes, M_SlightArch brows, S_Thin lashes.

**New candidate:** `/Game/Sphirus/CharacterLab/GD11_HeadRefinementB_20261004/`, with sources in `Saved/Codex/GD11_HeadRefinementB_20261004/`:

| Part | Asset |
|---|---|
| Face | `SKM_G11RB_Face_d85`. DNA `MHC_G11RB_D85_Head`, 858 morphs, 8 LODs. One fresh auto-rig of the D85 neutral; fit 0.015 mm mean. |
| Hair | `Hair/GR_LK_Hair_{Main,Loose}_h34` with retuned LOD table and helmet `SM_LK_HairHelmet_h34`. Colour identical to the final h32c values. |
| Bindings | `Face/Bindings/GB_G11RB_*_d85h34` |
| Skin / eyes / brows / lashes | GD11 k9 / e2 / M_SlightArch / S_Thin, used by reference, unchanged |

**Preserved:** R3/h32 (candidate A) and the original GD11 were used read-only as comparison sources.

## Protected assets: 47 / 48 groups byte-identical (`data/preservation_check.json`)

Identical: production, B2 body and correctives, outfits, GD1–GD15, the original GD11, h23 sources, reference images, all earlier source folders, and all R3/h32 data.

**One honest exception:** in candidate A (R3/h32), the two **studio presentation materials** `Studio/MI_LK_Backdrop` and `Studio/MI_LK_Floor2` were re-saved.
- Cause: the first camera-check capture of this pass, which still used A's capture script, whose studio-save folder was A.
- A's face, DNA, hair, bindings and every character asset are unchanged.
- From then on, all capture setup writes only to B (`gd11rb_face_run.sh`), and binding into A or archived folders is refused by the script.

## 1. Binding check

**Every capture used for judgement** was composed by a script that verifies each binding asset exists before capturing (`BINDINGS_OK` in the logs). Every final binding targets `SKM_G11RB_Face_d85`.
- **No silent fallback:** no binding was taken from archive folders.
- **Default paths:** each points explicitly to the B folder.

**Binding errors found:** no wrong-binding frames appeared in this pass.

## 2. Camera check (board 01): geometry fixed, only the camera varied

The old 3/4 camera (`camfit_close`, ~30° from front, **pitch 11°**) was re-solved on the R3 geometry (`data/camfit_close_*.json`):

| Constraints | Yaw from front | Pitch | Eyes / lips fit |
|---|---|---|---|
| Eyes + lips + ears (old setup, ears ×40) | 29° | 7° | 10.3 px |
| Eyes + lips + ears ×10 | 31° | 4° | 9.3 px |
| Eyes + lips only | 35° | −2° (roll 3°) | 5.5 px |
| **Eyes + lips, no roll (chosen)** | **32°** | **1°** | 7.0 px |
| Fixed 40°, pitch 1° | 40° | 1° | 9.4 px |
| Old camera as-is | 30° | 11° | 10.9 px |

**Independent check:** the far-eye / near-eye width ratio, which is nearly geometry-free, gives Tier A ≈ 0.69, i.e. ≈ 26–28°.

**Decision:**
- 3/4 reference comparisons use **32° yaw, pitch 1°**.
- The old camera's main error was **pitch**: it looked up under the jaw.
- The 40° camera hides more of the far eye than Tier A shows.

**Status:** best-supported, **not verified**. Uncertainty is roughly ±4°. Silhouette-based solves give 40°+, but they depend on the nose's own projection.

## 3. Nose dorsum: main face change (boards 04, 05)

**Problem (shown, not assumed):**

| Point | Height z (cm) | Forward y (cm) |
|---|---|---|
| Radix | 163.0 | 13.49 |
| Supratip | 159.7 | 15.09 |
| Tip | 158.8 | 15.45 |

- **Radix:** shallow (only 1.2 mm behind the glabella), so it was not the problem.
- **Mid–lower dorsum:** scooped up to **5.3 mm** behind a straight radix→supratip line (deepest around z 161).
- **Tip lobule:** bulged out after that scoop, so the tip read as a separate bump. This is visible in both clay profiles and the matched 3/4.
- **Tier A comparison:** the Tier A 3/4 (and the generated profile, an aid only) shows a long, nearly straight dorsum into a rounded tip.

**Method** (script, `tools/gd11rb_dorsum.py`):
- **Fill deficit only:** only the concave deficit is filled, at 85 %, toward a straight line plus a 0.4 mm natural convexity.
- **Lateral shape:** a lateral Gaussian keeps the bridge from becoming a ridge.
- **Hard guards:** tip lobule (0.00 mm), nostrils, alar base, columella and radix depth untouched; lids ≤ 0.22 mm (`data/dorsum_D85_report.txt`).
- **Candidates:** 60 % and 100 % fills were also made; 85 % was chosen as the straightest without losing a hint of supratip.

**Result:**
- **Profiles:** both now run straight into a connected tip.
- **Matched 3/4:** the bridge reads continuous, like Tier A.
- **Unchanged:** front width, nostrils and base from below (board 05).

**One fresh auto-rig** on D85: fit 0.015 mm mean, 858 morphs, DNA attached.

## 4. Hair: h32 → h34 (boards 06–08)

**What was wrong in h32**, seen in close-ups under neutral and side light:
- the hairline was a fuzzy band of randomly oriented bristles with a saw-tooth edge;
- the part opened into a bare V / oval at the front;
- the front lifted off as a cap (roots forced almost vertical before turning back);
- the top showed parallel wave ribbons.

**Structural changes** in a builder copy (`tools/blender_g11rb_hair.py`). This is code-level guide logic, not a seed change; parameters are in `data/hair_h32_to_h34_env_diff.txt`.

| Change | How |
|---|---|
| Front-root exit | New controls for root stand-off, rise ramp and the root normal's upward bias. Roots now leave the scalp at an angle and rise gradually; no vertical bristle wall. |
| Edge hairs | Rebuilt as **small clusters (≤ 8)** sharing one flow direction along the main back/up flow, lying close to the scalp; 3 600 instead of 8 000 random ones. |
| Hairline | Jag amplitude 2.0 → 0.7 (no saw edge); longer, sparser edge ramp; slightly smoother temple corner. |
| Part | Starts further back (no split at the hairline); more and longer part-crossing hairs. |
| Top | Less tertiary / strand clumping, more lateral fill, gentler secondary waves: the ribbon look breaks up. Crown height unchanged. |
| Bun | Same seat and height; slightly more irregular group loops and a few more escaping ends. |
| Unchanged | Temple / ear coverage from h32 (no bare band, no side wall), back mass, colour. |

**Iterations:** h33 was the intermediate step. It fixed the cap and zigzag but left a bare part oval and a sparse, net-like edge; h34 fixed both. Each was judged in UE studio and side light against h32.

**Colour:** unchanged (h32c values: melanin 0.53, redness 0.48, desaturation 0.11). Board 09 compares on identical light.

## 5. Groom LOD: now actually tested (board 10)

- **Previous claim:** "groom LOD not forced" was correct. In this engine build the groom component has **no Python LOD forcing**, and the `r.HairStrands.ForceLOD` / `LOD.Force` console variables do not exist (they read back 0). The capture tool's `groom_lod` option had silently done nothing.
- **Test used instead:** real **automatic LOD by distance** (1.25 / 3 / 6 / 9 / 12 m). It showed a real defect: at 6–12 m the decimated strand LODs broke the hair into a speckled cap and the scalp showed at the hairline.
- **Fix:** h34 LOD table retuned and verified after reopen:

| Groom | LOD1 | LOD2 | LOD3 |
|---|---|---|---|
| Main | 65 % curves, thickness ×1.25, screen size 0.5 | 40 % curves, thickness ×1.7, screen size 0.25 | helmet mesh from screen size 0.12 |
| Loose | 65 % curves, thickness ×1.25, screen size 0.5 | 40 % curves, thickness ×1.7, screen size 0.25 | hidden |

- **Result:** 12 m now shows a solid hair-mesh cap. At 6–9 m coverage is clearly better, but some temple speckle remains (sub-pixel strands).
- **Untested:** 20 m is out of frame in the studio (the backdrop blocks the camera). The active LOD index cannot be read back in this build.

## 6. Rig, motion, reopen (board 10)

- **Rig:** 27 cases on D85:
  - blinks (both and single), gaze, brows;
  - lips closed, visemes, smile, mouth and jaw open;
  - **upper-lip raise, sneer, nostril dilate / compress**;
  - all clean, no tearing around the new dorsum.
- **Face LOD 0–3:** consistent.
- **Motion:** 90° left and right turns (0.6 s / 1.2 s), look-around idle, run-stop (front / 3/4 / back / side, camera following).
  - No hair intersection with ears, forehead, nape or neck was seen.
  - The look-around clip has little head pitch, so strong up/down head motion is only partly covered.
- **Reopen:** fresh editor (`data/reopen_check.json`):
  - face (DNA, 858 morphs, 8 LODs), MHC, DNA, h34 grooms, materials and helmet, all four `d85h34` bindings and the retuned LOD table load;
  - nothing dirty before or after;
  - whole-head captures repeated after restart.

## 7. Eyes, brows, skin

- **Eyes / brows:** **not touched** (no eyeball, lid or brow change). The slight sclera under the iris is compared only as-is; with gaze and expression differing from the reference, it is **unresolved, not fixed**. M_SlightArch kept.
- **Skin:** k9 unchanged.
- **Head–neck and behind the ear:** checked under studio, side grazing and gameplay sun (board 09). No seam or dark band; no added age cues.

## Gates

| Gate | Result |
|---|---|
| R3/H32 STARTING POINT VERIFIED | PASS |
| CAMERA MATCH | PARTIAL (best-supported 32° / 1°, ±4°, not verified) |
| GD11 OVERALL TYPE PRESERVED | PASS |
| RADIX–DORSUM TRANSITION | PASS |
| DORSUM / HUMP LIKENESS | PARTIAL (clearly closer; aid profile not authority) |
| SUPRATIP–TIP CONNECTION | PASS |
| TIP PRESERVATION | PASS (0.00 mm) |
| NOSE BASE PRESERVATION | PASS |
| HAIR TOP POSTURE | PARTIAL (no cap / ribbons; still procedural) |
| FOREHEAD ROOT NATURALNESS | PARTIAL (clusters along flow; some crossing fine hairs) |
| FRONT HAIRLINE | PARTIAL (no saw edge; temple corner still defined) |
| PART | PASS (no bare V / oval) |
| TEMPLE / EAR TRANSITION | PASS (h32 gain kept, no wall) |
| BACK FLOW | PARTIAL |
| BUN POSITION | PASS |
| BUN SHAPE | PARTIAL |
| HAIR COLOUR / MATERIAL | PASS (unchanged by design) |
| FIT TO WHOLE HEAD | PARTIAL |
| EYE / BROW / EXPRESSION PRESERVATION | PASS (untouched; lower-sclera question unresolved) |
| SKIN / AGE PRESERVATION | PASS |
| HEAD–NECK INTEGRITY | PASS |
| BINDING | PASS |
| RIG | PASS |
| FACE LOD | PASS |
| GROOM LOD | PARTIAL (distance test + fix; index not readable; 20 m NOT_TESTED) |
| MOTION | PARTIAL (turns / run-stop PASS; strong pitch not covered) |
| REOPEN | PASS |
| PROTECTED ASSETS | PARTIAL (47 / 48; A's 2 studio materials re-saved, no character asset) |

**Artist grade for the hair:** NO. It is script-built. A hand-authored guide groom for the crown, the temple corner and the bun is still the next quality step.

## Boards

| Board | Content |
|---|---|
| 01 | Camera check |
| 02 | Whole head front |
| 03 | Whole head 3/4 at the chosen camera |
| 04 | Nose dorsum |
| 05 | Nose base preservation |
| 06 | Hair top posture |
| 07 | Forehead roots / part / temple, neutral and side light |
| 08 | Rear / bun |
| 09 | Colour, material, skin and head–neck under three lights |
| 10 | Technical: rig, groom LOD by distance, face LOD, motion, after restart |

Boards 02 and 03 include the change isolation: R3 + h32, D85 + h32 (nose only), R3 + h34 (hair only), D85 + h34 (both). Raw captures: `Saved/Codex/CharacterLookdev_20260930/captures/g11rb*`.
