# SPHIRUS protagonist: GUARDIAN face identity pass (2026-10-01)

**Status: isolated candidate. NOT promoted. STOP for user review.**

| | |
|---|---|
| Continues from | `2e60b34` (report `chatgpt-bridge/reports/character-corrective-pass-2026-10-01`) |
| New assets | `/Game/Sphirus/CharacterLab/CharacterGuardian_20261001/` |
| Visual authority | THE GUARDIAN reference |

## Answer to the final question first

> "Would an art director believe this is a high-quality 3D interpretation of the same intended woman?"

**Not yet.** This pass moved the face measurably and visibly toward her. But side by side without labels she still reads as a related, different woman.

**FACE GATE: PARTIAL** (not PASS).

What remains is the overall MetaHuman bone structure and cranium, plus the expression and skin character of the photo. Measured proportions now sit within ~5% on the main features (§1).

## Final candidate composition

| Part | Asset |
|---|---|
| Face | `Face/SKM_GD_FaceMesh_h` (MetaHumanCharacter fit `MHC/MHC_GD_H` → per-LOD BR_Neutral deploy; same DNA / RigLogic) |
| Face skin | `Skin/MI_LK_Face_*_VT_c14s` (c14: ageing roll-back kept + periorbital lift; seam shading from 2e60b34; common warm tint) |
| Brows / lashes | `Grooms/GR_GD_Eyebrows_M_SlightArch` (brown MI) / `GR_GD_Eyelashes_S_Thin` (short). Library grooms bound with their template head as source mesh. |
| Hair | `Hair/GR_LK_Hair_{Main,Loose}_id18` + `Face/Bindings/GB_GD_*_h` |
| Henley | `Outfit/SKM_LK_Henley_g17e` + `MI_LK_*_g17e` (new pattern reserve; correctives + body soft-tissue transfer kept) |
| Shorts | unchanged runtime Chaos `CharacterCorrective_20261001/Cloth/CA_CR_Shorts_m1` |
| Body | `Skin/MI_GD_Body_t1` (child of the lookdev body MI, same tint factor as the face) |

## Method change that mattered

1. **Objective likeness measurement.**
   - MetaHuman's own facial contour tracker (`track_face_landmarks_from_image`) is run on the reference photos and on candidate renders from the same solved cameras.
   - Its curves (eyelids, lips, philtrum, nasolabial) are bound to the mesh.
   - A Blender preview then shows any candidate head against the reference in seconds: 50% overlay, tracker curves, silhouette and contour picks.
2. **The old 3/4 reference camera was wrong by ~14° of yaw.**
   - Evidence:
     - The reference's far/near eye width ratio is 0.69; the candidate's under the old camera was 0.27.
     - The ear picks sat 45-50 px off.
   - Re-solved with the ear tragus/lobe as yaw constraints: about 33° off frontal (was 47°).
   - Previous passes had been deforming the nose and midface to compensate for this camera error.
   - Under the corrected camera the far cheek, far eye, ear and chin all land on the reference.
   - Evidence: `boards/supporting/3q_camera_resolve_j_vs_B.jpg`, `evidence/camfit_close.json`.
3. **Art-directed structural ops instead of micro-adjustments.**
   - `blender_gd_shape.py` provides ellipsoid moves, smooth lateral widening and teeth moved rigidly with the mouth.
   - Seven iterations (A–H) were judged on front, 3/4, profile and in UE real renders.
   - Rejected steps: an over-wide lower face in D/E (the reference's "wide lower cheek" picks were on hair), and lumpy ellipsoid widening.

## 1. FACE

Measured against the reference (MetaHuman tracker on real renders, IPD-normalised, front view; `evidence/face_metrics.txt`):

| Metric | Reference | 2e60b34 (j) | New (H) |
|---|---|---|---|
| eye width | 0.460 | 0.414 (0.90) | 0.432 (0.94) |
| eye aperture | 0.157 | 0.106 (0.68) | 0.137 (0.87) |
| eye → stomion (mouth height) | 1.119 | 0.994 (0.89) | 1.072 (0.96) |
| mouth width | 0.844 | 0.863 (1.02) | 0.878 (1.04) |
| lower lip | 0.153 | 0.153 | 0.141 (0.92) |
| inner canthi spacing | 0.535 | 0.587 (1.10) | 0.545 (1.02) |

| Area | Result | Detail |
|---|---|---|
| Identity | **PARTIAL** | See the final question above. |
| Eyes / orbits | **PARTIAL+** | Fissure longer and more open (it measured squinted), inner canthi brought in 1.3 mm, heavier lateral hood. Brow ridge pushed back ~1.8 mm, so the eyes are no longer deep-set. Dark baked periorbital patch lifted (it read as eyeshadow/fatigue; the clay showed it was texture, not form). |
| Brows | **PARTIAL+** | `M_Slit` (thick, straight, with a shaved slit) replaced by a thinner, slightly arched brown brow sitting higher. |
| Nose | **PARTIAL** | Length was already right (eye→subnasale 0.67 vs 0.685). Bridge broadened, tip lowered with less projection. Still slightly narrower at the bridge than the reference. |
| Midface | **PARTIAL** | Malar moved forward; smooth lateral widening of the lower face (half of an over-wide trial). The reference's flatter, broader midface is only partly reached. |
| Mouth | **PARTIAL+** | Mouth, nose base and teeth moved down (~5.5 / 2.5 mm), giving a longer upper lip as in the reference. Flatter lower lip, thinner upper lip, near-neutral corners (reference corners are slightly down). |
| Jaw / chin | **PARTIAL** | Chin lowered ~3 mm and broadened, softer taper. Not masculine and not pointed. |
| Skull / head | **PARTIAL** | Temples/forehead widened 2–3 mm. The cranial vault was re-evaluated; it is mostly hidden by hair in the reference and was left at the 2e60b34 height. The bald head still reads tall and domed. |
| Skin age | **PASS (no ageing reintroduced)** | No wrinkle, bag or hollow reintroduced: under-eye −0.09, line normals ×0.25, plus a periorbital lift. Warmer, more tanned, more matte tint applied to head and body together, so the seam ratio is kept. |
| Asymmetry | **retained, not added** | Natural asymmetry of the base face is kept: eye centres differ, and all handles were placed on actual per-side anatomy. No new deliberate asymmetry was added. |
| Rig | **PASS (technical)** | 23 RigLogic cases before and after restart: blink closure, lip seal, teeth behind the moved lips, jaw, visemes, extreme (board 08 / 16). Re-rigging was not needed for these changes. `request_auto_rigging` (Epic cloud service) was **not run**. |

## 2. HAIR (id18; board 09)

| Area | Result | Detail |
|---|---|---|
| Crown | **PARTIAL** | Higher and more broken (`BUMP_TOP` 1.1→1.5, `L_TOP` 2.3, `MESSY_P` 0.75). |
| Hairline / part | **PARTIAL+** | Centre part (`PART_X` 0.4); forehead visible as in the reference. The fringe that covered the forehead was reduced (`FRINGE_MULT` 2.2→1.4). |
| Face framing | **PARTIAL** | Thicker, asymmetric side waves (`FACE_MULT` 3.0, `L_SIDE` 2.6, `WAVE` 1.3). |
| Bun / nape | **PARTIAL** | Looser and larger, with more escapes (`BUN_R` 3.6, `BUN_ESC` 0.9, `BUN_RV` 2.9). |
| Colour | **PARTIAL** | Lighter brown-first auburn; less tip ombre and highlights (no dark roots, no blond tips). Loose strands still catch some light tips. |
| Silhouette | **PARTIAL** | Still a tighter cap than the reference's loose updo. |

## 3. HENLEY (boards 10–12)

- **Pattern reserve: DONE (g17e).**
  - Hem girth 99→104 cm, hip 97→100.5 cm, waist 93→95 cm.
  - Sleeve reserve 1.08→1.10.
  - A longer hem plus stronger sleeve reserve (g17a / g17b) slid the shirt off one shoulder. Isolation builds (g17c / g17d) proved the combination was the cause, so the lengthening was not adopted.
- **Hem / waistband: PARTIAL.**
  - The hem is slightly looser and less ruler-straight over the Chaos shorts, with no penetration.
  - Still no real bunching or ride-up. Next step: length reserve with shoulder pinning in the sim, then a fresh selective-Chaos test on that pattern.
- **Selective Chaos:** not retested. Per the brief it should follow a pattern that already bunches, and this one doesn't yet.
- **Sleeves: PARTIAL.** Slight elbow compression; no real forearm stack or cuff bunch. SHCB and elbow correctives are kept.
- **Neckline: technically stable.** No poke-through (the soft-tissue transfer is carried into g17e).
  - The V is still deeper than the reference's buttoned placket. The 20° step was not made subtler this pass.

## 4. SHORTS (board 13)

**Unchanged and retained.** The raised crotch / rise and selective runtime Chaos (`CA_CR_Shorts_m1`, pinned waist and crotch) are kept, and verified after restart. The art polish items (§24) were **NOT DONE** this pass.

## 5. SKIN SEAM (board 15)

- **Head side:** the seam shading from 2e60b34 is carried over unchanged.
- **Body side:** isolated SRMF match `T_GD_Body_SRMF_s1` was built.
  - The measured head/body gap at the weld is already small (ratio 0.99 / 1.03), so it was **not applied** (no visible effect).
- **The remaining gameplay-sun step is not specular/roughness.**
  - Next suspect: the different subsurface scatter maps (`T_Head_Scatter_VT` vs `T_LK_Body_Scatter_clean`).
- **Status: PARTIAL.**

## 6. TECHNICAL

| Item | Result |
|---|---|
| Save / restart / reopen | **PASS**. Fresh editor, 0 dirty packages before and after (`evidence/reopen_check.json`). Face H (865 morphs, BR_Neutral, 8 LODs), hair id18 (DEFAULT LOD mode, 4 LODs), all 4 face bindings, Henley g17e (17 correctives, own MIs), Chaos shorts and MIs all load from disk. |
| After-restart captures | rig, LODs, full character, Henley set, shorts set (board 16). |
| Chaos | **PASS**: shorts unchanged. |
| LOD | **PASS**: face LOD0–3, garment LODs (board 16). |
| Preservation | **PARTIAL**. 11 of 12 protected groups byte-identical. In the 2e60b34 folder, two **QA studio** materials (`Studio/MI_LK_Backdrop`, `Studio/MI_LK_Floor2`) were re-saved by the shared QA scene setup (its studio save folder still pointed there). They are backdrop/floor materials, not character assets. No byte backup exists; the setting is now redirected to the Guardian folder. |

## Boards

| Board | Content |
|---|---|
| 01_FACE_GATE_CLAY | bald neutral clay gate |
| 02_FACE_OVERLAY | 50% overlays |
| 03_FACE_EYES | eyes / orbits / brows |
| 04_FACE_NOSE | nose |
| 05_FACE_MIDFACE | midface / cheeks |
| 06_FACE_MOUTH_JAW | mouth / jaw / chin |
| 07_FACE_REAL_SKIN | real skin, neutral |
| 08_FACE_EXPRESSION_CHECK | facial rig |
| 09_HAIR_REFERENCE | hair vs reference |
| 10_HENLEY_PATTERN | old vs new hem reserve |
| 11_HENLEY_WAISTBAND | hem / waistband |
| 12_SLEEVES | sleeves |
| 13_SHORTS_CHAOS | shorts Chaos runtime |
| 14_FULL_CHARACTER | full character |
| 15_SKIN_SEAM | neck seam |
| 16_AFTER_RESTART | after restart |

`boards/supporting/`: tracker comparison, 3/4 camera re-solve, brows × lashes, periorbital texture fix, face G vs H, Henley isolation builds.

## Explicit shortcomings (not finished)

1. **Face identity:** not yet the same woman. Next step: deeper cranial/zygomatic restructuring (broader, flatter midface; lower, rounder vault) and a mouth-corner / expression match. If the BR_Neutral route plateaus, run the MetaHuman auto-rig on a re-fit neutral.
2. **Henley:** hem bunching over the waistband and sleeve bunching are still weak; neckline depth and the 20° opening are unchanged.
3. **Shorts:** art polish not done.
4. **Seam:** the scatter-map difference is untested.
5. **Hair:** still more cap-like than the reference.

**Do NOT promote. STOP for user review.**
