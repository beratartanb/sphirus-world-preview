# SPHIRUS protagonist: final art quality pass (candidate, not promoted)

**Date:** 2026-09-30
**Baseline:** lookdev candidate at commit cca9314 (`CharacterLookdev_20260930`, garment g13c, hair v13w).
**Candidate:** isolated, in `/Game/Sphirus/CharacterLab/CharacterLookdev_20260930/`. Production `MH_MainCharacter` is unchanged, and nothing was promoted.
**Status:** STOPPED, waiting for user approval.

Grades mean the following:
- **PASS:** visibly achieved and verified.
- **PARTIAL:** visibly improved, but not at the brief's target.
- **FAIL:** not achieved, or regressed.
- **NOT_TESTED:** not measured.

A grade never means "technically exists". Captures are UE 5.8 editor scene captures on this RTX machine, not a packaged build.

---

## 0. Final candidate composition

The QA-scene composition is saved as `candidate_composition_qa_config.json`.

| Part | Asset |
|---|---|
| Body | `Body/SKM_LK_BodyMesh` (new isolated derivative of the read-only revision body) with post-process `Body/ABP_LK_Body_PostProcess` |
| Face | Revision `SKM_RV_FaceMesh`, read-only (geometry, identity, proportions and vertex order unchanged) |
| Henley | `Outfit/SKM_LK_Henley_g14h`: 13 correctives on LOD0–2, 3 material sections per LOD |
| Shorts | `Outfit/SKM_LK_Shorts_g14h`: 4 correctives on LOD0–2, 3 material sections per LOD |
| Textiles | `Outfit/Materials/MI_LK_*_v2` (masters `M_LK_Textile` and `M_LK_Textile_B`), `Outfit/Textures/T_LK_*_v2` |
| Hair | `Hair/GR_LK_Hair_{Main,Loose}_v14k` plus bindings, `MI_LK_Hair_v14k`, `MI_LK_HairLoose_v14k`, `SM_LK_HairHelmet_v14k`. Manual LOD mode; the loose groom is simulated. |
| Skin (QA overrides, as in the previous pass) | Body `Skin/MI_LK_Body_Baked_C`; face `Skin/MI_LK_Face_*_c3`; textures `T_LK_Head_{BC,SRMF,N}_v2`, `T_LK_Body_{BC,N,SRMF}_v2` |
| Test actor | `Test/BP_FA_LODSyncTest` |

All earlier candidates (g13c, v13w, the c2/B skins, `BP_LK_LODSyncTest`) are still on disk and untouched.

**Checkpoints:**
- `checkpoint_pre_finalart/`: the whole lookdev content folder before work.
- `checkpoint_skeleton/`: the ShoulderFix skeleton copy before its curve registration.
- Snapshots of every modified tool script.

---

## 1. What changed, and the root causes found

### Hair: new lock-authored groom

Built with `Tools/CharacterLookdev_20260930/blender_lk_hair_locks.py`. Iterated v14a to v14k against the concept, using the same head cameras plus an offline strand preview.

**Main groom (60k strands):**
- The scalp is clustered into 130 section locks, each with an authored centreline:
  - region-dependent lift: crown, parietal and front are higher, with part asymmetry;
  - drape over the ears;
  - a low-frequency wave;
  - messy lifted sections.
- Strands clump partially onto their lock, giving group breakup.
- Locks finish in 9 bun loop groups with unequal radius, tilt, turns and ends (tucked or escaping). The bun axis is forced back and slightly up.
- **Hairline:** jagged, with a density gradient: sparse fine hairs at the edge, fuller about 1.5 cm back. There is no hard fringe and no scalp showing from above (v14i → v14j → v14k, board 02 crown).

**Loose groom (simulated):**
- 9 thick S-wave face-framing locks, placed from the measured face contour to the cheek and jaw, asymmetric left/right.
- Curtain wisps from the part across the forehead corners.
- Ear locks, short nape escapes and crown flyaways.

**Colour:**
- Main melanin raised to 0.55 and redness lowered to 0.42 (brown-first auburn).
- The loose groom has its own MI with low ombre and highlights, which fixes the blond tips.

**Physics (loose groom):** bend stiffness 0.45, damping 0.15, air drag 0.3, gravity preload, stretch projection, 5 substeps and 10 iterations. The settings were applied in a fresh editor, the known crash-safe path.

**LOD:**
- LOD0 strands, LOD1 50%, LOD2 20%, LOD3 helmet mesh.
- Groom LOD mode set to **Manual**. The project cvar `r.HairStrands.LODMode=1` (auto/continuous) had been ignoring the authored chain and the helmet.

### Garments (g14h): same pattern architecture, rebuilt through the proven chain

**Root cause found:** the UE mesh build (`ue_lk_j4_meshes.py`) created skeletal meshes without a materials map. That collapsed every material ID into **one section**. In the previous candidate, the trims, buttons and drawstring all rendered with the main fabric material. This was why the drawstring was dark and the placket read as a mismatched overlay. Fixed (unique slot names, materials map) and verified: 3 sections on every LOD.

**Henley:**
- The closed placket now starts at the settled V apex and continues 1.2 cm up behind it (under-placket). The dark V-bottom cavity is gone.
- Flatter bands.
- Buttons are smaller (radius 0.34 cm, height 0.10 cm, 16 segments), muted tan, with holes.

**Drawstring:**
- Taupe cord.
- An overhand knot loop.
- Uneven, wobbling tails of 12.5 / 9.5 cm.

**Textiles** (`blender_lk_textile_tex.py`, `SPH_TEX_V2`):
- **Henley:** heathered slub jersey (a gentler rib).
- **Wear:** placed in 3D through a position map of the pattern UVs — elbows, the front hem, and edge wear at the collar, cuffs and hem, with pilling breakup.
- **Shorts:** faded, hand-screened botanical linework print (sprigs of leaflets with a broken line weight) replacing the camo blotches, plus seat, thigh and pocket wear.
- **Placket trim:** uses the body fabric colour and an overlap step.
- **Pockets:** overlap line.

**Elbow corrective:**
- New PoseDrivers `RV_Elbow_l` and `RV_Elbow_r` (lowerarm in upperarm space, swing) in `ABP_LK_Body_PostProcess`.
- New Henley morphs solved in the elbow pose.
- Its free region covers the joint **and the side-torso/underarm contact**. The eval showed that the "elbow" contact was really the lowered arm pressing the sleeve against the ribcage.

**Underarm stretch:** fixed by underarm-local weight smoothing. The forearm bunching goes back to 1.08 (1.11 was feeding the stretch) and the cap geometry back to the g13 values.

**Shorts contact region:** extended up to the waistband (hip flex and crouch).

**Neckline:** lower per-pose gravity in the 30°/60°/90° bend solves.

### Body

- **`SKM_LK_BodyMesh`:** an always-on morph `LK_Neutral`, driven by a Modify Curve (the same pattern as `BR_Neutral`). Baked on LOD0–3 with base geometry verified unchanged. Maximum displacement 0.59 cm, so no proportion change.
- **Breast and ribcage:**
  - masked Laplacian softening of the root, inframammary fold, sternum and lateral root;
  - a chest-wall fill below the fold, so there is no undercut;
  - a slightly fuller, lower lower pole and a quieter upper pole;
  - axillary tail fill toward the armpit;
  - 2 mm asymmetry.
- **Torso:** lower-abdomen and flank softness.
- **Glute:** an infragluteal fold at z 78.5 (measured posterior profile).
- **Knee:** a vastus medialis hint above the inner knee.

### Skin (texture and material only; face geometry locked)

**Root cause found:** the face's baked base colour `T_Head_BC_VT` is only **512 px**, and it carries a **grey collar band** painted into the bottom of the head UV. That band was the "back-neck dark inner band" in every previous board. It isn't the shirt: it stays when the Henley is hidden and disappears in clay (verified).

**New 4K `T_LK_Head_BC_v2`:**
- band inpainted;
- hue-selective reduction of the rosy cast, strongest on the cheeks;
- sun variation on the forehead, nose bridge and cheekbones;
- low- and mid-frequency uneven complexion with olive/red drift;
- pore-level tonal speckle;
- crisper freckles;
- collar freckles and tone matched toward the body.

**Face SRMF v2:** roughness breakup (a slightly oilier T-zone, drier cheeks, pore noise).

**Face normal v2:** the band edge flattened.

**Body BC/N/SRMF v2:**
- pink cast reduced (hands and feet keep a flush);
- sun on the shoulders, upper back, chest V, outer forearms and shins;
- mottling and pores;
- roughness breakup;
- upper chest warmed;
- a cross-fade across the head/body weld seam.

**Micro detail:** micro-skin normal strength raised to 1.0 on the face and 0.95 on the body.

### Evidence tooling added

- `lk_outfit_eval.py`: the old eval's fixed `z < 143.5` collar filter produced **false 5–7 cm penetrations** in bent poses at the neck seam. The new eval excludes points whose nearest body point lies on the open neck boundary.
- **The g13f baseline was re-evaluated with the same eval.** For example, its elbow figure changes from 136 verts / 2.42 cm (old eval) to 41 / 2.10.
- Head-tracked motion cameras.
- An interior light mode.
- A crop tool for LOD distance shots.
- Automated LODSync, reopen, perf and preservation scripts.

---

## 2. Item grades

### §1 Hair (boards 02, 09, 12)

| Item | Grade | Evidence / note |
|---|---|---|
| v13w kept (not discarded) | PASS | Still on disk. The final groom was built alongside it. |
| Scalp-close sides, combed-back look, crown volume, breakup | PARTIAL | Locks, lift and part asymmetry read clearly; the crown and sides are fuller than v13w. Still less voluminous and frizzy than the concept. |
| Face-framing locks: thicker, wavy, to cheek and jaw | PARTIAL | 9 thick S-wave locks plus curtain wisps. Still sparser and lower-contrast than the concept, and the back locks sit slightly out from the cheek. |
| Bun: several loop groups, uneven edge, nape escapes | PARTIAL | 9 loop groups, escaping ends and short nape escapes. It reads as a messy mid-occipital bun, but darker and less wispy than the concept. |
| Blond tips removed | PASS | Separate loose MI (ombre 0.2). |
| Brown-first auburn, restrained copper, no orange wig | PARTIAL | Brown-auburn at most angles; the crown still reads copper under the top key. |
| Organic, uneven silhouette | PARTIAL | Clearly more organic than v13w. |
| Visibly closer to the concept than v13w | PASS | Board 02: same cameras, three rows. |
| Guide-/lock-level authored method | PASS | 130 authored section locks plus explicit face locks, wisps and bun loops. |
| Physics: idle, walk, jog, sprint, hard stop, 90/180 turn, bend, crouch, jump/land | PARTIAL | Head-tracked stills show stable bun and swinging face locks, with no explosions or scalp pops. Stills only; no motion video. |
| LOD transitions visible, popping fixed | PARTIAL | Manual chain plus helmet (the auto cvar had been bypassing it). The distance series at 1.5–15 m shows no pop at the sampled distances. Forced-LOD captures are **not honoured by the scene-capture path** (all four look identical), so per-LOD visuals are not demonstrated. |

### §2 Body (board 07)

| Item | Grade | Note |
|---|---|---|
| Breast attachment, lateral root, axillary tail, sternum, inframammary fold, poles; no implant or sphere look | PARTIAL | Softer fold and a natural lower pole are visible in the before/after. A lateral undercut shadow remains, milder. |
| Subtle asymmetry | PASS | Left 2 mm lower. |
| Forward-bend breast response 0/20/30/45/60/90 | PARTIAL | Existing revision `RV_Bend` soft-tissue correctives plus `LK_Neutral`. Board 07 row 3 is plausible, but it wasn't retuned in this pass. |
| Abdomen and waist softness | PARTIAL | Subtle. |
| Glute and glute-hamstring | PARTIAL | Fold readable in rear 3/4, subtle. |
| Thigh and knee | PARTIAL | Subtle knee (VMO) hint. |
| Hands and feet | — | Not changed; not judged distracting. |
| Proportions, topology, face and seam unchanged | PASS | Morph only (base geometry diff 0.0 cm on all LODs), guarded above the neck seam. |

### §3 Henley (boards 04, 13)

| Item | Grade | Note |
|---|---|---|
| Pattern kept | PASS | Same builder and architecture; only details and parameters changed. |
| Placket integrated, not an overlay | PARTIAL | Same fabric, flatter, real trim material (section bug fixed). The band edge is still slightly readable. |
| V-bottom dark cavity | PASS | Under-placket covers the apex in neutral. |
| Buttons smaller and flatter | PASS | |
| Wear on collar, cuff, elbow and hem; tonal variation | PARTIAL | Present in the textures and visible under grazing light, but restrained and subtle. |
| Fold hierarchy | PARTIAL | Forearm bunching is kept; no new secondary/tertiary fold authoring survived (the stronger bunching raised stretch). |
| Reduce sleeve-cap puff | **FAIL** | Tested three ways (cap ease 1.0; angular top reduction 0.6 and 0.3). Every one raised the 180° underarm stretch (5.1–5.6 vs a 4.08 baseline), so it was reverted in favour of the stretch fix. |
| Back-neck dark inner band | PASS | Root cause was the grey collar band in the head albedo; inpainted. |

### §4 Dynamic neckline (board 06)

| Angle | Grade | Note |
|---|---|---|
| 0° | PASS | Stable. |
| 20° | **PARTIAL** | Still opens visibly (the V widens and cleavage shadow shows); the target was "almost no change". |
| 30° and 45° | PARTIAL | Restrained. |
| 60° and 90° | PASS | Deep but believable. |
| No poke-through, no black void at the placket, no placket collapse, no sudden transitions | PASS | Placket apex covered. Natural cleavage shadow remains in bends. |

### §5 Henley deformation (board 08; `eval2_g13f_deform.json` vs `eval2_g14h_deform.json`, same corrected eval)

| Item | Grade | Result |
|---|---|---|
| SHCB untouched | PASS | |
| Underarm stretch p99 at 180° | PASS | 4.08 → **2.93**. Also 150°: 3.63 → 2.66; squat 3.74 → 2.72. |
| Elbow-flex corrective | PARTIAL | New driver plus morph. Elbow pose contacts: 41 verts / 2.10 cm → **22 / 0.74 cm**, remaining at the side torso. |
| Hip-flex hem contact | PASS | Henley 0; shorts 3 / 0.20 → 0. |
| Bend and crouch contacts | PARTIAL | Bend 90: Henley 2 / 0.12, unchanged. Crouch: Henley 1 / 0.12, unchanged. |
| Full pose list tested | PASS | 20 poses × 3 views; see the table below. |

Full deformation table (penetrating verts / max cm, stretch p99):

| Pose | Henley g13f | Henley g14h | Shorts g13f | Shorts g14h | Henley stretch p99 g13f | g14h |
|---|---|---|---|---|---|---|
| neutral | 0 / 0.00 | 0 / 0.00 | 0 / 0.00 | 0 / 0.00 | - | - |
| armsfwd | 0 / 0.00 | 0 / 0.00 | 0 / 0.00 | 0 / 0.00 | 2.244 | 1.776 |
| elev90 | 0 / 0.00 | 0 / 0.00 | 0 / 0.00 | 0 / 0.00 | 2.276 | 1.78 |
| elev120 | 0 / 0.00 | 0 / 0.00 | 0 / 0.00 | 0 / 0.00 | 3.038 | 2.267 |
| elev150 | 0 / 0.00 | 0 / 0.00 | 0 / 0.00 | 0 / 0.00 | 3.627 | 2.66 |
| elev165 | 0 / 0.00 | 0 / 0.00 | 0 / 0.00 | 0 / 0.00 | 3.879 | 2.81 |
| elev180 | 0 / 0.00 | 0 / 0.00 | 0 / 0.00 | 0 / 0.00 | 4.083 | 2.925 |
| pl_twist_l | 0 / 0.00 | 0 / 0.00 | 0 / 0.00 | 0 / 0.00 | 1.405 | 1.399 |
| pl_twist_r | 0 / 0.00 | 0 / 0.00 | 0 / 0.00 | 0 / 0.00 | 1.41 | 1.406 |
| elbow | 41 / 2.10 | 22 / 0.74 | 0 / 0.00 | 0 / 0.00 | 1.334 | 1.49 |
| backext | 0 / 0.00 | 0 / 0.00 | 0 / 0.00 | 0 / 0.00 | 3.783 | 2.74 |
| pl_bend30 | 0 / 0.00 | 0 / 0.00 | 0 / 0.00 | 0 / 0.00 | 1.388 | 1.388 |
| pl_bend45 | 0 / 0.00 | 0 / 0.00 | 0 / 0.00 | 0 / 0.00 | 1.436 | 1.435 |
| pl_bend60 | 0 / 0.00 | 0 / 0.00 | 0 / 0.00 | 0 / 0.00 | 1.481 | 1.481 |
| pl_bend90 | 2 / 0.12 | 2 / 0.12 | 2 / 0.21 | 0 / 0.00 | 1.581 | 1.582 |
| crouch | 1 / 0.12 | 1 / 0.12 | 4 / 0.65 | 3 / 0.65 | 1.383 | 1.532 |
| squat | 0 / 0.00 | 0 / 0.00 | 0 / 0.00 | 5 / 0.22 | 3.742 | 2.718 |
| hipflex | 0 / 0.00 | 0 / 0.00 | 3 / 0.20 | 0 / 0.00 | 3.892 | 2.786 |
| pl_highknee_l | 0 / 0.00 | 0 / 0.00 | 65 / 1.45 | 43 / 1.81 | 1.347 | 1.345 |
| pl_stride | 0 / 0.00 | 0 / 0.00 | 0 / 0.00 | 0 / 0.00 | 1.314 | 1.313 |

### §6 Shorts (boards 05, 13)

| Item | Grade | Note |
|---|---|---|
| Silhouette kept | PASS | |
| Fine, faded, irregular botanical linework (not camo) | PARTIAL | Linework sprigs with broken lines and fading replace the camo. Sparser and fainter than the concept print. |
| Drawstring: muted taupe, cord, knot, uneven tails | PASS | Root cause (section bug) fixed. |
| Readable pockets | PARTIAL | Slanted openings read as pockets, slightly harsh dark slots. |
| Restrained wear | PASS | Seat, thigh, edges. |
| High-knee contact | **FAIL** | 65 / 1.45 → 43 / **1.81**: fewer vertices but a deeper maximum. The deep-hip driver's target is the squat thigh, not a single raised knee. |
| Crouch contact | PARTIAL | 4 / 0.65 → 3 / 0.65. |
| Hip-flex contact | PASS | 3 / 0.20 → 0. |
| Squat | note | New minor contact, 5 / 0.22. |

### §7 Skin (board 03)

| Item | Grade | Note |
|---|---|---|
| Earlier improvements kept (freckles, warmth) | PASS | |
| Pores | PARTIAL | Tonal speckle plus stronger micro normal; subtle at review distance. |
| Regional redness, less rosy | PASS | |
| Sun variation, uneven complexion | PASS | Subtle. |
| Roughness breakup | PARTIAL | Subtle. |
| Face geometry locked | PASS | |
| Grey collar band | PASS | Removed. |
| Head/body tone seam at the upper chest | **PARTIAL** | Softened on both sides but still visible undressed and inside the V. It's partly a face-vs-body *shader* difference, not only texture. |

### §8–§9 Comparisons and lighting (boards 01, 02, 10, 13)

| Item | Grade |
|---|---|
| Whole-character comparison at front, 3/4, side, rear 3/4 and gameplay | PASS |
| Neutral studio | PASS |
| Grazing light | PASS |
| Softer interior light (new harness mode) | PASS |
| Gameplay sun | PASS |

### §10 Technical (boards 11, 12, 14; JSON)

| Item | Grade | Note |
|---|---|---|
| Garment LOD0–2 | PASS | Clean in neutral, walk, squat, 180° and bend. 3 material sections per LOD. |
| Hair LOD visible switching | PARTIAL | See §1. |
| LODSync in PIE | PASS | `lodsync_check.json`: the face drives; body/Henley/shorts follow the mapping across 8 forced LODs in the game world. |
| Save, restart, reopen, verified from disk | PASS | `reopen_check.json`: all assets load, 0 dirty packages before and after; the ABP compiles; curves are registered. |
| Representative poses after restart | PASS | Board 14. |
| Hashes preserved | PASS, with one documented change | `preservation_hashes.json`: production, B2, SHCB HelperFix, BR v5, Outfit V1, CharacterFinal and CharacterRevision are unchanged. See the note below. |

**The one documented change:** the isolated **ShoulderFix skeleton copy** gained three additive curve-metadata entries: `RV_Elbow_l`, `RV_Elbow_r` and `LK_Neutral`, with the morph flag.
- Why: the elbow driver needed a registered curve. UE 5.8 also reads mesh-level `AnimCurveMetaData` (verified in engine source), but that class has no Python-writable properties.
- What didn't change: no bones, retargeting or SHCB. The revision pass used the same method.
- Safety: checkpoint in `checkpoint_skeleton/`.

### §11 Performance (`perf_final.json`)

Editor, RTX machine, gameplay framing, walking, LOD0 forced. **Not a shipping measurement.**

| Metric | Grooms on | Grooms off | Difference |
|---|---|---|---|
| GPU time, CSV mean | 9.94 ms | 7.84 ms | **2.1 ms** for hair |
| ProfileGPU frame | 10.07 ms | 7.57 ms | |
| Game thread, editor | | | +4.4 ms (includes the loose-groom sim tick) |

- **Render thread:** not reported by the editor CSV.
- **Hair passes:** visibility, transmittance, tile classification, interpolation and a voxel transmittance mask (small), about 1.0 ms listed.
- **GPU skinning of body, face and garments:** under 0.02 ms each.
- **Memory:** main groom 15.6 MB and loose groom 2.9 MB resource; body mesh 2.8 MB, Henley 0.9 MB, shorts 0.6 MB.
- **Grade:** PASS. Measured and reported; no budget was set in the brief.

### §12 Evidence

**PASS:** boards 01–14 in `boards/`, plus data JSON.

---

## 3. Remaining PARTIAL and FAIL items

**FAIL:**
- **Sleeve-cap puff:** trades against underarm stretch. Needs a cap redesign, for example a lower cap height with a gusset-like underarm.
- **Shorts high-knee contact:** needs its own driver target (a single raised thigh) rather than the squat target.

**Main PARTIALs:**
- **Hair:** less crown volume and frizz than the concept; face locks sparser; per-LOD visual demonstration blocked by the scene-capture path.
- **Neckline at 20°:** opens more than the target.
- **Placket edge:** slightly readable.
- **Henley fold hierarchy:** no new fold authoring survived.
- **Body refinements:** subtle.
- **Bend and crouch residual contacts:** small.
- **Shorts print:** sparser than the concept.
- **Head/body skin tone seam** at the upper chest.
- **Hair physics:** tested with stills only.

**Known method for the next pass (not shipped):** the garment corrective solver's REST shape key is ignored by Blender 5.2, so correctives cannot relax skinning stretch.
- Shrink-group encoding (`SPH_GC_SHRINK`) did relax it: 180° p99 went from 4.8 to 3.4.
- But it moved the whole free region 3–5 cm, so it needs a tighter free mask before use.

---

## 4. Files

- **Boards:** `boards/01_concept_vs_final.jpg` … `boards/14_after_restart.jpg`.
- **Data:**
  - `eval2_g13f_deform.json`, `eval2_g14h_deform.json`;
  - `reopen_check.json`, `lodsync_check.json`, `perf_final.json`;
  - `preservation_baseline.json`, `preservation_hashes.json`;
  - `candidate_composition_qa_config.json`;
  - `body/ue_bake_body.json`.
- **Tools** (all under `Tools/CharacterLookdev_20260930/`):
  - hair: `blender_lk_hair_locks.py`, `blender_hair_preview.py`;
  - garments: `lk_garment_chain.sh`;
  - body: `ue_lk_body_setup.py`, `blender_lk_body_art.py`, `ue_lk_bake_body.py`;
  - skin: `blender_lk_face_skin.py`, `blender_lk_body_skin_v2.py`, `ue_lk_face_skin_v2.py`, `ue_lk_body_skin_v2.py`;
  - textiles: `ue_lk_textile_master_b.py`;
  - evidence: `lk_outfit_eval.py`, `ue_lk_perf.py`, `lk_parse_perf.py`, `fa_captures.sh`, `make_fa_boards.sh`, `ue_fa_reopen.py`, `ue_fa_lodsync_*.py`, `fa_preservation.py`.

**Candidate path:** `/Game/Sphirus/CharacterLab/CharacterLookdev_20260930/`

**STOP:** nothing is promoted to production. Waiting for user approval.
