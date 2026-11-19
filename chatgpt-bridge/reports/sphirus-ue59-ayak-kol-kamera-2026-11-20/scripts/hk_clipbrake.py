# hk_clipbrake.py (in-memory runtime prototype): CLIP-BOUND STOP. While no move key is held, on the ground, no montage, the capsule
# speed is pulled down to the root speed of the animation actually playing (movedata_speed curve of the GASP driver pose, blended
# across the blend stack, x CBK). Never accelerates; the drop per frame is limited to CBMAX cm/s^2 so the release itself is not a
# snap. Movement direction is kept. Any move key / montage / air -> untouched (normal PhysBrake).
import builtins, unreal as u
builtins.CBK = getattr(builtins, 'CBK', 1.0); builtins.CBMAX = getattr(builtins, 'CBMAX', 4000.0)
def _cb_hook(pw, ai, st, w_):
    mv = any(k in st['down'] for k in ('W', 'A', 'S', 'D'))
    cm = pw.get_movement_component(); v = pw.get_velocity(); sp = (v.x * v.x + v.y * v.y) ** 0.5
    c = float(ai.get_curve_value('movedata_speed'))
    if mv or cm.is_falling() or ai.get_current_active_montage() is not None or sp < 1.0: return {'c': round(c), 'on': 0}
    dt = max(1e-3, u.GameplayStatics.get_world_delta_seconds(w_))
    tgt = max(min(sp, c * builtins.CBK), sp - builtins.CBMAX * dt)
    k = tgt / sp
    cm.set_editor_property('velocity', u.Vector(v.x * k, v.y * k, v.z), u.PropertyAccessChangeNotifyMode.NEVER)
    return {'c': round(c), 'on': 1, 'tgt': round(tgt)}
builtins.VID_TICKHOOK = _cb_hook
print('CBHOOK set')
