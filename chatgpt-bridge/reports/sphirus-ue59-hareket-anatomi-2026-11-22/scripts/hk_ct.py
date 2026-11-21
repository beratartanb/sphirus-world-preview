# hk_ct.py (prelude): hk_pose3 + contact-system log (row.hook.ct) + optional test obstacle spawned in the PIE world on the first tick.
# builtins.CT_SCENE = (kind, D[, extra]) relative to the pawn start, travel +x: 'wall' | 'waist' | 'knee' | 'graze' (wall beside, gap = extra cm)
# builtins.CT_FAT = value 0..1 -> energy E forced so the fatigue input is high (state factor test)
import builtins, unreal as _u2
exec(open(_u2.Paths.project_dir()+'Tools/UE59_20261122/hk_pose3.py',encoding='utf8').read())
_base=builtins.VID_TICKHOOK; _stt={'done':False}
_CT=('CT_State','CT_Class','CT_DB','CT_Prox','CT_Graze','CT_VnPrev','CT_LastS','CT_LastV','CT_LastC','CT_LastL','CT_Count','CT_LockT','CT_ReachA','CT_CapT')
def _hk2(pw, ai, st, w_):
    if not _stt['done']:
        _stt['done']=True; sc=getattr(builtins,'CT_SCENE',None)
        if sc:
            try:
                p0=pw.get_actor_location(); fz=p0.z-86.0; kind=sc[0]; D=float(sc[1]); ex=float(sc[2]) if len(sc)>2 else 6.0
                spec={'wall':((D+15,0,fz+150),(0.3,6,3)),'waist':((D+40,0,fz+52.5),(0.8,3,1.05)),'knee':((D+30,0,fz+30),(0.6,3,0.6)),'graze':((D,30+ex+15,fz+150),(14,0.3,3))}[kind]
                tf=_u2.Transform(location=_u2.Vector(p0.x+spec[0][0],p0.y+spec[0][1],spec[0][2]),rotation=_u2.Rotator(0,0,0),scale=_u2.Vector(*spec[1]))
                a=_u2.GameplayStatics.begin_deferred_actor_spawn_from_class(pw,_u2.StaticMeshActor,tf); a.set_mobility(_u2.ComponentMobility.MOVABLE)
                a.static_mesh_component.set_static_mesh(_u2.load_asset('/Engine/BasicShapes/Cube')); _u2.GameplayStatics.finish_spawning_actor(a,tf)
                _stt['scene']='%s at +%.0f'%(kind,D)
            except Exception as e: _stt['scene']='ERR '+repr(e)[:160]
    o=_base(pw, ai, st, w_)
    try:
        o['ct']=[round(float(pw.get_editor_property(n)),2) for n in _CT]
        m=[c for c in pw.get_components_by_class(_u2.ActorComponent) if c.get_name()=='SphMotion'][0]
        f=getattr(builtins,'CT_FAT',None)
        if f is not None:
            try: m.set_editor_property('Fat',float(f))
            except Exception as e: o['fatset']=repr(e)[:100]
        o['ctm']=[round(float(m.get_editor_property(n)),2) for n in ('CtCap','ReachA','CtA','Fat','E')]
        o['scene']=_stt.get('scene')
    except Exception as e: o['cterr']=repr(e)[:120]
    return o
builtins.VID_TICKHOOK=_hk2
