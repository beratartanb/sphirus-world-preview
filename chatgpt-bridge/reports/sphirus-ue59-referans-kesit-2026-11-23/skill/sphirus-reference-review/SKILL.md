---
name: sphirus-reference-review
description: Use when user-supplied reference images, sheets or clips must steer SPHIRUS world, character, camera or atmosphere work in the existing Unreal project. Adapts the reference-to-game plugin (intake, per-reference authority, comparison, hashed evidence) to the Unreal workflow; never builds a browser game or Three.js prototype.
---
# Sphirus reference review (reference-to-game on Unreal)

Bridge between the `reference-to-game` plugin and the project skills. It adds a reference/evidence procedure; it replaces no rule.
`AGENTS.md`, `CLAUDE.md`, `sphirus-ue59-guardrails` and the current user request outrank it. Start game work with `sphirus-game-dev-director` as before.

## What is installed (checked 2026-11-23)
- Plugin `reference-to-game@reference-to-game` 0.1.0, commit `6a00e491f578bbfcbdba45f0c7bddf4693016e61`, project scope
  (`.claude/settings.json`), files in `~/.claude/plugins/cache/reference-to-game/reference-to-game/0.1.0/`.
- CLI: `skills/reference-to-game/scripts/r2g.py` in that folder. Run it with the engine Python
  (`C:/Program Files/Epic Games/UE_5.9/Engine/Binaries/ThirdParty/Python3/Win64/python.exe`) and
  `PYTHONPATH=Tools/R2G_20261123/deps` (Pillow lives there; the engine Python has none). No ffmpeg on this machine: `inspect` reads images only.
- The plugin's default profile is Three.js and it ships no Unreal generator. Use its intake, authority, comparison and evidence parts only.

## Where things live
- Cases: `Docs/ReferenceToGame/<case>/` (first one: `sphirus-slice-01`). Never run `r2g init` on the project root.
- Tools: `Tools/R2G_20261123/` (`tour2_r2g.sh` fixed-point player-camera stills, `rec_r2g.sh` input-driven recordings,
  `c_cam.py` / `c_atm.py` / `c_water.py` in-memory candidates, `unreal_source_manifest.py`, `sheet.py`).
- Raw captures: `Saved/UE59Work/r2g/`; reviewed copies go into the case `review/` folder.

## Procedure
1. **Verify the live project first** (engine, open map, pawn, camera owner, plugins) with a measure job; old reports are hints.
2. **Identify each image from its content**, give it an id, and write per-reference authority into `case.json` (what it governs and what it
   does not). A missing reference is recorded as missing; nothing is invented for it.
3. **Before captures**: `tour2_r2g.sh <tag> <views>` on the house map (real player camera, 1600x900, user save hash checked). Teleported
   stills prove framing and look only.
4. **Candidates in memory, one variable at a time** (`SHME_KIND=control`). Capture the same views. A candidate that shows no visible gain is
   reverted and written down as ruled out. Two attempts without progress: change the method or stop and report.
5. **Keep a change** only through the gated write path (`manifest233.py` backup, `SHME_KIND=write`), then relaunch after a compile job,
   read the values back and capture again on the saved and reopened state.
6. **Movement and camera behaviour** need a recording (`rec_r2g.sh`). Say what drove it: these runs inject key events and write the look
   rotation at a fixed 30 Hz step; they are not human or gamepad play, and a recording nobody watched is not visual acceptance.
7. **Evidence**: `unreal_source_manifest.py` writes hashes of the real Unreal files into the case `app/` folder, then `r2g freeze`, then
   `r2g evidence` per check. This records hashes and an author's notes. It is not an art-quality or playtest verdict.

## Owners this skill hands to
| Question | Owner skill |
|---|---|
| Framing, follow, collision, look priority | `sphirus-camera-direction`, `sphirus-character-camera`, `sphirus-camera-and-qa` |
| Gait, weight, turns, contact | `sphirus-natural-motion`, `sphirus-gasp-motion-lab`, `sphirus-biomechanics` |
| Face, body, hair, garments | `character-lookdev-costume-groom-art-direction`, `sphirus-metahuman-deformation` |
| Space, routes, reveals | `sphirus-level-art-direction` (its `references/reference-authority.md` stays the shared reference hierarchy) |
| Image mood, materials, light | `sphirus-visual-art-direction`, `sphirus-materials-lighting-rendering`, `sphirus-aaa-environment-polish` |
| Editor writes | `sphirus-safe-unreal-iteration`, `sphirus-mcp-operations` |

User-supplied case references rank above the game-study hierarchy in `reference-authority.md` only for the dimension the user gave them.

## Limits found on 2026-11-23
- `r2g freeze` fingerprints the four contract files plus `app/`. It does not read `.uasset` / `.umap`; the manifest in `app/` is the link.
- `r2g validate --release` needs all six checks signed. Leave a check pending when the evidence does not exist; do not sign to pass.
- The pond's white clipping toward the sun was not solved by water roughness, sun volumetric scattering, sun specular scale or
  murkiness (each alone, reverted). Do not repeat those four; the open lever is sun direction or canopy, which is a user decision.
