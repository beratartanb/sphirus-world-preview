#!/bin/bash
# res_r2g.sh <tag>: existing resonance state on the R04-like view: normal -> resonance held (ResTarget 1, ResHoldT 6 s on the pawn's AC_Sph_Camera) -> back.
# Calls the EXISTING AC_Sph_Camera.ResPulse(1.0, 7 s) by hand in PIE; this is not the story trigger and adds no rule.
P="<proje>/sphirus_UE59"; cd "$P"; T=Tools/R2G_20261123; STEP=$T/_step.py; O=emb; OUT=Saved/UE59Work/r2g/shots/$1; mkdir -p $OUT
J(){ printf "exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/h.py',encoding='utf8').read())\n%s\n" "$1" > $STEP; SHME_OWNER=$O SHME_KIND=measure bash Tools/SHME_V2_20261014/run_v2.sh "$P/$STEP" r2g_s 60 2>&1 | grep -v "^OK " | tail -1 | cut -c1-300; }
W(){ timeout $1 cat /dev/zero >/dev/null 2>&1; }
S(){ J "cmd('HighResShot 1600x900')" >/dev/null; W 4; f=$(ls -t Saved/Screenshots/WindowsEditor/HighresScreenshot*.png 2>/dev/null | head -1); [ -n "$f" ] && mv "$f" $OUT/$1.png; }
RD="c=[x for x in PW.get_components_by_class(u.ActorComponent) if x.get_class().get_name().startswith('AC_Sph_Camera')][0]; print('RES',round(c.get_editor_property('Res'),3),'target',c.get_editor_property('ResTarget'),'hold',round(c.get_editor_property('ResHoldT'),2),'pawn',[round(v) for v in (PW.get_actor_location().x,PW.get_actor_location().y)],'yaw',round(PC.get_control_rotation().yaw))"
USHA=$(sha1sum Saved/SaveGames/SFSaveSlot.sav | cut -c1-40); rm -f Saved/Screenshots/WindowsEditor/HighresScreenshot*.png
SHME_OWNER=$O SHME_KIND=pie bash Tools/SHME_V2_20261014/run_v2.sh "$P/Tools/SF52_20261105/pie_start.py" r2g_pie 60 2>&1 | tail -1 | cut -c1-40; W 10
SHME_OWNER=$O SHME_KIND=measure bash Tools/SHME_V2_20261014/run_v2.sh "$P/Tools/SF52_20261105/p0.py" r2g_p0 30 >/dev/null 2>&1; W 10
J "h=u.SystemLibrary.line_trace_single(W,u.Vector(1450,3000,6000),u.Vector(1450,3000,-3000),u.TraceTypeQuery.TRACE_TYPE_QUERY1,False,[PW],u.DrawDebugTrace.NONE,True); z=h.to_tuple()[4].z; tp(1450,3000,z+100,225,-4); PW.set_actor_rotation(u.Rotator(pitch=0,yaw=225,roll=0),False); print(1)" >/dev/null; W 6
J "$RD"; S 1_normal
J "c=[x for x in PW.get_components_by_class(u.ActorComponent) if x.get_class().get_name().startswith('AC_Sph_Camera')][0]; c.call_method('ResPulse',(1.0,7.0)); print('PULSE')"; W 1
J "$RD"; S 2_entering_1s; W 2; J "$RD"; S 3_resonance_held
W 9; J "$RD"; S 4_back_normal
SHME_OWNER=$O SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$P/Tools/SF52_20261105/pie_stop.py" r2g_stop 90 2>&1 | tail -1 | cut -c1-30
h=$(sha1sum Saved/SaveGames/SFSaveSlot.sav | cut -c1-40); [ "$h" = "$USHA" ] && echo "SLOT_OK $h" || echo "SLOT_CHANGED $h"; ls $OUT
