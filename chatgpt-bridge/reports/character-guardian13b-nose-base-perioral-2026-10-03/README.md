# GUARDIAN-13b: nose base and perioral correction (clay, before rig)

Date: 2026-10-03. Status: **STOPPED FOR USER REVIEW.** Nothing was promoted.

- **No new UE assets:** nothing was auto-rigged and the hair is still paused.
- **Protected folders were not modified:** all 25 protected groups are byte-identical (`data/preservation_check.json`).

This pass is sculpt **F3**, built on E6 (`data/ops/F3.json`). Every change was checked in front, verified 33° 3/4 and profile.

## Diagnosis (cross-sections of E6)

**Nose base:**
- **Tip–ala junction:** a sharp groove at |x| ≈ 1.0 cm, about 1 mm deep, between the tip lobule and the ala.
- **Ala → cheek:** a steep drop of 9 mm in 2 mm.
- **Alar rim:** rolled inward. This is the MetaHuman base nostril shape.

**Lips:**
- **Below the lower lip:** a sharp step of 3.5 mm within 2 mm, which isolates the lower lip as a block.
- **Lower-lip ends:** the lower lip ends abruptly toward the corners (13.15 → 12.73 within 3 mm).
- **Philtrum → upper lip:** a steep transition.

## Tried and rejected

| Attempt | Method | Why rejected |
|---|---|---|
| F1 | A new **height-map concavity fill** in `tools/blender_gd13_ops.py` (`hfill`). It raises only grooves toward a low-pass surface and can also trim bumps. | On the nose base it pulled nostril-interior vertices forward. That crumpled the alar base in 3/4 and made jagged artifacts in profile. |
| F2 | The same fill, limited to outer, forward-facing skin by a normal mask | The alar rim still crinkled |

**Conclusion:** the height-map method is unusable on the nose base, but it works well on the lips.

## Kept in F3

**Nose:** smooth ellipsoid edits along the surface normal, with no relax near the rim.
- Tip–ala junction filled by 0.6 mm.
- Supra-alar groove filled in three steps along the arc.
- Alar lobule softened by −0.3 mm.
- Alar–cheek crease filled by 0.5 mm.

**Lips:** height-map edits on the outer skin shell only. The mouth line is untouched, and lip-to-teeth clearance is unchanged at 8.0 mm.
- Philtrum → upper-lip concavity filled.
- Lower-lip bump trimmed by 0.3 mm.
- Lateral lower lip tapered into the corners.
- Groove below the lower lip filled by 0.8 mm.
- Modiolus around the mouth corners filled.
- Soft relax of the upper and lower perioral skin.

**Unchanged:** mouth width, jaw, eyes, nose dorsum and cranium; all moved 0 mm.

## Gates

| Gate | Result |
|---|---|
| NOSTRIL FORM | FAIL |
| ALAR UPPER FORM | PARTIAL |
| NOSE BASE INTEGRATION | PARTIAL |
| PHILTRUM-TO-UPPER-LIP | PARTIAL |
| UPPER-LIP FORM | PARTIAL |
| LOWER-LIP FORM | PARTIAL |
| PERIORAL INTEGRATION | PARTIAL |
| MOUTH NATURALNESS | PARTIAL |

### Honest read

**Better:**
- **Lips:** in 3/4 and front the lower lip is less of a separate block. It now tapers into the corners and flows into the chin.
- **Groove under the lower lip:** softened.
- **Philtrum → upper lip:** smoother.

**The nostril problem is not solved by this method.**
- **What is left:** the nostril/alar base is only slightly calmer (tip–ala groove and supra-alar crease filled, less pinched). The alar rim is still rolled inward, so from the front and 3/4 the nose base still reads as a round tip plus two curled wings with dark pockets (board A).
- **Why:** the curl is the base MetaHuman nostril shape, the rim of skin folding into the nostril. Every surface-level edit here either barely changes it (F3) or crumples it (F1, F2).

**Recommendation (your decision):** reshape the nose base before the auto-rig, using one of these:
- **(a) MetaHuman Creator nose-region edit:** the nostril/alar region controls or a preset blend on the MHC asset, then re-fit and auto-rig.
- **(b) Hands-on Blender sculpt session:** rebuild one on F3 (`blender_gd10_session.py`) to unroll the alar rim with mask + move brushes.

Both keep everything else that F3 has.

## Boards (`boards/`)

| Board | Content |
|---|---|
| A | NOSTRIL / ALAR UPPER FORM: REFERENCE / CURRENT E6 / NEW F3, front + 3/4 |
| B | NOSE BASE INTEGRATION: front + 3/4 + profile |
| C | PHILTRUM / UPPER LIP |
| D | FULL LIP REGION INTEGRATION |
