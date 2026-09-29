# Deformation-aware sculpting

Deep reference for [../SKILL.md](../SKILL.md). **A neutral sculpt is not successful if it breaks deformation.** Every
neutral change moves vertices that skin weights, helper bones, pose correctives and garments were authored against.
Rig mechanics belong to the animation/rig skills ([animation](../../ue-animation-system/SKILL.md),
[control rig / IK](../../ue-control-rig-and-ik/SKILL.md)); this file is the art review of the deformed surface.

## Deformation review set

| Region | Poses | Look for |
|---|---|---|
| Shoulder | Arm elevation 90 / 120 / 150 / 165 / 180 deg (front, side, abduction and flexion); any project high-elevation shoulder system | Deltoid collapse, trapezius wall/ridge, axilla tearing, clavicle sliding, neck-to-shoulder fold |
| Chest | Arms forward, arms raised, arms crossed, torso twist | Breast root tearing, lateral transition folding, sternum interpenetration, breast sliding |
| Abdomen | Forward bend, crouch, side bend | Belly collapse into a crease line, flank pinch, navel sliding |
| Back | Twist, arm reach forward/overhead | Scapula smear, spinal groove lost, lat fold, lumbar crease |
| Glutes | Hip flexion, sprint cycle, squat, stride | Glute flattening to a plane, fold sliding onto the thigh, hip candy-wrap |
| Thigh | Deep squat, high knee | Front-of-hip crease depth, inner-thigh interpenetration, quad collapse |
| Knee | Deep flexion (120-150 deg) | Knee losing width, front point collapse, popliteal interpenetration |
| Elbow | Strong flexion (130-150 deg) | Elbow point loss, forearm/biceps interpenetration, volume loss |
| Wrist / neck | Full rotation and flexion | Candy-wrap twist, thinning |

Review each pose in clay from at least the front, side and a 3/4 that looks into the problem area, plus the gameplay
camera for poses that appear in play (idle, walk, jog, sprint, jump, crouch).

## Volume preservation and compression logic

- **Flexion side compresses**: tissue must flatten and bulge outward (biceps mass in elbow flexion, abdomen roll in
  forward bend, calf-thigh contact in deep squat), not interpenetrate or thin.
- **Extension side stretches**: tissue flattens and the landmarks sharpen (olecranon, patella, scapula), but volume does
  not vanish; the joint keeps its width.
- **Twist distributes**: rotation must spread along the limb/spine segment; a twist concentrated at one ring is candy-wrap.
- **Landmarks stay attached to their bones**: the patella, clavicle, scapula and iliac crest move with their bones; soft
  tissue slides over them. A landmark that smears is a weighting/corrective problem, not a sculpt problem.
- **Soft tissue lags and settles**: breasts, glutes and back-of-arm respond to gravity in the posed direction (a
  corrective or secondary-motion task).

## What the neutral sculpt must respect

1. **Joint centres**: do not move soft forms so that a joint no longer sits inside its mass (the hinge shows as a bend in
   the wrong place). Changing proportions around joints requires re-evaluating weights and correctives.
2. **Weight boundaries**: large neutral displacements near a weight transition (shoulder, hip, knee, elbow) amplify
   linear-blend artefacts. Prefer changes away from the boundary, or plan the corrective with the sculpt.
3. **Existing correctives are additive**: a pose corrective authored on the old neutral adds its delta to the new one;
   if the neutral already contains the fix direction the result overshoots. Rebase correctives when neutral changes
   significantly, and review the combined result.
4. **Helper/twist bones**: sculpting volume that a helper bone was meant to produce (e.g. a deltoid pushed out where an
   upper-arm helper already pushes) doubles it at elevation.
5. **Room to compress**: a neutral with maximum projection everywhere has nowhere to compress; flexion then produces
   interpenetration.
6. **Head/body seam and other split-mesh seams**: identical deltas on both sides of a seam, or the seam opens in some pose.
7. **LODs**: neutral changes must propagate to every LOD (or be verified there); lower LODs often lack helper skinning.
8. **Garments**: every neutral change can create new body-through-garment penetration; re-run the clothing check.

## Method notes

- Test neutral changes against the full review set before accepting them; neutral-only acceptance is PARTIAL at best.
- Compare BEFORE/AFTER per pose with matched cameras; measure deformation defects (penetration, local volume/area ratios,
  seam gaps) as supporting evidence, but judge the art visually.
- When a pose defect survives a well-weighted neutral, the fix is a pose-space corrective or helper change owned by the
  rig pipeline, not more neutral sculpting.
- Document every pose that was not tested (NOT_TESTED) rather than implying coverage.
