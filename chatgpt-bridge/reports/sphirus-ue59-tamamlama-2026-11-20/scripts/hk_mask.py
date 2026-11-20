import builtins, unreal as u
_prev=getattr(builtins,'VID_TICKHOOK',None)
def _hk3(pw, ai, st, w_):
    o=_prev(pw,ai,st,w_) if _prev else {}
    try:
        m=[a for a in u.GameplayStatics.get_all_actors_of_class(w_,u.Actor) if a.get_class().get_name().startswith('BP_GR_MaskBench')][0]
        sm=m.get_editor_property('StaticMesh'); p=sm.get_world_location(); hr=pw.get_components_by_class(u.SkeletalMeshComponent)
        body=[c for c in hr if c.get_name()=='Manny'][0]; h=body.get_socket_location('hand_r')
        o['mk']=[m.get_editor_property('GR_P'),m.get_editor_property('GR_Stage'),bool(m.get_editor_property('GR_Held')),round(p.x,1),round(p.y,1),round(p.z,1),round(((p.x-h.x)**2+(p.y-h.y)**2+(p.z-h.z)**2)**0.5,1),sm.get_attach_parent().get_name() if sm.get_attach_parent() else None]
    except Exception as e: o['mkerr']=repr(e)[:100]
    return o
builtins.VID_TICKHOOK=_hk3
