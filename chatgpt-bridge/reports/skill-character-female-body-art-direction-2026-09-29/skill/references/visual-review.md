# Body visual review protocol

Deep reference for [../SKILL.md](../SKILL.md). Every serious body review uses this capture setup, checklist, language and
gate table. Anatomy judged outside this protocol is at best REVIEW_REQUIRED.

## Capture setup

**Material.** Review anatomy on a neutral clay material (mid-grey to warm light grey, roughness ~0.6-0.7, no subsurface,
no textures). Then repeat key views on the production skin to judge the material separately. Skin subsurface, specular
and colour variation hide or invent form; clay tells the truth about geometry.

**Lighting.**
- Neutral: soft key from front-above (~35-45 deg elevation, ~30-45 deg off axis), gentle fill, no strong rim. Fixed
  exposure (no auto-exposure between A/B captures).
- Grazing: a single hard-ish light nearly tangent to the surface (10-20 deg) from the side and from above, to reveal
  planes, flat spots, lumps, dents and noise. Rotate it; one grazing angle hides half the defects.
- Optional rim/back light to read the silhouette edge and the transitions it crosses (breast root, glute fold, calf).
- Never judge anatomy only under cinematic lighting, heavy contrast, colour grading or depth of field.

**Cameras.** Orthographic or long lens (35-50 deg FOV equivalent is the minimum; a long telephoto avoids perspective
distortion of proportions). Camera height at the navel/pelvis for full-body proportion views, at chest height for
upper-torso detail. Same camera, light and exposure for BEFORE and AFTER, pixel-aligned.

Required full-body views: **front, side (both sides when asymmetry matters), back, front 3/4, rear 3/4.** Add close-ups
for the regions under discussion (chest/ribcage 3/4, waist/abdomen side, pelvis/glute rear 3/4 and side, knee side,
elbow side, shoulder 3/4 from above). Add a gameplay-distance view (the actual third-person camera distance/FOV) because
a defect invisible there changes its priority, not its existence.

**Poses.** Neutral bind (A-pose or the project's review pose), a relaxed standing pose, and the deformation set in
[deformation-aware sculpting](deformation-aware-sculpting.md). A neutral-only review can never PASS the DEFORMATION gate.

**Evidence hygiene.** Record asset path, morph/corrective state, LOD, pose and capture time. Captures from different
sessions may differ by a noise floor; prove "no change" with geometry (vertex/measurement deltas), not pixel diffs.

## Review order (checklist)

Go top-down; stop and report if a higher level fails.

MACRO
- head/body balance; neck support
- shoulder width : waist : hip width rhythm (front) and chest : waist : glute depth rhythm (side)
- torso : leg length; knee height; arm length (fingertips around mid-thigh when relaxed)
- limb mass relative to torso mass
- silhouette in all five views; negative spaces (arm-to-waist gap, thigh gap/contact is anatomy-driven, not a target)

TORSO
- neck (sternocleidomastoid direction, trapezius slope, pit of the neck)
- clavicle (S-curve, span, subtle presence)
- ribcage (egg shape, costal margin, thoracic arch, side plane)
- breasts (root, poles, fold, lateral/medial transitions, gravity: [breast and ribcage](breast-ribcage.md))
- waist (lower rib to iliac crest flow, oblique/flank)
- abdomen (epigastric plane, lower abdomen, navel, linea alba)
- back (scapulae, spinal groove, erector masses, lumbar curve, sacral plane)

LOWER
- pelvis (iliac crest, ASIS, pelvic shelf)
- hips (lateral soft tissue, gluteus medius)
- glutes (origin, mass, fold, glute-ham transition: [pelvis, hips, glutes](pelvis-hips-glutes.md))
- thighs, knees, calves, ankles ([limbs and joints](limbs-joints.md))

UPPER LIMBS
- shoulder cap/deltoid, upper arm, elbow, forearm, wrist, hand connection

THEN deformation, then the clothed read, then skin surface.

## Professional review language

Write each finding as **region → observation → layer/form level → consequence → direction**. Good:

- "Lateral breast transition is too abrupt relative to ribcage curvature (secondary, fat/attachment): the mass reads
  pasted on in 3/4. Soften the lateral root into the serratus plane; keep the lower pole volume."
- "Glute projection is acceptable, but the glute-ham transition lacks weight (secondary, fat): the fold is a cut line
  with no overhang. Let the lower glute rest on the fold medially, fading out laterally."
- "Upper-arm circumference is fine; the problem is cylindrical surface anatomy (secondary): no deltoid insertion, no
  triceps mass shift to the back. Redistribute, do not add volume."
- "Waist size is not the issue; lower-rib-to-pelvis flow is too smooth (secondary, skeleton landmarks missing): the
  costal margin and iliac crest do not register, so the waist reads as a tube."
- "Shoulder width is accepted; the apparent narrowness comes from a flat deltoid cap in front view."

Bad (never write): "make her hotter", "make the butt bigger", "make the waist smaller", "more feminine", "sexier",
"looks weird". A direction without a region, a layer and a transition is not a direction.

Also state what is working. Protect good forms explicitly so a later pass does not "fix" them.

## Acceptance gates

No numeric beauty score. Each gate is PASS / PARTIAL / FAIL (or NOT_TESTED) with one line of evidence.

| Gate | PASS means |
|---|---|
| MACRO PROPORTIONS | Head/body, shoulder:waist:hip, torso:leg and limb mass read as one healthy adult woman in all five views |
| ANATOMICAL COHERENCE | Skeleton landmarks sit where the soft forms imply; no part contradicts its neighbour |
| SOFT-TISSUE REALISM | Fat and skin behave with weight, softness and attachment; no carved muscle under zero-fat skin, no mannequin surface |
| FEMININE BODY RHYTHM | Continuous alternating curves head-to-ankle and shoulder-to-hand; no straight tube segments, no pin-up exaggeration |
| BREAST / RIBCAGE | Attachment, shape, softness, gravity, transitions and deformation pass ([breast and ribcage](breast-ribcage.md)) |
| PELVIS / GLUTES | Pelvic structure and soft-tissue hip/glute curve coherent from front, side and rear |
| LIMB ANATOMY | Arms and legs have skeletal landmarks, directional masses and tapers without fitness carving |
| DEFORMATION | The deformation set holds volume without collapse, candy-wrapping, pinching or sliding landmarks |
| CLOTHING READINESS | The high-value regions read under the target outfits ([clothing readiness](clothing-readiness.md)) |
| SKIN SURFACE | Understated, regionally varied, non-noisy surface at gameplay and close range ([skin](skin-surface-realism.md)) |
| ARTIST-GRADE | YES / NO. YES only when a human (or genuinely manual brush) sculpt produced the forms and passed review; never for scripts alone ([procedural vs artist](procedural-vs-artist.md)) |

PARTIAL is normal and useful: say which view/pose/region fails. PASS requires direct visual evidence at the required
views; a numeric-only check (penetration counts, circumferences) never passes an art gate on its own.

## Report template

```
REVIEWED: <asset / morph state / LOD / pose>, evidence <path>, captured <date/time>
VIEWS/LIGHT: clay + neutral key + grazing; front/side/back/front3q/rear3q (+ close-ups ...)
MACRO: ...
FINDINGS (region → observation → layer/level → direction), strongest first:
  1. ...
WORKING / PROTECT: ...
DEFORMATION: ... | CLOTHED READ: ... | SKIN: ...
METHOD: procedural-safe / artist sculpt / material
GATES: table above
ARTIST-GRADE: YES/NO — reason
NOT_TESTED: ...
NEXT: one most valuable correction
```
