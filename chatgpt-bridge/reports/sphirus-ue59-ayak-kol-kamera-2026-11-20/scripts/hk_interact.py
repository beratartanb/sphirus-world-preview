# hk_interact.py (read-only runtime probe): interaction truth per frame. SFInteractionManager_AC (TargetInteractionActor, CanInteract),
# day hub (Tea/Woke/Fire*/Steam/Busy/DoorOpen), GenericDoor 'IsOpen?' + leaf yaw within 4 m, mask bench GR_Stage/Mode/Done/Held,
# active montage. First frame: row['hook']['ia_list'] = labels+classes of every InteractableBase_BP child in the world.
import builtins, unreal as u
def _g(o, k):
    try:
        v = o.get_editor_property(k)
        return v if isinstance(v, (bool, int, str)) else (round(float(v), 2) if isinstance(v, float) else (v.get_actor_label() if hasattr(v, 'get_actor_label') else str(v)[:40]))
    except Exception: return '?'
def _ia_hook(pw, ai, st, w_):
    o = {}
    if getattr(builtins, '_IA_W', None) is not w_ or st['f'] == 0:
        builtins._IA_W = w_; A = u.GameplayStatics.get_all_actors_of_class(w_, u.Actor)
        builtins._IA_HUB = [a for a in A if a.get_class().get_name().startswith('BP_GR_DayHub')]
        builtins._IA_DOORS = [a for a in A if a.get_class().get_name().startswith('GenericDoor_BP')]
        builtins._IA_MASK = [a for a in A if a.get_class().get_name().startswith('BP_GR_MaskBench')]
        def _isia(c):
            while c is not None:
                if c.get_name() == 'InteractableBase_BP_C': return True
                try: c = c.get_super_class()
                except Exception: return False
            return False
        o['ia_list'] = sorted('%s|%s' % (a.get_actor_label(), a.get_class().get_name()) for a in A if _isia(a.get_class()))
    pc = u.GameplayStatics.get_player_controller(w_, 0)
    for owner in (pc, pw):
        for c in owner.get_components_by_class(u.ActorComponent):
            if c.get_class().get_name().startswith('SFInteractionManager'):
                o['tgt'] = _g(c, 'TargetInteractionActor'); o['can'] = _g(c, 'CanInteract'); o['act'] = _g(c, 'IsPerfomingAction')
    if builtins._IA_HUB:
        h = builtins._IA_HUB[0]
        for k in ('GR_Tea', 'GR_Woke', 'GR_Fire', 'GR_FireOn', 'GR_FireLit', 'GR_SteamOn', 'GR_Busy', 'GR_DoorOpen', 'GR_Outfit', 'GR_Herb'):
            o[k[3:]] = _g(h, k)
    p = pw.get_actor_location()
    for d in builtins._IA_DOORS:
        q = d.get_actor_location()
        if ((q.x - p.x) ** 2 + (q.y - p.y) ** 2 + (q.z - p.z) ** 2) ** 0.5 < 400:
            o['door_' + d.get_actor_label()[9:]] = [_g(d, 'IsOpen?')] + [round(c.get_editor_property('relative_rotation').yaw, 1) for c in d.get_components_by_class(u.StaticMeshComponent)][:3]
    for m in builtins._IA_MASK:
        o['mask'] = [_g(m, k) for k in ('GR_Stage', 'GR_Mode', 'GR_Done', 'GR_Held', 'GR_FinishedMask')]
    return o
builtins.VID_TICKHOOK = _ia_hook
