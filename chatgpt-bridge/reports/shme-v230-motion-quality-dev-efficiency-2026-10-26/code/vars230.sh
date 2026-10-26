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
