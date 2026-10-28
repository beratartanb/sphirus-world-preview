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
