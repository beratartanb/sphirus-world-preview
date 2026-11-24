# hk_rear9.py (prelude, read-only for the game): hk_pose3 + a fixed rear full-body camera for house-map recordings.
# builtins.REAR=(back_cm, side_cm, up_cm, fov): an existing level CameraActor of the PIE world is moved behind the start pose once and
# becomes the view target (the player camera logic keeps running). PIE world only; nothing is saved.
import builtins, unreal as _ur, math as _m
exec(open(_ur.Paths.project_dir()+'Tools/UE59_20261122/hk_pose3.py',encoding='utf8').read())
_bR=builtins.VID_TICKHOOK; _sR={'n':0}
def _hkR(pw, ai, st, w_):
    o=_bR(pw, ai, st, w_); rr=getattr(builtins,'REAR',None)
    if rr and _sR['n']<3:
        _sR['n']+=1
        try:
            pc=_ur.GameplayStatics.get_player_controller(w_,0); c=_ur.GameplayStatics.get_all_actors_of_class(w_,_ur.CameraActor)[0]
            if _sR['n']==1:
                try: c.root_component.set_mobility(_ur.ComponentMobility.MOVABLE)
                except Exception: pass
                l=pw.get_actor_location(); y=_m.radians(pw.get_actor_rotation().yaw); f=(_m.cos(y),_m.sin(y)); r=(-_m.sin(y),_m.cos(y))
                loc=_ur.Vector(l.x-f[0]*rr[0]+r[0]*rr[1], l.y-f[1]*rr[0]+r[1]*rr[1], l.z+rr[2]); tg=_ur.Vector(l.x+f[0]*350, l.y+f[1]*350, l.z-10)
                c.set_actor_location_and_rotation(loc,_ur.MathLibrary.find_look_at_rotation(loc,tg),False,True)
                cc=c.get_component_by_class(_ur.CameraComponent); cc.set_editor_property('field_of_view',rr[3]); cc.set_editor_property('constrain_aspect_ratio',False); cc.set_editor_property('post_process_blend_weight',0.0)
            pc.set_view_target_with_blend(c,0.0)
        except Exception as e: o['rearerr']=repr(e)[:120]
    return o
builtins.VID_TICKHOOK=_hkR
