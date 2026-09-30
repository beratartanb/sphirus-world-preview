# SPHIRUS — Character revision pass (2026-09-30)

Hair rebuild · shorts redesign · dynamic Henley · soft-tissue deformation.

**Status: isolated candidate, NOT promoted.** Nothing in production changed. This pass awaits your review.

The candidate lives in `/Game/Sphirus/CharacterLab/CharacterRevision_20260930/`. The approved concept (THE GUARDIAN board) is the visual reference on every comparison board.

## Summary

| Area | Technical | Visual / anatomical |
|---|---|---|
| Custom groom (low messy bun) | PASS | PARTIAL |
| Lounge shorts (new garment) | PARTIAL | PARTIAL |
| Henley placket and neckline | PASS | PARTIAL |
| Dynamic neckline (forward bend) | PASS | PARTIAL |
| SHCB 90–180° with Henley | PASS | PASS (underarm fold remains) |
| Soft-tissue correctives | PASS | PARTIAL (procedural, subtle) |
| LOD0 / LOD1 / LOD2 | PASS / PARTIAL / PARTIAL | PASS / PARTIAL / PARTIAL |
| Save / reopen | PASS | PASS |
| Runtime LODSync pairing | PASS (PIE) | — |
| Performance | measured (editor GPU profile) | — |

Artist grade is **NO**. The body soft tissue and both garments are procedural, not sculpted, and the brief's visual bar is not fully met.

## 1. Hair — custom groom (board `rv_02`, `rv_12`, `rv_13`)

The pipeline is Blender procedural strands, then Alembic, then an Unreal Groom through `HairStrandsFactory`. The groom is bound to the candidate MetaHuman face (`GroomBinding`). No library groom is used.

There are two grooms:

- **Main groom** `GR_RV_Hair_Main_v12` (39,665 strands, not simulated). It holds scalp coverage from a slightly off-centre part, front hair swept sideways over the temples, and a low, loose bun at the lower occiput / upper nape. The bun centre sits at z 153.8 cm with a 2.9 cm radius, built from 18 irregular locks with loops.
- **Loose groom** `GR_RV_Hair_Loose_v12` (2,762 strands, simulated). It holds temple, ear and nape tendrils, bun escapes and flyaways.

The material is an auburn instance of the MetaHuman hair material (melanin 0.66, redness 0.5). The production eyebrow and eyelash grooms are re-bound to the candidate face.

Twelve iterations were needed. These defects were found and fixed along the way:

- **Face curtain:** strand routing snapped onto the face and neck, so the arc now follows the skull radius.
- **Fringe:** the front was a dense flat hairline, so it now has a sparse, irregular hairline and a sideways sweep from the part.
- **Bun shape:** the bun was a neat round donut, so it now has fewer wraps and larger lock offsets.
- **Colour:** it was over-saturated red, so melanin and redness were lowered.
- **Simulation streaks:** fast guides interpolated into long streaks, so every loose strand is now a guide and stretch is projected.

| Acceptance (31) | Verdict | Evidence / reason |
|---|---|---|
| HAIR DESIGN | PARTIAL | It is a genuine low messy bun, but sleeker, with less face-framing wave and volume than the concept. |
| HAIR REFERENCE MATCH | PARTIAL | Bun height, part and colour family match; the concept is fuller and curlier around the face. |
| CUSTOM GROOM | YES | Built from scratch in Blender and imported as a groom asset. |
| BUN HEIGHT | PASS | Low occiput / upper nape, clearly below the crown. |
| FACE FRAMING | PARTIAL | Temple and ear wisps exist but are thin; the concept's wavy tendrils down to the jaw are weaker here. |
| NAPE / FLYAWAYS | PARTIAL | Nape wisps, bun escapes and flyaways are present but subtle. |
| HAIR PHYSICS | PARTIAL | Loose strands simulate and the bun stays stable in hold, walk, jog, stop, yaw, bend, twist, jump and crouch (`rv_13`). Root-motion inertia is NOT_TESTED: the editor world renders grooms a frame late on a translated actor. Sprint frames leave the studio lights. |
| HAIR LOD | FAIL | No groom LOD or card chain was authored. Strands render at every distance. |

## 2. Shorts — new garment (board `rv_03`, `rv_08`)

This is a new pattern, not the old trousers cut down. It has:

- a soft elastic waistband (104 cm top) with a thin drawstring through eyelets, knotted and visible below the Henley hem;
- a curved hem, higher at the outer side, with a small side slit;
- a light A-line and an inseam of about 6.5–7 cm;
- a separate seat and leg construction.

Offline skin weights now weld UV-seam duplicates. Unwelded, the hip/leg seams opened in crouch and high-knee poses, which looked like skin poke-through. The pose-space contact correctives are driven by hip-flexion RBF curves.

| Acceptance (32) | Verdict | Evidence / reason |
|---|---|---|
| SHORTS REFERENCE MATCH | PARTIAL | Length, curved hem and drawstring match. The front reads flatter and boxier than the concept, the hem roll is heavy, and there is no fabric pattern. |
| SHORT LENGTH | PASS | Inseam about 6.5–7 cm; mid-thigh visual length. |
| WAIST / HIP FIT | PARTIAL | The waist sits right; the side-hip volume is bulky. |
| CROTCH | PARTIAL | No hanging crotch; the front crotch stitch arch still reads slightly constructed. |
| SEAT / GLUTE READ | PARTIAL | The glutes read; a mild seat ledge remains. |
| THIGH OPENING | PARTIAL | The A-line opening is fine; the side slit opens visibly in stride and high knee. |
| DEFORMATION | PARTIAL | Seam holes are fixed. Residual penetration below. |

Residual shorts penetration in the LOD0 eval (vertices inside the body):

| Pose | Vertices | Max depth |
|---|---|---|
| Crouch | 98 | 0.96 cm |
| High knee | 108 | 1.56 cm |
| Stride | 18 | 1.06 cm |

## 3. Henley (boards `rv_04`, `rv_05`, `rv_09`)

- **Construction:** a real overlapping placket. The outer band covers the cut in the closed zone, narrow bands follow the open V, and there are four buttons (top two open).
- **Neckline:** a wide scoop, lowered and widened (centre 129.2 cm, half-width 9 cm). Clavicles and upper sternum are visible.
- **V profile:** a post-simulation constraint keeps the open V straight. Previously, bust tension opened the middle wider than the top and it read as a keyhole.
- **Hem:** raised at the front to 102.8 cm, so the drawstring is visible as in the concept.

Two import defects were found and fixed:

- **Inverted normals:** the mesh import reversed triangle winding, so the panels faced inward and were invisible under one-sided material. This import code is shared with the previous CharacterFinal outfit, which likely has the same defect.
- **Underarm hole:** UV-seam duplicates at the armhole got different weights and pulled apart at 150–180°. Welded weights and a welded corrective solve fixed it.

The garment correctives are solved in Blender cloth against the posed, soft-tissue-deformed body. The cloth rest lengths come from the bind shape. There are 11 correctives: neckline gravity at 30°, 60° and 90° of bend, and underarm/neckline at 90°, 120°, 150° and 180° per side. They are driven continuously by the spine-flexion and arm-elevation RBF curves, and SHCB is untouched.

| Acceptance (33) | Verdict | Evidence / reason |
|---|---|---|
| PLACKET CONSTRUCTION | PASS / PARTIAL | Technically real cloth construction. Visually the buttons and bands bunch at the V bottom in deep bends. |
| STATIC NECKLINE | PASS / PARTIAL | Open decollete with clavicles and upper sternum. The V is shorter than in the concept. |
| DYNAMIC NECKLINE | PASS / PARTIAL | Continuous and gravity-driven, with no pops across 0/20/30/45/60/90° (`rv_05`). It opens too much already at 20°. That early opening comes from skinning, which reduced gravity and corrective gain did not change. |
| FORWARD-BEND DRAPE | PARTIAL | The drape follows the bend; small skin spots show on the shoulders at 90° bend. |
| CHEST COLLISION | PARTIAL | No visible breast poke-through at LOD0. The eval's upper-band hits are at the neck opening and cleavage, where the body surface reference is unreliable. |
| SHCB 90 | PASS | Clean. |
| SHCB 120 | PASS | Clean. |
| SHCB 150 | PASS | Clean; an underarm fold remains. |
| SHCB 165 | PASS | Clean; an underarm fold remains. |
| SHCB 180 | PASS | Clean; the neckline deepens with arm elevation. |

## 4. Body — soft tissue (boards `rv_06`, `rv_07`)

There are 19 procedural pose-space correctives on the body at LOD0–3, driven at runtime by six RBF drivers in the candidate post-process AnimBP:

- bend (RV_Bend30/60/90),
- twist (RV_Twist_l/r),
- arm elevation (RV_Arm090–180, RV_ArmFwd per side),
- hip flexion (RV_Hip075/110 per side).

The breast gravity gain was doubled in this pass: 90° bend now peaks at 3.0 cm, up from 1.4. The before/after boards use the same cameras. BEFORE is skinning plus SHCB with the soft-tissue morphs forced to 0. AFTER includes the correctives.

| Acceptance (34) | Verdict | Evidence / reason |
|---|---|---|
| BREAST FORWARD-BEND | PARTIAL | Visible gravity descent (up to 3.0 cm); the base breast shape is still sculpt-limited. |
| BREAST ARMS-UP | PARTIAL | Lift and flattening are present but subtle (≤0.9 cm). |
| BREAST TWIST | PARTIAL | Lag present, subtle (≤0.4 cm). |
| ABDOMEN COMPRESSION | PARTIAL | Bulge and crease in bend, subtle. |
| GLUTE HIP-FLEX | PARTIAL | Spread and flattening present (≤0.55 cm). |
| GLUTE SQUAT | PARTIAL | Present (≤0.94 cm). |
| THIGH / KNEE FLEXION | PARTIAL | Hamstring and inner-thigh spread in deep flexion; the knee uses skinning only. |
| SHOULDER | PASS | Accepted SHCB, unchanged. |
| SOFT-TISSUE DEFORMATION | PARTIAL | Technically PASS: driven, continuous, and persists after save/reopen. Visually subtle and procedural; not artist-grade. |

## 5. LOD (board `rv_11`)

The garment LODs are topology-aware: Blender un-subdivide on the cloth panels and light collapse on the details.

| LOD | Henley verts / tris | Shorts verts / tris |
|---|---|---|
| LOD0 | 8,251 / 15,575 | 5,557 / 10,116 |
| LOD1 | 4,426 / 8,222 | 3,024 / 5,374 |
| LOD2 | 2,497 / 4,532 | 1,711 / 2,904 |

**Root cause of the broken LOD2, found and fixed:** the body's LOD settings asset removes up to 266 helper bones at lower LODs (twist correctives, thigh forward/back, biceps, latissimus). The garment LOD2 had about 820 (Henley) and 1,020 (shorts) units of weight on those bones, so it stopped following the body. Garment LOD weights are now remapped to the nearest kept ancestor for the paired body LOD (`rv_weights_lod_remap.py`).

| LOD | Verdict | Reason |
|---|---|---|
| LOD0 | PASS | Follows all tested poses. |
| LOD1 | PARTIAL | Same issues as LOD0 plus shoulder skin spots in bend. |
| LOD2 | PARTIAL | Now follows the pose. Residual penetration against the lower-resolution LOD2 body. |

LOD2 residuals from the eval:

| Pose | Shorts vertices inside body | Max depth |
|---|---|---|
| Squat | 348 | 9.0 cm |
| Walk | 194 | 4.9 cm |

The LOD2 squat rear view also exposes the body's baked lower underwear. Only the top was repainted out of the body texture.

## 6. Save / reopen / runtime (board `rv_14`, `data/reopen_check.json`, `data/lodsync_check.json`)

The editor was killed and relaunched, then every asset was reloaded from disk with no dirty packages before or after. After reopen:

- body: 26 morphs, of which 19 are RV soft-tissue and 6 SHC;
- Henley: 11 correctives; shorts: 4 correctives;
- LODs: 4 on the body, 3 on each garment, 8 on the face;
- AnimBP up to date, with all six RV driver nodes present;
- all 19 RV curves registered as morph curves;
- both grooms loaded with bindings to the candidate face and the auburn material (0.66 / 0.5);
- loose groom simulation on, main groom off;
- eyebrow and eyelash bindings, and the pose-library animation, load.

The post-restart renders match the pre-restart state. **PASS.**

**Runtime LODSync, PASS (Play-In-Editor).** A test Blueprint (`Test/BP_RV_LODSyncTest`) has the face as Drive and the body and garments as Passive with explicit mappings. Stepping the forced LOD 0 to 7 gave these results:

| Face LOD | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| Body LOD | 0 | 0 | 1 | 1 | 2 | 2 | 3 | 3 |
| Henley and shorts LOD | 0 | 0 | 1 | 1 | 2 | 2 | 2 | 2 |

The natural screen-size LOD was face 2, body 1, garments 1. LODSync does not tick in the editor world, so an editor-world test is invalid.

## 7. Performance (`data/perf_summary.json`)

Measured with `ProfileGPU` on an NVIDIA RTX 4060 Laptop GPU. This is an editor build rendering a 1400×1400 scene capture at a gameplay-like distance, LOD0, with the walk animation playing.

| Item | GPU ms (inclusive) |
|---|---|
| Frame, hair on / off | 8.86 / 6.13 |
| Hair passes (interpolation 1.31, visibility 0.51, voxelization 0.16) | 2.00 |
| Hair ray-tracing geometry update | 1.04 |
| Loose-strand simulation (Niagara spring solver) | 0.33 |
| Morph updates: body / Henley / shorts / face | 0.019 / 0.012 / 0.012 / 0.021 |
| GPU skin cache | 0.04 |
| Shadow depths (whole scene) | 0.70 |

Three items are NOT_TESTED:

- **Garment simulation:** there is no runtime cloth; the garments use baked correctives only.
- **LOD transition cost:** not measured.
- **Shipping-build and console performance:** not measured.

## 8. Preservation and disclosed changes (`data/preservation_hashes.json`)

These are unchanged (same sha1 as the CharacterFinal baseline, and no file newer than the pass start):

- production `MetaHumans/MH_MainCharacter`,
- accepted B2 `NativeBody_20260928`,
- accepted SHCB `ShoulderFix_20260928/HighElevCorrective/HelperFix`,
- BR v5 `BodyRealism_20260929`,
- Outfit V1 `Outfit_Home_20260929`,
- the previous CharacterFinal candidate.

Disclosed changes outside the candidate folder:

1. **Shared skeleton copy.** `ShoulderFix_20260928/Common/.../metahuman_base_skel` got 19 additive curve-metadata entries so the RV curves drive morphs (sha1 52ca6620d996 → 8146cfb1cadf). Mesh-level curve metadata is not exposed to Python. A pre-change copy is in `checkpoint_skeleton/`.
2. **Project plugins.** `sphirus.uproject` now enables AlembicHairImporter and HairStrands. A backup is in `checkpoint/`.
3. **Editor setting.** Editor CPU throttling is off for the capture session.

The candidate folder also holds superseded work: intermediate grooms v1–v12p, the broken first pose-library attempt `AN_RV_PoseLib`, and the test Blueprint. None of it is deleted without your go-ahead.

## 9. Not done / honest gaps

- There is no hands-on artist sculpt pass on the body or garments. Shape quality is procedural.
- The optional local runtime Chaos cloth from the preferred hybrid was not implemented. The neckline and underarm use pose-space correctives only.
- There is no groom LOD or card chain.
- Hair motion under real locomotion root motion is NOT_TESTED, because the editor world lags grooms on translated actors.
- No sudden-stop body animation exists. A frozen-pose hair "stop" segment is shown instead.
- The body's baked lower underwear is still in the skin texture; only the top was removed.

## Boards

| File | Content |
|---|---|
| `rv_01_final_views` | Final candidate, 5 views, clay, close-ups, concept |
| `rv_02_hair_reference` | Concept vs groom: front, 3/4, sides, back, rear 3/4 |
| `rv_03_shorts_reference` | Concept vs shorts: crotch/hem, thigh opening, side hip, seat, waistband |
| `rv_04_henley_neckline` | Static neckline and placket vs concept |
| `rv_05_dynamic_neckline` | DYNAMIC HENLEY NECKLINE, 0/20/30/45/60/90°, chest-tracking cameras |
| `rv_06_breast_softtissue` | Clay before/after, same cameras |
| `rv_07_lower_softtissue` | Abdomen, glute and thigh before/after |
| `rv_08_deformation_1..3` | Full deformation set (20 poses × 3 views) |
| `rv_09_shcb` | 90/120/150/165/180° |
| `rv_10_gameplay` | Idle, walk, jog, sprint, jump, crouch, plus a gameplay camera |
| `rv_11_lods` | LOD0–2 in neutral, walk, deep squat, 180°, bend 60° |
| `rv_12_hair_poses` | Hair per gameplay pose |
| `rv_13_hair_motion` | Real-time hair motion sequence |
| `rv_14_after_reopen` | Renders after editor restart |

**Promotion requires your explicit approval. Nothing was promoted.**
