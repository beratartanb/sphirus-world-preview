## 1. Worst planted-ball slide (cm, owner clip) and upper-body pops (count / worst m/s2), fixed 30 FPS: production (o) vs pre238; * = database-not-ready frames

| scenario | o | o owner | o pops | pre238 | pre238 owner | pre238 pops |
|---|---|---|---|---|---|---|
| j38_c90r | 9.6 | SHM238_Cut_R_P21 | 1 / 26 | 12.5 | A_CT_Jog_FwdRight | 0 / 0 |
| j38_c90rb | 0.0 |  | 1 / 31 | 11.2 | A_CT_Jog_FwdRight | 0 / 0 |
| j38_c90l | 0.0 |  | 0 / 0 | 12.8 | A_CT_Jog_FwdLeft | 0 / 0 |
| j38_c90lb | 6.0 | SHM237_JogStop_Bl_P08 | 1 / 28 | 6.6 | A_CT_Jog_Fwd | 0 / 0 |
| j38_c45r | 6.4 | A_CT_Jog_Fwd | 0 / 0 | 5.3 | A_CT_Jog_Fwd | 0 / 0 |
| j38_c135r | 9.8 | SHM236_JogRev_F_B_P29 | 0 / 0 | 9.8 | SHM236_JogRev_F_B_P29 | 0 / 0 |
| j38_cc90 | 6.1 | SHM237_JogStop_Br_P11 | 5 / 71 | 15.9 | A_CT_Jog_FwdLeft | 0 / 0 |
| w38_c90r | 0.0 |  | 0 / 0 | 0.0 |  | 0 / 0 |
| s38_c90r | 11.1 | SHM218_W2S_Lfoot_a | 5 / 48 | 11.1 | SHM218_W2S_Lfoot_a | 3 / 47 |
| s38_c90l | 6.4 | SHM218_W2S_Lfoot_a | 7 / 36 | 6.4 | SHM218_W2S_Lfoot_a | 7 / 35 |
| jdiag | 7.2 | A_CT_Jog_Fwd | 0 / 0 | 6.3 | A_CT_Jog_Fwd | 0 / 0 |
| jswap | 36.4 | A_CT_Jog_FwdLeft | 0 / 0 | 36.4 | A_CT_Jog_FwdLeft | 0 / 0 |
| jlean | 12.0 | A_CT_Jog_Fwd | 6 / 36 | 25.9 | A_CT_Jog_Right | 3 / 36 |
| ad_jog | 10.2 | SHM238_Cut_R_P10 | 4 / 27 | 16.2 | SHM231L_LoadRev_B_F_P23 | 2 / 48 |
| chain_jogcut | 11.3 | SHM238_Cut_L_P13 | 1 / 26 | 12.5 | A_CT_Jog_Fwd | 2 / 32 |
| mt_jog | 14.4 | A_CT_Jog_Fwd | 0 / 0 | 17.7 | A_CT_Jog_Fwd | 0 / 0 |
| mtf_jog | 48.9 | SHM216_RevTurn_R_Lfoot | 4 / 43 | 24.1 | SHM216_RevTurn_L_Rfoot | 6 / 48 |
| cam32_j90 | 10.8 | SHM237_JogStop_Br_P12 | 1 / 26 | 11.8 | A_CT_Jog_Fwd | 0 / 0 |
| j36_stop | 0.0 |  | 0 / 0 | 9.0 | A_CT_Jog_Fwd | 0 / 0 |
| j36_stopr | 0.0 |  | 0 / 0 | 5.5 | SHM237_JogStop_Bl_P16 | 0 / 0 |
| j36_rsm | 10.4 | A_CT_Jog_Fwd | 0 / 0 | 0.0 |  | 0 / 0 |
| j36_wjs | 5.9 | SHM237_JogStop_Bl_P20 | 0 / 0 | 0.0 |  | 0 / 0 |
| j36_sside | 15.0 | A_LS_Jog_Right_Start | 1 / 37 | 15.8 | A_LS_Jog_Right_Start | 1 / 37 |
| j35_rev | 11.7 | SHM236_JogRev_F_B_P5 | 1 / 32 | 9.7 | SHM236_JogRev_B_F_P19 | 2 / 37 |
| j30_rel_3450 | 10.3 | SHM236_JogRev_B_F_P1 | 2 / 33 | 7.1 | SHM236_JogRev_B_F_P27 | 1 / 33 |
| j34_chain1 | 7.5 | SHM236_JogRev_B_F_P23 | 1 / 32 | 7.9 | A_CT_Jog_Fwd | 1 / 32 |
| jstart | 68.4 | af_Loco_Jog_Start_TurnR045_R | 4 / 42 | 83.0 | af_Loco_Jog_Start_TurnR045_R | 3 / 36 |
| e29_chain | 6.3 | SHM218_W2S_Lfoot_a | 7 / 76 | 11.1 | SHM218_W2S_Lfoot_a | 7 / 76 |
| c29_combo | 15.4 | A_LB_Walk_Left | 0 / 0 | 22.9 | A_LB_Walk_FwdLeft | 0 / 0 |
| wdiag | 0.0 |  | 1 / 26 | 12.3 | af_Stand_Idle_NaturalBaselin | 1 / 26 |
| wstart | 13.6 | SHM_StartTransfer_RL_Rfoot | 1 / 33 | 14.2 | SHM_StartTransfer_FR_Rfoot | 1 / 33 |
| ter_drop_jog | - |  | - | - |  | - |

## 2. Hard-turn balance read (balance238; yaw relative to the old heading, + = toward the turn)

| run | turn | heading 80 %% s | min speed | peak a after 0.1 s (mu_eff) | contacts 0-1.2 s | pel / chest / head @+1.0 | @+1.4 | turn clip |
|---|---|---|---|---|---|---|---|---|
| j38_c90r o | 90 | 0.833 | 176 | 522 (0.53) | 5 | 80 / 75 / 38 | 80 / 48 / 40 | SHM238_Cut_R_P21 |
| j38_c90r pre238 | 89 | 0.5 | 206 | 640 (0.65) | 5 | 81 / 64 / 12 | 85 / 51 / 20 | A_CT_Jog_Fwd, A_CT_Jog_FwdRight |
| j38_c90rb o | 90 | 0.834 | 162 | 657 (0.67) | 5 | 81 / 69 / 28 | 85 / 47 / 39 | SHM238_Cut_R_P05 |
| j38_c90rb pre238 | 89 | 0.5 | 206 | 626 (0.64) | 4 | 82 / 36 / 10 | 83 / 70 / 21 | A_CT_Jog_Fwd, A_CT_Jog_FwdRight |
| j38_c90l o | -90 | 0.766 | 116 | 558 (0.57) | 6 | 91 / 62 / 8 | 91 / 88 / 22 | SHM238_Cut_L_P20 |
| j38_c90l pre238 | -89 | 0.5 | 206 | 640 (0.65) | 4 | 89 / 65 / 1 | 89 / 85 / 16 | A_CT_Jog_Fwd, A_CT_Jog_FwdLeft |
| j38_c90lb o | -90 | 0.766 | 169 | 610 (0.62) | 5 | 83 / 85 / 25 | 87 / 55 / 29 | SHM238_Cut_L_P13 |
| j38_c90lb pre238 | -89 | 0.5 | 206 | 640 (0.65) | 3 | 85 / 54 / 2 | 91 / 86 / 13 | A_CT_Jog_Fwd, A_CT_Jog_FwdLeft |
| j38_c45r o | 45 | 0.466 | 279 | 485 (0.49) | 5 | 40 / 46 / 25 | 41 / 19 / 35 | A_CT_Jog_Fwd |
| j38_c45r pre238 | 45 | 0.466 | 279 | 485 (0.49) | 7 | 40 / 46 / 13 | 41 / 16 / 15 | A_CT_Jog_Fwd |
| j38_c135r o | 177 | 0.466 | 12 | 873 (0.89) | 4 | 3 / -5 / 2 | 6 / 15 / 4 | SHM236_JogRev_F_B_P29 |
| j38_c135r pre238 | 177 | 0.466 | 12 | 873 (0.89) | 4 | 3 / -5 / 2 | 6 / 15 / 4 | SHM236_JogRev_F_B_P29 |
| j38_cc90 o | 21 | 0.066 | 176 | 612 (0.62) | 8 | 66 / 60 / 21 | 8 / -13 / 16 | A_CT_Jog_Fwd, SHM238_Cut_R_P21 |
| j38_cc90 pre238 | 14 | 0.033 | 206 | 779 (0.79) | 3 | 36 / 14 / -9 | 9 / -6 / -10 | A_CT_Jog_Fwd, A_CT_Jog_FwdLeft, A_CT_Jog_FwdRight |

## 3. Frame-rate modes: worst slide cm o / pre238 (worst pop m/s2 o / pre238); * = database-not-ready frames

| scenario | 30 | 60 | 120 | 20 | real |
|---|---|---|---|---|---|
| j38_c90r | 9.6 / 12.5 (26 / 0) | 12.1 / 11.6 (52 / 33) | 8.3 / 12.8 (85 / 69) | - | 8.8 / 11.5 (31 / 0) |
| j38_c90l | 0.0 / 12.8 (0 / 0) | 37.6 / 27.2 (45 / 45) | 9.0 / 24.1 (83 / 74) | - | 8.2 / 8.8 (0 / 37) |
| j35_rev | 11.7 / 9.7 (32 / 37) | 12.3 / 15.7 (75 / 62) | 19.9 / 21.3 (146 / 146) | - | 8.0 / 8.5 (30 / 35) |
| j30_rel_3450 | 10.3 / 7.1 (33 / 33) | 13.8 / 13.4 (67 / 78) | 8.7 / 8.7 (133 / 132) | - | 13.3 / 6.3 (30 / 53) |
| e29_chain | 6.3 / 11.1 (76 / 76) | 19.8 / 20.6 (155 / 155) | 17.3 / 17.6 (146 / 146) | - | 6.3 / 25.9 (86 / 69) |
| w38_c90r | 0.0 / 0.0 (0 / 0) | 6.2 / 0.0 (30 / 30) | 11.4 / 10.3 (81 / 82) | - | 8.2 / 0.0 (0 / 0) |
| jlean | 12.0 / 25.9 (36 / 36) | 14.7 / 27.3 (73 / 70) | 40.1 / 27.7 (298 / 197) | - | 9.7 / 46.7 (35 / 61) |

## 4. Cold first use in the clean editor (production, no warm run)

| run | no-DB frames | worst cm | cut clip on the request |
|---|---|---|---|
| v238cold4_j38_c90r_o_r1 | 0 | 0.0 | SHM238_Cut_R_P21 |
| v238cold4_j38_c90l_o_r1 | 0 | 6.8 | SHM238_Cut_L_P20 |
