# GUARDIAN-10: sculpt pass on the face neutral (option 1)

Date: 2026-10-02. Status: **STOPPED FOR USER REVIEW.** Nothing was promoted.

- **Candidate:** `/Game/Sphirus/CharacterLab/CharacterGuardian10_20261002/`.
- **Protected folders were not modified:** production and GUARDIAN 1–9. All 21 protected groups are byte-identical to the checkpoint (`data/preservation_check.json`).

## How the sculpt was done (read this first)

The pass used **stroke-by-stroke sculpt brushes** written for this pass (`tools/blender_gd10_strokes.py`):

| Brush | What it does |
|---|---|
| inflate | adds flesh along the surface normal |
| clay | builds mass along the averaged normal |
| grab | moves tissue, used here to bring tissue forward without widening |
| smooth | volume-preserving relax |
| flatten | levels bumps toward the local plane |

Every stroke is mirrored on the facial midline, as with sculpt-mode X symmetry. Each round was judged visually against the Tier A front and 3/4 photos, using clay renders and 50 % clay-over-photo blends at the verified cameras, with the Tier B profile as a low-weight check only.

**Limit:** this is not freehand sculpting with a mouse or tablet; Claude Code cannot move a brush interactively. To continue by hand, a ready-to-use Blender session is included (see the last section).

## Rounds (board 10)

| Round | Result | Decision |
|---|---|---|
| r1 | First stroke set; about 0.2–0.3 mm, not visible. | Too weak |
| r2 | About 6× stronger; ridged nose bridge, radix bump, swollen lips. | **Rejected** |
| r3 | Broad clay strokes with a smooth after each area: fuller tip, lobule and alae, continuous radix-to-bridge flow, malar and mid-cheek flesh, lower cheek and jowl brought forward (not wider), lip volume. Clean surface. | Kept as base |
| r4 | r3 plus alar-base and tip widening and a lateral-malar mass; the malar stroke made a lump below the cheekbone in 3/4. | **Rejected** (alar and tip strokes kept) |
| r5 | r3 plus the alar-base and tip widening, plus heavier brow tissue (down and forward) and a lateral hood above the lid crease. | **Adopted** |

r5 changed the upper-lid tracker curve by 0.2 mm (L) / 0.8 mm (R). Blink was checked separately.

The data for every round is in `data/strokes/r1..r5.json`.

## One fresh auto-rig on r5

- `Face/SKM_GD10_Face_s5`, `MHC/MHC_GD10_S5`, `MHC/DNA/MHC_GD10_S5_Head`.
- RigLogic, 858 morphs, 8 LODs. Fit error is 0.14 mm mean.

**Joints vs GD9 G:**

| Joint measure | GD9 G | GD10 S5 |
|---|---|---|
| Eye-joint distance (cm) | 5.901 | 5.903 |
| Eye → nose-tip joint height (cm) | 3.016 | 3.051 |
| Mouth-corner joints (cm) | 4.602 | 4.671 (fuller lips) |
| Outer cheek joints (cm) | 7.471 | 7.555 (fuller cheeks) |
| Facial joints moved > 1 mm | – | 99 of 843 |

**Verification:**
- **Rig (board 11):** 23 cases. Blink closes both eyes fully, single-eye blinks work, and there is no cornea poke-through after the brow / hood strokes. Jaw, lips and visemes are fine.
- **LOD:** board 12.
- **Fresh-editor reopen:** face (DNA user data, 858 morphs, 8 LODs), MHC, DNA, h23 grooms and the four `s5h23` bindings all load; nothing dirty before or after.
- **After restart:** board 13.

The jaw / chin balance and the C8 skull were not touched: the strokes stay in the face and are mirrored. The h23 hair is unchanged and only rebound.

## The final question

**Does the sculpted neutral read as the same intended woman before skin and hair? No, not yet.**

**Closer than GD9:**
- fuller, broader nose with a continuous forehead-radix-bridge;
- more midface and lower-face flesh;
- fuller lips;
- heavier brow tissue, which reads more adult and less "young MetaHuman".

**Still different:**
- the eye region: the reference eyes are deeper-set under a heavier brow, and the lid shape differs;
- overall face character and age: the reference reads older and broader through the cheeks;
- the reference lower face reads longer in 3/4.

The brief said to continue sculpting until convincing before the auto-rig. I stopped after five rounds because further progress needs judgement-driven freehand sculpting: stronger stroke rounds start producing lumps (r2, r4). The one auto-rig was run on the best clean sculpt so that result is banked and verified.

## Gates

| Gate | Result |
|---|---|
| NOSE | PARTIAL |
| MIDFACE / CHEEKS | PARTIAL |
| LOWER FACE | PARTIAL |
| LIPS | PARTIAL |
| FOREHEAD → NOSE CONTINUITY | PARTIAL |
| SOFT-TISSUE CHARACTER | PARTIAL |
| JAW / CHIN BALANCE PRESERVATION | PASS |
| CRANIUM PRESERVATION | PASS |
| HAIR ARCHITECTURE PRESERVATION | PASS |
| NO HOLLOWING | PASS |
| RIG | PASS |
| LOD | PASS |
| RESTART | PASS |
| IDENTITY FRONT | PARTIAL |
| IDENTITY 3/4 | PARTIAL |
| IDENTITY PROFILE | FAIL |
| SAME WOMAN BEFORE SKIN / HAIR | FAIL |
| OVERALL FACE GATE | FAIL |
| OVERALL CHARACTER LIKENESS GATE | FAIL |

## Hands-on sculpt session (to continue by hand)

**File:** `Saved/Codex/CharacterGuardian10_20261002/sculpt_session/GD10_face_sculpt_session.blend`. A copy is in this folder; the local file is the one with working reference-image paths.

**Contents:**
- `FACE_SCULPT`: the r5 neutral, in the same vertex order as the pipeline.
- X-mirror on the facial midline.
- Vertex group `LOCK` (cranium, ears, jaw contour, chin sides, collar) to use as a sculpt mask.
- Eyes as a non-selectable reference.
- Cameras `TierA_Front` (render 800×960) and `TierA_3Q` (794×940) with the Tier A photos as 50 % backgrounds. They reproduce the review framing; checked by projection to within 2 px.
- `TierB_Profile_aid`: orthographic profile with the Tier B panel, low weight.

**Coordinates:** the session is in right-handed Blender space (UE x mirrored), so the photos line up. The export mirrors back automatically; the round-trip error was measured at 0.0 cm.

**When done:** in the Text Editor, run `EXPORT_TO_PIPELINE`. It writes `head_handsculpt.npy`; then I run the review boards, one auto-rig and the rig / LOD / restart checks.

## Boards

| Board | Content |
|---|---|
| 01 | Front clay |
| 02 | 3/4 clay |
| 03 | Profile clay |
| 04 | Nose (profile / 3/4 / front) |
| 05 | Midface / cheek volume |
| 06 | Lips |
| 07 | Full profile rhythm |
| 08 | Front overlay |
| 09 | 3/4 overlay |
| 10 | Sculpt rounds |
| 11 | Rig test |
| 12 | LOD |
| 13 | After restart |

Boards 01–09 compare REFERENCE | CURRENT (GD9) | NEW SCULPT with identical cameras.
