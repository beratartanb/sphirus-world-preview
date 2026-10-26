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
