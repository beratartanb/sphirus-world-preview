# SPHIRUS protagonist: CORRECTIVE art + garment-behaviour pass (2026-10-01)

**Status: isolated candidate. NOT promoted. STOP for user approval.**
Continues from `6255d92d` (report `chatgpt-bridge/reports/character-identity-pass-2026-10-01`).

- **Location:** every new asset is in `/Game/Sphirus/CharacterLab/CharacterCorrective_20261001/`.
- **Preservation:** byte-identical to the checkpoint. This covers production `MH_MainCharacter`, accepted B2, SHCB, every previous face/hair/garment candidate (Lookdev 889b1d9, Identity 6255d92) and every previous report (see §9).
- **Visual authority:** THE GUARDIAN concept.

## Final candidate composition

| Part | Asset |
|---|---|
| Face | `Face/SKM_CR_FaceMesh_j` (MetaHumanCharacter fit `MHC/MHC_CR_J` → per-LOD BR_Neutral deploy; DNA, joints and expression morphs unchanged) |
| Face skin | `Skin/MI_LK_Face_*_VT_c12s` (texture c12 + seam-shading SRMF / normal) |
| Hair | `Hair/GR_LK_Hair_{Main,Loose}_id17` + `Face/Bindings/GB_CR_{HairMain,HairLoose,Eyebrows,Eyelashes}_j` |
| Henley | `Outfit/SKM_LK_Henley_g16c` (skinned + correctives, body soft-tissue transferred), materials `MI_LK_Henley*_m1` (lived-in) |
| Shorts | **Chaos Cloth** `Cloth/CA_CR_Shorts_m1` on a `ChaosClothComponent` (leader pose = body). Source mesh `Outfit/SKM_LK_Shorts_g16c` (same pattern as g16a / g15b), materials `MI_LK_Shorts*_m1_cloth` (washed) |
| Body | unchanged lookdev body + `MI_LK_Body_Baked_G` (read-only reference) |

## Verdict summary (honest)

| Item | Result | Note |
|---|---|---|
| Preservation (10 protected groups) | **PASS** | All byte-identical to checkpoint (`evidence/preservation_check.json`) |
| Face: ageing removed | **PASS (technical) / PARTIAL (visual)** | Bags, tear trough, submalar hollow and line normals reduced. She no longer reads older or exhausted than 6255d92, and is not plastic. Some lower-lid darkness remains in some lights. |
| Face: identity forms toward GUARDIAN | **PARTIAL** | Mouth is wider and flatter with neutral corners, chin less pinched, smaller lid aperture. Still not a likeness: face is narrower, brows heavier. **FACE GATE: not passed as likeness.** |
| Face rig (23 RigLogic cases) | **PASS (technical)** | Captured before and after restart (board 13 / 14) |
| Hair id17 | **PARTIAL** | Crown breakup, top lift, forehead locks, face framing and looser bun with escapes all improved. Still reads as a tighter, darker cap than the reference updo. |
| Shorts: crotch / rise kept | **PASS** | g16a/g16c pattern measures identical to 6255d92 g15b (§3) |
| Shorts: selective Chaos | **PASS (technical) / PASS (visual A/B)** | No thigh poke-through (the skinned version has it at walk and stride). Hem reacts at high knee. **Used at runtime.** |
| Shorts: high knee R | **NOT_TESTED** | PoseLib has no right high-knee pose; ROM hip-flex window used instead |
| Henley: chest poke-through in crouch / deep bend | **FIXED (PASS)** | Pre-existing since 889b1d9 at least. Root cause and fix in §4. |
| Henley: selective Chaos hem | **NOT ADOPTED (FAIL as a benefit)** | Prototype built and A/B tested twice (plain, then with hem ease). Cut-line artifacts, drawstring hidden, hem gain only marginal. |
| Henley hem ↔ waistband ("no straight floating edge") | **PARTIAL** | No penetration, and the hem overlaps the band. The edge still reads fairly straight; more hem fabric (pattern change) is the next step. |
| Henley neckline 0/20/30/45/60/90 | **PASS (technical) / PARTIAL (visual)** | Placket does not collapse. 20° opening is moderate, a bit more than "subtle". |
| Henley sleeves bunching | **NOT_DONE** | No change made in this pass (SHCB untouched) |
| Materials: washed shorts / lived-in Henley | **PARTIAL** | m1 textures: print fade, edge wash and wear (shorts); heather, collar/cuff/elbow wear (Henley). Visible but subtle. |
| Skin seam | **PARTIAL** | Root cause found (§6). Head-side shading match removes the line in studio, interior and grazing light. A gloss step remains under the gameplay sun (body-side neck band untouched). |
| Save → restart → reopen | **PASS** | Two fresh-editor reopen checks, 0 dirty packages. Rig, garments, LODs and cloth captured after restart. |
| Final visual test ("healthy, grounded adult woman, lived-in home clothing reacting to body and each other") | **PARTIAL** | Healthier face and better shorts behaviour. Hem/waistband interaction and likeness are still short of the brief. |

## 1. Face (boards 01, 02, 03, 13)

The 6255d92 face got closer partly through ageing. That ageing was removed from geometry and texture. The primary forms were then changed.

**Geometry** (`blender_id_sculpt.py`, 6255d92 `sculpt_g` → `sc_j`)

| Term | 6255d92 | New |
|---|---|---|
| Tear trough | +0.10 | −0.05 (fill) |
| Lower-lid bag | +0.10 | −0.03 |
| Submalar hollow | −0.18 | −0.06 |
| Mouth narrow | +0.30 | −0.10 (wider) |
| Mouth corners down | 0 | −0.06 (lift) |
| Lower-lip thinning | 0.18 | 0 |
| Lower lip flat / muzzle back | – | 0.08 / 0.12 (flatter, less pursed) |
| Sulcus fill | 0.20 | 0.32 |
| Chin width | 0.08 | 0.13 (less pointed) |
| Malar | 0.12 | 0.16 (healthier cheeks) |
| Nose tip bulb / alar flare | 0.22 / 0.20 | 0.17 / 0.16 |
| Lid rotation | 2.5° | 6.5° (smaller aperture / hood) |

Pipeline: MetaHumanCharacter `import_from_template` → `fit_state_to_target_vertices` → `export_geometry`, then per-LOD BR_Neutral deploy with the seam normal override. Expression morphs, DNA and joints are unchanged.

**Skin** (`blender_fm_face_skin_c4.py`, 6255d92 = c6 + seam gain → new c12 + seam gain → c12s)

| Term | 6255d92 (c6) | New (c12) |
|---|---|---|
| Under-eye / tear-trough tone | +0.18 | −0.09 (lift) |
| Nasolabial tone | +0.08 | −0.03 |
| Marionette tone | +0.05 | −0.07 |
| Lid crease | 0.10 | 0.03 |
| Sun tone | 0.07 | 0.03 |
| Forehead, glabella and crow's-feet line normals | ×2.6 | ×0.25 |

Pores, freckles and blotchy redness are kept, so the skin is not plastic.

After the iteration the check was re-run: does she look older or exhausted? **No**, she looks less tired than 6255d92 (board 02 crops).

Iteration i (c11) was rejected: dark lower lid and pursed mouth remained.

## 2. Hair (board 04)

id17 vs 6255d92 id16d. Hairline, major-lock approach, low bun, palette, bindings, simulation and LOD chain are kept. Changes:

| Region | Parameter changes |
|---|---|
| Crown breakup / top lift | `BUMP_TOP` 0.75 → 1.1, `L_TOP` 1.9, `MESSY_P` 0.55 → 0.65 |
| Forehead-crossing locks | `FRINGE_MULT` 1.6 → 2.2, `FRINGE_DROP` 0.8 → 1.4 |
| Cheek / jaw framing | `FACE_MULT` 2.6 |
| Looser bun + nape escapes | `BUN_R` 2.7 → 3.2, `BUN_ESC` 0.6, `BUN_RV` 2.4 |

The flyaway count is unchanged (no flyaway spam).

**6255d92 defect found and fixed:** the loose groom was hidden by `GroomLODMode.MANUAL`, which picked the hidden far LOD. id17 uses DEFAULT; verified after restart.

## 3. Shorts: runtime cloth architecture (boards 05, 06a/b, 06c)

**Runtime architecture:**
- The skinned shorts mesh is **replaced at runtime** by a `ChaosClothComponent` driving `CA_CR_Shorts_m1`.
- Leader pose is the body, with a tick prerequisite on the body.

**Dataflow graph** (`DF_CR_Shorts_m1`), in order:
1. StaticMeshImport (sim = fabric section only)
2. TransferSkinWeights (from `SKM_LK_Shorts_g16c`)
3. **ProxyDeformer v3**: waistband binding, hem binding and cord follow the simulated fabric
4. MaxDistance (weight map, High 2.4 cm)
5. Backstop (distance 0, radius 40)
6. LongRangeAttachment v2 (tethers)
7. Damping 0.1
8. Collision
9. SetPhysicsAsset `PHYS_CR_ShortsCollider`

**Pin map** (board 06c, 4674 verts: 2182 pinned / 1477 partial / 1015 free):
- **Pinned (follows skinning):** waistband and upper pelvis (z ≥ 97.5), crotch core (Gaussian at x 0, z 77), CF/CB rise (|x| < 1.5 above z 80).
- **Simulated:** lower panels, ramping to the hem; the outer thigh, dolphin hem and side slit are 35% freer.

**Collision:** body capsules from the native MetaHuman physics asset (pelvis/glutes, thighs, spine), plus the backstop sphere.

**Crotch / rise preserved:** the pattern is identical to 6255d92 g15b.
- Crotch fabric 1.6 cm below the body crotch.
- Waistband to crotch 32.0 cm.
- Rise F/B 32.7 / 36.1 cm.
- The pinned crotch core keeps it there in motion.

**A/B against the skinned/corrective version** (same materials, walk / jog / sprint / hard stop / turn / crouch / squat / hip flex / high knee L / stride; front, 3/4, side, rear 3/4):
- The skinned version shows inner-thigh poke-through at walk and stride.
- Selective Chaos shows none, and its hem lags and swings naturally.
- **Adopted.**

**Own bug found and fixed:** the cloth build assigned the fabric MI to every render section, so trims and the drawstring rendered as fabric (dark cord). The material list was fixed and verified after the second restart.

## 4. Henley (boards 07, 08, 09, 09b, 11)

**Chest poke-through (pre-existing, fixed).** In crouch and deep bends the chest showed through the shirt.

Diagnosis:
- Hiding the body showed the shirt was intact. Zeroing the body `RV_Bend60/90` morphs removed the poke-through.
- The garment-corrective solver had collided against posed-body readbacks that **exclude morph targets**. So the breast "hang" soft-tissue morph (up to 3 cm) was never seen, against about 0.5 cm of shirt clearance.

Fix (`blender_cr_softtissue_transfer.py` → `g16c`):
- The body's real morph deltas were exported from the asset.
- They were transferred onto every Henley vertex within 3 cm of the body, for `RV_Bend30/60/90`, `RV_Arm*`, `RV_ArmFwd_*` and `RV_Twist_*`.
- Rule: the shirt moves at least as far as the body along the body delta. Example: Bend90 adds up to 2.7 cm on 1387 vertices.
- Neutral is unchanged. SHCB, neckline and elbow correctives are kept.

**Selective Chaos hem: prototype built, NOT adopted.**

Prototype design:
- The skinned upper (g16d) has its lower torso hidden (`M_CR_Hidden`).
- A Chaos lower piece (`CA_CR_HenleyLower_g16b`, then `_m1f`) is cut at z < 110.8, |x| < 21.
- It is pinned above z 107.5, with a 227-vertex overlap band pushed 0.8 mm out.
- MaxDistance High 3.5 cm.
- **Waistband interaction method:** proxy collision. `PHYS_CR_HenleyCollider` has the pelvis capsule inflated +2.6 cm (to 14.76 cm) and spine_02 +1.6 cm, so the hem rests on the shorts band. There is no cloth-to-cloth collision.
- Second variant `_m1f`: hem ease in the rest shape (+7% circumference, −1 cm drop below z 104).

Results:
- No penetration and correct layering.
- Cut-line dash artifacts are visible at the sides in bends.
- The shorts drawstring is hidden under the hem.
- Hem shape gain is only marginal.

**Runtime Henley = skinned/corrective g16c. No Chaos.** The hem sits over the band (hem z ≈ 96 vs band top 106.9) with no penetration, but still reads fairly straight: PARTIAL. More hem fabric (pattern) is the next step.

**Neckline / placket** (board 11, 0/20/30/45/60/90°): the placket stays intact and the buttons stay on their side. The opening grows progressively; at 20° it is moderate.

## 5. Materials (board 05 / 07 / 10)

`T_LK_*_m1` / `MI_LK_*_m1` are generated by `blender_lk_textile_tex.py` with the same pattern UVs (spec files: `evidence/spec_*.json`).

- **Shorts (washed):** print fade, wash 0.2, edge wash 0.2, edge wear 1.0, warm faded tint.
- **Henley (lived-in):** heather 0.12, edge wear, slightly yellowed edges, wear at elbows, belly, collar and under-arm.

Both MI sets have clothing-enabled copies (`*_m1_cloth`) for the Chaos asset.

## 6. Skin seam: diagnosis (boards 12, 12b, 12c)

What was ruled out:
- **Geometry:** 89 collar vertices are welded exactly to body vertices. There is no body surface under the collar, and geometric normal difference across the weld is only 1.5° (median).
- **In clay** (no textures) **the line disappears.**
- **Shader switches** were equalized: the body had Micro Skin Details ON (head OFF), and the head had Bent Normal + Material AO ON (body OFF); specular multipliers were also matched. The line remained.
- **Seam-blended body normal `T_ID_Body_N_s1`** renders correctly. The 6255d92 "pink chest" note was a Git-Bash path-mangling bug, not a material problem. The line remained with it too.
- **Baked normals off** on both sides: the line was weaker but still present.

**Root cause:** texture-space shading mismatch at the UV border along the weld.

| Measurement | Body side | Head side |
|---|---|---|
| SRMF specular (raw border band) | 0.68 | 0.54 |
| SRMF roughness (raw border band) | 0.49 | 0.69 |
| SRMF spec / rough (visible band means) | 0.60 / 0.54 | 0.54 / 0.69 |
| Baked normal along the neck border | perfectly flat (std 0) | pore detail |

**Fix (no colour paint):** `blender_cr_seam_shading.py` changes the head collar only.
- Specular ×1.11 and roughness ×0.81, converging to the visible body values at the seam (3 cm fade).
- Head normal detail fades to 30% at the weld (1.5 cm).

Result: the line is clearly reduced in studio, interior and grazing light. A gloss step remains in the gameplay sun. Next step: treat the body-side neck band (isolated body texture copies).

## 7. Shared QA (boards 06, 08, 09, 09b, 10, 11)

Both garments were captured together from front, 3/4, side and rear 3/4 in two pose sets:
- **Static** (3 s cloth settle): neutral, stride, high knee L, bend 45, twist.
- **In flight** (animation running, cloth inertia live): walk, jog, sprint, hard stop, turn, crouch, squat, hip flex.

## 8. Save / restart / reopen (board 14)

| Restart | Log | Reopen check | After-restart captures |
|---|---|---|---|
| 1 | `FinalArt17` | `evidence/reopen_check_restart1.json` | facial rig (46), Henley set (52), shorts, LOD, full |
| 2 (after the cloth material fix) | `FinalArt18` | `evidence/reopen_check_restart2.json` | shorts (52), LOD, full |

- Both reopen checks were run in a fresh editor with **0 dirty packages before and after**.
- Facial rig before vs after restart: per-pixel mean difference 0.6–0.9%, uniform across all expressions including neutral. This is render noise, with no structural change (`evidence/rig_restart_pixel_diff.txt`).
- Assets were last edited before restart 2. Henley, face and hair were unchanged between the restarts.
- A diagnostics material (`HeadMetaHuman_20260928/Diagnostics/M_QA_Clay`) became dirty in memory during clay captures with cloth components (automatic clothing usage flag). **It was never saved** and was discarded by the restart.

## 9. Preservation

Checkpoint taken before any edit (`evidence/checkpoint_hashes.json`). Re-hashed at the end; every group is **IDENTICAL**:

- production `MH_MainCharacter` (86 files)
- accepted B2 (19)
- SHCB HelperFix (4)
- BR v5 (4)
- Outfit V1 (17)
- ShoulderFix skeleton copies (168)
- CharacterFinal (29)
- CharacterRevision (81)
- Lookdev 889b1d9 (411)
- Identity 6255d92 (41)

Previous reports are untouched. No asset outside `CharacterCorrective_20261001` was written.

## 10. Defects found in earlier candidates

| Defect | Origin | Status |
|---|---|---|
| Loose groom hidden by MANUAL groom LOD mode | 6255d92 | fixed in id17 |
| "Seam-blended body normal renders the chest pink" claim was wrong (path bug) | 6255d92 report | corrected |
| Henley chest poke-through in crouch / deep bend | at least 889b1d9 | fixed in g16c |
| Corrective solver collides against posed geometry without morph targets | method limitation | worked around by the soft-tissue transfer |

## 11. Not done / next steps

- **Face:** likeness (wider face, softer brows) needs another identity iteration. The face gate is not passed as a likeness.
- **Hair:** a looser, more voluminous updo is needed to match the reference.
- **Henley:** add hem fabric (pattern change) for a softer, less straight edge over the waistband; sleeve bunching.
- **Shorts:** high knee R test pose.
- **Seam:** body-side neck band (SRMF + normal detail) in isolated body texture copies.

## Boards

| Board | Content |
|---|---|
| 01_FACE_CLEANUP | ageing removed; bald clay and skin |
| 02_FACE_PLANES | planes + 50% overlays |
| 03_FACE_SKIN_NEUTRAL | neutral skin |
| 04_HAIR_FINAL | hair |
| 05_SHORTS_STATIC | shorts static |
| 06_SHORTS_CHAOS_a / b, 06c_CHAOS_PIN_MAPS | skinned vs selective Chaos; pin maps |
| 07_HENLEY_STATIC | Henley static + crouch fix |
| 08_HENLEY_CHAOS | skinned vs hybrid Chaos hem |
| 09_GARMENT_INTERACTION, 09b | hem/waistband, incl. hem-ease variant |
| 10_FULL_CHARACTER | full character |
| 11_DEFORMATION | neckline + all motions |
| 12_SKIN_SEAM, 12b_SEAM_DIAGNOSIS, 12c_SEAM_ISOLATION | seam |
| 13_FACE_EXPRESSIONS_front / 3q | facial rig |
| 14_AFTER_RESTART | after restart |

**Do NOT promote. STOP for user approval.**
