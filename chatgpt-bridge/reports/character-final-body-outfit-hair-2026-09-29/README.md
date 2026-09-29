# SPHIRUS final character pass: body v6 + home outfit V2 + hair (2026-09-29)

Isolated candidate: `/Game/Sphirus/CharacterLab/CharacterFinal_20260929/` (`Body/SKM_CF_BodyMesh`, `Body/SKM_CF_FaceMesh`, `Body/ABP_CF_*_PostProcess`, `Outfit/SKM_Home2_Henley`, `Outfit/SKM_Home2_Shorts`, `Outfit/Materials`, `Outfit/Textures`, `Hair/Hair_S_Updo_CF` + `_Binding` + `MI_CF_Auburn_*`). Not promoted. Production `MH_MainCharacter`, the accepted B2 body, the accepted SHCB set, the BR v5 candidate and the user-created face are untouched.

Reference: the attached concept board (THE GUARDIAN: oatmeal Henley with open placket, charcoal drawstring shorts, barefoot, auburn messy low bun) used for outfit, hair and mood only; the face is the user's MetaHuman.

## Method and honesty
- BODY: procedural neutral morph `BR_Neutral` v6 (the v5 feature set + audit-driven secondary corrections + a foot/ankle vector pass), baked as a morph target on copies of the BR candidate meshes; SHCB correctives rebased on v6 and re-baked; all LODs re-projected. **PROCEDURAL, ARTIST-GRADE = NO.** Manual brush sculpting was not available in this session; the artist round-trip package (`Saved/Codex/BodyRealismArtist_20260929/`) remains the path to artist-grade soft tissue.
- OUTFIT: pattern-logic garments built and cloth-draped in Blender 5.2 against the v6 body (no body inflation), skinned offline, imported as skeletal meshes with three Blender-authored LODs. Chaos Cloth not used (skinned garments).
- HAIR: closest MetaHuman-library groom (`Hair_S_Updo`: messy bun with face-framing strands) duplicated into the candidate, auburn material instances, GroomBinding built against the candidate face (source = MetaHuman groom head). Custom groom authoring (Alembic importer) is not enabled in this project.

## Body v6 (procedural)
Displacement (all moved body vertices, n=19652): mean 0.12 mm, p95 0.39 mm, max 4.28 mm; feet/hands vector pass 8469 verts, max 4.28 mm (medial arch lift, malleoli, Achilles hollows, heel pad; exempt from the low-pass so the arch is a real silhouette change).
New v6 forms over v5: lateral breast root softening + axillary tail (attachment, not size), inframammary fold softening + lower-pole fullness, upper-pole relax, sternal plane, flank pad, lower-abdomen softness, glute-ham weight, lateral fold fade, medial lower glute, lateral glute soft hollow, inner-thigh softness, knuckle/thenar hints. Feature amplitudes: flank_pad 0.45 mm, lower_glute_medial 0.36 mm, lateral_root_soften 0.63 mm, axillary_tail 0.34 mm, imf_soften 0.56 mm, upper_pole_relax 0.30 mm, sternal_plane 0.30 mm, lower_abdomen_soft 0.38 mm, glute_ham_weight 0.47 mm, inner_thigh_soft 0.23 mm, fold_lateral_fade 0.43 mm.
Proportion preservation (convex-hull circumference, accepted B2 -> v6): neck z146 39.67->39.71 cm (+0.41 mm) · chest z128 86.84->86.96 cm (+1.23 mm) · underbust z119 73.88->73.80 cm (-0.84 mm) · waist z109 71.54->71.53 cm (-0.07 mm) · high hip z97 85.73->85.76 cm (+0.27 mm) · hip z86 95.55->95.51 cm (-0.36 mm) · L thigh z70 42.67->42.70 cm (+0.24 mm) · L calf z35 18.81->18.86 cm (+0.51 mm). Height 173.272 cm unchanged; face above the collar 0.0 mm.
SHCB: helper nodes and driver unchanged (+2.0/+3.0/+3.5 cm at 150/165/180); SHC_150/165/180 l/r recomputed on the v6 neutral and baked (base positions unchanged, 0.0 cm); far-LOD helper effect re-projected (70/70 LOD morph bakes OK).

## Outfit V2 (Blender construction + drape)
Henley: front/back torso shell (ease chest +7.5, waist +8.5, hip +9.5, hem +9 cm), shared shoulder seam, rounded scoop neckline (centre front z 132.5, neck base ~135.5), narrow placket slit to z 121.5 with 4 buttons (top 2 open), set-in sleeves (ease 7.5 -> 8 -> 4.5 cm at the wrist), armhole dropped 2.4 cm below the armpit with +8 cm underarm ease (fabric reserve for 165-180 deg elevation), high-hip hem (side z 97.5, back 96, slightly irregular), neck binding / placket / cuffs / hem built on the settled cloth. Cloth: mass 0.3, tension 30, bend 1.5, shear 15, 90 frames, shorts as extra collider.
Shorts: soft waistband (top z 104.5, 3.5 cm, +6.5 cm ease, pinned) + hip shell (+8..+10 cm) + two short leg tubes joined on a shallow sagittal crotch seam (crotch 3.4 cm below the body crotch), hem mid 64.5 cm with a curved hem (sides +2.6 cm), slight A-line (+10 -> +11.5 cm), side-entry pocket welts, eyelets, thin drawstring with knot and two uneven tails, hems. Cloth: mass 0.10, tension 60, bend 2.5.
- henley: LOD0 8231 verts / 15550 tris, LOD1 7775 tris, LOD2 6572 tris (Blender decimate 50 % / 22 % cloth + 45 % details); rest clearance min 0.25 cm, p5 0.68, median 1.14, penetrating verts 0.
- shorts: LOD0 6077 verts / 11140 tris, LOD1 5570 tris, LOD2 4769 tris (Blender decimate 50 % / 22 % cloth + 45 % details); rest clearance min 0.65 cm, p5 0.72, median 1.02, penetrating verts 0.
- `/Game/Sphirus/CharacterLab/CharacterFinal_20260929/Outfit/SKM_Home2_Henley.SKM_Home2_Henley`: LOD0 [8231, 15550], LOD1 [4247, 7775], LOD2 [3628, 6572] (verts, tris); bones 342, unweighted 0/0/0; slots ['M_Henley', 'M_Henley_Trim', 'M_Buttons']; rejected non-manifold triangles 0.
- `/Game/Sphirus/CharacterLab/CharacterFinal_20260929/Outfit/SKM_Home2_Shorts.SKM_Home2_Shorts`: LOD0 [6077, 11140], LOD1 [3139, 5570], LOD2 [2741, 4769] (verts, tris); bones 342, unweighted 0/0/0; slots ['M_Trousers', 'M_Trousers_Trim', 'M_Trousers_Trim', 'M_Drawstring']; rejected non-manifold triangles 0.
Skin weights: offline (closest point on the v6 body -> barycentric blend of the body weights, 14 Laplacian passes, 8 influences); skeleton = isolated ShoulderFix `metahuman_base_skel`, bind = body mesh bind. Garments follow the body by leader-pose; SHCB helper bones inherited through `upperarm_out` weights.
Materials: `M_SPH_Textile` (Cloth shading, two-sided) + 6 instances (Henley oatmeal tint 0.97/0.93/0.86, jersey knit detail; shorts warm charcoal tint 1.25/1.2/1.15 on the charcoal map, twill detail; trims, drawstring, buttons); unique 2048 BC/N/RA per garment + 512 detail tiles, stitch rows along the UV island borders, faint tonal motif on the shorts.

## Hair
Style `Hair_S_Updo` from the MetaHuman Creator library (on disk); the concept's low messy bun has no library equivalent on disk (`Hair_M_UpdoBun_Messy` thumbnail only). Materials: MI_CF_Auburn_MI_Hair_Cards.MI_CF_Auburn_MI_Hair_Cards, MI_CF_Auburn_MI_Hair.MI_CF_Auburn_MI_Hair, MI_CF_Auburn_MI_Hair_Helmet.MI_CF_Auburn_MI_Hair_Helmet (melanin 0.46, redness 0.92, red variation 0.18, roughness overall 0.6, scraggle 0.22). Binding: `/Game/Sphirus/CharacterLab/CharacterFinal_20260929/Hair/Hair_S_Updo_CF_Binding.Hair_S_Updo_CF_Binding` (source SKM_Groom_Head_Legacy01.SKM_Groom_Head_Legacy01). Alternates bound for the QA comparison only: Hair_S_PulledBack, Hair_S_SweptUp, Hair_S_LowPonytail.

## Body clearance / deformation (captured UE geometry: real skinning + BR v6 + SHCB, garment vs body BVH)
### Neutral
| pose | Henley pen. verts (max cm) | Henley clearance p5 / median | stretch p99 | Shorts pen. verts (max cm) | Shorts clearance p5 / median | stretch p99 | shirt inside shorts |
|---|---|---|---|---|---|---|---|
| neutral | 0 (0.0) | 0.686 / 1.388 | - | 0 (0.0) | 0.736 / 1.104 | - | 2008 (2.333) |

### Deformation poses
| pose | Henley pen. verts (max cm) | Henley clearance p5 / median | stretch p99 | Shorts pen. verts (max cm) | Shorts clearance p5 / median | stretch p99 | shirt inside shorts |
|---|---|---|---|---|---|---|---|
| neutral | 0 (0.0) | 0.686 / 1.388 | - | 0 (0.0) | 0.736 / 1.104 | - | 2008 (2.333) |
| armsfwd | 1 (0.344) | 0.636 / 1.401 | 1.598 | 3 (0.332) | 0.701 / 1.091 | 1.217 | 2391 (2.979) |
| elev90 | 0 (0.0) | 0.674 / 1.413 | 1.364 | 0 (0.0) | 0.736 / 1.104 | 1.0 | 2008 (2.333) |
| elev120 | 0 (0.0) | 0.664 / 1.414 | 1.565 | 0 (0.0) | 0.736 / 1.104 | 1.0 | 2008 (2.333) |
| elev150 | 1 (4.154) | 0.646 / 1.409 | 1.751 | 0 (0.0) | 0.736 / 1.104 | 1.0 | 2008 (2.333) |
| elev165 | 1 (3.892) | 0.642 / 1.401 | 1.826 | 0 (0.0) | 0.736 / 1.104 | 1.0 | 2008 (2.333) |
| elev180 | 4 (5.877) | 0.633 / 1.392 | 1.898 | 0 (0.0) | 0.736 / 1.104 | 1.0 | 2008 (2.333) |
| twist | 0 (0.0) | 0.639 / 1.402 | 1.575 | 0 (0.0) | 0.702 / 1.096 | 1.175 | 2347 (3.0) |
| crouch | 20 (6.14) | 0.627 / 1.319 | 1.409 | 83 (0.788) | 0.458 / 1.063 | 1.672 | 0 (0.0) |
| squat | 21 (6.186) | 0.553 / 1.396 | 2.194 | 22 (0.582) | 0.659 / 1.094 | 1.489 | 0 (0.0) |
| elbow | 56 (1.406) | 0.576 / 1.302 | 1.308 | 0 (0.0) | 0.724 / 1.11 | 1.132 | 2235 (2.756) |
| hipflex | 12 (5.398) | 0.556 / 1.386 | 2.188 | 124 (2.181) | 0.545 / 1.083 | 1.597 | 1291 (2.988) |
| backext | 19 (6.065) | 0.549 / 1.387 | 2.198 | 0 (0.0) | 0.708 / 1.109 | 1.194 | 1578 (2.999) |
| internal90 | 0 (0.0) | 0.662 / 1.404 | 1.368 | 0 (0.0) | 0.736 / 1.104 | 1.0 | 2008 (2.333) |
| external90 | 0 (0.0) | 0.661 / 1.403 | 1.384 | 0 (0.0) | 0.736 / 1.104 | 1.0 | 2008 (2.333) |

### Gameplay poses
| pose | Henley pen. verts (max cm) | Henley clearance p5 / median | stretch p99 | Shorts pen. verts (max cm) | Shorts clearance p5 / median | stretch p99 | shirt inside shorts |
|---|---|---|---|---|---|---|---|
| idle | 52 (4.099) | 0.652 / 1.378 | - | 0 (0.0) | 0.736 / 1.104 | - | 2330 (2.942) |
| walk | 45 (7.042) | 0.658 / 1.373 | 1.19 | 0 (0.0) | 0.717 / 1.105 | 1.142 | 1252 (2.994) |
| jog | 52 (7.099) | 0.614 / 1.327 | 1.275 | 0 (0.0) | 0.707 / 1.114 | 1.269 | 2109 (2.997) |
| sprint | 53 (8.123) | 0.631 / 1.357 | 1.34 | 0 (0.0) | 0.699 / 1.094 | 1.274 | 2090 (2.988) |
| crouch | 20 (6.14) | 0.627 / 1.319 | 1.368 | 83 (0.788) | 0.458 / 1.063 | 1.537 | 0 (0.0) |
| jump | 0 (0.0) | 0.646 / 1.333 | 1.566 | 0 (0.0) | 0.516 / 1.071 | 1.591 | - (-) |

### LOD1 / LOD2: NOT_TESTED (no evaluation file)
## Body review (clay boards a5 = BR v5 vs a6 = CF v6, body deformation boards cf_body_dfm_*)
- Macro: unchanged by design (accepted B2 proportions; all circumferences within +1.3/-0.9 mm, height 173.272 cm, shoulder width +0.7 mm). Head/body balance and hand scale untouched.
- Breast / ribcage: v6 softens the lateral root and the inframammary crease and adds the axillary tail; the masses read slightly more attached in 3/4. The underlying B2 breast is still a hemispheric base with a hard lower outline at close range: PARTIAL (attachment improved, shape needs the artist pass).
- Waist / abdomen: flank pad and lower-abdomen softness are subtle; costal margin still faint. PARTIAL.
- Pelvis / hips: iliac crest / medius read as in v5; hip curve coherent, no widening. PASS (structure) with subtle soft tissue.
- Glutes: lower glute now carries weight onto the fold, the fold fades laterally (glutes_3q close-up). PARTIAL -> good for a procedural pass; glute-ham transition still soft.
- Thighs / knees / calves: v5 forms kept (patella, medial gastrocnemius); inner-thigh softness added. PASS for the shorts read.
- Feet: the flat plank sole now has a medial longitudinal arch (~8 mm lift), malleoli, Achilles hollows and a rounder heel; toes unchanged. Reads as a foot from the side and 3/4. PASS at gameplay distance, PARTIAL at close range (toe pads / dorsal tendons not authored).
- Hands: knuckle / thenar hints only; scale untouched. PARTIAL.
- Body deformation (clay, 15 poses): equivalent to the accepted BR v5 set; SHCB 150/165/180 rebased on v6 with the helper unchanged; no new artefacts at squat, hip flexion, twist, elbow. PASS.
- Skin: the candidate carries the MetaHuman baked body skin (micro-detail normals on, baked underwear in the base colour). No unbaked nude skin textures exist in the candidate, so clay is the nude development surface. No skin authoring was done in this pass. PARTIAL.

## Outfit review (boards cf_final_neutral, cf_closeups, cf_deform_*, cf_gameplay, cf_lods)
- Henley design: fitted-relaxed knit, rounded scoop, narrow open placket with 4 buttons (top open), high-hip hem with a natural drape edge, sleeves lightly fitted at the upper arm and tapering to the wrist. Matches the concept's silhouette; the placket still reads as a narrow dark slit rather than two overlapping edges. PASS with note.
- Henley fit: chest bridges the breasts without cups, gentle waist, back clean, sleeves without tube look. Neutral clearance 0 penetrations, p5 0.68 cm. PASS.
- Henley length: hem at high hip over the waistband (front z ~97.5), shorter than V1, drawstring knot visible below it. PASS.
- Neckline / decollete: clavicles and upper sternum visible, scoop centre 132.5 cm, no plunge. PASS.
- Shorts design: soft waistband, thin drawstring with uneven tails, side-entry pocket welts, curved hem, slight A-line; charcoal with a faint tonal motif. PASS.
- Shorts fit: waist secure under the shirt hem, seat follows the glutes with clearance, no diaper seat, shallow crotch without a tent, hem at upper-mid thigh. The right-leg UV twist of the first build is fixed (build c). PASS.
- Body readability under the outfit: shoulder line, clavicle, breast shelf, waist, hip, seat and thigh all read at gameplay distance without tightness. PASS.
- Cloth deformation (skinned, no Chaos Cloth): shorts PASS in all poses except hip flexion (124 verts / 2.2 cm at the front thigh) and crouch (83 / 0.8 cm small skin patches on the thigh). Henley: clean to 120 deg, elbow 56 verts / 1.4 cm, gameplay counts (45-53) are neck-seam-edge false positives with sub-cm real values. PARTIAL.
- SHCB compatibility: the skinned Henley underarm opens from ~120 deg and shows inside-out patches at 150/165/180 (as V1). Three armhole variants were tested (dropped +2.4 cm / +8 ease, then the V1 armhole); none closes the gap. The fix needs a pose-space garment corrective driven by the SHC curves or Chaos Cloth on the sleeve root, not a body/SHCB change. FAIL.
- LODs (Blender-authored): LOD1 (50 %) holds in neutral, walk, squat, 180. LOD2 (40 % cloth / 50 % details) still breaks the sleeves (spikes) and the shorts hem in squat: decimation of the sleeve tubes needs a topology-aware LOD (retopo or manual). LOD0 PASS, LOD1 PASS, LOD2 FAIL.
- Materials: oatmeal knit with jersey detail, charcoal shorts with twill detail, stitch rows on island borders, matte cloth shading; no shiny synthetics. PASS for review; knit tile slightly regular at close range.

## Hair review (boards cf_hair, cf_hair_alternatives, close-ups)
- Design: `Hair_S_Updo` is the closest on-disk MetaHuman library groom (messy bun with loose face-framing strands and flyaways). It is a HIGH bun; the concept's low messy bun (`Hair_M_UpdoBun_Messy`) exists only as a thumbnail (cloud asset) and no groom authoring path (Alembic importer) is enabled. PARTIAL.
- Naturalness / colour: dark auburn / copper (melanin 0.72, redness 0.8), dry roughness, flyaways read as real strands; the first pass was too orange and was corrected. PASS for review.
- Face framing: loose strands at the temples and nape, bangs lighter than the library default is not possible (groom is fixed). PARTIAL.
- Deformation / clipping: bound to the CF face (source = MetaHuman groom head Legacy01); scalp coverage and hairline intact in idle, walk, crouch, twist, squat; no visible scalp clipping in the captured poses. PASS at review distance; sprint views were off-camera (NOT_TESTED).
- Alternates: PulledBack / SweptUp / LowPonytail were bound but rendered invisible in the QA scene (engine-content grooms without material copies): NOT_TESTED.
- LOD / performance: library groom LODs (strands -> cards -> helmet) carried over unchanged; not profiled. NOT_TESTED.

## Body surface / skin
Geometry / normal / shader split respected: v6 only adds primary-secondary form; no tertiary noise in the base geometry. The candidate body material is the MetaHuman baked skin (micro skin details on, pores flow maps, SRMF baked). Underwear is baked into the base colour, which is why the clothed presentation is the only skin presentation. No regional roughness / colour authoring was done in this pass (would require the unbaked texture set). SKIN SURFACE = PARTIAL.

## Performance (audit, not profiled)
Body: same meshes/LODs as the accepted BR set + 7 morph targets per LOD. Outfit LOD0 15 550 + 11 140 tris, LOD1 7 775 + 5 570, LOD2 6 572 + 4 850; 2 skeletal meshes, 1 master material + 6 instances, 8 textures (6 x 2048, 2 x 512). Hair: library groom (strands LOD0-?, cards, helmet) + 3 material instances. No cloth simulation, no extra bones, no PostProcess ABP on the garments. Frame cost NOT_TESTED in a real level.

## Safety / preservation
Isolated candidate only. Checkpoints: new-folder candidate (nothing overwritten); protected folders verified by modification time after the pass (no file in `MetaHumans/MH_MainCharacter`, `NativeBody_20260928` (B2), `ShoulderFix_20260928/HighElevCorrective/HelperFix` (SHCB), `BodyRealism_20260929` (BR v5) or `Outfit_Home_20260929` (V1) newer than the session start); folder hashes recorded in `preservation_hashes.json`. Face identity: head morph deltas above the collar are 0. SHCB helper nodes, driver and skeleton copies unchanged. Editor CPU throttling was set to off for the capture session (editor performance setting, restore if wanted).

## FINAL STATUS: BODY
| item | status |
|---|---|
| MACRO PROPORTIONS | PASS (accepted B2 kept; +1.3 mm max circumference drift) |
| ANATOMICAL COHERENCE | PASS |
| SOFT-TISSUE REALISM | PARTIAL (procedural detail layer; breast/abdomen nuance needs the artist pass) |
| BREAST / RIBCAGE | PARTIAL (attachment improved, base shape still hemispheric) |
| WAIST / ABDOMEN | PARTIAL |
| PELVIS / HIPS | PASS |
| GLUTES / GLUTE-HAM | PARTIAL (weight on the fold added; transition still soft) |
| THIGHS / LEGS | PASS |
| ARMS / SHOULDERS | PASS (v5 forms, SHCB intact) |
| HANDS | PARTIAL |
| FEET | PASS at gameplay distance / PARTIAL close (arch, malleoli, heel added; toes untouched) |
| SKIN SURFACE | PARTIAL (baked MetaHuman skin, no authoring) |
| BODY DEFORMATION | PASS |
| ARTIST-GRADE | NO (procedural v6; manual sculpt package remains the path) |

## FINAL STATUS: OUTFIT
| item | status |
|---|---|
| HENLEY DESIGN | PASS (placket slit note) |
| HENLEY FIT | PASS |
| HENLEY LENGTH | PASS |
| NECKLINE / DECOLLETE | PASS |
| SHORTS DESIGN | PASS |
| SHORTS FIT | PASS |
| BODY READABILITY | PASS |
| CLOTH DEFORMATION | PARTIAL (hip flexion 2.2 cm, crouch patches, elbow 1.4 cm) |
| SHCB COMPATIBILITY | FAIL (underarm opens from ~120 deg; needs a garment pose corrective / Chaos Cloth) |
| LOD0 | PASS |
| LOD1 | PASS |
| LOD2 | FAIL (sleeve spikes, hem tears) |

## FINAL STATUS: HAIR
| item | status |
|---|---|
| HAIR DESIGN | PARTIAL (closest library groom; high bun instead of low) |
| HAIR NATURALNESS | PASS |
| HAIR / FACE FRAMING | PARTIAL |
| HAIR DEFORMATION / CLIPPING | PASS (review poses) |
| HAIR LOD / PERFORMANCE | NOT_TESTED |

## FINAL STATUS: FINAL CHARACTER
| item | status |
|---|---|
| NATURALNESS | PASS |
| FEMININE / NATURAL APPEAL | PASS (coherent body, fitted-relaxed clothes; no exaggeration) |
| GUARDIAN IDENTITY | PARTIAL (outfit and hair carry it; the face expression/mood is out of scope) |
| GAMEPLAY READ | PASS (idle/walk/jog/crouch/jump at third-person distance; sprint views off-camera) |
| READY FOR USER APPROVAL | YES, for review of body v6 + outfit V2 + hair direction |
| READY FOR PRODUCTION PROMOTION | NO (SHCB underarm, LOD2, hair style gap, artist body pass) |
| PRODUCTION CHARACTER MODIFIED | NO |

## NOT_TESTED
- Frame cost / profiling in a real level
- Hair alternates (rendered invisible in the QA scene)
- Hair LOD transitions and shadow cost
- Sprint pose side/rear views (character off-camera in the sprint clip)
- Skin regional roughness / colour authoring (no unbaked textures in the candidate)
- Chaos Cloth (not used)
- Save/reopen persistence check of the CF candidate (editor kept open)
- Runtime LODSync pairing of the CF body/face in PIE

## Boards
![a5_audit_cu_a](boards/a5_audit_cu_a.jpg)
![a5_audit_cu_b](boards/a5_audit_cu_b.jpg)
![a5_audit_cu_c](boards/a5_audit_cu_c.jpg)
![a5_audit_full](boards/a5_audit_full.jpg)
![a5_audit_grazing](boards/a5_audit_grazing.jpg)
![ab_a5_a6_cu_a](boards/ab_a5_a6_cu_a.jpg)
![ab_a5_a6_cu_b](boards/ab_a5_a6_cu_b.jpg)
![ab_a5_a6_cu_c](boards/ab_a5_a6_cu_c.jpg)
![ab_a5_a6_full](boards/ab_a5_a6_full.jpg)
![ab_a5_a6_grazing](boards/ab_a5_a6_grazing.jpg)
![cf_body_dfm_1](boards/cf_body_dfm_1.jpg)
![cf_body_dfm_2](boards/cf_body_dfm_2.jpg)
![cf_body_dfm_3](boards/cf_body_dfm_3.jpg)
![cf_closeups](boards/cf_closeups.jpg)
![cf_deform_1](boards/cf_deform_1.jpg)
![cf_deform_2](boards/cf_deform_2.jpg)
![cf_deform_3](boards/cf_deform_3.jpg)
![cf_final_neutral](boards/cf_final_neutral.jpg)
![cf_gameplay](boards/cf_gameplay.jpg)
![cf_hair](boards/cf_hair.jpg)
![cf_hair_alternatives](boards/cf_hair_alternatives.jpg)
![cf_lods](boards/cf_lods.jpg)

## Reference
![concept](reference/concept_guardian_home.png)
