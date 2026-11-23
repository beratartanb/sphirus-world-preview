#!/bin/bash
# tour_r2g.sh <tag> [views file] [WxH]: PIE on the open map, teleport the real player to fixed points, HighResShot from the GAMEPLAY camera,
# real frame time per point. Copy of Tools/AAAEnv_20261111/tour.sh with lock owner emb and output under Saved/UE59Work/r2g/shots/<tag>.
# Teleported stills prove framing/look at a point only; they are not movement evidence.
P="<proje>/sphirus_UE59"; cd "$P"; T=Tools/R2G_20261123; STEP=$T/_step.py; O=emb
TAG=$1; VF=${2:-$T/views_slice.txt}; RES=${3:-1600x900}; OUT=Saved/UE59Work/r2g/shots/$TAG; mkdir -p $OUT
J(){ printf "exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/h.py',encoding='utf8').read())\n%s\n" "$1" > $STEP; SHME_OWNER=$O SHME_KIND=${2:-measure} bash Tools/SHME_V2_20261014/run_v2.sh "$P/$STEP" r2g_s 60 2>&1 | grep -v "^OK " | tail -${3:-1} | cut -c1-300; }
W(){ timeout $1 cat /dev/zero >/dev/null 2>&1; }
USHA=$(sha1sum Saved/SaveGames/SFSaveSlot.sav | cut -c1-40)
rm -f Saved/Screenshots/WindowsEditor/HighresScreenshot*.png
SHME_OWNER=$O SHME_KIND=pie bash Tools/SHME_V2_20261014/run_v2.sh "$P/Tools/SF52_20261105/pie_start.py" r2g_pie 60 2>&1 | tail -1 | cut -c1-60; W 10; SHME_OWNER=$O SHME_KIND=measure bash Tools/SHME_V2_20261014/run_v2.sh "$P/Tools/SF52_20261105/p0.py" r2g_p0 30 2>&1 | tail -1 | cut -c1-20; W 12
[ -n "$PRE" ] && { J "$PRE" measure 3; W 3; }
: > $OUT/perf.txt
while read LB X Y YAW PITCH ZZ; do
  [ -z "$LB" ] && continue
  J "tp($X,$Y,$ZZ,$YAW,$PITCH); print(1)" >/dev/null
  W 6
  A=$(J "import time; print('F',u.SystemLibrary.get_frame_count(),time.time())"); W 4; B=$(J "import time; cm=u.GameplayStatics.get_player_camera_manager(W,0); c=cm.get_camera_location(); r=cm.get_camera_rotation(); l=PW.get_actor_location(); print('F',u.SystemLibrary.get_frame_count(),time.time(),'CAM',round(c.x),round(c.y),round(c.z),round(r.yaw),round(r.pitch),'FOV',round(cm.get_fov_angle(),1),'PAWN',round(l.x),round(l.y),round(l.z))")
  echo "$LB | $A | $B" >> $OUT/perf.txt
  J "cmd('HighResShot $RES')" >/dev/null; W 4
  f=$(ls -t Saved/Screenshots/WindowsEditor/HighresScreenshot*.png 2>/dev/null | head -1); [ -n "$f" ] && mv "$f" $OUT/$LB.png
done < $VF
SHME_OWNER=$O SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$P/Tools/SF52_20261105/pie_stop.py" r2g_stop 90 2>&1 | tail -1 | cut -c1-30; W 5
h=$(sha1sum Saved/SaveGames/SFSaveSlot.sav | cut -c1-40); [ "$h" = "$USHA" ] && echo "SLOT_OK $h" || echo "SLOT_CHANGED $h"
"/c/Program Files/Epic Games/UE_5.9/Engine/Binaries/ThirdParty/Python3/Win64/python.exe" - $OUT/perf.txt <<'PY'
import sys
for l in open(sys.argv[1]):
    p=l.split('|'); a=p[1].split(); b=p[2].split()
    try:
        fps=(int(b[1])-int(a[1]))/(float(b[2])-float(a[2])); print('%-20s fps %5.1f ms %5.1f  %s'%(p[0].strip(),fps,1000/fps,' '.join(b[3:])))
    except Exception as e: print(l.strip()[:200],e)
PY
ls $OUT | wc -l
