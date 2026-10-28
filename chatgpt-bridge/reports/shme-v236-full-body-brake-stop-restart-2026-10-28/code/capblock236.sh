for c in S D G; do
  case $c in S) CAM=",$SIDE";; D) CAM=",$DIAG";; G) CAM="";; esac
  for v in ${CAPV4:-}; do [ -z "${MODE[$v]}" ] && continue
    bf="${BF[$v]}"; [ $c != G ] && bf="${bf/\"GR215_CamYawFromControl\":false/\"GR215_CamYawFromControl\":true}"
    MODE[$v$c]="${MODE[$v]}"; BF[$v$c]="$bf"; SX[$v$c]="${SX[$v]}"; AF[$v$c]="${AF[$v]:+${AF[$v]},}$CAP$CAM,$LIGHT,$LOOK,\"pie_window\":[1728,972]"
    CON[$v$c]="\"console\":[\"a.AnimNode.OrientationWarping.Enable 1\",\"a.AnimNode.StrideWarping.Enable 1\",\"a.AnimNode.FootPlacement.Enable 1\",\"a.AnimNode.LegIK.Enable 1\",\"t.MaxFPS 30\"]"
  done
done
