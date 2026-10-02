# GUARDIAN-4: jaw/chin asymmetry rollback (interim review)

Date: 2026-10-02. Status: **STOPPED FOR USER REVIEW.** Nothing was promoted. Production `MH_MainCharacter` and the GUARDIAN, GUARDIAN-2 and GUARDIAN-3 folders were not modified.

## What happened

- **Phase A (A2–A7)** rebuilt the cranium. The front no longer reads as a narrow-topped dome, and the occiput is about 0.6 cm shorter. The same candidates also pushed one-sided jaw narrowing (left xscale k up to −0.25, about 1 cm) to chase the Tier A front contour. The user judged the result **overcorrected**: a crooked-looking mandible.
- **Rollback baseline R0:** N7 plus only the symmetric cranium work (`crown_full`, `temple_fill`). All one-sided jaw, cheekbone and chin ops were removed.
- **New subtle candidate S1:** R0 plus four conservative changes:
  - a symmetric jaw narrowing (about 3.3 mm max);
  - a small left balance (1.3 mm) that cancels N7's own left-wider jaw;
  - near-symmetric cheekbone softening (2.4 / 1.9 mm);
  - the chin moved 2.5 mm toward the centreline.

## Measurements

All values are in cm, in the project frame. Character left = +x.

| | N7 / R0 | A7 (overcorrected) | S1 (subtle) |
|---|---|---|---|
| Menton (lowest point of chin), offset from facial midline | −0.69 | −0.57 | −0.50 |
| Jaw angle (gonion) height below the eyes, L / R | 9.26 / 9.48 | 10.09 / 9.48 (unreliable) | 9.45 / 9.48 |
| Lower jaw length, gonion to menton, L / R | 6.04 / 5.13 | 2.96 / 5.13 (left gonion not found) | 4.96 / 5.07 |
| Half-width 9.5 cm below the eyes, L / R | 4.80 / 4.76 | 4.00 / 4.64 | 4.40 / 4.49 |
| Front jaw contour in IPD units, L / R (Tier A: 0.543 / 0.641) | 0.727 / 0.669 | 0.579 / 0.654 | 0.671 / 0.635 |

The numbers are diagnostics only. S1 is still wider than Tier A, and its left side is still slightly wider than its right, the reverse of Tier A. It was left there on purpose: part of the Tier A left/right difference is probably head turn and lighting, not bone.

## Boards

All boards use Blender clay at the Tier A front camera.

- `J1`: REFERENCE | CURRENT OVERCORRECTED (A7) | ROLLBACK BASELINE (R0) | NEW SUBTLE (S1)
- `J2`: the same four, lower-face crop
- `J3`: mirrored split-face. Rows are REF, A7, R0, S1. Columns are the original, the character's left half mirrored, and the character's right half mirrored. The axis is the eye midpoint.

## Parked until review

- **B1 eye/mouth ops:** lateral canthi +1.1 mm, mouth corners +1.05 mm. They were built on A7 and will be re-applied on the approved jaw.
- **UE auto-rig cycle:** one cycle ran on B1 in the isolated G4 folder. Its output is unchecked and will not be used.

## Gates

| Gate | Result |
|---|---|
| LEFT JAW / CHIN ASYMMETRY | PARTIAL, pending user review |
| CRANIUM | PARTIAL; Blender clay only, UE clay gate not yet run |
| All other gates | NOT_TESTED in this interim package |
