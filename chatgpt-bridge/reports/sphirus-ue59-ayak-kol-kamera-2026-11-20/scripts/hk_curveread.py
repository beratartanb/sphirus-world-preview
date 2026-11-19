# hk_curveread.py (read-only runtime probe): per frame movedata_speed of the driver pose + motion component BrakeDecel / ClipBrakeOn.
import builtins, unreal as u
def _cr_hook(pw, ai, st, w_):
    o = {'c': round(float(ai.get_curve_value('movedata_speed')), 1)}
    try:
        m = [c for c in pw.get_components_by_class(u.ActorComponent) if c.get_class().get_name().startswith('AC_Sph_Motion')][0]
        o['bd'] = round(float(m.get_editor_property('BrakeDecel'))); o['on'] = bool(m.get_editor_property('ClipBrakeOn'))
    except Exception as e: o['e'] = str(e)[:40]
    cm = pw.get_movement_component(); o['bdw'] = round(float(cm.get_editor_property('braking_deceleration_walking')))
    return o
builtins.VID_TICKHOOK = _cr_hook
