# GUARDIAN-4 — identity, large form, skin and hair pass

Date: 2026-10-02. Status: **STOPPED FOR USER REVIEW.** Nothing was promoted.

- **Baseline:** GUARDIAN-3 N7, which is still the read-only technical baseline.
- **Candidate:** the isolated folder `/Game/Sphirus/CharacterLab/CharacterGuardian4_20261002/`.
- **Protected folders were not modified:** `/Game/MetaHumans/MH_MainCharacter`, the GUARDIAN, GUARDIAN-2 and GUARDIAN-3 folders, and `MetaHumans/Common`. All 15 protected groups are byte-identical to the checkpoint (`data/preservation_check.json`).

## Final candidate (NEW)

| Part | Asset |
|---|---|
| Face | `Face/SKM_GD4_Face_e1`. New DNA from a fresh Epic auto-rig (`MHC/MHC_GD4_E1`, `MHC/DNA/MHC_GD4_E1_Head`), RigLogic, 858 morphs, 8 LODs, plugin face skeleton and ABPs. |
| Neutral geometry | `headE1` = N7 → Phase A (cranium + balanced jaw S2) → midface soft tissue (M1) → eye and mouth (E1). Ops are in `data/ops/`. |
| Skin | `Skin/MI_LK_Face_*_VT_g4k3` and `Skin/MI_GD4_Body_k3`. New 4K base colour and normal plus a 2K SRMF (`T_LK_Head_{BC,N,SRMF}_k3`). The same olive-beige tint is applied to face and body. |
| Hair | `Hair/GR_LK_Hair_{Main,Loose}_h2`. New hierarchical lock builder; bindings `Face/Bindings/GB_GD4_*_e1h2`. |
| Eyes | GUARDIAN-3 `MI_GD3_Eye{L,R}_e2`, referenced read-only. |
| Body / garments | Unchanged: B2 body and correctives, Henley g17e, Chaos shorts m1. |
| Reference expression | `Face/Diagnostics/AS_GD4_RefExpression`, a separate QA pose. Nothing is baked into the neutral. |

## What was done, in order

### Phase A: large form

**Cranium.** A new smooth `crown` shape op rounds the coronal vault without the corner that A2's `vault` op created. It also lowers the vertex and shortens the occiput. Temples were filled a little.

| Measure (cm) | N7 | NEW |
|---|---|---|
| Breadth at +6 above the eyes | 13.48 | 14.30 |
| Breadth at +8 above the eyes | 11.57 | 12.17 |
| Glabella to opisthocranion | 19.57 | 18.97 |
| Vertex above the eyes | 10.84 | 10.41 |

The UE clay cranium gate was run on S2 before going further: boards 01–03, plus `boards/cranium_gate_ue/`.

**Jaw and chin.**
- A2–A7 pushed one-sided mandibular narrowing (left side up to about 1 cm). The user **rejected A7 as overcorrected**; it stays rejected.
- The work was rolled back to R0 (cranium only).
- The subtle S1 was approved by the user as the jaw/chin baseline. It narrows the jaw symmetrically and adds only a small left balance that cancels N7's own left-wider jaw.
- S2 moves the chin further toward the centreline with a chin-only soft move, so the jaw-border paths stay equal. No one-sided skeletal push was used.
- Board 09 and `boards/jaw_review/` show the history.

### Midface (M1)

The left cheek fullness was reduced slightly more than the right, as soft tissue only. The 3/4 far-cheek silhouette overshoot dropped from 16.8 to 10.7 px. The mid and low cheek rows were kept within 1–2 % of Tier A.

### Phase B: features (E1)

- **Eyes:** the lateral canthi were lengthened following Tier A's mild natural asymmetry, applied at half strength. Aperture was not changed.
- **Mouth:** each corner moved out by 1.05 mm structurally, with a subtle corner drop.
- **Nose:** re-checked at the ~33° camera and left unchanged.

### Phase C: fresh auto-rig

S2 and E1 each got a new Epic auto-rig: joints and blend shapes, about 75 s, no cost or terms prompt, fit error 0.1 mm mean. DNA was attached and consolidated.
- 79 of 843 facial joints moved more than 1 mm vs N7.
- Eye-joint distance is 5.899 cm (N7: 5.89, so the gain is kept).
- Mouth-corner joints are 0.8 mm wider.

### Phase E: skin

The new generator `blender_gd4_skin.py` produces regional detail with **no wrinkles, bags or folds**.
- **Base colour:** sun exposure on the forehead, nose bridge and cheekbones; low- and mid-frequency pigment mottling; sparse sun spots; the grey-purple periorbital patch neutralised; lips muted.
- **Normal:** pores in three size classes with per-region density and size, neck ring folds flattened, and detail faded at the collar so the c14s seam shading is kept.
- **SRMF:** roughness and specular set per region, with pore cavities.

Three tint iterations were run (k1 → k3). The k1/k2 renders read orange and over-saturated in the mid-tones. An extreme-tint test proved the tint parameter works; k3 neutralises the result.

### Phase F: hair

`blender_gd4_hair.py` is a hierarchical lock rebuild, not an id21 tweak:
- 16 primary masses → 118 secondary locks → ~700 tertiary clumps;
- a root-free part band so the scalp shows at the centre part;
- an irregular hairline;
- a low irregular bun in which every secondary lock wraps its own loop;
- a brown-first auburn material with the ombre off and only faint, dark highlights.

The first build, h1, was too voluminous and nearly black, so it was rejected. h2 is the result.

### Phase G and verification

- The full rig test passes: 23 cases, no cornea penetration on blink.
- QA lighting A–E: studio, grazing, grazing-top, gameplay and interior.
- Full-character captures.
- Save → fresh editor restart → read-only reopen (`data/reopen_check.json`). Everything loads: DNA user data, 858 morphs, 8 LODs, MHC, expression, grooms (4 LODs), skin MIs and the four bindings. No package was dirty before or after.
- After-restart captures (board 30) show RigLogic working, hair, the full character and LOD2.

## Measurements

Units: IPD = Tier A front camera, measured from the eye midpoint; cm = project frame. L = character left (+x, image right). These numbers are diagnostics only; the boards decide.

| Measure | Tier A | N7 | NEW (E1) |
|---|---|---|---|
| Menton offset (front projection, IPD) | −0.062 | −0.092 | −0.001 |
| Menton offset from the nose midline (3D, cm) | – | −0.685 | −0.252 |
| Jaw contour L / R (IPD) | 0.543 / 0.641 | 0.727 / 0.669 | 0.671 / 0.635 |
| Lower cheek L / R (IPD) | 0.915 / 0.930 | 0.928 / 0.944 | 0.916 / 0.936 |
| Mid cheek L / R (IPD) | 0.970 / 0.985 | 0.985 / 0.998 | 0.984 / 0.998 |
| Upper cheek, ear-free (y > 4), L / R (IPD) | 1.014 / 1.074 | 1.084 / 1.091 | 1.069 / 1.067 |
| Jaw-border path menton → ramus, L / R (cm) | – | 17.81 / 16.29 | 16.39 / 16.32 |
| Gonion height below the eyes, L / R (cm) | – | 9.26 / 9.48 | 9.45 / 9.48 |
| Half-width 9.5 cm below the eyes, L / R (cm) | – | 4.80 / 4.76 | 4.40 / 4.49 |
| Eye fissure width L / R (IPD, front) | 0.469 / 0.451 | 0.444 / 0.444 | 0.466 / 0.454 |
| Eye joint distance (cm) | – | 5.89 | 5.90 |
| Mouth width (IPD, mesh curves) | 0.844 | 0.821 | 0.852 |
| Cranium breadth at +6 / +8 (cm) | – | 13.48 / 11.57 | 14.30 / 12.17 |

The jaw-contour difference in Tier A (L narrower) was deliberately **not** reproduced with skeletal asymmetry. Part of it is head rotation, perspective and lighting.

The gonion/mandible-length heuristic in `blender_gd4_asym.py` is noisy (E1: 4.76 / 5.26 cm). The robust jaw-border paths are the balance measure.

Full data: `data/*.txt`, `data/joint_comparison.json`.

## Final gates

| Gate | Result | Note |
|---|---|---|
| IDENTITY FRONT | PARTIAL | Cranium, jaw balance and fissures improved; still reads younger and fuller-faced than Tier A. |
| IDENTITY 3/4 | PARTIAL | Far cheek improved; nose tip and lips still rounder and fuller. |
| IDENTITY PROFILE | PARTIAL | Shorter occiput; profile checked against Tier B as an aid only. |
| CRANIUM | PASS | UE clay: no narrow-topped dome; rear and top read broader and rounder. |
| FOREHEAD / TEMPLES | PARTIAL | Wider at +4…+6; temple fill is modest. |
| EYE PLACEMENT | PASS | N7 gain kept (5.90 cm). |
| EYE SHAPE / ORBITS | PARTIAL | Fissures lengthened; brow groom and orbit read unchanged from GUARDIAN-3. |
| ZYGOMA / MIDFACE | PARTIAL | Ear-free upper cheek within 5 %; midface still slightly full. |
| NOSE | PARTIAL | Not changed this pass. |
| MOUTH | PARTIAL | Wider and slightly downturned; lips still fuller than Tier A. |
| LEFT JAW / CHIN ASYMMETRY | PASS | Balanced, subtle, chin near the centreline; A7 rejected. |
| JAW / CHIN OVERALL | PARTIAL | Narrower and balanced, but still a little wider and squarer than Tier A. |
| SKIN FORM | PARTIAL | No wrinkles, bags or folds, as required; reads younger than the reference. |
| SKIN TEXTURE | PARTIAL | Regional pores, mottling and sun spots; pores at a normal camera distance are similar to N7. |
| SKIN MATERIAL RESPONSE | PARTIAL | Matte cheeks; the nose reads too glossy in close-up (board 18); grazing-top is harsh. |
| HEAD / BODY SKIN SEAM | PARTIAL | Same tint ratio on face and body; a faint arc across the upper chest remains in studio and interior light (board 20). |
| HAIR FLOW | PARTIAL | Real lock hierarchy and copper-brown colour; front framing is still more symmetric and curlier than Tier A. |
| HAIRLINE | PARTIAL | The part shows scalp; the temple edge is still a little hard. |
| BUN | PARTIAL | Low and built from locks; reads larger and rounder than Tier B. |
| HAIR MATERIAL | PARTIAL | Brown-first auburn without ombre; crown flyaways still catch a bright rim light. |
| REFERENCE EXPRESSION | PARTIAL | Calm and serious QA pose on the new rig (board 21). |
| HEAD / NECK | PASS | adapt_neck fit; no gap or step at the weld in clay or real. |
| RIG | PASS | 23 cases, blink closure, gaze, visemes, extreme. |
| LOD | PASS | Face 8 LODs, groom 4 LODs, garment LODs. |
| RESTART | PASS | Fresh-editor reopen plus after-restart captures. |
| OVERALL FACE GATE | FAIL | Large form is clearly better, but the face does not yet read as the Tier A woman: age, soft-tissue fullness, nose and lips. |
| OVERALL CHARACTER LIKENESS GATE | FAIL | Same reason; hair and skin moved closer but are not accepted. |

Technical passes (rig, LOD, restart, preservation) are separate from visual and likeness acceptance.

## Boards

| Group | Boards |
|---|---|
| Cranium | 01 front, 02 3/4, 03 profile / top / back; `cranium_gate_ue/` (UE clay gate on S2) |
| Face clay and overlays | 04 clay front, 05 clay 3/4, 06 overlay front, 07 overlay 3/4 |
| Asymmetry and features | 08 mirrored split-face, 09 left jaw/chin, 10 eye placement, 11 eye shape, 12 zygoma/midface, 13 nose, 14 mouth, 15 jaw/chin |
| Rig | 16 new auto-rig joints |
| Skin and expression | 17 skin macro, 18 skin micro close-up, 19 skin lighting A–E, 20 head/body seam, 21 reference expression |
| Hair | 22 hair flow front/3/4, 23 hair side/back, 24 hairline close-up, 25 bun structure |
| Integration and persistence | 26 head/neck/body, 27 full character, 28 rig test, 29 LOD test, 30 after restart |

## Open issues and suggested next pass

1. Soft-tissue age read (cheek fat, nasolabial planes, jowl shape) without adding wrinkles. Nose tip and lip volume.
2. Nose specular is too high: SRMF nose roughness 0.05 → 0. Grazing-top contrast.
3. Chest seam arc: a body-side SRMF / normal blend band.
4. Hair: less symmetric face framing, a softer temple edge, a smaller bun, darker crown flyaways.
5. Eye MIs and brow groom placement for GUARDIAN-4 (currently GUARDIAN-3 e2 and SlightArch).

Tools are in `tools/`: the new GUARDIAN-4 scripts and the modified `blender_gd_shape.py`, which adds the `crown` op and the per-side `xscale`.
