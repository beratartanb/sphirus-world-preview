# Validation selection matrix

Pick checks by *what changed* and *who shares the owner*. Unrun checks stay NOT_TESTED. Detailed protocols live in the linked owners.

| Change type | Technical checks | Acceptance / regression | Detailed protocol |
|---|---|---|---|
| Blueprint logic (any) | Compile affected BPs; open referencing assets; Output Log clean of new errors | Runtime path actually executed (PIE probe or log) | `ue-blueprint-cpp-debugging` |
| Movement / animation / IK / camera | Compile; PIE with actual possessed Pawn | Same start/input/camera before/after; ±90° turns, starts/stops, stairs, crouch, ladder; game-feel verdict | `sphirus-character-camera/references/verification.md` |
| Input | Mapping context active; physical KB/M and gamepad separately from injection | Rebinding, focus, no dead inputs | `ue-enhanced-input` |
| Interaction | Trace/overlap hit; prompt; cancel/interrupt; repeat | Alignment, hand/IK contact, camera, animation sync | `sphirus-interaction-traversal` |
| Environment composition/material | Save; dirty packages; no floating/buried assets; collision on routes | Matched BEFORE/AFTER, ±90°, lookback, 5–15 s traversal, delta tier | `sphirus-aaa-environment-polish` |
| Lighting / rendering / PP | Same exposure profile; shader compile complete | Values/focal hierarchy; temporal stability; no concealment by PP | `sphirus-materials-lighting-rendering` |
| VFX | Bounds, spawn caps, culling | Visible at gameplay distance only where intended; no orbs/spam | `sphirus-vfx-atmosphere-niagara` |
| Audio | Attenuation/concurrency | Indoor/outdoor transition; mix | `sphirus-audio-ambience` |
| Save/state | Save → quit → load; missing/corrupt save | State restored exactly; settings separate | `sphirus-save-state-progression` |
| Cinematic | Input lock/unlock; possession; camera restore | Skip mid-sequence; state after end | `sphirus-cinematics-sequencer` |
| Anything with runtime cost | Same poses/session conditions baseline vs after | Visual goal preserved | `sphirus-performance-profiling` |
| Release-sensitive | Package, cook log, Standalone | Smoke test packaged | `sphirus-build-packaging` |
| Environment publication | Bridge export success, 18 standard views inspected | Remote `chatgpt-bridge/latest/LATEST.json` run_id matches | `sphirus-editor-automation-mcp` |

Frame-rate-dependent motion: test at achieved (not requested) 30 and 60 FPS where relevant. Always record world, map, session freshness and camera provenance.
