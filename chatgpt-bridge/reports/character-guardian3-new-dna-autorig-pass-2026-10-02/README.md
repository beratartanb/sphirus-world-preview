# SPHIRUS protagonist — GUARDIAN-3: new DNA + MetaHuman auto-rig identity pass (2026-10-02)

**Isolated CharacterLab candidate. NOT promoted. STOP FOR USER REVIEW.**

| | |
|---|---|
| Continues from | `e9f3149` (GUARDIAN-2 face P, kept read-only as the comparison baseline) |
| New candidate | `/Game/Sphirus/CharacterLab/CharacterGuardian3_20261001/` |
| Final face | `Face/SKM_GD3_Face_n7` (new DNA) — from `MHC/MHC_GD3_N7`, DNA asset `MHC/DNA/MHC_GD3_N7_Head` |
| Authority | Tier A (original 3/4 portrait + original full body) decides identity. Tier B (turnaround / face-study sheets) is used only as a light profile aid. |

## Answer first

Is it the same intended woman? **Not yet.**

The method change worked technically and broke the GUARDIAN-2 structural ceiling:

- The face is a **new neutral**, solved in MetaHuman face-model space from the Tier A photos.
- It was **auto-rigged by Epic's service** into a **new DNA**. 652 of 843 facial joints were re-placed (eyes, jaw, nose, lips).
- Eye placement, eye→mouth spacing, nose profile and mouth line are measurably and visibly closer to Tier A than P.
- The rig works after an editor restart.

What still separates her from the photo:

- The new head reads as a **younger, smoother MetaHuman** woman. The skull is still the template vault; it was not rebuilt.
- The eyes are slightly narrower and rounder than hers.
- The skin lacks her sun-weathered texture.
- The hair is still a dense cap.

**OVERALL FACE GATE: FAIL** (not the same woman yet).

## Cleanup done first (user request)

GUARDIAN-2's rejected intermediates were removed (68 assets, ~830 MB). Removed:

- faces I/L2/M/N/O with their MHC assets and bindings;
- hair id19;
- skins c15/c16;
- unused default bindings.

**Archive first:** `Saved/Codex/Archive_PreGuardian3/Guardian2_rejected_intermediates.zip` (all 69 files, SHA-1 verified; restorable).

**Kept:**

- **Face N:** the RefExpression sequence uses it as its preview mesh.
- **P baseline:** face, bindings, id20, c17, RefExpression; loads intact.

## Method (what changed vs GUARDIAN-2)

1. **Face-model space instead of surface ops.**
   - The MetaHumanCharacter face model has 1397 coefficients in 22 regions. Each region has a quaternion, scale, translation and N PCA terms.
   - Its full Jacobian (all 33 845 DNA-order vertices, eyes included) was measured in the editor (`ue_gd3_jacobian.py`).
   - The PCA + translation subspace is exactly linear: predicted vs real geometry error ≤ 0.003 cm.
2. **Multi-view Tier A fit** (`gd3_fit.py`). The fit is regularised by a geometric prior, a PCA σ-ridge and a step trust region. Its terms:
   - MetaHuman tracker curves (eyelids, lips, philtrum, nasolabial) of the Tier A front photo and the verified ~33° Tier A 3/4 photo. The old 47° camera was not used.
   - Nose and ear picks, plus jaw / chin / far-cheek silhouette contours (true silhouette vertices).
   - Brow positions, measured on the mesh where the brow groom roots sit.
   - A per-view 2D similarity (absolute photo scale is solved, not imposed).
   - The Tier B profile at low weight.
   - The neck weld held, and eyeballs kept with their lids.
   - Front tracker-curve error went from 7.9 px (template) to 3.3 px; 3/4 from 17.6 to 11.9 px.
3. **New neutral → new DNA.** Eye placement in the MHC model is not tied to the old DNA; the auto-rig re-solves the joints. Steps:
   - A new MetaHumanCharacter carries **our accepted B2 body as a fixed whole rig** (`import_body_whole_rig` with the B2 DNA). This makes MHC space equal to the project frame, and the shared spine/neck/head joints equal our body (difference 0.0001 cm).
   - `fit_state_to_target_vertices` fits the face state to the new neutral (alignment NONE).
   - **`request_auto_rigging` (Epic MetaHuman service, JOINTS_AND_BLEND_SHAPES)**: ~70 s per rig, signed in as the user's Epic account. No payment, terms or credential step appeared.
   - The auto-rigged geometry reproduces the target to 0.10 mm mean.
   - DNA is exported (`.dna` + in-engine DNA asset), and the rigged head geometry is exported.
4. **Feature refinement on top of the auto-rig**, then a re-fit plus a fresh auto-rig each time:
   - brows lowered ~4.5 mm (straight, hooded fold);
   - wider nose bridge/tip/alae, thinner lips, broader chin and lower jaw;
   - measured Tier A mouth asymmetry;
   - lid hood; eye depths restored to the fitted relation.
5. **Integration.** Project face asset with the plugin face skeleton and RigLogic ABPs, P's material slots, the P-sourced hair binding (topology transfer), and a persisted DNA (see technical findings).

### Iterations (all isolated)

| Step | What | Verdict |
|---|---|---|
| fit A–I | model-space fits; fixed rotations/scales exploding (A), wrong contour vertices (neck), alar/subnasale definitions, brow + jaw terms | fit I adopted |
| N1 | template-space auto-rig test | integration route rejected (wrong frame) |
| N2 | B2 whole-rig MHC + fit I + auto-rig | first project-frame new-DNA face |
| N3 | brow mass lowered, eye depth averaged, nose/lips/chin | kept, except the eye-depth averaging (see N7) |
| N4 | canthi out, lid asymmetry, mouth shift / corner | kept |
| N5 | lower jaw +3–5 mm/side, broader chin, fuller nose tip | kept |
| N6 | upper-lid hood / lateral hood | kept; **rig test failed**: left cornea poked through the closed lid on blink |
| N7 | eyes restored to the fitted lid–eyeball relation | **FINAL**: clean blink both sides |

Also rejected:
- an earlier "eye depth averaging" (it broke the lid/eyeball relation; caught by the rig test);
- a DNA attached from the `.dna` file (rotated the head).

## Technical findings worth keeping

- **Exported MHC faces reference a TRANSIENT DNA.** `export_geometry` leaves `DNAAssetUserData` pointing at `/Engine/Transient.*_DNA`. RigLogic works in the creating session and silently does nothing after a restart.
  - Moving or duplicating the mesh drops the reference.
  - A DNA attached from the exported `.dna` file rotates the head ~90° with the plugin face ABPs.
  - **Working fix:** `import_and_attach_dna` (creates a saved reference), then `consolidate_assets` onto the in-engine DNA asset written by `export_dna`. Verified after a fresh editor start (board 20/22).
- **Hair grooms** bind to the new face with **P's face as source mesh** (same topology). A shell bug (MSYS path conversion of `/Game/...`) had hidden the hair.
- **Same-path re-creation of assets is unreliable here:** "deleted" assets stayed in memory and kept stale data. Final bindings use a fresh suffix (`_n7f`); `_n7` is stale.
- **Out-of-memory crash** after ~5 consecutive auto-rig/import cycles: restart the editor every 2–3 cycles.

## Final candidate composition

| Part | Asset |
|---|---|
| Face (new DNA, 858 morphs incl. auto-rig blend shapes, 8 LODs) | `Face/SKM_GD3_Face_n7`, DNA `MHC/DNA/MHC_GD3_N7_Head`, character `MHC/MHC_GD3_N7` (fixed B2 body) |
| Face anim | plugin `ABP_Face` (copy pose) + `ABP_Face_PostProcess` (RigLogic) |
| Skin | `Skin/MI_LK_Face_*_VT_g3s1`: child of GUARDIAN-2 c17. Less yellow, slightly red-brown, 6% darker, pore normal ×1.6, more matte. Body `Skin/MI_GD3_Body_s1` uses the same factor. |
| Eyes | `Skin/MI_GD3_Eye{L,R}_e2`: lighter, warmer iris; slightly warmer sclera |
| Brows / lashes | GUARDIAN `GR_GD_Eyebrows_M_SlightArch` / `GR_GD_Eyelashes_S_Thin`, bindings `Face/Bindings/GB_GD3_*_n7f` |
| Hair | `Hair/GR_LK_Hair_{Main,Loose}_id21`: sparser front edge, more baby hairs and face-framing strands, lower density; bindings `_n7f` |
| Reference expression | `Face/Diagnostics/AS_GD3_RefExpression`. QA pose only, not baked: calm / serious / alert. |
| Rig test sequence | `Face/Diagnostics/AS_GD3_FacialRig` (23 cases) |
| Unchanged | body, Henley g17e, Chaos shorts m1, correctives |

Intermediates kept in the candidate folder (isolated): faces n2–n5, n6r, MHC N1–N6, DNA assets, eye e1, the probe character, and stale `_n7` bindings.

## Measurements (`evidence/face_metrics.txt`; evidence, not the objective)

Tracker on the Tier A front (UE real render), normalised by inter-pupillary distance (IPD):

| Metric | Reference | P | NEW |
|---|---|---|---|
| IPD in frame (px ratio) | 1.00 | 1.08 | **1.04** |
| eye → stomion | 1.119 | 0.97 | **0.98** |
| lower lip | 0.153 | 0.91 | **1.01** |
| nasolabial top / bottom / height | | 0.93 / 1.05 / 0.87 | **0.97 / 0.97 / 1.01** |
| eye aperture | 0.157 | 0.96 | 0.99 |
| eye width | 0.460 | 0.95 | 0.92 (worse) |
| mouth width | 0.844 | 1.03 | 0.94 |
| mouth centre offset | −0.016 | −0.001 | −0.011 |
| corner drop L / R | 0.037 / 0.039 | 0.024 / 0.034 | 0.017 / 0.036 |

Tier B profile (aid, cm, + = more anterior):

| Region | P | NEW |
|---|---|---|
| nose dorsum | +0.82 | **−0.04** |
| nose tip | +0.07 | +0.23 |
| upper lip | −0.28 | +0.09 |
| lips | −0.02 | +0.18 |
| nasion | | −0.38 |

Joints, P → NEW (`evidence/joint_comparison.json`):

| Joint | P | NEW |
|---|---|---|
| eye joint distance | 6.08 cm | 5.89 cm |
| eye centre height | | +1.3 mm |
| jaw joint | | 1.0 cm lower / back |
| lip-corner joints | | ~4 mm lower |

P's joints were the archetype's, not matched to its BR_Neutral surface (board 13). The shared body joints are unchanged.

Face outline vs Tier A contour picks, NEW:

| Region | Width ratio |
|---|---|
| upper cheek | 1.15 (too wide at the zygomatic level) |
| mid / low cheek | 1.01 / 1.02 |

## Boards (`boards/`)

01_NEW_NEUTRAL_FRONT, 02_NEW_NEUTRAL_3Q, 03_NEW_NEUTRAL_PROFILE, 04_P_VS_NEW_CLAY_FRONT, 05_P_VS_NEW_CLAY_3Q, 06_REFERENCE_OVERLAY_FRONT, 07_REFERENCE_OVERLAY_3Q, 08_EYE_CENTRES_AND_ORBITS, 09_CRANIUM, 10_MIDFACE, 11_NOSE, 12_MOUTH_JAW_CHIN, 13_AUTORIG_JOINT_VALIDATION, 14_NEUTRAL_REAL_SKIN_FRONT, 15_NEUTRAL_REAL_SKIN_3Q, 16_REFERENCE_EXPRESSION, 17_HAIR, 18_HEAD_NECK_BODY, 19_FULL_CHARACTER, 20_RIG_TEST, 21_LOD_TEST, 22_AFTER_RESTART.

Face boards show REFERENCE | P | NEW from the same cameras.

## Technical tests

| Test | Result |
|---|---|
| Rig | 23 RigLogic cases on the new DNA in a fresh editor session (board 20): blink both / each side, gaze, brows, smile / frown, cheek raise, lip seal, MBP, jaw open / left / right, visemes, extreme. Teeth stay behind the lips. No eyelid penetration on N7. |
| LOD | face LOD0–3 and garment LODs (board 21); 8 face LODs present. |
| Save / restart / reopen | Fresh editor: 0 dirty packages before and after. Face (DNA attached), MHC character, DNA asset, grooms + bindings, MIs, sequences and Chaos shorts load from disk. After-restart captures on board 22 (`evidence/reopen_check.json`). |
| Preservation | 13 protected groups byte-identical to the pass checkpoint, including production `MH_MainCharacter`, GUARDIAN `dcb061c` and GUARDIAN-2 / P (`evidence/preservation_check.json`). No file under `/Game/MetaHumans` changed (MetaHuman assembly was not used). |

## Open issues

1. **Skull** not rebuilt: the template vault/occiput remains. Next: cranium terms from the Tier A 3/4 forehead/temple contour, plus a skull-envelope prior.
2. **Eyes:** fissure narrower and rounder than hers (width 0.92). Lateral canthus / lid shape is limited by the lid-on-eyeball fit.
3. **Age / skin:** reads younger and smoother. No wrinkles were allowed; next is pore / roughness breakup and tone variation.
4. **Hair** is still a dense cap with curly waves; hers is loose, damp-looking, with a low bun. Needs a lock rebuild, not parameter tweaks.
5. **Head / body seam:** a tone line is visible under studio light.
6. Mouth width 0.94 and a weak left corner drop.

## Gates

| Gate | Result |
|---|---|
| IDENTITY FRONT | PARTIAL |
| IDENTITY 3/4 | PARTIAL |
| IDENTITY PROFILE | PARTIAL |
| CRANIUM | FAIL |
| EYE PLACEMENT | PARTIAL |
| EYES / ORBITS | PARTIAL |
| MIDFACE | PARTIAL |
| NOSE | PARTIAL |
| MOUTH / JAW | PARTIAL |
| SKIN | PARTIAL |
| HAIR | FAIL |
| HEAD / NECK | PARTIAL |
| RIG | PASS |
| LOD | PASS |
| RESTART | PASS |
| OVERALL FACE GATE | FAIL |

**DO NOT PROMOTE. STOP FOR USER REVIEW.**
