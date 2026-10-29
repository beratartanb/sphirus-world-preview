## 1. Worst planted-ball slide / drag (cm, owner clip) and reversal hold (s), fixed 30 FPS: V2.37 production (o) vs pre237 (V2.36 values); + = first-build run (never searches the stop DB)

| scenario | o | o owner | pre237 | pre237 owner | o hold | pre237 hold |
|---|---|---|---|---|---|---|
| j36_stop | 0.0 |  | 5.6 | SHM236_JogStop_Br_P00 | 0.00 | 0.00 |
| j36_stopb | 6.8 | SHM237_JogStop_Bl_P08 | 5.9 | A_CP2_Jog_Fwd_Start | 0.00 | 0.00 |
| j36_stopr | 5.5 | SHM237_JogStop_Bl_P16 | 14.2 | SHM236_JogStart_F_Lfoot | 0.00 | 0.00 |
| j36_rse | 0.0 |  | 5.6 | SHM236_JogStop_Br_P00 | 0.00 | 0.00 |
| j36_rsm | 0.0 |  | 9.5 | SHM236_JogStop_Br_P03 | 0.00 | 0.00 |
| j36_rsl | 6.8 | SHM237_JogStop_Br_P12 | 8.7 | SHM236_JogStart_F_Lfoot | 0.00 | 0.00 |
| j36_rsx | 17.1 | SHM236_JogRev_F_B_P15 | 17.9 | SHM236_JogRev_F_B_P16 | 0.03 | 0.03 |
| j36_wjs | 8.9 | SHM237_JogStop_Bl_P09 | 14.3 | SHM236_JogStart_F_Lfoot | 0.00 | 0.00 |
| j36_wjsb | 13.3 | A_CT_Jog_Fwd | 16.6 | SHM236_JogStart_F_Lfoot | 0.00 | 0.00 |
| j36_sside | 22.2 | A_LS_Jog_Right_Start | 21.7 | A_LS_Jog_Right_Start | 0.00 | 0.00 |
| j35_rev | 9.3 | SHM236_JogRev_F_B_P21 | 8.0 | SHM236_JogRev_F_B_P16 | 0.07 | 0.07 |
| j35_rev2 | 7.0+ | SHM236_JogRev_B_F_P17 | 9.3+ | A_RB_Jog_Rear | 0.10 | 0.10 |
| j35_relstop | 9.9+ | SHM236_JogRev_F_B_P21 | - |  | 0.00 | - |
| j30_rel_3200 | 9.0 | SHM236_JogRev_F_B_P21 | - |  | 0.07 | - |
| j30_rel_3450 | 10.3 | SHM236_JogRev_B_F_P1 | 16.3 | SHM236_JogRev_B_F_P27 | 0.07 | 0.07 |
| j30_slow | 9.3 | A_RB_Jog_Rear | - |  | 0.07 | - |
| j34_chain1 | 7.9 | A_CT_Jog_Fwd | 17.1 | SHM236_JogStart_F_Lfoot | 0.07 | 0.07 |
| jstart | 57.4 | af_Loco_Jog_Start_TurnR045_Rfo | 50.2 | af_Loco_Jog_Left_Start_AAMS | 0.00 | 0.00 |
| wstart | 14.2+ | SHM_StartTransfer_FR_Rfoot | - |  | 0.00 | - |
| c29_combo | 15.4+ | A_LB_Walk_Left | 7.9+ | A_CR_Stand_M_Neutral_Walk_Pivo | 0.00 | 0.00 |
| e29_chain | 11.1+ | SHM218_W2S_Lfoot_a | 6.5+ | M_Ranger_Walk_Loop_F_PureForwa | 0.07 | 0.07 |
| e29_load | 14.2+ | SHM231L_LoadRev_B_F_P31 | 14.2+ | SHM231L_LoadRev_B_F_P31 | 0.13 | 0.13 |
| jback | 6.8+ | SHM_M_Neutral_Walk_Stop_BL_Rfo | 5.2+ | A_RB_Jog_Rear | 0.00 | 0.00 |
| wdiag | 12.7+ | A_CR_Stand_M_Neutral_Walk_Pivo | - |  | 0.00 | - |
| s29_swl12 | 11.1+ | SHM218_W2S_Lfoot_a | - |  | 0.03 | - |
| s34_straight | 15.9+ | A_RR_M_Relaxed_Run_Start_F_Rfo | - |  | 0.00 | - |
| ter_drop_jog | 5.0 | SHM237_JogStart_F_Rfoot | 7.7 | SHM236_JogStop_Br_P14 | 0.00 | 0.00 |
| map_r1 | 249.5+ | A_LB_Walk_Fwd | - |  | 0.00 | - |

## 2. Whole-body stop audit (stop236, visible mesh) + brake-window pelvis, fixed 30

| run | release s | arm swing kept | pull-back cm | trunk deg @0 / @+0.6 | pelvis dip vs final (incl. loop bob) | BRAKE pelvis min cm | support knee deg there | FootPlacement pelvis there cm | last landing s |
|---|---|---|---|---|---|---|---|---|---|
| j36_stop o | 5.07 | 0.48 | 8.7 | 13.3 / 0.2 | -5.9 | 90.2 | 142 | -0.5 | 1.5 |
| j36_stop pre237 | 5.07 | 0.54 | 2.7 | 11.9 / 0.6 | -8.5 | 84.5 | 117 | -6.2 | 0.83 |
| j36_stopb o | 5.27 | 0.4 | 14.8 | 12.9 / 0.2 | -5.6 | 87.4 | 131 | -0.6 | 1.0 |
| j36_stopb pre237 | 5.27 | 0.35 | 8.6 | 12.6 / 0.3 | -9.8 | 83.4 | 115 | -8.7 | 1.73 |
| j36_stopr o | 5.07 | 0.48 | 8.7 | 13.3 / 0.2 | -5.9 | 90.2 | 145 | -0.5 | 1.5 |
| j36_stopr o | 9.07 | 0.47 | 8.7 | 10.0 / 0.3 | -5.9 | 90.2 | 146 | -0.5 | 1.47 |
| j36_stopr pre237 | 5.07 | 0.54 | 2.7 | 11.9 / 0.6 | -8.4 | 84.5 | 117 | -6.2 | 0.83 |
| j36_stopr pre237 | 9.07 | 0.46 | 3.1 | 11.4 / 0.7 | -6.3 | 86.7 | 134 | -2.2 | 1.2 |
| j36_wjs o | 6.07 | 0.46 | 19.5 | 12.6 / 0.1 | -6.4 | 86.9 | 128 | -0.5 | 1.33 |
| j36_wjs o | 9.67 | 0.44 | 19.7 | 11.2 / -0.0 | -6.1 | 87.3 | 120 | -0.5 | 1.37 |
| j36_wjs pre237 | 6.07 | 0.36 | 5.5 | 12.7 / 0.8 | -6.4 | 86.5 | 119 | -0.6 | 1.1 |
| j36_wjs pre237 | 9.67 | 0.45 | 12.1 | 15.0 / 0.9 | -10.6 | 82.3 | 112 | -8.4 | 0.9 |
| j36_wjsb o | 6.27 | 0.57 | 0.3 | 14.7 / 0.5 | -6.4 | 88.9 | 130 | -0.9 | 0.8 |
| j36_wjsb o | 9.87 | 0.45 | 19.7 | 11.3 / 0.1 | -6.1 | 87.3 | 121 | -0.5 | 1.37 |
| j36_wjsb pre237 | 6.27 | 0.54 | 0.1 | 14.7 / 1.0 | -10.9 | 82.1 | 111 | -5.9 | 1.17 |
| j36_wjsb pre237 | 9.87 | 0.47 | 12.1 | 15.1 / 1.0 | -10.6 | 82.3 | 112 | -8.4 | 0.87 |

## 3. Start / re-push clip episodes (clip time span, clip rate), fixed 30

| run | episodes |
|---|---|
| j36_wjs o | JogStart_F_Lfoot 0.00-0.93 r1.03 |
| j36_wjs pre237 | 6:JogStart_F_Lfoot 0.00-0.48 r0.79 |
| j34_chain1 o | JogStart_F_Lfoot 0.00-0.58 r0.96; RePush_Br_P01_T057 0.20-0.59 r1.05 |
| j34_chain1 pre237 | 6:JogStart_F_Lfoot 0.00-0.45 r0.75 |
| j36_rsm o | JogStart_F_Rfoot 0.00-0.93 r1.03; JogStart_F_Lfoot 0.47-0.98 r1.02 |
| j36_rsm pre237 | none |
| j36_rse o | JogStart_F_Rfoot 0.00-0.93 r1.03 |
| j36_rse pre237 | none |
| j36_rsl o | JogStart_F_Rfoot 0.00-0.93 r1.03; JogStart_F_Rfoot 0.00-0.95 r1.01 |
| j36_rsl pre237 | 6:JogStart_F_Lfoot 0.00-0.48 r0.80 |
| j36_stopr o | JogStart_F_Rfoot 0.00-0.93 r1.03; JogStart_F_Rfoot 0.00-0.94 r1.01 |
| j36_stopr pre237 | 6:JogStart_F_Lfoot 0.00-0.48 r0.79 |
| jstart o | JogStart_F_Rfoot 0.00-0.93 r1.03 |
| jstart pre237 | none |

## 4. Frame-rate modes: worst slide cm o / pre237 (reversal hold s o / pre237); * = database-not-ready frames in the run

| scenario | 30 | 60 | 120 | 20 | real |
|---|---|---|---|---|---|
| j36_stop | 0.0 / 5.6 (0.00 / 0.00) | 6.7 / 8.5 (0.00 / 0.00) | 5.0 / 8.4 (0.00 / 0.00) | 0.0 / 8.7 (0.00 / 0.00) | 6.6 / 7.5+ (0.00 / 0.00) |
| j36_stopr | 5.5 / 14.2 (0.00 / 0.00) | 0.0 / 8.6 (0.00 / 0.00) | 6.2 / 12.5 (0.00 / 0.00) | 7.9 / 9.6 (0.00 / 0.00) | 8.5 / 16.1 (0.00 / 0.00) |
| j36_rsm | 0.0 / 9.5 (0.00 / 0.00) | 6.4 / 26.4 (0.00 / 0.00) | 5.0 / 44.1 (0.00 / 0.00) | 0.0 / 35.0 (0.00 / 0.00) | 0.0 / 15.0 (0.00 / 0.00) |
| j36_wjs | 8.9 / 14.3 (0.00 / 0.00) | 6.4 / 8.6 (0.00 / 0.00) | 11.3 / 20.1 (0.00 / 0.00) | 6.0 / 16.5 (0.00 / 0.00) | 14.0 / 13.5 (0.00 / 0.00) |
| j34_chain1 | 7.9 / 17.1 (0.07 / 0.07) | 6.8 / 27.9 (0.07 / 0.07) | 6.7 / 33.3 (0.12 / 0.12) | 10.8 / 17.3 (0.10 / 0.10) | 9.9+ / 17.9+ (0.07 / 0.07) |
| j35_rev | 9.3 / 8.0 (0.07 / 0.07) | 12.3+ / 10.0 (0.05 / 0.07) | 8.8 / 21.3 (0.03 / 0.03) | 7.9 / 7.1 (0.10 / 0.05) | 6.6 / 8.6 (0.06 / 0.12) |
| j30_rel_3450 | 10.3 / 16.3 (0.07 / 0.07) | 13.4 / 9.3 (0.05 / 0.05) | 9.1 / 9.0 (0.04 / 0.04) | 6.4 / 10.5 (0.05 / 0.05) | 6.4 / 9.7 (0.04 / 0.03) |
| jstart | 57.4 / 50.2 (0.00 / 0.00) | 46.3 / 46.2 (0.00 / 0.00) | 45.3 / 44.5 (0.00 / 0.00) | 54.1 / 54.1 (0.00 / 0.00) | 70.9 / 66.2 (0.00 / 0.00) |
| c29_combo | 15.4+ / 7.9+ (0.00 / 0.00) | 11.8+ / 11.8+ (0.00 / 0.00) | 12.9+ / 12.9+ (0.00 / 0.00) | 8.9+ / 8.9+ (0.00 / 0.00) | 13.0+ / 12.9+ (0.00 / 0.00) |
| e29_chain | 11.1+ / 6.5+ (0.07 / 0.07) | 19.8+ / 20.6+ (0.07 / 0.07) | 17.3+ / 17.6+ (0.08 / 0.08) | 6.0+ / 9.0+ (0.05 / 0.05) | 21.1+ / 13.9+ (0.09 / 0.06) |
| e29_load | 14.2+ / 14.2+ (0.13 / 0.13) | 12.6+ / 12.6+ (0.15 / 0.15) | 17.9+ / 17.9+ (0.10 / 0.10) | 7.0+ / 7.1+ (0.15 / 0.15) | 13.7+ / 6.4+ (0.15 / 0.14) |
| j36_sside | 22.2 / 21.7 (0.00 / 0.00) | 24.0+ / 35.9 (0.00 / 0.00) | 20.4 / 36.2 (0.00 / 0.00) | 17.3 / 17.7 (0.00 / 0.00) | 27.7 / 32.9 (0.00 / 0.00) |

## 5. Cold first use in the clean editor (no warm run): frames with no database + worst slide

| run | no-DB frames | worst cm |
|---|---|---|
| v237cold2_j36_stop_o_r1 | 0 | 0.0 |
| v237cold2_j36_rsm_o_r1 | 0 | 7.7 |
| v237cold2_j36_wjs_o_r1 | 0 | 6.5 |
| v237cold2_j34_chain1_o_r1 | 0 | 7.5 |
| v237cold2_j35_rev_o_r1 | 0 | 9.3 |
