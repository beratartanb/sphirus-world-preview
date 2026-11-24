#!/bin/bash
# hair_ab.sh: one PIE session; frame rate with hair simulation OFF, then ON with the candidate config (PIE pawn only), alternating twice.
source "<PROJECT>/Tools/VF2B_20261125/lib.sh"
CFG=$(cat ${1:-Tools/VF2B_20261125/hair_h6_cfg.txt})
FPS(){ A=$(J "import time; print('F',u.SystemLibrary.get_frame_count(),time.time())"); W 6; B=$(J "import time; print('F',u.SystemLibrary.get_frame_count(),time.time())"); echo "$1 $A $B" | awk '{printf "%s fps %.1f\n",$1,($6-$3)/($7-$4)}'; }
PIE_ON
J "tp(850,2080,90,90,-6); PW.set_actor_rotation(u.Rotator(pitch=0,yaw=90,roll=0),False); print(1)" >/dev/null; W 6
FPS off1
J "$CFG
exec(open(u.Paths.project_dir()+'Tools/VF2_20261124/hair_pie_apply.py',encoding='utf8').read())" measure 2; W 6
FPS on1
J "c=[x for x in PW.get_components_by_class(u.GroomComponent) if x.get_name().startswith('HairMain2')][0]; c.set_enable_simulation(False); print('off')" >/dev/null; W 4
FPS off2
J "c=[x for x in PW.get_components_by_class(u.GroomComponent) if x.get_name().startswith('HairMain2')][0]; c.set_enable_simulation(True); print('on')" >/dev/null; W 4
FPS on2
PIE_OFF
