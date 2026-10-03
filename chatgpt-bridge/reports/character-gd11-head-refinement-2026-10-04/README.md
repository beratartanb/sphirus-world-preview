# GD11 head refinement: back to GD11, same type, local fixes, hair h23 → h32

Date: 2026-10-03/04. Status: **STOP FOR USER REVIEW.** Nothing promoted; the playable character was not changed.

**Starting point:** the real GD11 package (report commit `58336a2`). The cancelled GD12–GD16 direction was not used:
- no face widening, eye moves, lower-face lengthening, new nose, or custom head;
- no millimetre targets from later reports.

**Protected:** all 46 protected groups are byte-identical to the checkpoint taken before this pass (`data/preservation_check.json`). They include:
- production `MH_MainCharacter`;
- GD1–GD15, GD11 itself, the GD8 h23 hair (assets and source), B2 body and correctives, outfits;
- the reference images and every earlier character source folder.

**Asset manifest:** `data/asset_manifest.md`. It covers the baseline GD11 package and the new candidate.

## 1. GD11 restored and verified (board 01)

The real GD11 package was found locally, complete, and is byte-identical to its checkpoint:
- **Face:** `SKM_GD11_Face_e` with DNA `MHC_GD11_E_Head`, 858 morphs and 8 LODs.
- **Skin:** k9.
- **Eyes:** e2.
- **Hair:** h23, from the GD8 folder.
- **Brows / lashes:** M_SlightArch / S_Thin.
- **Bindings:** `GB_GD11_*_e11`.
- **Body / garments:** B2, Henley g17e, Chaos shorts.

A fresh capture of this package, with no edits, matches the GD11 report frames exactly.

**Isolation:**
- Every new asset is in `/Game/Sphirus/CharacterLab/GD11_HeadRefinement_20261003/`.
- The capture, rig and hair scripts are copies that write only there.
- Binding into an archived `CharacterGuardian*` folder is refused by the script.
- The cancelled GD16 Blender job was stopped first. No other process was touched.

## 2. What was found on the real GD11, and what was done

| Region | Seen on GD11 | Change | Effect on overall type |
|---|---|---|---|
| **Right cheek** | A right-side-only crease line from under the outer eye down the cheek. It shows in the right profile in both real render and clay; the left side is clean (board 05, "R cheek"). | High-frequency surface of that band replaced by the mirrored high frequency of the clean left cheek. Low-frequency form, including GD11's natural asymmetry, kept. | None. Change max 3.4 mm in the crease, mean 0.5 mm. |
| **Nose base** | From below: pinched, curled nostril rims. In 3/4: hard, deep alar groove; the ala reads as a separate bulb. Confirmed as geometry in Blender clay. | GD14 method on GD11's own data: GD11's own face-model coefficients re-evaluated without the accumulated sculpt delta, then only the high frequency of the nose base transferred (k=120). **The tip lobule was restored from GD11**, so tip position is identical. No preset or K5/GD14 nose was used. | Front nose unchanged in shape. Rounder, open nostrils; softer alar groove. Max 4.85 mm at the nostril rim, mean 0.65 mm. |
| Mouth / lips / chin | No defect found: philtrum, corners, lower-lip ending and labiomental transition are natural in real and clay. | **Not touched.** | – |
| Eyes / lids | A little sclera shows under the iris (slightly alert look). | **Not touched.** Moving lids or eyeballs was not justified by a clear defect. | – |
| Brows | Groom-based. Tested M_Natural against GD11's M_SlightArch (board 06). | **Kept M_SlightArch.** M_Natural is thinner, lighter and further from the reference. | – |
| Cranium, jaw, cheeks, eye set | – | **Not touched.** All other skin moved ≤ 0.3 mm (smoothing spill); eyes and teeth 0 mm. | – |

**Method:** script-based (`tools/gd11r_face_ops.py`, `ue_g11r_nose_model.py` + `blender_gd14_nosebase.py`), judged in Blender clay and in Unreal real renders. It is not freehand sculpting.

**One fresh auto-rig** of the corrected neutral R3:
- auto-rig ok;
- fit to the sculpt 0.015 mm mean;
- 858 morphs, DNA attached;
- same skeleton and post-process ABP.

The face change alone is shown as "R3 + h23 (face only)" on boards 02/03.

## 3. Hair: h23 → h32 (board 07)

Built with the h23 builder and h23's exact parameter set. Only these changed (`data/hair_h23_to_h32_env_diff.txt`):

| h23 problem (seen) | Change in h32 |
|---|---|
| Bare, "shaved" temple / above-ear band (3/4 and side) | Temple-to-ear hairline (62–98°) brought back to a natural level, front hairline unchanged. Sparse edge (edge density 0.14, longer ramp, more fine edge hairs). Side-front density 0.7 (was 0.45). Low side lift, so no side wall. |
| Over-ear coverage | 3 (left) / 2 (right) temple groups from the side mass back over the upper ear. Asymmetric. |
| Regular top waves / parallel ribbons | Primary wave amplitude 1.0 → 0.5. Secondary wave and depth separation up; more primary masses (60 → 72); more lateral fill. |
| Over-uniform back | Back density 0.68 → 0.62, more layer separation. |
| Bun reads as a loose stuck-on clump | Same height and seat. Radius 2.35 → 2.05, tighter wrap, 8 groups, fewer escaping ends: more compact and gathered. |
| Symmetric thin face wisps | Long front wisps removed; one short framing group per side, different on each side. |

h30 and h31 were intermediate steps (`boards/` source captures). h32 was chosen because only it closed the temple wedge without a wall.

**Colour** (board 08), changed separately on the same h32 geometry:
- melanin 0.50 → 0.53
- redness 0.50 → 0.48
- desaturation 0.08 → 0.11
- highlight melanin 0.44 → 0.46

A mild move from orange toward the reference's warm auburn-brown, with no darkening.

## 4. Skin, age, ears, neck (board 08)

- **Skin:** k9 kept unchanged. No new age cues; the lips are not grey/purple.
- **Head–neck:** ears, nape and the head–neck transition are unchanged and show no seam in studio light.
- **Body and garments:** not edited.

## 5. Technical checks (board 09), run on the final candidate

- **Rig:** 27 cases on `SKM_G11R_Face_r3`:
  - neutral, both-eye and single-eye blinks, four gaze directions, brows up/down;
  - lips closed, smile, frown, mouth/jaw open, jaw left/right;
  - visemes OO / EE / MBP / W, cheek compress, extreme;
  - because the nose base changed, also **sneer, upper-lip raise, nostril dilate and nostril compress**.
  - All deform cleanly; blinks close fully.
- **LOD:** face LOD0–3 forced: consistent. **Groom LODs are not forced by the capture tool, so they are not tested.**
- **Motion:** 90° turn (0.6 s / 1.2 s) and run-stop with hair, from front, 3/4 and back. No visible hair–ear / neck / face intersection in these samples.
- **Reopen:** fresh-editor reopen (`data/reopen_check.json`):
  - face (DNA, 858 morphs, 8 LODs), MHC, DNA, h32 grooms and materials, the four `r3h32` bindings and the rig sequence load;
  - nothing dirty before or after;
  - captures repeated after restart.

**Process error (now fixed):**
- Several intermediate R3 captures showed "brows under the chin". The cause was my copied capture script: its default binding path still pointed at the GD11 folder, so the composition referenced bindings that don't exist.
- Fixed by giving the copy its own binding path. No GD11 file was written.
- All boards use correctly bound captures.

## Gates

| Gate | Result | Note |
|---|---|---|
| GD11 SOURCE VERIFIED | **PASS** | Package found, hash-identical; fresh capture matches the report |
| GD11 OVERALL TYPE PRESERVED | **PASS** | Edits only in the nose base and right cheek; boards 02–04 read as the same face |
| FRONT VIEW | PARTIAL | Same as GD11. Likeness to the reference is unchanged (GD11's remaining gap) |
| 3/4 VIEW | PARTIAL | Same as GD11; softer nose base |
| PROFILE | PARTIAL | Preserved. Profile likeness to the reference stays as in GD11 (FAIL there); not addressed by design |
| NOSE NATURAL CONTINUITY | PARTIAL | Clearly better from below and in 3/4; front nostril show essentially unchanged |
| MOUTH / LIP INTEGRITY | PASS | No defect found, not touched; closure and visemes fine |
| EYE / BROW / EXPRESSION | PARTIAL | Kept as GD11 (brows confirmed); slight lower-sclera show remains |
| CRANIUM / JAW PRESERVATION | PASS | 0 mm |
| HAIR FIT TO HEAD | PARTIAL | Better temple and side fit; still procedural strands |
| TEMPLE / FACE FRAME | PARTIAL | Shaved band gone, no wall; over-ear groups are subtle |
| CROWN / BACK FLOW | PARTIAL | Calmer top waves; still smoother than the reference |
| BUN | PARTIAL | More compact and gathered at the same seat; could be more irregular |
| HAIR COLOUR / MATERIAL | PARTIAL | Mild correction toward warm auburn-brown |
| SKIN / AGE LIMIT | PASS | k9 unchanged; no added ageing |
| HEAD–NECK INTEGRITY | PASS | Unchanged; no seam visible |
| RIG | PASS | 27 cases including nose / upper-lip |
| LOD | PARTIAL | Face LODs pass; groom LODs not tested |
| REOPEN | PASS | Fresh editor, nothing dirty |

Artist grade for the hair: **NO.** Script-built; strand-level flow and a less regular crown still need an artist's guide groom.

## Open items / proposals (not applied)

1. **Profile likeness** (forehead–radix–nose line, as in the GD11 report): needs a decision. Changing it would alter GD11's overall type.
2. **Lower-sclera show:** a sub-millimetre lower-lid raise is possible but changes expression. Not applied without approval.
3. **Hair:** a hand-authored guide groom for the crown and bun would be the next real quality step.
4. **3/4 camera:** the boards use the existing re-solved 3/4 camera (`camfit_close`). The old "33° verified" label was not re-verified in this pass; an independent solve during the cancelled GD16 trial gave about 40–42° yaw.

## Boards (`boards/`)

| Board | Content |
|---|---|
| 01 | GD11 restore: report frames vs fresh capture; whole head |
| 02 | Front: REFERENCE / GD11 / face-only change / NEW; no-hair and clay |
| 03 | 3/4, same layout |
| 04 | Both profiles, GD11 / NEW, real and clay; generated profile labelled AUX |
| 05 | Nose / mouth / cheek close-ups, with the whole face |
| 06 | Eyes and brows with iris and groom; brow groom test |
| 07 | Hair h23 / h32: front, 3/4, both sides, back, top |
| 08 | Hair colour on identical geometry, skin, head–neck |
| 09 | Rig, LOD, turn / stop, after restart |

Raw renders: `Saved/Codex/CharacterLookdev_20260930/captures/g11base*`, `g11rr3*`, `g11rh3*`, `g11rfin*`, `g11rafter*`. Frames: `Saved/Codex/GD11_HeadRefinement_20261003/frames`.
