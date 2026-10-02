# GUARDIAN-7: GUARDIAN-6 correction (hollowing rollback, cranium, hair volume and lock structure)

Date: 2026-10-02. Status: **STOPPED FOR USER REVIEW.** Nothing was promoted.

- **Candidate:** `/Game/Sphirus/CharacterLab/CharacterGuardian7_20261002/`.
- **Protected folders were not modified:** production and GUARDIAN 1–6. All 18 protected groups are byte-identical to the checkpoint (`data/preservation_check.json`).

## Final GD7 candidate

| Part | Asset |
|---|---|
| Face | `Face/SKM_GD7_Face_c8`: fresh Epic auto-rig on the corrected neutral C8 (`MHC/MHC_GD7_C8`, `MHC/DNA/MHC_GD7_C8_Head`). RigLogic, 858 morphs, 8 LODs. |
| Hair | `Hair/GR_LK_Hair_{Main,Loose}_h17`: new builder `blender_gd7_hair.py`. Bindings `Face/Bindings/GB_GD7_*_c8h17`. |
| Skin, eyes, body, garments | GUARDIAN-5 k7 skin, read-only. e2 eyes, B2 body, Henley g17e, Chaos shorts m1 unchanged. |

## 1. Over-hollowing rolled back (boards A, B)

- **Rollback baseline R7:** GD4 E1, plus the GD5 nose / lip / nasolabial cheek-side / jowl ops, plus the GD6 nose and upper-lid sculpt, plus the jaw lock. Removed:
  - every GD5 / GD6 hollowing op: submalar, lid-cheek, perioral, prejowl, malar descent, corner embed;
  - the GD6 nasolabial step, tear trough, malar deflation and submalar plane.
- **New corrected face C8:** R7 plus small *support* (positive) volume:
  - outside the nasolabial line: +0.5 mm;
  - at the modiolus (mouth-corner pillar): +0.3 mm;
  - soft cheek smoothing.
- **Hollowing check:** signed offset along the surface normal vs R7, mean / min in mm (`data/hollowing_vs_R7.txt`). Negative means hollowed.

  | Zone | GD6 S4 (mm) | C8 (mm) |
  |---|---|---|
  | Submalar | −1.4…−1.7 / −4.2 | ≥ 0 |
  | Malar | −0.9 / −3.2 | ≥ 0 |
  | Perioral | −0.6…−1.0 | ≥ 0 |
  | Tear trough | −0.9…−1.0 | ≥ 0 |
  | Nasolabial outside the line | – | +0.12 |

- **Jaw/chin lock unchanged:** Δ 0.9 / 5.0 / 0.8 px, menton 0 px.

## 2. Cranium: middle ground (board C, user correction applied)

The first spread, C7, over-widened the upper skull and flattened the top. It was rejected. C8 is the corrected version:
- parietal spread and upper-temple spread reduced to about half of C7;
- the upper-parietal op removed;
- a vertex arc restore added (+1.6 mm), giving a natural top arc.

| Breadth above the eyes (cm) | R7 (too narrow) | C7 (rejected) | C8 |
|---|---|---|---|
| +4 | 14.78 | 15.36 | 15.10 |
| +6 | 14.30 | 15.21 | 14.58 |
| +8 | 12.17 | 13.26 | 12.27 |

Vertex height above the eyes: 10.41 | 10.41 | 10.57 cm. Board C shows R7 | C7 | C8 in front, 3/4, profile, rear and top views, plus UE clay of C8. The skull was fixed bald first; the hair was then rebuilt on C8.

## 3. Hair: volume and lock structure (boards D, E, F; user directive)

### Diagnosis in the scene

The groom is strand geometry from the project's own builder (UE GroomAsset from Alembic), not cards. The rope / dreadlock look had three structural causes:

1. **Shared bun entry points.** Every lock aimed at one of seven shared bun entry points, so whole groups funnelled into one cord.
2. **Strong convergence.** Strand → tertiary → secondary convergence of 0.7–0.95 produced round, evenly thick cords separated by deep channels.
3. **Lift fixed at the lock root.** Front-rooted locks carried their low hairline lift over the crown, so the profile stayed flat. A lower lift right at the part made two symmetric ridges beside the part.

### Fix (`blender_gd7_hair.py`, h17)

- **Lift field evaluated along each lock path:** low at the hairline, rising to the crown and the rear-upper head, rolling down toward the nape. Side height above the ears is held down, a small left/right asymmetry is added, and there is no dip at the part.
- **Smaller masses, looser locks:** 60 smaller primary masses. Looser secondary and tertiary convergence (×0.6), with strand convergence 0.45–0.70. Persistent lateral fill so groups overlap with no empty channels, plus extra medium-scale depth variation on the back.
- **Bun entries per lock**, spread around the bun rim, so groups no longer funnel together. Jittered loops and fewer turns, so no ring.
- **Narrower loose locks at the sides:** temple, side and ear loose locks pulled 7–10 % closer to the head.

### Measured silhouette (`data/hair_silhouette_h9_h17.txt`)

Profile stand-off of hair above the skull, by angle around the head centre, in cm:

| View angle | h9 (cm) | h17 (cm) |
|---|---|---|
| 80° (front-top) | 2.36 | 2.46 |
| 95° (top) | 2.53 | 3.11 |
| 110° | 2.65 | 3.78 |
| 125° | 2.82 | 4.50 |
| 140° (rear-upper) | 3.39 | 5.10 |
| 155–170° (toward the nape) | 3.6–3.8 | 4.2–4.4 |

The rear-upper hair now rolls down toward the nape. Front robust width at +4 / +6 cm above the eyes changed by ≤ 0.5 cm, so the sides are not widened. The extra width is only at the top, which rounds instead of peaking.

### Before / after evidence (board F)

- **Identical conditions:** h9 vs h17 on the same C8 face, pose, camera, scale and light. Views: both sides, back, front, 3/4, back 3/4.
- **Main-mass-only silhouette** (no fine strands, no shine): the profile reads as a continuous arc from forehead over the crown to the nape.
- **Iterations:** h10–h16 were intermediates, each judged in UE captures:
  - h12/h13: front humps beside the part;
  - h14: flat crown;
  - h15: balloon dome and a ring bun.

### Hair components changed

- **Main groom:** primary / secondary / tertiary construction, the lift field, the bun entries.
- **Loose groom:** temple / side / ear lateral offsets.
- **Hairline (D):** temporal hairline raised about 1 cm at 62° / 74°, stronger jag, wider density ramp, more fine edge hairs.
- **Material:** h6 values kept (brown-first auburn, matte).

## Gates

| Gate | Result | Note |
|---|---|---|
| HOLLOWING DIRECTION | PASS | Every hollowed zone is back to ≥ 0 mm vs the rollback; no grooves. |
| SOFT-TISSUE SUPPORT | PARTIAL | Tissue-supported and not gaunt; adult character still relies on texture. |
| CRANIUM WIDTH | PARTIAL | Between too-narrow and over-wide (+0.3 / +0.3 / +0.1 cm vs R7). |
| TOP CRANIAL ARC | PASS | Natural arc restored (vertex +1.6 mm vs C7); no flat top. |
| PARIETAL WIDTH | PARTIAL | Subtle; judge on board C. |
| OVERALL CRANIUM PROPORTION | PARTIAL | |
| UPPER TEMPLE HAIR START | PARTIAL | Higher and broken up; the front part edge still shows a little dark scalp from high views. |
| SIDE TOP HAIR VOLUME | PASS | Lifted, uneven, connected to the bun; no puff. |
| CROWN PROFILE SILHOUETTE | PASS | Continuous arc in the main-mass-only silhouette. |
| Rope / dreadlock locks removed | PARTIAL | Cords are gone; the back still reads somewhat smooth and dense compared with the reference's airy, damp clumps. |
| Part / root rise / bun transition | PARTIAL | Narrow part and no symmetric ridges. The bun integrates into the flow, but its edge is soft and less defined than the reference. |
| Face / skull anatomy preserved during the hair work | PASS | Hair changes only; C8 is unchanged. |
| RIG | PASS | 23 cases. |
| LOD | PASS | Face 8 LODs, grooms 4 LODs. |
| RESTART | PASS | Fresh reopen: everything loads, nothing dirty; after-restart captures done. |
| OVERALL FACE GATE | FAIL | |
| OVERALL CHARACTER LIKENESS GATE | FAIL | |

## Not solved

- The rear mass is denser and smoother than the reference.
- Bun edge definition.
- The front part shows dark scalp in high views.
- Brows, skin micro-relief, seam arc and the overall likeness gap (see GUARDIAN-6).
- The hair is script-authored. Final lock placement for the bun and face framing still needs artist grooming (ARTIST-GRADE = NO).

## Boards

| Board | Content |
|---|---|
| A | Soft-tissue support |
| B | Nasolabial / submalar |
| C | Cranium width / top arc |
| D | Upper temple hair start |
| E | Side-view top hair / crown |
| F | Hair volume / lock before–after, plus main-mass silhouette |
| 01–03 | Neutral face: front, 3/4, profile |
| 04 | Lighting A–E |
| 05 | Seam |
| 06 | Reference expression |
| 07 | Full character |
| 08 | Rig |
| 09 | LOD |
| 10 | After restart |
