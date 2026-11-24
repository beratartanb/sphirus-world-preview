#!/bin/bash
# cr_tour2.sh <tag> [views] : PIE on the open map; per point: gameplay-camera still (g), face camera (f: 28 deg, 95 cm, 3/4 front) and
# full-body front camera (b: 40 deg, 330 cm). Temporary CameraActor in the PIE world only; scene lighting/post untouched. PRE = python run once.
P="/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; cd "$P"; STEP=Saved/UE59Work/cr1/_step.py; O=emb
TAG=$1; VF=${2:-Saved/UE59Work/cr1/views2.txt}; RES=${RES:-1600x900}; OUT=Saved/UE59Work/cr1/shots/$TAG; mkdir -p $OUT
J(){ printf "exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/h.py',encoding='utf8').read())\n%s\n" "$1" > $STEP; SHME_OWNER=$O SHME_KIND=${2:-measure} bash Tools/SHME_V2_20261014/run_v2.sh "$P/$STEP" cr_s 60 2>&1 | grep -v "^OK " | tail -${3:-1} | cut -c1-300; }
W(){ timeout $1 cat /dev/zero >/dev/null 2>&1; }
SHOT(){ J "cmd('HighResShot $RES')" >/dev/null; W 4; f=$(ls -t Saved/Screenshots/WindowsEditor/HighresScreenshot*.png 2>/dev/null | head -1); [ -n "$f" ] && mv "$f" $OUT/$1.png; }
CAM='import builtins
def _cam(d,rt,up,fov,tz):
    fc=[c for c in PW.get_components_by_class(u.SkeletalMeshComponent) if c.get_name()=="Face"][0]; hd=fc.get_socket_location("head"); f=PW.get_actor_forward_vector(); r=PW.get_actor_right_vector()
    tg=u.Vector(hd.x,hd.y,hd.z+tz); loc=u.Vector(tg.x+f.x*d+r.x*rt, tg.y+f.y*d+r.y*rt, tg.z+up); rot=u.MathLibrary.find_look_at_rotation(loc,tg)
    c=getattr(builtins,"CR_CAM",None)
    try: c.get_name()
    except Exception: c=None
    if c is None:
        cs=u.GameplayStatics.get_all_actors_of_class(W,u.CameraActor)
        if not cs: cmd("summon CameraActor"); cs=u.GameplayStatics.get_all_actors_of_class(W,u.CameraActor)
        print("CAMS",len(cs)); c=cs[0]; builtins.CR_CAM=c
        try: c.root_component.set_mobility(u.ComponentMobility.MOVABLE)
        except Exception as e: print("mob",e)
    c.set_actor_location_and_rotation(loc,rot,False,True); cc=c.get_component_by_class(u.CameraComponent); cc.set_editor_property("field_of_view",fov); cc.set_editor_property("constrain_aspect_ratio",False); cc.set_editor_property("post_process_blend_weight",0.0)
    PC.set_view_target_with_blend(c,0.0)'
USHA=$(sha1sum Saved/SaveGames/SFSaveSlot.sav | cut -c1-40); rm -f Saved/Screenshots/WindowsEditor/HighresScreenshot*.png
SHME_OWNER=$O SHME_KIND=pie bash Tools/SHME_V2_20261014/run_v2.sh "$P/Tools/SF52_20261105/pie_start.py" cr_pie 60 2>&1 | tail -1 | cut -c1-60; W 10; SHME_OWNER=$O SHME_KIND=measure bash Tools/SHME_V2_20261014/run_v2.sh "$P/Tools/SF52_20261105/p0.py" cr_p0 30 2>&1 | tail -1 | cut -c1-20; W 12
DOF0=$(J "print('DOF',u.SystemLibrary.get_console_variable_int_value('r.DepthOfFieldQuality'))" | grep -o "DOF [0-9]*" | cut -d' ' -f2); echo "dof was $DOF0"
[ -n "$PRE" ] && { J "$PRE" measure 3; W 3; }
while read LB X Y YAW PITCH ZZ KINDS; do
  [ -z "$LB" ] && continue
  J "tp($X,$Y,$ZZ,$YAW,$PITCH); PW.set_actor_rotation(u.Rotator(pitch=0,yaw=$YAW,roll=0),False); PC.set_view_target_with_blend(PW,0.0); print(1)" >/dev/null; W 6
  J "cmd('r.DepthOfFieldQuality ${DOF0:-2}')" >/dev/null
  case "$KINDS" in *g*) SHOT ${LB}_g;; esac
  J "cmd('r.DepthOfFieldQuality 0')" >/dev/null
  case "$KINDS" in *f*) J "$CAM
_cam(95.0,28.0,2.0,28.0,3.0); print(1)" >/dev/null; W 9; SHOT ${LB}_f;; esac
  case "$KINDS" in *s*) J "$CAM
_cam(8.0,100.0,0.0,28.0,2.0); print(1)" >/dev/null; W 3; SHOT ${LB}_s;; esac
  case "$KINDS" in *b*) J "$CAM
_cam(330.0,60.0,-10.0,40.0,-62.0); print(1)" >/dev/null; W 3; SHOT ${LB}_b;; esac
done < $VF
J "cmd('r.DepthOfFieldQuality ${DOF0:-2}')" >/dev/null
SHME_OWNER=$O SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$P/Tools/SF52_20261105/pie_stop.py" cr_stop 90 2>&1 | tail -1 | cut -c1-30; W 5
h=$(sha1sum Saved/SaveGames/SFSaveSlot.sav | cut -c1-40); [ "$h" = "$USHA" ] && echo "SLOT_OK $h" || echo "SLOT_CHANGED $h"; ls $OUT | tr '\n' ' '
