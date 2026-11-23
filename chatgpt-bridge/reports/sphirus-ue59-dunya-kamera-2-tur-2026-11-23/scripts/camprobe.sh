#!/bin/bash
# camprobe.sh <tag> [views]: PIE, teleport to tight spots, read AC_Sph_Camera internal state and shoot from the gameplay camera.
P="<PROJECT_ROOT>"; cd "$P"; T=Tools/R2G2_20261123; STEP=$T/_step.py; O=emb
TAG=$1; VF=${2:-$T/views_tight.txt}; OUT=Saved/UE59Work/r2g/shots/$TAG; mkdir -p $OUT
J(){ printf "exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/h.py',encoding='utf8').read())\n%s\n" "$1" > $STEP; SHME_OWNER=$O SHME_KIND=${2:-measure} bash Tools/SHME_V2_20261014/run_v2.sh "$P/$STEP" r2g_s 60 2>&1 | grep -v "^OK " | tail -${3:-1} | cut -c1-420; }
W(){ timeout $1 cat /dev/zero >/dev/null 2>&1; }
USHA=$(sha1sum Saved/SaveGames/SFSaveSlot.sav | cut -c1-40); rm -f Saved/Screenshots/WindowsEditor/HighresScreenshot*.png
SHME_OWNER=$O SHME_KIND=pie bash Tools/SHME_V2_20261014/run_v2.sh "$P/Tools/SF52_20261105/pie_start.py" r2g_pie 60 2>&1 | tail -1 | cut -c1-40; W 10; SHME_OWNER=$O SHME_KIND=measure bash Tools/SHME_V2_20261014/run_v2.sh "$P/Tools/SF52_20261105/p0.py" r2g_p0 30 >/dev/null 2>&1; W 10
[ -n "$PRE" ] && { J "$PRE" measure 3; W 2; }
RD="c=[x for x in PW.get_components_by_class(u.ActorComponent) if x.get_class().get_name().startswith('AC_Sph_Camera')][0]; g=lambda k: round(float(c.get_editor_property(k)),2); cm=u.GameplayStatics.get_player_camera_manager(W,0); cl=cm.get_camera_location(); hd=PW.mesh.get_socket_location('head') if False else None; print('ST',' '.join('%s=%s'%(k,g(k)) for k in ('SafeFrac','L','Y','Z','D','Open','DBack','DBackR','DRight','DLeft','DUp','TRaiseA','Home','DbgShoulderD','DbgHeadX','DbgHeadY','Fov')),'cam',round(cl.x),round(cl.y),round(cl.z),'pawn',round(PW.get_actor_location().x),round(PW.get_actor_location().y),round(PW.get_actor_location().z))"
: > $OUT/state.txt
while read LB X Y YAW PITCH ZZ; do
  [ -z "$LB" ] && continue
  J "tp($X,$Y,$ZZ,$YAW,$PITCH); PW.set_actor_rotation(u.Rotator(pitch=0,yaw=$YAW,roll=0),False); print(1)" >/dev/null; W 6
  echo "$LB | $(J "$RD")" | tee -a $OUT/state.txt | cut -c1-330
  J "cmd('HighResShot 1600x900')" >/dev/null; W 4
  f=$(ls -t Saved/Screenshots/WindowsEditor/HighresScreenshot*.png 2>/dev/null | head -1); [ -n "$f" ] && mv "$f" $OUT/$LB.png
done < $VF
SHME_OWNER=$O SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$P/Tools/SF52_20261105/pie_stop.py" r2g_stop 90 2>&1 | tail -1 | cut -c1-30; W 4
h=$(sha1sum Saved/SaveGames/SFSaveSlot.sav | cut -c1-40); [ "$h" = "$USHA" ] && echo "SLOT_OK $h" || echo "SLOT_CHANGED $h"
