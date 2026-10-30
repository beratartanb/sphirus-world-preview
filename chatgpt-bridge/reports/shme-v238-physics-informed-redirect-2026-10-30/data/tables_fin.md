## 1. Worst planted-ball slide (cm, owner clip) and upper-body pops (count / worst m/s2), fixed 30 FPS: production (o) vs pre238; * = database-not-ready frames

| scenario | o | o owner | o pops | pre238 | pre238 owner | pre238 pops |
|---|---|---|---|---|---|---|
| j38_c90r | 0.0 |  | 1 / 28 | 9.0 | A_CT_Jog_Fwd | 0 / 0 |
| j38_c90rb | 9.0 | A_CT_Jog_Fwd | 1 / 30 | 7.1 | A_CT_Jog_Fwd | 0 / 0 |
| j38_c90l | 0.0 |  | 2 / 26 | 8.9 | SHM237_JogStop_Br_P12 | 0 / 0 |
| j38_c90lb | 7.3 | A_CT_Jog_Fwd | 2 / 27 | 8.9 | A_CT_Jog_Fwd | 0 / 0 |
| j38_c45r | 5.3 | A_CT_Jog_Fwd | 0 / 0 | 5.1 | A_CT_Jog_Fwd | 0 / 0 |
| j38_c135r | 0.0 |  | 0 / 0 | 9.8 | SHM236_JogRev_F_B_P29 | 0 / 0 |
| j38_cc90 | 14.2 | SHM216_RevTurn_L_Rfoot | 5 / 72 | 15.9 | A_CT_Jog_FwdLeft | 0 / 0 |
| w38_c90r | 0.0 |  | 0 / 0 | 0.0 |  | 0 / 0 |
| s38_c90r | 6.4 | SHM218_W2S_Lfoot_a | 5 / 48 | 6.4 | SHM218_W2S_Lfoot_a | 3 / 47 |
| s38_c90l | - |  | - | - |  | - |
| jdiag | 6.3 | A_CT_Jog_Fwd | 0 / 0 | 6.3 | A_CT_Jog_Fwd | 0 / 0 |
| jswap | 36.4 | A_CT_Jog_FwdLeft | 1 / 26 | 36.4 | A_CT_Jog_FwdLeft | 0 / 0 |
| jlean | - |  | - | 25.9 | A_CT_Jog_Right | 3 / 36 |
| ad_jog | 18.4 | A_CT_Jog_Fwd | 4 / 27 | 16.2 | SHM231L_LoadRev_B_F_P23 | 2 / 48 |
| chain_jogcut | 10.1 | SHM238_Cut_L_P04 | 1 / 26 | 12.4 | A_CT_Jog_FwdLeft | 2 / 32 |
| mt_jog | 16.0 | A_CT_Jog_Fwd | 0 / 0 | 14.6 | A_CT_Jog_Fwd | 0 / 0 |
| mtf_jog | 48.9 | SHM216_RevTurn_R_Lfoot | 5 / 43 | 24.1 | SHM216_RevTurn_L_Rfoot | 6 / 48 |
| cam32_j90 | 6.6 | SHM238_Cut_R_P10 | 1 / 28 | 8.0 | A_CT_Jog_Fwd | 0 / 0 |
| j36_stop | 0.0 |  | 0 / 0 | 0.0 |  | 0 / 0 |
| j36_stopr | 0.0 |  | 0 / 0 | 0.0 |  | 0 / 0 |
| j36_rsm | 0.0 |  | 0 / 0 | 0.0 |  | 0 / 0 |
| j36_wjs | 0.0 |  | 0 / 0 | 6.6 | SHM237_JogStop_Br_P03 | 0 / 0 |
| j36_sside | 22.2 | A_LS_Jog_Right_Start | 1 / 37 | 15.0 | A_LS_Jog_Right_Start | 1 / 37 |
| j35_rev | 34.4 | A_CT_Jog_Fwd | 2 / 37 | 6.1 | SHM236_JogRev_B_F_P31 | 1 / 32 |
| j30_rel_3450 | 26.2 | A_CT_Jog_Fwd | 2 / 33 | 7.3 | A_CT_Jog_Fwd | 1 / 33 |
| j34_chain1 | 9.3 | A_RB_Jog_Rear | 1 / 32 | 7.5 | SHM236_JogRev_B_F_P23 | 1 / 32 |
| jstart | 57.4 | af_Loco_Jog_Start_TurnR045_R | 3 / 36 | 74.1 | af_Loco_Jog_Start_TurnR045_R | 4 / 42 |
| e29_chain | 43.9 | M_Neutral_Sprint_Turn_L_180_ | 8 / 44 | 6.4 | SHM218_W2S_Lfoot_a | 7 / 76 |
| c29_combo | 11.0 | A_CR_Stand_M_Neutral_Walk_Pi | 0 / 0 | 10.9 | A_CR_Stand_M_Neutral_Walk_Pi | 0 / 0 |
| ter_drop_jog | - |  | - | - |  | - |

## 2. Hard-turn balance read (balance238; yaw relative to the old heading, + = toward the turn)

| run | turn | heading 80 %% s | min speed | peak a after 0.1 s (mu_eff) | contacts 0-1.2 s | pel / chest / head @+1.0 | @+1.4 | turn clip |
|---|---|---|---|---|---|---|---|---|
| j38_c90r o | 90 | 0.833 | 176 | 527 (0.54) | 4 | 80 / 72 / 39 | 79 / 47 / 41 | SHM238_Cut_R_P10 |
| j38_c90r pre238 | 89 | 0.5 | 206 | 640 (0.65) | 4 | 81 / 64 / 12 | 85 / 51 / 20 | A_CT_Jog_Fwd, A_CT_Jog_FwdRight |
| j38_c90rb o | 90 | 0.834 | 162 | 657 (0.67) | 6 | 81 / 69 / 28 | 85 / 47 / 39 | SHM238_Cut_R_P05 |
| j38_c90rb pre238 | 89 | 0.5 | 206 | 626 (0.64) | 4 | 82 / 36 / 10 | 83 / 70 / 21 | A_CT_Jog_Fwd, A_CT_Jog_FwdRight |
| j38_c90l o | -90 | 0.666 | 115 | 561 (0.57) | 5 | 86 / 64 / 10 | 93 / 76 / 25 | SHM238_Cut_L_P20 |
| j38_c90l pre238 | -89 | 0.5 | 206 | 640 (0.65) | 5 | 92 / 71 / 0 | 89 / 81 / 15 | A_CT_Jog_Fwd, A_CT_Jog_FwdLeft |
| j38_c90lb o | -90 | 0.8 | 163 | 672 (0.69) | 7 | 86 / 82 / 22 | 91 / 61 / 28 | SHM238_Cut_L_P12 |
| j38_c90lb pre238 | -89 | 0.5 | 206 | 640 (0.65) | 3 | 85 / 54 / 2 | 91 / 86 / 13 | A_CT_Jog_Fwd, A_CT_Jog_FwdLeft |
| j38_c45r o | 45 | 0.466 | 279 | 485 (0.49) | 7 | 40 / 46 / 25 | 41 / 19 / 35 | A_CT_Jog_Fwd |
| j38_c45r pre238 | 45 | 0.466 | 279 | 485 (0.49) | 5 | 42 / 46 / 13 | 42 / 19 / 17 | A_CT_Jog_Fwd |
| j38_c135r o | 175 | 0.466 | 12 | 873 (0.89) | 4 | 3 / -5 / 2 | 6 / 16 / 4 | SHM236_JogRev_F_B_P29 |
| j38_c135r pre238 | 177 | 0.466 | 12 | 873 (0.89) | 4 | 3 / -5 / 2 | 6 / 15 / 4 | SHM236_JogRev_F_B_P29 |
| j38_cc90 o | 21 | 0.066 | 176 | 612 (0.62) | 6 | 65 / 62 / 21 | 9 / -20 / 16 | A_CT_Jog_Fwd, SHM238_Cut_R_P21 |
| j38_cc90 pre238 | 14 | 0.033 | 206 | 779 (0.79) | 4 | 36 / 14 / -9 | 9 / -6 / -10 | A_CT_Jog_Fwd, A_CT_Jog_FwdLeft, A_CT_Jog_FwdRight |

## 3. Frame-rate modes: worst slide cm o / pre238 (worst pop m/s2 o / pre238); * = database-not-ready frames

| scenario | 30 | 60 | 120 | 20 | real |
|---|---|---|---|---|---|
| j38_c90r | 0.0 / 9.0 (28 / 0) | 7.6 / 11.5 (45 / 37) | 14.5 / 12.2 (85 / 69) | 10.4 / 11.2 (0 / 0) | 9.6 / 10.2 (29 / 0) |
| j38_c90l | 0.0 / 8.9 (26 / 0) | - / 25.5 (- / 43) | 51.1 / 24.1 (73 / 75) | 5.9 / 28.0 (0 / 28) | 7.4 / - (0 / -) |
| j38_cc90 | 14.2 / 15.9 (72 / 0) | 16.4 / 39.6 (128 / 35) | 16.5 / 12.0 (72 / 62) | 19.9 / 9.2 (26 / 0) | 9.1 / 22.3 (99 / 29) |
| mtf_jog | 48.9 / 24.1 (43 / 48) | 34.8 / 26.0 (134 / 133) | 27.0 / 36.2 (237 / 238) | 26.2 / 26.8 (50 / 30) | 14.4 / 19.1 (52 / 65) |
| jlean | - / 25.9 (- / 36) | 63.7 / 27.3 (67 / 70) | 30.9 / 37.8 (308 / 197) | 9.8 / 17.4 (37 / 32) | 13.1 / 10.8 (41 / 62) |
| j36_rsm | 0.0 / 0.0 (0 / 0) | 6.7 / - (33 / -) | 7.0 / - (63 / -) | 0.0 / - (0 / -) | 10.0 / - (27 / -) |

## 4. Cold first use in the clean editor (production, no warm run)

| run | no-DB frames | worst cm | cut clip on the request |
|---|---|---|---|
| v238cold_j38_c90r_o_r1 | 0 | 10.7 | SHM238_Cut_R_P21 |
| v238cold_j38_c90l_o_r1 | 0 | 7.9 | SHM238_Cut_L_P20 |
