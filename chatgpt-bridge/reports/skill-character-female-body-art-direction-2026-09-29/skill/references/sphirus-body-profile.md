# SPHIRUS body profile

Project-specific reference for [../SKILL.md](../SKILL.md). Load it only for the SPHIRUS protagonist. The reusable skill
never carries these facts; this file never overrides `AGENTS.md`, `CLAUDE.md` or the current user request. Facts are
dated; the actual project (editor state > saved packages > dated evidence > this file) wins. Re-verify before relying on
a path or number.

## Accepted decisions (user-accepted, protected)

| Fact | Status / source |
|---|---|
| The user-created MetaHuman **face is final**. Never reconstruct or "improve" face identity during body work. | User decision |
| **B2 macro body proportions are accepted** (`/Game/Sphirus/CharacterLab/NativeBody_20260928/MH_B2_PendingNativeWorkflow`, never modify). | User decision; B2 validation evidence `Saved/Codex/CharacterNativeBodyB2Validation_20260928/` |
| Height ~173 cm (B2 validation: 173.27 cm, HeadScale unchanged). | Verified 2026-09-29 in the B2 validation report |
| Head/body balance accepted; hand size accepted. | User decision |
| Realistic adult female, **moderately active, not muscular**. | User brief |
| **SHCB** high-elevation shoulder system accepted: `upperarm_out` lateral support ≈ **+2.0 cm @150°, +3.0 cm @165°, +3.5 cm @180°** (≈⅓ of the medial helper collapse, helper stays medial of the joint). Must not be casually redesigned. | `Saved/Codex/CharacterShoulderFix_20260928/HighElevCorrective_20260929/public_report_shcb/README.md`; candidate `/Game/Sphirus/CharacterLab/ShoulderFix_20260928/HighElevCorrective/HelperFix/` |
| Face identity and the **head/body seam** are protected. The head mesh owns the upper trapezius/collar (seam ≈ z 140-143 cm, abs(x) ≤ 15 cm); shoulder/neck work must be solved on welded head+body with identical seam deltas. | Project memory, 2026-09-29 |
| Production character `/Game/MetaHumans/MH_MainCharacter/*` is not modified by candidate work. | CLAUDE.md |

## Current body state (dated 2026-09-29)

- **BR_Neutral** (procedural body-realism neutral morph, v5) on the isolated candidate
  `/Game/Sphirus/CharacterLab/BodyRealism_20260929/` (`SKM_BR_BodyMesh`, `SKM_BR_FaceMesh`). It is a **procedural
  foundation, not the final artist body**: ARTIST-GRADE = NO. It was built as a detail layer (low-pass subtracted) so
  circumferences/silhouette stay within ~±2 mm of B2.
- A safe **manual Blender sculpt round-trip package** exists: `Saved/Codex/BodyRealismArtist_20260929/` (HANDOFF.md,
  `Blender/SPH_BR_ArtistSculpt_20260929.blend`, PRISTINE copy, validator, exporter; tools in
  `Tools/CharacterArtistSculpt_20260929/`). Status at creation: waiting for the manual artist sculpt; after delivery the
  flow is validate → export `BR_ArtistNeutral` → isolated import → SHCB rebase → LOD propagation → QA → publish.
- Known data facts: the skeleton asset's reference pose is the generic MetaHuman base and does **not** match this body
  (elbow ~6 cm off): use the neutral-capture bind for body-space work. Runtime LOD pairing goes through LODSync; body
  LOD2+ carry no effective `upperarm_out` skinning, so helper effects must be baked into those LODs' morphs.

## Clothing direction

- User homewear direction: a **fitted-relaxed Henley + lounge shorts**.
- First outfit candidate built 2026-09-29: ivory Henley + charcoal drawstring trousers,
  `/Game/Sphirus/CharacterLab/Outfit_Home_20260929/` (not promoted; underarm opening at 165-180° elevation, engine LOD2
  poor; report `Saved/Codex/OutfitHome_20260929/REPORT.md`). Lounge shorts are not built yet; with shorts, thighs, knees
  and calves become primary reads and must be production quality.
- Rule from the outfit brief: never modify the body or SHCB to make clothes fit; fix the clothing.

## SPHIRUS body art direction

Target: naturally feminine, grounded, healthy, subtly attractive, realistic, capable, soft rather than muscular, an adult
mature body, not a glamour model.

Visual priorities (in order):
1. breast / ribcage realism
2. waist / abdomen soft-tissue realism
3. pelvis / hip structure
4. glute / glute-ham transition
5. thigh flow
6. back / scapular anatomy
7. arm realism
8. knee / elbow realism

Her fitted clothing should look good because the body underneath is coherent.

## Constraints on any SPHIRUS body task

- No git in the project: checkpoint before any asset/map mutation (`sphirus-source-control-asset-safety`); binary assets
  change only through the editor; work in isolated `/Game/Sphirus/CharacterLab/<task>/` candidates.
- Do not change accepted macro proportions, skeleton, face, SHCB, locomotion or animation assets unless explicitly asked.
- Deformation review must include the SHCB elevations (150/165/180°) and the head/body seam in those poses.
- Report PASS/PARTIAL/FAIL/NOT_TESTED per gate, ARTIST-GRADE honestly, and preservation hashes of protected assets.
- Evidence locations: `Saved/Codex/BodyRealism_20260929/`, `Saved/Codex/CharacterBodyAnatomy_20260927/`,
  `Saved/Codex/CharacterShoulderFix_20260928/`, `Saved/Codex/BodyRealismArtist_20260929/`.
