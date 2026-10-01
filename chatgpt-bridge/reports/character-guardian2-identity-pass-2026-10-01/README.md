# SPHIRUS protagonist — GUARDIAN-2 face identity pass (2026-10-01)

**Isolated CharacterLab candidate. NOT promoted. STOP FOR USER REVIEW.**

| | |
|---|---|
| Continues from | `dcb061c` (report `chatgpt-bridge/reports/character-guardian-face-pass-2026-10-01`); starting point was candidate H |
| New assets | `/Game/Sphirus/CharacterLab/CharacterGuardian2_20261001/` (94 new `.uasset`; nothing outside this folder written) |
| Identity authority | Tier A: original close 3/4 and front face photo, original full-body front/3/4 |
| Modelling aid | Tier B: the turnaround and face-study sheets (profile, opposite 3/4, skull, jaw, neck). Where Tier B contradicted Tier A, Tier A was used. |

## Answer first

Side by side and unlabeled, would an art director say this is the same woman? **No.**

The new candidate P is measurably and visibly closer than H:
- lower, straighter brows close to the eye;
- more open fissure (aperture 0.87 → 0.96 of the reference);
- mouth corners slightly down (corner drop 0.039 in the reference; −0.009 → 0.028 here);
- mouth no longer offset to the wrong side;
- longer lower face (menton 0.96 → 0.99);
- narrower alae; lateral zygoma 3% narrower;
- warmer-neutral cheeks instead of the baked rosy patch; muted lips.

It still reads as a related, different woman. Remaining gaps:
- the eye region reads heavier and more shadowed;
- the lateral brow ends droop, so the face reads sad rather than calm-serious;
- the lower face is broad and soft;
- the skin is smooth and orange next to the photo's textured olive-beige.

Close metrics are a guide, not proof. **OVERALL FACE GATE: FAIL.**

## Final candidate composition (NEW = P)

| Part | Asset | Status |
|---|---|---|
| Face | `Face/SKM_GD_FaceMesh_p`. MetaHumanCharacter fit `MHC/MHC_GD2_P` → per-LOD BR_Neutral deploy. Same DNA / RigLogic / 865 morphs / 8 LODs. | new |
| Face skin | `Skin/MI_LK_Face_*_VT_g2c17`: children of the GUARDIAN c14s MIs, so the seam shading and tint carry over; only the base colour is swapped. | new |
| Base colour texture | `Skin/Textures/T_LK_Head_BC_c17`. Base is c14, then: (1) the baked rosy/mauve cheek patch is pulled toward the surrounding skin, low frequency only; (2) light natural freckles on the nose/upper cheeks; (3) lips muted toward brown-rose. No wrinkles, bags or hollows. | new |
| Brows / lashes | `GR_GD_Eyebrows_M_SlightArch` / `GR_GD_Eyelashes_S_Thin`. Unchanged GUARDIAN grooms, newly bound: `Face/Bindings/GB_GD_*_p` (template-head source mesh). | grooms reused |
| Hair | `Hair/GR_LK_Hair_{Main,Loose}_id20` + `MI_GD_Hair*_id20`. Helmet, 4 LODs, DEFAULT LOD mode, bindings `GB_GD_Hair*_p`. | new |
| Reference expression | `Face/Diagnostics/AS_GD2_RefExpression`. QA pose only, **not baked into the neutral**. | new |
| Henley | GUARDIAN `Outfit/SKM_LK_Henley_g17e`, unchanged. Secondary; no art pass this time. | reused |
| Shorts | `CharacterCorrective_20261001/Cloth/CA_CR_Shorts_m1` (runtime Chaos), unchanged. Shorts kept; no switch to the reference's long pants. | reused |
| Body | GUARDIAN `Skin/MI_GD_Body_t1`, unchanged. | reused |

Intermediate candidates kept for comparison (isolated, revertible):
- faces `SKM_GD_FaceMesh_{i,l2,m,n,o}`;
- skins `g2c15` / `g2c16`;
- hair `id19`.

## Method

1. **Tier B used where it is useful: profile and skull.** New tools:
   - `blender_gd_sheet.py` renders the bald clay orthographically in the turnaround frames. Front, both profiles and back share one fitted scale (brow→menton on the right profile).
   - `blender_gd_profile.py` extracts the photo's anterior profile line and reports per-region differences in cm.
   - Fixing an interpolation bug in the first version of the profile tool changed its readings: the nose was *not* under-projected relative to Tier B.
2. **Judged in UE real renders, not Blender workbench clay.**
   - The workbench clay made H read gaunt (hard cavity shading). PASS A cheek fill was based on it, and the UE render showed it as a puffy lower face. That fill was rolled back in O (`boards/supporting/S2_WORKBENCH_CLAY_TRAP.jpg`).
   - Every candidate went through the full UE cycle and real-skin captures from the Tier A cameras: front recon camera and the re-solved ~33° 3/4 camera. The old 47° camera was not used.
3. **MetaHuman tracker on the renders** (guide only). It revealed that, in vertical units (eye→stomion), the face is ~5–7% too wide across the eyes and mouth. The interocular distance is fixed by the DNA eye joints, so it cannot change in a BR_Neutral pass. P compensates by:
   - lengthening the lower face (+1.8 mm lips, +3.2 mm chin);
   - narrowing the zygomatic arch by 3%;
   - widening and opening the fissure.
4. **Natural asymmetry:** only per-side differences measured on the Tier A photo were applied.
   - Mouth shifted ~1.2 mm toward the character's right (reference −0.016 IPD, H was +0.018, P −0.001).
   - Extra left mouth-corner drop.
   - Left fissure slightly wider.
   - Nothing was symmetrised.

### Iterations (all isolated; `boards/supporting/S1_ITERATION_PROGRESSION_*.png`)

| Step | Change | Verdict |
|---|---|---|
| I (PASS A) | Forehead slope back; lower, more horizontal jaw border (gonial angle −6 mm); temple fill; zygomatic arch +2 mm; submalar / buccal fill; nasolabial soften | Jaw border and forehead **kept**. Cheek fill **rejected later** (puffy in UE). |
| L2 (PASS B + asymmetry) | Bridge / radix widened; corners down; philtrum columns; chin broadened; brow-ridge soften; lids opened; mouth shift; lateral canthi out | Kept, except the alar widening. |
| M | Alar base narrowed (the reference alae are narrower than H; L2 went the wrong way); tip de-bulbed; skin c15 | Kept. |
| N | Brow mass lowered ~4 mm (H brows sat ~0.7 cm too high above the eye relative to Tier A); lateral hood | Kept. **Side effect:** the lateral brow ends now droop. |
| O | Submalar/buccal fill rolled back; central upper-lid fold lifted; lower lip reduced; skin c16, hair id19 | Kept. c16 lips read grey-mauve → c17. id19 **rejected**. |
| P (NEW) | Lower face +2–3 mm; zygoma −3%; mouth −5% (width); lateral canthi out; upper lid +0.5 mm | **Final.** |

Rejected:
- the PASS A cheek fill (I);
- alar widening (L2);
- hair id19 (lumpy, tall crown; `S3_HAIR_ITERATIONS.jpg`);
- the c16 lip tone.

## Measurements

Front tracker metrics on UE real renders, normalised by inter-pupillary distance (IPD). Full set in `evidence/face_metrics.txt`.

| Metric | Reference | OLD H | NEW P |
|---|---|---|---|
| eye width | 0.460 | 0.432 (0.94) | 0.435 (0.95) |
| eye aperture | 0.157 | 0.137 (0.87) | 0.152 (0.96) |
| aperture L / R | 0.166 / 0.152 | 0.140 / 0.135 | 0.152 / 0.152 |
| eye → stomion | 1.119 | 1.072 (0.96) | 1.090 (0.97) |
| menton below eyes (geometry) | 1.883 | 0.960 | 0.986 |
| mouth width | 0.844 | 1.04 | 1.03 |
| corner drop L / R | 0.037 / 0.039 | −0.004 / −0.010 | 0.024 / 0.034 |
| mouth centre offset | −0.016 | +0.018 | −0.001 |
| upper cheek width (zygomatic level) | 2.088 | 1.069 | 1.043 |

Tier B profile (aid, cm, + = candidate more anterior), NEW P:

| Region | Value | Note |
|---|---|---|
| forehead | −0.40 | |
| nasion | +0.26 | |
| dorsum | +0.82 | Tier A 3/4 does not support reducing it; not changed |
| tip | +0.07 | |
| upper lip | −0.28 | |
| lips | −0.02 | |
| chin | +0.38 | |

## Gates by area

| Area | Result | Detail |
|---|---|---|
| Cranium | **PARTIAL** | The bald vault sits 1.5–2 cm under the Tier B hair envelope, which fits the hair volume. So it is not too tall; it was not lowered. Forehead sloped back, jaw border lowered and made more horizontal (board 03). From the front the bald dome still reads narrow-topped. |
| Eyes / orbits / expression | **PARTIAL** | Fissure more open (0.96), brows lower and straighter, central lid fold lifted, lateral hood kept. Under the studio key the orbit still reads heavier and more shadowed than the photo. The lowered lateral brows tip the neutral toward "sad". REFERENCE_EXPRESSION exists as a separate QA pose (board 12): corner depress, lip press, inner squint, slightly heavy lids, faint brow down. |
| Nose | **PARTIAL** | Bridge and radix wider, alae narrower, tip less bulbous. Length unchanged (it was already right). |
| Midface | **PARTIAL** | Zygomatic level 1.07 → 1.04 of the reference (still wide). The lower cheek remains narrower than the Tier A picks; those picks are partly on hair (known from GUARDIAN D/E). |
| Mouth / jaw / chin | **PARTIAL** | Corners down, asymmetric like the reference; lower lip less full; lower face longer; jaw border more horizontal. Lower face still broad and soft. |
| Skin | **PARTIAL** | Rosy cheek patch removed, freckles added, lips muted, no wrinkles. Still smoother and more orange than the photo. |
| Hair | **PARTIAL** | id20 vs id18: browner, darker auburn with no ombre/highlights on the loose groom; more temporal mass; looser, larger bun; more nape escapes. Still a dense cap with a hard hairline. A few loose strand tips still catch light. |
| Head / neck / body | **PARTIAL** | Head scale and neck read plausible against the Tier A full body (board 14). Shorts kept. Seam unchanged from GUARDIAN. |
| Henley | **NOT DONE** | Secondary per the brief; the time went to the face. g17e unchanged. Hem / sleeve bunching, the deep neckline and the mechanical opening are still open. |

## Technical

| Item | Result | Evidence |
|---|---|---|
| RigLogic | **PASS** | 23 cases on P (blink closure, lip seal, MBP, teeth behind lips on jaw open, visemes, extreme), also after restart (boards 16 / 17). Same DNA; eyes, teeth and joints untouched by BR_Neutral. |
| LOD | **PASS** | Face LOD0–3 and garment LODs (board 16); 8 face LODs, all with BR_Neutral (`evidence/reopen_check.json`). |
| Grooms | **PASS** | 4 bindings on P load and render; id20 in DEFAULT LOD mode with 4 LODs. |
| Chaos shorts / garment correctives | **PASS** | Henley, shorts, waist, neck, sleeve, full, seam and LOD sets re-run on P (`zg_*`). |
| Save / restart / reopen | **PASS** | Fresh editor; 0 dirty packages before and after reopen; all assets load from disk; after-restart captures on board 17. |
| Preservation | **PASS** | 12 protected groups byte-identical to the pass checkpoint, including production `MH_MainCharacter` and the GUARDIAN dcb061c candidate (`evidence/preservation_check.json`). The QA studio save folder was redirected to the Guardian-2 folder before the first scene setup. |

## BR_Neutral plateau evidence

- **The local fit is not what limits large forms.** The MetaHumanCharacter fit reproduces the authored targets to 0.5–0.9 mm mean (cranium ~1.5 mm) in every region, for H and for P. The P ops moved the surface up to 6 mm.
- **Hard limit: eye and joint placement are fixed by the DNA.** BR_Neutral cannot move the eyeballs, so interocular distance and eye height stay as they are. The tracker suggests the reference's eyes sit relatively closer together for her face width; that cannot be fixed in this route.
- **Next route:** re-fit a neutral and run the MetaHuman auto-rig as a separate candidate. `request_auto_rigging` is an Epic cloud service, so **it was not run**. It needs your approval.

## Boards (`boards/`)

01_BALD_CLAY_FRONT, 02_BALD_CLAY_3Q, 03_BALD_CLAY_PROFILES, 04_ORIGINAL_OVERLAY_FRONT, 05_ORIGINAL_OVERLAY_3Q, 06_EYES_ORBITS, 07_NOSE, 08_MIDFACE_CHEEKS, 09_MOUTH_JAW_CHIN, 10_REAL_SKIN_FRONT, 11_REAL_SKIN_3Q, 12_REFERENCE_EXPRESSION, 13_HAIR_REFERENCE, 14_HEAD_NECK_BODY, 15_FULL_CHARACTER, 16_RIG_EXPRESSION_CHECK, 17_AFTER_RESTART.

- Face boards show REFERENCE | OLD H | NEW from the same cameras.
- Supporting: `S1` iteration progression, `S2` workbench-clay trap, `S3` hair iterations.

## Open gaps / next steps

1. **Neutral mood:** raise the lateral brow tails 1–1.5 mm and soften the lateral hood so the neutral reads calm-serious, not sad.
2. **Eye region:** re-check the orbit under softer frontal light. If the heavy read is form rather than lighting, reduce the central preseptal fullness further.
3. **Lower face:** reduce the broad, soft lower face with a jawline / jowl refinement (no inflation).
4. **Interocular distance:** only changeable via auto-rig / re-fit neutral (needs your approval).
5. **Skin:** micro-detail (pores, roughness breakup) and a less orange base, without wrinkles.
6. **Hair:** break up the hard hairline cap (sparser front-edge density, see-through strands); fix the light-catching loose tips.
7. **Henley:** neckline depth / opening and hem / sleeve bunching (not done).

## Final gates

| Gate | Result |
|---|---|
| IDENTITY FRONT | **FAIL** |
| IDENTITY 3/4 | **FAIL** |
| IDENTITY PROFILE | **PARTIAL** |
| CRANIUM | **PARTIAL** |
| EYES/EXPRESSION | **PARTIAL** |
| NOSE | **PARTIAL** |
| MIDFACE | **PARTIAL** |
| MOUTH/JAW | **PARTIAL** |
| SKIN | **PARTIAL** |
| HAIR | **PARTIAL** |
| RIG | **PASS** |
| LOD | **PASS** |
| RESTART | **PASS** |
| OVERALL FACE GATE | **FAIL** |

**Do NOT promote. STOP FOR USER REVIEW.**
