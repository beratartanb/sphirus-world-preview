# V2.36 working notes (2026-10-28)

Base: V2.35 production (Bridge 742af76), lock owner v236, folder Saved/Codex/SHME_V236_20261028, tools Tools/SHME_V236_20261028.

## 1. Real motion reference (inspected, with time ranges)
Method: free Pexels stock videos loaded into a browser video element, frames drawn at fixed times into time-stamped contact sheets
(0.1-0.2 s steps). Sheets were inspected frame by frame; titles / thumbnails were NOT counted as inspected.

| Source (pexels.com/video/...) | Frames inspected | View | Use |
|---|---|---|---|
| a-woman-getting-tired-of-running-4763889 | 0-19 s @1 s, 3.6-7.5 s @0.1 s | front, normal speed | jog -> slow -> stop (4.3-5.6 s) |
| woman-taking-a-rest-on-her-workout-5029482 | 0-11.9 s @0.5 s, 5.8-9.0 s @0.1 s | front | stand -> restart into jog (7.4-8.4 s) |
| a-woman-takes-breath-and-stretches-after-jogging-3048882 | 0-26 s @1 s, 5.0-11.4 s @0.2 s | rear 3/4, SLOW MOTION | pose only (walk-jog slowing), timing not used |
| couple-doing-exercise-together-4859229 | 0-2.4 s @0.1 s | side (tracking, 2.5 s clip) | person passes the frame in 1 s: not usable |
| a-female-runner-resting-8520621, a-woman-jogging-in-the-beach-stops-...-3129402 | full overview | side / close | already bent over / close-up: not usable |

Limitation: no SIDE-view normal-speed stop of a woman jogging was found in the accessible free footage; the stop study is from the
front view (arms, trunk, head, step rhythm) - foot placement distances come from the project's own loop and the measured capsule.
Fatigue gestures (hands on knees, hand to face) in 4763889 / 5029482 are performance-specific and were ignored.

Motion design taken from the references:
- the stop from a relaxed jog is distributed over 2-3 shortening steps (~1.0-1.5 s), not one brake lunge;
- arms: the swing amplitude shrinks and the elbows open, the hands drop from chest to hip level over ~0.5 s (4763889 4.6-5.3 s) - not in
  one frame, not glued to the body;
- trunk: the chest rises (forward lean reduces) during the slow-down; the head stays level;
- final: feet near hip width, a small settle;
- restart (5029482 7.4-8.0 s): the trunk leans in and the hands rise into carriage WITH the first steps.

## 2. Stop owner (production)
Forward jog stop = ABP Update_MotionMatching K2Node_CallFunction_42 (literal PSD_CP2_JogStop) and K2Node_Select_3 (option 0) -> one vendor
clip SHM_A_CP2_Jog_Fwd_Stop entered at any time (ct 0.43-0.7), played at rate 0.71 in the decel; capsule = CMC brake 300 -> 0 at a constant
410 cm/s2 (0.73 s, 110 cm; identical at 30 / 60 FPS).
