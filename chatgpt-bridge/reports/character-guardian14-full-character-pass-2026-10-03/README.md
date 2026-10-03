# GUARDIAN-14: full character pass — identity, anatomy, hair, skin, wardrobe

Date: 2026-10-03. Status: **STOP FOR USER REVIEW.** Nothing was promoted.

## Candidate

`/Game/Sphirus/CharacterLab/CharacterGuardian14_20261003/`

| Part | Asset |
|---|---|
| Face | `Face/SKM_GD14_Face_k2` (MHC `MHC/MHC_GD14_K2`, DNA `MHC/DNA/MHC_GD14_K2_Head`). One fresh auto-rig on the selected sculpt K2: RigLogic, 858 morphs, 8 LODs. RIGFIT mean 0.17 mm, max 3.6 mm; eyes 0. |
| Skin | k12 = k11 with muted lip colour: `Skin/MI_LK_Face_*_VT_g14k12`, `Skin/MI_GD14_Body_k12`. |
| Hair | h29: `Hair/GR_LK_Hair_{Main,Loose}_h29`, `MI_GD_Hair_h29`, bindings `Face/Bindings/GB_GD14_*_k2h29`. |
| Brows / lashes | Brows `GR_GD_Eyebrows_M_Natural` (was SlightArch); lashes `S_Thin`. |
| Henley | `Outfit/SKM_LK_Henley_g18p`. Neckline correction of g17e on the same topology; materials m1 referenced read-only. |
| Shorts | Chaos `SKM_LK_Shorts_g16c` (m1), unchanged. |
| Eyes, body | Unchanged: eyes e2, accepted B2 body and correctives. |

**Previous baselines:**
- Sculpt: GD13c HS3, not rigged.
- Last rigged: GD12C G with k11 skin, h24 hair and g17e Henley.

**Protection:** all 26 protected groups are byte-identical to the checkpoint taken at the start of this pass (`data/preservation_check.json`). That covers production, GUARDIAN 1–13 and the body, outfit and lookdev candidates.

**Disk:** C: ran down to 4 GB free. With your standing approval, I deleted 7,135 capture files (13 GB) of already-published passes (GD4–GD12C capture sets) from `CharacterLookdev_20260930/captures`. Their reports keep their own boards.

## Method changes (what was learned)

### 1. The nostril curl was not MetaHuman base topology

I fitted the HS3 sculpt to a fresh MetaHuman character and re-evaluated **our own face-model coefficients without the fit's high-frequency delta**. That gives a clean nose base: open nostrils, no rolled rim, no loop ala (board 14).

The curled rim and slit nostrils were accumulated sculpt detail from many passes. That is why every surface operation (normal offsets, height fills, geodesic grabs) could only half-fix it.

**Selected nose base:**
- A blend of 65 % our own model reconstruction and 35 % of the Celeste preset's nose region. The nose is PCA region 13, coefficients 835–904 of 1397.
- It is transferred into the sculpt as **detail only**: our low-frequency nose (projection, width, dorsum) plus the model's rim, ala, nostril, columella and sill form. Inside a soft nose-base mask, k = 120 (`tools/blender_gd14_nosebase.py`).

**Candidates tried:**

| Candidate | Result |
|---|---|
| Own-model only (full replacement) | Natural, but the tip is 3 mm less projected and the alar base 9 % wider |
| Celeste full | Narrowest ala, but sharp |
| 50/50 full | Rejected |
| 65/35 detail-only, k = 60 | Close, but kept some of the old rim |
| **65/35 detail-only, k = 120** | **Selected** |

All 29 MetaHuman Creator presets were read, and 10 were rendered (`data/explore_MHC_GD14_W.json`, board 14).

### 2. Detail separation for the whole face

D = sculpt − model is split into a low-pass part, LP(k = 30), and a high-frequency part, HF.

- **Kept:** every deliberate broad edit (zygoma band, cheek and maxilla support, brow shelter, lid hood mass, mouth width, bridge width, lower-face rhythm) plus 50 % of HF.
- **Kept at 100 %:** HF at the eyelids and the lip seam, so lid/globe and closed-mouth fit stay exact.
- **Removed:** the accumulated gaunt creases that made the clay read older and pinched (`tools/blender_gd14_detailsep.py`).

### 3. Face width judged on silhouette, not landmarks

The clay silhouette was drawn over the Tier A photo (`tools/blender_gd14_outline.py`, boards 04 and 19).

- **What it showed:** the remaining "narrow, vertical" read is the **lower cheek / buccal tissue at mouth level**, about 4 mm per side inside the Tier A outline. The zygoma is not the cause.
- **What I did:** widened that tissue with a wide-ramp field (`data/ops/D4.json`). The mandible border, chin and cranium are unchanged (max 0.35 mm).

### 4. Eyes judged in UE real, not clay

The clay renders hid how open the eyes are. The UE real render (iris visible) showed it clearly.

- **Edit:** upper lids rotated 6° down and lower lids 1.5° up about each eyeball centre. The lids stay on the globe and nothing pokes through.
- **Result:** eye-opening height/width went from 0.358 to 0.337; the reference is 0.345.
- **Cost:** it needed a **second auto-rig**. The first rig, K, was superseded by K2. Both are kept in the candidate folder.

### 5. Lip proportion remapped between the semantic border curves

Each lip vertex keeps its fractional position inside its band (upper border → stomion → lower border), and the bands were re-proportioned:

| Measure (centre) | Before | After |
|---|---|---|
| Upper vermilion | 6.1 mm | 7.6 mm |
| Lower vermilion | 11.8 mm | 10.0 mm |
| Upper/lower ratio | 0.68 | 1.00 (Tier A front 1.11) |

A cupid-peak lift was added, the seam stays closed, and the mouth corners are unchanged.

### 6. Henley neckline warp

The g17e neck edge is much wider and lower than its builder parameters:

| Point | g17e | g18p |
|---|---|---|
| HPS half-width | 12.5 cm | ~8 cm |
| V bottom (z) | 123 | 126 |

`tools/blender_gd14_neckline.py` remaps the ordered neck-edge chain on the same topology, so the weights and solved corrective morphs stay valid.

**Rejected first version (g18n):** it propagated the change over mesh topology and opened the front shoulder seams between the separately meshed panels. The 41 FULL FRONT board showed visible holes.

**Fixed version (g18p):** a spatial Shepard displacement field. Coincident seam vertices of different panels get one shared displacement, so seams cannot open; the worst remaining gap is 3 mm at the placket.

**Why not a full pattern rebuild:** the corrective re-solve pose captures (`g13s_*_front.json`) were removed by the capture cleanup.

## Face edits (K2 vs HS3)

| Area | Edit |
|---|---|
| Nose base | Model morphology transfer (see above) |
| Whole face | Detail separation (LP 30, HF 50 %) |
| Lower cheek | Up to +4.2 mm outward and +1.2 mm forward, wide ramps |
| Upper lid / lower lid | 6° down / 1.5° up about the eyeball |
| Lip vermilion | Re-proportioned, cupid peaks |
| Lower vermilion border, alar hook | Softened (`data/ops/E1.json`) |
| Untouched | Eyes, IPD, cranium, top arc, upper temple, jaw lower border and chin |

**Measurements** (`data/face_measurements.txt`, `data/image_ratios.json`, `data/tracker_real_ratios.json`):

| Measure | HS3 | K2 | Tier A |
|---|---|---|---|
| IPD (cm) | 5.951 | 5.951 (rig joints 5.932) | – |
| Bizygomatic (cm) | 14.34 | 14.34 | – |
| Midface width (cm) | 13.54 | 13.77 | – |
| Malar lateral x (cm) | 6.19 | 6.27 | – |
| Width at z 153.5, lower-cheek tissue (cm) | 10.01 | 10.72 | – |
| Radix / bridge width (cm) | 1.50 / 0.97 | 1.45 / 1.12 | – |
| Alar-base width (cm) | 3.08 | 3.11 | – |
| Mouth width (cm) | 5.32 | 5.31 | – |
| Mouth/IPD, clay curves | 0.853 | 0.853 | 0.855 |
| Mouth/IPD, UE real tracker | 0.830 (GD12C) | **0.818** | 0.855 |
| Eye opening h/w, clay | 0.358 | 0.337 | 0.345 |
| Eye opening h/w, real tracker | 0.352 (GD12C) | 0.328 | 0.345 |
| Upper/lower lip ratio | 0.68 | 1.00 | 1.11 |

**Joints vs GD12C G:**
- Eye-joint distance 5.904 → 5.932 cm.
- Mouth-corner width 4.698 → 4.703 cm.
- Cheek outer width 7.58 → 8.00 cm.
- 122 of 843 joints moved by more than 1 mm (`data/joint_comparison.json`).

## Hair h29

Builder: `tools/blender_gd14_hair.py`, the GD13 structural mode. Build env: `data/hair_h29_build_env.txt`.

**Structure:**
- Irregular multi-frequency top flow with bumpy amplitude envelopes.
- Per-mass cross sweep, so neighbouring masses overlap instead of running parallel.
- Occasional lifted locks.
- Single-direction twist-coil bun.

**Changes vs h24:**
- **Temple hairline:** the bald temple band of h23/h24 was caused by a raised side hairline plus side-front density 0.45, i.e. roots removed. The natural hairline is restored (z 165.6 / 163.0 / 161.3 / 160.9 / 161.6) at full density, with a softer edge ramp. Low side lift keeps it from becoming a wall.
- **Top:** lift 1.5 → 1.3, front lift 0.25, and a visible centre part.
- **Face framing:** asymmetric framing locks on both sides.
- **Rear:** lift 1.8 → 0.9 and stronger rear clumping; the bun is pushed back so it reads in profile (stand-off at 170° = 6.9 cm).
- **Colour:** melanin 0.60, redness 0.38, highlights 0.55 / 0.40, loose strands 0.66. Brown-first and muted; it may now read slightly too dark (board 34).

## Skin and wardrobe

- **Skin k12:** k11 with the lip region pulled 35 % toward a muted rose-brown luminance (`tools/blender_gd14_skin_lips.py`). k11 lips rendered too red and dark in UE. No other changes, and no wrinkles added.
- **Head/body seam (board 37):** it reads as one skin under studio, grazing, interior and gameplay light. The known faint collar line across the chest is still visible under grazing light (pre-existing).
- **Henley g18p (board 39):**
  - The neckline is higher and narrower, the placket starts higher, and the shoulders are intact.
  - Open issues: in a 45° bend the V bottom still crumples; the folds are still cleaner than real cotton; the material is unchanged (m1).
- **Shorts:** unchanged Chaos m1 (board 40).

## Verification

| Check | Result |
|---|---|
| Rig, board 48 | 23 rig cases (blink, single blinks, four gaze directions, brows, smile/frown, jaw, visemes, extreme) plus squint half/full, nose wrinkle, upper-lip raise, sneer, mouth stretch and wide smile. The new nose base survives all of them: no curl returns and no nostril inversion. |
| LOD, board 49 | Face LOD0–3 and full character LOD0–2 including groom. Identity holds to LOD3. |
| Restart, board 50 | Fresh editor reopen loads MHC, DNA (858 morphs, 8 LODs, DNAAssetUserData), h29 grooms and four bindings, Henley g18p, Shorts g16c, the k12 face and body MIs and the hair MI. Dirty packages before and after: none. After-restart captures match. |
| Zero-byte captures | 0 |
| Disk | 29 GB free at the end |

## Gates

| Gate | Result |
|---|---|
| FACE WIDTH / HEIGHT | PARTIAL |
| ZYGOMATIC | PARTIAL |
| MIDFACE | PARTIAL |
| EYES / ORBITS | PARTIAL |
| NOSE BRIDGE | PARTIAL |
| NOSE DORSUM | PARTIAL |
| NOSE BASE | PARTIAL |
| NOSTRILS | PASS |
| ALAR | PARTIAL |
| COLUMELLA | PARTIAL |
| MOUTH WIDTH | PARTIAL |
| UPPER LIP | PARTIAL |
| LOWER LIP | PARTIAL |
| PERIORAL | PARTIAL |
| JAW / CHIN | PASS |
| AGE | PASS |
| SKIN | PARTIAL |
| IDENTITY FRONT | PARTIAL |
| IDENTITY 3/4 | PARTIAL |
| IDENTITY PROFILE | FAIL |
| OVERALL FACE GATE | FAIL |
| HAIRLINE | PARTIAL |
| HAIR FLOW | PARTIAL |
| CROWN | PARTIAL |
| BUN | PARTIAL |
| REAR MASS | PARTIAL |
| HAIR COLOUR | PARTIAL |
| HAIR MATERIAL | PARTIAL |
| ARTIST-GRADE HAIR | FAIL |
| HENLEY | PARTIAL |
| SHORTS | PARTIAL |
| HEAD/BODY | PARTIAL |
| FULL CHARACTER | PARTIAL |
| RIG | PASS |
| LOD | PASS |
| RESTART | PASS |
| OVERALL CHARACTER LIKENESS GATE | FAIL |

### Honest read: same-woman test

**Clearly better than GD12C / GD13c:**
- **Nose base:** the nostrils are natural openings, with no curled rim, slit nostril or dark alar pocket, and they survive sneer and nose wrinkle.
- **Eyes:** the lids are heavier and the eye no longer reads as an open, generic MetaHuman eye.
- **Upper lip:** it has real volume.
- **Lower face:** the cheek tissue now fills the Tier A outline at mouth level.
- **Clay:** without the accumulated creases it reads less gaunt and more like a supported adult face.
- **Hair:** the temple band is gone, the hairline is natural and the bun reads in profile.
- **Henley:** the neckline is closer to a real henley.

**Not yet the same woman.** Tier A beside the character, without overlays, still reads as "same archetype":
- **Overall face:** Tier A's face is softer and wider through the whole lower half, with a fuller chin pad and lower-face fat. Ours is still more angular.
- **Midface in profile:** still flatter than Tier A suggests.
- **Brows:** they sit slightly higher and are straighter.
- **Mouth:** it still reads narrower in the real render (tracker 0.818 vs 0.855).
- **Hair:** still visibly procedural. The bun is a clean coil, the strand groups are regular, and the face-framing locks are combed ribbons rather than damp, stringy pieces, so ARTIST-GRADE HAIR = FAIL as the brief requires.
- **Henley:** the folds and material are still CG-clean.

**Single most valuable next correction:**
1. A hands-on sculpt of the lower-face fat distribution: chin pad, jowl-free lower cheek, and mouth corners about 1 mm wider.
2. Then one auto-rig.
3. Hand-authored primary locks and bun for the hair (an artist groom pass).

Further generator tuning will not make the hair artist-grade.

## Boards

`boards/` contains 01–50 as required:
- **Face:** 01–20.
- **Hair:** 21–35.
- **Full character:** 36–50.

PREVIOUS means GD13c HS3 for clay and GD12C G for UE; NEW means GD14 K2. Cameras and lights are identical throughout.
