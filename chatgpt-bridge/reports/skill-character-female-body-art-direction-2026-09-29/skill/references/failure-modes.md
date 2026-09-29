# Failure modes

Deep reference for [../SKILL.md](../SKILL.md). Name the failure family first; it points at the right layer and method.
A body can show several families in different regions (e.g. generic torso + over-sculpted limbs).

| Family | Symptoms | Root cause | Direction |
|---|---|---|---|
| **Generic MetaHuman / base body** | Smooth undefined torso, generic breasts, flat back (no scapulae, spinal groove, sacral plane), limbs as soft cylinders, landmarks averaged away | Statistical/blendshape base with averaged secondary form | Add secondary structure through soft tissue: ribcage planes, costal margin, scapulae, sacral plane, limb direction; keep primary masses |
| **Bodybuilder** | Carved muscle separations, hard separated deltoids, six-pack, veins, striation, hard calf diamonds | Muscle sculpted without a fat layer; wrong character brief | Restore the soft layer; keep mass and direction, remove separations |
| **Pin-up** | Tiny waist, oversized chest, oversized glutes, extreme pelvis, arched display posture | Optimizing isolated parts for appeal | Return to whole-figure proportion and rhythm; restore ribcage/pelvis mass around the waist |
| **Doll** | Smooth plastic surfaces, perfect symmetry, no bony landmarks, no creases | No skeleton or skin logic | Add readable bone landmarks, natural asymmetry, skin behaviour at joints |
| **Masculinized female** | Excessively broad square shoulders, thick high traps, block ribcage, straight waist-to-hip rhythm, narrow pelvis read, hard angular limbs (jaw shape is face scope, not body) | Male-coded skeleton widths or male muscle emphasis | Rebalance shoulder/pelvis read, egg-shaped ribcage, waist taper from crest and costal margin, softer limb contours |
| **Over-sculpted** | Anatomy visible everywhere, every muscle equally emphasized, noisy surface, tertiary detail in geometry | Lack of hierarchy; detail used as quality | Choose accents per view, subordinate secondary forms, move tertiary detail to maps |
| **Under-sculpted** | Mannequin surface, no skeleton beneath the skin, no soft-tissue logic, featureless transitions | Primary masses only | Add landmarks and transitions; build the four layers |
| **Inflated / vacuum** | Tight skin over balloon volumes, no gravity, hard boundaries | Volume added without soft-tissue behaviour | Gravity settle, softer transitions, lower-pole weighting |
| **Pasted-on parts** | Breasts or glutes correct in isolation but unattached | Part-by-part work | Rework roots and transitions; check the chain through the body |
| **Neutral-only success** | Good bind pose, breaks in elevation/squat/twist | No deformation review | Deformation set; rebase correctives ([deformation](deformation-aware-sculpting.md)) |
| **Clothing-blind** | Good nude read, poor read under shirts/trousers | Sculpted for nude presentation | High-value clothing regions ([clothing](clothing-readiness.md)) |
| **Material-faked anatomy** | Muscle definition painted into colour/normal maps, anatomy that disappears in clay | Material used to hide missing geometry | Put secondary form back into geometry; keep maps for tertiary |
| **Script-grade presented as artist-grade** | Measured, symmetric, averaged "anatomy" with uniform amplitude; claimed as finished art | Procedural pass mislabelled | Relabel honestly; prepare an artist round-trip ([procedural vs artist](procedural-vs-artist.md)) |

## Quick triage from a single screenshot

1. Squint (thumbnail): silhouette and rhythm OK? If not, it is primary (pin-up, masculinized, proportions).
2. Clay with grazing light: planes and landmarks present? If not, under-sculpted / generic / doll.
3. Are there hard lines everywhere? Over-sculpted / bodybuilder.
4. Do the breasts, glutes and hips connect to ribcage and pelvis? If not, pasted-on / inflated.
5. Does it hold in a pose? If you have not seen one, DEFORMATION is NOT_TESTED.
