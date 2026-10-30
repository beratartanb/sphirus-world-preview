## 1. Worst planted-ball slide (cm, owner clip) and upper-body pops (count / worst m/s2), fixed 30 FPS: production (o) vs pre238; * = database-not-ready frames

| scenario | o | o owner | o pops | pre238 | pre238 owner | pre238 pops |
|---|---|---|---|---|---|---|
| j38_c90r | 0.0 |  | 1 / 26 | 12.7 | A_CT_Jog_Fwd | 0 / 0 |
| j38_c90rb | 7.3 | SHM238_Cut_R_P05 | 1 / 30 | 11.2 | A_CT_Jog_FwdRight | 0 / 0 |
| j38_c90l | 6.8 | SHM237_JogStop_Bl_P16 | 2 / 26 | 12.8 | A_CT_Jog_FwdLeft | 0 / 0 |
| j38_c90lb | 0.0 |  | 1 / 27 | 8.9 | A_CT_Jog_Fwd | 0 / 0 |
| j38_c45r | 0.0 |  | 0 / 0 | 6.4 | A_CT_Jog_Fwd | 0 / 0 |
| j38_c135r | 0.0 |  | 0 / 0 | 0.0 |  | 0 / 0 |
| j38_cc90 | 11.6 | A_CT_Jog_Fwd | 5 / 65 | 15.4 | A_CT_Jog_FwdLeft | 0 / 0 |
| w38_c90r | 5.1 | A_LB_Walk_FwdRight | 0 / 0 | 0.0 |  | 0 / 0 |
| s38_c90r | 6.4 | SHM218_W2S_Lfoot_a | 5 / 48 | 11.1 | SHM218_W2S_Lfoot_a | 3 / 47 |
| s38_c90l | 6.4 | SHM218_W2S_Lfoot_a | 7 / 36 | 11.1 | SHM218_W2S_Lfoot_a | 7 / 35 |
| jdiag | 7.2 | A_CT_Jog_Fwd | 0 / 0 | 7.2 | A_CT_Jog_Fwd | 0 / 0 |
| jswap | 36.4 | A_CT_Jog_FwdLeft | 0 / 0 | 36.4 | A_CT_Jog_FwdLeft | 0 / 0 |
| jlean | 11.9 | SHM236_JogRev_F_B_P0 | 6 / 36 | 28.2 | A_CT_Jog_Fwd | 3 / 37 |
| ad_jog | 9.7 | SHM238_Cut_R_P10 | 4 / 27 | 16.2 | SHM231L_LoadRev_B_F_P23 | 2 / 48 |
| chain_jogcut | 11.8 | SHM238_Cut_L_P13 | 1 / 26 | 12.2 | A_CT_Jog_Fwd | 2 / 32 |
| mt_jog | 23.6 | SHM238_Cut_L_P21 | 0 / 0 | 17.7 | A_CT_Jog_Fwd | 0 / 0 |
| mtf_jog | 48.9 | SHM216_RevTurn_R_Lfoot | 5 / 43 | 13.2 | A_CT_Jog_Fwd | 7 / 48 |
| cam32_j90 | 10.8 | SHM237_JogStop_Br_P12 | 1 / 26 | 12.2 | A_CT_Jog_FwdRight | 0 / 0 |
| j36_stop | 9.0 | A_CT_Jog_Fwd | 0 / 0 | 0.0 |  | 0 / 0 |
| j36_stopr | 0.0 |  | 0 / 0 | 5.5 | SHM237_JogStop_Bl_P16 | 0 / 0 |
| j36_rsm | 9.0 | A_CT_Jog_Fwd | 0 / 0 | 0.0 |  | 0 / 0 |
| j36_wjs | 7.8 | A_LB_Walk_Fwd | 0 / 0 | 8.9 | SHM237_JogStop_Bl_P09 | 0 / 0 |
| j36_sside | 22.2 | A_LS_Jog_Right_Start | 1 / 37 | 22.2 | A_LS_Jog_Right_Start | 1 / 38 |
| j35_rev | 9.3 | SHM236_JogRev_F_B_P21 | 2 / 38 | 33.7 | A_CT_Jog_Fwd | 2 / 38 |
| j30_rel_3450 | 16.3 | SHM236_JogRev_B_F_P27 | 1 / 33 | 10.3 | SHM236_JogRev_B_F_P1 | 2 / 33 |
| j34_chain1 | 9.3 | A_RB_Jog_Rear | 1 / 32 | 9.3 | A_RB_Jog_Rear | 1 / 32 |
| jstart | 82.9 | af_Loco_Jog_Start_TurnR045_R | 4 / 42 | 83.0 | af_Loco_Jog_Start_TurnR045_R | 4 / 42 |
| e29_chain | 6.4 | SHM218_W2S_Lfoot_a | 7 / 76 | 6.4 | SHM218_W2S_Lfoot_a | 7 / 76 |
| c29_combo | 15.4 | A_LB_Walk_Left | 0 / 0 | 11.0 | A_CR_Stand_M_Neutral_Walk_Pi | 0 / 0 |
| wdiag | 10.2 | A_CT_Walk_RearLeft | 1 / 26 | 12.5 | A_CR_Stand_M_Neutral_Walk_Pi | 1 / 26 |
| wstart | 17.0 | SHM_M_Neutral_Walk_Stop_FL_R | 1 / 32 | 14.2 | SHM_StartTransfer_FR_Rfoot | 0 / 0 |
| ter_drop_jog | - |  | - | - |  | - |

## 2. Hard-turn balance read (balance238; yaw relative to the old heading, + = toward the turn)

| run | turn | heading 80 %% s | min speed | peak a after 0.1 s (mu_eff) | contacts 0-1.2 s | pel / chest / head @+1.0 | @+1.4 | turn clip |
|---|---|---|---|---|---|---|---|---|
| j38_c90r o | 90 | 0.833 | 176 | 522 (0.53) | 6 | 80 / 75 / 38 | 80 / 48 / 40 | SHM238_Cut_R_P21 |
| j38_c90r pre238 | 89 | 0.5 | 206 | 640 (0.65) | 4 | 81 / 64 / 12 | 85 / 51 / 20 | A_CT_Jog_Fwd, A_CT_Jog_FwdRight |
| j38_c90rb o | 90 | 0.834 | 162 | 657 (0.67) | 4 | 81 / 69 / 28 | 85 / 47 / 39 | SHM238_Cut_R_P05 |
| j38_c90rb pre238 | 89 | 0.5 | 206 | 626 (0.64) | 3 | 82 / 36 / 10 | 83 / 70 / 21 | A_CT_Jog_Fwd, A_CT_Jog_FwdRight |
| j38_c90l o | -90 | 0.666 | 115 | 561 (0.57) | 6 | 86 / 64 / 10 | 93 / 76 / 25 | SHM238_Cut_L_P20 |
| j38_c90l pre238 | -89 | 0.5 | 206 | 640 (0.65) | 4 | 89 / 65 / 1 | 89 / 85 / 16 | A_CT_Jog_Fwd, A_CT_Jog_FwdLeft |
| j38_c90lb o | -90 | 0.766 | 169 | 610 (0.62) | 5 | 83 / 85 / 25 | 87 / 55 / 29 | SHM238_Cut_L_P13 |
| j38_c90lb pre238 | -89 | 0.5 | 206 | 640 (0.65) | 3 | 85 / 54 / 2 | 91 / 86 / 13 | A_CT_Jog_Fwd, A_CT_Jog_FwdLeft |
| j38_c45r o | 45 | 0.466 | 279 | 485 (0.49) | 7 | 40 / 46 / 25 | 41 / 19 / 35 | A_CT_Jog_Fwd |
| j38_c45r pre238 | 45 | 0.466 | 279 | 485 (0.49) | 6 | 40 / 46 / 13 | 41 / 16 / 15 | A_CT_Jog_Fwd |
| j38_c135r o | 177 | 0.466 | 12 | 873 (0.89) | 4 | 3 / -5 / 2 | 6 / 15 / 4 | SHM236_JogRev_F_B_P29 |
| j38_c135r pre238 | 177 | 0.466 | 12 | 873 (0.89) | 4 | 3 / -5 / 2 | 6 / 15 / 4 | SHM236_JogRev_F_B_P29 |
| j38_cc90 o | 21 | 0.066 | 176 | 612 (0.62) | 5 | 67 / 63 / 21 | 10 / -17 / 17 | A_CT_Jog_Fwd, SHM238_Cut_R_P21 |
| j38_cc90 pre238 | 14 | 0.033 | 206 | 779 (0.79) | 4 | 36 / 14 / -9 | 9 / -6 / -10 | A_CT_Jog_Fwd, A_CT_Jog_FwdLeft, A_CT_Jog_FwdRight |

## 3. Frame-rate modes: worst slide cm o / pre238 (worst pop m/s2 o / pre238); * = database-not-ready frames

| scenario | 30 | 60 | 120 | 20 | real |
|---|---|---|---|---|---|
| j38_c90r | 0.0 / 12.7 (26 / 0) | - / - (- / -) | - / - (- / -) | - | - / - (- / -) |
| j38_c90l | 6.8 / 12.8 (26 / 0) | - / - (- / -) | - / - (- / -) | - | - / - (- / -) |
| j35_rev | 9.3 / 33.7 (38 / 38) | - / - (- / -) | - / - (- / -) | - | - / - (- / -) |
| j30_rel_3450 | 16.3 / 10.3 (33 / 33) | - / - (- / -) | - / - (- / -) | - | - / - (- / -) |
| e29_chain | 6.4 / 6.4 (76 / 76) | - / - (- / -) | - / - (- / -) | - | - / - (- / -) |
| w38_c90r | 5.1 / 0.0 (0 / 0) | - / - (- / -) | - / - (- / -) | - | - / - (- / -) |
| jlean | 11.9 / 28.2 (36 / 37) | - / - (- / -) | - / - (- / -) | - | - / - (- / -) |

## 4. Cold first use in the clean editor (production, no warm run)

| run | no-DB frames | worst cm | cut clip on the request |
|---|---|---|---|
| v238cold3_j38_c90r_o_r1 | 0 | 10.2 | SHM238_Cut_R_P21 |
| v238cold3_j38_c90l_o_r1 | 0 | 8.6 | SHM238_Cut_L_P20 |
