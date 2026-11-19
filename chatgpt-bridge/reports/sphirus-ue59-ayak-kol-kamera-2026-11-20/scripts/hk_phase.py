# hk_phase.py (read-only runtime probe): driver pose curves movedata_speed / phase / enable_warping per frame.
import builtins, unreal as u
def _ph_hook(pw, ai, st, w_):
    return {k: round(float(ai.get_curve_value(k)), 3) for k in ('movedata_speed', 'phase', 'enable_warping')}
builtins.VID_TICKHOOK = _ph_hook
