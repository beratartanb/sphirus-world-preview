import builtins, unreal as u
_prev=getattr(builtins,'VID_TICKHOOK',None)
def _hk2(pw, ai, st, w_):
    o=_prev(pw,ai,st,w_) if _prev else {}
    try:
        o['top']=[c.get_skeletal_mesh_asset().get_name() if c.get_skeletal_mesh_asset() else None for c in pw.get_components_by_class(u.SkeletalMeshComponent) if c.get_name() in ('Henley','Shorts')]
        o['groom']=[(c.get_name(),c.is_visible()) for c in pw.get_components_by_class(u.GroomComponent)][:3]
        h=[a for a in u.GameplayStatics.get_all_actors_of_class(w_,u.Actor) if a.get_class().get_name().startswith('BP_GR_DayHub')][0]
        o['days']=h.get_editor_property('GR_Days'); o['fireSt']=bool(h.get_editor_property('GR_FireSt').get_actor_enable_collision()) if h.get_editor_property('GR_FireSt') else None
    except Exception as e: o['oerr']=repr(e)[:80]
    return o
builtins.VID_TICKHOOK=_hk2
