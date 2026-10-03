# GUARDIAN-13: face-structure review (clay, before hair)

Date: 2026-10-03. Status: **STOPPED FOR USER REVIEW before hair resumes.** Nothing was promoted.

- **Candidate:** `/Game/Sphirus/CharacterLab/CharacterGuardian13_20261003/`.
- **No new UE assets yet:** the face has not been auto-rigged and the hair was not imported.
- **Protected folders were not modified:** all 25 protected groups, including GUARDIAN-12C, are byte-identical (`data/preservation_check.json`).

## What happened in this pass

1. **First round (A–D):** the eye/brow/orbit, midface, upper-lip and nasal-alar work produced checkpoint **H** (D2).
2. **Hair started on H:** I extended the hair builder (`tools/blender_gd13_hair.py`, `SPH_G13`) with irregular multi-frequency flow, crossing primary masses, lifted locks and a single-direction twist-coil bun, and built **h25**.
3. **Stopped on your instruction:** the UE import and the auto-rig were stopped before they ran. h25 is parked and not deleted (`Saved/Codex/CharacterGuardian13_20261003/hair/h25`).
4. **H unlocked:** H stays as a checkpoint only.
5. **Structural round (E1–E6) on H:** current state is **E6**. All edits are clay sculpt, evaluated in front, 33° 3/4 and profile.

## Structural round E (`data/ops/E6.json`)

**Rejected attempts:**
- **E1:** point-centred grabs were too weak to read.
- **E2:** the same grabs pushed harder made visible lumps on the zygoma in 3/4.
- **Fix:** I added a smooth **field** op to `tools/blender_gd13_ops.py`: a plateau band in z, y and |x| with no point centres, so no lumps.

| Area | Change |
|---|---|
| Zygomatic band | Pushed outward up to 3 mm per side, from the malar body back along the arch toward the ear. A smooth band over z 158–163.8. |
| Malar front | Up to 1.4 mm forward |
| Mid-cheek | 0.6 mm forward |
| Lower cheek | Up to 1.4 mm outward |
| Malar–temporal transition | Filled |
| Paranasal maxilla | Forward |
| Smoothing | A large soft cheek relax |
| Nasal bones / bridge | Sidewalls widened into the orbit, radix widened, plus a bridge-top band |
| Dorsum | A supratip dip of up to 1.4 mm was filled, so the dorsum runs as one line into the tip |
| Alar base | Widened by up to 0.8 mm (field) |
| Nostril rim | Relaxed |
| Mouth | Corners moved outward by 0.85 mm per side and relaxed; lateral upper lip given more volume |

**Unchanged:** jaw widths (8.33 / 8.41 / 10.01 cm), chin, cranium top arc, upper-temple wall and eye joints.

## Measurements

From `data/face_measurements.txt` and `data/image_ratios.json`.

**3D, in cm:**

| Measure | H (current) | E6 (new) |
|---|---|---|
| Bizygomatic (frontal zygomatic contour) | 13.75 | **14.34** |
| Upper-midface width | 13.10 | **13.54** |
| Malar lateral position, x | 5.90 | **6.19** |
| Radix width | 1.41 | **1.50** |
| Bridge width | 0.86 | **0.97** |
| Alar-base width | 2.99 | **3.09** |
| Mouth width | 5.17 | **5.32** |
| Mouth / IPD | 0.869 | **0.894** |
| Jaw widths | Unchanged | Unchanged |

**Front image, same camera as the reference:**

| Ratio | REF | H | E6 |
|---|---|---|---|
| Mouth / IPD | 0.855 | 0.838 | **0.853** |
| Alar base / IPD | 0.528 | 0.484 | 0.499 |
| Eye–stomion / IPD | 1.153 | 1.064 | 1.064 |
| Eye opening, h/w | 0.345 | 0.375 | 0.358 |

**Notes on the ratios:**
- **Mouth / IPD:** now essentially matches the reference.
- **Alar base / IPD:** still narrower than the reference.
- **Eye–stomion / IPD:** the measured ratio is shorter than the reference, not longer, so the narrow read is coming from width, not from too much height. I did not lengthen or shorten the face.

## Gates

| Gate | Result |
|---|---|
| FACE WIDTH / HEIGHT PROPORTION | PARTIAL |
| ZYGOMATIC ARCH | PARTIAL |
| MALAR POSITION | PARTIAL |
| MIDFACE PROJECTION | PARTIAL |
| MAXILLA SUPPORT | PARTIAL |
| NASAL BONE WIDTH | PARTIAL |
| RADIX WIDTH | PARTIAL |
| BRIDGE WIDTH | PARTIAL |
| DORSAL PROFILE FLOW | PARTIAL |
| TIP / SUPRATIP | PARTIAL |
| NOSTRIL SHAPE | FAIL |
| ALAR INTEGRATION | FAIL |
| COLUMELLA | PARTIAL |
| MOUTH WIDTH | PASS |
| UPPER-LIP FORM | PARTIAL |
| LOWER-LIP FORM | PARTIAL |
| MOUTH NATURALNESS | PARTIAL |
| JAW / CHIN PRESERVATION | PASS |
| CRANIUM PRESERVATION | PASS |
| NO-HOLLOWING PRESERVATION | PASS |
| IDENTITY FRONT | PARTIAL |
| IDENTITY 3/4 | PARTIAL |
| IDENTITY PROFILE | FAIL |
| OVERALL FACE GATE | FAIL |

### Honest read: the face is not convincing yet, so the hair stays paused

**Better:**
- **Cheek and midface:** the face carries more width and forward support through the cheekbones. The zygoma now continues outward toward the ear, with no lumps and no hollows (boards 01–03).
- **Nose:** the bridge is wider from the front and the dorsal dip is gone (boards 05, 07).
- **Mouth:** the width now matches the reference ratio (board 09).

**Still wrong:**
- **Nostrils and alae:** in front and 3/4 (board 08) the nostrils still read as two dark curled pockets beside a round tip, so the "three-part" nose remains. The MetaHuman base nostril topology (deep curled alar rim, open sill) is not changed by soft-tissue ops. A real fix needs either hands-on sculpting of the rim or a different base nostril shape from the MetaHuman Creator nose presets before rigging.
- **Profile:** the midface is still flat compared with the Tier B aid. The zygomatic width reads in front and 3/4, but the face plane in profile has little cheek projection.
- **Overall:** front and 3/4 are closer, but the face still reads narrower and longer through the upper face than Tier A.

**Proposed next step (your decision):**
- **Option 1:** keep pushing the midface and profile projection with field ops.
- **Option 2:** treat the nostrils and alae with a MetaHuman Creator nose-region edit, then one auto-rig.

The hair stays parked until the face gate improves.

## Boards (`boards/`)

| Board | Content |
|---|---|
| 01 | FACE_PROPORTION_FRONT (with 50 % overlays) |
| 02 | ZYGOMATIC_MALAR_FRONT |
| 03 | ZYGOMATIC_MALAR_3Q |
| 04 | MIDFACE_PROFILE |
| 05 | NOSE_BRIDGE_FRONT |
| 06 | NOSE_3Q |
| 07 | NOSE_PROFILE_DORSUM |
| 08 | NOSTRIL_ALAR_BASE (front / 3/4 / profile) |
| 09 | MOUTH_WIDTH |
| 10 | LIP_FORM |
| 11 | FULL_FACE_FRONT |
| 12 | FULL_FACE_3Q + profile |

Comparisons are REFERENCE | CURRENT (H checkpoint) | NEW (E6), clay with identical cameras and lights.
