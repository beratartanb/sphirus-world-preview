## 1. Worst planted-ball slide (cm, owner) and upper-body pops (count / worst m/s2), fixed 30 FPS: production o vs tk; * = database-not-ready frames

| scenario | o | o owner | o pops | tk | tk owner | tk pops |
|---|---|---|---|---|---|---|
| j40_rlw | 10.0 | A_CP2_Jog_Fwd_Start | 8 / 82 | 8.7 | A_CP2_Jog_Fwd_Start | 7 / 184 |
| j40_lrw | - |  | - | 11.7 | A_CT_Jog_Fwd | 5 / 269 |
| j39_rl | - |  | - | 46.3 | A_LS_Jog_Left_Stop | 8 / 184 |
| j39_rw | 12.9 | A_CT_Jog_Fwd | 7 / 73 | 7.6 | A_CT_Jog_Fwd | 5 / 307 |
| j39_rl_e | - |  | - | 9.4 | SHM237_JogStop_Bl_P16 | 9 / 156 |
| j39_rl_l | - |  | - | 11.9 | A_CT_Jog_Fwd | 7 / 120 |
| j39_lr | 38.8 | SHM216_RevTurn_R_Lfoot | 6 / 89 | 12.2 | SHM214_RevPush_Rfoot | 9 / 117 |
| j39_lw | - |  | - | 11.3 | SHM239_Tk_L_P22_K1_Back | 7 / 288 |
| j38_cc90 | 21.5 | SHM216_RevTurn_L_Rfoot | 7 / 228 | 9.6 | SHM239_Tk_R_P16_K1_Back | 7 / 277 |
| mtf_jog | - |  | - | - |  | - |
| jlean | - |  | - | - |  | - |
| j38_c90r | - |  | - | - |  | - |
| j38_c90l | - |  | - | - |  | - |
| j38_c90rb | - |  | - | - |  | - |
| j38_c90lb | - |  | - | - |  | - |
| j38_c45r | - |  | - | - |  | - |
| j38_c135r | - |  | - | - |  | - |
| w38_c90r | - |  | - | - |  | - |
| s38_c90r | - |  | - | - |  | - |
| j36_rsm | - |  | - | - |  | - |
| j36_stop | - |  | - | - |  | - |
| j36_stopr | - |  | - | - |  | - |
| j34_chain1 | - |  | - | - |  | - |
| j35_rev | - |  | - | - |  | - |
| j30_rel_3450 | - |  | - | - |  | - |
| j36_sside | - |  | - | - |  | - |
| jstart | - |  | - | - |  | - |
| e29_chain | - |  | - | - |  | - |
| c29_combo | - |  | - | - |  | - |
| jdiag | - |  | - | - |  | - |
| wdiag | - |  | - | - |  | - |
| wstart | - |  | - | - |  | - |
| cam32_j90 | - |  | - | - |  | - |
| chain_jogcut | - |  | - | - |  | - |
| ad_jog | - |  | - | - |  | - |
| mt_jog | - |  | - | - |  | - |
| j39_push_plan | - |  | - | - |  | - |
| j39_push_jog | - |  | - | - |  | - |

## 2. Control stages after each input change (s after the request frame; tk239)

| scenario | variant | input | first body reaction | first support | velocity transfer | stable heading |
|---|---|---|---|---|---|---|
| j40_rlw | o |   90 deg at 5.32 s (speed 287, heading    2) | - | 0.12 | 0.36 | - |
| j40_rlw | o |  -90 deg at 5.77 s (speed 208, heading   17) | - | 0.27 | 0.02 | - |
| j40_rlw | o |    0 deg at 6.27 s (speed 219, heading  -73) | 0.17 (head) | 0.13 | 0.45 | 0.79 |
| j40_rlw | o |    0 deg at 9.82 s (speed   1, heading    0) | - | - | 0.22 | 0.97 |
| j40_rlw | tk |   90 deg at 5.32 s (speed 287, heading    2) | - | 0.12 | 0.36 | - |
| j40_rlw | tk |  -90 deg at 5.77 s (speed 208, heading   17) | 0.49 (head) | 0.42 | 0.22 | - |
| j40_rlw | tk |    0 deg at 6.27 s (speed 141, heading  -22) | - | 0.25 | 0.97 | 1.26 |
| j40_rlw | tk |    0 deg at 9.82 s (speed   1, heading    0) | - | - | 0.22 | 0.97 |
| j40_lrw | tk |  -90 deg at 5.32 s (speed 287, heading   -2) | 0.1 (head) | 0.38 | - | - |
| j40_lrw | tk |   90 deg at 5.77 s (speed 269, heading   -4) | 0.26 (head) | 0.08 | - | - |
| j40_lrw | tk |    0 deg at 6.27 s (speed 241, heading  -90) | 0.12 (head) | 0.12 | 0.27 | 1.92 |
| j39_rl | tk |   90 deg at 5.32 s (speed 287, heading    2) | - | 0.12 | 0.36 | - |
| j39_rl | tk |  -90 deg at 5.77 s (speed 208, heading   17) | 0.49 (head) | 0.42 | 0.22 | 1.05 |
| j39_rl | tk | -154 deg at 9.82 s (speed   1, heading -154) | - | - | 0.21 | 0.97 |
| j39_rw | o |   90 deg at 5.32 s (speed 287, heading    2) | - | 0.38 | - | - |
| j39_rw | o |    0 deg at 5.77 s (speed 258, heading    5) | 0.46 (head) | 0.23 | 1.15 | 0.0 |
| j39_rw | tk |   90 deg at 5.32 s (speed 287, heading    2) | - | 0.12 | 0.36 | - |
| j39_rw | tk |    0 deg at 5.77 s (speed 208, heading   17) | 0.07 (head) | 0.29 | 0.52 | 0.57 |
| j39_rl_e | tk |   90 deg at 5.32 s (speed 287, heading    2) | - | 0.12 | - | - |
| j39_rl_e | tk |  -90 deg at 5.57 s (speed 256, heading    5) | 0.53 (head) | 0.18 | 0.44 | 1.12 |
| j39_rl_l | tk |   90 deg at 5.32 s (speed 287, heading    2) | - | 0.12 | 0.36 | - |
| j39_rl_l | tk |  -90 deg at 6.07 s (speed 185, heading   62) | 0.86 (head) | 0.33 | 0.7 | 1.74 |
| j39_lr | o |  -90 deg at 5.32 s (speed 287, heading   -2) | 0.1 (head) | 0.38 | - | - |
| j39_lr | o |   90 deg at 5.77 s (speed 269, heading   -4) | 0.02 (head) | 0.27 | 0.04 | 0.9 |
| j39_lr | tk |  -90 deg at 5.32 s (speed 287, heading   -2) | 0.1 (head) | 0.38 | - | - |
| j39_lr | tk |   90 deg at 5.77 s (speed 269, heading   -4) | 0.26 (head) | 0.08 | 1.13 | 2.17 |
| j39_lw | tk |  -90 deg at 5.32 s (speed 287, heading   -2) | 0.1 (head) | 0.38 | - | - |
| j39_lw | tk |    0 deg at 5.77 s (speed 269, heading   -4) | 0.07 (head) | 0.25 | 1.09 | 0.0 |
| j38_cc90 | o |   90 deg at 5.32 s (speed 287, heading    2) | - | 0.12 | 0.36 | - |
| j38_cc90 | o |    0 deg at 6.12 s (speed 192, heading   66) | 0.06 (head) | - | 0.22 | - |
| j38_cc90 | o |  -90 deg at 6.92 s (speed 285, heading   11) | 0.18 (head) | - | 0.07 | 1.02 |
| j38_cc90 | tk |   90 deg at 5.32 s (speed 287, heading    2) | - | 0.38 | 0.52 | - |
| j38_cc90 | tk |    0 deg at 6.12 s (speed 164, heading   50) | 0.05 (head) | 0.32 | 0.15 | 0.56 |
| j38_cc90 | tk |  -90 deg at 6.92 s (speed 279, heading   -1) | 0.08 (head) | 0.32 | 0.66 | 1.25 |

## 3. Body alignment after the second request (yaw minus the velocity heading, deg; balance238)

| scenario | variant | second request s | pelvis / chest / head @+1.2 | @+1.8 | speed @+1.8 |
|---|---|---|---|---|---|
| j40_rlw | o | 5.77 | 2 / 22 / 11 | -1 / -1 / -3 | 294 |
| j40_rlw | tk | 5.77 | -1 / 11 / 71 | 0 / -5 / 6 | 292 |
| j40_lrw | o | - |
| j40_lrw | tk | 5.77 | 2 / 16 / -7 | -15 / -35 / -13 | 124 |
| j39_rl | o | - |
| j39_rl | tk | 5.77 | -4 / 11 / 70 | 2 / 1 / 56 | 294 |
| j39_rw | o | 5.77 | -4 / -13 / -11 | 5 / 17 / -10 | 294 |
| j39_rw | tk | 5.77 | 0 / 2 / -4 | 0 / -19 / -5 | 294 |
| j39_rl_e | o | - |
| j39_rl_e | tk | 5.57 | -3 / 4 / 76 | 2 / 3 / 61 | 294 |
| j39_rl_l | o | - |
| j39_rl_l | tk | 6.07 | 14 / 0 / 56 | 21 / 40 / 63 | 250 |
| j39_lr | o | 5.77 | 16 / -7 / -24 | -10 / -44 / -24 | 294 |
| j39_lr | tk | 5.77 | 1 / 13 / -9 | -12 / -51 / -61 | 167 |
| j39_lw | o | - |
| j39_lw | tk | 5.77 | -3 / 5 / 10 | -6 / -11 / 8 | 294 |
| j38_cc90 | o | 6.12 | 65 / 58 / 25 | 61 / 74 / 63 | 245 |
| j38_cc90 | tk | 6.12 | 7 / 9 / -37 | -2 / -10 / 39 | 146 |

## 4. External effect vs planned velocity change

| run | max residual cm/s | Ext frames | families seen | worst slide |
|---|---|---|---|---|
| j39_rl tk | 5 | 0 | [0, 4] | 46.3 |

## 5. Frame-rate modes: worst slide cm o / tk (worst pop m/s2 o / tk)

| scenario | f120 | f30 | f120 |
|---|---|---|---|
| j39_rl | - / 46.3 (- / 184) | - / 25.3 (- / 63) | - / 46.3 (- / 184) |
| j39_rw | 12.9 / 7.6 (73 / 307) | 17.6 / 10.5 (26 / 73) | 12.9 / 7.6 (73 / 307) |
| j39_lr | 38.8 / 12.2 (89 / 117) | 12.0 / 7.2 (37 / 56) | 38.8 / 12.2 (89 / 117) |
| j38_cc90 | 21.5 / 9.6 (228 / 277) | 11.4 / 9.0 (71 / 37) | 21.5 / 9.6 (228 / 277) |
| mtf_jog | - / - (- / -) | - / - (- / -) | - / - (- / -) |
| jlean | - / - (- / -) | - / - (- / -) | - / - (- / -) |
| j38_c90r | - / - (- / -) | - / - (- / -) | - / - (- / -) |
| j38_c90l | - / - (- / -) | - / - (- / -) | - / - (- / -) |
| j39_push_plan | - / - (- / -) | - / - (- / -) | - / - (- / -) |
