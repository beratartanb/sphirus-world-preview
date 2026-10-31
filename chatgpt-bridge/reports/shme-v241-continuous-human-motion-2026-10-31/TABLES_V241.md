# SHME V2.41 tabloları

Her değer sabit adımlı editör PIE'si (LTP). `o` = kayıtlı üretim; `tkha` (30 FPS) / `tkhaB` (FPS blokları) = Own + HeadOn + KOn + bölgesel AO (bellek içi PRE, her blokta `PREAO241 set 1` doğrulandı); `tkp*` = + PushYawK 0.15; `wst` = tkh + V2.37 JogStop engel DB'si; `wsto` = wst + BlkOnce; `aoh` = yalnız AO. Kayma = basılı top SLIP/DRAG sapması (contact231, > 4 cm), cm. Not: aynı build'de bile koşular ilk adımda ayrışabiliyor (REPORT §5); kapısız senaryolarda o–aday farkı aynı fiziksel durum değildir.

## 1. (30 FPS) Worst planted-ball slide (cm, owner) and upper-body pops (count / worst m/s2), fixed 30 FPS: production o vs tkha; * = database-not-ready frames

| scenario | o | o owner | o pops | tkha | tkha owner | tkha pops |
|---|---|---|---|---|---|---|
| j40_rlw | 21.9 | A_CP2_Jog_Fwd_Start | 3 / 32 | 7.3 | SHM237_JogStop_Bl_P08 | 4 / 33 |
| j40_lrw | 26.8 | SHM238_Cut_L_P20 | 1 / 31 | 10.8 | A_CT_Jog_Fwd | 2 / 58 |
| j39_rl | 39.7 | A_LS_Jog_Left_Stop | 3 / 68 | 25.0 | A_LS_Jog_Left_Stop | 6 / 64 |
| j39_rw | 7.2 | SHM237_JogStop_Br_P14 | 1 / 26 | 8.9 | A_CT_Jog_Fwd | 3 / 76 |
| j39_rl_e | 0.0 |  | 1 / 29 | 7.0* | A_CT_Jog_Fwd | 3 / 49 |
| j39_rl_l | 31.7 | A_LS_Jog_Left_Stop | 5 / 43 | 8.3* | A_CT_Jog_Fwd | 3 / 33 |
| j39_lr | 16.1 | SHM216_RevTurn_L_Lfoot | 3 / 36 | 7.7 | A_CT_Jog_Fwd | 1 / 59 |
| j39_lw | 11.1 | A_CT_Jog_Fwd | 1 / 26 | 5.7* | SHM237_JogStop_Bl_P17 | 2 / 70 |
| j38_cc90 | 12.2 | A_CT_Jog_Fwd | 6 / 66 | 7.0 | SHM237_JogStop_Br_P03 | 3 / 38 |
| mtf_jog | 50.7 | SHM216_RevTurn_R_Lfoot | 5 / 43 | 48.9 | SHM216_RevTurn_R_Lfoot | 5 / 43 |
| jlean | 11.9 | SHM236_JogRev_F_B_P0 | 6 / 36 | 25.2 | SHM236_JogRev_B_F_P18 | 4 / 39 |
| j38_c90r | 9.7 | SHM238_Cut_R_P21 | 1 / 26 | 0.0 |  | 1 / 28 |
| j38_c90l | 7.3 | SHM237_JogStop_Br_P03 | 0 / 0 | 7.3 | SHM237_JogStop_Br_P03 | 1 / 26 |
| j38_c90rb | 7.7 | A_CT_Jog_Fwd | 0 / 0 | 0.0 |  | 1 / 35 |
| j38_c90lb | 0.0 |  | 2 / 27 | 0.0 |  | 2 / 27 |
| j38_c45r | 6.4 | A_CT_Jog_Fwd | 0 / 0 | 0.0 |  | 0 / 0 |
| j38_c135r | 9.7 | SHM236_JogRev_F_B_P29 | 0 / 0 | 0.0 |  | 0 / 0 |
| w38_c90r | 0.0 |  | 0 / 0 | 5.1 | A_LB_Walk_FwdRight | 0 / 0 |
| s38_c90r | 6.4 | SHM218_W2S_Lfoot_a | 5 / 48 | 14.0 | SHM216_Cut_R_090_Lfoot | 4 / 44 |
| j36_rsm | 0.0 |  | 0 / 0 | 0.0 |  | 0 / 0 |
| j36_stop | 7.7 | A_CT_Jog_Fwd | 0 / 0 | 0.0 |  | 0 / 0 |
| j36_stopr | 0.0 |  | 0 / 0 | 5.5 | SHM237_JogStop_Bl_P16 | 0 / 0 |
| j34_chain1 | 7.5 | SHM236_JogRev_B_F_P23 | 1 / 32 | 7.5 | SHM236_JogRev_B_F_P23 | 1 / 32 |
| j35_rev | 10.2 | SHM236_JogRev_B_F_P31 | 1 / 32 | 34.5 | A_CT_Jog_Fwd | 2 / 38 |
| j30_rel_3450 | 11.1 | SHM236_JogRev_B_F_P27 | 1 / 33 | 16.3 | SHM236_JogRev_B_F_P27 | 1 / 33 |
| j36_sside | 20.5 | A_LS_Jog_Right_Start | 1 / 37 | 13.6 | A_LS_Jog_Right_Start | 1 / 37 |
| jstart | 64.9 | af_Loco_Jog_Start_TurnR045_R | 4 / 42 | 83.0 | af_Loco_Jog_Start_TurnR045_R | 4 / 41 |
| e29_chain | 11.1 | SHM218_W2S_Lfoot_a | 7 / 76 | 11.1 | SHM218_W2S_Lfoot_a | 6 / 76 |
| c29_combo | 15.4 | A_LB_Walk_Left | 0 / 0 | 15.5 | A_LB_Walk_Left | 1 / 28 |
| jdiag | 5.2 | A_CT_Jog_Fwd | 0 / 0 | 7.2 | A_CT_Jog_Fwd | 1 / 26 |
| wdiag | 10.2 | A_CT_Walk_RearLeft | 1 / 26 | 12.1 | A_CR_Stand_M_Neutral_Walk_Pi | 1 / 26 |
| wstart | 14.2 | SHM_StartTransfer_FR_Rfoot | 0 / 0 | 14.2 | SHM_StartTransfer_FR_Rfoot | 0 / 0 |
| cam32_j90 | 10.2 | SHM238_Cut_R_P21 | 1 / 26 | 10.8 | SHM237_JogStop_Br_P12 | 1 / 26 |
| chain_jogcut | 10.1 | SHM238_Cut_L_P04 | 1 / 26 | 6.4 | A_CT_Jog_Fwd | 1 / 26 |
| ad_jog | 16.1 | A_CT_Jog_Fwd | 4 / 27 | 11.3 | SHM231L_LoadRev_B_F_P26 | 2 / 29 |
| mt_jog | 9.1 | A_CT_Jog_Fwd | 0 / 0 | 14.5 | A_CT_Jog_Fwd | 0 / 0 |
| j39_push_plan | 0.0 |  | 1 / 28 | 21.6 | A_CP2_Jog_Left_Pivot | 1 / 36 |
| j39_push_jog | 7.2 | A_CT_Jog_Fwd | 0 / 0 | 17.3 | SHM_Rec_FL_Lfoot | 1 / 25 |

## 2. Control stages after each input change (s after the request frame; tk239)

| scenario | variant | input | first body reaction | first support | velocity transfer | stable heading |
|---|---|---|---|---|---|---|
| j40_rlw | o |   90 deg at 5.37 s (speed 250, heading    7) | - | 0.13 | 0.3 | - |
| j40_rlw | o |  -90 deg at 5.83 s (speed 186, heading   32) | - | 0.2 | 0.07 | - |
| j40_rlw | o |    0 deg at 6.33 s (speed 227, heading  -74) | 0.2 (head) | 0.1 | 0.4 | 0.7 |
| j40_rlw | o |    0 deg at 9.87 s (speed   4, heading    0) | - | - | 0.23 | 0.97 |
| j40_rlw | tkha |   90 deg at 5.37 s (speed 250, heading    7) | - | 0.13 | 0.3 | - |
| j40_rlw | tkha |  -90 deg at 5.83 s (speed 184, heading   33) | - | 0.2 | 0.33 | - |
| j40_rlw | tkha |    0 deg at 6.33 s (speed  28, heading  -18) | - | 0.03 | 0.3 | 1.03 |
| j40_rlw | tkha |    0 deg at 9.87 s (speed   5, heading    0) | - | - | 0.2 | 0.97 |
| j40_lrw | o |  -90 deg at 5.37 s (speed 250, heading   -7) | 0.1 (head) | 0.13 | - | - |
| j40_lrw | o |   90 deg at 5.83 s (speed 149, heading  -11) | 0.07 (head) | 0.3 | 0.1 | 0.4 |
| j40_lrw | o |    0 deg at 6.33 s (speed 219, heading   89) | 0.1 (head) | 0.13 | 0.1 | 0.47 |
| j40_lrw | tkha |  -90 deg at 5.37 s (speed 250, heading   -7) | 0.07 (head) | 0.13 | 0.47 | - |
| j40_lrw | tkha |   90 deg at 5.83 s (speed 120, heading  -30) | 0.17 (head) | 0.2 | 0.37 | - |
| j40_lrw | tkha |    0 deg at 6.33 s (speed  46, heading   33) | 0.07 (head) | 0.03 | 0.23 | 0.9 |
| j39_rl | o |   90 deg at 5.37 s (speed 250, heading    7) | - | 0.13 | 0.3 | - |
| j39_rl | o |  -90 deg at 5.83 s (speed 186, heading   32) | 1.83 (head) | 0.2 | 0.07 | 0.6 |
| j39_rl | o | -162 deg at 9.87 s (speed   4, heading -162) | - | - | 0.23 | 0.97 |
| j39_rl | tkha |   90 deg at 5.37 s (speed 250, heading    7) | - | 0.13 | 0.3 | - |
| j39_rl | tkha |  -90 deg at 5.83 s (speed 184, heading   33) | 0.7 (head) | 0.2 | 0.33 | 1.17 |
| j39_rl | tkha | -158 deg at 9.87 s (speed   5, heading -158) | - | - | 0.23 | 0.97 |
| j39_rw | o |   90 deg at 5.37 s (speed 250, heading    7) | - | 0.13 | 0.3 | - |
| j39_rw | o |    0 deg at 5.83 s (speed 186, heading   32) | 0.17 (head) | - | 0.6 | 0.93 |
| j39_rw | tkha |   90 deg at 5.37 s (speed 250, heading    7) | - | 0.13 | 0.3 | - |
| j39_rw | tkha |    0 deg at 5.83 s (speed 183, heading   33) | 0.17 (head) | 0.2 | 0.8 | 1.03 |
| j39_rl_e | o |   90 deg at 5.37 s (speed 250, heading    7) | - | 0.13 | - | - |
| j39_rl_e | o |  -90 deg at 5.63 s (speed 239, heading   14) | 0.03 (head) | 0.1 | 0.13 | 0.77 |
| j39_rl_e | tkha |   90 deg at 5.37 s (speed 250, heading    7) | - | 0.13 | - | - |
| j39_rl_e | tkha |  -90 deg at 5.63 s (speed 236, heading   14) | 1.6 (head) | 0.1 | 0.4 | 1.27 |
| j39_rl_l | o |   90 deg at 5.37 s (speed 250, heading    7) | - | 0.13 | 0.3 | - |
| j39_rl_l | o |  -90 deg at 6.13 s (speed 193, heading   70) | - | - | 0.33 | 1.57 |
| j39_rl_l | tkha |   90 deg at 5.37 s (speed 250, heading    7) | - | 0.13 | 0.3 | - |
| j39_rl_l | tkha |  -90 deg at 6.13 s (speed 191, heading   69) | 1.93 (head) | 0.3 | 0.63 | 1.7 |
| j39_lr | o |  -90 deg at 5.37 s (speed 250, heading   -7) | 0.07 (head) | 0.13 | 0.47 | - |
| j39_lr | o |   90 deg at 5.83 s (speed 120, heading  -30) | 0.07 (head) | 0.2 | 0.07 | 0.6 |
| j39_lr | tkha |  -90 deg at 5.37 s (speed 250, heading   -7) | 0.1 (head) | 0.13 | - | - |
| j39_lr | tkha |   90 deg at 5.83 s (speed 149, heading  -11) | 0.37 (head) | 0.3 | 0.53 | 1.33 |
| j39_lw | o |  -90 deg at 5.37 s (speed 250, heading   -7) | 0.07 (head) | 0.13 | 0.47 | - |
| j39_lw | o |    0 deg at 5.83 s (speed 120, heading  -30) | - | 0.2 | 0.57 | 1.07 |
| j39_lw | tkha |  -90 deg at 5.37 s (speed 250, heading   -7) | 0.07 (head) | 0.13 | 0.47 | - |
| j39_lw | tkha |    0 deg at 5.83 s (speed 120, heading  -30) | - | 0.2 | 0.63 | 0.83 |
| j38_cc90 | o |   90 deg at 5.37 s (speed 250, heading    7) | - | 0.13 | 0.3 | - |
| j38_cc90 | o |    0 deg at 6.17 s (speed 199, heading   72) | 0.2 (head) | - | 0.27 | - |
| j38_cc90 | o |  -90 deg at 6.97 s (speed 238, heading   12) | 0.23 (head) | - | 0.07 | 1.0 |
| j38_cc90 | tkha |   90 deg at 5.37 s (speed 250, heading    7) | - | 0.13 | 0.3 | - |
| j38_cc90 | tkha |    0 deg at 6.17 s (speed 196, heading   71) | 0.33 (head) | 0.27 | 0.67 | - |
| j38_cc90 | tkha |  -90 deg at 6.97 s (speed 175, heading   29) | 0.67 (head) | 0.1 | 0.1 | 1.17 |

## 3. Body alignment after the second request (yaw minus the velocity heading, deg; balance238)

| scenario | variant | second request s | pelvis / chest / head @+1.2 | @+1.8 | speed @+1.8 |
|---|---|---|---|---|---|
| j40_rlw | o | 5.83 | 11 / 32 / 13 | 3 / 6 / 4 | 299 |
| j40_rlw | tkha | 5.83 | -3 / 11 / 3 | 1 / -1 / 3 | 299 |
| j40_lrw | o | 5.83 | -10 / -2 / -5 | -11 / -11 / 2 | 299 |
| j40_lrw | tkha | 5.83 | -5 / 5 / 0 | -5 / 4 / 2 | 299 |
| j39_rl | o | 5.83 | 9 / 38 / 64 | 4 / 23 / 40 | 299 |
| j39_rl | tkha | 5.83 | -2 / 12 / 22 | 1 / 0 / 2 | 299 |
| j39_rw | o | 5.83 | 0 / -1 / 2 | 2 / -14 / 0 | 298 |
| j39_rw | tkha | 5.83 | 6 / 18 / 1 | 5 / 11 / 1 | 299 |
| j39_rl_e | o | 5.63 | 6 / 26 / 73 | 9 / 10 / 57 | 299 |
| j39_rl_e | tkha | 5.63 | 3 / -13 / 61 | 8 / 0 / 20 | 299 |
| j39_rl_l | o | 6.13 | 91 / 88 / 81 | -174 / 128 / 106 | 252 |
| j39_rl_l | tkha | 6.13 | 21 / 7 / 61 | 27 / 24 / 56 | 254 |
| j39_lr | o | 5.83 | -9 / -37 / -48 | -9 / -14 / -22 | 299 |
| j39_lr | tkha | 5.83 | -3 / 7 / -33 | -6 / -3 / -2 | 299 |
| j39_lw | o | 5.83 | -3 / 10 / 1 | -10 / -16 / 4 | 299 |
| j39_lw | tkha | 5.83 | -3 / 9 / 3 | -8 / 2 / 4 | 299 |
| j38_cc90 | o | 6.17 | 45 / 42 / 28 | 36 / 28 / 83 | 265 |
| j38_cc90 | tkha | 6.17 | 22 / 10 / 14 | 7 / -9 / 9 | 273 |

## 4. External effect vs planned velocity change

| run | max residual cm/s | Ext frames | families seen | worst slide |
|---|---|---|---|---|
| j39_push_plan o | 282 | 0 | [0, 4] | 0.0 |
| j39_push_plan tkha | 282 | 18 | [0, 3, 4] | 21.6 |
| j39_push_jog o | 0 | 0 | [0, 4] | 7.2 |
| j39_push_jog tkha | 0 | 0 | [0, 4, 6] | 17.3 |
| j38_c90r o | 9 | 0 | [0, 4] | 9.7 |
| j38_c90r tkha | 9 | 0 | [0, 4] | 0.0 |
| j39_rl o | 11 | 0 | [0, 4] | 39.7 |
| j39_rl tkha | 11 | 0 | [0, 3, 4] | 25.0 |

## 5. Devralma girişi — 30 FPS regresyon (entry241)

```
ENTRY241 v241reg_j38_cc90_tkha_r1 cut SHM238_Cut_R_P21 tau 0.775 -> SHM239_Tk_R_P21_K3_Back @0.833 expK 3 gotK 3 jump -0.009 s | old-side overshoot 11 deg, turn-back latency 0.37 s
ENTRY241 v241reg_j39_lr_tkha_r1 cut SHM238_Cut_L_P20 tau 0.411 -> SHM239_Tk_L_P20_K2_Opp @0.467 expK 1 gotK 2 jump -0.011 s | old-side overshoot 25 deg, turn-back latency 0.17 s
ENTRY241 v241reg_j39_lw_tkha_r1 cut SHM238_Cut_L_P20 tau 0.508 -> SHM239_Tk_L_P20_K2_Back @0.633 expK 2 gotK 2 jump -0.008 s | old-side overshoot 43 deg, turn-back latency 0.23 s
ENTRY241 v241reg_j39_rl_e_tkha_r1 cut SHM238_Cut_R_P10 tau 0.204 -> SHM239_Tk_R_P10_K1_Opp @0.133 expK 1 gotK 1 jump -0.203 s | old-side overshoot 10 deg, turn-back latency 0.23 s
ENTRY241 v241reg_j39_rl_l_tkha_r1 cut SHM238_Cut_R_P21 tau 0.742 -> SHM239_Tk_R_P21_K3_Opp @0.867 expK 3 gotK 3 jump -0.008 s | old-side overshoot 13 deg, turn-back latency 0.63 s
ENTRY241 v241reg_j39_rl_tkha_r1 cut SHM238_Cut_R_P10 tau 0.408 -> SHM239_Tk_R_P10_K2_Opp @0.467 expK 2 gotK 2 jump -0.008 s | old-side overshoot 24 deg, turn-back latency 0.30 s
ENTRY241 v241reg_j39_rw_tkha_r1 cut SHM238_Cut_R_P10 tau 0.408 -> SHM239_Tk_R_P10_K2_Back @0.467 expK 2 gotK 2 jump -0.008 s | old-side overshoot 23 deg, turn-back latency 0.27 s
ENTRY241 v241reg_j40_lrw_tkha_r1 cut SHM238_Cut_L_P20 tau 0.508 -> SHM239_Tk_L_P20_K2_Opp @0.567 expK 2 gotK 2 jump -0.009 s | old-side overshoot 34 deg, turn-back latency 0.23 s
ENTRY241 v241reg_j40_rlw_tkha_r1 cut SHM238_Cut_R_P10 tau 0.408 -> SHM239_Tk_R_P10_K2_Opp @0.467 expK 2 gotK 2 jump -0.008 s | old-side overshoot 24 deg, turn-back latency 0.30 s
ENTRY241 v241reg_j41_lr_p10_tkha_r1 cut SHM238_Cut_L_P20 tau 0.411 -> SHM239_Tk_L_P20_K2_Opp @0.467 expK 1 gotK 2 jump -0.011 s | old-side overshoot 25 deg, turn-back latency 0.17 s
ENTRY241 v241reg_j41_rl_p10_tkha_r1 cut SHM238_Cut_R_P10 tau 0.408 -> SHM239_Tk_R_P10_K2_Opp @0.467 expK 2 gotK 2 jump -0.008 s | old-side overshoot 24 deg, turn-back latency 0.30 s
ENTRY241 v241reg_j41_rl_p16_tkha_r1 cut SHM238_Cut_R_P02 tau 0.412 -> SHM239_Tk_R_P02_K1_Opp @0.467 expK 1 gotK 1 jump -0.012 s | old-side overshoot 9 deg, turn-back latency 0.13 s
ENTRY241 v241reg_j41_rlw_p10_tkha_r1 cut SHM238_Cut_R_P10 tau 0.408 -> SHM239_Tk_R_P10_K2_Opp @0.467 expK 2 gotK 2 jump -0.008 s | old-side overshoot 24 deg, turn-back latency 0.30 s
ENTRY241 v241reg_j41_rw_p10_tkha_r1 cut SHM238_Cut_R_P10 tau 0.408 -> SHM239_Tk_R_P10_K2_Back @0.467 expK 2 gotK 2 jump -0.008 s | old-side overshoot 23 deg, turn-back latency 0.27 s
```

## 6. Devralma girişi — 120 / 60 / 20 / gerçek FPS (entry241)

```
ENTRY241 v241f120_j41_rl_p10_tkhaB_r1 cut SHM238_Cut_R_P09 tau 0.436 -> SHM239_Tk_R_P09_K2_Opp @0.433 expK 2 gotK 2 jump -0.019 s | old-side overshoot 41 deg, turn-back latency 0.36 s
ENTRY241 v241f120_j41_rl_p16_tkhaB_r1 cut SHM238_Cut_R_P16 tau 0.436 -> SHM239_Tk_R_P16_K1_Opp @0.467 expK 1 gotK 1 jump +0.014 s | old-side overshoot 22 deg, turn-back latency 0.30 s
ENTRY241 v241f120_j41_lr_p10_tkhaB_r1 cut SHM238_Cut_L_P22 tau 0.436 -> SHM239_Tk_L_P22_K1_Opp @0.467 expK 1 gotK 1 jump +0.014 s | old-side overshoot 24 deg, turn-back latency 0.31 s
ENTRY241 v241f120_j41_rlw_p10_tkhaB_r1 cut SHM238_Cut_R_P09 tau 0.436 -> SHM239_Tk_R_P09_K2_Opp @0.433 expK 2 gotK 2 jump -0.019 s | old-side overshoot 41 deg, turn-back latency 0.36 s
ENTRY241 v241f120_j39_lr_tkhaB_r1 cut SHM238_Cut_L_P22 tau 0.436 -> SHM239_Tk_L_P22_K1_Opp @0.467 expK 1 gotK 1 jump +0.014 s | old-side overshoot 24 deg, turn-back latency 0.31 s
ENTRY241 v241f120_j38_cc90_tkhaB_r1 cut SHM238_Cut_R_P09 tau 0.784 -> SHM239_Tk_R_P09_K3_Back @0.800 expK 3 gotK 3 jump -0.001 s | old-side overshoot 16 deg, turn-back latency 0.38 s
ENTRY241 v241f60_j41_rl_p10_tkhaB_r1 cut SHM238_Cut_R_P09 tau 0.421 -> SHM239_Tk_R_P09_K2_Opp @0.467 expK 2 gotK 2 jump +0.013 s | old-side overshoot 41 deg, turn-back latency 0.33 s
ENTRY241 v241f60_j41_rl_p16_tkhaB_r1 cut SHM238_Cut_R_P16 tau 0.422 -> SHM239_Tk_R_P16_K1_Opp @0.467 expK 1 gotK 1 jump +0.011 s | old-side overshoot 22 deg, turn-back latency 0.32 s
ENTRY241 v241f60_j41_lr_p10_tkhaB_r1 cut SHM238_Cut_L_P22 tau 0.422 -> SHM239_Tk_L_P22_K1_Opp @0.467 expK 1 gotK 1 jump +0.012 s | old-side overshoot 24 deg, turn-back latency 0.32 s
ENTRY241 v241f60_j41_rlw_p10_tkhaB_r1 cut SHM238_Cut_R_P09 tau 0.454 -> SHM239_Tk_R_P09_K2_Opp @0.500 expK 2 gotK 2 jump +0.013 s | old-side overshoot 36 deg, turn-back latency 0.30 s
ENTRY241 v241f60_j39_lr_tkhaB_r1 cut SHM238_Cut_L_P22 tau 0.422 -> SHM239_Tk_L_P22_K1_Opp @0.467 expK 1 gotK 1 jump +0.012 s | old-side overshoot 24 deg, turn-back latency 0.32 s
ENTRY241 v241f60_j38_cc90_tkhaB_r1 cut SHM238_Cut_R_P09 tau 0.802 -> SHM239_Tk_R_P09_K3_Back @0.833 expK 3 gotK 3 jump -0.002 s | old-side overshoot 13 deg, turn-back latency 0.37 s
ENTRY241 v241f20_j41_rl_p10_tkhaB_r1 cut SHM238_Cut_R_P09 tau 0.423 -> SHM239_Tk_R_P09_K2_Opp @0.533 expK 2 gotK 2 jump +0.010 s | old-side overshoot 32 deg, turn-back latency 0.30 s
ENTRY241 v241f20_j41_rl_p16_tkhaB_r1 cut SHM238_Cut_R_P16 tau 0.392 -> SHM239_Tk_R_P16_K1_Opp @0.500 expK 1 gotK 1 jump +0.008 s | old-side overshoot 20 deg, turn-back latency 0.30 s
ENTRY241 v241f20_j41_lr_p10_tkhaB_r1 cut SHM238_Cut_L_P08 tau 0.363 -> SHM239_Tk_L_P08_K1_Opp @0.467 expK 1 gotK 1 jump +0.003 s | old-side overshoot 12 deg, turn-back latency 0.15 s
ENTRY241 v241f20_j41_rlw_p10_tkhaB_r1 cut SHM238_Cut_R_P09 tau 0.423 -> SHM239_Tk_R_P09_K2_Opp @0.533 expK 2 gotK 2 jump +0.010 s | old-side overshoot 32 deg, turn-back latency 0.30 s
ENTRY241 v241f20_j39_lr_tkhaB_r1 cut SHM238_Cut_L_P20 tau 0.363 -> SHM239_Tk_L_P20_K1_Opp @0.433 expK 1 gotK 1 jump -0.030 s | old-side overshoot 15 deg, turn-back latency 0.15 s
ENTRY241 v241f20_j38_cc90_tkhaB_r1 cut SHM238_Cut_R_P21 tau 0.736 -> SHM239_Tk_R_P21_K3_Back @0.833 expK 3 gotK 3 jump -0.002 s | old-side overshoot 12 deg, turn-back latency 0.40 s
ENTRY241 v241freal_j41_rl_p10_tkhaB_r1 cut SHM238_Cut_R_P10 tau 0.414 -> SHM239_Tk_R_P10_K2_Opp @0.467 expK 2 gotK 2 jump -0.006 s | old-side overshoot 29 deg, turn-back latency 0.31 s
ENTRY241 v241freal_j41_rl_p16_tkhaB_r1 cut SHM238_Cut_R_P02 tau 0.410 -> SHM239_Tk_R_P02_K1_Opp @0.467 expK 1 gotK 1 jump -0.003 s | old-side overshoot 8 deg, turn-back latency 0.12 s
ENTRY241 v241freal_j41_lr_p10_tkhaB_r1 cut SHM238_Cut_L_P20 tau 0.421 -> SHM239_Tk_L_P20_K2_Opp @0.467 expK 1 gotK 2 jump -0.015 s | old-side overshoot 52 deg, turn-back latency 0.35 s
ENTRY241 v241freal_j41_rlw_p10_tkhaB_r1 cut SHM238_Cut_R_P10 tau 0.423 -> SHM239_Tk_R_P10_K2_Opp @0.500 expK 2 gotK 2 jump +0.017 s | old-side overshoot 28 deg, turn-back latency 0.24 s
ENTRY241 v241freal_j39_lr_tkhaB_r1 cut SHM238_Cut_L_P20 tau 0.417 -> SHM239_Tk_L_P20_K2_Opp @0.467 expK 1 gotK 2 jump -0.013 s | old-side overshoot 59 deg, turn-back latency 0.32 s
ENTRY241 v241freal_j38_cc90_tkhaB_r1 cut SHM238_Cut_R_P09 tau 0.803 -> SHM239_Tk_R_P09_K3_Back @0.867 expK 3 gotK 3 jump -0.021 s | old-side overshoot 11 deg, turn-back latency 0.36 s
```

Aşama A (V2.40 tkh ve kapılı ilk ölçüm) ve aşama E (tkk):

```
v240reg_j39_rl_tkh_r1 cut SHM238_Cut_R_P10 tau 0.408 -> SHM239_Tk_R_P10_K3_Opp @0.667 expK 2 gotK 3 jump +0.192 s | old-side overshoot 49 deg, turn-back latency 0.73 s
v240i30f_j39_rl_tkh_r1 cut SHM238_Cut_R_P21 tau 0.442 -> SHM239_Tk_R_P21_K2_Opp @0.500 expK 2 gotK 2 jump -0.009 s | old-side overshoot 26 deg, turn-back latency 0.30 s
v241a30_j41_rl_p10_tkh_r1 cut SHM238_Cut_R_P10 tau 0.408 -> SHM239_Tk_R_P10_K3_Opp @0.667 expK 2 gotK 3 jump +0.192 s | old-side overshoot 49 deg, turn-back latency 0.73 s
v241a30_j41_rl_p16_tkh_r1 cut SHM238_Cut_R_P02 tau 0.412 -> SHM239_Tk_R_P02_K4_Opp @1.100 expK 1 gotK 4 jump +0.621 s | old-side overshoot 80 deg, turn-back latency 0.87 s
v241a30_j41_rl_p21_tkh_r1 cut SHM238_Cut_R_P21 tau 0.442 -> SHM239_Tk_R_P21_K2_Opp @0.500 expK 2 gotK 2 jump -0.009 s | old-side overshoot 26 deg, turn-back latency 0.30 s
v241a30_j41_rl_p04_tkh_r1 cut SHM238_Cut_R_P16 tau 0.477 -> SHM239_Tk_R_P16_K1_Opp @0.533 expK 1 gotK 1 jump -0.009 s | old-side overshoot 14 deg, turn-back latency 0.17 s
v241d30_j41_rl_p10_tkh_r2 cut SHM238_Cut_R_P10 tau 0.408 -> SHM239_Tk_R_P10_K2_Opp @0.467 expK 2 gotK 2 jump -0.008 s | old-side overshoot 24 deg, turn-back latency 0.30 s
v241e30_j41_rl_p10_tkk_r1 cut SHM238_Cut_R_P10 tau 0.408 -> SHM239_Tk_R_P10_K2_Opp @0.500 expK 2 gotK 2 jump -0.042 s | old-side overshoot 24 deg, turn-back latency 0.33 s
v241e30_j41_rl_p16_tkk_r1 cut SHM238_Cut_R_P02 tau 0.412 -> SHM239_Tk_R_P02_K2_Opp @0.567 expK 1 gotK 2 jump -0.045 s | old-side overshoot 56 deg, turn-back latency 0.40 s
v241e30_j41_rl_p21_tkk_r1 cut SHM238_Cut_R_P21 tau 0.442 -> SHM239_Tk_R_P21_K2_Opp @0.533 expK 2 gotK 2 jump -0.041 s | old-side overshoot 26 deg, turn-back latency 0.33 s
v241e30_j41_rl_p04_tkk_r1 cut SHM238_Cut_R_P16 tau 0.477 -> SHM239_Tk_R_P16_K1_Opp @0.533 expK 1 gotK 1 jump -0.077 s | old-side overshoot 17 deg, turn-back latency 0.23 s
v241e30_j41_rw_p10_tkk_r1 cut SHM238_Cut_R_P10 tau 0.408 -> SHM239_Tk_R_P10_K2_Back @0.500 expK 2 gotK 2 jump -0.042 s | old-side overshoot 28 deg, turn-back latency 0.23 s
v241e30_j41_rw_p16_tkk_r1 cut SHM238_Cut_R_P02 tau 0.412 -> SHM239_Tk_R_P02_K2_Back @0.600 expK 1 gotK 2 jump -0.012 s | old-side overshoot 58 deg, turn-back latency 0.37 s
v241e30_j41_lr_p10_tkk_r1 cut SHM238_Cut_L_P20 tau 0.411 -> SHM239_Tk_L_P20_K2_Opp @0.533 expK 1 gotK 2 jump -0.012 s | old-side overshoot 52 deg, turn-back latency 0.33 s
v241e30_j41_lr_p16_tkk_r1 cut SHM238_Cut_L_P03 tau 0.474 -> SHM239_Tk_L_P03_K2_Opp @0.567 expK 2 gotK 2 jump -0.041 s | old-side overshoot 25 deg, turn-back latency 0.33 s
v241e30_j41_rlw_p10_tkk_r1 cut SHM238_Cut_R_P10 tau 0.408 -> SHM239_Tk_R_P10_K2_Opp @0.467 expK 2 gotK 2 jump -0.008 s | old-side overshoot 24 deg, turn-back latency 0.30 s
v241e30_j41_rlw_p16_tkk_r1 cut SHM238_Cut_R_P02 tau 0.412 -> SHM239_Tk_R_P02_K1_Opp @0.433 expK 1 gotK 1 jump -0.046 s | old-side overshoot 11 deg, turn-back latency 0.13 s
v241e30_j41_rl_p10_tkk_r2 cut SHM238_Cut_R_P10 tau 0.408 -> SHM239_Tk_R_P10_K2_Opp @0.467 expK 2 gotK 2 jump -0.008 s | old-side overshoot 24 deg, turn-back latency 0.30 s
```

## 7. Baş / göğüs hizası — FPS (align241)

```
v241h30_j39_lr_o_r1            t2 5.83  pel/chest/head @+0.6 -8/-30/-74 @+1.2 -9/-37/-48 @+1.8 -9/-14/-22 | mean|head| 47.5 mean|chest| 31.2
v241h30_j39_lr_aoh_r1          t2 5.83  pel/chest/head @+0.6 4/-9/-48 @+1.2 -3/-8/-17 @+1.8 -5/2/-11 | mean|head| 23.1 mean|chest| 9.1
v241h30_j39_lr_tkk_r1          t2 5.83  pel/chest/head @+0.6 0/2/-11 @+1.2 -8/-28/-55 @+1.8 -5/-1/-3 | mean|head| 36.2 mean|chest| 25.2
v241h30_j39_lr_tkha_r1         t2 5.83  pel/chest/head @+0.6 1/2/-4 @+1.2 -2/2/-28 @+1.8 -4/5/-2 | mean|head| 22.9 mean|chest| 12.6
v241h30_j38_cc90_o_r1          t2 6.17  pel/chest/head @+0.6 7/-13/9 @+1.2 71/65/40 @+1.8 35/26/82 | mean|head| 36.3 mean|chest| 33.5
v241h30_j38_cc90_aoh_r1        t2 6.17  pel/chest/head @+0.6 10/-3/9 @+1.2 45/40/24 @+1.8 35/12/63 | mean|head| 30.1 mean|chest| 18.2
v241h30_j38_cc90_tkk_r1        t2 6.17  pel/chest/head @+0.6 8/-16/-49 @+1.2 21/7/16 @+1.8 7/-7/13 | mean|head| 23.4 mean|chest| 17.4
v241h30_j38_cc90_tkha_r1       t2 6.17  pel/chest/head @+0.6 14/10/-27 @+1.2 22/10/14 @+1.8 7/-9/9 | mean|head| 15.3 mean|chest| 19.1
v241h30_j39_rw_tkk_r1          t2 5.83  pel/chest/head @+0.6 1/-11/-28 @+1.2 6/19/0 @+1.8 5/8/1 | mean|head| 9.2 mean|chest| 10.1
v241h30_j39_rw_tkha_r1         t2 5.83  pel/chest/head @+0.6 5/-2/-16 @+1.2 7/20/0 @+1.8 6/13/1 | mean|head| 6.6 mean|chest| 10.6
ALIGN241 v241f120_j41_rl_p10_o_r1       t2 5.77  pel/chest/head @+0.6 4/25/69 @+1.2 -4/21/51 @+1.8 -2/3/37 | mean|head| 52.3 mean|chest| 15.7
ALIGN241 v241f120_j41_rl_p10_tkhaB_r1   t2 5.77  pel/chest/head @+0.6 5/9/-33 @+1.2 -8/0/37 @+1.8 -3/-14/-1 | mean|head| 23.1 mean|chest| 12.0
ALIGN241 v241f120_j41_lr_p10_o_r1       t2 5.77  pel/chest/head @+0.6 -48/-56/-53 @+1.2 16/-7/-24 @+1.8 -10/-44/-24 | mean|head| 40.1 mean|chest| 37.8
ALIGN241 v241f120_j41_lr_p10_tkhaB_r1   t2 5.77  pel/chest/head @+0.6 9/16/31 @+1.2 2/10/-31 @+1.8 -2/5/1 | mean|head| 19.4 mean|chest| 12.1
ALIGN241 v241f120_j39_lr_o_r1           t2 5.77  pel/chest/head @+0.6 -48/-56/-53 @+1.2 7/-18/-29 @+1.8 -10/-40/-25 | mean|head| 41.0 mean|chest| 38.5
ALIGN241 v241f120_j39_lr_tkhaB_r1       t2 5.77  pel/chest/head @+0.6 9/15/31 @+1.2 2/10/-31 @+1.8 -2/5/1 | mean|head| 19.4 mean|chest| 12.1
ALIGN241 v241f120_j38_cc90_o_r1         t2 6.12  pel/chest/head @+0.6 11/-20/-2 @+1.2 65/58/25 @+1.8 61/74/63 | mean|head| 28.8 mean|chest| 42.5
ALIGN241 v241f120_j38_cc90_tkhaB_r1     t2 6.12  pel/chest/head @+0.6 11/-6/-40 @+1.2 19/3/5 @+1.8 19/14/8 | mean|head| 14.4 mean|chest| 16.9
ALIGN241 v241f60_j41_rl_p10_o_r1        t2 6.02  pel/chest/head @+0.6 -2/-20/28 @+1.2 1/13/66 @+1.8 3/28/58 | mean|head| 54.8 mean|chest| 16.9
ALIGN241 v241f60_j41_rl_p10_tkhaB_r1    t2 6.02  pel/chest/head @+0.6 -1/-18/11 @+1.2 -9/-29/26 @+1.8 0/16/9 | mean|head| 28.4 mean|chest| 13.4
ALIGN241 v241f60_j41_lr_p10_o_r1        t2 6.02  pel/chest/head @+0.6 -4/-13/-34 @+1.2 -2/-28/-73 @+1.8 -5/-17/-37 | mean|head| 47.7 mean|chest| 24.8
ALIGN241 v241f60_j41_lr_p10_tkhaB_r1    t2 5.78  pel/chest/head @+0.6 10/16/32 @+1.2 3/10/-31 @+1.8 0/8/0 | mean|head| 19.4 mean|chest| 12.1
ALIGN241 v241f60_j39_lr_o_r1            t2 5.78  pel/chest/head @+0.6 -32/-57/-82 @+1.2 -14/-60/-47 @+1.8 1/-33/-34 | mean|head| 43.5 mean|chest| 39.4
ALIGN241 v241f60_j39_lr_tkhaB_r1        t2 5.78  pel/chest/head @+0.6 11/18/33 @+1.2 4/12/-30 @+1.8 2/10/1 | mean|head| 19.2 mean|chest| 12.3
ALIGN241 v241f60_j38_cc90_o_r1          t2 6.13  pel/chest/head @+0.6 11/-19/5 @+1.2 67/60/32 @+1.8 64/78/69 | mean|head| 33.0 mean|chest| 45.0
ALIGN241 v241f60_j38_cc90_tkhaB_r1      t2 6.13  pel/chest/head @+0.6 12/3/-34 @+1.2 20/6/9 @+1.8 18/12/8 | mean|head| 14.0 mean|chest| 18.7
ALIGN241 v241f20_j41_rl_p10_o_r1        t2 6.15  pel/chest/head @+0.6 -11/-29/4 @+1.2 0/8/66 @+1.8 6/31/57 | mean|head| 53.3 mean|chest| 19.1
ALIGN241 v241f20_j41_rl_p10_tkhaB_r1    t2 6.15  pel/chest/head @+0.6 3/-9/10 @+1.2 -11/-33/30 @+1.8 -6/-20/8 | mean|head| 27.7 mean|chest| 13.2
ALIGN241 v241f20_j41_lr_p10_o_r1        t2 6.15  pel/chest/head @+0.6 -2/-16/-25 @+1.2 -1/-28/-72 @+1.8 -7/-18/-41 | mean|head| 48.5 mean|chest| 24.0
ALIGN241 v241f20_j41_lr_p10_tkhaB_r1    t2 6.15  pel/chest/head @+0.6 -2/-13/6 @+1.2 2/-5/-42 @+1.8 -3/8/-2 | mean|head| 17.5 mean|chest| 11.4
ALIGN241 v241f20_j39_lr_o_r1            t2 5.85  pel/chest/head @+0.6 -3/-12/-71 @+1.2 -36/-69/-53 @+1.8 15/-1/-26 | mean|head| 50.4 mean|chest| 39.3
ALIGN241 v241f20_j39_lr_tkhaB_r1        t2 5.85  pel/chest/head @+0.6 10/28/-20 @+1.2 -4/-13/3 @+1.8 -2/-19/6 | mean|head| 9.5 mean|chest| 11.1
ALIGN241 v241f20_j38_cc90_o_r1          t2 6.20  pel/chest/head @+0.6 8/-30/2 @+1.2 4/9/28 @+1.8 34/28/76 | mean|head| 39.7 mean|chest| 19.5
ALIGN241 v241f20_j38_cc90_tkhaB_r1      t2 6.20  pel/chest/head @+0.6 13/10/-28 @+1.2 20/9/12 @+1.8 18/19/-2 | mean|head| 13.4 mean|chest| 20.9
ALIGN241 v241freal_j41_rl_p10_o_r1      t2 6.13  pel/chest/head @+0.6 -5/-23/22 @+1.2 -2/1/63 @+1.8 6/28/57 | mean|head| 53.6 mean|chest| 16.8
ALIGN241 v241freal_j41_rl_p10_tkhaB_r1  t2 5.84  pel/chest/head @+0.6 -/-/- @+1.2 -3/12/17 @+1.8 -2/-2/-2 | mean|head| 21.0 mean|chest| 11.7
ALIGN241 v241freal_j41_lr_p10_o_r1      t2 6.09  pel/chest/head @+0.6 -4/-18/-28 @+1.2 6/-29/-78 @+1.8 -5/-16/-36 | mean|head| 47.3 mean|chest| 24.7
ALIGN241 v241freal_j41_lr_p10_tkhaB_r1  t2 5.87  pel/chest/head @+0.6 8/27/39 @+1.2 2/12/-28 @+1.8 0/4/4 | mean|head| 23.5 mean|chest| 13.0
ALIGN241 v241freal_j39_lr_o_r1          t2 5.82  pel/chest/head @+0.6 -3/-13/-68 @+1.2 -8/-24/-36 @+1.8 -10/-24/-7 | mean|head| 37.3 mean|chest| 28.3
ALIGN241 v241freal_j39_lr_tkhaB_r1      t2 5.84  pel/chest/head @+0.6 9/25/32 @+1.2 2/13/-28 @+1.8 -1/5/2 | mean|head| 23.4 mean|chest| 12.8
ALIGN241 v241freal_j38_cc90_o_r1        t2 6.17  pel/chest/head @+0.6 12/-16/5 @+1.2 22/21/5 @+1.8 26/42/78 | mean|head| 22.5 mean|chest| 22.1
ALIGN241 v241freal_j38_cc90_tkhaB_r1    t2 6.18  pel/chest/head @+0.6 16/15/-23 @+1.2 22/14/15 @+1.8 20/10/17 | mean|head| 16.0 mean|chest| 21.2
```

## 8. En kötü ayak kayması — FPS blokları (fps241; cm, sahip klip @ s)

| scenario | var | f120 | f60 | f20 | freal |
|---|---|---|---|---|---|
| j38_c90r | o | 8.4 (SHM238_Cut_R_P09 @6.01) | 8.5 (SHM238_Cut_R_P21 @5.98) | - | - |
| j38_c90r | tkhaB | 8.1 (SHM238_Cut_R_P09 @5.69) | 5.9 (SHM238_Cut_R_P21 @6.13) | - | - |
| j38_cc90 | o | 21.3 (SHM216_RevTurn_L_Rfoot @6.83) | 11.8 (SHM216_RevTurn_L_Rfoot @6.80) | 19.7 (SHM216_RevTurn_L_Rfoot @7.00) | 7.3 (CT_Jog_Fwd @6.60) |
| j38_cc90 | tkhaB | 9.1 (CT_Jog_Fwd @8.10) | 8.1 (SHM239_Tk_R_P09_K3_Back @6.13) | 13.4 (SHM238_Cut_L_P16 @7.75) | 7.6 (CT_Jog_Fwd @8.14) |
| j39_lr | o | 38.7 (SHM216_RevTurn_R_Lfoot @6.15) | 45.3 (SHM216_RevTurn_L_Lfoot @6.18) | 14.6 (CT_Jog_Right @7.25) | 7.1 (SHM238_Cut_L_P20 @5.82) |
| j39_lr | tkhaB | 8.4 (CT_Jog_Fwd @7.00) | 0 | 5.4 (CT_Jog_Fwd @6.50) | 8.6 (SHM237_JogStop_Bl_P05 @8.62) |
| j39_push_plan | o | 12.7 (CT_Jog_FwdRight @6.10) | 8.9 (CT_Jog_Fwd @6.73) | - | - |
| j39_push_plan | tkhaB | 30.3 (LS_Jog_Right_Stop @8.20) | 32.6 (LS_Jog_Right_Stop @8.25) | 29.7 (LS_Jog_Right_Stop @8.30) | 29.7 (SHM216_RevTurn_L_Lfoot @5.72) |
| j39_push_plan | tkpB | 30.4 (LS_Jog_Right_Stop @8.22) | 32.8 (LS_Jog_Right_Stop @8.25) | 32.3 (LS_Jog_Right_Stop @8.30) | 33.5 (SHM216_RevTurn_L_Lfoot @5.71) |
| j39_rw | o | 16.6 (CT_Jog_Fwd @6.16) | 24.4 (CT_Jog_FwdLeft @6.12) | - | - |
| j39_rw | tkhaB | 11.9 (CT_Jog_Fwd @6.30) | 12.3 (CT_Jog_Fwd @6.28) | - | - |
| j40_rlw | o | 22.2 (CP2_Jog_Fwd_Start @10.66) | 14.4 (CP2_Jog_Fwd_Start @10.43) | - | - |
| j40_rlw | tkhaB | 9.1 (SHM237_JogStop_Br_P15 @8.62) | 24.6 (CT_Jog_Fwd @7.20) | - | - |
| j40_wall | o | 29.6 (af_Stand_Idle_NaturalBasel @7.01) | 38.1 (SHM_M_Neutral_Stand_Turn_0 @6.78) | - | - |
| j40_wall | wst | 44.2 (af_Loco_Jog_Left_Start_AAM @6.38) | 31.4 (af_Stand_Idle_NaturalBasel @7.12) | 42.9 (af_Loco_Jog_Fwd_NoRM @6.50) | 40.6 (af_Loco_Jog_Left_Start_AAM @6.42) |
| j40_wall | wsto | 30.1 (af_Loco_Jog_FwdRight_AAMS @6.38) | 43.0 (af_Loco_Jog_Left_Start_AAM @6.37) | 42.9 (af_Loco_Jog_Fwd_NoRM @6.50) | 32.3 (af_Loco_Jog_FwdRight_AAMS @6.69) |
| j41_lr_p10 | o | 38.8 (SHM216_RevTurn_R_Lfoot @6.15) | 6.0 (SHM237_JogStop_Br_P15 @9.48) | 0 | 5.9 (CT_Jog_Fwd @7.34) |
| j41_lr_p10 | tkhaB | 7.0 (CT_Jog_Fwd @7.00) | 7.4 (CT_Jog_Fwd @7.02) | 0 | 11.3 (CT_Jog_Fwd @7.18) |
| j41_rl_p10 | o | 30.6 (LS_Jog_Left_Stop @10.95) | 64.7 (LS_Jog_Left_Stop @11.62) | 60.6 (LS_Jog_Left_Stop @11.80) | 15.9 (LS_Jog_Left_Stop @12.17) |
| j41_rl_p10 | tkhaB | 31.3 (LS_Jog_Left_Stop @10.94) | 57.1 (LS_Jog_Left_Stop @11.62) | 61.2 (LS_Jog_Left_Stop @11.80) | 33.6 (LS_Jog_Left_Stop @11.01) |
| j41_rl_p16 | o | 38.6 (LS_Jog_Left_Stop @11.27) | 64.3 (LS_Jog_Left_Stop @12.00) | - | - |
| j41_rl_p16 | tkhaB | 16.2 (LS_Jog_Left_Stop @11.66) | 57.2 (LS_Jog_Left_Stop @11.30) | 28.7 (LS_Jog_Left_Stop @12.55) | 47.0 (LS_Jog_Left_Stop @12.29) |
| j41_rlw_p10 | o | 17.7 (SHM238_Cut_R_P20 @6.96) | 14.6 (CP2_Jog_Fwd_Start @11.35) | 14.9 (CP2_Jog_Fwd_Start @11.35) | 73.5 (SHM237_JogStop_Bl_P05 @11.17) |
| j41_rlw_p10 | tkhaB | 8.7 (CT_Jog_Fwd @6.92) | 28.1 (CT_Jog_Fwd @7.17) | 6.7 (SHM239_Tk_R_P09_K2_Opp @6.50) | 10.6 (SHM239_Tk_R_P10_K2_Opp @6.95) |
| mtf_jog | o | 23.3 (SHM216_RevTurn_L_Rfoot @14.22) | 22.2 (SHM_Rec_F_Rfoot @9.13) | - | - |
| mtf_jog | tkhaB | 22.8 (CT_Jog_Fwd @13.55) | 17.2 (SHM216_RevTurn_R_Rfoot @12.17) | - | - |

## 9. İtme pencereleri (30 FPS, 300 cm/s sola itme, planlı sağ 90)

```
v241f30_j39_push_plan_o_r1         catch[5.55,6.10) 0.0  exit[6.10,6.90) 0.0  rest 0.0
v241f30_j39_push_plan_tkk_r1       catch[5.55,6.10) 22.6  exit[6.10,6.90) 8.2  rest 6.2
v241f30_j39_push_plan_tkp_r1       catch[5.55,6.10) 0.0  exit[6.10,6.90) 25.6  rest 0.0
v241f30_j39_push_plan_ext_r1       catch[5.55,6.10) 19.3  exit[6.10,6.90) 9.4  rest 6.5
v241f30_j39_push_plan_extp_r1      catch[5.55,6.10) 7.3  exit[6.10,6.90) 25.9  rest 0.0
v241f30_j39_push_jog_tkk_r1        catch[5.55,6.10) 8.7  exit[6.10,6.90) 0.0  rest 5.6
v241f30_j39_push_jog_tkp_r1        catch[5.55,6.10) 11.8  exit[6.10,6.90) 32.4  rest 0.0
```

## 10. En büyük üst beden ivmesi (m/s², kemik, zaman, sahne) — 120 / 60 / 30 FPS

| koşu | t | tepe | sahne | kemik | sapma cm |
|---|---|---|---|---|---|
| v241f120_j38_c90r_o_r1 | 6.26 | 85 | mv_kb_90_5_D | 218 | head |
| v241f120_j38_c90r_tkhaB_r1 | 6.26 | 90 | mv_kb_90_5_D | 218 | head |
| v241f120_j38_cc90_o_r1 | 7.52 | 227 | mv_kb_-90_9_A | 185 | pelvis |
| v241f120_j38_cc90_tkhaB_r1 | 6.45 | 123 | mv_kb_0_7_W | 238 | head |
| v241f120_j39_lr_o_r1 | 9.36 | 89 | mv_kb_rel_8_0 | 0 | head |
| v241f120_j39_lr_tkhaB_r1 | 6.07 | 251 | mv_kb_90_7_D | 157 | head |
| v241f120_j39_push_plan_o_r1 | 5.75 | 71 | mv_kb_90_5_D | 265 | sh_l |
| v241f120_j39_push_plan_tkhaB_r1 | 8.00 | 149 | mv_kb_rel_6_0 | 176 | sh_r |
| v241f120_j39_push_plan_tkpB_r1 | 8.00 | 150 | mv_kb_rel_6_0 | 176 | sh_r |
| v241f120_j39_rw_o_r1 | 6.26 | 88 | mv_kb_0_7_W | 206 | head |
| v241f120_j39_rw_tkhaB_r1 | 6.10 | 186 | mv_kb_0_7_W | 153 | head |
| v241f120_j40_rlw_o_r1 | 6.40 | 82 | mv_kb_0_9_W | 250 | head |
| v241f120_j40_rlw_tkhaB_r1 | 6.10 | 245 | mv_kb_-90_7_A | 157 | head |
| v241f120_j40_wall_o_r1 | 6.83 | 88 | mv_kb_90_5_D | 0 | head |
| v241f120_j40_wall_wst_r1 | 6.28 | 60 | mv_kb_90_5_D | 223 | sh_l |
| v241f120_j40_wall_wsto_r1 | 6.28 | 61 | mv_kb_90_5_D | 223 | sh_l |
| v241f120_j41_lr_p10_o_r1 | 9.36 | 89 | mv_kb_rel_8_0 | 0 | head |
| v241f120_j41_lr_p10_tkhaB_r1 | 6.07 | 251 | mv_kb_90_7_D | 157 | head |
| v241f120_j41_rl_p10_o_r1 | 11.57 | 102 | mv_kb_rel_10_0 | 0 | head |
| v241f120_j41_rl_p10_tkhaB_r1 | 6.10 | 245 | mv_kb_-90_7_A | 157 | head |
| v241f120_j41_rl_p16_o_r1 | 6.93 | 187 | mv_kb_-90_7_A | 242 | pelvis |
| v241f120_j41_rl_p16_tkhaB_r1 | 6.38 | 195 | mv_kb_-90_7_A | 159 | head |
| v241f120_j41_rlw_p10_o_r1 | 6.40 | 82 | mv_kb_0_9_W | 250 | head |
| v241f120_j41_rlw_p10_tkhaB_r1 | 6.10 | 245 | mv_kb_-90_7_A | 157 | head |
| v241f120_mtf_jog_o_r1 | 14.79 | 237 | yaw_0_5+mv_jog_0_0 | 32 | pelvis |
| v241f120_mtf_jog_tkhaB_r1 | 14.79 | 236 | yaw_0_5+mv_jog_0_0 | 32 | pelvis |
| v241f60_j38_c90r_o_r1 | 6.23 | 51 | mv_kb_90_5_D | 218 | head |
| v241f60_j38_c90r_tkhaB_r1 | 6.23 | 51 | mv_kb_90_5_D | 218 | head |
| v241f60_j38_cc90_o_r1 | 7.53 | 128 | mv_kb_-90_9_A | 183 | pelvis |
| v241f60_j38_cc90_tkhaB_r1 | 6.43 | 55 | mv_kb_0_7_W | 238 | sh_l |
| v241f60_j39_lr_o_r1 | 6.67 | 118 | mv_kb_90_7_D | 237 | pelvis |
| v241f60_j39_lr_tkhaB_r1 | 6.08 | 116 | mv_kb_90_7_D | 157 | head |
| v241f60_j39_push_plan_o_r1 | 6.23 | 50 | mv_kb_90_5_D | 217 | head |
| v241f60_j39_push_plan_tkhaB_r1 | 8.03 | 56 | mv_kb_rel_6_0 | 166 | sh_r |
| v241f60_j39_push_plan_tkpB_r1 | 8.03 | 56 | mv_kb_rel_6_0 | 166 | sh_r |
| v241f60_j39_rw_o_r1 | 6.25 | 43 | mv_kb_0_7_W | 205 | head |
| v241f60_j39_rw_tkhaB_r1 | 6.05 | 116 | mv_kb_0_7_W | 166 | head |
| v241f60_j40_rlw_o_r1 | 5.57 | 40 | mv_kb_90_5_D | 248 | sh_l |
| v241f60_j40_rlw_tkhaB_r1 | 6.08 | 85 | mv_kb_-90_7_A | 134 | head |
| v241f60_j40_wall_o_r1 | 6.85 | 97 | mv_kb_90_5_D | 0 | sh_r |
| v241f60_j40_wall_wst_r1 | 5.90 | 34 | mv_kb_90_5_D | 178 | sh_r |
| v241f60_j40_wall_wsto_r1 | 5.57 | 40 | mv_kb_90_5_D | 248 | sh_l |
| v241f60_j41_lr_p10_o_r1 | 7.17 | 43 | mv_kb_90_7_D | 251 | head |
| v241f60_j41_lr_p10_tkhaB_r1 | 6.08 | 115 | mv_kb_90_7_D | 157 | head |
| v241f60_j41_rl_p10_o_r1 | 12.33 | 83 | mv_kb_rel_10_0 | 0 | head |
| v241f60_j41_rl_p10_tkhaB_r1 | 6.77 | 133 | mv_kb_-90_7_A | 155 | head |
| v241f60_j41_rl_p16_o_r1 | 7.70 | 158 | mv_kb_-90_7_A | 238 | pelvis |
| v241f60_j41_rl_p16_tkhaB_r1 | 6.42 | 118 | mv_kb_-90_7_A | 159 | head |
| v241f60_j41_rlw_p10_o_r1 | 11.22 | 46 | mv_kb_0_11_W | 120 | head |
| v241f60_j41_rlw_p10_tkhaB_r1 | 6.05 | 119 | mv_kb_-90_7_A | 155 | head |
| v241f60_mtf_jog_o_r1 | 14.85 | 134 | yaw_0_5+mv_jog_0_0 | 36 | pelvis |
| v241f60_mtf_jog_tkhaB_r1 | 14.85 | 134 | yaw_0_5+mv_jog_0_0 | 36 | pelvis |
| v241reg_j41_lr_p10_o_r1 | 7.73 | 25 | mv_kb_90_7_D | 255 | sh_l |
| v241reg_j41_lr_p10_tkha_r1 | 6.97 | 56 | mv_kb_90_7_D | 103 | head |
| v241reg_j41_rl_p10_o_r1 | 12.37 | 65 | mv_kb_rel_10_0 | 0 | head |
| v241reg_j41_rl_p10_tkha_r1 | 12.40 | 67 | mv_kb_rel_10_0 | 0 | head |
| v241reg_j41_rl_p16_o_r1 | 12.80 | 67 | mv_kb_rel_10_0 | 0 | head |
| v241reg_j41_rl_p16_tkha_r1 | 6.83 | 75 | mv_kb_-90_7_A | 148 | sh_r |
| v241reg_j41_rlw_p10_tkha_r1 | 6.13 | 32 | mv_kb_-90_7_A | 135 | head |
| v241reg_j41_rw_p10_tkha_r1 | 6.83 | 75 | mv_kb_0_7_W | 148 | head |
| v241reg_j39_lr_o_r1 | 6.73 | 36 | mv_kb_90_7_D | 300 | pelvis |
| v241reg_j39_lr_tkha_r1 | 6.23 | 59 | mv_kb_90_7_D | 104 | head |
| v241reg_j40_rlw_o_r1 | 6.50 | 32 | mv_kb_0_9_W | 272 | head |
| v241reg_j40_rlw_tkha_r1 | 6.13 | 33 | mv_kb_-90_7_A | 135 | head |

Karşılaştırma: V2.40 `tk` (AO yok) 120 FPS koşularında tepe 117–307 m/s² (`Saved/Codex/SHME_V212_20261017/Reports/v240*120*_tk_r1.txt`).
