# Anatomy, form hierarchy and body rhythm

Deep reference for [../SKILL.md](../SKILL.md). Region deep dives: [breast and ribcage](breast-ribcage.md),
[pelvis, hips, glutes](pelvis-hips-glutes.md), [limbs and joints](limbs-joints.md), [soft tissue](female-soft-tissue.md).

## Primary / secondary / tertiary form

| Level | What it is | Where it belongs |
|---|---|---|
| **Primary** | Skeleton/ribcage, pelvis, shoulder width, torso mass, breast mass, glute mass, thigh mass, arm mass, the overall silhouette | Proportions, skeleton/joint placement, base mesh, body blend shapes |
| **Secondary** | Clavicle, scapula, deltoid, sternum, costal margin, abdominal wall, iliac crest, gluteal fold, hamstring transition, patella, calf heads, elbow landmarks, forearm masses | Sculpt on the base mesh (morph/corrective) |
| **Tertiary** | Pores, tiny wrinkles, subtle veins, micro skin breakup, very fine folds, cellulite-scale variation, fine roughness variation | Normal/displacement maps, roughness, skin shader, microdetail tiles ([skin](skin-surface-realism.md)) |

Rules:
- Work in order: primary → secondary → tertiary. Refining secondary forms on a wrong primary wastes the pass and hides the
  real problem.
- Secondary forms are **subordinate**: they are read through soft tissue, not carved. Choose a small number of accents per
  view; not every landmark is equally visible (see over-sculpted in [failure modes](failure-modes.md)).
- Tertiary detail in base geometry pollutes deformation, LODs, morph deltas and garment collision. Test: *if the feature
  disappears at normal character distance, it is not base geometry.*

## Whole-body rhythm

Evaluate continuous chains, never isolated parts:

- head → neck → shoulders → ribcage → waist → pelvis → hips → thighs → knees → calves → ankles
- shoulder → upper arm → elbow → forearm → wrist → hand

The female figure alternates convex masses and narrower connections, and the curves on opposite sides of a limb or torso
are **offset**, not mirrored (e.g. the outer calf high, inner calf lower; outer thigh high at the hip, inner thigh mass
lower). Straight segments and mirrored bulges read artificial. In side view, check the S-rhythm: thoracic curve → lumbar
curve → sacral plane → glute → hamstring → calf → heel.

Always ask: **"Does this still read as one coherent human body?"** A good breast on a tube torso, or strong glutes on a
flat pelvis, fails that question.

## Proportion reading (not targets)

Use proportions to diagnose, not to force a template. Useful comparisons for a realistic adult woman:
- Shoulder (acromion) width and hip (greater trochanter) width are close; hips usually slightly wider in front view, but
  the femininity comes more from the waist taper and soft-tissue curve than from raw hip width.
- Waist sits between the lowest ribs and the iliac crest; a waist that reads well has visible rib-cage and pelvis masses
  above and below it, not a narrow circumference.
- Torso:leg: crotch near mid-height; knees roughly midway between crotch and ankle; relaxed fingertips around mid-thigh.
- Side view: ribcage depth, lumbar curve and glute projection are balanced; neither the chest nor the glute dominates.
Accepted project proportions (in a project profile) override these general readings.

## Head / body balance

A head that looks too large is **not** automatically a head problem. Check first, in this order:
1. Shoulder width and deltoid cap (a flat or narrow shoulder makes any head look big).
2. Neck support: thickness, trapezius slope, sternocleidomastoid presence (a thin stalk neck enlarges the head).
3. Clavicle span.
4. Torso mass and ribcage volume.
5. Arm thickness (stick arms enlarge the head read).
6. Hair/headwear/camera (lens distortion at short distance; a tight FOV enlarges the head).
Only after these are right is head scale a candidate, and a project's face/head is often protected: then fix the support.

## Shoulders and upper torso

Target: naturally narrower female shoulder structure **without fragility**; soft rounded deltoid volume; a real clavicle
(S-curve, visible medially, fading laterally under the deltoid); subtle trapezius with a gentle neck-to-shoulder slope;
smooth deltoid-to-upper-arm transition; a believable egg-shaped ribcage that is narrower at the top and widest around the
lower ribs.

Avoid: broad square male shoulders; overdeveloped/separated deltoids; high bodybuilder traps (the neck disappears);
excessively narrow, sloping, fragile shoulders; a ribcage that is a block or a cylinder.

Diagnostics: from the front the shoulder line should descend gently from the neck and round over the deltoid; from above
the shoulders sit slightly forward of the spine line with the clavicles angled back. From the back, the scapulae show as
flat plates with a soft medial border, not ridges.

## Waist and abdomen

A realistic female abdomen is **not** a flat sheet.
- Epigastric plane: a gentle plane below the sternum that turns into the costal margin arch.
- Abdominal wall: one soft convex mass; the lower abdomen below the navel is slightly fuller and softer than the upper
  abdomen, even on a fit woman.
- Linea alba: at most a very faint vertical groove above the navel; no segmented rectus.
- Navel: a soft, slightly vertical depression in a small rounded pad, not a drilled hole.
- Oblique/flank: a soft roll over the iliac crest (the flank pad) that turns the corner from front to side.
- Ribcage → waist: the costal margin should register as a subtle change of plane; if it vanishes, the waist reads as a tube.
- Pelvis → abdomen: the lower abdomen settles into the pelvic bowl above the inguinal line.

Avoid: six-pack or visible rectus segments, vacuum waist, corset torso, excessive oblique definition, a perfectly smooth
mannequin belly with no planes.

## Back

Two erector masses flanking a soft spinal groove that deepens in the lumbar region; scapulae as moving plates; a lumbar
curve that sets the pelvis tilt; the sacral plane (a flat diamond between the dimples of Venus) leading into the glutes.
Lower-back soft tissue sits over the iliac crest at the sides. A flat back with no scapula, groove or sacral plane is a
typical generic-base failure.

## Sculpt amplitude

Practical guidance at human scale (1 unit = 1 cm; scale proportionally for other units or body sizes):

| Change | Typical displacement |
|---|---|
| Subtle anatomical refinement (planes, soft landmarks) | ~1-3 mm |
| Important secondary correction (a missing costal margin, a hard fold) | ~3-5 mm |
| Larger local correction | Only with a named anatomical/visual reason and matched evidence |

These are guidance, not limits: context, mesh density and the viewing distance matter. Warning signs that a neutral sculpt
is changing the **body type** rather than refining anatomy: circumferences or silhouette move beyond the intended local
region, the side-view rhythm changes, garment fit changes, or a body-proportion measurement shifts. When that happens
stop and ask whether the body type change is actually requested. A useful discipline is to keep a detail layer separated
from its low-frequency component so silhouette stays fixed while planes change.

## Symmetry

1. Primary structure starts symmetric: skeleton, proportions, primary masses.
2. Then introduce very subtle natural asymmetry, soft tissue only: one breast slightly fuller/lower, scapula prominence,
   hip soft tissue, a glute, a calf, one shoulder slightly lower in relaxed pose.
3. Keep it below the threshold of being noticed as a feature; obvious asymmetry reads as an error or injury.
4. Skeleton, root and gameplay alignment stay centred; never asymmetrize joints to get a soft-tissue read.
5. Asymmetry must survive mirrored animations and correctives without flipping sides.
