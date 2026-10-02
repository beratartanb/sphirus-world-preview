# GUARDIAN-8: hair architecture (side hair start, bun height/position, rear mass) on the locked C8 face

Date: 2026-10-02. Status: **STOPPED FOR USER REVIEW.** Nothing was promoted.

- **Candidate:** `/Game/Sphirus/CharacterLab/CharacterGuardian8_20261002/` (hair and bindings only).
- **Protected folders were not modified:** production and GUARDIAN 1–7. All 19 protected groups are byte-identical to the checkpoint (`data/preservation_check.json`).

## What is locked and what changed

- **Locked:** the GUARDIAN-7 C8 face, DNA and skull (`CharacterGuardian7_20261002/Face/SKM_GD7_Face_c8`, read-only). Jaw/chin balance, non-hollow soft tissue, skin k7 and the cranium are unchanged. No new auto-rig was needed.
- **New hair:** `Hair/GR_LK_Hair_{Main,Loose}_h23`, built with `blender_gd8_hair.py` (an extension of the GUARDIAN-7 lift-field builder).
- **New bindings:** `Face/Bindings/GB_GD8_*_c8h23`, targeting the C8 face.
- **Profile guide image:** the user-marked image mentioned in the brief did not arrive with the task. The written direction was followed (side mass further back and higher, side-head plane more open). The side-start metrics and guide in board A can be checked against the user's marked curve.

## Structural causes found in the GD7 groom

1. **Ear drape.** A lock rule (`SPH_EAR_D`) pulled the main locks over the ear about 2–3 cm down, creating a low side wall.
2. **Low side hairline.** The hairline above and in front of the ear (86–115°) sat at z 160.4–161.4.
3. **Forward side curtain.** Four loose temple locks, lateral face-framing locks, an ear lock over the front of the ear and a front side lock together hung in front of the ear.
4. **Bun on the nape.** The bun anchor was at z 155.0, 5.7 cm behind the nape surface, so the bun hung on the neck.
5. **Dense rear.** Even root density and high lateral fill made a smooth, blanket-like back.

## Changes (h18 → h23, each judged in UE captures and measured)

| Area | Change |
|---|---|
| Side hair start | Temporal / side hairline raised: 62° 166.8, 74° 166.0, 86° 164.2, 98° 163.2, 115° 162.0 cm. Ear drape off. Side-front root density −55 %. Lower side stand-off. Edge density ramp softened (h23) to avoid a bare-scalp band above the ear. |
| Forward curtain | Temple locks 4 → 0. Lateral face-framing locks removed (`SPH_FACE_SKIP` 2,3). Remaining face-framing locks thinner and shifted back. Front ear lock and front side lock removed. The two central face-framing wisps are kept (seen in the Tier A front). |
| Bun | Anchor z 155.0 → 159.6, y −8.3 → −7.4: lower occiput, not nape. Smaller jitter for a clearer edge. Entering locks unchanged in principle (per-lock rim entries, no funnel / ring). |
| Rear mass | Rear root density −32 %. Stronger group separation (clump +70 %, lateral fill −80 % at the rear). More secondary depth variation. |
| Nape | Nape root density ×1.8 and 8 short nape wisps, so the area under the raised bun is not bare. |
| Part | 1600 short flat part-cover hairs crossing the part line. The part stays visible but narrower. |
| Kept from GD7 | Lift field along the lock path (crown arc), loose convergence, per-lock bun entries, no part dip. |

## Measurements (`data/hair_architecture_h17_h23.txt`, `data/hair_silhouette_h17_h23.txt`)

| Measure | GD7 h17 | GD8 h23 |
|---|---|---|
| Side-mass lower edge above / in front of the ear, z at y = 3 / 1.5 / 0 (cm) | 161.4 / 160.6 / 160.5 | 164.5 / 163.6 / 163.2 |
| Side-mass forward reach at z 164.5 / 166 (cm) | 5.57 / 6.36 | 4.82 / 5.36 |
| Hair points inside the ear box, L / R | 21485 / 20225 | 580 / 576 |
| Bun-section centroid z / y (cm) | 156.0 / −7.2 | 160.6 / −6.1 |
| Bun distance off the skull at its centroid height (cm) | 4.3 | 2.1 |
| Profile stand-off, top (95°) / rear-upper (125–140°) (cm) | 3.1 / 4.5–5.1 | 3.0 / 5.0–5.2 |
| Robust front width at +4 / +6 / +8 cm above the eyes (cm) | 17.9 / 16.9 / 16.2 | 17.5 / 16.4 / 15.5 |

The side-front reach value at z 160–163 (about 11 cm) is the two kept central face-framing wisps beside the cheek, not side mass.

## Gates

| Gate | Result | Note |
|---|---|---|
| SIDE HAIR START POSITION | PASS | Profile: side mass starts above and behind the ear, side-head plane open, no hard edge. |
| SIDE HAIR MASS PLACEMENT | PARTIAL | Correct in profile. In the front view the temples and ear zone now read thinner than the Tier A front, which shows wavy hair partly over the ears (board F). |
| TEMPORAL HAIRLINE | PARTIAL | |
| TOP HAIR VOLUME | PASS | Kept from GD7. |
| CROWN PROFILE SILHOUETTE | PASS | Kept: continuous arc in the main-mass-only silhouette. |
| BUN HEIGHT | PASS | Mid-ear height, not the nape. |
| BUN POSITION | PASS | On the lower occiput, 2.1 cm off the skull. |
| BUN INTEGRATION | PARTIAL | Attached to the rear flow; looser and fuller than the reference's compact twist. |
| REAR MASS DENSITY | PARTIAL | Lower and more grouped; upper rear still smoother than the reference. |
| REAR MASS AIRINESS | PARTIAL | |
| HAIR OVERALL ARCHITECTURE | PARTIAL | |
| CRANIUM PRESERVATION | PASS | C8 unchanged. |
| JAW / CHIN PRESERVATION | PASS | |
| SOFT-TISSUE SUPPORT PRESERVATION | PASS | |
| IDENTITY FRONT | PARTIAL | |
| IDENTITY 3/4 | PARTIAL | |
| IDENTITY PROFILE | PARTIAL | |
| OVERALL FACE GATE | FAIL | |
| OVERALL CHARACTER LIKENESS GATE | FAIL | |

**Technical:** rig, LOD and restart PASS. After a fresh-editor reopen the C8 face (DNA user data, 858 morphs, 8 LODs), the h23 grooms (4 LODs) and the four `c8h23` bindings all load; nothing was dirty before or after. After-restart captures are on board G.

## Not done / open

- **Face priorities 5–6** (brows, eye-area character, skin micro-relief) were **not** worked in this pass: hair architecture was the stated priority. The face is GD7 C8 unchanged.
- **Front side read:** the profile correction leaves the temples and ear zone thinner from the front than the Tier A front. A follow-up could add loose wavy side strands that hang over the upper ear from behind the side mass, without bringing back the low side wall.
- The upper rear is still smoother than the reference; the bun is looser and fuller.
- Script-authored groom: final lock placement for the side, bun and face framing still needs artist grooming (ARTIST-GRADE = NO).

## Boards

| Board | Content |
|---|---|
| A | Side hair start / profile mass position: Tier B profile, both sides; guide overlay GD7 (red) vs GD8 (green) |
| B | Bun height / position: side + rear |
| C | Rear mass density / airiness |
| D | Top / crown silhouette, plus main-mass-only silhouette GD7 vs GD8 |
| E | Full hair before / after: identical camera, pose and light; front, 3/4, top, both sides, rear |
| F | Face front / 3/4 neutral: REFERENCE / GD7 / GD8 / GD8 with hair |
| G | Rig / LOD / after restart |
| H | Full character |
