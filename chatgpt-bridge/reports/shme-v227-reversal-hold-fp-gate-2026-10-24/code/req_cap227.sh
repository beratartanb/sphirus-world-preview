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
