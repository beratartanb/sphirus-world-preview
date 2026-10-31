#!/bin/bash
# media_xr2.sh [cine] : normal-speed route videos (30 FPS fixed-step capture played at 30 = real speed; same frame number = same game time).
#   XR2_route<A|B>_before_vs_after_clay_vs_lit.avi : BEFORE lit | AFTER clay (NEUTRAL light) | AFTER lit, each scaled 0.4, side by side
#   XR2_routeA_after_cinematic.avi (arg 'cine')    : AFTER + dress (path soil, glade stand) under the TRIAL2 light, scaled 0.6
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"
SC="/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/xr2"
PY="/c/Program Files/Blender Foundation/Blender 5.2/5.2/python/bin/python.exe"; O=Saved/Codex/ExteriorWorld_XR2_20261031/video; mkdir -p $O
TRI="Tools/AIToolingEval_20261031/triptych.ps1"
if [ "$1" = cine ]; then
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File $TRI -Base "$(cygpath -w $SC)" -Clip frames -Out "$(cygpath -w $SC/tri_cine)" -Scale 0.6 -Sets "walk_after_A_cine" -Names "AFTER + giydirme, sinematik isik onerisi (TRIAL2)" | tail -1
  "$PY" Tools/SHME_V29_20261016/mjpeg_avi.py $SC/tri_cine $O/XR2_routeA_after_cinematic.avi 30 | tail -1; exit 0
fi
for r in A B; do
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File $TRI -Base "$(cygpath -w $SC)" -Clip frames -Out "$(cygpath -w $SC/tri_$r)" -Scale 0.4 \
     -Sets "walk_before_${r}_lit,walk_after_${r}_clay,walk_after_${r}_lit" -Names "BEFORE isikli,AFTER kil (notr isik),AFTER isikli" | tail -1
  "$PY" Tools/SHME_V29_20261016/mjpeg_avi.py $SC/tri_$r $O/XR2_route${r}_before_vs_after_clay_vs_lit.avi 30 | tail -1
done
ls -la $O
