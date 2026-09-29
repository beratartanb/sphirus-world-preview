# Skin surface realism

Deep reference for [../SKILL.md](../SKILL.md). Shader implementation belongs to
[materials-lighting-rendering](../../sphirus-materials-lighting-rendering/SKILL.md); this file sets the art intent for the
body skin and decides what is geometry and what is material. Keep realism **understated**.

## Geometry vs material decision

Ask: **"If this feature disappears at normal character distance, should it really be base geometry?"**

| Put in | Features |
|---|---|
| Geometry (base mesh / morphs / correctives) | Silhouette, primary and secondary anatomy, major folds (glute fold, IMF, axilla, joint creases in pose) |
| Normal / displacement | Pores, follicles, fine wrinkles (knuckles, elbows, knees), tiny skin irregularity, stretch marks if used |
| Shader | Subsurface scattering, roughness/specular, colour variation, sheen, wetness |

Tertiary detail in geometry costs deformation quality, LOD stability, morph size and garment collision, and reads as noise.

## Base colour

- Subtle vascular/temperature variation: slightly warmer/redder at elbows, knees, knuckles, heels, and cheeks of the
  glutes; slightly cooler/bluer where veins are near the surface (inner wrist, inner elbow, upper chest in fair skin).
- Chest/shoulder tone: sun-exposed areas (shoulders, upper back, forearms) marginally warmer or darker than covered areas.
- Palms and soles lighter and less saturated; the transition along the side of the hand/foot is soft.
- Keep all variation low-amplitude and low-frequency; the skin should read as one person's skin, not patches.

## Roughness

- Regional variation: slightly lower roughness (oilier) at the upper chest/sternum, upper back, and where skin is
  thinner; higher (drier) at elbows, knees, shins, heels.
- Cloth-contact zones (under waistband, straps) marginally different, never a visible band.
- Never uniform roughness: uniform values are the main cause of plastic or wax skin. Never a noisy roughness map either.

## Normal

- Pores: correct scale (body pores are smaller and sparser than facial pores); a directional follicle pattern on limbs.
- Fine wrinkles: joint creases (knuckles, elbow backs, knee fronts in extension, wrist creases), neck lines.
- Tiled detail normals must be scaled to real skin scale and blended so tiling does not read.

## Micro displacement

Extremely subtle skin breakup visible only in close-ups and grazing light. If it reads at gameplay distance it is too strong.

## Optional understated detail

Faint veins (inner arm, top of the feet, chest in fair skin), very subtle cellulite-scale variation (outer thigh, lower
glute; almost imperceptible), small scars, freckles and body marks. Each must be motivated by the character and kept below
the threshold of drawing attention.

## Avoid

Noisy procedural skin, wax/plastic skin, uniform roughness, oversized or evenly distributed pores, painted-on muscle
definition (colour or normal maps faking anatomy that the geometry lacks), and high-contrast subsurface that makes skin
look like candle wax.

## Review

Judge skin separately from anatomy: first clay (geometry), then the production skin in neutral light at close range,
gameplay distance and grazing light. Check the head/body skin match at the seam (tone, roughness, pore scale) — a
mismatched body skin breaks the character read even when the anatomy is right.
