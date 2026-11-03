# TABLES V2.51 (2026-11-03)

contact250 on the visible skeleton: PEN = deepest ball below the standing floor (cm, negative = above), PLANT = planted-point translation per contact (pivot is not a slide), BALL = ball travel while grounded; then pivot249, contact231 (ball only), pops >25 m/s2 / worst.

## 1. Start windows, same session before (pre = V2.51 knobs off) vs after (o), 60 FPS jstart
| v251f60_jstart_pre_r1 | 45deg | l PEN 3.8 PLANT 3.4 BALL 3.9 r PEN 3.9 PLANT 2.4 BALL 4.9  |
| v251f60_jstart_pre_r1 | lateral | l PEN 4.4 PLANT 0.8 BALL 4.5 r PEN 5.0 PLANT 1.1 BALL 4.2  |
| v251f60_jstart_pre_r1 | backward-1 | l PEN -0.5 PLANT 0.1 BALL 0.6 r PEN -0.7 PLANT 4.6 BALL 4.7  |
| v251f60_jstart_pre_r1 | backward-2 | l PEN 3.9 PLANT 0.3 BALL 0.3 r PEN 4.0 PLANT 5.5 BALL 7.4  |
| v251f60_jstart_pre_r1 | 180 | l PEN -1.7 PLANT 0.3 BALL 0.7 r PEN 0.3 PLANT 4.0 BALL 7.1  |
| v251f60_jstart_o_r1 | 45deg | l PEN -0.5 PLANT 1.6 BALL 2.1 r PEN -0.7 PLANT 0.2 BALL 0.5  |
| v251f60_jstart_o_r1 | lateral | l PEN -0.2 PLANT 0.7 BALL 2.1 r PEN 1.1 PLANT 0.9 BALL 2.1  |
| v251f60_jstart_o_r1 | backward-1 | l PEN -0.5 PLANT 1.0 BALL 1.2 r PEN -0.7 PLANT 2.8 BALL 3.2  |
| v251f60_jstart_o_r1 | backward-2 | l PEN -1.9 PLANT 0.0 BALL 0.0 r PEN -1.8 PLANT 4.1 BALL 4.2  |
| v251f60_jstart_o_r1 | 180 | l PEN -1.7 PLANT 0.3 BALL 0.7 r PEN 0.9 PLANT 4.0 BALL 4.1  |

## 2. Start-window penetration, all FPS (45 / lateral / backward; l r)
| v251f120_jstart_o_r1 | -0.5/-0.6/ -0.1/1.1/ -1.9/-1.8/  |
| v251f20_jstart_o_r1 | -0.6/-0.7/ -0.2/1.1/ -2.0/-1.9/  |
| v251f30_jstart_o_r1 | -0.5/-0.7/ -0.1/1.1/ -1.9/-1.8/  |
| v251f60_jstart_o_r1 | -0.5/-0.7/ -0.2/1.1/ -1.9/-1.8/  |
| v251f60_jstart_pre_r1 | 3.8/3.9/ 4.4/5.0/ 3.9/4.0/  |
| v251freal_jstart_o_r1 | -0.7/-0.8/ -0.4/1.0/ -2.3/-1.9/  |
| v251freal_jstart_o_r2 | -0.7/-0.5/ -0.5/-0.6/ -2.2/-1.8/  |

## 3. Production after promotion (chain F)
| v251f60_gait_o_r1 | PEN 2.2/1.8 | PLANT 6.6/8.9 | BALL 7.8/9.2 | 8.0 (SHM245_Walk_Fwd) | 10.6 | 21 / 52 |
| v251f60_j40_rlw_o_r1 | PEN 2.4/2.2 | PLANT 2.4/4.2 | BALL 4.2/6.0 | 4.8 (SHM237_RePush_Bl_P08_T057) | 18.7 | 12 / 40 |
| v251f60_j41_rl_p10_o_r1 | PEN 1.5/2.2 | PLANT 4.2/4.8 | BALL 10.0/9.3 | 2.9 (SHM244_LatStop_L_Br_P00) | 9.3 | 16 / 37 |
| v251f60_j45_sl2_o_r1 | PEN 1.4/2.2 | PLANT 3.7/6.1 | BALL 8.7/8.7 | 2.8 (A_CT_Jog_Fwd) | 12.1 | 18 / 51 |
| v251f60_j45_sl_o_r1 | PEN 1.7/1.9 | PLANT 6.0/3.5 | BALL 6.9/6.7 | 2.9 (A_CT_Jog_Fwd) | 17.4 | 13 / 52 |
| v251f60_jstart_o_r1 | PEN 3.0/2.4 | PLANT 8.2/10.8 | BALL 12.6/11.0 | 10.8 (A_CT_Jog_FwdLeft) | 50.0 | 14 / 81 |
| v251f60_jstart_pre_r1 | PEN 4.4/5.0 | PLANT 5.4/11.3 | BALL 7.7/11.3 | 19.2 (ogQ_af_Loco_Jog_Bwd_Start_AAMS) | 37.8 | 19 / 73 |
| v251f60_taps_o_r1 | PEN 1.0/2.6 | PLANT 8.2/13.6 | BALL 13.2/19.0 | 18.4 (SHM_StartTransfer_BL_Lfoot) | 18.8 | 6 / 61 |
| v251f60_w42_id_o_r1 | PEN 1.9/0.8 | PLANT 5.9/8.0 | BALL 11.2/8.4 | 6.6 (_Idle_NaturalBaseline_Phase275) | 10.2 | 2 / 33 |
| v251f60_w43_idle_o_r1 | PEN 1.0/0.8 | PLANT 9.1/3.7 | BALL 9.1/4.2 | 8.2 (_Idle_NaturalBaseline_Phase275) | 5.5 | 4 / 39 |
| v251f60_wstart_o_r1 | PEN 1.8/2.5 | PLANT 12.3/14.5 | BALL 13.7/14.6 | 13.8 (A_LB_Walk_Right) | 23.5 | 5 / 36 |
| v251f30_gait_o_r1 | PEN 1.8/1.7 | PLANT 3.6/6.6 | BALL 5.7/6.6 | 5.2 (SHM245_Walk_Fwd) | 6.8 | 0 / 0 |
| v251f30_j40_rlw_o_r1 | PEN 6.1/1.7 | PLANT 5.0/6.4 | BALL 8.5/6.4 | 2.8 (A_CT_Jog_Fwd) | 44.9 | 5 / 56 |
| v251f30_j41_rl_p10_o_r1 | PEN 2.4/1.5 | PLANT 4.3/7.5 | BALL 7.3/9.3 | 5.9 (A_CT_Jog_Fwd) | 19.4 | 2 / 28 |
| v251f30_j42_lr_p10_o_r1 | PEN 1.9/2.2 | PLANT 2.3/14.7 | BALL 10.6/15.3 | 6.7 (SHM_JogQ_A_LS_Jog_Right_Start) | 10.9 | 1 / 27 |
| v251f30_j45_sl2_o_r1 | PEN 1.6/2.2 | PLANT 2.1/6.0 | BALL 7.0/8.2 | 2.4 (A_CT_Jog_Fwd) | 10.2 | 2 / 29 |
| v251f30_jstart_o_r1 | PEN 3.1/2.3 | PLANT 8.6/7.9 | BALL 15.0/9.5 | 11.8 (HM_M_Neutral_Walk_Stop_F_Rfoot) | 34.8 | 1 / 26 |
| v251f30_taps_o_r1 | PEN 1.0/2.9 | PLANT 8.2/14.2 | BALL 8.6/19.7 | 13.5 (_Idle_NaturalBaseline_Phase275) | 17.3 | 0 / 0 |
| v251f30_w42_id_o_r1 | PEN 1.9/0.8 | PLANT 6.7/6.5 | BALL 11.0/7.3 | 7.2 (HM_M_Neutral_Walk_Stop_F_Rfoot) | 10.2 | 0 / 0 |
| v251f30_w43_idle_o_r1 | PEN 1.0/0.8 | PLANT 7.2/3.6 | BALL 7.5/4.6 | 7.3 (_Idle_NaturalBaseline_Phase275) | 6.5 | 0 / 0 |
| v251f30_wstart_o_r1 | PEN 2.1/2.4 | PLANT 20.9/15.9 | BALL 21.0/16.7 | 14.6 (_Idle_NaturalBaseline_Phase275) | 21.0 | 0 / 0 |
| v251freal_j45_sl2_o_r1 | PEN 1.6/1.8 | PLANT 2.2/4.6 | BALL 6.8/5.9 | 2.5 (A_CT_Jog_Fwd) | 11.7 | 2 / 31 |
| v251freal_j45_sl2_o_r2 | PEN 1.6/1.9 | PLANT 3.4/4.8 | BALL 7.8/8.8 | 3.4 (A_CT_Jog_Fwd) | 12.7 | 3 / 30 |
| v251freal_j45_sl2_o_r3 | PEN 1.6/2.0 | PLANT 3.7/2.7 | BALL 6.5/7.8 | 2.1 (A_CT_Jog_Fwd) | 12.9 | 2 / 26 |
| v251freal_j45_sl2_o_r4 | PEN 1.6/1.9 | PLANT 3.4/5.3 | BALL 7.4/9.1 | 2.7 (SHM238_Cut_R_P21) | 11.8 | 2 / 33 |
| v251freal_jstart_o_r1 | PEN 3.0/3.8 | PLANT 8.4/8.8 | BALL 9.4/9.9 | 0.9 (A_LS_Jog_Right_Start) | 56.2 | 3 / 42 |
| v251freal_jstart_o_r2 | PEN 2.8/2.5 | PLANT 8.5/7.6 | BALL 8.9/10.4 | 5.0 (SHM_JogQ_A_LS_Jog_Left_Start) | 35.5 | 3 / 42 |
| v251freal_taps_o_r1 | PEN 0.9/2.7 | PLANT 6.8/13.6 | BALL 7.1/19.3 | 15.5 (SHM_StartTransfer_BL_Lfoot) | 15.9 | 2 / 33 |
| v251freal_wstart_o_r1 | PEN 1.3/2.3 | PLANT 22.6/12.9 | BALL 22.7/13.1 | 22.5 (_Idle_NaturalBaseline_Phase275) | 22.6 | 0 / 0 |
| v251f20_j45_sl2_o_r1 | PEN 1.7/2.0 | PLANT 4.8/5.4 | BALL 7.5/7.0 | 4.8 (SHM238_Cut_R_P21) | 9.5 | 0 / 0 |
| v251f20_jstart_o_r1 | PEN 4.7/5.1 | PLANT 6.2/7.8 | BALL 6.9/11.8 | PIVOT249 v251f20_jstart_o_r1 worst translation 0.0 cm (None) | 49.2 | 0 / 0 |
| v251f20_w43_idle_o_r1 | PEN 1.0/0.6 | PLANT 5.9/6.5 | BALL 6.1/8.5 | 6.0 (_Idle_NaturalBaseline_Phase275) | 6.0 | 0 / 0 |
| v251f120_j45_sl2_o_r1 | PEN 1.6/2.2 | PLANT 4.7/5.8 | BALL 9.0/9.0 | 4.7 (A_CT_Jog_Fwd) | 10.3 | 14 / 92 |
| v251f120_jstart_o_r1 | PEN 2.7/2.4 | PLANT 4.7/9.7 | BALL 5.4/11.0 | 34.8 (A_CT_Jog_FwdLeft) | 59.3 | 24 / 102 |
| v251f120_w43_idle_o_r1 | PEN 1.0/0.7 | PLANT 7.5/7.4 | BALL 7.5/7.6 | 6.9 (_Idle_NaturalBaseline_Phase275) | 5.4 | 10 / 86 |

## 4. V2.50 production references
| v250d60_gait_o_r1 | PEN 2.2/1.8 | PLANT 6.6/8.9 | BALL 7.8/9.2 | 8.0 (SHM245_Walk_Fwd) | 10.6 | 21 / 52 |
| v250d60_j40_rlw_o_r1 | PEN 1.9/2.1 | PLANT 2.4/9.7 | BALL 4.3/9.7 | 5.4 (A_CT_Jog_Fwd) | 9.9 | 14 / 40 |
| v250d60_j41_rl_p10_o_r1 | PEN 1.5/2.2 | PLANT 4.2/4.9 | BALL 10.0/9.6 | 2.9 (SHM244_LatStop_L_Br_P00) | 9.3 | 16 / 37 |
| v250d60_j45_sl2_o_r1 | PEN 1.7/1.9 | PLANT 6.0/3.5 | BALL 6.9/6.7 | 2.9 (A_CT_Jog_Fwd) | 17.4 | 19 / 52 |
| v250d60_j45_sl_o_r1 | PEN 1.7/1.9 | PLANT 6.0/7.8 | BALL 6.9/8.5 | 6.3 (SHM237_JogStop_Br_P15) | 17.4 | 14 / 51 |
| v250d60_jstart_o_r1 | PEN 4.4/5.0 | PLANT 5.8/11.3 | BALL 7.6/11.3 | 19.9 (ogQ_af_Loco_Jog_Bwd_Start_AAMS) | 37.8 | 17 / 77 |
| v250d60_taps_o_r1 | PEN 1.0/2.6 | PLANT 18.3/13.6 | BALL 18.4/19.0 | 18.9 (SHM_StartTransfer_B_Rfoot) | 18.8 | 5 / 61 |
| v250d60_w42_id_o_r1 | PEN 1.9/0.8 | PLANT 5.9/8.0 | BALL 11.2/8.4 | 6.6 (_Idle_NaturalBaseline_Phase275) | 10.2 | 2 / 33 |
| v250d60_w43_idle_o_r1 | PEN 1.0/0.8 | PLANT 9.1/3.7 | BALL 9.1/4.2 | 8.2 (_Idle_NaturalBaseline_Phase275) | 5.5 | 4 / 39 |
| v250d60_wstart_o_r1 | PEN 1.8/2.5 | PLANT 12.3/14.5 | BALL 13.7/14.6 | 13.8 (A_LB_Walk_Right) | 23.5 | 5 / 36 |
| v250d30_gait_o_r1 | PEN 1.8/1.7 | PLANT 3.6/6.6 | BALL 5.7/6.6 | 5.2 (SHM245_Walk_Fwd) | 6.8 | 0 / 0 |
| v250d30_j40_rlw_o_r1 | PEN 6.1/1.7 | PLANT 5.0/6.4 | BALL 8.9/6.4 | 3.0 (SHM238_Cut_R_P21) | 44.9 | 6 / 56 |
| v250d30_j41_rl_p10_o_r1 | PEN 3.6/2.3 | PLANT 4.0/7.5 | BALL 7.5/9.3 | 1.3 (A_CT_Jog_Fwd) | 28.3 | 2 / 28 |
| v250d30_j42_lr_p10_o_r1 | PEN 1.7/2.2 | PLANT 2.5/12.6 | BALL 9.1/13.6 | 6.7 (A_CT_Jog_Right) | 17.3 | 1 / 26 |
| v250d30_j45_sl2_o_r1 | PEN 1.6/2.2 | PLANT 2.1/7.5 | BALL 7.0/8.9 | 5.3 (SHM_JogQ_A_LS_Jog_Left_Start) | 10.2 | 2 / 30 |
| v250d30_jstart_o_r1 | PEN 4.3/4.4 | PLANT 8.5/7.6 | BALL 15.4/12.9 | 2.0 (f_Loco_Jog_Start_TurnR045_Rfoo) | 34.3 | 1 / 25 |
| v250d30_taps_o_r1 | PEN 1.0/2.9 | PLANT 8.2/14.2 | BALL 13.1/19.7 | 13.5 (_Idle_NaturalBaseline_Phase275) | 17.3 | 0 / 0 |
| v250d30_w42_id_o_r1 | PEN 1.9/0.8 | PLANT 6.7/6.5 | BALL 11.0/7.3 | 7.2 (HM_M_Neutral_Walk_Stop_F_Rfoot) | 10.2 | 0 / 0 |
| v250d30_w43_idle_o_r1 | PEN 1.0/0.8 | PLANT 7.2/3.6 | BALL 7.5/4.6 | 7.3 (_Idle_NaturalBaseline_Phase275) | 6.5 | 0 / 0 |
| v250d30_wstart_o_r1 | PEN 2.1/2.4 | PLANT 20.9/15.9 | BALL 21.0/16.7 | 14.6 (_Idle_NaturalBaseline_Phase275) | 21.0 | 0 / 0 |
| v250dreal_j45_sl2_o_r1 | PEN 1.6/1.9 | PLANT 2.4/6.1 | BALL 7.4/8.5 | 5.7 (SHM_JogQ_A_LS_Jog_Left_Start) | 13.4 | 2 / 30 |
| v250dreal_j45_sl2_o_r2 | PEN 1.1/1.8 | PLANT 2.5/4.6 | BALL 5.5/7.4 | 3.1 (SHM_JogQ_A_LS_Jog_Left_Start) | 14.2 | 3 / 30 |
| v250dreal_j45_sl2_o_r3 | PEN 1.7/1.8 | PLANT 5.9/5.5 | BALL 6.4/10.8 | 2.8 (A_CT_Jog_Fwd) | 12.7 | 2 / 29 |
| v250dreal_j45_sl2_o_r4 | PEN 1.3/2.4 | PLANT 2.2/6.2 | BALL 5.7/11.4 | 7.7 (A_CT_Jog_FwdRight) | 11.6 | 3 / 31 |
| v250dreal_j45_sl2_o_r5 | PEN 1.7/2.0 | PLANT 2.5/6.4 | BALL 8.2/7.7 | 3.1 (SHM_JogQ_A_LS_Jog_Left_Start) | 14.3 | 3 / 32 |
| v250dreal_jstart_o_r1 | PEN 3.0/4.0 | PLANT 4.4/8.3 | BALL 6.1/15.0 | 5.5 (SHM_JogQ_A_LS_Jog_Right_Start) | 52.5 | 5 / 30 |
| v250dreal_jstart_o_r2 | PEN 3.9/4.3 | PLANT 8.9/9.7 | BALL 10.2/11.0 | 0.0 (SHM_JogQ_A_LS_Jog_Right_Start) | 61.0 | 4 / 26 |
| v250dreal_taps_o_r1 | PEN 0.9/2.7 | PLANT 8.0/13.3 | BALL 12.3/18.6 | 15.4 (_Idle_NaturalBaseline_Phase275) | 18.2 | 1 / 28 |
| v250dreal_wstart_o_r1 | PEN 1.5/2.4 | PLANT 11.1/14.9 | BALL 11.2/16.1 | 12.6 (A_LB_Walk_Right) | 20.1 | 1 / 30 |
| v250d20_j45_sl2_o_r1 | PEN 1.7/2.1 | PLANT 3.2/5.4 | BALL 9.0/8.1 | 1.2 (SHM237_JogStop_Bl_P17) | 9.5 | 0 / 0 |
| v250d20_jstart_o_r1 | PEN 4.3/2.4 | PLANT 9.2/8.4 | BALL 15.5/13.9 | 19.6 (HM_M_Neutral_Walk_Stop_F_Rfoot) | 49.8 | 3 / 26 |
| v250d20_w43_idle_o_r1 | PEN 1.0/0.6 | PLANT 5.9/6.5 | BALL 6.1/8.5 | 6.0 (_Idle_NaturalBaseline_Phase275) | 6.0 | 0 / 0 |
| v250d120_j45_sl2_o_r1 | PEN 1.6/2.2 | PLANT 4.7/7.2 | BALL 9.0/9.2 | 5.4 (SHM_JogQ_A_LS_Jog_Left_Start) | 10.3 | 17 / 92 |
| v250d120_jstart_o_r1 | PEN 3.9/3.5 | PLANT 4.7/9.2 | BALL 5.3/10.4 | 20.9 (ogQ_af_Loco_Jog_Bwd_Start_AAMS) | 50.3 | 23 / 102 |
| v250d120_w43_idle_o_r1 | PEN 1.0/0.7 | PLANT 7.5/7.4 | BALL 7.5/7.6 | 6.9 (_Idle_NaturalBaseline_Phase275) | 5.4 | 10 / 86 |

## 5. Weighted idle (oiL = idle + V2.51 fixes), before / after the relaxed-leg rule
| v251b30_gait_oiL_r1 | PEN 2.1/3.0 | PLANT 3.0/9.5 | BALL 5.6/10.0 | 5.9 (A_CT_Jog_Fwd) | 14.7 | 4 / 30 |
| v251b30_j45_sl2_oiL_r1 | PEN 2.0/2.8 | PLANT 3.2/8.3 | BALL 5.8/9.9 | 2.0 (A_CT_Jog_Fwd) | 10.2 | 2 / 29 |
| v251b30_jstart_oiL_r1 | PEN 3.5/2.9 | PLANT 6.3/12.1 | BALL 11.7/15.7 | 11.8 (HM_M_Neutral_Walk_Stop_F_Rfoot) | 37.4 | 1 / 26 |
| v251b30_taps_oiL_r1 | PEN 1.5/1.4 | PLANT 10.7/12.6 | BALL 12.4/13.5 | 10.9 (SHM_StartTransfer_BL_Lfoot) | 11.9 | 1 / 26 |
| v251b30_w42_id_oiL_r1 | PEN 1.3/1.3 | PLANT 7.4/8.2 | BALL 8.0/8.2 | 12.5 (SHM244_Idle_Weighted) | 19.7 | 0 / 0 |
| v251b30_w43_idle_oiL_r1 | PEN 1.3/1.4 | PLANT 7.8/5.8 | BALL 8.3/5.9 | 3.8 (SHM244_Idle_Weighted) | 6.4 | 0 / 0 |
| v251b30_wstart_oiL_r1 | PEN 1.3/3.6 | PLANT 15.5/16.1 | BALL 17.2/18.1 | 24.0 (SHM_StartTransfer_LR_Rfoot) | 39.5 | 1 / 29 |
| v251b60_gait_oiL_r1 | PEN 2.0/2.7 | PLANT 2.0/10.6 | BALL 6.8/11.0 | 8.2 (A_CT_Jog_Fwd) | 14.0 | 23 / 70 |
| v251b60_j45_sl2_oiL_r1 | PEN 2.1/2.6 | PLANT 3.7/7.0 | BALL 8.2/9.4 | 2.9 (SHM238_Cut_R_P21) | 12.0 | 18 / 52 |
| v251b60_taps_oiL_r1 | PEN 1.6/1.1 | PLANT 12.8/5.5 | BALL 13.5/7.2 | 9.3 (SHM244_Idle_Weighted) | 6.5 | 6 / 37 |
| v251b60_w42_id_oiL_r1 | PEN 1.3/1.3 | PLANT 10.3/9.1 | BALL 12.6/9.1 | 10.6 (SHM244_Idle_Weighted) | 20.2 | 2 / 32 |
| v251b60_w43_idle_oiL_r1 | PEN 1.3/1.2 | PLANT 6.1/8.4 | BALL 6.1/8.4 | 4.8 (SHM244_Idle_Weighted) | 5.6 | 2 / 26 |
| v251b60_wstart_oiL_r1 | PEN 2.0/2.9 | PLANT 12.0/14.8 | BALL 13.2/14.9 | 14.1 (A_LB_Walk_Right) | 27.7 | 2 / 36 |
| v251d30_gait_oiL_r1 | PEN 2.1/3.0 | PLANT 3.0/9.5 | BALL 5.6/10.0 | 5.9 (A_CT_Jog_Fwd) | 14.7 | 4 / 30 |
| v251d30_j45_sl2_oiL_r1 | PEN 2.0/2.8 | PLANT 3.2/8.3 | BALL 5.7/9.9 | 2.0 (A_CT_Jog_Fwd) | 10.2 | 2 / 29 |
| v251d30_jstart_oiL_r1 | PEN 3.5/2.9 | PLANT 6.3/12.1 | BALL 11.7/15.7 | 11.8 (HM_M_Neutral_Walk_Stop_F_Rfoot) | 37.4 | 1 / 26 |
| v251d30_taps_oiL_r1 | PEN 1.5/1.2 | PLANT 10.7/6.1 | BALL 12.4/8.1 | 6.7 (SHM244_Idle_Weighted) | 6.7 | 2 / 26 |
| v251d30_w42_id_oiL_r1 | PEN 1.5/1.5 | PLANT 8.2/6.3 | BALL 9.9/6.7 | 5.4 (HM_M_Neutral_Walk_Stop_F_Rfoot) | 8.8 | 0 / 0 |
| v251d30_w43_idle_oiL_r1 | PEN 1.3/1.4 | PLANT 7.8/5.8 | BALL 8.3/5.9 | 3.8 (SHM244_Idle_Weighted) | 6.4 | 0 / 0 |
| v251d30_wstart_oiL_r1 | PEN 2.4/3.0 | PLANT 9.7/15.7 | BALL 10.4/16.5 | 12.2 (A_LB_Walk_Right) | 30.0 | 0 / 0 |
| v251d60_gait_oiL_r1 | PEN 2.2/2.8 | PLANT 2.0/10.6 | BALL 6.8/11.0 | 8.2 (A_CT_Jog_Fwd) | 14.0 | 23 / 70 |
| v251d60_taps_oiL_r1 | PEN 1.6/1.1 | PLANT 12.8/5.5 | BALL 13.5/7.2 | 9.3 (SHM244_Idle_Weighted) | 6.5 | 6 / 37 |
| v251d60_w42_id_oiL_r1 | PEN 1.8/1.3 | PLANT 10.3/9.1 | BALL 12.6/9.1 | 7.0 (SHM245_Walk_Fwd) | 10.7 | 2 / 32 |
| v251d60_wstart_oiL_r1 | PEN 2.0/2.9 | PLANT 12.0/15.1 | BALL 12.6/15.2 | 14.4 (A_LB_Walk_Right) | 29.7 | 2 / 36 |

## 6. A/B chains (eA / eY / eAY / eAYL / eAYLX / crop block)
| v251a30_gait_eAY_r1 | PEN 1.8/1.7 | PLANT 3.6/6.6 | BALL 5.7/6.6 | 5.2 (SHM245_Walk_Fwd) | 6.8 | 0 / 0 |
| v251a30_j41_rl_p10_eAY_r1 | PEN 3.6/1.7 | PLANT 4.3/7.5 | BALL 7.3/9.3 | 3.9 (A_CT_Jog_Fwd) | 28.3 | 2 / 28 |
| v251a30_j42_lr_p10_eAY_r1 | PEN 1.7/2.2 | PLANT 2.3/14.7 | BALL 10.6/15.3 | 6.7 (SHM_JogQ_A_LS_Jog_Right_Start) | 10.9 | 1 / 27 |
| v251a30_j45_sl2_eAY_r1 | PEN 1.6/2.2 | PLANT 2.1/6.0 | BALL 7.0/8.2 | 2.4 (A_CT_Jog_Fwd) | 9.9 | 2 / 29 |
| v251a30_jstart_eAY_r1 | PEN 3.1/2.3 | PLANT 8.6/7.7 | BALL 15.0/8.8 | 11.8 (HM_M_Neutral_Walk_Stop_F_Rfoot) | 34.8 | 0 / 0 |
| v251a30_taps_eAY_r1 | PEN 1.0/2.9 | PLANT 8.2/14.2 | BALL 13.1/19.7 | 13.5 (_Idle_NaturalBaseline_Phase275) | 17.3 | 0 / 0 |
| v251a30_w42_id_eAY_r1 | PEN 1.9/0.8 | PLANT 6.7/6.5 | BALL 11.0/7.3 | 7.2 (HM_M_Neutral_Walk_Stop_F_Rfoot) | 10.2 | 0 / 0 |
| v251a30_wstart_eAY_r1 | PEN 2.1/2.4 | PLANT 20.9/15.9 | BALL 21.0/16.7 | 14.6 (_Idle_NaturalBaseline_Phase275) | 21.0 | 0 / 0 |
| v251a60_gait_eAY_r1 | PEN 2.2/1.8 | PLANT 6.6/8.9 | BALL 7.8/9.2 | 8.0 (SHM245_Walk_Fwd) | 10.6 | 21 / 52 |
| v251a60_j40_rlw_eAY_r1 | PEN 2.4/2.2 | PLANT 2.4/4.2 | BALL 4.2/6.0 | 4.8 (SHM237_RePush_Bl_P08_T057) | 18.7 | 13 / 40 |
| v251a60_j41_rl_p10_eAY_r1 | PEN 1.8/2.5 | PLANT 4.2/5.7 | BALL 10.0/9.9 | 2.9 (SHM244_LatStop_L_Br_P00) | 9.3 | 16 / 37 |
| v251a60_j45_sl2_eAY_r1 | PEN 1.7/1.9 | PLANT 6.0/3.5 | BALL 6.9/6.6 | 2.9 (A_CT_Jog_Fwd) | 17.4 | 19 / 52 |
| v251a60_jstart_eAY_r1 | PEN 3.0/2.4 | PLANT 8.4/10.8 | BALL 8.4/11.0 | 10.8 (A_CT_Jog_FwdLeft) | 50.0 | 13 / 77 |
| v251a60_jstart_eA_r1 | PEN 3.0/2.4 | PLANT 8.4/10.8 | BALL 8.4/11.0 | 10.8 (A_CT_Jog_FwdLeft) | 50.0 | 12 / 77 |
| v251a60_jstart_eY_r1 | PEN 4.4/5.0 | PLANT 5.8/11.3 | BALL 7.6/11.3 | 19.9 (ogQ_af_Loco_Jog_Bwd_Start_AAMS) | 37.8 | 17 / 77 |
| v251a60_jstart_o_r1 | PEN 4.4/5.0 | PLANT 5.8/11.3 | BALL 7.6/11.3 | 19.9 (ogQ_af_Loco_Jog_Bwd_Start_AAMS) | 37.8 | 17 / 77 |
| v251a60_taps_eAY_r1 | PEN 1.0/2.6 | PLANT 18.3/13.6 | BALL 18.4/19.0 | 18.9 (SHM_StartTransfer_B_Rfoot) | 18.8 | 5 / 61 |
| v251a60_w43_idle_eAY_r1 | PEN 1.0/0.8 | PLANT 9.1/3.7 | BALL 9.1/4.2 | 8.2 (_Idle_NaturalBaseline_Phase275) | 5.5 | 4 / 39 |
| v251a60_wstart_eAY_r1 | PEN 1.8/2.5 | PLANT 12.3/14.5 | BALL 13.7/14.6 | 13.8 (A_LB_Walk_Right) | 23.5 | 5 / 36 |
| v251areal_j45_sl2_eAY_r1 | PEN 1.7/2.0 | PLANT 3.0/3.7 | BALL 8.0/5.6 | 2.7 (A_CT_Jog_Fwd) | 12.8 | 3 / 28 |
| v251areal_j45_sl2_eAY_r2 | PEN 1.7/1.8 | PLANT 4.8/3.9 | BALL 7.6/7.4 | 2.2 (A_CT_Jog_Fwd) | 13.3 | 3 / 27 |
| v251areal_j45_sl2_eAY_r3 | PEN 1.6/1.8 | PLANT 4.6/6.4 | BALL 6.8/7.9 | 2.8 (A_CT_Jog_Fwd) | 12.5 | 1 / 30 |
| v251areal_jstart_eAY_r1 | PEN 2.7/4.0 | PLANT 2.9/7.4 | BALL 7.3/9.9 | 1.4 (SHM_JogQ_A_LS_Jog_Left_Start) | 56.8 | 4 / 28 |
| v251areal_jstart_eAY_r2 | PEN 2.8/2.3 | PLANT 7.8/8.5 | BALL 7.8/10.5 | 2.9 (SHM_JogQ_A_LS_Jog_Right_Start) | 34.3 | 3 / 29 |
| v251areal_taps_eAY_r1 | PEN 1.0/2.1 | PLANT 8.2/12.8 | BALL 11.7/15.0 | 16.6 (_Idle_NaturalBaseline_Phase275) | 15.2 | 1 / 30 |
| v251b30_gait_eAYL_r1 | PEN 1.8/1.7 | PLANT 3.6/6.6 | BALL 5.7/6.6 | 5.2 (SHM245_Walk_Fwd) | 6.8 | 0 / 0 |
| v251b30_gait_oiL_r1 | PEN 2.1/3.0 | PLANT 3.0/9.5 | BALL 5.6/10.0 | 5.9 (A_CT_Jog_Fwd) | 14.7 | 4 / 30 |
| v251b30_j42_lr_p10_eAYL_r1 | PEN 1.9/2.2 | PLANT 2.3/14.7 | BALL 10.6/15.3 | 6.7 (SHM_JogQ_A_LS_Jog_Right_Start) | 10.9 | 1 / 27 |
| v251b30_j45_sl2_oiL_r1 | PEN 2.0/2.8 | PLANT 3.2/8.3 | BALL 5.8/9.9 | 2.0 (A_CT_Jog_Fwd) | 10.2 | 2 / 29 |
| v251b30_jstart_eAYL_r1 | PEN 3.1/2.3 | PLANT 8.6/7.7 | BALL 15.0/8.8 | 11.8 (HM_M_Neutral_Walk_Stop_F_Rfoot) | 34.8 | 0 / 0 |
| v251b30_jstart_oiL_r1 | PEN 3.5/2.9 | PLANT 6.3/12.1 | BALL 11.7/15.7 | 11.8 (HM_M_Neutral_Walk_Stop_F_Rfoot) | 37.4 | 1 / 26 |
| v251b30_taps_eAYL_r1 | PEN 1.0/2.9 | PLANT 8.2/14.2 | BALL 8.6/19.7 | 13.5 (_Idle_NaturalBaseline_Phase275) | 17.3 | 0 / 0 |
| v251b30_taps_oiL_r1 | PEN 1.5/1.4 | PLANT 10.7/12.6 | BALL 12.4/13.5 | 10.9 (SHM_StartTransfer_BL_Lfoot) | 11.9 | 1 / 26 |
| v251b30_w42_id_eAYL_r1 | PEN 1.9/0.8 | PLANT 6.7/6.5 | BALL 11.0/7.3 | 7.2 (HM_M_Neutral_Walk_Stop_F_Rfoot) | 10.2 | 0 / 0 |
| v251b30_w42_id_oiL_r1 | PEN 1.3/1.3 | PLANT 7.4/8.2 | BALL 8.0/8.2 | 12.5 (SHM244_Idle_Weighted) | 19.7 | 0 / 0 |
| v251b30_w43_idle_oiL_r1 | PEN 1.3/1.4 | PLANT 7.8/5.8 | BALL 8.3/5.9 | 3.8 (SHM244_Idle_Weighted) | 6.4 | 0 / 0 |
| v251b30_wstart_eAYL_r1 | PEN 2.1/2.4 | PLANT 20.9/15.9 | BALL 21.0/16.7 | 14.6 (_Idle_NaturalBaseline_Phase275) | 21.0 | 0 / 0 |
| v251b30_wstart_oiL_r1 | PEN 1.3/3.6 | PLANT 15.5/16.1 | BALL 17.2/18.1 | 24.0 (SHM_StartTransfer_LR_Rfoot) | 39.5 | 1 / 29 |
| v251b60_gait_eAYL_r1 | PEN 2.2/1.8 | PLANT 6.6/8.9 | BALL 7.8/9.2 | 8.0 (SHM245_Walk_Fwd) | 10.6 | 21 / 52 |
| v251b60_gait_oiL_r1 | PEN 2.0/2.7 | PLANT 2.0/10.6 | BALL 6.8/11.0 | 8.2 (A_CT_Jog_Fwd) | 14.0 | 23 / 70 |
| v251b60_j40_rlw_eAYL_r1 | PEN 2.4/2.2 | PLANT 2.4/4.2 | BALL 4.2/6.0 | 4.8 (SHM237_RePush_Bl_P08_T057) | 18.7 | 13 / 40 |
| v251b60_j45_sl2_eAYL_r1 | PEN 1.7/1.9 | PLANT 6.0/3.8 | BALL 7.0/6.7 | 2.9 (A_CT_Jog_Fwd) | 17.4 | 15 / 52 |
| v251b60_j45_sl2_oiL_r1 | PEN 2.1/2.6 | PLANT 3.7/7.0 | BALL 8.2/9.4 | 2.9 (SHM238_Cut_R_P21) | 12.0 | 18 / 52 |
| v251b60_jstart_eAYL_r1 | PEN 3.0/2.4 | PLANT 8.4/10.8 | BALL 9.8/11.0 | 10.8 (A_CT_Jog_FwdLeft) | 50.0 | 13 / 80 |
| v251b60_jstart_o_r1 | PEN 4.4/5.0 | PLANT 5.8/11.3 | BALL 7.6/11.3 | 19.9 (ogQ_af_Loco_Jog_Bwd_Start_AAMS) | 37.8 | 17 / 77 |
| v251b60_taps_eAYL_r1 | PEN 1.0/2.6 | PLANT 8.2/13.6 | BALL 13.2/19.0 | 18.4 (SHM_StartTransfer_BL_Lfoot) | 18.8 | 6 / 61 |
| v251b60_taps_oiL_r1 | PEN 1.6/1.1 | PLANT 12.8/5.5 | BALL 13.5/7.2 | 9.3 (SHM244_Idle_Weighted) | 6.5 | 6 / 37 |
| v251b60_w42_id_eAYL_r1 | PEN 1.9/0.8 | PLANT 5.9/8.0 | BALL 11.2/8.4 | 6.6 (_Idle_NaturalBaseline_Phase275) | 10.2 | 2 / 33 |
| v251b60_w42_id_oiL_r1 | PEN 1.3/1.3 | PLANT 10.3/9.1 | BALL 12.6/9.1 | 10.6 (SHM244_Idle_Weighted) | 20.2 | 2 / 32 |
| v251b60_w43_idle_eAYL_r1 | PEN 1.0/0.8 | PLANT 9.1/3.7 | BALL 9.1/4.2 | 8.2 (_Idle_NaturalBaseline_Phase275) | 5.5 | 4 / 39 |
| v251b60_w43_idle_oiL_r1 | PEN 1.3/1.2 | PLANT 6.1/8.4 | BALL 6.1/8.4 | 4.8 (SHM244_Idle_Weighted) | 5.6 | 2 / 26 |
| v251b60_wstart_eAYL_r1 | PEN 1.8/2.5 | PLANT 12.3/14.5 | BALL 13.7/14.6 | 13.8 (A_LB_Walk_Right) | 23.5 | 5 / 36 |
| v251b60_wstart_oiL_r1 | PEN 2.0/2.9 | PLANT 12.0/14.8 | BALL 13.2/14.9 | 14.1 (A_LB_Walk_Right) | 27.7 | 2 / 36 |
| v251breal_gait_oiL_r1 | PEN 2.0/2.8 | PLANT 8.7/8.1 | BALL 11.5/11.1 | 6.3 (A_CT_Jog_Fwd) | 13.1 | 5 / 46 |
| v251breal_j45_sl2_eAYL_r1 | PEN 1.1/2.2 | PLANT 2.2/5.4 | BALL 7.0/9.3 | 2.7 (A_CT_Jog_Fwd) | 9.3 | 3 / 32 |
| v251breal_j45_sl2_eAYL_r2 | PEN 1.9/1.8 | PLANT 3.5/2.8 | BALL 7.8/5.6 | 2.5 (A_CT_Jog_Fwd) | 16.1 | 2 / 29 |
| v251breal_jstart_eAYL_r1 | PEN 3.2/1.9 | PLANT 4.5/7.2 | BALL 6.0/8.8 | 26.9 (SHM_JogQ_A_LS_Jog_Left_Start) | 43.1 | 4 / 37 |
| v251breal_taps_oiL_r1 | PEN 1.4/1.9 | PLANT 10.7/11.3 | BALL 12.2/14.4 | 12.6 (SHM244_Idle_Weighted) | 14.0 | 1 / 27 |
| v251breal_w42_id_oiL_r1 | PEN 1.3/1.3 | PLANT 7.9/7.1 | BALL 9.7/7.1 | 10.7 (SHM244_Idle_Weighted) | 20.1 | 0 / 0 |
| v251breal_wstart_oiL_r1 | PEN 1.9/2.8 | PLANT 15.7/13.6 | BALL 17.5/14.2 | 23.9 (SHM_StartTransfer_LR_Rfoot) | 29.6 | 0 / 0 |
| v251c60_j45_sl2_eAYLX_r1 | PEN 1.8/1.9 | PLANT 4.7/3.7 | BALL 7.0/6.7 | 3.3 (A_CT_Jog_Fwd) | 17.4 | 17 / 51 |
| v251c60_jstart_eAYLX_r1 | PEN 3.0/2.4 | PLANT 8.4/10.8 | BALL 9.8/11.0 | 10.8 (A_CT_Jog_FwdLeft) | 50.0 | 13 / 80 |
| v251c60_jstart_eAYL_r1 | PEN 3.0/2.4 | PLANT 8.4/10.8 | BALL 9.8/11.0 | 10.8 (A_CT_Jog_FwdLeft) | 50.0 | 13 / 80 |
| v251e60_j45_sl2_eAY_r1 | PEN 1.7/1.9 | PLANT 6.0/3.5 | BALL 6.9/6.7 | 2.9 (A_CT_Jog_Fwd) | 17.4 | 17 / 52 |
| v251e60_jstart_eAY_r1 | PEN 3.0/2.4 | PLANT 8.2/10.8 | BALL 8.4/11.0 | 10.8 (A_CT_Jog_FwdLeft) | 50.0 | 14 / 74 |
| v251e60_jstart_o_r1 | PEN 4.4/5.0 | PLANT 5.4/11.3 | BALL 7.7/11.3 | 19.2 (ogQ_af_Loco_Jog_Bwd_Start_AAMS) | 37.8 | 19 / 73 |
