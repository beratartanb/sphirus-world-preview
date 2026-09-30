# SPHIRUS protagonist: FACE MATCH / HAIRLINE / SKIN CONTINUITY pass (isolated candidate, NOT promoted)

Continues from commit `40035574ec1bd099d9e747607b76fab105f766d0` ("4003557" below). Isolated in
`/Game/Sphirus/CharacterLab/CharacterLookdev_20260930/`. Nothing is promoted. Production `MH_MainCharacter` and every accepted
baseline are byte-identical to 4003557 (see *Preservation*). The old report was not replaced; this is a new folder.

**Status: waiting for user approval. Nothing has been promoted.**

## Candidate composition

| Part | 4003557 | This candidate |
|---|---|---|
| Face mesh | `CharacterRevision_20260930/Body/SKM_RV_FaceMesh` (read-only) | `Face/SKM_FM_FaceMesh_c` (new isolated derivative) |
| Hair | `GR_LK_Hair_{Main,Loose}_v14k` | `GR_LK_Hair_{Main,Loose}_v15c` (same v14 lock architecture) |
| Hair / brow / lash bindings | `GR_LK_Hair_*_v14k_Binding`, `RV_*_Binding` | `Face/Bindings/GB_FM_{HairMain,HairLoose,Eyebrows,Eyelashes}_c` |
| Face skin MIs | `MI_LK_Face_*_VT_c3` | `MI_LK_Face_*_VT_c8` (children of c3) |
| Body skin MI | `MI_LK_Body_Baked_C` | `MI_LK_Body_Baked_F` (child of C) |
| Body / garments | `SKM_LK_BodyMesh`, `g14h` | unchanged |

## Method (short)

- **Measure first (§0).** Reference and captures were compared in a *pupil-aligned* frame: a similarity transform maps the candidate's projected pupils onto the concept's, so both share one scale. The first grid readings were distorted by a non-uniform crop; the aligned frame corrected them. That correction reversed two early conclusions: the lower face is *not* shorter, and the jaw should *not* be narrowed.
- **Hairline before geometry (§1–2).** The hairline was fixed by re-authoring the groom's root region. Scalp and cranium were then found adequate (no-hair and clay views), so no skull edit was made.
- **Face (§3–4).** The MetaHuman-safe route was used: the likeness is written only into the candidate's own copy of the always-on `BR_Neutral` morph. That morph is already driven to 1 by the referenced post-process ABP. The collar deltas are kept, and the likeness is transferred to LOD1–7 barycentrically. DNA, RigLogic, joints, skeleton, the 858 expression morphs, the post-process ABP and the base vertices are untouched; base-geometry difference is 0.0 cm on all 8 LODs after reopen.
- **Skin (§5–6).** Material parameters were matched, then the remaining head-collar/body albedo step was removed with a low-frequency, multiplicative gain in texture space. The gain converges to the body exactly at the 92-vertex weld seam and fades out over 5 cm, so detail is preserved; this is not a painted band.

## Changes

### Face geometry (`SKM_FM_FaceMesh_c`, `BR_Neutral` = collar deltas + likeness)
- 16.4k head vertices move: max 3.9 mm, p99 2.8 mm. Eyeballs, teeth and saliva are locked to 0; below z 146.5 cm only the original collar deltas remain.
- **Eyes:** upper lid margin rotated 5.5° down about the eyeball centre (stays on the globe). Lateral fold hooding 2 mm, lower lid 0.6 mm up.
- **Brows:** brow soft tissue 2 mm lower and slightly forward.
- **Lips:** upper vermilion thinned (border rolled toward the stomion, up to 2.5 mm). Lower lip slightly less everted; mouth corners 0.5 mm in.
- **Chin:** 2.7 mm lower and slightly forward, broader and squarer (+1.4 mm per side). Lower jaw 1 mm fuller; the candidate tapered to a point.
- **Nose:** tip 0.8 mm longer / less upturned.
- **Ageing soft tissue:** buccal flattening 1 mm, mild malar definition, nasolabial fold (1 mm groove + 1 mm cheek mass), tear trough 0.7 mm, lower-lid bag 0.6 mm, marionette 0.5 mm, subtle asymmetry.
- All parameters are in `evidence/face_c_params.txt`; generator `tools/blender_fm_face_delta.py` (v2 block).

### Skull / scalp
- **None.**

### Hairline and hair (v15c, v14k architecture kept)
- **Hairline:**
  - The frontal hairline was re-authored as an azimuth-dependent root boundary: centre 168.6 cm, temporal recession 38–50°, temples brought forward and down (164.8 / 162.0 cm at 62 / 74°).
  - Sparse edge (30 % density) ramping over 1.3 cm with a jagged micro-breakup; 1,800 fine baby hairs lying back along the edge.
  - The front root lift is lower (0.55×), so there is no pompadour or helmet roll.
- **Hair:**
  - Face-lock and curtain-wisp roots moved onto the new hairline.
  - Three new temple locks per side sweep back over the upper ear, covering the bare temple wedge that v15a/b left.
  - Locks, low messy bun loops, colour/material (`hair_mat_v14d`), loose groom, physics settings (LK_SIM as v14k), 4-level groom LOD with helmet, and manual LOD mode are all as v14k. No scaling.
  - Strands: 61.8k main / 3.9k loose (v14k: 60.0k / 3.7k).

### Skin and materials
- **Face c8** = the v2 face textures with the following changes:
  - under-eye tear-trough tone in brown, not violet;
  - periocular red excess reduced;
  - mild nasolabial and marionette tone;
  - sun-warm, uneven forehead;
  - blotchy redness in place of a uniform pink;
  - lips muted to rose-brown;
  - forehead lines, glabella lines and crow's feet in the normal map;
  - plus the calibrated seam gain (c4 → c6 → c8 iterations).
- **Body F** = C plus matched micro detail:
  - micro-skin tiling 70 → 134, matching world-space pore size across the UV-density difference (46 vs 141 cm/UV);
  - roughness offset, specular multiply and concavity multipliers moved to the face's;
  - micro normal and cavity specular matched.
  - Body colour multiplier and saturation stay C's: copying the face's made the chest sallow (MI E).
- **Seam result.** Hue / value / saturation measured 1.5 cm on each side of the seam (front, both sides, studio and interior):

  | | Before | After |
  |---|---|---|
  | Hue | 23.9° / 29.3° | within 0.3° |
  | Value | 0.764 / 0.765 | within 1.5 % |
  | Saturation | 0.35 / 0.28 | within 0.02 |

- **Superseded, no effect:** `MI_LK_Body_Baked_D` was created with parameter names that do not exist on the master (reads back fine, changes nothing). It is kept but unused. `ue_fm_skin_match.py` now refuses unknown names.

### Rig / LOD effects
- The RigLogic validation sequence `Face/Diagnostics/AS_FM_FacialRig` covers 23 cases via the ctrl_expressions curves:
  - neutral, blink, blink L, blink R;
  - look up, down, left, right;
  - brows up, brows down, smile, frown;
  - lips closed, mouth open, jaw open, jaw left, jaw right;
  - phonemes OO, EE, MBP, W;
  - cheek compress, extreme.
  - Each case was captured front and 3/4 on the 4003557 face vs the candidate (boards F, F2).
- **No regressions:**
  - lip seal (lips closed, MBP) intact;
  - teeth and inner mouth unchanged;
  - jaw and phonemes deform as before;
  - smile and cheek compress show the new nasolabial fold naturally;
  - brows move with the brow groom.
- Blink closes fully. Look-down reads slightly more closed, as expected from the hooded neutral lid.
- Likeness is present on LOD0–3 (board I). Vertex counts per LOD equal the source.

## Acceptance (§10), honest status

| Item | Status | Evidence / note |
|---|---|---|
| Face visibly substantially closer than 4003557, front AND 3/4 | **PARTIAL** (my assessment; your call) | Boards A, B, D. Clearly closer in both views: hooded lids (aperture 0.17 → 0.13 IPD, concept 0.11), lower brows, thin muted upper lip, broader longer chin (pupil→menton 1.73 → 1.78, concept 1.79), forehead lines, nasolabial / tear-trough ageing. Remaining gaps: overall skin weathering / texture density of the concept, fuller bulbous nose tip, stronger cheekbone hollows, heavier lateral lid hooding, the concept's asymmetric expression. It is closer, but not yet a likeness. |
| Hairline much closer | **PASS (height) / PARTIAL (naturalness)** | Board C. Brow→hairline 0.34 → 0.75 IPD (concept 0.84); temples covered. The edge still reads more groomed / defined than the concept's loose, broken front, and no strands fall over the forehead. |
| Head / body skin seam not perceptually obvious | **PARTIAL** | Boards E, E2. Studio / interior: albedo seam removed (numbers above). Grazing and low gameplay light: a thin line remains, a shading / normal discontinuity between the two meshes along the collar edge. It exists in 4003557 as well and is not albedo. |
| v14k progress retained | **PASS** | Same builder architecture, bun, colour, loose groom, physics, LOD chain + helmet, manual LOD (reopen check). |
| Facial rig | **PASS, no regression** / pre-existing defect noted | Boards F, F2; after reopen all 46 rig captures match the pre-restart run (max mean diff 0.005). **Pre-existing:** during blink the character-LEFT eyeball shows through the closed upper lid. Identical on the 4003557 / revision face; neutral eye geometry is symmetric; not introduced here, not fixed. |
| Bindings (hair / brows / lashes) under neutral, blink, expressions, head turn, neck bend, walk | **PASS (visual, capture scale)** | Boards F, H: no scalp gaps, floating roots or brow drift seen. |
| Save / restart / reopen | **PASS** | Fresh editor (FinalArt11) before any QA scene; `evidence/reopen_check.json`. Face_c 865 morphs incl. BR_Neutral; LOD verts / skeleton / PP ABP equal to the source; base diff 0.0 on LOD0–7; grooms, helmet, bindings (target face_c), MIs, sequence load; nothing dirty. |
| Production + accepted baselines untouched | **PASS** | `evidence/preservation_hashes.json`: all 8 protected groups hash-equal to 4003557. In the lookdev folder only 2 pre-existing files were re-saved: the capture-studio `MI_LK_Backdrop` / `MI_LK_Floor2`, re-saved with unchanged values by the QA scene setup, as in every earlier pass. 89 new files. |

### NOT_TESTED / limits
- **Groom LOD transitions:** the LOD chain is configured and verified to load (4 LODs + helmet, manual mode), but the capture's forced-LOD switch only drives skeletal meshes. The groom was not visually stepped through LODs in this pass.
- **Runtime:** no PIE / gameplay-runtime test; RigLogic was driven by an AnimSequence on the head in single-node mode with the post-process ABP active.
- **Face LOD2/3 shading:** these LODs render redder / darker than LOD0/1. This is identical on 4003557 (board I row 1), so it's pre-existing in the LOD material instances and untouched.
- **Visual review:** likeness judgements are from captures at the given cameras; no side-by-side review in the level lighting.
- **Full-body boards:** the `camera_z=90 / fov 11.5` full-body preset of the final-art harness clips the head in this pass; board G uses custom full-body cameras instead.

## Boards
A face reference match · B pupil-aligned overlays (red = concept brow / subnasale / stomion / menton levels across every frame) · C hairline (front, crown, L / R temple) · D head shape (no hair / clay) · E skin continuity (4 lights) + E2 seam zoom · F expressions (23 cases, front + 3/4) + F2 lid / lip zoom · G final concept vs character · H bindings under poses · I LOD0–3.

## Asset list (all new, isolated)
- **Face:** `Face/SKM_FM_FaceMesh_{a,b,c}` (a, b = earlier iterations); `Face/Bindings/GB_FM_*_{a,b,c}`; `Face/Diagnostics/AS_FM_FacialRig`.
- **Hair:** `Hair/GR_LK_Hair_{Main,Loose}_{v15a,v15b,v15c}` (+ RV bindings, MIs); `Hair/SM_LK_HairHelmet_v15c`.
- **Skin:**
  - `Skin/MI_LK_Face_*_VT_{c4..c8}`;
  - `Skin/Textures/T_LK_Head_{BC,N}_{c4..c8}`;
  - `Skin/MI_LK_Body_Baked_{D (no effect), E, F}`.
