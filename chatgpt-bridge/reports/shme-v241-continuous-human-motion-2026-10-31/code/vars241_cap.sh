CAPV4='o tkh tkha tkk tkp aoh'
# vars232.sh: V2.32 variants = vars231 (all earlier candidate definitions; o = the SAVED PRODUCTION = V2.31) + the V2.32 section at the end
# vars229f.sh: V2.29 final variants. o = SAVED PRODUCTION. Before the switch: bn = new body (effort ef2 + resume) + reference camera,
# cn = reference body + new camera, fin = new body + new camera. After the switch: efoff = production with the effort off (same entries).
ON='"a.AnimNode.OrientationWarping.Enable 1","a.AnimNode.StrideWarping.Enable 1","a.AnimNode.FootPlacement.Enable 1","a.AnimNode.LegIK.Enable 1"'
cand() { MODE[$1]=candidate; AF[$1]=""; [ -n "$2" ] && AF[$1]="\"abp_flags\":{$2}"; SX[$1]="{$3}"; CON[$1]="\"console\":[$ON"; [ -n "$4" ] && CON[$1]="${CON[$1]},$4"; CON[$1]="${CON[$1]}]"; PF[$1]="$5"; BF[$1]="$6"; }
EF2='"EffortEnabled":true,"EffortGain":1.6,"EffortTurnK":0.5,"EffortAccK":0.5,"EffortLoadK":0.6,"EffortTauRec":5.0'
CW='"CamSwapMinSpeed":230.0,"CamFolDZLatWalk":3.0,"CamFolDZFwdWalk":4.0'
cand bn  '"SHM229_ResumeWin":0.2' "$EF2"
cand cn  ""                       "$CW"
cand fin '"SHM229_ResumeWin":0.2' "$EF2,$CW"
cand efoff "" '"EffortEnabled":false'
# V2.29 push-phase cancel (sprint S->W control lock fix), on top of the saved production
cand pc '"SHM229_PushCancel":1.0' ""
# V2.29 effort x reversal-route gap: with effort the back-run is slower (80-135 cm/s) at the next W -> below RedirectEpisodeMinSpeed 120 ->
# vendor stand-sprint-pivot tail + WalkToSprint (head pop 88-110). ems = pc + episode minimum speed 70.
cand ems '"SHM229_PushCancel":1.0' '"RedirectEpisodeMinSpeed":70.0'
cand pcoff '"SHM229_PushCancel":1.0' '"EffortEnabled":false'
cand ems40 '"SHM229_PushCancel":1.0' '"RedirectEpisodeMinSpeed":40.0'
# V2.29 effort floor: with scales down to 0.55 the capsule lags the authored reversal clips -> clip ends early -> vendor sprint-pivot tail
cand sm70 "" '"EffortScaleMin":0.7'
cand sm80 "" '"EffortScaleMin":0.8'
# V2.29 reference state for captures (V2.28 behaviour + the RevTurn content fix, which flags cannot undo)
cand ref '"SHM229_PushCancel":0.0,"SHM229_ResumeWin":0.0' '"EffortEnabled":false,"CamSwapMinSpeed":60.0,"CamFolDZLatWalk":12.0,"CamFolDZFwdWalk":10.0'
# V2.30 sway isolation (one layer off at a time, on top of production)
cand oPBI "" "" "" '"ProfileEnabled":false'
cand oSCR "" "" "" '"SpineCounterRotation":0.0'
cand oCLD "" '"CurveLeanDirectEnabled":false'
cand oOW  "" "" '"a.AnimNode.OrientationWarping.Enable 0"'
cand oRAW "" "" '"a.AnimNode.FootPlacement.Enable 0","a.AnimNode.LegIK.Enable 0","a.AnimNode.StrideWarping.Enable 0","a.AnimNode.OrientationWarping.Enable 0"'
cand oSET "" '"SettleBodyEnabled":false,"TerrainBodyEnabled":false'
# V2.30 low-speed reversal class (after build A): lr = production + RedirectLowRevSpeed 30
cand lr "" '"RedirectLowRevSpeed":30.0'
# V2.30 recovery family gate while an authored clip is held
cand fg '"SHM230_FamGate":1.0' ""
cand lrfg '"SHM230_FamGate":1.0' '"RedirectLowRevSpeed":30.0'
# V2.30 low-speed reversal entry: class (lr) + frame-0 EarlyRev lower bound for a recently running body
cand lr2 '"SHM230_EarlyRevMin":30.0' '"RedirectLowRevSpeed":30.0'
cand er  '"SHM230_EarlyRevMin":30.0' ""
# V2.30 effort -> body: loaded reversal family when the short-term effort is high (on top of lr2)
cand lrL '"SHM230_EarlyRevMin":30.0,"SHM230_LoadedOn":1.0' '"RedirectLowRevSpeed":30.0'
# V2.30 terrain: planned step preparation (V2.25 T2) for the 28 cm rise / drop chain
cand sp1 '"SHM230_EarlyRevMin":30.0' '"RedirectLowRevSpeed":30.0,"StepPrepEnabled":true,"StepPrepMax":32.0'
cand sp2 '"SHM230_EarlyRevMin":30.0' '"RedirectLowRevSpeed":30.0,"StepPrepEnabled":true,"StepPrepMax":32.0,"StepPrepGain":0.5'
# V2.30 capture reference after the switch: production with the low-speed reversal route OFF (V2.29 routing on the V2.30 re-authored content)
cand nolr '"SHM230_EarlyRevMin":0.0' '"RedirectLowRevSpeed":0.0'
# V2.30 (after the switch) idle-entry guard inside the held reversal (release -> re-press) and the low-speed route floor 70 cm/s
cand ig '"SHM230_IdleGuard":1.0' ''
cand lr70 '"SHM230_EarlyRevMin":70.0' '"RedirectLowRevSpeed":70.0'
cand lr70ig '"SHM230_EarlyRevMin":70.0,"SHM230_IdleGuard":1.0' '"RedirectLowRevSpeed":70.0'
# V2.23 variants (eval'd after mk). base = FINAL V2.22 production (v223_ab.sh).
AF[o]="${AF[base]}"; SX[o]="${SX[base]}"
# V2.26 FULL-FRAME capture variants (floating PIE window 1728x972, 16:9, no crop). V2.24 capture variants: variants named in CAPV get S / D / G camera suffixes; game camera FULL frame (no crop)
# (SHME V2.21 flags off, recovery hold off). Cameras S side / D front-right diagonal (input frame from the control yaw) / G gameplay camera.
# Real-time mcap 30 fps, neutral fill lights, PIE-only clay test look on the visible body (same as V2.12-V2.20). No frame is cut or edited.
CAP="\"mcap\":{\"start\":${CAP_START:-3.8},\"seconds\":${CAP_SECS:-7.0},\"fps\":30,\"quality\":88}"
SIDE="\"track_cam\":{\"side\":${SIDE_D:-520},\"back\":0,\"up\":${CUP:-90},\"look_z\":${CLZ:-90},\"fov\":${FOV:-58},\"world_yaw\":${WYAW:-0},\"lag\":0.15}"
DIAG="\"track_cam\":{\"side\":${DIAG_S:-380},\"back\":${DIAG_B:--420},\"up\":${CUP:-90},\"look_z\":${CLZ:-90},\"fov\":${FOV:-58},\"world_yaw\":${WYAW:-0},\"lag\":0.15}"
LIGHT="\"fill_lights\":[[0,330,170,${LI:-8000},1600],[300,-200,160,${LI2:-4000},1400],[-250,0,200,${LI2:-4000},1400]]"
LOOK="\"test_look\":{\"components\":[\"Manny\"]}"
for c in S D G; do
  case $c in S) CAM=",$SIDE";; D) CAM=",$DIAG";; G) CAM="";; esac
  for v in ${CAPV:-o}; do [ -z "${MODE[$v]}" ] && continue
    bf="${BF[$v]}"; [ $c != G ] && bf="${bf/\"GR215_CamYawFromControl\":false/\"GR215_CamYawFromControl\":true}"
    MODE[$v$c]="${MODE[$v]}"; BF[$v$c]="$bf"; SX[$v$c]="${SX[$v]}"; AF[$v$c]="${AF[$v]:+${AF[$v]},}$CAP$CAM,$LIGHT,$LOOK,\"pie_window\":[1728,972]"
    CON[$v$c]="\"console\":[\"a.AnimNode.OrientationWarping.Enable 1\",\"a.AnimNode.StrideWarping.Enable 1\",\"a.AnimNode.FootPlacement.Enable 1\",\"a.AnimNode.LegIK.Enable 1\",\"t.MaxFPS 30\"]"
  done
done
# ===== V2.31 candidates (on top of the saved V2.30 production) =====
# s1 = low-speed authored reversal family (PSD_SHM231S_SlowRev*, episode started < SHM231_SlowV 90 cm/s); x1 = no V2.14 RevPush window after an authored clip
cand s1 '"SHM231_SlowOn":1.0' ""
cand x1 '"SHM231_ExitAuth":1.0' ""
cand sx '"SHM231_SlowOn":1.0,"SHM231_ExitAuth":1.0' ""
# B1 (after the profiles / funcs build): inspection resolver (InspectFocusMode 2 = V2.31 tag + mask focus), step-up lift compensation,
# CMC perch (PIE-only live overrides on the spawned pawn) for the step-down hover
cand ins2 "" '"InspectFocusMode":2.0'
cand sl1 "" '"SwingLiftBaseComp":1.0'
cand pr1 '"live_cm":{"PerchRadiusThreshold":22.0,"PerchAdditionalHeight":40.0}' ""
cand slpr '"live_cm":{"PerchRadiusThreshold":22.0,"PerchAdditionalHeight":40.0}' '"SwingLiftBaseComp":1.0'
# determinism study: PIE-only always-tick pose + URO off on the spawned pawn's meshes (production otherwise)
cand det '"live_anim":{"always_tick":true}' ""
# B1 routing: forward low-speed reversal in jog mode (episode -> clip-bound capsule + hold for the slow family)
cand lf "" '"RedirectLowRevFwdMax":330.0'
cand slf '"SHM231_SlowOn":1.0' '"RedirectLowRevFwdMax":330.0'
# request-level keys (NOT abp_flags): live_cm / live_anim are qa_pie request keys -> AF holds the raw JSON member
AF[pr1]='"live_cm":{"PerchRadiusThreshold":22.0,"PerchAdditionalHeight":40.0}'
AF[slpr]='"live_cm":{"PerchRadiusThreshold":22.0,"PerchAdditionalHeight":40.0}'
AF[det]='"live_anim":{"always_tick":true}'
# B2: loaded catch-step F_B family through the V2.30 load route (B_F stays production); TIP-end one-frame hold
cand ld '"SHM230_LoadedOn":1.0,"SHM230_DB_JRFwdL":"/Game/GraceRanger/SHME/Animations/V231/PSD_SHM231L_LoadRevFwd","SHM230_DB_JRBwdL":"/Game/GraceRanger/SHME/Animations/V226/PSD_SHM226_JogRevBwd"' ""
cand sxld '"SHM231_SlowOn":1.0,"SHM231_ExitAuth":1.0,"SHM230_LoadedOn":1.0,"SHM230_DB_JRFwdL":"/Game/GraceRanger/SHME/Animations/V231/PSD_SHM231L_LoadRevFwd","SHM230_DB_JRBwdL":"/Game/GraceRanger/SHME/Animations/V226/PSD_SHM226_JogRevBwd"' ""
cand te '"SHM231_TipEndHold":1.0' ""
# P = every V2.31 group together (the promotion candidate); Pnl = P without the loaded family; Pnt = P without the TIP-end hold
LDF='"SHM230_LoadedOn":1.0,"SHM230_DB_JRFwdL":"/Game/GraceRanger/SHME/Animations/V231/PSD_SHM231L_LoadRevFwd","SHM230_DB_JRBwdL":"/Game/GraceRanger/SHME/Animations/V226/PSD_SHM226_JogRevBwd"'
cand P "\"SHM231_SlowOn\":1.0,\"SHM231_ExitAuth\":1.0,\"SHM231_TipEndHold\":1.0,$LDF" '"RedirectLowRevFwdMax":330.0,"InspectFocusMode":2.0,"SwingLiftBaseComp":1.0'
cand Pnl '"SHM231_SlowOn":1.0,"SHM231_ExitAuth":1.0,"SHM231_TipEndHold":1.0' '"RedirectLowRevFwdMax":330.0,"InspectFocusMode":2.0,"SwingLiftBaseComp":1.0'
cand Pnt "\"SHM231_SlowOn\":1.0,\"SHM231_ExitAuth\":1.0,$LDF" '"RedirectLowRevFwdMax":330.0,"InspectFocusMode":2.0,"SwingLiftBaseComp":1.0'
# AFTER the V2.31 switch: pre = the saved production with every V2.31 knob back at its V2.30 value (the "before" of the captures; the curved
# sprint loops were re-baked in place, so their before = the V2.30 published media)
cand pre '"SHM231_SlowOn":0.0,"SHM231_ExitAuth":0.0,"SHM231_TipEndHold":0.0,"SHM230_LoadedOn":0.0' '"RedirectLowRevFwdMax":0.0,"InspectFocusMode":1.0,"SwingLiftBaseComp":0.0'
# capture variants for variants defined after the V2.26 block above (same camera / light / look recipe)
for c in S D G; do
  case $c in S) CAM=",$SIDE";; D) CAM=",$DIAG";; G) CAM="";; esac
  for v in ${CAPV2:-}; do [ -z "${MODE[$v]}" ] && continue
    bf="${BF[$v]}"; [ $c != G ] && bf="${bf/\"GR215_CamYawFromControl\":false/\"GR215_CamYawFromControl\":true}"
    MODE[$v$c]="${MODE[$v]}"; BF[$v$c]="$bf"; SX[$v$c]="${SX[$v]}"; AF[$v$c]="${AF[$v]:+${AF[$v]},}$CAP$CAM,$LIGHT,$LOOK,\"pie_window\":[1728,972]"
    CON[$v$c]="\"console\":[\"a.AnimNode.OrientationWarping.Enable 1\",\"a.AnimNode.StrideWarping.Enable 1\",\"a.AnimNode.FootPlacement.Enable 1\",\"a.AnimNode.LegIK.Enable 1\",\"t.MaxFPS 30\"]"
  done
done
# ===== V2.32 candidates (on top of the saved V2.31 production) =====
# camera: cinematic orbit (SHM_UpdateCameraV21 -> GR_SHM_CamOrbit, boom yaw only). c1s small first, c1 default, c1l larger (only if c1 is safe)
cand c1s "" '"CamOrbitEnabled":true,"CamOrbitMaxWalk":1.0,"CamOrbitMaxJog":5.0,"CamOrbitMaxSprint":9.0'
cand c1  "" '"CamOrbitEnabled":true'
cand c1l "" '"CamOrbitEnabled":true,"CamOrbitMaxWalk":3.0,"CamOrbitMaxJog":12.0,"CamOrbitMaxSprint":20.0'
# motion: tick-order candidate (PIE-only live key, request level -> raw AF): SHME before the mesh animation (one-frame routing lag removed)
cand tk "" ""
AF[tk]='"live_tick":{"shm_pre":true}'
# D owner isolation (stop closing step lowered 6-8 cm at runtime): settle / terrain body off; FootPlacement off only
cand oFP "" "" '"a.AnimNode.FootPlacement.Enable 0"'
# C: backward start from stand bound to the clip's designed speed (start witness SHM232_SW on SHM_JogQ_af_Loco_Jog_Bwd_Start_AAMS)
cand sb '"SHM232_StartBind":1.0' ""
cand sbtk '"SHM232_StartBind":1.0' ""
AF[sbtk]="${AF[sbtk]},\"live_tick\":{\"shm_pre\":true}"
# E: walk plant settings - the planted foot pivots on its ball instead of unplanting at 45 deg of twist (PlantSettings_Walk = PivotAroundBall)
cand pa90 "" ""
AF[pa90]='"live_plant":{"PlantSettings_Walk":{"unplant_angle":90.0}}'
cand pa120 "" ""
AF[pa120]='"live_plant":{"PlantSettings_Walk":{"unplant_angle":120.0}}'
# camera round 2: the arc inside the physical event (shorter lag / smoother), sprint 16 deg; c2b body-only target (no travel term)
cand c2  "" '"CamOrbitEnabled":true,"CamOrbitLagTau":0.3,"CamOrbitFreq":5.0,"CamOrbitMaxSprint":16.0'
cand c2b "" '"CamOrbitEnabled":true,"CamOrbitLagTau":0.3,"CamOrbitFreq":5.0,"CamOrbitMaxSprint":16.0,"CamOrbitTravelW":0.0'
# effort: loaded catch-step reversal on BOTH directions (B_F loaded family PSD_SHM231L_LoadRevBwd) + the rebuilt F_B DB (P29 re-made, P21/P30
# production fallback); ldbtk = + the tick-order fix
LDB='"SHM230_DB_JRBwdL":"/Game/GraceRanger/SHME/Animations/V231/PSD_SHM231L_LoadRevBwd"'
cand ldb "$LDB" ""
cand ldbtk "$LDB" ""
AF[ldbtk]="${AF[ldbtk]},\"live_tick\":{\"shm_pre\":true}"
# tick order through the EXISTING owner (V2.0 tick split, DA flag IntentTickPrePhysics read at BeginPlay) = what the live tk experiment does
cand itp "" '"IntentTickPrePhysics":true'
# A: B_F databases WITH the forward exit loop (no end-of-clip search into another B_F bin); bfxl = + the loaded B_F family (catch step)
BFX='"SHM224_DB_JRBwd":"/Game/GraceRanger/SHME/Animations/V232/PSD_SHM232_JogRevBwdX","SHM224_DB_JRBwdM":"/Game/GraceRanger/SHME/Animations/V232/PSD_SHM232_JogRevBwdX","SHM231_DB_JRBwdS":"/Game/GraceRanger/SHME/Animations/V232/PSD_SHM232_SlowRevBwdX"'
cand bfx "$BFX" ""
cand bfxl "$BFX,\"SHM230_DB_JRBwdL\":\"/Game/GraceRanger/SHME/Animations/V232/PSD_SHM232_LoadRevBwdX\"" ""
# E (corrected): pa90 / pa120 were NOT_TRIGGERED (live_plant: the struct is not editable on the anim instance) -> through the ABP CDO
# abp_flags '<struct>.<field>' (qa_pie V2.32 _gp/_sp, restored after the run)
cand pb90 '"PlantSettings_Walk.unplant_angle":90.0' ""
cand pb120 '"PlantSettings_Walk.unplant_angle":120.0' ""
# camera round 3 (capture comparison): c3 = a wider arc (sprint 22, jog 10) with the same smooth dynamics
cand c3  "" '"CamOrbitEnabled":true,"CamOrbitLagTau":0.25,"CamOrbitFreq":5.5,"CamOrbitMaxSprint":22.0,"CamOrbitMaxJog":10.0'
# T6 (after the C1 build): the swing target lowered by the pelvis lag after a step-up (floored at the path ground + SwingLiftMargin)
cand t6a "" '"SwingPelvisComp":1.0'
cand t6b "" '"SwingPelvisComp":0.7'
# D owner isolation round 2 (the swing foot dips 3 cm under its planted level at the closing step in the MM output pose, not in the clip):
# PBI off / SHME brake posture off / both
cand oBRK "" '"BrakePostureEnabled":false'
cand oPB "" '"BrakePostureEnabled":false' "" '"ProfileEnabled":false'
# T7 swing floor guard (after the C1 build): the closing / starting swing foot never under its planted height + 1.5 cm
cand fg "" '"SwingFloorGuard":1.5'
cand t6fg "" '"SwingPelvisComp":1.0,"SwingFloorGuard":1.5'
# ===== P = the V2.32 promotion candidate: camera c2 + B_F exit-loop DBs incl. the loaded B_F catch-step family (bfxl) + T7 swing floor
# guard (fg). Rejected (not in P): tick order (tk / itp), T6, start bind (sb), idle-stance start copies (neutralised), stop clip re-bake
# (reverted), walk unplant angle (no effect).
cand P "$BFX,\"SHM230_DB_JRBwdL\":\"/Game/GraceRanger/SHME/Animations/V232/PSD_SHM232_LoadRevBwdX\"" '"CamOrbitEnabled":true,"CamOrbitLagTau":0.3,"CamOrbitFreq":5.0,"CamOrbitMaxSprint":16.0,"SwingFloorGuard":1.5'
# V2.32 ISO (after P2: P regressed c29_combo 48.8 -> 57.6 and j30_rel_3450 24.5 -> 27.3): P without the floor guard
cand Pnf "$BFX,\"SHM230_DB_JRBwdL\":\"/Game/GraceRanger/SHME/Animations/V232/PSD_SHM232_LoadRevBwdX\"" '"CamOrbitEnabled":true,"CamOrbitLagTau":0.3,"CamOrbitFreq":5.0,"CamOrbitMaxSprint":16.0'
# ---- V2.33 candidates
cand sbk '"SHM233_StandBackOn":1.0' ""
cand sbk2 '"SHM233_StandBackOn":1.0,"SHM233_DB_StandBack":"/Game/GraceRanger/SHME/Animations/V233/PSD_SHM233_StandBackStart2"' ""
cand sb22 '"SHM233_StandBackOn":2.0,"SHM233_DB_StandBack":"/Game/GraceRanger/SHME/Animations/V233/PSD_SHM233_StandBackStart2"' ""
cand rec "" '"CamRecEnabled":true'
cand Q '"SHM233_StandBackOn":2.0,"SHM233_DB_StandBack":"/Game/GraceRanger/SHME/Animations/V233/PSD_SHM233_StandBackStart2"' '"CamRecEnabled":true'
# Qp = Q with the GAMEPAD recentre profile (the harness input is keyboard -> the mouse profile 0.35 applies by default)
cand Qp '"SHM233_StandBackOn":2.0,"SHM233_DB_StandBack":"/Game/GraceRanger/SHME/Animations/V233/PSD_SHM233_StandBackStart2"' '"CamRecEnabled":true'
AF[Qp]="${AF[Qp]},\"pawn_flags\":{\"GR233_RecMouseScale\":1.0}"
cand Q2 '"SHM233_StandBackOn":2.0,"SHM233_DB_StandBack":"/Game/GraceRanger/SHME/Animations/V233/PSD_SHM233_StandBackStart2"' '"CamRecEnabled":true,"CamRecMaxErr":110.0'
cand Q3 '"SHM233_StandBackOn":2.0,"SHM233_DB_StandBack":"/Game/GraceRanger/SHME/Animations/V233/PSD_SHM233_StandBackStart2"' '"CamRecEnabled":true,"CamRecMaxErr":110.0,"CamRecMinSpeed":200.0'
cand sc '"SHM211_DB_Sprint":"/Game/GraceRanger/SHME/Animations/V233/SprintCalm/PSD_SHM233_SprintCalm"' ''
# ---- post-promotion matrix (A/B/C/D): pre233 = every V2.33 knob at its V2.32 value; body = new body + old camera; cam = old body + new camera
cand pre233 '"SHM233_StandBackOn":0.0' '"CamRecEnabled":false'
cand body233 "" '"CamRecEnabled":false'
cand cam233 '"SHM233_StandBackOn":0.0' ''
cand pad233 "" ''
AF[pad233]="\"pawn_flags\":{\"GR233_RecMouseScale\":1.0}"
# ---- V2.34 candidates (locomotion frame). p suffix = gamepad recentre profile (harness input is keyboard -> mouse scale 0.35 otherwise)
PADF='"pawn_flags":{"GR233_RecMouseScale":1.0}'
cand L    "" '"LocoFrameEnabled":true'
cand Lx   "" '"LocoFrameEnabled":true,"LocoExploreEnabled":true'
cand LxW  "" '"LocoFrameEnabled":true,"LocoExploreEnabled":true,"CamRecMinSpeed":60.0'
cand LxWoff "" '"LocoFrameEnabled":true,"LocoExploreEnabled":true,"CamRecEnabled":false'
cand oW   "" '"CamRecMinSpeed":60.0'
cand ooff "" '"CamRecEnabled":false'
for v in L Lx LxW LxWoff oW ooff; do cand ${v}p "" "${SX[$v]:1:-1}"; AF[${v}p]="$PADF"; done
cand op "" ''; AF[op]="$PADF"
# ---- V2.34 B2 candidate C: locomotion frame + exploration + walk recentre (calm walk rate) + phase envelope + body-facing gate + real-turn side
CX='"LocoFrameEnabled":true,"LocoExploreEnabled":true,"CamRecMinSpeed":60.0,"CamEnvEnabled":true,"CamRecFaceMax":40.0,"CamRecTurnSide":true,"CamRecWalkRate":45.0'
cand C  "" "$CX"
cand Cp "" "$CX"; AF[Cp]="$PADF"
cand Coffp "" "$CX,\"CamRecEnabled\":false"; AF[Coffp]="$PADF"
cand CnoEp "" "$CX,\"CamEnvEnabled\":false"; AF[CnoEp]="$PADF"
# ---- V2.34 sprint upper-body owner isolation (calm sprint DB sc + one stage off each)
SCDB='"SHM211_DB_Sprint":"/Game/GraceRanger/SHME/Animations/V233/SprintCalm/PSD_SHM233_SprintCalm"'
cand scPBI "$SCDB" "" "" '"ProfileEnabled":false'
cand scSS  "$SCDB" '"SupportShiftEnabled":false'
cand scCL  "$SCDB" '"CurveLeanDirectEnabled":false'
cand scAPA "$SCDB" '"ApaBodyEnabled":false'
cand scFP  "$SCDB" "" '"a.AnimNode.FootPlacement.Enable 0"'
cand scALL "$SCDB" '"SupportShiftEnabled":false,"CurveLeanDirectEnabled":false,"ApaBodyEnabled":false,"BrakePostureEnabled":false' "" '"ProfileEnabled":false'
# ---- V2.34 B3 release-repress keep (RevGraceTime) on top of the camera candidate C
cand R  "" "$CX,\"RevGraceTime\":0.4"
cand Ro "" '"RevGraceTime":0.4'
# ---- V2.34 B4 candidate C2 = C + exploration limited to walk / jog (< 380), input held 0.25 s, body frame turn <= 150 deg/s
CX2="$CX,\"LocoExploreMaxSpeed\":380.0,\"LocoExploreStable\":0.25,\"LocoTurnRate\":150.0"
cand C2  "" "$CX2"
cand C2p "" "$CX2"; AF[C2p]="$PADF"
cand C2offp "" "$CX2,\"CamRecEnabled\":false"; AF[C2offp]="$PADF"
cand C2R "" "$CX2,\"RevGraceTime\":0.4"
cand C2Rp "" "$CX2,\"RevGraceTime\":0.4"; AF[C2Rp]="$PADF"
# ---- V2.34 B6 candidate C3 = C + exploration only in calm normal travel below 380, input held 0.25 s (no body-frame rate limit)
CX3="$CX,\"LocoExploreMaxSpeed\":380.0,\"LocoExploreStable\":0.25"
cand C3  "" "$CX3"
cand C3p "" "$CX3"; AF[C3p]="$PADF"
cand C3offp "" "$CX3,\"CamRecEnabled\":false"; AF[C3offp]="$PADF"
# ---- V2.34 B7 release-repress: ABP reversal-DB keep (SHM234_RevKeepOn) alone / with the component grace
cand K  '"SHM234_RevKeepOn":1.0' ""
cand KR '"SHM234_RevKeepOn":1.0' '"RevGraceTime":0.4'
# ---- V2.34 B8 combined candidate F = C3 (+ exploration only >= 0.5 s into the normal family, built in B8) + release-repress keep (ABP + grace)
FX="$CX3,\"RevGraceTime\":0.4"
cand F  '"SHM234_RevKeepOn":1.0' "$FX"
cand Fp '"SHM234_RevKeepOn":1.0' "$FX"; AF[Fp]="${AF[Fp]},$PADF"
cand Foffp '"SHM234_RevKeepOn":1.0' "$FX,\"CamRecEnabled\":false"; AF[Foffp]="${AF[Foffp]},$PADF"
cand Fsc '"SHM234_RevKeepOn":1.0,"SHM211_DB_Sprint":"/Game/GraceRanger/SHME/Animations/V233/SprintCalm/PSD_SHM233_SprintCalm"' "$FX"
# ---- V2.34 B10 candidate G = C (no stability wait) + exploration < 380 + B10 start gate (built) + release-repress keep (ABP + grace incl. the gap)
GX="$CX,\"LocoExploreMaxSpeed\":380.0,\"RevGraceTime\":0.4"
cand G  '"SHM234_RevKeepOn":1.0' "$GX"
cand Gp '"SHM234_RevKeepOn":1.0' "$GX"; AF[Gp]="${AF[Gp]},$PADF"
cand Goffp '"SHM234_RevKeepOn":1.0' "$GX,\"CamRecEnabled\":false"; AF[Goffp]="${AF[Goffp]},$PADF"
cand Gsc '"SHM234_RevKeepOn":1.0,"SHM211_DB_Sprint":"/Game/GraceRanger/SHME/Animations/V233/SprintCalm/PSD_SHM233_SprintCalm"' "$GX"
cand Gscp '"SHM234_RevKeepOn":1.0,"SHM211_DB_Sprint":"/Game/GraceRanger/SHME/Animations/V233/SprintCalm/PSD_SHM233_SprintCalm"' "$GX"; AF[Gscp]="${AF[Gscp]},$PADF"
# ---- V2.34 post-promotion matrix (A/B/C/D) + profiles. pre234 = every V2.34 knob at its V2.33 value (the stop-clip toe clearance is content
# and stays in all four); body234 = new body (loco frame + exploration, release-repress keep, calm sprint) + V2.33 camera; cam234 = V2.33
# body + new camera (walk follow, envelope, facing gate, turn side).
PRE_AF='"SHM234_RevKeepOn":0.0,"SHM211_DB_Sprint":"/Game/GraceRanger/Animations/LocomotionBehavior/PSD_LB_SprintLoops"'
PRE_CAM='"CamRecMinSpeed":170.0,"CamRecWalkRate":0.0,"CamRecFaceMax":0.0,"CamRecTurnSide":false,"CamEnvEnabled":false'
PRE_BODY='"LocoFrameEnabled":false,"LocoExploreEnabled":false,"LocoExploreMaxSpeed":0.0,"RevGraceTime":0.0'
cand pre234 "$PRE_AF" "$PRE_CAM,$PRE_BODY"
cand body234 "" "$PRE_CAM"
cand cam234 "$PRE_AF" "$PRE_BODY"
cand pad234 "" ''; AF[pad234]="$PADF"
cand pre234p "$PRE_AF" "$PRE_CAM,$PRE_BODY"; AF[pre234p]="${AF[pre234p]},$PADF"
# ===== V2.35 candidates (on top of the saved V2.34 production) =====
# rv = support-exchange jog reversal content (gen235_rev.py: SHM235_JogRev_* in PSD_SHM235_JogRevFwd / PSD_SHM235_JogRevBwdX)
RV='"SHM224_DB_JRFwd":"/Game/GraceRanger/SHME/Animations/V235/PSD_SHM235_JogRevFwd","SHM224_DB_JRFwdM":"/Game/GraceRanger/SHME/Animations/V235/PSD_SHM235_JogRevFwd","SHM224_DB_JRBwd":"/Game/GraceRanger/SHME/Animations/V235/PSD_SHM235_JogRevBwdX","SHM224_DB_JRBwdM":"/Game/GraceRanger/SHME/Animations/V235/PSD_SHM235_JogRevBwdX"'
cand rv "$RV" ""
# capture variants (side S / diagonal D / game G) for the V2.35 variants listed in CAPV3
for c in S D G; do
  case $c in S) CAM=",$SIDE";; D) CAM=",$DIAG";; G) CAM="";; esac
  for v in ${CAPV3:-}; do [ -z "${MODE[$v]}" ] && continue
    bf="${BF[$v]}"; [ $c != G ] && bf="${bf/\"GR215_CamYawFromControl\":false/\"GR215_CamYawFromControl\":true}"
    MODE[$v$c]="${MODE[$v]}"; BF[$v$c]="$bf"; SX[$v$c]="${SX[$v]}"; AF[$v$c]="${AF[$v]:+${AF[$v]},}$CAP$CAM,$LIGHT,$LOOK,\"pie_window\":[1728,972]"
    CON[$v$c]="\"console\":[\"a.AnimNode.OrientationWarping.Enable 1\",\"a.AnimNode.StrideWarping.Enable 1\",\"a.AnimNode.FootPlacement.Enable 1\",\"a.AnimNode.LegIK.Enable 1\",\"t.MaxFPS 30\"]"
  done
done
# owner isolation of the rv planted-foot slide (F_B P16 catch foot +11 cm in game, pinned in the clip): stride / orientation warping / foot placement off
cand rvSW "$RV" "" '"a.AnimNode.StrideWarping.Enable 0"'
cand rvOW "$RV" "" '"a.AnimNode.OrientationWarping.Enable 0"'
cand rvFP "$RV" "" '"a.AnimNode.FootPlacement.Enable 0"'
# B1 (after the routing build): reversal takes over a hard-turn episode (RevOverHard), with and without the V2.35 reversal content
cand oR "" '"RevOverHard":true'
cand rvR "$RV" '"RevOverHard":true'
# B3: camera on / off on the same candidate body (selection divergence test) and the mouse walk-follow scale
cand rvRoff "$RV" '"RevOverHard":true,"CamRecEnabled":false'
cand rvRm "$RV" '"RevOverHard":true'; AF[rvRm]="${AF[rvRm]},\"pawn_flags\":{\"GR233_RecMouseScale\":0.7}"
# B6 (after the second routing build): the release gap keeps the reversal episode (RevGapKeep)
cand rvRG2 "$RV" '"RevOverHard":true,"RevGapKeep":true'
cand oRG2 "" '"RevOverHard":true,"RevGapKeep":true'
# ---- V2.35 post-promotion matrix: pre235 = every V2.35 knob at its V2.34 value (the jog stop re-plan is content and stays in all);
# body235 = new body (reversal content, route, gap keep) + V2.34 camera (mouse follow 0.35); cam235 = V2.34 body + new camera (mouse 0.7)
PRE5_AF='"SHM224_DB_JRFwd":"/Game/GraceRanger/SHME/Animations/V226/PSD_SHM226_JogRevFwd","SHM224_DB_JRFwdM":"/Game/GraceRanger/SHME/Animations/V226/PSD_SHM226_JogRevFwd","SHM224_DB_JRBwd":"/Game/GraceRanger/SHME/Animations/V232/PSD_SHM232_JogRevBwdX","SHM224_DB_JRBwdM":"/Game/GraceRanger/SHME/Animations/V232/PSD_SHM232_JogRevBwdX"'
cand pre235 "$PRE5_AF" '"RevOverHard":false,"RevGapKeep":false'; AF[pre235]="${AF[pre235]},\"pawn_flags\":{\"GR233_RecMouseScale\":0.35}"
cand body235 "" ''; AF[body235]="\"pawn_flags\":{\"GR233_RecMouseScale\":0.35}"
cand cam235 "$PRE5_AF" '"RevOverHard":false,"RevGapKeep":false'
cand pad235 "" ''; AF[pad235]="$PADF"
# ---- V2.36: jog stop family candidates (ABP SHM236_DB_JogStop; default = production PSD_CP2_JogStop)
V6=/Game/GraceRanger/SHME/Animations/V236
cand s1 "\"SHM236_DB_JogStop\":\"$V6/PSD_SHM236_JogStop\"" ''
cand s2 "\"SHM236_DB_JogStop\":\"$V6/PSD_SHM236_JogStop2\"" ''
cand s3 "\"SHM236_DB_JogStop\":\"$V6/PSD_SHM236_JogStop3\"" ''
# capture variants (side S / diagonal D / game G) for the V2.36 variants listed in CAPV4
for c in S D G; do
  case $c in S) CAM=",$SIDE";; D) CAM=",$DIAG";; G) CAM="";; esac
  for v in ${CAPV4:-}; do [ -z "${MODE[$v]}" ] && continue
    bf="${BF[$v]}"; [ $c != G ] && bf="${bf/\"GR215_CamYawFromControl\":false/\"GR215_CamYawFromControl\":true}"
    MODE[$v$c]="${MODE[$v]}"; BF[$v$c]="$bf"; SX[$v$c]="${SX[$v]}"; AF[$v$c]="${AF[$v]:+${AF[$v]},}$CAP$CAM,$LIGHT,$LOOK,\"pie_window\":[1728,972]"
    CON[$v$c]="\"console\":[\"a.AnimNode.OrientationWarping.Enable 1\",\"a.AnimNode.StrideWarping.Enable 1\",\"a.AnimNode.FootPlacement.Enable 1\",\"a.AnimNode.LegIK.Enable 1\",\"t.MaxFPS 30\"]"
  done
done
# V2.36 straight jog starts (left / right first swing) in COPIES of the production start databases
STDB="\"SHM_JogStartDB_L\":\"$V6/PSD_SHM236_JogStartS_L\",\"SHM_JogStartDB_R\":\"$V6/PSD_SHM236_JogStartS_R\""
cand st "$STDB" ''
cand s2st "\"SHM236_DB_JogStop\":\"$V6/PSD_SHM236_JogStop2\",$STDB" ''
# V2.36 whole-body reversal content (+ loaded effort family) on top of the stop / start candidate
RV6="\"SHM224_DB_JRFwd\":\"$V6/PSD_SHM236_JogRevFwd\",\"SHM224_DB_JRFwdM\":\"$V6/PSD_SHM236_JogRevFwd\",\"SHM224_DB_JRBwd\":\"$V6/PSD_SHM236_JogRevBwdX\",\"SHM224_DB_JRBwdM\":\"$V6/PSD_SHM236_JogRevBwdX\",\"SHM230_DB_JRFwdL\":\"$V6/PSD_SHM236L_LoadRevFwd\""
cand wb "\"SHM236_DB_JogStop\":\"$V6/PSD_SHM236_JogStop2\",$STDB,$RV6" ''
cand rvo "$RV6" ''
# V2.36 resume route: a re-press during a jog stop searches the vendor start + the jog loop (ABP SHM236_DB_JogResume)
cand wbr "\"SHM236_DB_JogStop\":\"$V6/PSD_SHM236_JogStop2\",$STDB,$RV6,\"SHM236_DB_JogResume\":\"$V6/PSD_SHM236_JogResume\"" ''
# ---- V2.36 post-promotion matrix: pre236 = every V2.36 group at its V2.35 value (old CP2 jog stop, production start DBs, V2.35 reversal,
# V2.31 loaded reversal); o = the saved V2.36 production
PRE6_AF="\"SHM236_DB_JogStop\":\"/Game/GraceRanger/Animations/CorePerformance/PSD_CP2_JogStop\",\"SHM_JogStartDB_L\":\"/Game/GraceRanger/SHME/Animations/Starts/PSD_SHM_JogStartS_L\",\"SHM_JogStartDB_R\":\"/Game/GraceRanger/SHME/Animations/Starts/PSD_SHM_JogStartS_R\",$RV,\"SHM230_DB_JRFwdL\":\"/Game/GraceRanger/SHME/Animations/V231/PSD_SHM231L_LoadRevFwd\""
cand pre236 "$PRE6_AF" ''
# camera on / off with the SAME (V2.36 production) body: camoff = only the auto recentre switched off (CamRecEnabled false)
cand camoff "" '"CamRecEnabled":false'
# ---- V2.37: footstep-planned straight starts (start DB copies of the VENDOR start DBs) + CP start route copy (resume) with the starts and
# the re-push links; o = the saved V2.36 production
V7=/Game/GraceRanger/SHME/Animations/V237
ST7="\"SHM_JogStartDB_L\":\"$V7/PSD_SHM237_JogStartS_L\",\"SHM_JogStartDB_R\":\"$V7/PSD_SHM237_JogStartS_R\""
RS7="\"SHM236_DB_JogResume\":\"$V7/PSD_SHM237_JogResume\""
cand s7 "$ST7,$RS7" ''
cand s7a "$ST7" ''
# V2.37 pelvis owned by the clip in the stop brake: V237 stop family copy (soft brake knee, absorption dip, SHM237_FPPelvisOff curve;
# ABP FootPlacement DisablePelvisCurveName = SHM237_FPPelvisOff, a no-op for clips without the curve)
SP7="\"SHM236_DB_JogStop\":\"$V7/PSD_SHM237_JogStop\""
cand s8 "$ST7,$RS7,$SP7" ''
cand sp7 "$SP7" ''
# ---- V2.37 post-promotion matrix: pre237 = every V2.37 group at its V2.36 value (V2.36 stop family, V2.36 start DB copies, CP2 start route);
# the FootPlacement DisablePelvisCurveName stays installed (a no-op for the V2.36 clips, which carry no curve); o = the saved V2.37 production
PRE7_AF="\"SHM236_DB_JogStop\":\"$V6/PSD_SHM236_JogStop2\",\"SHM_JogStartDB_L\":\"$V6/PSD_SHM236_JogStartS_L\",\"SHM_JogStartDB_R\":\"$V6/PSD_SHM236_JogStartS_R\",\"SHM236_DB_JogResume\":\"/Game/GraceRanger/Animations/CorePerformance/PSD_CP2_JogStart\""
cand pre237 "$PRE7_AF" ''
# ---- V2.37 stop-entry stickiness: the stop DB re-selected a new phase bin at clip time 0 on every search for ~0.08 s after the release
# (P04->P16->P05->P17->P06 at 120 FPS) -> the bin that finally plays starts ~0.07 s late with its speed clock at the release speed (planted
# foot slides 15-20 cm at 60/120). Candidates: copies of the promoted stop DB with a stronger continuing-pose bias (same 24 entries).
cand cb10 "\"SHM236_DB_JogStop\":\"$V7/PSD_SHM237_JogStop_cb10\"" ''
cand cb25 "\"SHM236_DB_JogStop\":\"$V7/PSD_SHM237_JogStop_cb25\"" ''
# ---- V2.38: jog 90 cut route = the V2.10 jog lateral bridge switch (jog lateral episodes not skipped -> SHM_RedirectDB_JL, held while the
# episode lives) with the existing bridge database (route test) or a V2.38 cut database (candidate)
V8=/Game/GraceRanger/SHME/Animations/V238
cand jc1 '"SHM210_JogCutMode":1.0' ''
# V2.38 candidate: jog lateral episodes routed to the physics-planned cut family (PSD_SHM238_JogCut, bias -25) + the clip-bound heading contract
cand cut1 "\"SHM210_JogCutMode\":1.0,\"SHM_RedirectDB_JL\":\"$V8/PSD_SHM238_JogCut\",\"SHM238_Yaw\":1.0" ''
for c in S D G; do
  case $c in S) CAM=",$SIDE";; D) CAM=",$DIAG";; G) CAM="";; esac
  for v in ${CAPV4:-}; do [ -z "${MODE[$v]}" ] && continue
    bf="${BF[$v]}"; [ $c != G ] && bf="${bf/\"GR215_CamYawFromControl\":false/\"GR215_CamYawFromControl\":true}"
    MODE[$v$c]="${MODE[$v]}"; BF[$v$c]="$bf"; SX[$v$c]="${SX[$v]}"; AF[$v$c]="${AF[$v]:+${AF[$v]},}$CAP$CAM,$LIGHT,$LOOK,\"pie_window\":[1728,972]"
    CON[$v$c]="\"console\":[\"a.AnimNode.OrientationWarping.Enable 1\",\"a.AnimNode.StrideWarping.Enable 1\",\"a.AnimNode.FootPlacement.Enable 1\",\"a.AnimNode.LegIK.Enable 1\",\"t.MaxFPS 30\"]"
  done
done
# V2.38 cut2 = cut1 + post-clip recovery guard 1.6 s (the component push detector also fires on the clip's own re-acceleration; PerturbTau 0.6 s)
cand cut2 "\"SHM210_JogCutMode\":1.0,\"SHM_RedirectDB_JL\":\"$V8/PSD_SHM238_JogCut\",\"SHM238_Yaw\":1.0,\"SHM238_GuardS\":1.6" ''
for c in S D G; do
  case $c in S) CAM=",$SIDE";; D) CAM=",$DIAG";; G) CAM="";; esac
  for v in ${CAPV4:-}; do [ -z "${MODE[$v]}" ] && continue
    bf="${BF[$v]}"; [ $c != G ] && bf="${bf/\"GR215_CamYawFromControl\":false/\"GR215_CamYawFromControl\":true}"
    MODE[$v$c]="${MODE[$v]}"; BF[$v$c]="$bf"; SX[$v$c]="${SX[$v]}"; AF[$v$c]="${AF[$v]:+${AF[$v]},}$CAP$CAM,$LIGHT,$LOOK,\"pie_window\":[1728,972]"
    CON[$v$c]="\"console\":[\"a.AnimNode.OrientationWarping.Enable 1\",\"a.AnimNode.StrideWarping.Enable 1\",\"a.AnimNode.FootPlacement.Enable 1\",\"a.AnimNode.LegIK.Enable 1\",\"t.MaxFPS 30\"]"
  done
done
# V2.38 cut3 = cut2 + travel gaze while the camera recentre is pending / active (GR LookAt chain; vendor aim offset untouched)
cand cut3 "\"SHM210_JogCutMode\":1.0,\"SHM_RedirectDB_JL\":\"$V8/PSD_SHM238_JogCut\",\"SHM238_Yaw\":1.0,\"SHM238_GuardS\":1.6,\"SHM238_Gaze\":1.0" ''
cand gz "\"SHM238_Gaze\":1.0" ''
for c in S D G; do
  case $c in S) CAM=",$SIDE";; D) CAM=",$DIAG";; G) CAM="";; esac
  for v in ${CAPV4:-}; do [ -z "${MODE[$v]}" ] && continue
    bf="${BF[$v]}"; [ $c != G ] && bf="${bf/\"GR215_CamYawFromControl\":false/\"GR215_CamYawFromControl\":true}"
    MODE[$v$c]="${MODE[$v]}"; BF[$v$c]="$bf"; SX[$v$c]="${SX[$v]}"; AF[$v$c]="${AF[$v]:+${AF[$v]},}$CAP$CAM,$LIGHT,$LOOK,\"pie_window\":[1728,972]"
    CON[$v$c]="\"console\":[\"a.AnimNode.OrientationWarping.Enable 1\",\"a.AnimNode.StrideWarping.Enable 1\",\"a.AnimNode.FootPlacement.Enable 1\",\"a.AnimNode.LegIK.Enable 1\",\"t.MaxFPS 30\"]"
  done
done
# ---- V2.38 post-promotion matrix: o = saved V2.38 production; pre238 = every V2.38 knob at its V2.37 value (content stays installed, inert)
cand pre238 "\"SHM210_JogCutMode\":0.0,\"SHM_RedirectDB_JL\":\"/Game/GraceRanger/SHME/Animations/Redirect/PSD_SHM_Redirect_JogLateral\",\"SHM238_Yaw\":0.0,\"SHM238_GuardS\":0.8,\"SHM238_Gaze\":0.0" ''
for c in S D G; do
  case $c in S) CAM=",$SIDE";; D) CAM=",$DIAG";; G) CAM="";; esac
  for v in ${CAPV4:-}; do [ -z "${MODE[$v]}" ] && continue
    bf="${BF[$v]}"; [ $c != G ] && bf="${bf/\"GR215_CamYawFromControl\":false/\"GR215_CamYawFromControl\":true}"
    MODE[$v$c]="${MODE[$v]}"; BF[$v$c]="$bf"; SX[$v$c]="${SX[$v]}"; AF[$v$c]="${AF[$v]:+${AF[$v]},}$CAP$CAM,$LIGHT,$LOOK,\"pie_window\":[1728,972]"
    CON[$v$c]="\"console\":[\"a.AnimNode.OrientationWarping.Enable 1\",\"a.AnimNode.StrideWarping.Enable 1\",\"a.AnimNode.FootPlacement.Enable 1\",\"a.AnimNode.LegIK.Enable 1\",\"t.MaxFPS 30\"]"
  done
done
cand tk '"SHM239_Own":1.0' ''
cand tkx '"SHM239_Own":1.0,"SHM239_DB_Opp":"/Game/GraceRanger/SHME/Animations/V239/PSD_SHM239_Tk_Back"' ''
cand tk2 '"SHM239_Own":1.0,"SHM239_TkThr":999.0,"SHM_RedirectDB_JL":"/Game/GraceRanger/SHME/Animations/V239/PSD_SHM239_JogCutTk"' ''
cand ext '"SHM240_ExtOn":1.0' ''
cand hd '"SHM240_HeadOn":1.0' ''
cand tkh '"SHM239_Own":1.0,"SHM240_HeadOn":1.0' ''
cand wst '"SHM239_Own":1.0,"SHM240_HeadOn":1.0,"SHM240_BlkDB":"/Game/GraceRanger/SHME/Animations/V237/PSD_SHM237_JogStop"' ''
cand wof '"SHM239_Own":1.0,"SHM240_HeadOn":1.0,"SHM240_BlkSpd":-1.0' ''
# ---- V2.41
cand tkk '"SHM239_Own":1.0,"SHM240_HeadOn":1.0,"SHM241_KOn":1.0' ''
cand tkp '"SHM239_Own":1.0,"SHM240_HeadOn":1.0,"SHM241_KOn":1.0,"SHM241_PushYawK":0.15' ''
cand extp '"SHM240_ExtOn":1.0,"SHM241_PushYawK":0.15' ''
cand st '"SHM241_StartOn":1.0' ''
cand tks '"SHM239_Own":1.0,"SHM240_HeadOn":1.0,"SHM241_KOn":1.0,"SHM241_StartOn":1.0' ''
cand aoh '' ''
PRE[aoh]=Tools/SHME_V241_20261031/pre241_ao.py; POST[aoh]=Tools/SHME_V241_20261031/post241_ao.py
cand tkha '"SHM239_Own":1.0,"SHM240_HeadOn":1.0,"SHM241_KOn":1.0' ''
PRE[tkha]=Tools/SHME_V241_20261031/pre241_ao.py; POST[tkha]=Tools/SHME_V241_20261031/post241_ao.py
# ---- V2.41 capture variants (after the V2.41 cands): S side / D diagonal / G game camera
for c in S D G; do
  case $c in S) CAM=",$SIDE";; D) CAM=",$DIAG";; G) CAM="";; esac
  for v in ${CAPV4:-}; do [ -z "${MODE[$v]}" ] && continue
    bf="${BF[$v]}"; [ $c != G ] && bf="${bf/\"GR215_CamYawFromControl\":false/\"GR215_CamYawFromControl\":true}"
    MODE[$v$c]="${MODE[$v]}"; BF[$v$c]="$bf"; SX[$v$c]="${SX[$v]}"; AF[$v$c]="${AF[$v]:+${AF[$v]},}$CAP$CAM,$LIGHT,$LOOK,\"pie_window\":[1728,972]"
    CON[$v$c]="\"console\":[\"a.AnimNode.OrientationWarping.Enable 1\",\"a.AnimNode.StrideWarping.Enable 1\",\"a.AnimNode.FootPlacement.Enable 1\",\"a.AnimNode.LegIK.Enable 1\",\"t.MaxFPS 30\"]"
    [ -n "${PRE[$v]}" ] && PRE[$v$c]="${PRE[$v]}" && POST[$v$c]="${POST[$v]}"
  done
done
