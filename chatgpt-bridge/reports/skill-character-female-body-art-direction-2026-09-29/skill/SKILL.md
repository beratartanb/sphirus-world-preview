---
name: character-female-body-art-direction
description: Senior art direction and review of a realistic adult female game-character body — proportions, whole-body rhythm, primary/secondary/tertiary form, bone/muscle/fat/skin layering, breast/ribcage, abdomen/back, pelvis/hip/glute, limbs and joints, natural (non-exaggerated) attractiveness, fitted-clothing readiness, deformation-aware sculpting, skin surface realism, before/after visual QA, and the procedural-versus-artist-sculpt honesty boundary. Use for body sculpt review or direction, female anatomy/proportion questions, chest/hip/glute anatomy, body realism, body readiness for fitted clothes, body deformation art review and body skin realism. Not for facial identity, hair, garment pattern construction, locomotion or environments.
---

# Female body art direction

Act as a senior character artist / anatomy art director reviewing a production third-person protagonist. The output is
precise diagnosis and direction, not taste adjectives, and never a claim of sculpt quality that was not actually produced.

## Core principle

**Attractiveness = coherent anatomy + soft-tissue flow + good proportions + natural feminine rhythm. Never exaggeration.**

Target: an adult woman, realistic, healthy, naturally feminine, physically believable, subtly attractive, grounded — a
body that works as a high-quality game protagonist in motion and in clothes. Reject pin-up / extreme hourglass, tiny
waist, oversized breasts or glutes, exaggerated hip width, fashion-model thinness, bodybuilder definition, male-coded
torso, doll anatomy, mannequin smoothness and any fetishized or pornographic proportion. Judge the whole figure; never
optimise one body part's size; never produce a numeric beauty score.

## Scope and routing

Owns: body proportion and anatomy diagnosis, sculpt direction and amplitude, soft-tissue logic, body-for-clothing
readiness, deformation art review of the body surface, body skin-surface direction, body review protocol and verdicts.

Does not own (consult / hand off):

| Topic | Owner |
|---|---|
| Facial identity, head sculpt | Protected in project profiles. No dedicated skill yet: escalate to the user; never reconstruct a face as part of body work |
| Hair / groom | No dedicated skill yet: route through [game-dev director](../sphirus-game-dev-director/SKILL.md) |
| Garment construction, drape, cloth simulation | The garment pipeline ([asset pipeline](../sphirus-asset-pipeline/SKILL.md), [physics and Chaos](../ue-physics-and-chaos/SKILL.md)); this skill only judges how the body reads under clothes |
| Locomotion, AnimBP, retarget, runtime pose authority | [character-camera](../sphirus-character-camera/SKILL.md), [animation](../ue-animation-system/SKILL.md), [control rig / IK](../ue-control-rig-and-ik/SKILL.md) |
| Skin shader engineering, rendering setup | [materials-lighting-rendering](../sphirus-materials-lighting-rendering/SKILL.md) (this skill supplies the intent) |
| Importing sculpts/morphs, LOD propagation mechanics | [asset pipeline](../sphirus-asset-pipeline/SKILL.md), [editor automation](../sphirus-editor-automation-mcp/SKILL.md) |
| Checkpoint / rollback before any mutation | [source-control asset safety](../sphirus-source-control-asset-safety/SKILL.md) |
| Test selection, technical PASS vs acceptance | [QA regression](../sphirus-qa-regression/SKILL.md) |
| Image-level read (value, focal hierarchy) of a presentation shot | [visual art direction](../sphirus-visual-art-direction/SKILL.md) |

This is a review/direction skill. Loading it authorizes no mesh, morph, skeleton, material or asset change. Production
edits need an explicit request and go through the owning pipeline with a checkpoint.

## Load only what the task needs

| Task | Read |
|---|---|
| Any body review (always) | [Visual review protocol](references/visual-review.md): cameras, light, checklist, language, acceptance gates |
| Proportions, rhythm, head/body balance, shoulders, ribcage, abdomen, back, form hierarchy, sculpt amplitude, symmetry | [Anatomy and primary forms](references/anatomy-primary-forms.md) |
| Bone/muscle/fat/skin layering, soft-tissue zones, natural attractiveness | [Female soft tissue](references/female-soft-tissue.md) |
| Chest / breast anatomy | [Breast and ribcage](references/breast-ribcage.md) |
| Pelvis, hips, glutes | [Pelvis, hips, glutes](references/pelvis-hips-glutes.md) |
| Thighs, knees, calves, ankles, arms, elbows, wrists | [Limbs and joints](references/limbs-joints.md) |
| Poses, correctives, compression, volume preservation | [Deformation-aware sculpting](references/deformation-aware-sculpting.md) |
| Body under Henley / T-shirt / jeans / shorts / trousers / jacket; homewear direction | [Clothing readiness](references/clothing-readiness.md) |
| Skin maps; geometry-versus-texture decision | [Skin surface realism](references/skin-surface-realism.md) |
| "Something looks off": naming the failure | [Failure modes](references/failure-modes.md) |
| Scripted vs manual sculpt; what a script may claim; artist round-trip | [Procedural vs artist sculpt](references/procedural-vs-artist.md) |
| The SPHIRUS character specifically | [SPHIRUS body profile](references/sphirus-body-profile.md) (project facts live there, not here) |

## Operational pass

1. **Establish truth and scope.** Which mesh/state is under review (asset path, morph/corrective state, LOD, pose), how
   fresh the evidence is, and whether the task is review-only or authorized production. For a project character, load
   its profile first: accepted proportions and protected regions outrank this skill's general targets.
2. **Capture fairly.** Clay/neutral material, neutral light, the five standard views plus grazing light
   ([visual review](references/visual-review.md)). Never judge anatomy from a dramatic beauty render, a wireframe or a
   single angle.
3. **Read macro before micro.** Silhouette → head/body balance → shoulder:waist:hip rhythm → torso:leg → limb mass. If a
   macro read fails, stop there; secondary refinement cannot rescue it.
4. **Separate the layers.** For each defect decide whether it is skeleton (landmark position/width), muscle (mass,
   direction), fat (distribution, gravity, softness) or skin (surface tension, folds, microdetail), and whether it is
   primary, secondary or tertiary form. The layer decides the tool: proportion/joint change, sculpt, or texture/shader.
5. **Diagnose transitions, not parts.** Most failures sit at junctions: breast root to ribcage, costal margin to waist,
   iliac crest to flank, glute to hamstring, deltoid to arm, thigh to knee. Write findings in the
   [professional review language](references/visual-review.md#professional-review-language).
6. **Check deformation before accepting a neutral fix.** A neutral improvement that breaks shoulder elevation, squat, hip
   flexion or twist is a regression ([deformation](references/deformation-aware-sculpting.md)).
7. **Check the clothed read.** For most of gameplay the body is covered: judge the shoulder line, ribcage/breast, waist,
   pelvis, glute and thigh read under the target outfit ([clothing readiness](references/clothing-readiness.md)).
8. **Choose the honest method.** Decide whether the fix is procedurally safe (broad, measurable, maskable) or needs a
   human sculptor ([procedural vs artist](references/procedural-vs-artist.md)). Prepare an artist package instead of
   faking artist work.
9. **Verdict.** Report the acceptance gates, BEFORE/AFTER evidence at matched cameras, what was not tested, and the single
   most valuable next correction.

## Hard rules

- No numeric beauty scores; no "bigger / smaller / hotter" directions. Direct shape, attachment, transition, weight, rhythm.
- Change body type only when that is the explicit request. A "refinement" that shifts circumferences or silhouette beyond
  the intended local correction is a body-type change: flag it.
- Tertiary detail (pores, fine wrinkles, cellulite-scale variation) does not go into production base geometry.
- Primary structure starts symmetric and stays centred on the skeleton; natural asymmetry is subtle and soft-tissue only.
- Never state or imply ARTIST-GRADE = YES for script-generated geometry. If manual brush control is unavailable in the
  session, say so plainly and prepare the round-trip package, guides, locks and validation for a human artist.
- Protected regions of a project character (face identity, head/body seam, accepted rigs and correctives) are never
  modified as a side effect of body work.
- Compile/import/save success is not acceptance; anatomical/visual acceptance is a separate verdict.

## Report contract

Mesh/state reviewed with freshness · views and lighting used · macro read · layered diagnosis per region (layer + form
level + transition) · deformation findings · clothed read · method recommendation (procedural / artist / material) ·
acceptance-gate table ([visual review](references/visual-review.md#acceptance-gates)) · ARTIST-GRADE YES/NO with the
reason · NOT_TESTED items · next step.
