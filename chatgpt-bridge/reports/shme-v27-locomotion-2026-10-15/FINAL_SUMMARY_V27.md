# V2.7 final: old (base = V2.6 production flags, V2.7 clip bakes + long walk loop already saved) -> new (c27 = V2.7 candidate), mean of 2 interleaved reps

| scenario | turn deg/s | turn lag s | turn lat g | cut 90% s | cut lat g | stop s | stop cm | start s | pops | worst | skate p90 | skate max |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| wfwd | - | - | - | - | - | 0.52 -> 0.51 | 34 -> 34 | 0.71 -> 0.73 | 0.0 -> 0.0 | 0 -> 0 | 1.6 -> 1.9 | 2.0 -> 2.5 |
| jfwd | - | - | - | - | - | 0.72 -> 0.70 | 115 -> 114 | 1.02 -> 0.97 | 2.5 -> 0.5 | 32 -> 16 | 2.5 -> 2.3 | 3.1 -> 3.4 |
| sfwd | - | - | - | - | - | 1.17 -> 1.17 | 296 -> 296 | 1.31 -> 1.31 | 2.5 -> 5.0 | 29 -> 35 | 2.6 -> 2.9 | 3.2 -> 3.5 |
| wst | - | - | - | - | - | 0.52 -> 0.51 | 33 -> 33 | 0.71 -> 0.73 | 0.0 -> 0.0 | 0 -> 0 | 3.3 -> 3.7 | 7.9 -> 5.2 |
| wstart | - | - | - | - | - | 0.48 -> 0.48 | 29 -> 29 | 0.75 -> 0.75 | 0.0 -> 0.0 | 0 -> 0 | 3.3 -> 3.5 | 8.1 -> 8.1 |
| stx | - | - | - | - | - | 0.52 -> 0.52 | 33 -> 33 | 0.70 -> 0.71 | 0.0 -> 0.0 | 0 -> 0 | 2.8 -> 2.7 | 4.3 -> 5.7 |
| st_walk | - | - | - | - | - | 0.52 -> 0.50 | 34 -> 33 | 0.70 -> 0.70 | 0.0 -> 0.0 | 0 -> 0 | 2.5 -> 2.5 | 4.1 -> 4.8 |
| st_jog | - | - | - | - | - | 0.75 -> 0.74 | 115 -> 115 | 0.99 -> 0.99 | 2.0 -> 1.5 | 26 -> 28 | 2.4 -> 2.8 | 3.5 -> 4.0 |
| st_sprint | - | - | - | - | - | 1.02 -> 1.03 | 258 -> 259 | 1.30 -> 1.31 | 6.0 -> 6.0 | 36 -> 33 | 3.5 -> 3.1 | 4.9 -> 6.5 |
| gait2 | - | - | - | - | - | 0.62 -> 0.62 | 74 -> 74 | 0.71 -> 0.72 | 2.5 -> 3.0 | 30 -> 33 | 3.0 -> 2.7 | 3.3 -> 3.3 |
| gait3 | - | - | - | - | - | 0.52 -> 0.52 | 33 -> 33 | 0.71 -> 0.72 | 2.0 -> 1.0 | 28 -> 28 | 2.6 -> 2.6 | 3.6 -> 4.3 |
| sd_jog | - | - | - | 0.78 -> 0.80 | 0.58 -> 0.56 | 0.76 -> 0.74 | 115 -> 114 | 1.01 -> 1.04 | 0.5 -> 1.0 | 13 -> 25 | 2.7 -> 2.6 | 5.6 -> 3.3 |
| sd_sprint | - | - | - | 0.86 -> 0.85 | 0.86 -> 0.85 | 1.17 -> 1.18 | 296 -> 297 | 1.30 -> 1.33 | 4.0 -> 6.5 | 31 -> 33 | 3.5 -> 3.4 | 4.2 -> 4.2 |
| jswap | - | - | - | 0.76 -> 0.77 | 0.86 -> 0.85 | 0.72 -> 0.63 | 105 -> 103 | 1.00 -> 0.97 | 1.0 -> 1.0 | 30 -> 30 | 2.9 -> 3.0 | 5.0 -> 3.3 |
| jrev | - | - | - | 0.75 -> 0.76 | 0.85 -> 0.84 | 0.73 -> 0.71 | 105 -> 105 | 1.01 -> 0.99 | 5.0 -> 5.5 | 38 -> 34 | 3.3 -> 3.5 | 4.9 -> 4.8 |
| ad_walk | - | - | - | 0.66 -> 0.66 | 0.47 -> 0.46 | 0.52 -> 0.54 | 33 -> 33 | 0.70 -> 0.73 | 1.5 -> 3.0 | 30 -> 40 | 3.5 -> 3.9 | 6.3 -> 6.5 |
| ad_jog | - | - | - | 0.75 -> 0.76 | 0.82 -> 0.81 | 0.74 -> 0.76 | 115 -> 115 | 0.98 -> 1.02 | 3.0 -> 4.0 | 38 -> 37 | 2.8 -> 2.7 | 4.8 -> 3.9 |
| ad_sprint | - | - | - | 0.80 -> 0.88 | 0.83 -> 0.94 | 1.17 -> 1.17 | 296 -> 296 | 1.30 -> 1.32 | 6.5 -> 6.0 | 39 -> 49 | 3.0 -> 3.7 | 4.0 -> 4.5 |
| mt_jog | 180 -> 177 | 0.85 -> 0.85 | 0.81 -> 0.79 | - | - | 0.76 -> 0.74 | 116 -> 114 | 1.00 -> 0.99 | 0.5 -> 1.0 | 14 -> 26 | 3.0 -> 3.3 | 4.3 -> 4.8 |
| mt_sprint | 194 -> 179 | 0.90 -> 0.88 | 1.01 -> 1.00 | - | - | 1.17 -> 1.17 | 296 -> 297 | 1.31 -> 1.31 | 7.0 -> 6.0 | 31 -> 34 | 3.7 -> 2.8 | 4.4 -> 3.7 |
| mtf_sprint | 296 -> 252 | 0.63 -> 0.64 | 0.97 -> 0.97 | - | - | 1.17 -> 1.18 | 296 -> 297 | 1.29 -> 1.31 | 16.0 -> 5.5 | 202 -> 98 | 2.9 -> 3.4 | 3.3 -> 4.0 |
| taps | - | - | - | - | - | 0.52 -> 0.51 | 34 -> 33 | 0.30 -> 0.30 | 0.5 -> 0.5 | 17 -> 16 | 7.1 -> 6.6 | 14.4 -> 15.4 |
| s10f10 | - | - | - | - | - | - | - | - | 0.0 -> 0.0 | 0 -> 0 | - | - |

pops total old 63.0 -> new 57.0

## V2.6 item metrics (raw tool lines, base r1 / r2 then c27 r1 / r2)

### start
```
== v27f_wfwd_base_r1
  start t  2.13 mv_walk_0_0    owned 0.67 s | rate StartEvalTime 1.02  TC_StartPoseTime 0.71 | v at hand-over 126 cm/s
== v27f_wfwd_base_r2
  start t  2.09 mv_walk_0_0    owned 0.70 s | rate StartEvalTime 1.02  TC_StartPoseTime 0.71 | v at hand-over 131 cm/s
== v27f_wfwd_c27_r1
  start t  2.14 mv_walk_0_0    owned 0.67 s | rate StartEvalTime 0.95  TC_StartPoseTime 0.68 | v at hand-over 128 cm/s
== v27f_wfwd_c27_r2
  start t  2.09 mv_walk_0_0    owned 0.69 s | rate StartEvalTime 1.03  TC_StartPoseTime 0.71 | v at hand-over 128 cm/s
== v27f_wst_base_r1
  start t  2.24 mv_walk_0_0    owned 0.58 s | rate StartEvalTime 0.89  TC_StartPoseTime 0.66 | v at hand-over 128 cm/s
  start t  6.57 mv_walk_0_2    owned 0.82 s | rate StartEvalTime 1.01  TC_StartPoseTime 0.72 | v at hand-over 132 cm/s
  start t 11.06 mv_walk_0_4    owned 0.83 s | rate StartEvalTime 1.02  TC_StartPoseTime 0.73 | v at hand-over 132 cm/s
  start t 15.56 mv_walk_0_6    owned 0.83 s | rate StartEvalTime 1.02  TC_StartPoseTime 0.73 | v at hand-over 132 cm/s
== v27f_wst_base_r2
  start t  2.09 mv_walk_0_0    owned 0.68 s | rate StartEvalTime 1.02  TC_StartPoseTime 0.71 | v at hand-over 125 cm/s
  start t  6.56 mv_walk_0_2    owned 0.81 s | rate StartEvalTime 1.02  TC_StartPoseTime 0.73 | v at hand-over 132 cm/s
  start t 11.08 mv_walk_0_4    owned 0.82 s | rate StartEvalTime 1.02  TC_StartPoseTime 0.73 | v at hand-over 132 cm/s
  start t 15.59 mv_walk_0_6    owned 0.81 s | rate StartEvalTime 1.02  TC_StartPoseTime 0.72 | v at hand-over 132 cm/s
== v27f_wst_c27_r1
  start t  2.26 mv_walk_0_0    owned 0.66 s | rate StartEvalTime 0.98  TC_StartPoseTime 0.7 | v at hand-over 125 cm/s
  start t  6.58 mv_walk_0_2    owned 0.81 s | rate StartEvalTime 1.02  TC_StartPoseTime 0.73 | v at hand-over 132 cm/s
  start t 11.07 mv_walk_0_4    owned 0.84 s | rate StartEvalTime 1.02  TC_StartPoseTime 0.73 | v at hand-over 132 cm/s
  start t 15.59 mv_walk_0_6    owned 0.81 s | rate StartEvalTime 1.02  TC_StartPoseTime 0.72 | v at hand-over 132 cm/s
== v27f_wst_c27_r2
  start t  2.08 mv_walk_0_0    owned 0.71 s | rate StartEvalTime 1.03  TC_StartPoseTime 0.72 | v at hand-over 132 cm/s
  start t  6.58 mv_walk_0_2    owned 0.83 s | rate StartEvalTime 1.02  TC_StartPoseTime 0.73 | v at hand-over 132 cm/s
  start t 11.07 mv_walk_0_4    owned 0.83 s | rate StartEvalTime 1.03  TC_StartPoseTime 0.73 | v at hand-over 132 cm/s
  start t 15.57 mv_walk_0_6    owned 0.84 s | rate StartEvalTime 1.03  TC_StartPoseTime 0.73 | v at hand-over 132 cm/s
== v27f_wstart_base_r1
  start t  2.09 mv_walk_0_0    owned 0.67 s | rate StartEvalTime 1.03  TC_StartPoseTime 0.71 | v at hand-over 124 cm/s
== v27f_wstart_base_r2
  start t  2.09 mv_walk_0_0    owned 0.69 s | rate StartEvalTime 1.04  TC_StartPoseTime 0.72 | v at hand-over 128 cm/s
== v27f_wstart_c27_r1
  start t  2.12 mv_walk_0_0    owned 0.67 s | rate StartEvalTime 0.99  TC_StartPoseTime 0.7 | v at hand-over 127 cm/s
== v27f_wstart_c27_r2
  start t  2.10 mv_walk_0_0    owned 0.70 s | rate StartEvalTime 1.02  TC_StartPoseTime 0.71 | v at hand-over 130 cm/s
== v27f_stx_base_r1
  start t  2.08 mv_walk_0_0    owned 0.70 s | rate StartEvalTime 1.03  TC_StartPoseTime 0.72 | v at hand-over 131 cm/s
  start t  7.58 mv_walk_0_2    owned 0.82 s | rate StartEvalTime 1.03  TC_StartPoseTime 0.73 | v at hand-over 132 cm/s
  start t 13.07 mv_walk_0_4    owned 0.82 s | rate StartEvalTime 1.03  TC_StartPoseTime 0.73 | v at hand-over 132 cm/s
== v27f_stx_base_r2
  start t  2.09 mv_walk_0_0    owned 0.68 s | rate StartEvalTime 1.0  TC_StartPoseTime 0.7 | v at hand-over 128 cm/s
  start t  7.58 mv_walk_0_2    owned 0.84 s | rate StartEvalTime 1.02  TC_StartPoseTime 0.73 | v at hand-over 132 cm/s
  start t 13.09 mv_walk_0_4    owned 0.82 s | rate StartEvalTime 1.03  TC_StartPoseTime 0.73 | v at hand-over 132 cm/s
== v27f_stx_c27_r1
  start t  2.08 mv_walk_0_0    owned 0.68 s | rate StartEvalTime 1.03  TC_StartPoseTime 0.71 | v at hand-over 127 cm/s
  start t  7.57 mv_walk_0_2    owned 0.83 s | rate StartEvalTime 1.02  TC_StartPoseTime 0.73 | v at hand-over 132 cm/s
  start t 13.06 mv_walk_0_4    owned 0.82 s | rate StartEvalTime 1.03  TC_StartPoseTime 0.73 | v at hand-over 132 cm/s
== v27f_stx_c27_r2
  start t  2.09 mv_walk_0_0    owned 0.70 s | rate StartEvalTime 1.04  TC_StartPoseTime 0.72 | v at hand-over 129 cm/s
  start t  7.57 mv_walk_0_2    owned 0.82 s | rate StartEvalTime 1.03  TC_StartPoseTime 0.73 | v at hand-over 132 cm/s
  start t 13.06 mv_walk_0_4    owned 0.83 s | rate StartEvalTime 1.03  TC_StartPoseTime 0.73 | v at hand-over 132 cm/s
== v27f_taps_base_r1
  start t  2.07 mv_walk_0_0    owned 0.09 s | rate StartEvalTime 1.88  TC_StartPoseTime 1.02 | v at hand-over 17 cm/s
  start t  3.69 mv_walk_0_2    owned 0.10 s | rate StartEvalTime 1.85  TC_StartPoseTime 1.02 | v at hand-over 18 cm/s
  start t  8.64 mv_walk_0_8    owned 0.81 s | rate StartEvalTime 1.02  TC_StartPoseTime 0.72 | v at hand-over 132 cm/s
  start t 12.12 mv_walk_0_10   owned 0.82 s | rate StartEvalTime 1.02  TC_StartPoseTime 0.73 | v at hand-over 132 cm/s
== v27f_taps_base_r2
  start t  2.13 mv_walk_rel_1  owned 0.03 s | rate StartEvalTime None  TC_StartPoseTime None | v at hand-over 12 cm/s
  start t  3.69 mv_walk_0_2    owned 0.10 s | rate StartEvalTime 1.83  TC_StartPoseTime 1.01 | v at hand-over 18 cm/s
  start t  8.65 mv_walk_0_8    owned 0.83 s | rate StartEvalTime 1.02  TC_StartPoseTime 0.73 | v at hand-over 132 cm/s
  start t 12.15 mv_walk_0_10   owned 0.81 s | rate StartEvalTime 1.02  TC_StartPoseTime 0.73 | v at hand-over 132 cm/s
== v27f_taps_c27_r1
  start t  2.11 mv_walk_0_0    owned 0.08 s | rate StartEvalTime 2.0  TC_StartPoseTime 1.08 | v at hand-over 16 cm/s
  start t  3.70 mv_walk_0_2    owned 0.10 s | rate StartEvalTime 1.73  TC_StartPoseTime 0.97 | v at hand-over 19 cm/s
  start t  8.65 mv_walk_0_8    owned 0.82 s | rate StartEvalTime 1.01  TC_StartPoseTime 0.72 | v at hand-over 132 cm/s
  start t 12.14 mv_walk_0_10   owned 0.82 s | rate StartEvalTime 1.02  TC_StartPoseTime 0.73 | v at hand-over 132 cm/s
== v27f_taps_c27_r2
  start t  2.10 mv_walk_0_0    owned 0.07 s | rate StartEvalTime 2.21  TC_StartPoseTime 1.17 | v at hand-over 14 cm/s
  start t  3.70 mv_walk_0_2    owned 0.10 s | rate StartEvalTime 1.8  TC_StartPoseTime 0.99 | v at hand-over 18 cm/s
  start t  8.64 mv_walk_0_8    owned 0.84 s | rate StartEvalTime 1.02  TC_StartPoseTime 0.73 | v at hand-over 132 cm/s
  start t 12.13 mv_walk_0_10   owned 0.82 s | rate StartEvalTime 1.02  TC_StartPoseTime 0.73 | v at hand-over 132 cm/s
== v27f_gait2_base_r1
  start t  2.10 mv_walk_0_0    owned 0.67 s | rate StartEvalTime 0.97  TC_StartPoseTime 0.69 | v at hand-over 126 cm/s
  start t 13.58 mv_walk_0_2    owned 0.82 s | rate StartEvalTime 1.03  TC_StartPoseTime 0.73 | v at hand-over 132 cm/s
== v27f_gait2_base_r2
  start t  2.13 mv_walk_0_0    owned 0.67 s | rate StartEvalTime 0.99  TC_StartPoseTime 0.7 | v at hand-over 128 cm/s
  start t 13.58 mv_walk_0_2    owned 0.84 s | rate StartEvalTime 1.03  TC_StartPoseTime 0.73 | v at hand-over 132 cm/s
== v27f_gait2_c27_r1
  start t  2.09 mv_walk_0_0    owned 0.69 s | rate StartEvalTime 1.02  TC_StartPoseTime 0.71 | v at hand-over 129 cm/s
  start t 13.58 mv_walk_0_2    owned 0.85 s | rate StartEvalTime 1.03  TC_StartPoseTime 0.73 | v at hand-over 132 cm/s
== v27f_gait2_c27_r2
  start t  2.12 mv_walk_0_0    owned 0.68 s | rate StartEvalTime 0.92  TC_StartPoseTime 0.67 | v at hand-over 132 cm/s
  start t 13.57 mv_walk_0_2    owned 0.84 s | rate StartEvalTime 1.03  TC_StartPoseTime 0.73 | v at hand-over 132 cm/s
```

### stop
```
== v27f_wfwd_base_r1
  stop t 12.03 v0  132 | head fwd excursion +5.9 / -1.2 cm | walk-stand +2.1 cm overshoot +3.8 cm | lean peak +5.4 deg (final +11.4 walk +13.5, overshoot +3.3) | pelvis drop 8.3 cm | settle 1.52 s
== v27f_wfwd_base_r2
  stop t 12.01 v0  132 | head fwd excursion +5.9 / -1.1 cm | walk-stand +2.2 cm overshoot +3.7 cm | lean peak +5.2 deg (final +11.3 walk +13.5, overshoot +3.1) | pelvis drop 8.2 cm | settle 1.52 s
== v27f_wfwd_c27_r1
  stop t 12.01 v0  132 | head fwd excursion +5.9 / -1.2 cm | walk-stand +2.1 cm overshoot +3.8 cm | lean peak +5.3 deg (final +11.4 walk +13.5, overshoot +3.2) | pelvis drop 8.3 cm | settle 1.54 s
== v27f_wfwd_c27_r2
  stop t 12.02 v0  132 | head fwd excursion +5.9 / -1.2 cm | walk-stand +2.1 cm overshoot +3.8 cm | lean peak +4.9 deg (final +11.4 walk +13.4, overshoot +2.8) | pelvis drop 8.1 cm | settle 1.5 s
== v27f_wst_base_r1
  stop t  4.53 v0  132 | head fwd excursion +2.0 / -9.6 cm | walk-stand -4.9 cm overshoot +2.0 cm | lean peak +3.0 deg (final +14.9 walk +15.1, overshoot +2.8) | pelvis drop 6.9 cm | settle None s
  stop t  9.03 v0  132 | head fwd excursion +1.8 / -13.1 cm | walk-stand -5.9 cm overshoot +1.8 cm | lean peak +2.8 deg (final +15.2 walk +14.1, overshoot +2.8) | pelvis drop 6.4 cm | settle None s
  stop t 13.52 v0  132 | head fwd excursion +2.3 / -11.7 cm | walk-stand -5.6 cm overshoot +2.3 cm | lean peak +2.9 deg (final +14.7 walk +14.0, overshoot +2.9) | pelvis drop 6.6 cm | settle None s
  stop t 18.00 v0  132 | head fwd excursion +8.9 / -0.2 cm | walk-stand +6.3 cm overshoot +2.6 cm | lean peak +4.2 deg (final +11.1 walk +13.6, overshoot +1.7) | pelvis drop 7.2 cm | settle 1.56 s
== v27f_wst_base_r2
  stop t  4.51 v0  132 | head fwd excursion +2.3 / -9.2 cm | walk-stand -5.5 cm overshoot +2.3 cm | lean peak +3.0 deg (final +14.5 walk +14.1, overshoot +3.0) | pelvis drop 6.7 cm | settle None s
  stop t  9.00 v0  132 | head fwd excursion +3.2 / -10.6 cm | walk-stand -4.3 cm overshoot +3.2 cm | lean peak +3.1 deg (final +14.1 walk +13.8, overshoot +3.1) | pelvis drop 6.7 cm | settle 2.48 s
  stop t 13.51 v0  132 | head fwd excursion +3.2 / -10.3 cm | walk-stand -4.7 cm overshoot +3.2 cm | lean peak +3.1 deg (final +14.3 walk +13.8, overshoot +3.1) | pelvis drop 6.8 cm | settle 2.45 s
  stop t 18.03 v0  132 | head fwd excursion +9.2 / -0.2 cm | walk-stand +6.7 cm overshoot +2.5 cm | lean peak +4.3 deg (final +11.0 walk +13.8, overshoot +1.5) | pelvis drop 7.4 cm | settle 1.53 s
== v27f_wst_c27_r1
  stop t  4.52 v0  132 | head fwd excursion +2.1 / -9.3 cm | walk-stand -4.8 cm overshoot +2.1 cm | lean peak +3.0 deg (final +14.7 walk +14.4, overshoot +3.0) | pelvis drop 7.5 cm | settle None s
  stop t  9.01 v0  132 | head fwd excursion +2.5 / -11.7 cm | walk-stand -5.1 cm overshoot +2.5 cm | lean peak +2.9 deg (final +14.6 walk +13.9, overshoot +2.9) | pelvis drop 7.0 cm | settle 2.45 s
  stop t 13.51 v0  132 | head fwd excursion +3.2 / -10.4 cm | walk-stand -4.7 cm overshoot +3.2 cm | lean peak +3.0 deg (final +14.3 walk +13.9, overshoot +3.0) | pelvis drop 6.7 cm | settle 2.47 s
  stop t 18.00 v0  132 | head fwd excursion +8.9 / -0.2 cm | walk-stand +6.5 cm overshoot +2.4 cm | lean peak +4.3 deg (final +11.1 walk +13.7, overshoot +1.7) | pelvis drop 7.7 cm | settle 1.53 s
== v27f_wst_c27_r2
  stop t  4.52 v0  132 | head fwd excursion +2.3 / -9.2 cm | walk-stand -4.4 cm overshoot +2.3 cm | lean peak +2.9 deg (final +14.4 walk +15.2, overshoot +2.2) | pelvis drop 6.9 cm | settle 2.45 s
  stop t  9.03 v0  132 | head fwd excursion +1.9 / -12.5 cm | walk-stand -5.8 cm overshoot +1.9 cm | lean peak +2.9 deg (final +15.0 walk +13.9, overshoot +2.9) | pelvis drop 6.7 cm | settle None s
  stop t 13.52 v0  132 | head fwd excursion +2.4 / -11.1 cm | walk-stand -5.5 cm overshoot +2.4 cm | lean peak +3.0 deg (final +14.7 walk +14.0, overshoot +3.0) | pelvis drop 6.8 cm | settle None s
  stop t 18.02 v0  132 | head fwd excursion +9.2 / -0.2 cm | walk-stand +6.5 cm overshoot +2.6 cm | lean peak +4.4 deg (final +11.0 walk +13.9, overshoot +1.4) | pelvis drop 7.1 cm | settle 1.51 s
== v27f_stx_base_r1
  stop t  5.03 v0  132 | head fwd excursion +8.1 / -1.2 cm | walk-stand +6.1 cm overshoot +2.0 cm | lean peak +4.0 deg (final +11.3 walk +14.6, overshoot +0.7) | pelvis drop 6.7 cm | settle 1.53 s
  stop t 10.51 v0  132 | head fwd excursion +4.3 / -1.5 cm | walk-stand +0.7 cm overshoot +3.6 cm | lean peak +3.4 deg (final +12.1 walk +13.7, overshoot +1.8) | pelvis drop 8.1 cm | settle 1.52 s
  stop t 16.02 v0  132 | head fwd excursion +7.4 / -0.0 cm | walk-stand +4.1 cm overshoot +3.3 cm | lean peak +4.6 deg (final +10.3 walk +13.8, overshoot +1.1) | pelvis drop 7.8 cm | settle 1.5 s
== v27f_stx_base_r2
  stop t  5.01 v0  132 | head fwd excursion +8.4 / -1.3 cm | walk-stand +6.4 cm overshoot +2.0 cm | lean peak +4.0 deg (final +11.3 walk +14.5, overshoot +0.9) | pelvis drop 6.9 cm | settle 1.6 s
  stop t 10.50 v0  132 | head fwd excursion +4.3 / -1.6 cm | walk-stand +0.7 cm overshoot +3.6 cm | lean peak +3.4 deg (final +12.1 walk +13.7, overshoot +1.8) | pelvis drop 8.1 cm | settle 1.53 s
  stop t 16.01 v0  132 | head fwd excursion +7.3 / -0.0 cm | walk-stand +4.0 cm overshoot +3.3 cm | lean peak +5.4 deg (final +10.2 walk +13.7, overshoot +1.9) | pelvis drop 8.1 cm | settle 1.52 s
== v27f_stx_c27_r1
  stop t  5.01 v0  132 | head fwd excursion +8.4 / -1.3 cm | walk-stand +6.4 cm overshoot +2.0 cm | lean peak +4.0 deg (final +11.4 walk +14.7, overshoot +0.6) | pelvis drop 6.9 cm | settle 1.54 s
  stop t 10.52 v0  132 | head fwd excursion +4.4 / -1.4 cm | walk-stand +1.0 cm overshoot +3.4 cm | lean peak +2.9 deg (final +12.0 walk +14.4, overshoot +0.5) | pelvis drop 7.8 cm | settle 1.54 s
  stop t 16.02 v0  132 | head fwd excursion +7.3 / -0.0 cm | walk-stand +4.0 cm overshoot +3.3 cm | lean peak +4.8 deg (final +10.3 walk +13.7, overshoot +1.3) | pelvis drop 7.9 cm | settle 1.48 s
== v27f_stx_c27_r2
  stop t  5.00 v0  132 | head fwd excursion +8.4 / -1.2 cm | walk-stand +6.3 cm overshoot +2.1 cm | lean peak +3.9 deg (final +11.4 walk +14.5, overshoot +0.8) | pelvis drop 7.0 cm | settle 1.54 s
  stop t 10.52 v0  132 | head fwd excursion +4.4 / -1.5 cm | walk-stand +0.8 cm overshoot +3.6 cm | lean peak +2.9 deg (final +12.1 walk +13.7, overshoot +1.2) | pelvis drop 7.9 cm | settle 1.53 s
  stop t 16.01 v0  132 | head fwd excursion +7.3 / -0.0 cm | walk-stand +4.0 cm overshoot +3.3 cm | lean peak +4.7 deg (final +10.3 walk +13.8, overshoot +1.2) | pelvis drop 8.1 cm | settle 1.48 s
== v27f_st_walk_base_r1
  stop t  5.00 v0  132 | head fwd excursion +8.0 / -5.2 cm | walk-stand +1.8 cm overshoot +6.2 cm | lean peak +3.5 deg (final +11.8 walk +14.4, overshoot +1.0) | pelvis drop 5.8 cm | settle None s
  stop t 10.21 v0  132 | head fwd excursion +5.0 / -4.0 cm | walk-stand -1.7 cm overshoot +5.0 cm | lean peak +3.4 deg (final +12.1 walk +13.7, overshoot +1.8) | pelvis drop 6.7 cm | settle None s
  stop t 15.42 v0  132 | head fwd excursion +6.9 / -0.4 cm | walk-stand +3.2 cm overshoot +3.7 cm | lean peak +4.1 deg (final +11.0 walk +12.9, overshoot +2.2) | pelvis drop 8.0 cm | settle 1.53 s
== v27f_st_walk_base_r2
  stop t  5.02 v0  132 | head fwd excursion +7.8 / -6.5 cm | walk-stand +1.1 cm overshoot +6.6 cm | lean peak +3.2 deg (final +12.1 walk +14.8, overshoot +0.5) | pelvis drop 5.1 cm | settle None s
  stop t 10.20 v0  132 | head fwd excursion +5.1 / -4.0 cm | walk-stand -1.6 cm overshoot +5.1 cm | lean peak +3.2 deg (final +12.1 walk +13.7, overshoot +1.5) | pelvis drop 6.5 cm | settle None s
  stop t 15.42 v0  132 | head fwd excursion +6.7 / -0.4 cm | walk-stand +3.0 cm overshoot +3.6 cm | lean peak +3.8 deg (final +11.2 walk +13.7, overshoot +1.2) | pelvis drop 7.9 cm | settle 1.51 s
== v27f_st_walk_c27_r1
  stop t  5.01 v0  132 | head fwd excursion +8.5 / -5.5 cm | walk-stand +2.0 cm overshoot +6.4 cm | lean peak +3.4 deg (final +11.9 walk +14.5, overshoot +0.8) | pelvis drop 5.5 cm | settle None s
  stop t 10.23 v0  132 | head fwd excursion +4.8 / -4.6 cm | walk-stand -2.2 cm overshoot +4.8 cm | lean peak +2.7 deg (final +12.3 walk +13.7, overshoot +1.3) | pelvis drop 6.6 cm | settle None s
  stop t 15.43 v0  132 | head fwd excursion +6.8 / -0.3 cm | walk-stand +3.2 cm overshoot +3.6 cm | lean peak +3.9 deg (final +11.0 walk +13.8, overshoot +1.2) | pelvis drop 7.9 cm | settle 1.5 s
== v27f_st_walk_c27_r2
  stop t  5.00 v0  132 | head fwd excursion +8.4 / -5.4 cm | walk-stand +2.1 cm overshoot +6.2 cm | lean peak +3.5 deg (final +11.8 walk +14.4, overshoot +0.8) | pelvis drop 5.7 cm | settle None s
  stop t 10.21 v0  132 | head fwd excursion +5.0 / -4.0 cm | walk-stand -1.6 cm overshoot +5.0 cm | lean peak +3.0 deg (final +12.2 walk +13.7, overshoot +1.4) | pelvis drop 6.7 cm | settle None s
  stop t 15.41 v0  132 | head fwd excursion +6.9 / -0.4 cm | walk-stand +3.2 cm overshoot +3.6 cm | lean peak +4.2 deg (final +11.0 walk +13.7, overshoot +1.5) | pelvis drop 8.1 cm | settle 1.55 s
== v27f_st_jog_base_r1
  stop t  5.00 v0  300 | head fwd excursion +14.3 / -2.3 cm | walk-stand +11.2 cm overshoot +3.1 cm | lean peak +11.7 deg (final +13.6 walk +21.5, overshoot +3.8) | pelvis drop 11.7 cm | settle None s
  stop t 10.21 v0  300 | head fwd excursion +16.4 / -1.4 cm | walk-stand +10.9 cm overshoot +5.5 cm | lean peak +11.3 deg (final +13.7 walk +21.5, overshoot +3.5) | pelvis drop 11.1 cm | settle None s
  stop t 15.42 v0  300 | head fwd excursion +15.0 / -1.9 cm | walk-stand +11.0 cm overshoot +4.0 cm | lean peak +11.2 deg (final +13.9 walk +21.5, overshoot +3.6) | pelvis drop 11.4 cm | settle 1.8 s
== v27f_st_jog_base_r2
  stop t  5.02 v0  300 | head fwd excursion +13.8 / -2.3 cm | walk-stand +10.9 cm overshoot +2.9 cm | lean peak +11.2 deg (final +14.1 walk +21.6, overshoot +3.7) | pelvis drop 11.6 cm | settle None s
  stop t 10.21 v0  300 | head fwd excursion +16.0 / -1.5 cm | walk-stand +13.9 cm overshoot +2.0 cm | lean peak +11.3 deg (final +13.8 walk +23.6, overshoot +1.6) | pelvis drop 11.4 cm | settle None s
  stop t 15.41 v0  300 | head fwd excursion +14.2 / -2.2 cm | walk-stand +11.3 cm overshoot +3.0 cm | lean peak +11.8 deg (final +13.6 walk +21.5, overshoot +3.9) | pelvis drop 12.1 cm | settle 1.87 s
== v27f_st_jog_c27_r1
  stop t  5.03 v0  300 | head fwd excursion +14.6 / -2.8 cm | walk-stand +10.1 cm overshoot +4.5 cm | lean peak +10.9 deg (final +14.0 walk +21.4, overshoot +3.5) | pelvis drop 11.1 cm | settle None s
  stop t 10.20 v0  300 | head fwd excursion +15.7 / -1.4 cm | walk-stand +11.1 cm overshoot +4.6 cm | lean peak +12.0 deg (final +13.3 walk +21.5, overshoot +3.8) | pelvis drop 11.8 cm | settle None s
  stop t 15.41 v0  300 | head fwd excursion +15.0 / -2.2 cm | walk-stand +11.2 cm overshoot +3.8 cm | lean peak +11.6 deg (final +13.6 walk +21.6, overshoot +3.6) | pelvis drop 11.7 cm | settle 1.83 s
== v27f_st_jog_c27_r2
  stop t  5.02 v0  300 | head fwd excursion +14.2 / -2.2 cm | walk-stand +11.1 cm overshoot +3.1 cm | lean peak +11.8 deg (final +13.5 walk +21.5, overshoot +3.9) | pelvis drop 12.0 cm | settle None s
  stop t 10.21 v0  300 | head fwd excursion +15.7 / -1.4 cm | walk-stand +11.2 cm overshoot +4.5 cm | lean peak +11.9 deg (final +13.4 walk +21.4, overshoot +3.8) | pelvis drop 11.9 cm | settle None s
  stop t 15.41 v0  300 | head fwd excursion +14.7 / -2.0 cm | walk-stand +10.8 cm overshoot +3.8 cm | lean peak +11.3 deg (final +13.8 walk +21.4, overshoot +3.7) | pelvis drop 11.4 cm | settle 1.81 s
== v27f_st_sprint_base_r1
  stop t  5.02 v0  490 | head fwd excursion +18.7 / -3.9 cm | walk-stand +20.3 cm overshoot -1.6 cm | lean peak +29.5 deg (final +15.2 walk +39.4, overshoot +5.4) | pelvis drop 12.2 cm | settle None s
  stop t 10.20 v0  490 | head fwd excursion +19.5 / -2.8 cm | walk-stand +17.9 cm overshoot +1.5 cm | lean peak +30.4 deg (final +14.8 walk +39.7, overshoot +5.5) | pelvis drop 12.0 cm | settle None s
  stop t 15.42 v0  490 | head fwd excursion +22.1 / -1.1 cm | walk-stand +21.7 cm overshoot +0.3 cm | lean peak +28.0 deg (final +16.5 walk +39.4, overshoot +5.1) | pelvis drop 11.1 cm | settle None s
== v27f_st_sprint_base_r2
  stop t  5.02 v0  490 | head fwd excursion +18.5 / -3.7 cm | walk-stand +19.9 cm overshoot -1.5 cm | lean peak +29.3 deg (final +15.4 walk +39.4, overshoot +5.3) | pelvis drop 12.3 cm | settle None s
  stop t 10.22 v0  490 | head fwd excursion +19.7 / -3.0 cm | walk-stand +17.8 cm overshoot +1.9 cm | lean peak +30.6 deg (final +14.8 walk +39.6, overshoot +5.7) | pelvis drop 11.9 cm | settle None s
  stop t 15.41 v0  490 | head fwd excursion +27.4 / -1.0 cm | walk-stand +25.7 cm overshoot +1.7 cm | lean peak +27.6 deg (final +17.0 walk +39.6, overshoot +4.9) | pelvis drop 9.7 cm | settle None s
== v27f_st_sprint_c27_r1
  stop t  5.00 v0  490 | head fwd excursion +20.6 / -3.8 cm | walk-stand +19.6 cm overshoot +1.0 cm | lean peak +29.3 deg (final +15.4 walk +39.6, overshoot +5.1) | pelvis drop 12.2 cm | settle None s
  stop t 10.22 v0  490 | head fwd excursion +20.1 / -2.4 cm | walk-stand +21.0 cm overshoot -0.9 cm | lean peak +29.0 deg (final +14.6 walk +39.6, overshoot +4.0) | pelvis drop 12.6 cm | settle None s
  stop t 15.40 v0  490 | head fwd excursion +25.4 / -1.2 cm | walk-stand +27.3 cm overshoot -1.9 cm | lean peak +26.9 deg (final +15.6 walk +39.8, overshoot +2.6) | pelvis drop 11.0 cm | settle None s
== v27f_st_sprint_c27_r2
  stop t  5.01 v0  490 | head fwd excursion +18.7 / -3.9 cm | walk-stand +20.2 cm overshoot -1.5 cm | lean peak +29.5 deg (final +15.2 walk +39.5, overshoot +5.3) | pelvis drop 12.3 cm | settle None s
  stop t 10.22 v0  490 | head fwd excursion +19.5 / -2.9 cm | walk-stand +19.6 cm overshoot -0.1 cm | lean peak +30.7 deg (final +14.7 walk +39.9, overshoot +5.5) | pelvis drop 12.0 cm | settle None s
  stop t 15.46 v0  490 | head fwd excursion +20.7 / -1.3 cm | walk-stand +20.2 cm overshoot +0.5 cm | lean peak +27.9 deg (final +16.7 walk +39.5, overshoot +5.1) | pelvis drop 11.3 cm | settle None s
== v27f_gait2_base_r1
  stop t 11.01 v0  300 | head fwd excursion +14.1 / -1.2 cm | walk-stand +15.3 cm overshoot -1.2 cm | lean peak +11.6 deg (final +12.9 walk +23.0, overshoot +1.5) | pelvis drop 13.8 cm | settle 1.98 s
  stop t 17.02 v0  132 | head fwd excursion +7.6 / -0.0 cm | walk-stand +4.4 cm overshoot +3.1 cm | lean peak +4.5 deg (final +11.5 walk +13.6, overshoot +2.4) | pelvis drop 8.0 cm | settle 1.49 s
== v27f_gait2_base_r2
  stop t 11.01 v0  300 | head fwd excursion +14.5 / -1.2 cm | walk-stand +15.0 cm overshoot -0.4 cm | lean peak +11.4 deg (final +12.9 walk +22.9, overshoot +1.4) | pelvis drop 13.4 cm | settle 1.91 s
  stop t 17.01 v0  132 | head fwd excursion +5.5 / -0.7 cm | walk-stand +2.3 cm overshoot +3.2 cm | lean peak +5.2 deg (final +11.3 walk +13.6, overshoot +2.9) | pelvis drop 7.8 cm | settle 1.5 s
== v27f_gait2_c27_r1
  stop t 11.03 v0  300 | head fwd excursion +14.1 / -1.2 cm | walk-stand +15.0 cm overshoot -1.0 cm | lean peak +12.0 deg (final +12.9 walk +22.7, overshoot +2.2) | pelvis drop 13.6 cm | settle 1.79 s
  stop t 17.01 v0  132 | head fwd excursion +5.5 / -0.7 cm | walk-stand +2.3 cm overshoot +3.2 cm | lean peak +5.2 deg (final +11.3 walk +13.6, overshoot +3.0) | pelvis drop 7.8 cm | settle 1.51 s
== v27f_gait2_c27_r2
  stop t 11.03 v0  300 | head fwd excursion +14.4 / -1.3 cm | walk-stand +14.9 cm overshoot -0.5 cm | lean peak +11.6 deg (final +12.9 walk +22.8, overshoot +1.7) | pelvis drop 13.3 cm | settle 1.93 s
  stop t 17.02 v0  132 | head fwd excursion +7.5 / -0.0 cm | walk-stand +4.3 cm overshoot +3.2 cm | lean peak +4.5 deg (final +11.5 walk +13.6, overshoot +2.5) | pelvis drop 8.1 cm | settle 1.51 s
== v27f_taps_base_r1
  stop t  2.13 v0   13 | head fwd excursion +9.4 / -1.0 cm | walk-stand +0.4 cm overshoot +9.0 cm | lean peak +2.2 deg (final +11.0 walk +10.0, overshoot +2.2) | pelvis drop 5.9 cm | settle None s
  stop t  3.76 v0   14 | head fwd excursion +8.8 / -2.4 cm | walk-stand +0.7 cm overshoot +8.1 cm | lean peak +0.9 deg (final +12.2 walk +12.3, overshoot +0.7) | pelvis drop 6.0 cm | settle None s
  stop t  5.45 v0   21 | head fwd excursion +9.9 / -0.2 cm | walk-stand +1.0 cm overshoot +9.0 cm | lean peak +5.5 deg (final +7.5 walk +11.0, overshoot +2.0) | pelvis drop 8.0 cm | settle 2.21 s
  stop t  7.07 v0   11 | head fwd excursion +0.7 / -16.4 cm | walk-stand -14.4 cm overshoot +0.7 cm | lean peak +1.0 deg (final +21.1 walk +9.4, overshoot +1.0) | pelvis drop 3.4 cm | settle None s
  stop t 10.59 v0  132 | head fwd excursion +1.1 / -11.0 cm | walk-stand -8.2 cm overshoot +1.1 cm | lean peak +1.2 deg (final +21.0 walk +14.1, overshoot +1.2) | pelvis drop 3.8 cm | settle None s
  stop t 14.06 v0  132 | head fwd excursion +5.2 / -1.1 cm | walk-stand +1.7 cm overshoot +3.5 cm | lean peak +3.7 deg (final +11.2 walk +14.2, overshoot +0.7) | pelvis drop 7.5 cm | settle 1.54 s
== v27f_taps_base_r2
  stop t  2.13 v0    8 | head fwd excursion +9.3 / -1.0 cm | walk-stand +0.1 cm overshoot +9.2 cm | lean peak +2.0 deg (final +11.0 walk +10.0, overshoot +2.0) | pelvis drop 5.9 cm | settle None s
  stop t  3.76 v0   14 | head fwd excursion +8.4 / -2.9 cm | walk-stand +0.4 cm overshoot +8.0 cm | lean peak +0.8 deg (final +11.3 walk +12.3, overshoot -0.3) | pelvis drop 6.2 cm | settle None s
  stop t  5.46 v0   25 | head fwd excursion +9.7 / -0.1 cm | walk-stand +1.0 cm overshoot +8.7 cm | lean peak +3.9 deg (final +7.6 walk +11.0, overshoot +0.5) | pelvis drop 7.6 cm | settle 2.19 s
  stop t  7.08 v0   11 | head fwd excursion +0.7 / -16.4 cm | walk-stand -14.3 cm overshoot +0.7 cm | lean peak +1.0 deg (final +21.1 walk +9.1, overshoot +1.0) | pelvis drop 3.1 cm | settle None s
  stop t 10.58 v0  132 | head fwd excursion +0.7 / -11.2 cm | walk-stand -8.5 cm overshoot +0.7 cm | lean peak +1.1 deg (final +21.0 walk +14.1, overshoot +1.1) | pelvis drop 3.4 cm | settle None s
  stop t 14.08 v0  132 | head fwd excursion +5.3 / -0.9 cm | walk-stand +1.7 cm overshoot +3.6 cm | lean peak +3.7 deg (final +11.1 walk +14.0, overshoot +0.9) | pelvis drop 7.4 cm | settle 1.52 s
== v27f_taps_c27_r1
  stop t  2.14 v0   10 | head fwd excursion +8.5 / -1.5 cm | walk-stand -0.4 cm overshoot +8.5 cm | lean peak +1.8 deg (final +11.2 walk +10.0, overshoot +1.8) | pelvis drop 5.8 cm | settle None s
  stop t  3.77 v0   14 | head fwd excursion +7.6 / -3.7 cm | walk-stand -0.3 cm overshoot +7.6 cm | lean peak +0.2 deg (final +11.7 walk +12.6, overshoot -0.7) | pelvis drop 6.1 cm | settle 2.19 s
  stop t  5.47 v0   26 | head fwd excursion +10.0 / -0.2 cm | walk-stand +1.2 cm overshoot +8.8 cm | lean peak +4.5 deg (final +7.3 walk +10.9, overshoot +1.0) | pelvis drop 8.0 cm | settle 2.2 s
  stop t  7.08 v0    8 | head fwd excursion +0.7 / -16.1 cm | walk-stand -13.5 cm overshoot +0.7 cm | lean peak +1.0 deg (final +21.1 walk +9.8, overshoot +1.0) | pelvis drop 3.5 cm | settle None s
  stop t 10.59 v0  132 | head fwd excursion +0.7 / -11.3 cm | walk-stand -8.5 cm overshoot +0.7 cm | lean peak +1.0 deg (final +21.2 walk +14.2, overshoot +1.0) | pelvis drop 3.6 cm | settle None s
  stop t 14.08 v0  132 | head fwd excursion +5.2 / -1.1 cm | walk-stand +1.7 cm overshoot +3.5 cm | lean peak +3.7 deg (final +11.2 walk +14.2, overshoot +0.7) | pelvis drop 7.5 cm | settle 1.52 s
== v27f_taps_c27_r2
  stop t  2.14 v0    9 | head fwd excursion +9.6 / -1.1 cm | walk-stand +0.4 cm overshoot +9.3 cm | lean peak +2.1 deg (final +11.0 walk +10.0, overshoot +2.1) | pelvis drop 5.9 cm | settle None s
  stop t  3.77 v0   13 | head fwd excursion +8.7 / -2.8 cm | walk-stand +0.3 cm overshoot +8.4 cm | lean peak +0.8 deg (final +11.1 walk +12.3, overshoot -0.3) | pelvis drop 6.1 cm | settle None s
  stop t  5.47 v0   26 | head fwd excursion +10.1 / -0.2 cm | walk-stand +1.1 cm overshoot +9.0 cm | lean peak +3.9 deg (final +7.5 walk +11.0, overshoot +0.3) | pelvis drop 8.1 cm | settle 2.18 s
  stop t  7.09 v0   11 | head fwd excursion +0.7 / -16.4 cm | walk-stand -14.4 cm overshoot +0.7 cm | lean peak +1.0 deg (final +21.2 walk +8.9, overshoot +1.0) | pelvis drop 3.8 cm | settle None s
  stop t 10.59 v0  132 | head fwd excursion +1.0 / -10.9 cm | walk-stand -8.0 cm overshoot +1.0 cm | lean peak +1.2 deg (final +21.0 walk +14.3, overshoot +1.2) | pelvis drop 3.7 cm | settle None s
  stop t 14.08 v0  132 | head fwd excursion +5.1 / -1.1 cm | walk-stand +1.5 cm overshoot +3.6 cm | lean peak +3.6 deg (final +11.2 walk +14.1, overshoot +0.8) | pelvis drop 7.4 cm | settle 1.54 s
```

### shake
```
== v27f_wfwd_base_r1
  mv_walk_0_0        v 132 | cam pos cm rms/range lat 0.01/0.01 up 0.08/0.25 fwd 0.02/0.00 | rot deg rms/range p 0.000/-0.000 y 0.000/0.000 r 0.020/0.058
== v27f_wfwd_base_r2
  mv_walk_0_0        v 132 | cam pos cm rms/range lat 0.00/0.01 up 0.08/0.25 fwd 0.00/0.00 | rot deg rms/range p 0.000/-0.000 y 0.000/0.000 r 0.021/0.060
== v27f_wfwd_c27_r1
  mv_walk_0_0        v 132 | cam pos cm rms/range lat 0.00/0.00 up 0.08/0.26 fwd 0.02/0.00 | rot deg rms/range p 0.000/-0.000 y 0.000/0.000 r 0.021/0.059
== v27f_wfwd_c27_r2
  mv_walk_0_0        v 132 | cam pos cm rms/range lat 0.01/0.01 up 0.08/0.26 fwd 0.00/0.00 | rot deg rms/range p 0.000/-0.000 y 0.000/0.000 r 0.021/0.060
== v27f_jfwd_base_r1
  mv_jog_0_0         v 300 | cam pos cm rms/range lat 0.01/0.03 up 0.10/0.33 fwd 0.37/0.46 | rot deg rms/range p 0.000/0.000 y 0.000/0.000 r 0.020/0.062
== v27f_jfwd_base_r2
  mv_jog_0_0         v 300 | cam pos cm rms/range lat 0.01/0.04 up 0.10/0.33 fwd 0.31/0.34 | rot deg rms/range p 0.000/0.000 y 0.000/0.000 r 0.020/0.062
== v27f_jfwd_c27_r1
  mv_jog_0_0         v 300 | cam pos cm rms/range lat 0.03/0.02 up 0.10/0.34 fwd 0.22/0.29 | rot deg rms/range p 0.000/0.000 y 0.000/0.000 r 0.020/0.062
== v27f_jfwd_c27_r2
  mv_jog_0_0         v 300 | cam pos cm rms/range lat 0.01/0.04 up 0.10/0.33 fwd 0.32/0.38 | rot deg rms/range p 0.000/0.000 y 0.000/0.000 r 0.020/0.062
== v27f_sfwd_base_r1
  mv_sprint_0_0      v 490 | cam pos cm rms/range lat 0.02/0.06 up 0.08/0.27 fwd 0.66/0.57 | rot deg rms/range p 0.000/0.000 y 0.000/0.000 r 0.042/0.122
== v27f_sfwd_base_r2
  mv_sprint_0_0      v 490 | cam pos cm rms/range lat 0.02/0.05 up 0.08/0.29 fwd 0.57/0.52 | rot deg rms/range p 0.000/0.000 y 0.000/0.000 r 0.042/0.119
== v27f_sfwd_c27_r1
  mv_sprint_0_0      v 490 | cam pos cm rms/range lat 0.02/0.05 up 0.09/0.28 fwd 0.69/0.62 | rot deg rms/range p 0.000/0.000 y 0.000/0.000 r 0.043/0.122
== v27f_sfwd_c27_r2
  mv_sprint_0_0      v 490 | cam pos cm rms/range lat 0.01/0.04 up 0.09/0.26 fwd 0.77/0.75 | rot deg rms/range p 0.000/0.000 y 0.000/0.000 r 0.043/0.125
```

### gait
```
== v27f_gait2_base_r1
  t  0.45 yaw_hold         Gait <E_Gait.WALK: 0>             v    0
  t  5.60 mv_walk_0_0      Gait <E_Gait.RUN: 1>              v  230
  t  6.10 mv_walk_0_0      Gait <E_Gait.SPRINT: 2>           v  412
  t  8.20 mv_walk_0_0      Gait <E_Gait.RUN: 1>              v  300
  t 12.11 mv_walk_rel_1    Gait <E_Gait.WALK: 0>             v    0
== v27f_gait2_base_r2
  t  0.45 yaw_hold         Gait <E_Gait.WALK: 0>             v    0
  t  5.62 mv_walk_0_0      Gait <E_Gait.RUN: 1>              v  243
  t  6.10 mv_walk_0_0      Gait <E_Gait.SPRINT: 2>           v  416
  t  8.20 mv_walk_0_0      Gait <E_Gait.RUN: 1>              v  300
  t 12.10 mv_walk_rel_1    Gait <E_Gait.WALK: 0>             v    0
== v27f_gait2_c27_r1
  t  0.45 yaw_hold         Gait <E_Gait.WALK: 0>             v    0
  t  5.61 mv_walk_0_0      Gait <E_Gait.RUN: 1>              v  225
  t  6.15 mv_walk_0_0      Gait <E_Gait.SPRINT: 2>           v  420
  t  8.20 mv_walk_0_0      Gait <E_Gait.RUN: 1>              v  300
  t 12.12 mv_walk_rel_1    Gait <E_Gait.WALK: 0>             v    0
== v27f_gait2_c27_r2
  t  0.45 yaw_hold         Gait <E_Gait.WALK: 0>             v    0
  t  5.63 mv_walk_0_0      Gait <E_Gait.RUN: 1>              v  234
  t  6.13 mv_walk_0_0      Gait <E_Gait.SPRINT: 2>           v  414
  t  8.19 mv_walk_0_0      Gait <E_Gait.RUN: 1>              v  300
  t 12.15 mv_walk_rel_1    Gait <E_Gait.WALK: 0>             v    0
== v27f_gait3_base_r1
  t  0.45 yaw_hold         Gait <E_Gait.WALK: 0>             v    0
  t  5.46 mv_walk_0_0      Gait <E_Gait.RUN: 1>              v  222
  t  8.61 mv_walk_0_0      Gait <E_Gait.SPRINT: 2>           v  412
  t 11.18 mv_walk_0_0      Gait <E_Gait.RUN: 1>              v  312
  t 14.29 mv_walk_0_0      Gait <E_Gait.WALK: 0>             v  132
== v27f_gait3_base_r2
  t  0.45 yaw_hold         Gait <E_Gait.WALK: 0>             v    0
  t  5.44 mv_walk_0_0      Gait <E_Gait.RUN: 1>              v  222
  t  8.61 mv_walk_0_0      Gait <E_Gait.SPRINT: 2>           v  416
  t 11.19 mv_walk_0_0      Gait <E_Gait.RUN: 1>              v  303
  t 14.31 mv_walk_0_0      Gait <E_Gait.WALK: 0>             v  132
== v27f_gait3_c27_r1
  t  0.45 yaw_hold         Gait <E_Gait.WALK: 0>             v    0
  t  5.49 mv_walk_0_0      Gait <E_Gait.RUN: 1>              v  227
  t  8.62 mv_walk_0_0      Gait <E_Gait.SPRINT: 2>           v  415
  t 11.18 mv_walk_0_0      Gait <E_Gait.RUN: 1>              v  312
  t 14.30 mv_walk_0_0      Gait <E_Gait.WALK: 0>             v  132
== v27f_gait3_c27_r2
  t  0.45 yaw_hold         Gait <E_Gait.WALK: 0>             v    0
  t  5.46 mv_walk_0_0      Gait <E_Gait.RUN: 1>              v  224
  t  8.62 mv_walk_0_0      Gait <E_Gait.SPRINT: 2>           v  414
  t 11.18 mv_walk_0_0      Gait <E_Gait.RUN: 1>              v  309
  t 14.27 mv_walk_0_0      Gait <E_Gait.WALK: 0>             v  133
== v27f_st_sprint_base_r1
  t  0.45 yaw_hold         Gait <E_Gait.WALK: 0>             v    0
  t  1.36 yaw_hold         Gait <E_Gait.SPRINT: 2>           v    0
  t 15.74 mv_stop          Gait <E_Gait.RUN: 1>              v  365
  t 16.98 mv_stop          Gait <E_Gait.WALK: 0>             v    0
== v27f_st_sprint_base_r2
  t  0.44 yaw_hold         Gait <E_Gait.WALK: 0>             v    0
  t  1.37 yaw_hold         Gait <E_Gait.SPRINT: 2>           v    0
  t 15.74 mv_stop          Gait <E_Gait.RUN: 1>              v  365
  t 17.00 mv_stop          Gait <E_Gait.WALK: 0>             v    0
== v27f_st_sprint_c27_r1
  t  0.45 yaw_hold         Gait <E_Gait.WALK: 0>             v    0
  t  1.40 yaw_hold         Gait <E_Gait.SPRINT: 2>           v    0
  t 15.72 mv_stop          Gait <E_Gait.RUN: 1>              v  366
  t 16.99 mv_stop          Gait <E_Gait.WALK: 0>             v    0
== v27f_st_sprint_c27_r2
  t  0.45 yaw_hold         Gait <E_Gait.WALK: 0>             v    0
  t  1.39 yaw_hold         Gait <E_Gait.SPRINT: 2>           v    0
  t 15.82 mv_stop          Gait <E_Gait.RUN: 1>              v  360
  t 17.06 mv_stop          Gait <E_Gait.WALK: 0>             v    0
```

### turn
```
v27f_ad_walk_base_r1   +90: roll 1.6 deg (0.44 s) tilt 6.6 deg head 2.9 cm twist 33.4 deg | -90: roll 1.8 deg (0.51 s) tilt -0.0 deg head 0.1 cm twist 16.9 deg | -90: roll 0.4 deg (0.18 s) tilt 9.0 deg head 3.0 cm twist 9.7 deg | +90: roll 0.9 deg (0.27 s) tilt 7.4 deg head 2.4 cm twist 13.9 deg
v27f_ad_walk_base_r2   +90: roll 1.0 deg (0.36 s) tilt 5.7 deg head 2.5 cm twist 24.9 deg | -90: roll 1.9 deg (0.56 s) tilt -0.0 deg head 0.0 cm twist 17.1 deg | -90: roll 0.6 deg (0.23 s) tilt 9.4 deg head 3.1 cm twist 11.1 deg | +90: roll 1.0 deg (0.32 s) tilt 6.6 deg head 1.9 cm twist 13.1 deg
v27f_ad_walk_c27_r1    +90: roll 1.4 deg (0.48 s) tilt 5.9 deg head 2.5 cm twist 29.4 deg | -90: roll 1.8 deg (0.59 s) tilt -0.0 deg head 0.1 cm twist 18.4 deg | -90: roll 0.5 deg (0.21 s) tilt 9.3 deg head 3.0 cm twist 10.3 deg | +90: roll 0.7 deg (0.22 s) tilt 7.4 deg head 1.9 cm twist 12.0 deg
v27f_ad_walk_c27_r2    +90: roll 1.1 deg (0.37 s) tilt 5.6 deg head 2.5 cm twist 25.0 deg | -90: roll 1.8 deg (0.54 s) tilt -0.0 deg head 0.0 cm twist 17.3 deg | -90: roll 0.5 deg (0.21 s) tilt 9.2 deg head 3.0 cm twist 10.3 deg | +90: roll 1.1 deg (0.33 s) tilt 6.4 deg head 1.8 cm twist 12.9 deg
v27f_ad_jog_base_r1    +90: roll 0.2 deg (0.09 s) tilt 5.9 deg head 3.9 cm twist 32.4 deg | -90: roll 0.1 deg (0.06 s) tilt 5.4 deg head 4.6 cm twist 29.1 deg | -90: roll 3.1 deg (0.45 s) tilt 4.8 deg head 2.5 cm twist 38.2 deg | +90: roll 0.8 deg (0.17 s) tilt 0.0 deg head 0.0 cm twist 44.4 deg
v27f_ad_jog_base_r2    +90: roll 0.2 deg (0.09 s) tilt 6.1 deg head 4.0 cm twist 33.0 deg | -90: roll 0.2 deg (0.12 s) tilt 5.2 deg head 4.7 cm twist 29.5 deg | -90: roll 3.0 deg (0.48 s) tilt 4.4 deg head 2.3 cm twist 37.8 deg | +90: roll 0.8 deg (0.15 s) tilt 0.0 deg head 0.0 cm twist 46.0 deg
v27f_ad_jog_c27_r1     +90: roll 0.0 deg (0.06 s) tilt 5.2 deg head 4.2 cm twist 33.6 deg | -90: roll 0.7 deg (0.17 s) tilt 5.5 deg head 5.2 cm twist 31.4 deg | -90: roll 3.1 deg (0.47 s) tilt 5.1 deg head 2.8 cm twist 33.2 deg | +90: roll 1.0 deg (0.21 s) tilt 0.0 deg head 0.0 cm twist 45.0 deg
v27f_ad_jog_c27_r2     +90: roll 0.0 deg (0.03 s) tilt 5.0 deg head 3.2 cm twist 33.3 deg | -90: roll -0.0 deg (0.00 s) tilt 5.0 deg head 4.7 cm twist 26.3 deg | -90: roll 2.9 deg (0.45 s) tilt 4.3 deg head 2.1 cm twist 42.6 deg | +90: roll 0.1 deg (0.06 s) tilt 0.0 deg head 0.0 cm twist 44.8 deg
v27f_ad_sprint_base_r1 +90: roll 0.1 deg (0.03 s) tilt 2.1 deg head 4.6 cm twist 28.5 deg | -90: roll 1.0 deg (0.20 s) tilt 2.3 deg head 4.5 cm twist 26.8 deg | -90: roll 0.3 deg (0.11 s) tilt 7.2 deg head 5.0 cm twist 36.5 deg | +90: roll 4.9 deg (0.26 s) tilt 0.9 deg head 0.0 cm twist 35.4 deg
v27f_ad_sprint_base_r2 +90: roll 1.7 deg (0.57 s) tilt 0.0 deg head 3.3 cm twist 28.8 deg | -90: roll 0.8 deg (0.24 s) tilt 3.2 deg head 5.0 cm twist 26.9 deg | -90: roll 1.0 deg (0.19 s) tilt 5.7 deg head 2.6 cm twist 45.5 deg | +90: roll 3.7 deg (0.40 s) tilt 1.9 deg head 0.6 cm twist 38.1 deg
v27f_ad_sprint_c27_r1  +90: roll 4.4 deg (0.58 s) tilt 4.1 deg head 0.6 cm twist 27.7 deg | -90: roll 1.3 deg (0.42 s) tilt 1.5 deg head -0.0 cm twist 23.3 deg | -90: roll 4.5 deg (0.94 s) tilt 5.9 deg head 0.1 cm twist 18.9 deg | +90: roll 6.6 deg (0.77 s) tilt 6.2 deg head 1.1 cm twist 19.6 deg
v27f_ad_sprint_c27_r2  +90: roll 3.4 deg (0.59 s) tilt 3.8 deg head 0.8 cm twist 26.4 deg | -90: roll 2.3 deg (0.48 s) tilt 1.8 deg head -0.0 cm twist 23.9 deg | -90: roll 4.8 deg (1.03 s) tilt 6.0 deg head 0.0 cm twist 18.8 deg | +90: roll 7.2 deg (0.74 s) tilt 6.6 deg head 1.1 cm twist 20.5 deg
v27f_sd_jog_base_r1    +45: roll 0.0 deg (0.00 s) tilt 1.7 deg head 1.3 cm twist 12.9 deg | -45: roll 0.4 deg (0.45 s) tilt 4.9 deg head 3.4 cm twist 12.2 deg | -45: roll 0.6 deg (0.33 s) tilt 0.7 deg head 2.8 cm twist 13.9 deg | +45: roll 1.8 deg (0.48 s) tilt 6.1 deg head 4.3 cm twist 15.7 deg
v27f_sd_jog_base_r2    +45: roll 0.0 deg (0.00 s) tilt 1.8 deg head 1.5 cm twist 12.1 deg | -45: roll 0.3 deg (0.38 s) tilt 4.7 deg head 3.2 cm twist 11.9 deg | -45: roll 0.6 deg (0.80 s) tilt 1.4 deg head 3.0 cm twist 15.3 deg | +45: roll 1.7 deg (0.42 s) tilt 5.3 deg head 3.6 cm twist 14.9 deg
v27f_sd_jog_c27_r1     +45: roll 0.0 deg (0.00 s) tilt 1.3 deg head 0.8 cm twist 13.7 deg | -45: roll 0.5 deg (0.47 s) tilt 4.8 deg head 3.2 cm twist 12.5 deg | -45: roll 0.0 deg (0.08 s) tilt 1.2 deg head 2.9 cm twist 12.9 deg | +45: roll 1.9 deg (0.43 s) tilt 6.6 deg head 5.0 cm twist 14.6 deg
v27f_sd_jog_c27_r2     +45: roll 0.0 deg (0.00 s) tilt 1.7 deg head 1.1 cm twist 13.7 deg | -45: roll 0.6 deg (0.40 s) tilt 5.0 deg head 3.3 cm twist 12.3 deg | -45: roll 0.5 deg (0.67 s) tilt 0.8 deg head 2.7 cm twist 15.8 deg | +45: roll 1.8 deg (0.46 s) tilt 5.9 deg head 4.1 cm twist 15.7 deg
v27f_sd_sprint_base_r1 +45: roll 1.1 deg (0.58 s) tilt 4.4 deg head 1.5 cm twist 6.2 deg | -45: roll 3.0 deg (0.62 s) tilt 6.3 deg head 0.9 cm twist 11.2 deg | -45: roll 1.5 deg (0.36 s) tilt 6.6 deg head 1.2 cm twist 8.0 deg | +45: roll 5.1 deg (0.93 s) tilt 5.0 deg head 1.5 cm twist 8.7 deg
v27f_sd_sprint_base_r2 +45: roll 1.4 deg (0.34 s) tilt 4.8 deg head 1.0 cm twist 7.2 deg | -45: roll 2.8 deg (0.61 s) tilt 6.0 deg head 1.0 cm twist 10.8 deg | -45: roll 1.1 deg (0.33 s) tilt 7.1 deg head 1.1 cm twist 7.1 deg | +45: roll 5.3 deg (0.76 s) tilt 5.5 deg head 0.8 cm twist 11.9 deg
v27f_sd_sprint_c27_r1  +45: roll 1.2 deg (0.73 s) tilt 4.8 deg head 0.8 cm twist 8.2 deg | -45: roll 3.6 deg (0.67 s) tilt 6.3 deg head 1.0 cm twist 14.4 deg | -45: roll 1.1 deg (0.26 s) tilt 6.7 deg head 0.9 cm twist 8.3 deg | +45: roll 5.4 deg (0.81 s) tilt 5.8 deg head 0.8 cm twist 11.3 deg
v27f_sd_sprint_c27_r2  +45: roll 0.5 deg (0.24 s) tilt 6.2 deg head 1.8 cm twist 5.9 deg | -45: roll 3.8 deg (0.73 s) tilt 5.2 deg head 0.9 cm twist 10.5 deg | -45: roll 5.3 deg (0.83 s) tilt 4.9 deg head -0.0 cm twist 8.4 deg | +45: roll 1.8 deg (0.62 s) tilt 7.8 deg head 1.9 cm twist 11.5 deg
v27f_jswap_base_r1     +90: roll 0.0 deg (0.03 s) tilt 1.7 deg head 1.2 cm twist 30.5 deg | -90: roll 0.2 deg (0.20 s) tilt 4.1 deg head 3.3 cm twist 28.3 deg | +90: roll 0.7 deg (0.44 s) tilt 6.4 deg head 4.8 cm twist 29.8 deg
v27f_jswap_base_r2     +90: roll 1.9 deg (0.55 s) tilt 7.7 deg head 5.2 cm twist 31.7 deg | -90: roll 0.3 deg (0.17 s) tilt 3.8 deg head 3.1 cm twist 28.6 deg | +90: roll 0.6 deg (0.42 s) tilt 6.0 deg head 4.6 cm twist 29.2 deg
v27f_jswap_c27_r1      +90: roll 1.6 deg (0.57 s) tilt 8.0 deg head 5.3 cm twist 31.0 deg | -90: roll 0.0 deg (0.03 s) tilt 3.5 deg head 2.9 cm twist 27.9 deg | +90: roll 1.5 deg (0.50 s) tilt 7.8 deg head 5.6 cm twist 29.9 deg
v27f_jswap_c27_r2      +90: roll 2.0 deg (0.53 s) tilt 7.9 deg head 5.4 cm twist 31.3 deg | -90: roll 0.2 deg (0.14 s) tilt 3.9 deg head 3.3 cm twist 28.6 deg | +90: roll 0.4 deg (0.39 s) tilt 6.4 deg head 4.8 cm twist 29.5 deg
v27f_jrev_base_r1      +90: roll 1.0 deg (0.34 s) tilt 5.0 deg head 3.2 cm twist 28.9 deg
v27f_jrev_base_r2      +90: roll 1.0 deg (0.38 s) tilt 5.3 deg head 3.4 cm twist 29.9 deg
v27f_jrev_c27_r1       +90: roll 1.1 deg (0.37 s) tilt 5.3 deg head 3.6 cm twist 30.2 deg
v27f_jrev_c27_r2       +90: roll 1.3 deg (0.38 s) tilt 5.8 deg head 3.8 cm twist 32.1 deg
v27f_mt_jog_base_r1    
v27f_mt_jog_base_r2    
v27f_mt_jog_c27_r1     
v27f_mt_jog_c27_r2
v27f_mt_sprint_base_r1 
v27f_mt_sprint_base_r2 
v27f_mt_sprint_c27_r1  
v27f_mt_sprint_c27_r2
```

### kin
```
v27f_wfwd_base_r1      v 132 | cadence 113.9 /min stride  139 cm | pelvis bob 4.1 head bob 4.1 cm | twist pp 26.5 hip yaw pp 10.4 deg | obliquity pp 8.8 shoulder roll pp 7.0 deg | hand swing 4.2 cm
v27f_wfwd_base_r2      v 132 | cadence 113.8 /min stride  139 cm | pelvis bob 4.1 head bob 4.1 cm | twist pp 26.5 hip yaw pp 10.5 deg | obliquity pp 8.9 shoulder roll pp 7.0 deg | hand swing 4.1 cm
v27f_wfwd_c27_r1       v 132 | cadence 113.9 /min stride  139 cm | pelvis bob 4.1 head bob 4.1 cm | twist pp 26.4 hip yaw pp 10.4 deg | obliquity pp 8.9 shoulder roll pp 7.0 deg | hand swing 4.1 cm
v27f_wfwd_c27_r2       v 132 | cadence 113.4 /min stride  140 cm | pelvis bob 4.0 head bob 4.1 cm | twist pp 26.4 hip yaw pp 10.5 deg | obliquity pp 8.9 shoulder roll pp 7.0 deg | hand swing 4.1 cm
v27f_jfwd_base_r1      v 300 | cadence 168.2 /min stride  214 cm | pelvis bob 8.6 head bob 9.4 cm | twist pp 39.8 hip yaw pp 9.3 deg | obliquity pp 8.4 shoulder roll pp 7.8 deg | hand swing 13.7 cm
v27f_jfwd_base_r2      v 300 | cadence 167.4 /min stride  215 cm | pelvis bob 8.7 head bob 9.4 cm | twist pp 39.8 hip yaw pp 9.4 deg | obliquity pp 8.8 shoulder roll pp 8.0 deg | hand swing 13.8 cm
v27f_jfwd_c27_r1       v 300 | cadence 170.4 /min stride  211 cm | pelvis bob 8.8 head bob 9.2 cm | twist pp 39.8 hip yaw pp 9.5 deg | obliquity pp 8.7 shoulder roll pp 8.1 deg | hand swing 13.8 cm
v27f_jfwd_c27_r2       v 300 | cadence 167.3 /min stride  215 cm | pelvis bob 8.7 head bob 9.1 cm | twist pp 39.8 hip yaw pp 9.4 deg | obliquity pp 8.6 shoulder roll pp 8.0 deg | hand swing 13.7 cm
v27f_sfwd_base_r1      v 490 | cadence 176.3 /min stride  334 cm | pelvis bob 5.0 head bob 4.8 cm | twist pp 50.5 hip yaw pp 24.8 deg | obliquity pp 15.8 shoulder roll pp 16.3 deg | hand swing 31.4 cm
v27f_sfwd_base_r2      v 490 | cadence 176.7 /min stride  333 cm | pelvis bob 5.0 head bob 4.7 cm | twist pp 50.4 hip yaw pp 25.1 deg | obliquity pp 15.8 shoulder roll pp 16.1 deg | hand swing 31.4 cm
v27f_sfwd_c27_r1       v 490 | cadence 176.8 /min stride  333 cm | pelvis bob 5.1 head bob 4.9 cm | twist pp 49.9 hip yaw pp 25.3 deg | obliquity pp 15.9 shoulder roll pp 16.5 deg | hand swing 31.3 cm
v27f_sfwd_c27_r2       v 490 | cadence 176.1 /min stride  334 cm | pelvis bob 5.2 head bob 4.9 cm | twist pp 50.2 hip yaw pp 25.6 deg | obliquity pp 15.7 shoulder roll pp 16.4 deg | hand swing 31.8 cm
```

### p2
```
v27f_s10f10_base_r1 | CP stop entries 14 | stop DB selections 18 | rows 732
v27f_s10f10_base_r2 | CP stop entries 14 | stop DB selections 18 | rows 727
v27f_s10f10_c27_r1 | CP stop entries 14 | stop DB selections 18 | rows 744
v27f_s10f10_c27_r2 | CP stop entries 14 | stop DB selections 18 | rows 728
```

### turngait
```
v27f_ad_sprint_base_r1   DB jog 49% sprint 44% other 6% walk 0% | gait PRINT:  58% t.RUN:  42%
    print_90_1 v 490->min 206->255 [sprint>jog] | sprint_0_2 v 255->min 192->490 [jog>sprint] | rint_-90_3 v 490->min 205->255 [sprint>jog] | sprint_0_4 v 255->min 192->490 [jog>sprint] | rint_180_5 v 490->min 2->84 [sprint>walk] | sprint_0_6 v 300->min 3->274 [sprint>other>jog]
v27f_ad_sprint_base_r2   DB jog 48% sprint 46% other 6% walk 0% | gait PRINT:  59% t.RUN:  41%
    print_90_1 v 490->min 207->255 [sprint>jog] | sprint_0_2 v 255->min 193->490 [jog>sprint] | rint_-90_3 v 490->min 203->255 [sprint>jog] | sprint_0_4 v 255->min 206->490 [jog>sprint] | rint_180_5 v 490->min 3->84 [sprint>walk] | sprint_0_6 v 300->min 0->270 [sprint>other>jog]
v27f_ad_sprint_c27_r1    DB sprint 91% other 6% jog 3% walk 1% | gait PRINT:  100%
    print_90_1 v 490->min 310->416 [sprint] | sprint_0_2 v 416->min 314->490 [sprint] | rint_-90_3 v 490->min 309->416 [sprint] | sprint_0_4 v 416->min 318->490 [sprint] | rint_180_5 v 490->min 2->145 [sprint>walk] | sprint_0_6 v 300->min 1->273 [sprint>other>jog]
v27f_ad_sprint_c27_r2    DB sprint 91% other 6% jog 3% walk 0% | gait PRINT:  100%
    print_90_1 v 490->min 309->416 [sprint] | sprint_0_2 v 416->min 314->490 [sprint] | rint_-90_3 v 490->min 318->416 [sprint] | sprint_0_4 v 416->min 320->490 [sprint] | rint_180_5 v 490->min 0->107 [sprint>walk] | sprint_0_6 v 300->min 2->280 [sprint>other>jog]
v27f_mt_sprint_base_r1   DB sprint 90% jog 9% other 1% | gait PRINT:  100%
    yaw_90_0 v 490->min 425->488 [sprint] | yaw_0_1 v 490->min 420->488 [sprint] | aw_-90_2 v 490->min 427->488 [sprint] | yaw_0_3 v 490->min 419->488 [sprint] | aw_180_4 v 490->min 393->393 [sprint] | yaw_0_5 v 489->min 247->247 [sprint>jog] | yaw_done v 484->min 220->220 [sprint>other]
v27f_mt_sprint_base_r2   DB sprint 90% jog 9% other 1% | gait PRINT:  100%
    yaw_90_0 v 490->min 427->488 [sprint] | yaw_0_1 v 490->min 422->488 [sprint] | aw_-90_2 v 490->min 429->488 [sprint] | yaw_0_3 v 490->min 418->488 [sprint] | aw_180_4 v 490->min 356->356 [sprint>jog] | yaw_0_5 v 490->min 153->153 [sprint>jog] | yaw_done v 390->min 210->210 [sprint>other]
v27f_mt_sprint_c27_r1    DB sprint 99% other 1% | gait PRINT:  100%
    yaw_90_0 v 490->min 449->489 [sprint] | yaw_0_1 v 490->min 444->489 [sprint] | aw_-90_2 v 490->min 448->488 [sprint] | yaw_0_3 v 490->min 442->489 [sprint] | aw_180_4 v 490->min 357->357 [sprint] | yaw_0_5 v 490->min 327->327 [sprint] | yaw_done v 490->min 212->212 [sprint>other]
v27f_mt_sprint_c27_r2    DB sprint 99% other 1% | gait PRINT:  100%
    yaw_90_0 v 490->min 448->489 [sprint] | yaw_0_1 v 490->min 444->489 [sprint] | aw_-90_2 v 490->min 448->489 [sprint] | yaw_0_3 v 490->min 442->489 [sprint] | aw_180_4 v 490->min 360->360 [sprint] | yaw_0_5 v 490->min 329->329 [sprint] | yaw_done v 490->min 229->229 [sprint>other]
v27f_mtf_sprint_base_r1  DB sprint 71% jog 28% other 1% | gait PRINT:  100%
    yaw_90_0 v 490->min 336->489 [sprint>jog] | yaw_0_1 v 490->min 316->489 [sprint>jog] | aw_-90_2 v 490->min 338->489 [sprint>jog] | yaw_0_3 v 490->min 317->489 [sprint>jog] | aw_180_4 v 490->min 87->257 [sprint>jog] | yaw_0_5 v 490->min 54->231 [sprint>jog] | yaw_done v 490->min 216->216 [sprint>other]
v27f_mtf_sprint_base_r2  DB sprint 69% jog 29% other 1% | gait PRINT:  100%
    yaw_90_0 v 490->min 326->489 [sprint>jog] | yaw_0_1 v 490->min 317->489 [sprint>jog] | aw_-90_2 v 490->min 334->490 [sprint>jog] | yaw_0_3 v 490->min 317->489 [sprint>jog] | aw_180_4 v 490->min 71->251 [sprint>jog] | yaw_0_5 v 490->min 54->222 [sprint>jog] | yaw_done v 490->min 223->223 [sprint>other]
v27f_mtf_sprint_c27_r1   DB sprint 91% jog 8% other 1% | gait PRINT:  100%
    yaw_90_0 v 490->min 360->490 [sprint] | yaw_0_1 v 490->min 362->490 [sprint] | aw_-90_2 v 490->min 365->490 [sprint] | yaw_0_3 v 490->min 356->490 [sprint] | aw_180_4 v 490->min 86->240 [sprint>jog] | yaw_0_5 v 490->min 56->220 [sprint>jog] | yaw_done v 490->min 222->222 [sprint>other]
v27f_mtf_sprint_c27_r2   DB sprint 91% jog 8% other 1% | gait PRINT:  100%
    yaw_90_0 v 490->min 367->490 [sprint] | yaw_0_1 v 490->min 367->490 [sprint] | aw_-90_2 v 490->min 363->490 [sprint] | yaw_0_3 v 490->min 360->490 [sprint] | aw_180_4 v 490->min 92->236 [sprint>jog] | yaw_0_5 v 490->min 62->208 [sprint>jog] | yaw_done v 490->min 205->205 [sprint>other]
v27f_sd_sprint_base_r1   DB sprint 99% other 1% | gait PRINT:  100%
    print_45_1 v 490->min 426->468 [sprint] | sprint_0_2 v 468->min 435->490 [sprint] | rint_-45_3 v 490->min 425->468 [sprint] | sprint_0_4 v 468->min 435->490 [sprint]
v27f_sd_sprint_base_r2   DB sprint 99% other 1% | gait PRINT:  100%
    print_45_1 v 490->min 428->468 [sprint] | sprint_0_2 v 468->min 435->490 [sprint] | rint_-45_3 v 490->min 424->468 [sprint] | sprint_0_4 v 468->min 435->490 [sprint]
v27f_sd_sprint_c27_r1    DB sprint 99% other 1% | gait PRINT:  100%
    print_45_1 v 490->min 437->468 [sprint] | sprint_0_2 v 468->min 442->490 [sprint] | rint_-45_3 v 490->min 441->468 [sprint] | sprint_0_4 v 468->min 443->490 [sprint]
v27f_sd_sprint_c27_r2    DB sprint 99% other 1% | gait PRINT:  100%
    print_45_1 v 490->min 437->468 [sprint] | sprint_0_2 v 468->min 443->490 [sprint] | rint_-45_3 v 490->min 441->468 [sprint] | sprint_0_4 v 468->min 445->490 [sprint]
v27f_ad_jog_base_r1      DB jog 89% other 11% walk 0% | gait t.RUN:  100%
    v_jog_90_1 v 300->min 194->255 [jog] | mv_jog_0_2 v 255->min 188->300 [jog] | _jog_-90_3 v 300->min 194->255 [jog] | mv_jog_0_4 v 255->min 188->300 [jog] | _jog_180_5 v 300->min 2->158 [jog>other>walk] | mv_jog_0_6 v 245->min 2->230 [jog>other]
v27f_ad_jog_base_r2      DB jog 89% other 11% walk 0% | gait t.RUN:  100%
    v_jog_90_1 v 300->min 194->255 [jog] | mv_jog_0_2 v 255->min 189->300 [jog] | _jog_-90_3 v 300->min 192->255 [jog] | mv_jog_0_4 v 255->min 187->300 [jog] | _jog_180_5 v 300->min 0->158 [jog>other>walk] | mv_jog_0_6 v 245->min 3->231 [jog>other]
v27f_ad_jog_c27_r1       DB jog 91% other 8% walk 0% | gait t.RUN:  100%
    v_jog_90_1 v 300->min 197->255 [jog] | mv_jog_0_2 v 255->min 199->300 [jog] | _jog_-90_3 v 300->min 196->255 [jog] | mv_jog_0_4 v 255->min 200->300 [jog] | _jog_180_5 v 300->min 1->142 [jog>other>walk] | mv_jog_0_6 v 245->min 1->233 [jog>other]
v27f_ad_jog_c27_r2       DB jog 90% other 9% walk 1% | gait t.RUN:  100%
    v_jog_90_1 v 300->min 197->255 [jog] | mv_jog_0_2 v 255->min 200->300 [jog] | _jog_-90_3 v 300->min 195->255 [jog] | mv_jog_0_4 v 255->min 200->300 [jog] | _jog_180_5 v 300->min 1->152 [jog>other>walk] | mv_jog_0_6 v 245->min 1->232 [jog>other]
v27f_mt_jog_base_r1      DB jog 100% | gait t.RUN:  100%
    yaw_90_0 v 300->min 284->300 [jog] | yaw_0_1 v 300->min 282->300 [jog] | aw_-90_2 v 300->min 284->300 [jog] | yaw_0_3 v 300->min 282->300 [jog] | aw_180_4 v 300->min 262->262 [jog] | yaw_0_5 v 300->min 236->247 [jog] | yaw_done v 300->min 40->40 [jog>other]
v27f_mt_jog_base_r2      DB jog 100% | gait t.RUN:  100%
    yaw_90_0 v 300->min 284->300 [jog] | yaw_0_1 v 300->min 283->300 [jog] | aw_-90_2 v 300->min 285->300 [jog] | yaw_0_3 v 300->min 278->300 [jog] | aw_180_4 v 300->min 271->271 [jog] | yaw_0_5 v 300->min 246->254 [jog] | yaw_done v 300->min 39->39 [jog>other]
v27f_mt_jog_c27_r1       DB jog 100% | gait t.RUN:  100%
    yaw_90_0 v 300->min 290->300 [jog] | yaw_0_1 v 300->min 289->300 [jog] | aw_-90_2 v 300->min 291->300 [jog] | yaw_0_3 v 300->min 288->300 [jog] | aw_180_4 v 300->min 284->284 [jog] | yaw_0_5 v 300->min 249->253 [jog] | yaw_done v 300->min 33->33 [jog>other]
v27f_mt_jog_c27_r2       DB jog 100% | gait t.RUN:  100%
    yaw_90_0 v 300->min 289->300 [jog] | yaw_0_1 v 300->min 289->300 [jog] | aw_-90_2 v 300->min 290->300 [jog] | yaw_0_3 v 300->min 288->300 [jog] | aw_180_4 v 300->min 286->288 [jog] | yaw_0_5 v 300->min 252->265 [jog] | yaw_done v 300->min 32->32 [jog>other]
```

### stopdip
```
== v27f_stx_base_r1
  stop t  5.03 v0  132 | pelvis walk 91.1 min 89.1 @0.18s final 95.7 -> dip below final 6.7, below walk 2.0 cm | head dip 6.9 | knee L/R at min 31/54 end 13/13 | feet fore-aft/lat 6/27 cm
  stop t 10.51 v0  132 | pelvis walk 90.8 min 87.5 @0.17s final 95.6 -> dip below final 8.1, below walk 3.3 cm | head dip 8.3 | knee L/R at min 42/36 end 15/13 | feet fore-aft/lat 4/28 cm
  stop t 16.02 v0  132 | pelvis walk 90.8 min 87.7 @0.20s final 95.5 -> dip below final 7.8, below walk 3.1 cm | head dip 8.0 | knee L/R at min 47/41 end 15/13 | feet fore-aft/lat 4/28 cm
== v27f_stx_base_r2
  stop t  5.01 v0  132 | pelvis walk 91.2 min 88.8 @0.15s final 95.7 -> dip below final 6.9, below walk 2.4 cm | head dip 7.2 | knee L/R at min 25/50 end 13/13 | feet fore-aft/lat 6/26 cm
  stop t 10.50 v0  132 | pelvis walk 90.8 min 87.5 @0.21s final 95.6 -> dip below final 8.1, below walk 3.3 cm | head dip 8.3 | knee L/R at min 48/41 end 15/13 | feet fore-aft/lat 4/28 cm
  stop t 16.01 v0  132 | pelvis walk 90.8 min 87.5 @0.17s final 95.6 -> dip below final 8.1, below walk 3.3 cm | head dip 8.2 | knee L/R at min 42/34 end 15/13 | feet fore-aft/lat 3/28 cm
== v27f_stx_c27_r1
  stop t  5.01 v0  132 | pelvis walk 91.2 min 88.8 @0.15s final 95.8 -> dip below final 6.9, below walk 2.3 cm | head dip 7.2 | knee L/R at min 27/51 end 13/13 | feet fore-aft/lat 6/26 cm
  stop t 10.52 v0  132 | pelvis walk 90.6 min 87.6 @0.20s final 95.4 -> dip below final 7.8, below walk 3.0 cm | head dip 8.0 | knee L/R at min 47/42 end 16/14 | feet fore-aft/lat 5/28 cm
  stop t 16.02 v0  132 | pelvis walk 90.9 min 87.6 @0.21s final 95.5 -> dip below final 7.9, below walk 3.3 cm | head dip 8.1 | knee L/R at min 48/42 end 15/13 | feet fore-aft/lat 4/28 cm
== v27f_stx_c27_r2
  stop t  5.00 v0  132 | pelvis walk 91.1 min 88.8 @0.16s final 95.8 -> dip below final 7.0, below walk 2.4 cm | head dip 7.3 | knee L/R at min 27/49 end 13/13 | feet fore-aft/lat 5/27 cm
  stop t 10.52 v0  132 | pelvis walk 90.9 min 87.7 @0.21s final 95.5 -> dip below final 7.9, below walk 3.2 cm | head dip 8.1 | knee L/R at min 48/43 end 15/13 | feet fore-aft/lat 5/28 cm
  stop t 16.01 v0  132 | pelvis walk 90.9 min 87.6 @0.21s final 95.7 -> dip below final 8.1, below walk 3.3 cm | head dip 8.2 | knee L/R at min 48/42 end 14/13 | feet fore-aft/lat 4/28 cm
== v27f_st_walk_base_r1
  stop t  5.00 v0  132 | pelvis walk 91.1 min 88.5 @0.15s final 95.1 -> dip below final 6.6, below walk 2.6 cm | head dip 6.8 | knee L/R at min 16/42 end 28/52 | feet fore-aft/lat 6/24 cm
  stop t 10.21 v0  132 | pelvis walk 90.8 min 87.6 @0.19s final 95.0 -> dip below final 7.5, below walk 3.2 cm | head dip 7.6 | knee L/R at min 44/37 end 28/52 | feet fore-aft/lat 5/24 cm
  stop t 15.42 v0  132 | pelvis walk 91.1 min 87.6 @0.20s final 95.6 -> dip below final 8.0, below walk 3.5 cm | head dip 8.2 | knee L/R at min 47/41 end 15/13 | feet fore-aft/lat 4/28 cm
== v27f_st_walk_base_r2
  stop t  5.02 v0  132 | pelvis walk 91.0 min 89.2 @0.16s final 95.1 -> dip below final 5.9, below walk 1.9 cm | head dip 6.0 | knee L/R at min 24/58 end 27/52 | feet fore-aft/lat 9/23 cm
  stop t 10.20 v0  132 | pelvis walk 90.8 min 87.8 @0.24s final 95.0 -> dip below final 7.3, below walk 3.0 cm | head dip 7.4 | knee L/R at min 47/42 end 28/52 | feet fore-aft/lat 5/24 cm
  stop t 15.42 v0  132 | pelvis walk 90.9 min 87.7 @0.21s final 95.6 -> dip below final 7.9, below walk 3.2 cm | head dip 8.1 | knee L/R at min 48/44 end 15/13 | feet fore-aft/lat 4/28 cm
== v27f_st_walk_c27_r1
  stop t  5.01 v0  132 | pelvis walk 91.1 min 88.8 @0.16s final 95.2 -> dip below final 6.4, below walk 2.3 cm | head dip 6.5 | knee L/R at min 27/51 end 27/52 | feet fore-aft/lat 7/24 cm
  stop t 10.23 v0  132 | pelvis walk 90.9 min 87.7 @0.19s final 95.0 -> dip below final 7.3, below walk 3.2 cm | head dip 7.4 | knee L/R at min 44/39 end 27/52 | feet fore-aft/lat 8/23 cm
  stop t 15.43 v0  132 | pelvis walk 90.9 min 87.6 @0.21s final 95.6 -> dip below final 7.9, below walk 3.2 cm | head dip 8.1 | knee L/R at min 47/42 end 15/13 | feet fore-aft/lat 4/28 cm
== v27f_st_walk_c27_r2
  stop t  5.00 v0  132 | pelvis walk 91.2 min 88.7 @0.15s final 95.2 -> dip below final 6.5, below walk 2.5 cm | head dip 6.7 | knee L/R at min 23/47 end 28/52 | feet fore-aft/lat 6/24 cm
  stop t 10.21 v0  132 | pelvis walk 90.8 min 87.6 @0.21s final 95.1 -> dip below final 7.5, below walk 3.2 cm | head dip 7.6 | knee L/R at min 49/43 end 28/52 | feet fore-aft/lat 5/24 cm
  stop t 15.41 v0  132 | pelvis walk 90.8 min 87.5 @0.21s final 95.6 -> dip below final 8.1, below walk 3.3 cm | head dip 8.2 | knee L/R at min 48/42 end 15/13 | feet fore-aft/lat 4/28 cm
== v27f_st_jog_base_r1
  stop t  5.00 v0  300 | pelvis walk 90.7 min 80.5 @0.84s final 92.3 -> dip below final 11.8, below walk 10.2 cm | head dip 12.8 | knee L/R at min 82/23 end 20/40 | feet fore-aft/lat 1/26 cm
  stop t 10.21 v0  300 | pelvis walk 91.1 min 81.1 @0.79s final 92.5 -> dip below final 11.4, below walk 10.0 cm | head dip 12.5 | knee L/R at min 87/21 end 20/37 | feet fore-aft/lat 0/23 cm
  stop t 15.42 v0  300 | pelvis walk 91.1 min 80.9 @0.79s final 92.3 -> dip below final 11.4, below walk 10.2 cm | head dip 12.3 | knee L/R at min 87/30 end 26/40 | feet fore-aft/lat 1/22 cm
== v27f_st_jog_base_r2
  stop t  5.02 v0  300 | pelvis walk 90.8 min 80.4 @0.82s final 92.3 -> dip below final 11.9, below walk 10.4 cm | head dip 12.8 | knee L/R at min 83/26 end 20/42 | feet fore-aft/lat 1/21 cm
  stop t 10.21 v0  300 | pelvis walk 90.0 min 80.8 @0.78s final 92.4 -> dip below final 11.7, below walk 9.2 cm | head dip 12.7 | knee L/R at min 86/24 end 20/38 | feet fore-aft/lat 1/23 cm
  stop t 15.41 v0  300 | pelvis walk 91.0 min 80.4 @0.82s final 92.4 -> dip below final 12.1, below walk 10.6 cm | head dip 12.9 | knee L/R at min 83/32 end 26/39 | feet fore-aft/lat 1/27 cm
== v27f_st_jog_c27_r1
  stop t  5.03 v0  300 | pelvis walk 91.0 min 81.0 @0.77s final 92.4 -> dip below final 11.4, below walk 10.1 cm | head dip 12.4 | knee L/R at min 87/22 end 17/38 | feet fore-aft/lat 1/25 cm
  stop t 10.20 v0  300 | pelvis walk 91.0 min 80.6 @0.80s final 92.4 -> dip below final 11.8, below walk 10.5 cm | head dip 12.9 | knee L/R at min 83/21 end 18/34 | feet fore-aft/lat 1/27 cm
  stop t 15.41 v0  300 | pelvis walk 91.1 min 80.7 @0.77s final 92.4 -> dip below final 11.7, below walk 10.3 cm | head dip 12.6 | knee L/R at min 86/26 end 26/39 | feet fore-aft/lat 1/27 cm
== v27f_st_jog_c27_r2
  stop t  5.02 v0  300 | pelvis walk 91.0 min 80.3 @0.84s final 92.4 -> dip below final 12.1, below walk 10.7 cm | head dip 13.1 | knee L/R at min 82/22 end 19/37 | feet fore-aft/lat 1/27 cm
  stop t 10.21 v0  300 | pelvis walk 91.0 min 80.5 @0.81s final 92.5 -> dip below final 11.9, below walk 10.5 cm | head dip 12.9 | knee L/R at min 84/24 end 18/31 | feet fore-aft/lat 1/21 cm
  stop t 15.41 v0  300 | pelvis walk 91.0 min 80.9 @0.77s final 92.2 -> dip below final 11.4, below walk 10.2 cm | head dip 12.4 | knee L/R at min 85/19 end 27/40 | feet fore-aft/lat 1/22 cm
== v27f_st_sprint_base_r1
  stop t  5.02 v0  490 | pelvis walk 89.4 min 80.8 @0.67s final 92.3 -> dip below final 11.4, below walk 8.6 cm | head dip 15.4 | knee L/R at min 52/47 end 35/25 | feet fore-aft/lat 2/27 cm
  stop t 10.20 v0  490 | pelvis walk 90.3 min 81.6 @0.92s final 92.5 -> dip below final 10.9, below walk 8.7 cm | head dip 15.6 | knee L/R at min 51/47 end 21/28 | feet fore-aft/lat 1/27 cm
  stop t 15.42 v0  490 | pelvis walk 89.4 min 80.5 @0.77s final 91.5 -> dip below final 11.1, below walk 8.9 cm | head dip 14.8 | knee L/R at min 40/72 end 48/36 | feet fore-aft/lat 15/31 cm
== v27f_st_sprint_base_r2
  stop t  5.02 v0  490 | pelvis walk 89.4 min 80.7 @0.67s final 92.3 -> dip below final 11.6, below walk 8.6 cm | head dip 15.3 | knee L/R at min 48/45 end 35/25 | feet fore-aft/lat 2/27 cm
  stop t 10.22 v0  490 | pelvis walk 90.4 min 81.8 @0.91s final 92.5 -> dip below final 10.7, below walk 8.6 cm | head dip 15.4 | knee L/R at min 49/45 end 22/30 | feet fore-aft/lat 0/27 cm
  stop t 15.41 v0  490 | pelvis walk 91.1 min 81.1 @0.54s final 90.8 -> dip below final 9.7, below walk 9.9 cm | head dip 13.8 | knee L/R at min 58/49 end 63/31 | feet fore-aft/lat 13/27 cm
== v27f_st_sprint_c27_r1
  stop t  5.00 v0  490 | pelvis walk 90.9 min 80.8 @0.67s final 92.2 -> dip below final 11.4, below walk 10.1 cm | head dip 15.4 | knee L/R at min 52/47 end 35/25 | feet fore-aft/lat 2/27 cm
  stop t 10.22 v0  490 | pelvis walk 89.8 min 80.3 @0.62s final 92.5 -> dip below final 12.2, below walk 9.4 cm | head dip 16.2 | knee L/R at min 35/69 end 39/30 | feet fore-aft/lat 15/31 cm
  stop t 15.40 v0  490 | pelvis walk 89.8 min 80.4 @0.53s final 91.4 -> dip below final 11.0, below walk 9.3 cm | head dip 14.9 | knee L/R at min 37/72 end 48/30 | feet fore-aft/lat 37/31 cm
== v27f_st_sprint_c27_r2
  stop t  5.01 v0  490 | pelvis walk 89.3 min 80.7 @0.65s final 92.3 -> dip below final 11.5, below walk 8.6 cm | head dip 15.4 | knee L/R at min 48/45 end 35/25 | feet fore-aft/lat 2/27 cm
  stop t 10.22 v0  490 | pelvis walk 90.8 min 81.6 @0.92s final 92.5 -> dip below final 10.9, below walk 9.2 cm | head dip 15.6 | knee L/R at min 51/47 end 21/28 | feet fore-aft/lat 0/27 cm
  stop t 15.46 v0  490 | pelvis walk 89.4 min 80.6 @0.85s final 91.9 -> dip below final 11.3, below walk 8.7 cm | head dip 15.0 | knee L/R at min 37/70 end 47/34 | feet fore-aft/lat 13/31 cm
```

### startsize
```
== v27f_wst_base_r1
  start t  2.07 mv_walk_0_0  | pelvis stand 94.6 min -7.8 max +0.1 | head lat -0.2/+9.3 fwd max +7.6 | pitch stand 10.4 peak +6.7 | roll pp 5.6 | steady: pelvis pp 4.2 head lat pp 3.2 pitch 15.4 roll pp 5.8
  start t  6.50 mv_walk_0_2  | pelvis stand 95.8 min -7.5 max +0.0 | head lat -3.3/+3.6 fwd max +12.0 | pitch stand 11.5 peak +10.6 | roll pp 5.9 | steady: pelvis pp 4.1 head lat pp 5.0 pitch 14.6 roll pp 7.9
  start t 11.00 mv_walk_0_4  | pelvis stand 95.8 min -7.5 max -0.0 | head lat -3.1/+3.8 fwd max +15.7 | pitch stand 11.5 peak +10.7 | roll pp 5.3 | steady: pelvis pp 4.0 head lat pp 5.1 pitch 14.6 roll pp 7.9
  start t 15.50 mv_walk_0_6  | pelvis stand 95.5 min -7.2 max -0.0 | head lat -3.9/+3.0 fwd max +14.3 | pitch stand 11.9 peak +10.3 | roll pp 5.3 | steady: pelvis pp 3.6 head lat pp 4.9 pitch 14.3 roll pp 7.8
== v27f_wst_base_r2
  start t  2.02 mv_walk_0_0  | pelvis stand 94.6 min -7.2 max +0.3 | head lat -0.1/+9.4 fwd max +7.3 | pitch stand 10.4 peak +7.3 | roll pp 6.9 | steady: pelvis pp 4.3 head lat pp 3.3 pitch 14.4 roll pp 5.6
  start t  6.50 mv_walk_0_2  | pelvis stand 95.6 min -7.3 max +0.0 | head lat -3.1/+3.4 fwd max +12.1 | pitch stand 11.4 peak +10.7 | roll pp 5.2 | steady: pelvis pp 3.6 head lat pp 5.0 pitch 14.4 roll pp 7.8
  start t 11.02 mv_walk_0_4  | pelvis stand 95.4 min -7.1 max +0.0 | head lat -4.4/+2.6 fwd max +14.7 | pitch stand 11.1 peak +11.1 | roll pp 5.8 | steady: pelvis pp 4.0 head lat pp 5.0 pitch 14.5 roll pp 7.9
  start t 15.53 mv_walk_0_6  | pelvis stand 95.7 min -7.4 max +0.0 | head lat -2.8/+4.0 fwd max +14.1 | pitch stand 12.1 peak +10.0 | roll pp 5.5 | steady: pelvis pp 3.6 head lat pp 5.0 pitch 14.4 roll pp 7.8
== v27f_wst_c27_r1
  start t  2.04 mv_walk_0_0  | pelvis stand 94.5 min -7.8 max +0.3 | head lat -0.3/+9.2 fwd max +7.6 | pitch stand 10.4 peak +7.1 | roll pp 3.6 | steady: pelvis pp 4.2 head lat pp 3.2 pitch 15.0 roll pp 5.8
  start t  6.51 mv_walk_0_2  | pelvis stand 95.6 min -7.4 max +0.0 | head lat -2.9/+3.5 fwd max +12.0 | pitch stand 11.4 peak +10.7 | roll pp 4.8 | steady: pelvis pp 3.6 head lat pp 4.9 pitch 14.4 roll pp 7.9
  start t 11.01 mv_walk_0_4  | pelvis stand 95.7 min -7.4 max +0.0 | head lat -3.3/+3.8 fwd max +15.1 | pitch stand 11.4 peak +10.7 | roll pp 5.6 | steady: pelvis pp 3.7 head lat pp 5.0 pitch 14.4 roll pp 7.9
  start t 15.52 mv_walk_0_6  | pelvis stand 95.7 min -7.4 max +0.0 | head lat -2.6/+4.1 fwd max +14.2 | pitch stand 12.2 peak +10.0 | roll pp 5.3 | steady: pelvis pp 3.7 head lat pp 5.0 pitch 14.4 roll pp 7.8
== v27f_wst_c27_r2
  start t  2.01 mv_walk_0_0  | pelvis stand 94.6 min -7.8 max +0.3 | head lat -0.2/+9.4 fwd max +7.9 | pitch stand 10.4 peak +7.1 | roll pp 5.6 | steady: pelvis pp 4.3 head lat pp 3.3 pitch 15.3 roll pp 5.9
  start t  6.52 mv_walk_0_2  | pelvis stand 95.6 min -7.3 max +0.0 | head lat -3.5/+3.5 fwd max +12.2 | pitch stand 11.4 peak +10.8 | roll pp 5.9 | steady: pelvis pp 4.0 head lat pp 5.0 pitch 14.6 roll pp 7.9
  start t 11.01 mv_walk_0_4  | pelvis stand 95.7 min -7.4 max -0.0 | head lat -3.5/+3.4 fwd max +15.2 | pitch stand 11.3 peak +10.8 | roll pp 5.4 | steady: pelvis pp 3.9 head lat pp 5.0 pitch 14.5 roll pp 7.9
  start t 15.51 mv_walk_0_6  | pelvis stand 95.6 min -7.3 max +0.0 | head lat -3.4/+3.6 fwd max +14.0 | pitch stand 12.0 peak +10.1 | roll pp 5.8 | steady: pelvis pp 4.0 head lat pp 5.1 pitch 14.5 roll pp 7.9
== v27f_wfwd_base_r1
  start t  2.05 mv_walk_0_0  | pelvis stand 94.6 min -7.8 max +0.3 | head lat -0.2/+9.4 fwd max +7.7 | pitch stand 10.4 peak +7.1 | roll pp 5.6 | steady: pelvis pp 4.3 head lat pp 3.2 pitch 15.3 roll pp 5.8
== v27f_wfwd_base_r2
  start t  2.02 mv_walk_0_0  | pelvis stand 94.6 min -7.8 max +0.3 | head lat -0.2/+9.3 fwd max +7.8 | pitch stand 10.4 peak +7.1 | roll pp 5.6 | steady: pelvis pp 4.2 head lat pp 3.3 pitch 15.3 roll pp 5.9
== v27f_wfwd_c27_r1
  start t  2.04 mv_walk_0_0  | pelvis stand 94.6 min -7.7 max +0.3 | head lat -0.4/+9.2 fwd max +7.6 | pitch stand 10.4 peak +7.2 | roll pp 5.6 | steady: pelvis pp 4.2 head lat pp 3.2 pitch 15.2 roll pp 5.8
== v27f_wfwd_c27_r2
  start t  2.02 mv_walk_0_0  | pelvis stand 94.6 min -7.7 max +0.3 | head lat +0.0/+9.4 fwd max +7.7 | pitch stand 10.4 peak +7.1 | roll pp 5.6 | steady: pelvis pp 4.3 head lat pp 3.3 pitch 15.2 roll pp 5.7
== v27f_stx_base_r1
  start t  2.02 mv_walk_0_0  | pelvis stand 94.6 min -7.8 max +0.3 | head lat -0.3/+9.4 fwd max +7.8 | pitch stand 10.4 peak +7.1 | roll pp 5.6 | steady: pelvis pp 4.3 head lat pp 2.9 pitch 15.0 roll pp 5.8
  start t  7.52 mv_walk_0_2  | pelvis stand 95.7 min -7.5 max +0.0 | head lat -2.8/+3.5 fwd max +15.2 | pitch stand 11.4 peak +10.8 | roll pp 4.8 | steady: pelvis pp 3.8 head lat pp 4.9 pitch 14.4 roll pp 7.7
  start t 13.01 mv_walk_0_4  | pelvis stand 95.6 min -7.3 max +0.0 | head lat -2.9/+4.0 fwd max +9.9 | pitch stand 12.1 peak +10.0 | roll pp 5.7 | steady: pelvis pp 3.9 head lat pp 4.8 pitch 14.7 roll pp 7.9
== v27f_stx_base_r2
  start t  2.02 mv_walk_0_0  | pelvis stand 94.6 min -7.8 max +0.3 | head lat -0.1/+9.4 fwd max +7.7 | pitch stand 10.4 peak +7.2 | roll pp 5.6 | steady: pelvis pp 4.3 head lat pp 3.2 pitch 15.3 roll pp 5.8
  start t  7.51 mv_walk_0_2  | pelvis stand 95.7 min -7.5 max +0.0 | head lat -2.8/+3.9 fwd max +15.4 | pitch stand 11.4 peak +10.8 | roll pp 4.6 | steady: pelvis pp 3.6 head lat pp 5.0 pitch 14.4 roll pp 7.8
  start t 13.03 mv_walk_0_4  | pelvis stand 95.6 min -7.3 max +0.0 | head lat -2.6/+4.0 fwd max +9.9 | pitch stand 12.1 peak +10.0 | roll pp 5.1 | steady: pelvis pp 3.7 head lat pp 5.0 pitch 14.5 roll pp 7.9
== v27f_stx_c27_r1
  start t  2.01 mv_walk_0_0  | pelvis stand 94.6 min -7.7 max +0.3 | head lat -0.2/+9.4 fwd max +7.7 | pitch stand 10.4 peak +7.1 | roll pp 5.6 | steady: pelvis pp 4.2 head lat pp 3.3 pitch 15.3 roll pp 5.8
  start t  7.51 mv_walk_0_2  | pelvis stand 95.8 min -7.5 max +0.0 | head lat -3.1/+3.8 fwd max +15.3 | pitch stand 11.4 peak +10.8 | roll pp 5.9 | steady: pelvis pp 4.1 head lat pp 4.9 pitch 14.3 roll pp 7.8
  start t 13.00 mv_walk_0_4  | pelvis stand 95.4 min -7.1 max +0.0 | head lat -2.8/+3.8 fwd max +10.0 | pitch stand 12.0 peak +10.1 | roll pp 5.0 | steady: pelvis pp 3.6 head lat pp 5.0 pitch 14.5 roll pp 7.9
== v27f_stx_c27_r2
  start t  2.02 mv_walk_0_0  | pelvis stand 94.6 min -7.8 max +0.3 | head lat -0.2/+9.4 fwd max +7.7 | pitch stand 10.4 peak +7.0 | roll pp 5.6 | steady: pelvis pp 4.3 head lat pp 3.3 pitch 15.3 roll pp 5.9
  start t  7.51 mv_walk_0_2  | pelvis stand 95.8 min -7.5 max +0.0 | head lat -3.1/+3.8 fwd max +15.3 | pitch stand 11.4 peak +10.8 | roll pp 5.9 | steady: pelvis pp 4.1 head lat pp 5.0 pitch 14.5 roll pp 7.8
  start t 13.00 mv_walk_0_4  | pelvis stand 95.5 min -7.1 max +0.0 | head lat -2.8/+4.0 fwd max +10.0 | pitch stand 12.1 peak +10.1 | roll pp 5.0 | steady: pelvis pp 3.7 head lat pp 5.1 pitch 14.5 roll pp 8.0
```

### error gate
```
v27f_wfwd_base_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_wfwd_base_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_wfwd_c27_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_wfwd_c27_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_jfwd_base_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_jfwd_base_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_jfwd_c27_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_jfwd_c27_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_sfwd_base_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_sfwd_base_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_sfwd_c27_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_sfwd_c27_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_wst_base_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_wst_base_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_wst_c27_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_wst_c27_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_wstart_base_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_wstart_base_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_wstart_c27_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_wstart_c27_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_stx_base_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_stx_base_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_stx_c27_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_stx_c27_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_st_walk_base_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_st_walk_base_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_st_walk_c27_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_st_walk_c27_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_st_jog_base_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_st_jog_base_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_st_jog_c27_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_st_jog_c27_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_st_sprint_base_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_st_sprint_base_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_st_sprint_c27_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_st_sprint_c27_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_gait2_base_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_gait2_base_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_gait2_c27_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_gait2_c27_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_gait3_base_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_gait3_base_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_gait3_c27_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_gait3_c27_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_sd_jog_base_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_sd_jog_base_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_sd_jog_c27_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_sd_jog_c27_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_sd_sprint_base_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_sd_sprint_base_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_sd_sprint_c27_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_sd_sprint_c27_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_jswap_base_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_jswap_base_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_jswap_c27_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_jswap_c27_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_jrev_base_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_jrev_base_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_jrev_c27_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_jrev_c27_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_ad_walk_base_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_ad_walk_base_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_ad_walk_c27_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_ad_walk_c27_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_ad_jog_base_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_ad_jog_base_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_ad_jog_c27_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_ad_jog_c27_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_ad_sprint_base_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_ad_sprint_base_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_ad_sprint_c27_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_ad_sprint_c27_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_mt_jog_base_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_mt_jog_base_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_mt_jog_c27_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_mt_jog_c27_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_mt_sprint_base_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_mt_sprint_base_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_mt_sprint_c27_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_mt_sprint_c27_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_mtf_sprint_base_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_mtf_sprint_base_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_mtf_sprint_c27_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_mtf_sprint_c27_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_taps_base_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_taps_base_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_taps_c27_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_taps_c27_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_s10f10_base_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_s10f10_base_r2 | Accessed None (SHME): 0 | index skips: 0
v27f_s10f10_c27_r1 | Accessed None (SHME): 0 | index skips: 0
v27f_s10f10_c27_r2 | Accessed None (SHME): 0 | index skips: 0
```
