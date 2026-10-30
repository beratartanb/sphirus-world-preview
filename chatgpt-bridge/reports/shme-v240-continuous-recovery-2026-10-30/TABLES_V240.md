# SHME V2.40: ölçüm tabloları

Tüm sayılar aynı build'in (oturum içi) sabit adım koşularından; 'o' = kayıtlı üretim, 'tkh' = aday (SHM239_Own 1 + SHM240_HeadOn 1). Kayma = en kötü yere basmış top kayması (cm, contact231).

## A. FPS kipleri (o / tkh)

| scenario | 30 (reg) o / tkh | 60 o / tkh | 20 o / tkh | real o / tkh |
|---|---|---|---|---|
| j39_rl | 27.3 / 78.9 | 51.6 / 57.5 | 28.5 / 28.6 | 16.9 / 30.2 |
| j39_rw | 9.2 / 10.3 | 23.0 / 6.7 | 15.3 / 8.3 | 23.9 / 8.2 |
| j39_lr | 10.2 / 6.3 | 45.3 / 10.1 | 15.3 / 7.0 | 6.0 / 9.7 |
| j38_cc90 | 12.8 / 7.0 | 19.5 / 8.8 | 20.1 / 13.4 | 11.0 / 7.2 |
| j40_rlw | 7.1 / 7.9 | 14.4 / 9.5 | 14.8 / 23.8 | 26.3 / 6.7 |
| j40_lrw | 5.5 / 10.9 | 45.3 / 11.7 | 13.8 / 15.1 | 7.8 / 6.4 |
| j39_push_plan | 0.0 / 26.5 | 7.4 / 33.0 | 9.5 / 30.7 | 25.6 / 41.7 |
| j40_wall | 27.7 / 43.4 | 19.8 / 31.8 | 18.5 / 21.2 | 26.2 / 21.5 |
| j38_c90r | 9.8 / 10.2 | 12.1 / 8.6 | 9.0 / 5.8 | 0.0 / 8.7 |
| j38_c90l | 6.8 / 0.0 | 15.0 / 5.8 | 6.4 / 6.3 | 56.0 / 15.3 |

## V2.39 vs V2.40 takeover at 120 FPS (first cause fixed; same scenarios; worst planted-ball slide cm)

| scenario | V2.39 tk 120 | V2.40 tk 120 (f120) | V2.40 production o 120 |
|---|---|---|---|
| j39_rw | 116.2 | 7.6 A_CT_Jog_Fwd | 12.9 A_CT_Jog_Fwd |
| j38_cc90 | 112.3 | 9.6 SHM239_Tk_R_P16_K1_Back | 21.5 SHM216_RevTurn_L_Rfoot |
| j39_rl | 57.5 | 46.3 A_LS_Jog_Left_Stop | - |
| j39_lr | - | 12.2 SHM214_RevPush_Rfoot | 38.8 SHM216_RevTurn_R_Lfoot |
| j39_lw | - | 11.3 SHM239_Tk_L_P22_K1_Back | - |
| j39_rl_e | - | 9.4 SHM237_JogStop_Bl_P16 | - |
| j39_rl_l | - | 11.9 A_CT_Jog_Fwd | - |
| j40_rlw | - | 8.7 A_CP2_Jog_Fwd_Start | 10.0 A_CP2_Jog_Fwd_Start |
| j40_lrw | - | 11.7 A_CT_Jog_Fwd | - |

## Wall contact during a planned cut (j40_wall; worst slide cm / first clips after contact)

| variant | 30 FPS | 120 FPS |
|---|---|---|
| production | 35.2 af_Stand_Idle_NaturalBaselin | - |
| tkh: forced stand DB | 43.1 af_Stand_Idle_NaturalBaselin | 35.8 af_Loco_Jog_FwdRight_AAMS |
| wst: forced stop DB | 25.7 af_Stand_Idle_NaturalBaselin | 22.6 SHM237_JogStop_Br_P14 |
| wof: Ext yield only, no forced search | 24.2 af_Stand_Idle_NaturalBaselin | 35.8 af_Loco_Jog_FwdRight_AAMS |

## External shove during a planned cut (j39_push_plan; worst slide cm)

| variant | 30 | 120 |
|---|---|---|
| o | 10.2 SHM238_Cut_R_P21 | 14.5 A_CT_Jog_FwdRight |
| tk | 21.6 A_CT_Jog_Fwd | 30.5 A_LS_Jog_Right_Stop |
| ext | 8.8 A_CT_Jog_Fwd | 30.2 A_LS_Jog_Right_Stop |
| tkh | 26.5 A_CT_Jog_Fwd | - |
| wst | 14.2 A_CT_Jog_Fwd | - |

# B. 30 FPS geniş regresyon (v240reg_*)

## 1. Worst planted-ball slide (cm, owner) and upper-body pops (count / worst m/s2), fixed 30 FPS: production o vs tkh; * = database-not-ready frames

| scenario | o | o owner | o pops | tkh | tkh owner | tkh pops |
|---|---|---|---|---|---|---|
| j40_rlw | 7.1 | A_CP2_Jog_Fwd_Start | 3 / 32 | 7.9 | SHM239_Tk_R_P21_K2_Opp | 3 / 45 |
| j40_lrw | 5.5 | A_CT_Jog_Fwd | 2 / 28 | 10.9 | A_CT_Jog_Fwd | 2 / 57 |
| j39_rl | 27.3 | A_LS_Jog_Left_Stop | 3 / 68 | 78.9 | A_LS_Jog_Left_Start | 5 / 72 |
| j39_rw | 9.2 | A_CT_Jog_FwdLeft | 1 / 26 | 10.3 | A_CT_Jog_Fwd | 3 / 73 |
| j39_rl_e | 6.3 | A_CT_Jog_Fwd | 1 / 32 | 9.0 | A_CT_Jog_Fwd | 2 / 42 |
| j39_rl_l | 31.7 | A_LS_Jog_Left_Stop | 5 / 43 | 7.1 | SHM237_JogStop_Bl_P17 | 3 / 35 |
| j39_lr | 10.2 | SHM238_Cut_L_P20 | 0 / 0 | 6.3 | SHM237_JogStop_Bl_P06 | 3 / 57 |
| j39_lw | 16.8 | A_CT_Jog_Fwd | 1 / 26 | 9.5 | SHM239_Tk_L_P20_K2_Back | 2 / 59 |
| j38_cc90 | 12.8 | A_CT_Jog_Fwd | 6 / 59 | 7.0 | SHM237_JogStop_Br_P03 | 3 / 38 |
| mtf_jog | 50.7 | SHM216_RevTurn_R_Lfoot | 5 / 43 | 48.9 | SHM216_RevTurn_R_Lfoot | 5 / 43 |
| jlean | 11.9 | SHM236_JogRev_F_B_P0 | 6 / 36 | 12.0 | A_CT_Jog_Fwd | 5 / 34 |
| j38_c90r | 9.8 | SHM238_Cut_R_P21 | 1 / 26 | 10.2 | SHM238_Cut_R_P21 | 1 / 26 |
| j38_c90l | 6.8 | SHM237_JogStop_Bl_P16 | 2 / 26 | 0.0 |  | 2 / 26 |
| j38_c90rb | 9.8 | SHM237_JogStop_Br_P12 | 0 / 0 | 8.1 | A_CT_Jog_Fwd | 1 / 31 |
| j38_c90lb | 0.0 |  | 2 / 27 | 6.3 | SHM237_JogStop_Bl_P08 | 2 / 28 |
| j38_c45r | 5.5 | A_CT_Jog_Fwd | 0 / 0 | 6.4 | A_CT_Jog_Fwd | 0 / 0 |
| j38_c135r | 9.7 | SHM236_JogRev_F_B_P29 | 0 / 0 | 9.8 | SHM236_JogRev_F_B_P29 | 0 / 0 |
| w38_c90r | 0.0 |  | 0 / 0 | 5.6 | A_LB_Walk_FwdRight | 0 / 0 |
| s38_c90r | 6.4 | SHM218_W2S_Lfoot_a | 5 / 48 | 6.3 | SHM218_W2S_Lfoot_a | 4 / 44 |
| j36_rsm | 7.1 | A_CT_Jog_Fwd | 0 / 0 | 0.0 |  | 0 / 0 |
| j36_stop | 0.0 |  | 0 / 0 | 0.0 |  | 0 / 0 |
| j36_stopr | 5.5 | SHM237_JogStop_Bl_P16 | 0 / 0 | 0.0 |  | 0 / 0 |
| j34_chain1 | 7.9 | A_CT_Jog_Fwd | 1 / 32 | 9.3 | A_RB_Jog_Rear | 1 / 32 |
| j35_rev | 9.3 | SHM236_JogRev_F_B_P21 | 2 / 38 | 9.3 | SHM236_JogRev_F_B_P21 | 2 / 37 |
| j30_rel_3450 | 10.3 | SHM236_JogRev_B_F_P1 | 2 / 33 | 10.3 | SHM236_JogRev_B_F_P1 | 2 / 33 |
| j36_sside | 22.2 | A_LS_Jog_Right_Start | 1 / 37 | 22.2 | A_LS_Jog_Right_Start | 1 / 37 |
| jstart | 83.0 | af_Loco_Jog_Start_TurnR045_R | 4 / 42 | 57.4 | af_Loco_Jog_Start_TurnR045_R | 3 / 36 |
| e29_chain | 6.4 | SHM218_W2S_Lfoot_a | 7 / 76 | 6.4 | SHM218_W2S_Lfoot_a | 6 / 76 |
| c29_combo | 15.4 | A_LB_Walk_Left | 0 / 0 | 8.8 | A_LB_Walk_Fwd | 0 / 0 |
| jdiag | 6.3 | A_CT_Jog_Fwd | 0 / 0 | 7.2 | A_CT_Jog_Fwd | 1 / 26 |
| wdiag | 13.0 | A_CR_Stand_M_Neutral_Walk_Pi | 1 / 26 | 10.2 | A_CT_Walk_RearLeft | 1 / 26 |
| wstart | 14.2 | SHM_StartTransfer_FR_Rfoot | 0 / 0 | 13.6 | af_Stand_Idle_NaturalBaselin | 0 / 0 |
| cam32_j90 | 11.2 | SHM237_JogStop_Br_P12 | 1 / 26 | 5.6 | A_CT_Jog_Fwd | 1 / 26 |
| chain_jogcut | 10.2 | SHM238_Cut_R_P10 | 1 / 26 | 13.2 | SHM238_Cut_L_P13 | 1 / 26 |
| ad_jog | 10.3 | SHM238_Cut_R_P10 | 4 / 27 | 26.3 | SHM231L_LoadRev_B_F_P7 | 1 / 26 |
| mt_jog | 14.4 | A_CT_Jog_Fwd | 0 / 0 | 23.6 | SHM238_Cut_L_P21 | 0 / 0 |
| j39_push_plan | 0.0 |  | 1 / 28 | 26.5 | A_CT_Jog_Fwd | 2 / 63 |
| j39_push_jog | 8.7 | A_CT_Jog_Fwd | 0 / 0 | 6.4 | A_CT_Jog_Fwd | 0 / 0 |

## 2. Control stages after each input change (s after the request frame; tk239)

| scenario | variant | input | first body reaction | first support | velocity transfer | stable heading |
|---|---|---|---|---|---|---|
| j40_rlw | o |   90 deg at 5.37 s (speed 250, heading    7) | - | 0.13 | 0.3 | - |
| j40_rlw | o |  -90 deg at 5.83 s (speed 186, heading   32) | - | 0.2 | 0.07 | - |
| j40_rlw | o |    0 deg at 6.33 s (speed 227, heading  -74) | 0.2 (head) | 0.1 | 0.4 | 0.7 |
| j40_rlw | o |    0 deg at 9.87 s (speed   4, heading    0) | - | - | 0.23 | 0.97 |
| j40_rlw | tkh |   90 deg at 5.37 s (speed 250, heading    7) | - | 0.13 | 0.3 | - |
| j40_rlw | tkh |  -90 deg at 5.83 s (speed 186, heading   32) | 0.5 (head) | 0.2 | 0.37 | - |
| j40_rlw | tkh |    0 deg at 6.33 s (speed  35, heading  -12) | - | 0.03 | 0.3 | 1.0 |
| j40_rlw | tkh |    0 deg at 9.87 s (speed   5, heading    0) | - | - | 0.2 | 0.97 |
| j40_lrw | o |  -90 deg at 5.37 s (speed 250, heading   -7) | 0.07 (head) | 0.13 | 0.47 | - |
| j40_lrw | o |   90 deg at 5.83 s (speed 120, heading  -30) | 0.07 (head) | 0.2 | 0.07 | 0.37 |
| j40_lrw | o |    0 deg at 6.33 s (speed 233, heading   90) | 0.03 (head) | 0.07 | 0.03 | 0.37 |
| j40_lrw | tkh |  -90 deg at 5.37 s (speed 250, heading   -7) | 0.07 (head) | 0.13 | 0.47 | - |
| j40_lrw | tkh |   90 deg at 5.83 s (speed 120, heading  -30) | 0.17 (head) | 0.2 | 0.37 | - |
| j40_lrw | tkh |    0 deg at 6.33 s (speed  46, heading   33) | 0.03 (head) | 0.03 | 0.23 | 0.9 |
| j39_rl | o |   90 deg at 5.37 s (speed 250, heading    7) | - | 0.13 | 0.3 | - |
| j39_rl | o |  -90 deg at 5.83 s (speed 186, heading   32) | 1.83 (head) | 0.2 | 0.07 | 0.6 |
| j39_rl | o | -162 deg at 9.87 s (speed   4, heading -162) | - | - | 0.23 | 0.97 |
| j39_rl | tkh |   90 deg at 5.37 s (speed 250, heading    7) | - | 0.13 | 0.3 | - |
| j39_rl | tkh |  -90 deg at 5.83 s (speed 184, heading   33) | 2.03 (head) | 0.13 | 0.83 | 1.8 |
| j39_rl | tkh | -143 deg at 9.87 s (speed   4, heading -143) | 0.23 (head) | - | 0.23 | 0.97 |
| j39_rw | o |   90 deg at 5.37 s (speed 250, heading    7) | - | 0.13 | 0.3 | - |
| j39_rw | o |    0 deg at 5.83 s (speed 186, heading   32) | 0.17 (head) | - | 0.6 | 0.93 |
| j39_rw | tkh |   90 deg at 5.37 s (speed 250, heading    7) | - | 0.13 | 0.3 | - |
| j39_rw | tkh |    0 deg at 5.83 s (speed 186, heading   32) | 0.17 (head) | 0.2 | 0.83 | 1.07 |
| j39_rl_e | o |   90 deg at 5.37 s (speed 250, heading    7) | - | 0.13 | - | - |
| j39_rl_e | o |  -90 deg at 5.63 s (speed 236, heading   14) | 0.03 (head) | 0.1 | 0.13 | 0.77 |
| j39_rl_e | tkh |   90 deg at 5.37 s (speed 250, heading    7) | - | 0.13 | - | - |
| j39_rl_e | tkh |  -90 deg at 5.63 s (speed 239, heading   14) | 1.43 (head) | 0.1 | 0.23 | 1.07 |
| j39_rl_l | o |   90 deg at 5.37 s (speed 250, heading    7) | - | 0.13 | 0.3 | - |
| j39_rl_l | o |  -90 deg at 6.13 s (speed 193, heading   70) | - | - | 0.33 | 1.57 |
| j39_rl_l | tkh |   90 deg at 5.37 s (speed 250, heading    7) | - | 0.13 | 0.3 | - |
| j39_rl_l | tkh |  -90 deg at 6.13 s (speed 193, heading   70) | 0.83 (head) | 0.3 | 0.67 | 1.73 |
| j39_lr | o |  -90 deg at 5.37 s (speed 250, heading   -7) | 0.1 (head) | 0.13 | - | - |
| j39_lr | o |   90 deg at 5.83 s (speed 149, heading  -11) | 0.07 (head) | 0.3 | 0.1 | 0.67 |
| j39_lr | tkh |  -90 deg at 5.37 s (speed 250, heading   -7) | 0.07 (head) | 0.13 | 0.47 | - |
| j39_lr | tkh |   90 deg at 5.83 s (speed 120, heading  -30) | 0.17 (head) | 0.2 | 0.37 | 1.23 |
| j39_lw | o |  -90 deg at 5.37 s (speed 250, heading   -7) | 0.07 (head) | 0.13 | 0.47 | - |
| j39_lw | o |    0 deg at 5.83 s (speed 120, heading  -30) | - | 0.2 | 0.57 | 1.07 |
| j39_lw | tkh |  -90 deg at 5.37 s (speed 250, heading   -7) | 0.07 (head) | 0.13 | 0.47 | - |
| j39_lw | tkh |    0 deg at 5.83 s (speed 120, heading  -30) | - | 0.2 | 0.6 | 0.83 |
| j38_cc90 | o |   90 deg at 5.37 s (speed 250, heading    7) | - | 0.13 | 0.3 | - |
| j38_cc90 | o |    0 deg at 6.17 s (speed 199, heading   72) | 0.2 (head) | - | 0.27 | - |
| j38_cc90 | o |  -90 deg at 6.97 s (speed 238, heading   12) | 0.17 (head) | - | 0.07 | 1.0 |
| j38_cc90 | tkh |   90 deg at 5.37 s (speed 250, heading    7) | - | 0.13 | 0.3 | - |
| j38_cc90 | tkh |    0 deg at 6.17 s (speed 196, heading   71) | 0.3 (head) | 0.27 | 0.67 | - |
| j38_cc90 | tkh |  -90 deg at 6.97 s (speed 175, heading   29) | 0.63 (head) | 0.1 | 0.1 | 1.17 |

## 3. Body alignment after the second request (yaw minus the velocity heading, deg; balance238)

| scenario | variant | second request s | pelvis / chest / head @+1.2 | @+1.8 | speed @+1.8 |
|---|---|---|---|---|---|
| j40_rlw | o | 5.83 | 11 / 32 / 13 | 3 / 6 / 4 | 299 |
| j40_rlw | tkh | 5.83 | -3 / 9 / 3 | 1 / -3 / 1 | 299 |
| j40_lrw | o | 5.83 | -7 / 1 / -3 | -9 / -1 / 0 | 299 |
| j40_lrw | tkh | 5.83 | -6 / 4 / 0 | -5 / 4 / 2 | 299 |
| j39_rl | o | 5.83 | 9 / 38 / 64 | 4 / 23 / 40 | 299 |
| j39_rl | tkh | 5.83 | 0 / -20 / 31 | 9 / 25 / 62 | 245 |
| j39_rw | o | 5.83 | 0 / -1 / 2 | 2 / -14 / 0 | 298 |
| j39_rw | tkh | 5.83 | 6 / 19 / 1 | 5 / 8 / 1 | 299 |
| j39_rl_e | o | 5.63 | 19 / 35 / 75 | 7 / 6 / 55 | 299 |
| j39_rl_e | tkh | 5.63 | 6 / 27 / 78 | 7 / 3 / 15 | 299 |
| j39_rl_l | o | 6.13 | 91 / 88 / 81 | -174 / 128 / 106 | 252 |
| j39_rl_l | tkh | 6.13 | 22 / 8 / 68 | 24 / 41 / 72 | 254 |
| j39_lr | o | 5.83 | -12 / -27 / -42 | -14 / -26 / -13 | 299 |
| j39_lr | tkh | 5.83 | -8 / -28 / -55 | -5 / -1 / -3 | 298 |
| j39_lw | o | 5.83 | -3 / 10 / 1 | -10 / -16 / 4 | 299 |
| j39_lw | tkh | 5.83 | -4 / 6 / 3 | -5 / 7 / 3 | 299 |
| j38_cc90 | o | 6.17 | 4 / 12 / 35 | 37 / 30 / 79 | 270 |
| j38_cc90 | tkh | 6.17 | 21 / 7 / 16 | 7 / -7 / 13 | 273 |

## 4. External effect vs planned velocity change

| run | max residual cm/s | Ext frames | families seen | worst slide |
|---|---|---|---|---|
| j39_push_plan o | 282 | 0 | [0, 4] | 0.0 |
| j39_push_plan tkh | 282 | 18 | [0, 4, 6] | 26.5 |
| j39_push_jog o | 0 | 0 | [0, 4] | 8.7 |
| j39_push_jog tkh | 0 | 0 | [0, 4] | 6.4 |
| j38_c90r o | 9 | 0 | [0, 4] | 9.8 |
| j38_c90r tkh | 9 | 0 | [0, 4] | 10.2 |
| j39_rl o | 11 | 0 | [0, 4] | 27.3 |
| j39_rl tkh | 20 | 0 | [0, 3, 4] | 78.9 |

# C. 120 FPS devralma (f120: once + edb + exit2, yield öncesi)

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
