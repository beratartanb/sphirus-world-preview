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
