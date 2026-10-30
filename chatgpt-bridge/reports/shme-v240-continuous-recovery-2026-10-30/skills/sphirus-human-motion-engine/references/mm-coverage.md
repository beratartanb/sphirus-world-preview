# Motion Matching coverage and transition quality (D)

Use before adding, re-keying, re-biasing or replacing locomotion clips, and whenever a transition "looks wrong". Engine
mechanics: `ue-animation-system` (references/motion-matching-and-warping.md); research sources:
`Saved/Codex/SHME_V28_20261015/research_sources.md` (Epic MM / Distance Matching / Pose Warping docs = DOCS_PAGE level).

## Inventory first (tool: `../scripts/clip_inventory.py`, editor job → inventory.json)
Per clip: path, family folder, skeleton, length, root entry / exit speed, distance, travel direction, facing change, support
foot at start / end, per-foot contact intervals, curves (distance / foot-lock), loop flag, database membership; per database:
members and tags; only databases referenced by the production ABPs, a chooser or the SHME component count.

## Classify every NEED (one of four — never from the file name)
| State | Evidence required |
|---|---|
| Suitable clip exists AND is used | in-game `mmdb/mmanim` (or CP ownership) shows it at the event and the contact / pose metrics pass |
| Suitable clip exists but is NOT selected | inventory shows a matching entry speed / support / direction; runtime shows another DB/clip → route conditions, chooser, cost bias, BranchIn range, interrupt mode |
| Clip exists but is unsuitable (motion / style) | it is selected but entry speed, support configuration, step length, dip or style mismatch is measured (e.g. relaxed walk stops enter at 170 cm/s, our walk is 132) |
| No suitable clip | no inventory entry covers the speed / support / direction / style combination → author (contact-authoring.md) or brief an asset |

## Coverage axes (check each, not just clip count)
movement type (start / stop / loop / pivot / turn-in-place / reversal / landing) × speed band (walk 132, jog 300, sprint 490 in
this project) × travel direction × facing change × support phase (which foot, early / late stance) × style family (Relaxed
sample, AAMS neutral, Core Motion, LB loops). The walk stop gap found in V2.8: every stop clip enters faster than the game walk
and none covers all support phases → 12 phase-matched clips generated from the production loop.

## Selection / transition quantities to measure (with the harness)
- Route conditions: read the literals in `Update_MotionMatching` (e.g. sprint DB only for Speed ≥ 380 and |Direction| ≤ 65,
  jog route takes Sprint below 380 — fixed in V2.7 by ABP members `SHM_SprintDBMinSpeed/DirMin/DirMax`).
- Hysteresis: time spent per family across a threshold (`turngait.py`); count re-selections within 0.3 s.
- Entry / exit: CP ownership start / end, clip time at entry (distance table vs elapsed), entry pose error vs the current pose.
- Distance curves: does the clip have one; is the clock a distance table, `AdvanceTimeByDistanceMatching` (play-rate clamped) or
  `DistanceMatchToTarget` (sets time directly, no clamp → any jump in predicted distance is a pop; research E4/A11).
- Play-rate and warping limits: stride / orientation warping ratios and their minimum root-motion speed thresholds (research E5);
  a clip played far outside its authored speed slides even when the family is "right".
- Bias sign: the docs disagree (debugging page vs database API); verify on a known case in the Rewind Debugger before relying
  on a bias direction.

## Failure examples
- "Animation family preserved" ≠ contact preserved: keeping the sprint DB down to 230 cm/s (V2.7) kept the family; check stride
  warping / mid-stance slip at those speeds before widening any window (V2.8: sprint mid-stance p90 ≈ 0, rare 39–52 cm events
  during 180° flicks remain open).
- A database edit without re-key serves a cached index (notify / tag changes are not in the DDC key) — re-key with a new tag.

## V2.10 entry-window control (verified 2026-10-16)
- A clip that is "used" can still be used WRONG: check the clip time at entry against the clip's phase table. Speed mismatch (vendor
  sprint turns 716 cm/s vs project 490) makes the search prefer the clip's slowest frames (mid-turn) and skip brake / plant.
- Narrowing the BranchIn notify is NOT an entry window: BranchIn sets the entry's sampling range, frames outside it are not indexed and
  the continuing pose is lost -> playback stops at the window edge.
- Use "Pose Search: Block Transition In" (UAnimNotifyState_PoseSearchBlockTransition, UE 5.8) on an OWNED copy over the frames that
  must not be entered (sprint 90 turns: [0.78 s, end]); continuing play through them stays allowed. Result: entry 0.77 s (brake onset),
  continuous play to the push-off. New notifies need a NEW / re-keyed database (PSD_SHM210_SprintCut).
- The first use of a database in an editor session builds its index: the selection is None for ~0.1-0.4 s (hitch, fake pops, wrong
  routes). Warm every database with one discarded run after an editor (re)start before measuring.

## V2.11 sprint push route (verified 2026-10-16)
- Re-acceleration toward sprint uses the relaxed run starts (PSD_RR_Start) through a gated route instead of the steady jog / sprint loops
  (MM enters the start clip at the matching speed: walk -> sprint 226 -> 385 cm/s at clip 0.43 -> 0.89 s).
- Trap: a straight-ahead start entered right after a redirect episode, while the chest is still 60-80 deg off the capsule, snaps the
  body in ~0.1 s (head pop 192 m/s2, v211f r_ms2). Gate the push >= 0.35 s after the episode (SHM211_PushRdCool) and cap it above the
  gait switch (420) so no single jog-loop frame sits between the push and the sprint loop.
- The C01R WalkToSprint / RunToSprint transitions (Chapter01Refinement/Sprint) are 206 -> 721 cm/s with 28-44 deg trunk lean: athletic
  content for another speed band; not used.

## V2.12 gait push content and cut-reversal candidate (verified 2026-10-17)
- Walk -> sprint push content: owned copies of AAMS M_Neutral_Transition_Walk_to_Sprint_{L,R}foot / Run_to_Sprint (PSD_SHM212_GaitPush) with
  the VENDOR entry windows (their BranchIn ranges: walk 1.01-1.45 s, run 0.56-0.81 s; vendor ExcludeFromDatabase / BlockTransition kept).
  From a 150 cm/s walk MM enters the last walking step (1.03 s) and plays the clip's own push: trunk lean rises progressively (max 12-13 deg
  per 0.1 s instead of the RR_Start mid-clip snap 16.5 deg / 0.1 s), sprint-loop entry on a planted foot (1-4 cm) when the push runs to
  490 (SHM211_PushMaxSpeed 485). Raw vendor drive = sprinter block start at runtime (lean 50 deg, pelvis -21 to -23 cm): the owned copies
  carry a posture bake (Tools/SHME_V212_20261017/v212_push_posture.py, single pass from the vendor source: 75 % of the trunk pitch above
  20 deg removed, pelvis raised toward 88 cm under a SMOOTHED leg-reach envelope - the per-frame clamp jumped 6 cm at toe-off - legs
  re-solved to the same feet, leg_guard on write) -> runtime 35.6-35.8 deg / 11.9-12.8 cm (V2.11 walk push 35 / 9.5, standing RR_Start
  37 / 16-17). Calibrate on the RUNTIME metric: during the push runtime lean ~ clip pelvis->spine_05 pitch + ~11 deg and the pelvis ~9 cm
  below the clip (inertia / lean layers); a clip-only target (pelvis->neck) under-corrected (first pass 40.5 deg at runtime).
- Do NOT route a STANDING sprint start into it: from ~200 cm/s inside the run start MM jumps to the walking step (trunk 20 -> 10 -> 50 deg,
  a second start). Route by push origin (PushWalk = push started at 110..210 cm/s; else the run starts).
- Support-phase gate tried (start the walk push only within 0.12 s after the SHM component's SupportSide change): delayed the push past the
  walk band or skipped it (v212i) - off (SHM212_PhaseGate 0). The entry slip stays 10-12 cm (RR_Start 7-13).
- Cut-reversal candidate (sprint right cut -> A before the cut push completes): the reversal bridge must SEARCH on its frame - inside an
  episode SHM_RedirectHold throttles MM searches to 0.25 s and Update_MotionMatching_PostSelection writes the still-playing pose's database
  back into CurrentSelectedDatabase (the frame-2 hold then locks the old database). SprintReversal_L/R hand MM backward pivots / rear runs
  first; a turn-only database (PSD_SHM212_CutRev_*: sprint 180 copies, entry in the brake phase) plays the brake/pivot/push but the vendor
  brake (727 -> 21 cm/s in 0.3 s, ~2400 cm/s2) does not match the capsule (~800 cm/s2 from 300 cm/s): stance feet slide 48-132 cm, and the
  push is cut when the episode ends (jog loop -> run start). Not promoted; missing: a 180 redirect authored at game speed, or capsule /
  root-motion coupling during the response.
