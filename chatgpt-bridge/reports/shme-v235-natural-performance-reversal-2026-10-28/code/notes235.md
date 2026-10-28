# V2.35 working notes (2026-10-28)

Base: V2.34 production (Bridge d71d03d), verified state = PROBE235 (ABP DB vars, knobs) in a fresh editor 13:38. Lock owner v235.
Tools: Tools/SHME_V235_20261028 (diag235 first-broken-frame inspector, sheet235.ps1 time-stamped frame strips, gen235_rev, gen235_stop,
curves235, build235_dbs, probe235_*), folder Saved/Codex/SHME_V235_20261028.

## A. Reversal freeze - owner (j30_rel_3200 / j35_rev, production, fixed 30)
- First broken frame 5.17-5.87 s (forward jog -> S): clip SHM226_JogRev_F_B_P14 (DB PSD_SHM226_JogRevFwd, family 3), clip rate 1.0 (no
  clock hold, no re-selection), BOTH feet planted 0.64 s, pose speed 30-100 cm/s, arms in jog carriage = the visible freeze; the capsule
  goes 116 -> 0 -> 80 cm/s backward meanwhile.
- Class E (+ content B): no technical lock; the support exchange is missing in the CONTENT. gen225/226 plan: the capsule table (measured V2.24
  production) lingers < 40 cm/s for ~0.3 s after the zero crossing, and the first step of the new travel lands T_FIRST 0.40 s after the
  zero crossing (S hovers in a 0.6 s slow swing) -> tS 0.75-0.9 s.
- Counter-case (sound): low-speed B_F SHM231S_SlowRev (j30_slow 5.25 s) steps continuously.
- Fix (gen235_rev, 64 clips SHM235_JogRev_*, DBs PSD_SHM235_JogRevFwd / BwdX): designed capsule (brake 800 cm/s^2, push continues through
  zero at 550 / 650, no dwell) + S = catch / first step at the zero crossing (tS 0.28-0.57 s) + a planted S leaves at its natural toe-off
  + a touching-down S is redirected at once. Dry: foot error <= 6.1 cm, planted drift < 3 cm on all 64.
- In game (a1/a2 rv): F_B double support 0.64 s -> ~0.15 s, back-run 157 cm/s at 0.67 s after the request (prod 49); B_F hold 0.5 s gone.
  Worst slip 8.0 (no capture) / 16.2 (capture run, frame hitches dt 0.125) vs prod 5.9: the catch foot lands 12 cm off its clip spot =
  MM entry blend (warping / FootPlacement off change nothing: rvSW 9.8, rvOW 8.0, rvFP 8.6 elsewhere).
- First-use trap again: the first run after the DB build read DB None (vendor CP2 pivot) - discard the first run after a DB build.

## B. Abrupt stop - owner (j35_rev 10.2 s / j30_slow 7.5 s, SHM_A_CP2_Jog_Fwd_Stop via PSD_CP2_JogStop, CP distance matching)
- Clip (probe235_stopbody): root 357 cm/s constant to 0.8 s then 800 cm/s^2 to 0 at 1.33 s; in game the clip runs at rate 0.71 in the
  decel (capsule 390 cm/s^2). Brake step lands 55-63 cm ahead of the final root, apex 26.9 cm (knee-high 'march'), closing step leaves a
  41 cm stagger, then the lead foot is pulled 43 cm BACK at 1.55-1.8 s (post-stop correction step). Trunk straightens from the jog lean in
  0.15 s right at the MM entry (ct 0.43-0.6) = 'pop upright'; arms drop 1.0-1.2 s. IdleUpperW = 0 (idle layer not involved).
- gen235_stop r1 (in place, root / curves / distance timeline kept): final landings re-targeted to the final idle stance, correction step
  removed, forward-half swing apex capped, upper body smoothed 0.85-1.9 s. Game: march + correction gone, settle by +1.0 s; slip 14.2 at
  the closing step (left apex cap 13 -> 9 made it skim) -> r2: apex cap 15 (right only), trunk clock remap (half speed at 0.45 s).

## C. Release-repress at 60 FPS: route owner
- SHM_UpdateRouting `allowed`: cand 3 from family 2 needs FamilyTime > RouteMinHold -> V2.35 revOver (knob RevOverHard): a revCand request
  takes over a hard-turn episode at once; other holds unchanged.

## Performance reference (honest scope)
- No external video reference was inspected this turn. Style anchor = the project's own female Core Motion performance (af_Loco_* sources
  -> A_CT_Jog_Fwd / A_RB_Jog_Rear loops used by every new clip), measured: jog trunk lean ~8-10 deg (head 12-16 cm ahead of the pelvis),
  hand path +-30 cm fore-aft, pelvis bob 86-95 cm. New brake / catch / stop content is built FROM these loops (same arm carriage, same
  cadence) so the transitions stay the same person; the vendor CP2 stop was a different posture (upright 0.15 s after entry).
