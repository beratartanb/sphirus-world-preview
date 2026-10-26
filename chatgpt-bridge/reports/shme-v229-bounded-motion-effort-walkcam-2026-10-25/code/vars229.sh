# vars229.sh: V2.29 variants. base o = SAVED PRODUCTION (state_mode production: no flags). Candidates = production + explicit changes.
ON='"a.AnimNode.OrientationWarping.Enable 1","a.AnimNode.StrideWarping.Enable 1","a.AnimNode.FootPlacement.Enable 1","a.AnimNode.LegIK.Enable 1"'
cand() { MODE[$1]=candidate; AF[$1]=""; [ -n "$2" ] && AF[$1]="\"abp_flags\":{$2}"; SX[$1]="{$3}"; CON[$1]="\"console\":[$ON"; [ -n "$4" ] && CON[$1]="${CON[$1]},$4"; CON[$1]="${CON[$1]}]"; PF[$1]="$5"; BF[$1]="$6"; }
# isolation of the sprint-reversal upper-body spin (V2.29 diag)
cand oOW  "" "" '"a.AnimNode.OrientationWarping.Enable 0"'
cand oSW  "" "" '"a.AnimNode.StrideWarping.Enable 0"'
cand oRAW "" "" '"a.AnimNode.FootPlacement.Enable 0","a.AnimNode.LegIK.Enable 0","a.AnimNode.StrideWarping.Enable 0","a.AnimNode.OrientationWarping.Enable 0"'
cand oPBI "" "" "" '"ProfileEnabled":false'
cand oSCR "" "" "" '"SpineCounterRotation":0.0'
cand oDR  "" "" "" '"EnableDirectionReaction":false'
# V2.29 candidates (after run229_build): effort, walk framing, release->re-press resume
EF='"EffortEnabled":true'
CW='"CamSwapMinSpeed":230.0,"CamFolDZLatWalk":3.0,"CamFolDZFwdWalk":4.0'
cand ef  ""                          "$EF"
cand cw  ""                          "$CW"
cand rs  '"SHM229_ResumeWin":0.2'    ""
cand all '"SHM229_ResumeWin":0.2'    "$EF,$CW"
EF2='"EffortEnabled":true,"EffortGain":1.6,"EffortTurnK":0.5,"EffortAccK":0.5,"EffortLoadK":0.6,"EffortTauRec":5.0'
EF3='"EffortEnabled":true,"EffortGain":2.4,"EffortTurnK":0.55,"EffortAccK":0.55,"EffortLoadK":0.7,"EffortTauRec":5.0'
cand ef2 "" "$EF2"
cand ef3 "" "$EF3"
cand all2 '"SHM229_ResumeWin":0.2' "$EF2,$CW"
