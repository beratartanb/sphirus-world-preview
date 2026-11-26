# hk_imp.py (prelude): impact test driver. builtins.IMP_PLAN = [(t, sim_root, hit_bone, all_below 0/1, (fwd, right, up) velocity change cm/s)]
# in the pawn frame (a 3-tuple (t, bone, vec) = sim root and hit bone the same, all bodies);
# at game time t (from the first tick) it writes IMP_Bone / IMP_Imp / IMP_Fire on the pawn (BP_HybridA_Player tick applies the hit).
# Row hook gets 'imp' = [IMP_Act, IMP_W, IMP_T] and 'impn' = index of the last fired hit.
import builtins, unreal as _u3
_bimp = builtins.VID_TICKHOOK; _si = {'t0': None, 'n': 0}
def _hki(pw, ai, st, w_):
    t = _u3.GameplayStatics.get_time_seconds(w_)
    if _si['t0'] is None: _si['t0'] = t
    tt = t - _si['t0']; P = getattr(builtins, 'IMP_PLAN', None) or []
    if _si['n'] < len(P) and tt >= P[_si['n']][0]:
        e = P[_si['n']]; e = e if len(e) == 5 else (e[0], e[1], e[1], 1, e[2]); _, sb, b, al, (a, r, z) = e; f = pw.get_actor_forward_vector(); rv = pw.get_actor_right_vector()
        v = _u3.Vector(f.x * a + rv.x * r, f.y * a + rv.y * r, f.z * a + rv.z * r + z)
        N = _u3.PropertyAccessChangeNotifyMode.NEVER
        pw.set_editor_property('IMP_Bone', b, N); pw.set_editor_property('IMP_SimB', sb, N); pw.set_editor_property('IMP_All', float(al), N); pw.set_editor_property('IMP_Imp', v, N); pw.set_editor_property('IMP_Fire', 1.0, N); _si['n'] += 1
    F = getattr(builtins, 'FL_PLAN', None) or []
    if _si.get('fn', 0) < len(F) and tt >= F[_si.get('fn', 0)][0]:
        _, (a, r, z) = F[_si.get('fn', 0)]; f = pw.get_actor_forward_vector(); rv = pw.get_actor_right_vector(); N = _u3.PropertyAccessChangeNotifyMode.NEVER
        pw.set_editor_property('FL_Imp', _u3.Vector(f.x * a + rv.x * r, f.y * a + rv.y * r, f.z * a + rv.z * r + z), N); pw.set_editor_property('FL_Fire', 1.0, N); _si['fn'] = _si.get('fn', 0) + 1
    o = _bimp(pw, ai, st, w_)
    try:
        o['imp'] = [round(float(pw.get_editor_property(k)), 3) for k in ('IMP_Act', 'IMP_W', 'IMP_T')]; o['impn'] = _si['n']; o['fl'] = [round(float(pw.get_editor_property(k)), 3) for k in ('FL_State', 'FL_T', 'FL_Still', 'FL_W', 'FL_Tries', 'FL_Prone')]; o['tt'] = round(tt, 3)
        m_ = pw.mesh; vw = [c for c in pw.get_components_by_class(_u3.SkeletalMeshComponent) if c.get_name() == 'Manny'][0]
        o['mw'] = [[round(v, 1) for v in (m_.get_world_location().x, m_.get_world_location().y, m_.get_world_location().z)], round(m_.get_world_rotation().yaw, 1), [round(v, 1) for v in (m_.relative_location.x, m_.relative_location.y, m_.relative_location.z)], [round(v, 1) for v in (vw.get_world_location().x, vw.get_world_location().y, vw.get_world_location().z)], str(pw.character_movement.movement_mode)[-12:]]
    except Exception as e: o['imperr'] = repr(e)[:100]
    return o
builtins.VID_TICKHOOK = _hki
