## suite 1 (v12z_s1)
| stage | baseline | V1.1 | V1.2 | clips (V1.2) |
|---|---|---|---|---|
| yaw_reset | 7.2 | - | **3.5** | None |
| camera_fast_180_setup | 4.7 | - | **0.2** | R_M_Relaxed_Run_Stop_F_Rfoot |
| finish | 19.1 | - | **1.3** | R_M_Relaxed_Run_Stop_F_Rfoot |
suite max slide: baseline 19.1 / V1.1 - / V1.2 18.1; stages worse than the reference by >= 2 cm: 0

## suite 2 (v12f5_s2)
| stage | baseline | V1.1 | V1.2 | clips (V1.2) |
|---|---|---|---|---|
| idle_jump | 0.0 | 0.0 | **0.0** | None |
| idle_jump_air | 11.5 | 11.5 | **11.4** | None, A_LR_StandAir_Loop |
| walk_forward_jump | 0.0 | 0.0 | **0.0** | A_LB_Walk_Fwd |
| walk_forward_air | 51.3 | 12.5 | **12.4** | A_LB_Walk_Fwd, A_LR_StandAir_Loop |
| walk_stop | 11.1 | 11.0 | **1.1** | A_LB_Walk_Fwd, SHM_A_CP2_Jog_Fwd_Stop |
| sprint_select | 3.0 | 3.0 | **0.1** | dle_NaturalBaseline_Phase275 |
| finish | 19.3 | 19.3 | **0.2** | R_M_Relaxed_Run_Stop_F_Rfoot |
suite max slide: baseline 51.3 / V1.1 19.3 / V1.2 15.8; stages worse than the reference by >= 2 cm: 0

## suite 3 (v12z_s3)
| stage | baseline | V1.1 | V1.2 | clips (V1.2) |
|---|---|---|---|---|
| jog | 6.9 | 6.7 | **3.5** | M_Neutral_Walk_Start_F_Rfoot, M_Neutral_Walk_Start_F_Lfoot |
| camera_backward_settle | 27.0 | 27.0 | **33.1** | A_RB_Jog_Rear, _M_Neutral_Walk_Stop_B_Rfoot |
| short_stop_0 | 4.5 | 4.5 | **0.5** | A_CP2_Jog_Fwd_Start, SHM_A_CP2_Jog_Fwd_Stop |
| short_stop_1 | 5.1 | 5.1 | **0.6** | A_CP2_Jog_Fwd_Start, SHM_A_CP2_Jog_Fwd_Stop |
| short_stop_2 | 5.1 | 5.1 | **0.6** | A_CP2_Jog_Fwd_Start, SHM_A_CP2_Jog_Fwd_Stop |
| crouch_enter | 0.0 | 0.0 | **0.0** | SHM_A_CP2_Jog_Fwd_Stop, None |
| crouch_walk | 0.0 | 0.0 | **0.0** | None |
| crouch_stop | 0.0 | 0.0 | **0.0** | None |
| crouch_exit | 0.0 | 0.0 | **0.0** | None, dle_NaturalBaseline_Phase275 |
| standing_settle | 27.1 | 27.1 | **2.5** | dle_NaturalBaseline_Phase275 |
| wall_approach | 8.8 | 8.8 | **13.6** | dle_NaturalBaseline_Phase275, A_CP2_Jog_Fwd_Start |
| wall_retreat | 67.6 | 64.9 | **67.8** | dle_NaturalBaseline_Phase275, af_Loco_Jog_Bwd_Start_AAMS |
| master_off | 42.3 | 42.3 | **9.7** | A_RB_Jog_Rear, _M_Neutral_Walk_Stop_B_Lfoot |
suite max slide: baseline 67.6 / V1.1 64.9 / V1.2 67.8; stages worse than the reference by >= 2 cm: 3

## suite 5 (v12f5_s5)
| stage | baseline | V1.1 | V1.2 | clips (V1.2) |
|---|---|---|---|---|
| walk_stop | 9.5 | 6.8 | **1.0** | A_LB_Walk_Fwd, SHM_A_CP2_Jog_Fwd_Stop |
| walk_tap | 1.9 | 1.9 | **0.8** | dle_NaturalBaseline_Phase275, M_Neutral_Walk_Start_F_Rfoot |
| tap_stop | 7.8 | 7.9 | **1.2** | M_Neutral_Walk_Start_F_Rfoot, _M_Neutral_Walk_Stop_F_Rfoot |
| sprint_90_l_approach | 1.8 | 1.8 | **2.2** | _M_Neutral_Walk_Stop_F_Rfoot, _M_Relaxed_Run_Start_F_Lfoot |
| sprint_90_l_await | 0.0 | 0.0 | **0.0** | A_LB_Sprint_Fwd |
| sprint_90_l | 4.7 | 4.7 | **4.7** | A_LB_Sprint_Fwd, tral_Sprint_Turn_R_090_Rfoot |
| sprint_90_l_stop | 7.7 | 7.1 | **7.7** | A_CT_Jog_Right, A_LS_Jog_Right_Stop |
| sprint_90_r_approach | 2.1 | 2.1 | **2.1** | A_LS_Jog_Right_Stop, _M_Relaxed_Run_Start_F_Lfoot |
| sprint_90_r_await | 0.0 | 0.0 | **0.0** | A_LB_Sprint_Fwd |
| sprint_90_r | 6.2 | 6.2 | **6.2** | A_LB_Sprint_Fwd, tral_Sprint_Turn_R_090_Lfoot |
| sprint_90_r_stop | 7.2 | 6.2 | **7.2** | A_CT_Jog_Right, A_LS_Jog_Right_Stop |
| sprint_180_l_approach | 2.2 | 2.2 | **2.2** | A_LS_Jog_Right_Stop, _M_Relaxed_Run_Start_F_Lfoot |
| sprint_180_l_await | 0.0 | 0.0 | **0.0** | A_LB_Sprint_Fwd |
| sprint_180_l | 1.9 | 1.9 | **1.9** | A_LB_Sprint_Fwd, A_LR_Run_Pivot_F_B_Rfoot |
| sprint_180_l_back_to_forward | 5.3 | 5.3 | **5.3** | A_RB_Run_Rear, A_LR_Run_Pivot_B_F_Lfoot |
| sprint_180_l_stop | 6.3 | 6.3 | **6.3** | A_LB_Sprint_Fwd, R_M_Relaxed_Run_Stop_F_Lfoot |
| sprint_180_r_approach | 1.0 | 2.4 | **1.0** | R_M_Relaxed_Run_Stop_F_Lfoot, _M_Relaxed_Run_Start_F_Lfoot |
| sprint_180_r_await | 0.0 | 0.0 | **0.0** | A_LB_Sprint_Fwd |
| sprint_180_r | 3.0 | 3.0 | **3.0** | A_LB_Sprint_Fwd, A_LR_Run_Pivot_F_B_Rfoot |
| sprint_180_r_back_to_forward | 4.3 | 4.3 | **4.3** | A_RB_Run_Rear, A_LR_Run_Pivot_B_F_Rfoot |
| sprint_180_r_stop | 4.3 | 4.3 | **4.3** | A_LB_Sprint_Fwd, R_M_Relaxed_Run_Stop_F_Rfoot |
suite max slide: baseline 9.5 / V1.1 7.9 / V1.2 7.7; stages worse than the reference by >= 2 cm: 0

## suite 6 (v12f5_s6)
| stage | baseline | V1.1 | V1.2 | clips (V1.2) |
|---|---|---|---|---|
| walk_stairs_up_setup | 2.2 | 2.1 | **2.2** | None |
| walk_stairs_up | 7.0 | 6.8 | **6.8** | None, A_LB_Walk_Fwd |
| walk_stairs_up_settle | 0.7 | 0.9 | **0.5** | A_LB_Walk_Fwd, SHM_A_CP2_Jog_Fwd_Stop |
| walk_stairs_down_setup | 5.9 | 7.0 | **0.0** | dle_NaturalBaseline_Phase275 |
| walk_stairs_down | 8.0 | 8.0 | **7.6** | dle_NaturalBaseline_Phase275, M_Neutral_Walk_Start_F_Rfoot |
| walk_stairs_down_settle | 6.0 | 6.0 | **1.5** | A_LB_Walk_Fwd, SHM_A_CP2_Jog_Fwd_Stop |
| jog_stairs_up_setup | 1.8 | 1.8 | **0.1** | dle_NaturalBaseline_Phase275 |
| jog_stairs_up | 9.5 | 9.5 | **9.5** | dle_NaturalBaseline_Phase275, A_CP2_Jog_Fwd_Start |
| jog_stairs_up_settle | 1.7 | 3.9 | **1.7** | A_CT_Jog_Fwd, SHM_A_CP2_Jog_Fwd_Stop |
| jog_stairs_down_setup | 6.1 | 4.3 | **0.1** | SHM_A_CP2_Jog_Fwd_Stop, dle_NaturalBaseline_Phase275 |
| jog_stairs_down | 9.6 | 9.6 | **11.0** | dle_NaturalBaseline_Phase275, A_CP2_Jog_Fwd_Start |
| jog_stairs_down_settle | 1.7 | 3.9 | **5.3** | A_CT_Jog_Fwd, SHM_A_CP2_Jog_Fwd_Stop |
suite max slide: baseline 9.6 / V1.1 9.6 / V1.2 11.0; stages worse than the reference by >= 2 cm: 0

## suite 7 (v12f5_s7)
| stage | baseline | V1.1 | V1.2 | clips (V1.2) |
|---|---|---|---|---|
| walk_wall_0 | 31.9 | 31.9 | **8.0** | None, A_LB_Walk_Fwd |
| walk_wall_0_release | 2.0 | 2.1 | **0.0** | dle_NaturalBaseline_Phase275 |
| walk_wall_45_release | 25.1 | 23.1 | **0.3** | A_LB_Walk_Fwd, M_Neutral_Walk_Stop_FR_Lfoot |
| walk_wall_75_release | 10.3 | 10.3 | **1.5** | A_LB_Walk_Fwd, SHM_A_CP2_Jog_Fwd_Stop |
| jog_wall_0 | 21.1 | 21.1 | **10.8** | dle_NaturalBaseline_Phase275, A_CP2_Jog_Fwd_Start |
| jog_wall_45_setup | 2.0 | 2.0 | **0.0** | dle_NaturalBaseline_Phase275 |
| jog_wall_45 | 9.4 | 9.4 | **11.8** | dle_NaturalBaseline_Phase275, A_CP2_Jog_Fwd_Start |
| jog_wall_45_release | 35.0 | 35.0 | **24.7** | A_CT_Jog_Fwd, M_Neutral_Walk_Stop_FR_Rfoot |
| jog_wall_75_setup | 4.1 | 4.1 | **1.2** | M_Neutral_Walk_Stop_FR_Rfoot |
| jog_wall_75 | 8.6 | 8.6 | **10.9** | M_Neutral_Walk_Stop_FR_Rfoot, A_CP2_Jog_Fwd_Start |
| sprint_wall_0_setup | 2.7 | 2.7 | **0.1** | dle_NaturalBaseline_Phase275 |
| sprint_wall_45_release | 12.9 | 12.9 | **38.9** | A_C01R_Sprint_WalkToSprint_L, dle_NaturalBaseline_Phase275 |
| sprint_wall_75 | 2.1 | 2.1 | **13.4** | dle_NaturalBaseline_Phase275, _M_Relaxed_Run_Start_F_Lfoot |
| sprint_low_speed_setup | 5.8 | 6.4 | **1.0** | R_M_Relaxed_Run_Stop_F_Lfoot |
| sprint_low_speed | 8.8 | 8.9 | **1.9** | R_M_Relaxed_Run_Stop_F_Lfoot, _M_Relaxed_Run_Start_F_Lfoot |
suite max slide: baseline 38.7 / V1.1 35.0 / V1.2 38.9; stages worse than the reference by >= 2 cm: 4

## suite 8 (v12z_s8)
| stage | baseline | V1.1 | V1.2 | clips (V1.2) |
|---|---|---|---|---|
| corridor_setup | 2.2 | 2.2 | **2.2** | None |
| corridor_entry | 8.0 | 8.0 | **8.0** | None, A_LB_Walk_Fwd |
| indoor_surface_yaw_45 | 8.0 | 8.3 | **2.0** | SHM_A_CP2_Jog_Fwd_Stop, dle_NaturalBaseline_Phase275 |
| indoor_surface_yaw_135 | 7.8 | 7.8 | **5.4** | dle_NaturalBaseline_Phase275 |
| indoor_surface_yaw_225 | 32.4 | 32.4 | **36.7** | dle_NaturalBaseline_Phase275 |
| corner_setup | 9.1 | 9.1 | **3.5** | dle_NaturalBaseline_Phase275 |
| corner_sweep_90 | 8.0 | 8.0 | **2.3** | dle_NaturalBaseline_Phase275 |
| corridor_exit_setup | 6.8 | 6.8 | **4.7** | dle_NaturalBaseline_Phase275 |
| corridor_exit | 29.2 | 27.8 | **7.8** | dle_NaturalBaseline_Phase275, _Neutral_Walk_Start_FL_Rfoot |
suite max slide: baseline 36.1 / V1.1 36.1 / V1.2 36.7; stages worse than the reference by >= 2 cm: 1

## suite 10 (v12f5_s10)
| stage | baseline | V1.1 | V1.2 | clips (V1.2) |
|---|---|---|---|---|
| start_l_0_tap_setup | 8.0 | 8.0 | **8.0** | None, A_LB_Walk_Fwd |
| start_l_0_tap | 0.5 | 0.5 | **0.5** | SHM_A_CP2_Jog_Fwd_Stop, M_Neutral_Walk_Start_F_Rfoot |
| start_l_0_tap_stop | 15.1 | 19.6 | **6.4** | M_Neutral_Walk_Start_F_Rfoot, _M_Neutral_Walk_Stop_F_Lfoot |
| start_l_0_sustained_stop | 9.9 | 11.1 | **1.2** | A_LB_Walk_Fwd, SHM_A_CP2_Jog_Fwd_Stop |
| start_l_-45_tap_setup | 7.4 | 7.4 | **7.7** | dle_NaturalBaseline_Phase275, M_Neutral_Walk_Start_F_Rfoot |
| start_l_-45_tap | 0.7 | 0.7 | **0.7** | SHM_A_CP2_Jog_Fwd_Stop, _Neutral_Walk_Start_FL_Rfoot |
| start_l_-45_tap_stop | 15.3 | 17.4 | **0.6** | _Neutral_Walk_Start_FL_Rfoot, M_Neutral_Walk_Stop_FL_Lfoot |
| start_l_-45_sustained_stop | 29.1 | 29.1 | **1.1** | A_LB_Walk_FwdLeft, M_Neutral_Walk_Stop_FL_Lfoot |
| start_l_45_tap_setup | 7.4 | 7.4 | **7.4** | M_Neutral_Walk_Stop_FL_Lfoot, M_Neutral_Walk_Start_F_Rfoot |
| start_l_45_tap | 0.6 | 0.6 | **0.6** | SHM_A_CP2_Jog_Fwd_Stop, _Neutral_Walk_Start_FR_Rfoot |
| start_l_45_tap_stop | 13.3 | 18.3 | **0.4** | _Neutral_Walk_Start_FR_Rfoot, M_Neutral_Walk_Stop_FR_Rfoot |
| start_l_45_sustained_stop | 21.6 | 19.9 | **7.6** | A_LB_Walk_FwdRight, M_Neutral_Walk_Stop_FR_Lfoot |
| start_r_0_tap_setup | 5.0 | 5.0 | **5.5** | M_Neutral_Walk_Stop_FR_Lfoot, M_Neutral_Walk_Start_F_Rfoot |
| start_r_0_tap | 0.7 | 1.1 | **0.7** | SHM_A_CP2_Jog_Fwd_Stop, M_Neutral_Walk_Start_F_Rfoot |
| start_r_0_tap_stop | 10.0 | 10.1 | **1.9** | M_Neutral_Walk_Start_F_Rfoot, _M_Neutral_Walk_Stop_F_Rfoot |
| start_r_-45_tap_setup | 5.0 | 5.0 | **7.7** | dle_NaturalBaseline_Phase275, M_Neutral_Walk_Start_F_Rfoot |
| start_r_-45_tap | 0.2 | 0.2 | **0.2** | SHM_A_CP2_Jog_Fwd_Stop, _Neutral_Walk_Start_FL_Rfoot |
| start_r_-45_tap_stop | 14.6 | 15.8 | **1.6** | _Neutral_Walk_Start_FL_Rfoot, M_Neutral_Walk_Stop_FL_Lfoot |
| start_r_-45_sustained_setup | 5.0 | 5.0 | **7.6** | M_Neutral_Walk_Stop_FL_Lfoot, M_Neutral_Walk_Start_F_Rfoot |
| start_r_-45_sustained_stop | 26.0 | 27.9 | **1.0** | A_LB_Walk_FwdLeft, M_Neutral_Walk_Stop_FL_Lfoot |
| start_r_45_tap_setup | 6.4 | 6.7 | **6.7** | M_Neutral_Walk_Stop_FL_Lfoot, M_Neutral_Walk_Start_F_Rfoot |
| start_r_45_tap | 0.5 | 0.5 | **0.5** | SHM_A_CP2_Jog_Fwd_Stop, _Neutral_Walk_Start_FR_Rfoot |
| start_r_45_tap_stop | 6.1 | 4.3 | **4.3** | _Neutral_Walk_Start_FR_Rfoot, M_Neutral_Walk_Stop_FR_Rfoot |
| start_r_45_sustained_stop | 22.6 | 20.3 | **6.7** | A_LB_Walk_FwdRight, M_Neutral_Walk_Stop_FR_Lfoot |
suite max slide: baseline 29.1 / V1.1 29.1 / V1.2 8.0; stages worse than the reference by >= 2 cm: 2

## suite 10 @10fps (v12z_s10lo)
| stage | baseline | V1.1 | V1.2 | clips (V1.2) |
|---|---|---|---|---|
| start_l_0_tap_setup | 23.3 | 23.3 | **23.4** | None, A_LB_Walk_Fwd |
| start_l_0_tap | 0.2 | 0.2 | **0.0** | _M_Neutral_Walk_Stop_F_Rfoot, M_Neutral_Walk_Start_F_Rfoot |
| start_l_0_tap_stop | 18.3 | 18.5 | **6.2** | M_Neutral_Walk_Start_F_Rfoot, _M_Neutral_Walk_Stop_F_Lfoot |
| start_l_0_sustained_setup | 22.4 | 22.4 | **8.6** | _M_Neutral_Walk_Stop_F_Lfoot, M_Neutral_Walk_Start_F_Lfoot |
| start_l_-45_tap_setup | 22.4 | 22.2 | **23.4** | dle_NaturalBaseline_Phase275, M_Neutral_Walk_Start_F_Rfoot |
| start_l_-45_tap | 0.0 | 0.0 | **0.0** | _M_Neutral_Walk_Stop_F_Rfoot, _Neutral_Walk_Start_FL_Rfoot |
| start_l_-45_tap_stop | 12.9 | 13.0 | **0.6** | _Neutral_Walk_Start_FL_Rfoot, M_Neutral_Walk_Stop_FL_Lfoot |
| start_l_-45_sustained_setup | 22.4 | 5.3 | **22.4** | M_Neutral_Walk_Stop_FL_Lfoot, M_Neutral_Walk_Start_F_Rfoot |
| start_l_-45_sustained_stop | 31.6 | 28.9 | **1.4** | A_LB_Walk_FwdLeft, M_Neutral_Walk_Stop_FL_Lfoot |
| start_l_45_tap_setup | 5.3 | 22.2 | **22.4** | M_Neutral_Walk_Stop_FL_Lfoot, M_Neutral_Walk_Start_F_Rfoot |
| start_l_45_tap | 0.1 | 0.0 | **0.1** | _M_Neutral_Walk_Stop_F_Rfoot, _Neutral_Walk_Start_FR_Rfoot |
| start_l_45_tap_stop | 11.7 | 15.5 | **0.2** | _Neutral_Walk_Start_FR_Rfoot, M_Neutral_Walk_Stop_FR_Lfoot |
| start_l_45_sustained_stop | 22.9 | 19.7 | **4.7** | A_LB_Walk_FwdRight, M_Neutral_Walk_Stop_FR_Lfoot |
| start_r_0_tap_setup | 5.3 | 5.3 | **8.1** | M_Neutral_Walk_Stop_FR_Lfoot, M_Neutral_Walk_Start_F_Rfoot |
| start_r_0_tap | 0.0 | 0.3 | **0.3** | _M_Neutral_Walk_Stop_F_Rfoot, M_Neutral_Walk_Start_F_Rfoot |
| start_r_0_tap_stop | 9.5 | 9.1 | **2.9** | M_Neutral_Walk_Start_F_Rfoot, _M_Neutral_Walk_Stop_F_Rfoot |
| start_r_0_sustained_setup | 21.4 | 21.4 | **5.3** | _M_Neutral_Walk_Stop_F_Rfoot, M_Neutral_Walk_Start_F_Rfoot |
| start_r_0_sustained_stop | 21.2 | 21.2 | **9.6** | A_LB_Walk_Fwd, _M_Neutral_Walk_Stop_F_Rfoot |
| start_r_-45_tap_setup | 5.3 | 5.3 | **5.3** | dle_NaturalBaseline_Phase275, M_Neutral_Walk_Start_F_Rfoot |
| start_r_-45_tap | 0.0 | 0.0 | **0.0** | _M_Neutral_Walk_Stop_F_Rfoot, _Neutral_Walk_Start_FL_Rfoot |
| start_r_-45_tap_stop | 12.6 | 12.4 | **0.6** | _Neutral_Walk_Start_FL_Rfoot, M_Neutral_Walk_Stop_FL_Lfoot |
| start_r_-45_sustained_stop | 30.5 | 30.6 | **1.4** | A_LB_Walk_FwdLeft, M_Neutral_Walk_Stop_FL_Lfoot |
| start_r_45_tap_setup | 5.3 | 5.3 | **12.3** | M_Neutral_Walk_Stop_FL_Lfoot, M_Neutral_Walk_Start_F_Rfoot |
| start_r_45_tap | 0.0 | 0.0 | **0.0** | _M_Neutral_Walk_Stop_F_Rfoot, _Neutral_Walk_Start_FR_Rfoot |
| start_r_45_tap_stop | 18.5 | 18.5 | **0.2** | _Neutral_Walk_Start_FR_Rfoot, M_Neutral_Walk_Stop_FR_Lfoot |
| start_r_45_sustained_stop | 23.1 | 22.8 | **4.7** | A_LB_Walk_FwdRight, M_Neutral_Walk_Stop_FR_Lfoot |
suite max slide: baseline 31.6 / V1.1 30.6 / V1.2 23.4; stages worse than the reference by >= 2 cm: 3

## suite 10 @60fps (v12z_s10hi)
| stage | baseline | V1.1 | V1.2 | clips (V1.2) |
|---|---|---|---|---|
| start_l_0_tap_setup | - | - | **6.2** | None, A_LB_Walk_Fwd |
| start_l_0_tap | - | - | **0.6** | SHM_A_CP2_Jog_Fwd_Stop, M_Neutral_Walk_Start_F_Rfoot |
| start_l_0_tap_stop | - | - | **0.1** | M_Neutral_Walk_Start_F_Rfoot, _M_Neutral_Walk_Stop_F_Lfoot |
| start_l_-45_tap_setup | - | - | **8.0** | dle_NaturalBaseline_Phase275, M_Neutral_Walk_Start_F_Rfoot |
| start_l_-45_tap | - | - | **0.7** | SHM_A_CP2_Jog_Fwd_Stop, _Neutral_Walk_Start_FL_Rfoot |
| start_l_-45_tap_stop | - | - | **3.3** | _Neutral_Walk_Start_FL_Rfoot, M_Neutral_Walk_Stop_FL_Lfoot |
| start_l_45_tap_setup | - | - | **6.9** | M_Neutral_Walk_Stop_FL_Lfoot, M_Neutral_Walk_Start_F_Rfoot |
| start_l_45_tap | - | - | **0.7** | SHM_A_CP2_Jog_Fwd_Stop, _Neutral_Walk_Start_FR_Rfoot |
| start_l_45_tap_stop | - | - | **2.1** | _Neutral_Walk_Start_FR_Rfoot, M_Neutral_Walk_Stop_FR_Rfoot |
| start_r_0_tap_setup | - | - | **6.8** | M_Neutral_Walk_Stop_FR_Lfoot, M_Neutral_Walk_Start_F_Rfoot |
| start_r_0_tap | - | - | **0.7** | SHM_A_CP2_Jog_Fwd_Stop, M_Neutral_Walk_Start_F_Rfoot |
| start_r_0_tap_stop | - | - | **0.9** | M_Neutral_Walk_Start_F_Rfoot, _M_Neutral_Walk_Stop_F_Rfoot |
| start_r_-45_tap_setup | - | - | **7.7** | dle_NaturalBaseline_Phase275, M_Neutral_Walk_Start_F_Rfoot |
| start_r_-45_tap | - | - | **0.3** | SHM_A_CP2_Jog_Fwd_Stop, _Neutral_Walk_Start_FL_Rfoot |
| start_r_-45_tap_stop | - | - | **6.5** | _Neutral_Walk_Start_FL_Rfoot, M_Neutral_Walk_Stop_FL_Lfoot |
| start_r_45_tap_setup | - | - | **7.5** | M_Neutral_Walk_Stop_FL_Lfoot, M_Neutral_Walk_Start_F_Rfoot |
| start_r_45_tap | - | - | **0.5** | SHM_A_CP2_Jog_Fwd_Stop, _Neutral_Walk_Start_FR_Rfoot |
| start_r_45_tap_stop | - | - | **0.5** | _Neutral_Walk_Start_FR_Rfoot, M_Neutral_Walk_Stop_FR_Rfoot |
suite max slide: baseline - / V1.1 - / V1.2 8.4; stages worse than the reference by >= 2 cm: 0

## suite 10 SHME off (v12z_s10off)
| stage | baseline | V1.1 | V1.2 | clips (V1.2) |
|---|---|---|---|---|
| start_l_0_tap_setup | 8.0 | - | **8.0** | None, A_LB_Walk_Fwd |
| start_l_0_tap | 0.5 | - | **0.5** | SHM_A_CP2_Jog_Fwd_Stop, M_Neutral_Walk_Start_F_Rfoot |
| start_l_0_tap_stop | 15.1 | - | **24.4** | M_Neutral_Walk_Start_F_Rfoot, _M_Neutral_Walk_Stop_F_Lfoot |
| start_l_-45_tap_setup | 7.4 | - | **7.4** | dle_NaturalBaseline_Phase275, M_Neutral_Walk_Start_F_Rfoot |
| start_l_-45_tap | 0.7 | - | **0.7** | SHM_A_CP2_Jog_Fwd_Stop, _Neutral_Walk_Start_FL_Rfoot |
| start_l_-45_tap_stop | 15.3 | - | **15.3** | _Neutral_Walk_Start_FL_Rfoot, M_Neutral_Walk_Stop_FL_Lfoot |
| start_l_45_tap_setup | 7.4 | - | **7.4** | M_Neutral_Walk_Stop_FL_Lfoot, M_Neutral_Walk_Start_F_Rfoot |
| start_l_45_tap | 0.6 | - | **0.6** | SHM_A_CP2_Jog_Fwd_Stop, _Neutral_Walk_Start_FR_Rfoot |
| start_l_45_tap_stop | 13.3 | - | **13.3** | _Neutral_Walk_Start_FR_Rfoot, M_Neutral_Walk_Stop_FR_Rfoot |
| start_r_0_tap_setup | 5.0 | - | **5.0** | M_Neutral_Walk_Stop_FR_Lfoot, M_Neutral_Walk_Start_F_Rfoot |
| start_r_0_tap | 0.7 | - | **0.7** | SHM_A_CP2_Jog_Fwd_Stop, M_Neutral_Walk_Start_F_Rfoot |
| start_r_0_tap_stop | 10.0 | - | **12.4** | M_Neutral_Walk_Start_F_Rfoot, _M_Neutral_Walk_Stop_F_Rfoot |
| start_r_-45_tap_setup | 5.0 | - | **5.0** | dle_NaturalBaseline_Phase275, M_Neutral_Walk_Start_F_Rfoot |
| start_r_-45_tap | 0.2 | - | **0.2** | SHM_A_CP2_Jog_Fwd_Stop, _Neutral_Walk_Start_FL_Rfoot |
| start_r_-45_tap_stop | 14.6 | - | **14.6** | _Neutral_Walk_Start_FL_Rfoot, M_Neutral_Walk_Stop_FL_Lfoot |
| start_r_45_tap_setup | 6.4 | - | **4.9** | M_Neutral_Walk_Stop_FL_Lfoot, M_Neutral_Walk_Start_F_Rfoot |
| start_r_45_tap | 0.5 | - | **0.5** | SHM_A_CP2_Jog_Fwd_Stop, _Neutral_Walk_Start_FR_Rfoot |
| start_r_45_tap_stop | 6.1 | - | **6.2** | _Neutral_Walk_Start_FR_Rfoot, M_Neutral_Walk_Stop_FR_Rfoot |
suite max slide: baseline 29.1 / V1.1 - / V1.2 29.1; stages worse than the reference by >= 2 cm: 2

## suite 2 SHME off (v12z_s2off)
| stage | baseline | V1.1 | V1.2 | clips (V1.2) |
|---|---|---|---|---|
| idle_jump | 0.0 | - | **0.0** | None |
| idle_jump_air | 11.5 | - | **11.5** | None, A_LR_StandAir_Loop |
| walk_forward_jump | 0.0 | - | **0.0** | A_LB_Walk_Fwd |
| walk_forward_air | 51.3 | - | **8.2** | A_LB_Walk_Fwd, A_LR_StandAir_Loop |
| finish | 19.3 | - | **21.9** | R_M_Relaxed_Run_Stop_F_Rfoot |
suite max slide: baseline 51.3 / V1.1 - / V1.2 21.9; stages worse than the reference by >= 2 cm: 1
