# GUARDIAN-15b: lower-face rhythm (N2), one fresh auto-rig, real-render check

Date: 2026-10-03. Status: **STOP FOR USER REVIEW.** Nothing promoted.

**Not changed in this pass:**
- Hair h29, body, Henley g18p and shorts were not edited.
- Skin k12 was used for diagnostics only.
- The 1.2 mm medial eye set stayed locked (eyes not moved further, IPD not reduced again).
- The nose was not sculpted.

**Protected folders:** all 27 protected groups are byte-identical (`data/preservation_check.json`), including GD12 to GD14 and production.

## 1. N2 sculpt (before rig)

**Method** (`tools/blender_gd15_rhythm.py`): N2 = N1 plus a distributed vertical lower-face rhythm, a smooth dz(z) field rather than a chin drag:

| Region | Downward shift |
|---|---|
| Philtrum / upper lip | ~0.5 to 1.5 mm |
| Stomion / mouth | **2.0 mm** |
| Lower lip / labiomental | 1.45 to 1.25 mm |
| Chin pad | 0.75 to 0.45 mm |
| Menton | ~0.15 mm |
| Jaw border | 0 |

The field fades out laterally at |x| 3.0 to 4.8 cm, so cheeks, zygoma and the jaw angle are untouched.

**Why 2.0 mm, not 1.5 mm:** I tested both, at 1.5 and 2.0 mm (`hs/head_N2_s10`, `hs/head_N2_s133`). In the clay review the 1.5 mm variant still fell short on both Tier A overlays, so I used 2.0 mm.

| Clay review (pre-rig) | Tier A | N1 | N2 1.5 mm | **N2 2.0 mm** |
|---|---|---|---|---|
| Eye→stomion / IPD, front | 1.153 | 1.115 | 1.139 | **1.147** |
| Alar base→stomion / IPD, 3/4 | 0.830 | 0.781 | 0.809 | **0.819** |

| 3D (cm) | N1 | N2 |
|---|---|---|
| Eye→stomion | 6.61 | 6.80 |
| Subnasale→stomion (upper lip) | 1.90 | 2.09 |
| Stomion→menton (mouth→chin) | 4.38 | 4.24 |
| **Total lower face** (subnasale→menton) | 6.28 | 6.33 |
| Upper-lip / mouth→chin | 0.434 | 0.493 |
| Bizygomatic / mouth-level width / chin-pad width | 14.74 / 13.29 / 7.99 | unchanged |

**Movement check, N1 → N2:**

| Region | Max movement |
|---|---|
| Nose tip / alae / bridge | **0.00 mm** |
| Eyes, eye assembly and brow region | 0.00 mm |
| Jaw border | 0.00 mm |
| Cheek / zygoma | ≤0.13 mm |
| Nostril sill / subnasale junction (where the philtrum rhythm fades in) | ≤0.6 mm (mean 0.27 mm). This is flagged; the nose itself did not move. |

Boards: `A1` front, `A2` verified 33° 3/4, `A3` profile (Tier B aid), `A4` 50 % overlay (REFERENCE | N1 | N2).

## 2. One fresh auto-rig (N2)

**Steps:**
- B2 whole-rig import, then fit (align NONE), then `request_auto_rigging` (JOINTS_AND_BLEND_SHAPES), then DNA attached to `SKM_GD15_Face_n2`.
- Grooms re-bound to the new face in the GD15 folder only. The hair groom h29 itself is unchanged.
- The first capture run crashed the editor (a D3D12 `UniformBufferRHI` assert) after the rig was saved. I restarted the editor and redid the captures only; there was no second rig.

**Fit results:**
- Rig fit to the N2 sculpt: skin mean 0.17 mm (p99 1.85 mm). The mouth region was within 0.08 mm on average.
- Eye-joint IPD after rig: **5.689 cm** (GD14 K2: 5.928), so the full 1.2 mm per eye survived the rig.
- Eye→mouth joint height: +2.2 mm vs K2.

## 3. Real-render check

Measurements use the MetaHuman image tracker on both Tier A and the renders, in the same review frame (`data/real_ratios.json`, `data/brow_profile.json`). This is tracker vs tracker, so it is the fairest comparison.

| Real render | Tier A | GD14 K2 | **N2** |
|---|---|---|---|
| IPD px (same frame) | 172.8 | 182.0 (+5.3 %) | **174.7 (+1.1 %)** |
| Inner canthal / IPD | 0.538 | 0.570 | **0.552** |
| Mouth width / IPD, front | 0.855 | 0.816 | **0.857** |
| Mouth width / IPD, 3/4 | 0.853 | 0.818 | **0.858** |
| Eye→stomion / IPD, front | 1.153 | 1.129 | **1.206** (+4.6 %) |
| Eye→stomion / IPD, 3/4 | 1.461 | 1.297 | **1.385** (−5 %) |
| Eye opening (h/w), front | 0.345 | 0.323 | **0.327** |
| Eye opening (h/w), 3/4 | 0.427 | 0.407 | **0.407** |
| **Brow (groom) → eye centre / IPD, front** | **0.308** | 0.248 | **0.252** (−18 %) |
| Brow → eye centre / IPD, 3/4 (less reliable) | 0.376 | 0.188 | 0.198 |

### What the real render shows (boards R1 to R5)

- **Eye spacing: fixed.** The real-render IPD is now within 1 % of Tier A (K2 was 5 % wide). The inner-canthal gap is also closer. **Do not move the eyes inward any further:** the render doesn't call for it.
- **Mouth width: fixed.** 0.857 vs 0.855 front, 0.858 vs 0.853 in 3/4. The narrow-mouth impression from GD14 is gone.
- **Brow position with groom: the biggest remaining identity miss.**
  - The M_Natural brows sit low and straight, right on the orbital rim, and crowd the eye. That gives a stern, compressed eye area.
  - Tier A's brow sits clearly higher, with a soft arch and a visible upper-lid fold.
  - Measured: the brow→eye gap is about **18 % short** in front (≈3 mm at this scale).
  - GD15's −1.2 mm brow-band move went the wrong way. In clay that band looked high; with the groom it is low.
- **Eye opening:** our aperture is about 5 % flatter than Tier A in both views. Her eye reads rounder and more open under a higher brow; ours reads narrower and more almond.
- **Vertical rhythm: in range, but the two views disagree.**
  - Front: tracker-vs-tracker says eye→stomion is now 4.6 % long.
  - 3/4: it is 5 % short when normalised by IPD, and equal in absolute pixels (193.6 vs 192.5 px).
  - Pre-rig clay review: matched (1.147 vs 1.153).
  - Front evidence suggests the eye sits high, not that the mouth is low. In the same front frame, the Tier A brow and stomion line up with N2 within ~3 px, but the N2 eye centre sits ~8 px (~2.7 mm) higher. Two independent normalisations agree on ~3 mm: brow→eye short, eye→stomion long.
  - The 3/4 view does not confirm this, so I am **not** acting on it without your decision.
- **Mouth→chin / chin:** the chin moved only ~0.5 mm. In the overlays (R3) the chin outline stays inside the Tier A chin, with no long-chin effect. The tracker has no chin landmark, so the Tier A mouth→chin ratio is not measured numerically (NOT_TESTED as a number).
- **Lower lip (skin, out of scope):** the lower lip reads grey-violet in the real render (k12 lip map). Noted, not touched.
- **Same-woman likeness:**
  - Closer than GD14 K2: spacing, mouth width and lower-face rhythm now sit on Tier A in the overlays.
  - Not yet the same woman: the brow/eye band (low, straight brow over a narrow almond eye) is now the dominant "other woman" cue in front and 3/4.

### Rig test (boards R6, R7)

All 20 expressions behave cleanly in front and 3/4:
- Neutral, blink (both and single), brows up/down, frown and smile.
- Jaw open/left/right, mouth open, lips closed, cheek compress and extreme.
- Visemes EE/OO/MBP/W, and look left/up/down/right.

No tearing, teeth or tongue show-through, or lid gaps were seen. Smile and frown read natural; the low brow ridge is also visible in the bald rig captures.

## Gates

| Gate | Result |
|---|---|
| EYE SET LOCKED (1.2 mm kept, no further move) | PASS |
| EYE SPACING (real render) | PASS |
| MOUTH WIDTH (real render) | PASS |
| LOWER-FACE VERTICAL RHYTHM | PARTIAL: front +4.6 %, 3/4 −5 % / equal in px |
| MOUTH→CHIN / TOTAL LOWER-FACE HEIGHT | PARTIAL: 3D 6.28 → 6.33 cm, chin +0.5 mm; Tier A ratio NOT_TESTED numerically |
| BROW POSITION WITH GROOM | **FAIL**: brow→eye gap −18 % front |
| EYE OPENING | PARTIAL: 0.327 vs 0.345 |
| JAW / CHIN CENTRE / CHEEK / ZYGOMA PRESERVATION | PASS |
| K5 NOSE PRESERVATION | PASS (nose 0.00 mm; sill junction ≤0.6 mm flagged) |
| CRANIUM / UPPER TEMPLE | PASS |
| AUTO-RIG TECHNICAL (DNA, joints, fit) | PASS |
| RIG TEST (20 expressions, front + 3/4) | PASS (technical) |
| PROTECTED ASSETS (27 groups) | PASS |
| IDENTITY FRONT | PARTIAL |
| IDENTITY 3/4 | PARTIAL |
| OVERALL SAME-WOMAN GATE | FAIL (brow/eye band) |

## Decision needed (nothing applied)

1. **Brow/eye vertical band.** This is the main remaining lever. Options:
   - **(a) Recommended:** raise the brow skin band ~1.2 mm (undo GD15-F) and lower the eye assembly and lids ~1.5 mm, without moving them horizontally. The brow gap grows ~2.7 mm and eye→stomion shortens ~1.5 mm. Clay-test in front and 3/4 before any rig.
   - **(b)** Raise the brow only, by ~2–2.5 mm.
   - **(c)** Change the brow groom shape (higher/arched) instead of the face. This is a groom change, so it waits for your OK while hair is frozen.
2. **Keep the 2.0 mm rhythm.** No further lowering. If (a) is chosen, re-check whether the front still needs all 2.0 mm.
3. Then a slightly taller eye aperture (~+5 %), and one more rig.

## Boards (`boards/`)

| Board | Content |
|---|---|
| A1 / A2 / A3 | Pre-rig clay REFERENCE \| N1 \| N2: front, verified 33° 3/4, profile |
| A4 | Pre-rig 50 % overlay on Tier A: N1 / N2, front and 3/4 |
| R1 / R2 | Real render with groom REFERENCE \| GD14 K2 \| N2: front, 3/4 |
| R3 | Real-render 50 % overlay: K2 / N2, front and 3/4 |
| R4 | Eyes and brow with groom, close-up, front and 3/4 |
| R5 | Mouth and chin close-up, front and 3/4 |
| R6 / R7 | N2 rig test: 20 expressions front, 14 in 3/4 |
