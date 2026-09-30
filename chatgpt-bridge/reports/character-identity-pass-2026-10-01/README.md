# SPHIRUS protagonist: IDENTITY / LARGE-FORM pass (isolated candidate, NOT promoted)

Continues from commit `889b1d92` (report `character-face-match-2026-09-30`). Nothing is promoted. Production `MH_MainCharacter`, accepted B2, SHCB, all previous body / character candidates and all previous reports are untouched. Their files are byte-identical to the checkpoint taken before the first mutation (`evidence/preservation_check.json`).

**Status: STOPPED for user approval.**

**Final test:** "Would an art director recognise this as the same intended woman and wardrobe design?"
- **Wardrobe:** closer. The shorts are no longer dropped-crotch or long, and the Henley is shorter and softer. It is still not the concept's soft lounge set.
- **Woman:** no, not yet. The bald clay face is materially closer than 889b1d9, but it is not yet recognisably the same person. The face gate is **not passed** (details below). I am reporting this rather than calling the task finished.

## Candidate composition

| Part | 889b1d9 | This candidate |
|---|---|---|
| Face | `SKM_FM_FaceMesh_c` | `/Game/Sphirus/CharacterLab/CharacterIdentity_20260930/Face/SKM_ID_FaceMesh_c` |
| MetaHuman state | none | `.../CharacterIdentity_20260930/MHC/MHC_ID_C` (+ `MHC_ID_Base`, `Export/*_Head`) |
| Hair | `GR_LK_Hair_{Main,Loose}_v15c` | `GR_LK_Hair_{Main,Loose}_id16d` + `SM_LK_HairHelmet_id16d` (sim, 4 LODs, manual LOD mode) |
| Bindings | `GB_FM_*_c` | `.../CharacterIdentity_20260930/Face/Bindings/GB_ID_{HairMain,HairLoose,Eyebrows,Eyelashes}_c` |
| Garments | `SKM_LK_{Henley,Shorts}_g14h` | `SKM_LK_{Henley,Shorts}_g15b` + `MI_LK_*_g15b` (duplicated from `_v2`, new pattern-space textures `T_LK_*_g15b`) |
| Face skin | `MI_LK_Face_*_VT_c8` | `MI_LK_Face_*_VT_c9` (head normal map seam-blended) |
| Body skin | `MI_LK_Body_Baked_F` | `MI_LK_Body_Baked_G` (child of F, roughness offset matched to the face) |
| Body mesh / skeleton | unchanged | unchanged |

## 1. Face: the method changed

The 1–4 mm neutral-morph polish of the previous pass was dropped. What this pass inspected and used:

1. **Pipeline check.**
   - The project runs the in-editor MetaHumanCharacter plugin (UE 5.8).
   - Its Python API supports `import_from_template` (our rigged face, matched by UV), `fit_state_to_target_vertices`, `translate_face_landmarks`, `track_face_landmarks_from_image`, `export_geometry` and `request_auto_rigging`.
   - Verified in isolation: a fit reproduces a target shape to within 0.15 mm (nose +6 mm → 5.85 mm, chin −4 mm → −3.86 mm) while the eyes and teeth stay put.
2. **Reference-driven reconstruction (multi-view).** `tools/blender_id_recon.py`:
   - **Inputs:** MetaHuman tracker curves (eyelids, lips, philtrum, nasolabial) run on both the reference and the candidate renders, plus hand-picked brows, nose, ears and silhouette contours on the front and 3/4 reference.
   - **Solve:** weak-perspective reference cameras and a 220-control smooth RBF shape field, solved together (ridge, symmetry and depth priors; eyes and teeth locked; collar untouched).
   - **Result:** landmark error went from 0.12–0.28 to 0.02–0.05 IPD on lips and nose.
3. **Art-directed volume layer** (`tools/blender_id_sculpt.py`, `evidence/sculpt_g_params.txt`).
   - **Why:** 2D landmarks cannot constrain these forms, so they were judged in clay renders pixel-aligned to the reference (`boards/03b_*`).
   - **Forms added:**
     - broader, bulbous nose tip and alae;
     - zygomatic projection with a submalar hollow;
     - hooded upper lid with filled sulcus, lid bags and tear trough;
     - thinner, flatter mouth, 3 mm narrower;
     - broader, squarer chin;
     - lowered cranial vault.
4. **MetaHuman-compatible deployment.**
   - The target is fitted into the MetaHuman state (`MHC_ID_C`) and exported (DNA vertex order, all 8 LODs, the MetaHuman model's own LOD shapes).
   - Per-LOD deltas are written into the derivative face's always-on `BR_Neutral`.
   - Unchanged: DNA, RigLogic, joints, skeleton, the post-process ABP, the 858 expression morphs and the base vertices (0.0 cm difference on all 8 LODs after reopen).
   - Limitation: the rig's joint positions were **not** re-solved for the new neutral (no `request_auto_rigging` / DNA re-calibration was run). Maximum displacement is 9.5 mm, and the expression cases show no breakage (boards 13 and 15).

### What changed (face, head)
- **Eyes / orbits:**
  - upper-lid margin rotated 2.5° down on the globe;
  - lateral hooding up to 2.4 mm;
  - orbital sulcus filled 2 mm;
  - lower-lid bag 1 mm and tear trough 1 mm.
- **Brows:** follow the landmark solve. The brow groom (Slit) was kept; four MetaHuman library brows were tested (Natural, SlightArch, Fine, Thin). All render too faint and grey on this material, so none was adopted.
- **Nose:** tip rounder and fuller (+1.9 mm), alae +2 mm per side, bridge slightly broader; nose length and tip position follow the landmark solve.
- **Cheeks / midface:** zygoma +2.9 mm, submalar hollow −1.8 mm, malar fat +1.1 mm, no jowl.
- **Mouth:** upper vermilion rolled in ~1 mm, lower lip thinner and flatter (1.9 mm), corners 3 mm narrower.
- **Jaw / chin:** chin broader (+0.8 mm per side) and squarer; lower face positioned by the solve; jaw angle +0.45 mm.
- **Cranium:** vault top lowered up to 13 mm, ramped from the brow up. The reference head reads lower and rounder under the hair; front, 3/4 and profile were checked together.

### Face gate (boards 01 / 02 / 03 / 04): **NOT PASSED — PARTIAL**

**Closer in clay, front and 3/4:**
- heavier lids and smaller aperture;
- broader nose, lower in the face;
- a real cheekbone / hollow transition;
- flatter mouth and broader chin.

**Still a different person:**
- The eyes still read large and wide-set, and the orbital structure is still MetaHuman-clean.
- The reference's long, straight mid-face and flat, wide mouth line are not reproduced; the candidate mouth reads slightly pursed.
- The concept's asymmetric, lived-in expression is absent.
- The 3/4 cheek and jaw silhouette is close; the front face shape is not.

The brief says hair should not be authored before the face gate passes. I continued to the hair, outfit and seam work anyway, and those parts are **large-form candidates to re-verify** once the face is right. The honest next step for the face is below.

## 2. Hair: large forms first (id16d)
- **Authored major locks** (curve groups, not strand count):
  - 3 asymmetric fringe groups falling into the forehead;
  - 5 per side temple / face-framing S-wave locks reaching cheek, jaw and neck;
  - 3 per side long side / behind-ear locks to the shoulders;
  - 3 per side temple locks over the ear.
- **Mass and bun:** wider side / temple mass, rounded but broken top (lumps kept), lower and smaller bun, more flyaways.
- **Hairline:** keeps the v15 height, with baby hairs (2,200), a jagged edge and locks crossing it.
- **Silhouette (board 05):**
  - The front width now fills the reference outline at the temples (889b1d9 was narrow and slicked, with pink "bald" gaps).
  - The 3/4 outer mass and bun position are close.
  - Still missing: the concept's loose, voluminous crown; too many long locks sit on the shoulders; the bun is still too neat.
- **Verdict:** hair large form **PARTIAL**; hairline **PARTIAL** (height good, edge still reads groomed).

## 3. Shorts: pattern rebuild (g15b)
The crotch height was changed in the **pattern**, not by vertex pushes: crotch point, rise knee, hem heights and ease table.

| Measure | 889b1d9 (g14h) | Candidate (g15b) |
|---|---|---|
| Crotch fabric below anatomical crotch | 7.9 cm | **1.6 cm** |
| Waistband top → crotch fabric | 36.7 cm | **32.0 cm** |
| Inseam below crotch | 7.6 cm | **0.9 cm** |
| Front / back rise | 32.4 / 36.3 cm | 32.7 / 36.1 cm (back keeps seat volume) |
| Hem (inner / side) | 68.9 / 69.1 cm | 75.6 / 76.0 cm, side notch rises to ~78.7 cm |
| Leg ease at hem | +2.5 cm | +3.0–4.0 cm (relaxed opening), gather 0.22 |

- **Fabric:** lighter cloth (mass 0.15, bend 0.45).
- **Print:** botanical linework made finer (motif 11 cm vs 18 cm), lower contrast and more washed. Drawstring unchanged.
- **Correctives:** re-solved on the new geometry, with the same pose set and settings as g14h.

**Verdicts:**
- Crotch **PASS** (the dropped-crotch read is gone, no pouch, no tension).
- Lounge silhouette **PARTIAL:** the dolphin side flares a little stiffly and the front is still clean rather than soft and crumpled.
- Deformation (board 14) **PARTIAL:** no new penetration at stride, crouch, squat, hip flex or high knee. The high-knee thigh still overlaps the hem edge. A light "worn patch" on the front panel in stride and squat is the wear-mask texture (present in 889b1d9 too).
- **Body read:** no body change. The higher crotch and hem visibly lengthen the legs (board 11), which is closer to the concept.

## 4. Henley (g15b)
- Hem raised to 99.5 / 99.0 / 98.5 cm (CF / side / CB; it was 103 / 101.6 / 100.8) so it meets the shorts waistband like the concept.
- Waist / hip / hem ease +2.5–3 cm, cloth lighter.
- **Verdict PARTIAL:** shorter and softer, but still reads constructed. The V-opening is deeper than the concept's and the sleeves are not bunched.

## 5. Skin seam
- **Measured:** positions weld exactly (0 mm gap). Vertex normals differ by 1.9° mean / 6.1° max at the weld and were overridden to the body normals. Roughness was matched. The head collar normal map was blended flat over 2.5 cm around the seam (c9).
- **Result (board 12):** studio / interior seam not visible. **Grazing and low gameplay light still show a thin line: FAIL for grazing.**
- **Cause not yet found:** vertex normals, roughness and the head normal map are ruled out.
  - Next suspect: the body normal map's neck border.
  - A seam-blended body map (`T_ID_Body_N_s1`, MI `MI_ID_Body_Baked_H`) was produced. In UE it rendered the chest pink, so it is **rejected / unused** (kept in the isolated folder).

## 6. Technical gate

| Item | Status | Evidence |
|---|---|---|
| Facial rig (23 RigLogic cases, front + 3/4) | **PASS** | Board 13: blink closes, lip seal (lips closed / MBP) intact, jaw / phonemes / smile / extreme deform normally. Pre-existing left-eyeball poke-through on blink unchanged. |
| Save / restart / reopen | **PASS** | Fresh editor FinalArt13, `evidence/reopen_check.json`: face 865 morphs incl. BR_Neutral, LOD verts / skeleton / PP ABP equal to source, base diff 0.0 on LOD0–7, grooms (sim, 4 LODs, helmet, manual), 4 bindings → face_c, g15b meshes (13 / 4 morphs, own MIs), MIs and MHC assets load, nothing dirty. |
| Rig after restart | **PASS** | 46 captures vs pre-restart: max mean diff 0.005 (`evidence/rig_reopen_diff.json`, board 15). |
| Bindings (turn / bend / walk) | **PASS** (visual) | Board 14 bottom row. |
| Face LODs | **PASS** | Likeness on LOD0–7 (MetaHuman-exported LOD shapes). |
| Groom LOD switching / performance / PIE | **NOT_TESTED** | Deliberately deferred per the brief's large-forms-first rule. |
| Production / baselines untouched | **PASS** | All 8 protected groups byte-identical. In the 889b1d9 lookdev folder only the capture-studio `MI_LK_Backdrop` / `MI_LK_Floor2` were re-saved (by the QA scene setup, values unchanged); 77 new files. |

## Summary: PASS / PARTIAL / FAIL / NOT_TESTED
- **PASS:** shorts crotch height; facial rig; save / reopen; bindings; preservation.
- **PARTIAL:** face identity (gate not passed); head shape; hair large form; hairline; shorts lounge silhouette; Henley; deformation.
- **FAIL:** skin seam under grazing light; overall "same woman" test.
- **NOT_TESTED:** groom LOD transitions, runtime / PIE, performance.

## Most valuable next step
The face is the gating item.
- The fitted MetaHuman state `MHC_ID_C` now exists. The next move is to edit it directly in MetaHuman Creator with the reference beside it (eye size / spacing, mid-face length, mouth line: a judgement-driven sculpt).
- Then run `request_auto_rigging` / a DNA export so joints are re-solved for the new neutral. The morph-only deployment would then no longer be needed.
- This needs a person in the MetaHuman Creator UI (and the rig service). It is not something another scripted iteration of the same generator will fix.

## Boards
00 recon landmark fit · 01 face clay / reference · 02 face 50% overlay · 03 face planes (+03b aligned clay iterations) · 04 head shape · 05 hair silhouette · 06 hair form (+06b iteration) · 07 hairline · 08 shorts pattern / proportion · 09 shorts final · 10 Henley · 11 full character · 12 skin seam (4 lights) · 13 face expressions (front, 3/4) · 14 deformation + bindings · 15 after restart.
