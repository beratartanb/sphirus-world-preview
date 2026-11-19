# hk_rmstop.py (in-memory runtime experiment): while no move key is held, the pawn is on the ground, no montage plays and the
# capsule still moves, the GASP anim instance runs RootMotionFromEverything so the stop clip's own root motion moves the
# capsule (planted foot stays where the clip puts it). Any move key / montage / air -> the original mode.
import builtins, unreal as u
builtins._RMKEYS = ('W', 'A', 'S', 'D')
def _rm_hook(pw, ai, st, w_):
    if not hasattr(builtins, '_RM0'): builtins._RM0 = ai.get_editor_property('root_motion_mode')
    mv = any(k in st['down'] for k in builtins._RMKEYS)
    v = pw.get_velocity(); sp = (v.x * v.x + v.y * v.y) ** 0.5
    cm = pw.get_movement_component(); mont = ai.get_current_active_montage()
    on = (not mv) and (not cm.is_falling()) and mont is None and (sp > 1.0 or st.get('rmon', False) and sp > 0.2)
    st['rmon'] = on
    want = u.RootMotionMode.ROOT_MOTION_FROM_EVERYTHING if on else builtins._RM0
    if ai.get_editor_property('root_motion_mode') != want: ai.set_root_motion_mode(want)
    return {'rm': int(on)}
builtins.VID_TICKHOOK = _rm_hook
print('RMHOOK set')
