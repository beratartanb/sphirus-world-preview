# hk_mask5.py (prelude): hk_pose3 + mask inspection log: camera context target / chest / side, the mask bench's components and the
# visible head + hand positions (row.hook.mk).
import builtins, unreal as _u3
exec(open(_u3.Paths.project_dir()+'Tools/UE59_20261122/hk_pose3.py',encoding='utf8').read())
_base3=builtins.VID_TICKHOOK; _mk={}
def _r(v): return [round(v.x,1),round(v.y,1),round(v.z,1)]
def _hk3(pw, ai, st, w_):
    o=_base3(pw, ai, st, w_)
    try:
        d={}
        cam=[c for c in pw.get_components_by_class(_u3.ActorComponent) if c.get_name()=='SphCamera' or c.get_class().get_name().startswith('AC_Sph_Camera')]
        if cam:
            c=cam[0]
            for n in ('CtxTarget','Chest','HeadF','CamW','AimW','Axis'):
                try: d[n]=_r(c.get_editor_property(n))
                except Exception as e: d[n]=repr(e)[:40]
            for n in ('CtxSide','WB','WS','WH','WW','CtxKind'):
                try: d[n]=round(float(c.get_editor_property(n)),2)
                except Exception as e: d[n]=repr(e)[:40]
        if 'bench' not in _mk:
            _mk['bench']=[a for a in _u3.GameplayStatics.get_all_actors_of_class(pw,_u3.Actor) if a.get_class().get_name()=='BP_GR_MaskBench_C']
        if _mk['bench']:
            b=_mk['bench'][0]; d['bench']=_r(b.get_actor_location())
            d['comps']={c.get_name():_r(c.get_world_location()) for c in b.get_components_by_class(_u3.StaticMeshComponent)}
        k={c.get_name():c for c in pw.get_components_by_class(_u3.SkeletalMeshComponent)}; vis=k.get('Manny')
        d['head']=_r(vis.get_socket_location('head')); d['hand_r']=_r(vis.get_socket_location('hand_r')); d['hand_l']=_r(vis.get_socket_location('hand_l'))
        d['att']=[(a.get_name()[:24],_r(a.get_actor_location())) for a in pw.get_attached_actors()][:4]
        o['mk']=d
    except Exception as e: o['mkerr']=repr(e)[:160]
    return o
builtins.VID_TICKHOOK=_hk3
