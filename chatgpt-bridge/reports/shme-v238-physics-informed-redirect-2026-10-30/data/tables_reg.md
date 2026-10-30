## 1. Worst planted-ball slide (cm, owner clip) and upper-body pops (count / worst m/s2), fixed 30 FPS: production (o) vs cut3; * = database-not-ready frames

| scenario | o | o owner | o pops | cut3 | cut3 owner | cut3 pops |
|---|---|---|---|---|---|---|
| j38_c90r | 12.7 | A_CT_Jog_Fwd | 0 / 0 | 0.0 |  | 1 / 26 |
| j38_c90l | 5.6 | A_CT_Jog_Fwd | 0 / 0 | 0.0 |  | 2 / 26 |
| j38_c45r | 6.4 | A_CT_Jog_Fwd | 0 / 0 | 9.0 | A_CT_Jog_Fwd | 0 / 0 |
| j38_c135r | 9.8 | SHM236_JogRev_F_B_P29 | 0 / 0 | 0.0 |  | 0 / 0 |
| j38_cc90 | 15.9 | A_CT_Jog_FwdLeft | 0 / 0 | 11.4 | A_CT_Jog_Fwd | 5 / 72 |
| w38_c90r | 0.0 |  | 0 / 0 | 10.5 | A_LB_Walk_FwdRight | 0 / 0 |
| s38_c90r | 5.3 | SHM233_Calm_A_LB_Sprint_Fwd | 3 / 47 | 5.3 | SHM233_Calm_A_LB_Sprint_Fwd | 5 / 48 |
| s38_c90l | 6.4 | SHM218_W2S_Lfoot_a | 7 / 35 | 6.3 | SHM218_W2S_Lfoot_a | 7 / 36 |
| jdiag | 5.6 | A_CT_Jog_Fwd | 0 / 0 | 7.4 | A_CT_Jog_Fwd | 0 / 0 |
| jswap | 36.4 | A_CT_Jog_FwdLeft | 0 / 0 | 36.4 | A_CT_Jog_FwdLeft | 0 / 0 |
| jlean | 25.9 | A_CT_Jog_Right | 3 / 37 | 11.9 | SHM236_JogRev_F_B_P0 | 6 / 36 |
| ad_jog | 16.2 | SHM231L_LoadRev_B_F_P23 | 2 / 48 | 17.8 | SHM231L_LoadRev_B_F_P31 | 4 / 27 |
| chain_jogcut | 12.2 | A_CT_Jog_Left | 2 / 32 | 10.3 | SHM238_Cut_R_P10 | 1 / 26 |
| mt_jog | 16.8 | A_CT_Jog_Fwd | 0 / 0 | 14.4 | A_CT_Jog_Fwd | 0 / 0 |
| mtf_jog | 25.5 | SHM216_RevTurn_L_Rfoot | 6 / 48 | 48.9 | SHM216_RevTurn_R_Lfoot | 5 / 43 |
| cam32_j90 | 12.2 | A_CT_Jog_FwdRight | 0 / 0 | 10.7 | SHM237_JogStop_Br_P12 | 1 / 26 |
| j36_stop | 0.0 |  | 0 / 0 | 0.0 |  | 0 / 0 |
| j36_stopr | 5.5 | SHM237_JogStop_Bl_P16 | 0 / 0 | 0.0 |  | 0 / 0 |
| j36_rsm | 10.4 | A_CT_Jog_Fwd | 0 / 0 | 0.0 |  | 0 / 0 |
| j36_wjs | 6.3 | A_CT_Jog_Fwd | 0 / 0 | 6.3 | A_CT_Jog_Fwd | 0 / 0 |
| j36_sside | 12.3 | A_LS_Jog_Right_Start | 1 / 38 | 22.2 | A_LS_Jog_Right_Start | 1 / 37 |
| j35_rev | 9.3 | SHM236_JogRev_F_B_P21 | 2 / 37 | 9.3 | SHM236_JogRev_F_B_P21 | 2 / 38 |
| j30_rel_3450 | 16.3 | SHM236_JogRev_B_F_P27 | 1 / 33 | 10.3 | SHM236_JogRev_B_F_P1 | 2 / 33 |
| j34_chain1 | 9.3 | A_RB_Jog_Rear | 1 / 32 | 9.3 | A_RB_Jog_Rear | 1 / 32 |
| jstart | 57.4 | af_Loco_Jog_Start_TurnR045_R | 3 / 36 | 57.4 | af_Loco_Jog_Start_TurnR045_R | 4 / 42 |
| e29_chain | 6.4 | SHM218_W2S_Lfoot_a | 7 / 76 | 6.4 | SHM218_W2S_Lfoot_a | 7 / 76 |
| c29_combo | 15.4 | A_LB_Walk_Left | 0 / 0 | 7.8 | A_CR_Stand_M_Neutral_Walk_Pi | 0 / 0 |
| ter_drop_jog | 0.0 |  | 3 / 261 | 0.0 |  | 3 / 261 |

## 2. Hard-turn balance read (balance238; yaw relative to the old heading, + = toward the turn)

| run | turn | heading 80 %% s | min speed | peak a after 0.1 s (mu_eff) | contacts 0-1.2 s | pel / chest / head @+1.0 | @+1.4 | turn clip |
|---|---|---|---|---|---|---|---|---|
| j38_c90r o | 89 | 0.5 | 206 | 640 (0.65) | 4 | 79 / 58 / 12 | 85 / 54 / 21 | A_CT_Jog_Fwd, A_CT_Jog_FwdRight |
| j38_c90r cut3 | 90 | 0.833 | 176 | 522 (0.53) | 5 | 80 / 74 / 38 | 80 / 48 / 40 | SHM238_Cut_R_P21 |
| j38_c90l o | -89 | 0.5 | 206 | 640 (0.65) | 4 | 89 / 65 / 1 | 89 / 85 / 16 | A_CT_Jog_Fwd, A_CT_Jog_FwdLeft |
| j38_c90l cut3 | -90 | 0.666 | 115 | 561 (0.57) | 5 | 86 / 64 / 10 | 93 / 76 / 25 | SHM238_Cut_L_P20 |
| j38_c45r o | 45 | 0.466 | 279 | 485 (0.49) | 6 | 40 / 46 / 13 | 41 / 16 / 15 | A_CT_Jog_Fwd |
| j38_c45r cut3 | 45 | 0.466 | 279 | 485 (0.49) | 6 | 40 / 46 / 25 | 41 / 19 / 35 | A_CT_Jog_Fwd |
| j38_c135r o | 175 | 0.466 | 12 | 873 (0.89) | 4 | 3 / -5 / 2 | 6 / 15 / 4 | SHM236_JogRev_F_B_P29 |
| j38_c135r cut3 | 175 | 0.466 | 12 | 873 (0.89) | 4 | 3 / -5 / 2 | 6 / 15 / 4 | SHM236_JogRev_F_B_P29 |
| j38_cc90 o | 14 | 0.033 | 206 | 779 (0.79) | 5 | 36 / 14 / -9 | 9 / -6 / -10 | A_CT_Jog_Fwd, A_CT_Jog_FwdLeft, A_CT_Jog_FwdRight |
| j38_cc90 cut3 | 21 | 0.066 | 176 | 613 (0.62) | 4 | 66 / 58 / 22 | 7 / -15 / 17 | A_CT_Jog_Fwd, SHM238_Cut_R_P10 |
