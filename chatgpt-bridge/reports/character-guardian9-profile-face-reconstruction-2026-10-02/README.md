# GUARDIAN-9: profile face reconstruction (nose, midface, lips, mouth–chin)

Date: 2026-10-02. Status: **STOPPED FOR USER REVIEW.** Nothing was promoted.

- **Candidate:** `/Game/Sphirus/CharacterLab/CharacterGuardian9_20261002/`.
- **Protected folders were not modified:** production and GUARDIAN 1–8. All 20 protected groups are byte-identical to the checkpoint (`data/preservation_check.json`).

## Final GD9 candidate

| Part | Asset |
|---|---|
| Face | `Face/SKM_GD9_Face_g`: fresh isolated Epic auto-rig on the profile-corrected neutral G (`MHC/MHC_GD9_G`, `MHC/DNA/MHC_GD9_G_Head`). RigLogic, 858 morphs, 8 LODs. |
| Hair | GUARDIAN-8 h23, unchanged and referenced read-only; only rebound to the new face (`Face/Bindings/GB_GD9_*_gh23`). |
| Skin, eyes, body, garments | Unchanged: k7, e2, B2, Henley g17e, Chaos shorts m1. |

## Locked and verified unchanged

| Item | Evidence |
|---|---|
| C8 cranium | Breadth profile and vertex height identical (`data/cranium.txt`). |
| Jaw / chin | Jaw contour half-widths at z 150.5 / 152.0 / 153.5 identical to C8 to 0.001 cm (`data/hollowing_and_jaw_vs_C8.txt`). The chin was only moved anteroposteriorly, never sideways. |
| No hollowing | Signed offset vs C8 along the surface normal is ≥ 0 mm in the nasolabial, submalar, perioral and tear-trough zones. Malar and anterior cheek are +0.9 to +1.0 mm (support). |
| Eye spacing | Eye-joint distance 5.901 cm (C8: 5.901). |
| h23 hair | Not rebuilt. |

## Passes

Every pass was checked in strict profile, the ~33° 3/4 Tier A camera and front, using Blender clay.

| Pass | Changes |
|---|---|
| A — nose | Tip lowered and lengthened. Columella and alar rim lowered (less nostril show). Supratip filled. Lower dorsum straightened. Glabella +1.1 mm. |
| B — midface | Malar apex +1.7 mm (normal) and maxilla +0.6 mm forward. |
| C — lips | Upper vermilion border raised and everted along the tracked border. Both lips projected about 1.2–1.3 mm. Lower-lip body volume +0.6 mm. Width unchanged. |
| D — mouth–chin | Chin pad back 2 mm, soft labiomental transition, small chin-pad rounding. |
| G — coherence | Nose tip forward 2.4 mm and down 1.3 mm. Lower dorsum +1.3 mm. Lobule fuller. Anterior cheek +1.6 mm. Light smoothing. |

### Reverted or not adopted

- **Radix forward** (pass A2): Tier B suggested a higher radix, but the Tier A 3/4 silhouette pick contradicts it, and Tier A wins.
- **Mirror-symmetrisation after the sculpt:** it shifted the lower face sideways because the reshaped nose moves the midline estimate. It was dropped. The sculpt ops are already symmetric, and the jaw contour proves the jaw is unchanged.

### Auto-rig and joints

One fresh isolated auto-rig on G. Joints vs C8 (`data/joint_comparison.json`):

| Joint measure | C8 | G |
|---|---|---|
| Eye-joint distance (cm) | 5.901 | 5.901 |
| Mouth-corner joints (cm) | 4.605 | 4.602 |
| Eye → nose-tip joint height (cm) | 2.915 | 3.016 (follows the longer nose) |

Only 12 of 843 facial joints moved more than 1 mm.

## Measurements (`data/`)

Midline profile values are in cm. Tier A has no strict profile, so there is no Tier A column for them.

| Measure | GD8 (C8) | GD9 (G) | Tier A |
|---|---|---|---|
| Tip projection from subnasale (cm) | 1.49 | 1.64 | – |
| Nasion → tip length (cm) | 4.25 | 4.56 | – |
| Nasion depth behind glabella (cm) | 0.13 | 0.23 | – |
| Lower lip ahead of pogonion (cm) | 0.66 | 0.96 | – |
| Upper lip ahead of lower lip (cm) | 0.20 | 0.12 | – |
| Labiomental depth (cm) | 0.06 | 0.05 | – |
| Upper lip thickness, 3/4 tracker (IPD) | 0.110 (0.66×) | 0.118 (0.71×) | 0.167 |
| Lower lip thickness, 3/4 tracker (IPD) | 0.204 (0.90×) | 0.210 (0.92×) | 0.227 |
| Lower lip thickness, front (IPD) | 0.143 (0.94×) | 0.156 (1.02×) | 0.153 |
| Mouth width, front (IPD) | 0.852 | 0.852 | 0.844 |

**Tier B profile fit (aid only):** `data/profile_tierB_fit.txt`. The two Tier B panels disagree with each other, by up to 1.6 cm at the chin. They were not used as targets where Tier A disagreed.

## Gates

| Gate | Result |
|---|---|
| PROFILE NOSE | PARTIAL |
| PROFILE RADIX / BRIDGE | PARTIAL |
| PROFILE TIP / ALA / COLUMELLA | PARTIAL |
| PROFILE ZYGOMA | PARTIAL |
| PROFILE MALAR | PARTIAL |
| PROFILE MAXILLA | PARTIAL |
| PROFILE MIDFACE | PARTIAL |
| PROFILE UPPER LIP | PARTIAL |
| PROFILE LOWER LIP | PARTIAL |
| PROFILE LIP PROJECTION | PARTIAL |
| PROFILE MOUTH-CHIN RELATION | PARTIAL |
| FULL PROFILE SILHOUETTE | FAIL |
| 3/4 IDENTITY PRESERVATION | PASS |
| FRONT IDENTITY PRESERVATION | PASS |
| SOFT-TISSUE SUPPORT PRESERVATION | PASS |
| JAW / CHIN BALANCE PRESERVATION | PASS |
| CRANIUM PRESERVATION | PASS |
| HAIR ARCHITECTURE PRESERVATION | PASS |
| RIG | PASS |
| LOD | PASS |
| RESTART | PASS |
| IDENTITY FRONT | PARTIAL |
| IDENTITY 3/4 | PARTIAL |
| IDENTITY PROFILE | FAIL |
| OVERALL FACE GATE | FAIL |
| OVERALL CHARACTER LIKENESS GATE | FAIL |

### Why

Every regional change moved in the direction of the reference: longer and more projecting nose, fuller lips with more projection, more anterior cheek mass, softer chin. None regressed 3/4 or front.

Under the user's own test (reference profile next to GD9, no labels), the profile **still reads as another woman** (board 01):

- **Nose:** the reference nose is visibly larger and longer, with a fuller, lower tip. GD9 is closer, but still smaller.
- **Midface:** the reference midface and lower face carry more soft-tissue mass. GD9 still reads leaner and younger.
- **Lips:** the reference lips are fuller in profile.
- **Profile line:** the reference forehead-to-nose line is more continuous.

The remaining gap is several millimetres to about a centimetre of soft-tissue volume. That is beyond what the parametric region brushes reached in this pass without risking a lumpy surface.

### Recommendation

Use one of these for the next pass:

- **Option 1:** a proper interactive sculpt session on the G neutral (Blender sculpt mode or ZBrush) against Tier A overlays, focused on nose volume, midface / lower-face soft-tissue mass and lip volume, then one auto-rig.
- **Option 2:** explicit approval for larger parametric amplitudes (nose tip +3–5 mm, midface volume +2–4 mm).

The rig, LOD and restart pipeline is proven and can absorb either.

**Technical:** the fresh-editor reopen loads the face (DNA user data, 858 morphs, 8 LODs), the MHC and DNA, the h23 grooms and the four `gh23` bindings, with nothing dirty before or after. After-restart captures are on board 13.

## Boards

| Board | Content |
|---|---|
| 01 | Profile full |
| 02 | Profile nose (profile / 3/4 / front) |
| 03 | Cheekbone / midface |
| 04 | Lips |
| 05 | Mouth–chin |
| 06 | Profile overlay (Tier B fit plus Tier A 3/4 clay-edge overlay) |
| 07 | 3/4 after profile edits |
| 08 | Front regression check |
| 09 | Soft-tissue support |
| 10 | Hair preservation |
| 11 | Rig test |
| 12 | LOD |
| 13 | After restart |

All comparisons are REFERENCE | GD8 | GD9 with the same cameras and lights. The head is not rotated and the FOV is not changed.
