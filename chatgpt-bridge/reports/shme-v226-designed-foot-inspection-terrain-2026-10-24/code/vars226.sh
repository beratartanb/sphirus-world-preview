# vars226.sh: V2.26 variants. base = SAVED PRODUCTION (state_mode production: no flags). Candidates = production + explicit changes.
RV='"SHM224_DB_JRBwd":"/Game/GraceRanger/SHME/Animations/V225/PSD_SHM225_JogRevBwd","SHM224_DB_JRBwdM":"/Game/GraceRanger/SHME/Animations/V225/PSD_SHM225_JogRevBwd","SHM224_DB_JRFwd":"/Game/GraceRanger/SHME/Animations/V225/PSD_SHM225_JogRevFwd","SHM224_DB_JRFwdM":"/Game/GraceRanger/SHME/Animations/V225/PSD_SHM225_JogRevFwd"'
ON='"a.AnimNode.OrientationWarping.Enable 1","a.AnimNode.StrideWarping.Enable 1","a.AnimNode.FootPlacement.Enable 1","a.AnimNode.LegIK.Enable 1"'
MB=',"mbones":["ik_foot_l","ik_foot_r","ik_foot_root","thigh_l","thigh_r","calf_l","calf_r"]'
cand() { MODE[$1]=candidate; AF[$1]="\"abp_flags\":{$2}"; SX[$1]="{$3}"; CON[$1]="\"console\":[$ON${4:+,$4}]$MB"; }
cand rv   "$RV" ""                                                                                           # authored reversal clips (V2.25 candidate)
cand rvF  "$RV" "" '"a.AnimNode.FootPlacement.Enable 0"'                                                     # + FootPlacement off
cand rvL  "$RV" "" '"a.AnimNode.LegIK.Enable 0"'                                                             # + LegIK off
cand rvFL "$RV" "" '"a.AnimNode.FootPlacement.Enable 0","a.AnimNode.LegIK.Enable 0"'                          # + both off
cand rvRAW "$RV" "" '"a.AnimNode.FootPlacement.Enable 0","a.AnimNode.LegIK.Enable 0","a.AnimNode.StrideWarping.Enable 0","a.AnimNode.OrientationWarping.Enable 0"'   # raw MM output
cand oF   "" "" '"a.AnimNode.FootPlacement.Enable 0"'                                                        # production + FootPlacement off
cand oFL  "" "" '"a.AnimNode.FootPlacement.Enable 0","a.AnimNode.LegIK.Enable 0"'
cand oRAW "" "" '"a.AnimNode.FootPlacement.Enable 0","a.AnimNode.LegIK.Enable 0","a.AnimNode.StrideWarping.Enable 0","a.AnimNode.OrientationWarping.Enable 0"'
RV32='"SHM224_DB_JRBwd":"/Game/GraceRanger/SHME/Animations/V226/PSD_SHM226_JogRevBwd","SHM224_DB_JRBwdM":"/Game/GraceRanger/SHME/Animations/V226/PSD_SHM226_JogRevBwd","SHM224_DB_JRFwd":"/Game/GraceRanger/SHME/Animations/V226/PSD_SHM226_JogRevFwd","SHM224_DB_JRFwdM":"/Game/GraceRanger/SHME/Animations/V226/PSD_SHM226_JogRevFwd"'
cand rv32 "$RV32" ""                                        # 32-bin authored reversal clips (V2.26)
cand te   "" '"StepEdgeOn":true'                            # terrain: landing shift onto a step (T3b)
cand insA "" '"CamInspectEnabled":false'                    # camera A: normal follow (inspection off)
cand insC "" '"InspectZoomOn":true'                         # camera C: inspection + small closeness (production = B: no closeness)
cand rv32F  "$RV32" "" '"a.AnimNode.FootPlacement.Enable 0"'
cand rv32RAW "$RV32" "" '"a.AnimNode.FootPlacement.Enable 0","a.AnimNode.LegIK.Enable 0","a.AnimNode.StrideWarping.Enable 0","a.AnimNode.OrientationWarping.Enable 0"'
cand te6  "" '"StepEdgeOn":true,"SwingLiftMargin":6.0'       # T3g full-deficit lift + landing shift, margin 6
cand m6   "" '"SwingLiftMargin":6.0'                          # T3g full-deficit lift only, margin 6
cand r12 "" '"InspectRadius":12.0'                             # inspect: narrower gaze (two masks 29 cm apart separable with 12 cm probes)
cand te6x "" '"StepEdgeOn":true,"SwingLiftMargin":6.0,"StepEdgeMin":10.0'   # landing shift with a 10 cm edge threshold (no trigger on <= 18 deg slopes over the 30 cm probe span)
