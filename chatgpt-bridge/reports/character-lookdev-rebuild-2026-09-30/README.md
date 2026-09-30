# SPHIRUS — Character lookdev / art-direction rebuild (2026-09-30)

**Status: isolated candidate, NOT promoted.** Nothing in production changed. **Artist-grade: NO.**

- **Visual target:** the approved concept *THE GUARDIAN* (`concept_guardian_approved.png`), used for hair, complexion, wardrobe, textiles and mood.
- **Face:** the user's MetaHuman face geometry is unchanged. Only skin lookdev was touched.
- **Candidate content:** `/Game/Sphirus/CharacterLab/CharacterLookdev_20260930/…`
  - Outfit: `SKM_LK_Henley_g13c`, `SKM_LK_Shorts_g13c`, `M_LK_Textile` plus six instances, textures.
  - Hair: `GR_LK_Hair_{Main,Loose}_v13w` with bindings, `MI_LK_Hair_v13w`, `SM_LK_HairHelmet_v13w`.
  - Skin: `MI_LK_Body_Baked_B`, clean body textures, `MI_LK_Face_*_c2`.
  - Studio: studio materials.
- **Body and face:** the revision candidate meshes and their post-process ABP are used read-only and are unchanged.
- **Evidence:** `Saved/Codex/CharacterLookdev_20260930/`. Boards A–J are in `boards/`.

## 0. What was done (priority order of the brief's FINAL RULE)

| Area | Before (rejected revision) | Now |
|---|---|---|
| Skill system | No owner for lookdev / costume / groom art direction | New skill `character-lookdev-costume-groom-art-direction` (SKILL.md, 11 references, SPHIRUS profile), routed from the game-dev director |
| Review conditions | Black void | Neutral grey character-review studio: soft key, fill and rim; fixed manual exposure, 6500 K white balance, ACES. Grazing-light and gameplay variants; the same cameras for every iteration |
| Skin | Pale and pink; baked underwear in the body maps | Warm golden sun-exposed complexion with freckles; face and body aligned. Underwear removed properly: the Creator's own clean detail albedo was regressed onto the character's baked albedo, and its unbaked normal used in the covered region. No flat paint-over |
| Hair | Sleek, dark red, organised bun | Rebuilt groom (v13w): brown-first auburn/copper; zig-zag part; root lift; low compact bun with loose loops; wave locks at the temples, cheeks, ears and nape; flyaways. Full density (38k strands + 2.4k loose). LOD chain; simulated loose groom |
| Henley | Offset shell, procedural folds, crude placket | **Rebuilt from real pattern pieces:** front, back and two sleeves, flattened (SLIM) and sewn. Rest shape = the pattern (ARAP sewn relaxation). Jersey cloth drape, interfaced placket with 5 buttons, stretched-on neck binding, rib cuffs, coverstitch hem, full-bust adjustment. Rib-jersey textile with tonal motif and heathered yarn; stitches only on real seams |
| Shorts | Boxy, inflated sides, crotch arch, rope hem | **Rebuilt from real pattern pieces:** four panels plus an elastic waistband. Short 6–7 cm inseam, curved dolphin hem rising to a rounded side slit, soft shallow crotch, light A-line, gathered elastic waist, drawstring, slanted pockets. Washed charcoal twill with a faded irregular leaf print |
| Deformation | Neckline opened at 20°; breast poke-through | 15 garment pose-space correctives, re-solved against the current soft-tissue body. Arm raise 90–180° and bends 30–60° are penetration-free |
| LOD | Broken LOD2 garments, no groom LOD | Garment LOD0–2 correct (root cause fixed, §9). Groom LOD chain: strands 100 % / 50 % / 20 %, then a helmet mesh |

## 1. Skill

`.agents/skills/character-lookdev-costume-groom-art-direction/`: SKILL.md plus these references:
- reference-matching, visual-acceptance-gates, character-presentation-lighting;
- groom-art-direction, hair-color-lookdev;
- garment-silhouette, garment-construction-art, textile-lookdev;
- skin-complexion-lookdev, character-material-hierarchy, failure-modes;
- sphirus-guardian-profile.

Routed from `sphirus-game-dev-director`; the body skill points to it. Claude wrappers were synced (71 skills, 0 errors).

## 2. Skin (board D)

**Complexion:**
- Face MIs `c2`: post-bake multiply (0.90, 0.83, 0.72), saturation −0.04.
- Body `MI_LK_Body_Baked_B`: multiply (0.92, 0.855, 0.765), saturation −0.09, roughness +0.10, specular ×0.85.
- Result: light / light-medium, warm golden undertone, freckles on the face, chest, shoulders, arms and legs, restrained redness.

**Clean body skin** (`blender_lk_body_clean.py`), applied inside the union of the plugin's underwear masks (dilated 22 px, feathered 12 px at 4K):
- **BC:** a per-channel quadratic regression of the Creator's clean detail albedo (`T_Skin_V1_Body_BC`) onto this character's baked albedo, fitted on clean texels (fit error 0.0035 linear), plus a push-pull low-frequency residual.
- **Normal:** the character's unbaked body normal.
- **Roughness/specular and scatter:** push-pull inpainted.
- **Result:** the garment-free hip, seat and chest views show no underwear.

## 3. Hair (boards B, C, I3, J2)

**Builder:** `blender_hair_build.py` (V13), env in `hair/v13w/build_env.txt`.
- Strands: 38,265 main + 2,444 loose; widths 0.0065 / 0.009 cm.
- Material `MI_LK_Hair_v13w`: melanin 0.46, redness 0.50, ombre/highlight layers, roughness 0.72.

**Iterations:** v13p → v13q → v13r (shadow smudge found) → v13s → v13t (full density) → v13v (compact bun, sideburn thinning) → v13w (lift, ear drape, denser face waves).

**Fixed along the way:**
- The dark cheek/temple smudge: face-framing locks now stand off the skin, the loose groom's shadow density is lower, and sideburn roots are thinned.
- A bun that drooped into a ponytail.
- Colour that was too dark or too red.

**LOD chain** (saved, reopened):
- Main groom: LOD0 strands; LOD1 50 % curves at screen 0.45; LOD2 20 % curves at 0.2; LOD3 a helmet mesh (5k tris, from a points-to-volume of the strands) at 0.08.
- Loose groom: hidden at LOD3.
- The groom binding was rebuilt after adding the mesh LOD, which needs binding data.

**Physics:** the loose groom is simulated:
- every strand is a guide;
- bend 0.35, damping 0.12, 5 substeps, 10 iterations;
- gravity preloading 1.

Motion views: board I3.

**Stopping rule applied:** after v13v/v13w the procedural generator stopped producing visible gains. Per the skill's failure-mode rule the remaining groom work goes to a human groom artist (§12).

## 4. Garment method (pattern-based, replaces the offset shell)

`blender_lk_garment_build.py`:

1. **Charts:** a torso tube, arm tubes and a trunk tube per side (full pelvis ring above the crotch, so the CF/CB seams sit on smooth surface). Each chart is expanded by the design ease per height.
2. **Panels:** designed seams, hems, neckline, armhole and crotch curves, sampled once and shared by both panels of every seam.
3. **Pass 1:** mesh in the chart parameter space, placed directly with no inverse. **SLIM** flattening gives the flat pattern (grain aligned). **Pass 2:** isotropic CDT remesh in the flat pattern.
4. **Pattern design edits:**
   - row-width correction to the true 3D arc width (SLIM spreads bust curvature into the lower torso);
   - full-bust adjustment;
   - lived-in length;
   - sleeve bunching reserve;
   - waist gathering;
   - the Henley V cut after flattening, because the open V otherwise acts as a free dart.
5. **ARAP sewn-pattern relaxation:** the welded 3D shell whose triangles are congruent to the flat pattern (pattern/shell edge ratio p1–p99 0.94–1.10). It becomes the cloth rest.
   - **Blender 5.2 ignores `rest_shape_key`** (verified). Every "flat-rest" result before this fix was really the placed shell.
6. **Blender cloth:** gravity, body collision, self-collision. The rib cuffs and elastic band use the shrink vertex group, with the semantics corrected (`shrink_min=0`, `shrink_max=amount`). The placket and binding use a bending-stiffness group. Then a light relax.
7. **Construction details on the settled cloth:** binding, placket bands plus overlap band, buttons, cuffs, hems, band casing, drawstring and eyelets, pocket edges.
8. **UVs = the flat pattern**, packed at one texel density. The pattern outline JSON drives the textures.

**Textiles** (`blender_lk_textile_tex.py`):
- 4K pattern-space BC/N/M for both garments.
- 2K trim strips (20 cm per tile).
- 512 tiled knit/twill detail normals, faded by camera distance in `M_LK_Textile` (Cloth shading, two-sided).
- **Stitches are drawn only along sewn or hemmed pattern edges:** shoulder topstitch; rise, inseam and band topstitches; hem stitches.

**Mesh counts:**

| Garment | LOD0 tris | LOD1 tris | LOD2 tris |
|---|---|---|---|
| Henley | 13,725 | 7,076 | 3,644 |
| Shorts | 8,047 | 4,250 | 2,238 |

## 5. Henley (boards E, G, I1)

- **Silhouette:** relaxed, body-aware, high-hip.
  - The hem lands at the waistband top (CF 102.8 cm, side 100.1, back 99.5); the drawstring shows below it.
  - Long sleeves with rib cuffs.
- **Neckline and placket:**
  - wide scoop (neck point 8.2 cm from CF) with a binding;
  - an open V to about mid-sternum;
  - an interfaced overlapping placket, 2 open buttons plus 3 closed.
- **Dynamic neckline** (I1, same chest-tracking cameras, before vs after correctives):
  - 0° stable;
  - 20° slight V deepening;
  - 30° subtle, 45° noticeable, 60° natural;
  - 90° controlled.
  - Breast poke-through at 20–60° is removed by the correctives.

## 6. Shorts (boards F, G)

Pattern shorts:
- inseam hem at about 69 cm (crotch 76.5 cm);
- side corner at 72 cm with a 2.8 cm rounded slit;
- band top 101.8 cm at CF and 104.1 cm at the side;
- fabric falls from the hip with no inflated side;
- soft seat;
- no crotch arch.

## 7. Deformation and correctives (boards I1, I2)

**Correctives:** 15 garment correctives on LOD0–2. They reuse the revision RBF curve names, which are already driven by the revision body post-process ABP and follow the body through leader pose:
- Henley: `RV_Bend30/60/90`, `RV_Arm090/120/150/180_l/r`;
- shorts: `RV_Hip075/110_l/r`.

They are solved in Blender cloth against the **current** posed soft-tissue body. The skinning-vs-render check is accurate to 0.004 cm.

**Penetration, LOD0** (`eval_g13f_deform.json`; vertices inside the body / max cm):

| Pose | Henley | Shorts |
|---|---|---|
| Neutral | 0 / 0 | 0 / 0 |
| Arms forward | 0 / 0 | 0 / 0 |
| Arm raise 90° | 0 / 0 | 0 / 0 |
| Arm raise 120° | 0 / 0 | 0 / 0 |
| Arm raise 150° | 0 / 0 | 0 / 0 |
| Arm raise 165° | 0 / 0 | 0 / 0 |
| Arm raise 180° | 0 / 0 | 0 / 0 |
| Twist left | 0 / 0 | 0 / 0 |
| Twist right | 0 / 0 | 0 / 0 |
| Back extension | 0 / 0 | 0 / 0 |
| Bend 30° | 0 / 0 | 0 / 0 |
| Bend 45° | 0 / 0 | 0 / 0 |
| Bend 60° | 0 / 0 | 0 / 0 |
| Bend 90° | 2 / 0.12 | 7 / 0.38 |
| Crouch | 8 / 0.35 | 20 / 0.65 |
| Squat | 0 / 0 | 0 / 0 |
| Hip flex | 5 / 3.66 (hem vs thigh) | 3 / 0.20 |
| High knee (left) | 0 / 0 | **89 / 1.45** |
| Stride | 0 / 0 | 0 / 0 |
| Elbow flex | **136 / 2.42** (sleeve into the forearm; no elbow driver exists) | 0 / 0 |

The Henley underarm stretch p99 reaches 4.1× at 180°. The SHCB body correctives are unchanged.

## 8. Gameplay (board H)

The third-person camera shows idle, walk, jog, sprint, jump and crouch, all with a coherent silhouette.

## 9. LOD (boards J1, J2)

**Garment LOD2 root cause, found and fixed:** a garment following the body through leader pose may only use bones that the paired **body LOD actually skins**.
- The body LODs skin 285, 167, 95 and 35 bones.
- The LOD-settings bone-removal list (the revision fix) is not enough. Garment LOD2 twisted around the shoulders even in the bind pose.
- The weights were remapped with `lk_weights_lod_usedbones.py`:
  - LOD1 → the body LOD1 set;
  - LOD2 → the body LOD3 set (the most restrictive of its pair), plus ancestors.
- Lower LODs are also inflated 0.2 / 0.6 cm.

Clean at LOD0, LOD1 and LOD2 in neutral, walk, squat and 180° arm raise. One small upper-back skin show-through remains at LOD2 squat.

**Groom LODs:** configured and verified after reopen. The forced-groom-LOD capture shows no visible switch, so the runtime transition is *not visually demonstrated*.

## 10. Save / reopen, runtime, preservation

- **Save/reopen: PASS** (`reopen_check.json`). The editor was killed and relaunched, then every lookdev asset was loaded from disk with no dirty packages. Confirmed after reopen:
  - garments: 11 and 4 corrective morphs, 3 LODs each, correct material slots;
  - 14 never-stream textures, the master and 6 instances;
  - grooms: LOD chain, helmet LOD, voxelization, material parameters, bindings;
  - skin MIs;
  - the body ABP and all 15 curve metadata entries.
- **Runtime LODSync (PIE): PASS** (`lodsync_check.json`, `Test/BP_LK_LODSyncTest`). The face is forced through LOD 0..7:

  | Face LOD | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
  |---|---|---|---|---|---|---|---|---|
  | Body LOD | 0 | 0 | 1 | 1 | 2 | 2 | 3 | 3 |
  | Garment LOD | 0 | 0 | 1 | 1 | 2 | 2 | 2 | 2 |

  At the natural distance: body 2, garments 2.
- **Preservation: PASS** (`preservation_hashes.json`). These are all hash-identical to the revision baseline:
  - production `MH_MainCharacter`;
  - accepted B2;
  - SHCB HelperFix;
  - the BR v5, Outfit V1 and CharacterFinal candidates;
  - the ShoulderFix skeleton copies.

  The rejected CharacterRevision folder has 0 files modified.

## 11. Art-director review (strict)

Compared against the concept in the same neutral studio:

**Hair.** Brown-first auburn with copper lights is now close to the concept. The low bun sits in the right place and is no longer a clean donut.
- It still reads combed back and scalp-close at the sides.
- The concept's big, messy, voluminous crown and the thick wavy locks framing the whole face are **not** reproduced. The face-framing strands are too thin and wispy and read blond at their tips under the key light.
- It still reads procedural.

**Skin.** Warm and freckled, with face and body in the same family; the underwear contamination is gone.
- The face is rosier and cleaner than the concept's weathered complexion. The face geometry is locked, so any age/weathering has to come from texture work.

**Henley.** The first version that reads as a real garment: pattern cut, soft jersey drape, rib knit, correct placket logic, binding, cuffs.
- It is still too clean and new; there is no washed wear.
- The placket overlay and buttons read slightly applied and oversized.
- The sleeve cap is a little full.
- A dark inner band shows at the back neckline.
- Fold hierarchy is moderate but correct (gravity drape, soft waist folds, sleeve compression).

**Shorts.** The silhouette is now close to the concept: short, light, dolphin hem, side slit, soft seat, no boxiness, no crotch graphic.
- The print reads as camouflage blotches instead of the concept's fine faded leaf print.
- The drawstring renders dark instead of taupe.
- The pockets are faint.

**Whole character.** A coherent home-outfit character, no longer "MetaHuman demo + CG garments". It is not yet a hero-quality art piece.

## 12. Art gates (§53) and technical gates (§54)

| Art gate | Verdict |
|---|---|
| HAIR SILHOUETTE | PARTIAL |
| HAIR REFERENCE MATCH | FAIL (improved; volume and face framing not matched) |
| HAIR COLOUR | PARTIAL (brown-first auburn matched; loose tips read light) |
| HAIR MATERIAL | PARTIAL |
| SKIN COMPLEXION | PARTIAL |
| FACE/BODY SKIN COHERENCE | PASS |
| SKIN MATERIAL | PARTIAL (clean body PASS; weathering and pores limited) |
| HENLEY SILHOUETTE | PARTIAL |
| HENLEY CONSTRUCTION | PARTIAL (correct construction; placket and buttons read applied) |
| HENLEY MATERIAL | PARTIAL (rib knit and heather PASS; no wash or wear; inner neckline band) |
| SHORTS SILHOUETTE | PASS |
| SHORTS CONSTRUCTION | PARTIAL (drawstring colour, faint pockets) |
| SHORTS MATERIAL | PARTIAL (print design wrong) |
| GARMENT DRAPE | PARTIAL |
| CHARACTER MATERIAL COHERENCE | PARTIAL |
| CONCEPT ART-DIRECTION MATCH | PARTIAL |
| HERO CHARACTER QUALITY | FAIL |

| Technical gate | Verdict |
|---|---|
| BODY DEFORMATION | PASS (unchanged accepted body system) |
| DYNAMIC NECKLINE | PARTIAL (continuous, gravity-driven; 20° opens more than "almost no change"; dark V bottom in deep bends) |
| SHCB 90 | PASS |
| SHCB 120 | PASS |
| SHCB 150 | PASS |
| SHCB 165 | PASS |
| SHCB 180 | PASS |
| SHORTS DEFORMATION | PARTIAL (high knee 89 verts / 1.45 cm; crouch 20 / 0.65 cm) |
| HAIR PHYSICS | PARTIAL (simulated and saved; untuned; the sim-settings job crashed the engine twice before it succeeded) |
| HAIR LODS | PARTIAL (configured and saved; visual switch not demonstrated) |
| GARMENT LOD0 | PASS |
| GARMENT LOD1 | PASS |
| GARMENT LOD2 | PASS (minor squat back show-through) |
| SAVE/REOPEN | PASS |
| RUNTIME LODSYNC | PASS |

Technical passes are not evidence of art quality.

## 13. ARTIST-GRADE: **NO** — regions that need a human artist

1. **Hair groom (highest):**
   - volume and crown breakup;
   - thick wavy face-framing locks around the whole face;
   - a messier bun with loop groups.
   - Method: a manual guide groom (Blender hair tools or Houdini) on the provided scalp and bun guides and the concept camera.
2. **Henley surface:**
   - wash and wear painting (collar, cuffs, hem, elbows);
   - softer fold detail at the waist and sleeves;
   - smaller, flatter buttons;
   - a placket sewn into the panel (instead of an overlay);
   - the inner neckline shading.
3. **Shorts textile:** print design (fine faded leaf linework), drawstring colour and cord detail, visible pocket construction.
4. **Skin weathering:** face and body texture paint (sun damage, pores, subtle redness zones) within the locked face geometry.
5. **Elbow corrective:** needs a new elbow driver in the body post-process ABP, which is out of scope for this isolated pass.

**Artist package:** `artist_package/SPH_Lookdev_ArtistPackage_20260930.blend` contains:
- the body collider;
- the garments plus construction details;
- the flat PATTERN objects;
- the groom curves (main and loose) in place;
- the concept reference plane;
- review cameras (front, 3/4, side, head, neckline, shorts).

Source data and tools:
- `garments/g13*`: geometry and pattern JSON, weights, textures;
- `hair/v13w`: Alembic, build env, helmet;
- `Tools/CharacterLookdev_20260930/*`: builders and validation scripts.

## 14. Honest gaps and not done

- Hair reference match not reached; the generator plateaued (§3).
- Elbow-flex sleeve penetration.
- The hip-flex Henley hem contact (5 vertices).
- The shorts high-knee contact.
- The groom LOD visual transition is not demonstrated.
- The hair sim is not tuned.
- The shorts print design, the drawstring colour, and Henley wash/wear are not done.
- No performance profiling this pass (budget: Henley 13.7k and shorts 8k tris at LOD0; strands 38k + 2.4k).
- Nothing promoted. **STOP: waiting for user review.**

## 15. Boards

`boards/`:
- A_concept_vs_final;
- B_hair_match, C_hair_colour;
- D_skin;
- E_henley, F_shorts, G_grazing_material;
- H_gameplay;
- I1_dynamic_neckline, I2_deformation, I3_hair_motion;
- J1_garment_lods, J2_hair_lods.

Iteration history boards are in `boards/_*`.
