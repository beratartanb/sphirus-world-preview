# hk_tele5.py (prelude, read-only; appended after the recorder hook): versioned, NAME-BASED telemetry, schema 'sph-tele/5.1'.
# row.hook.tele = {'schema', 'scene', 'frame', 'gt' (game time), 'rt' (real time), 'input': raw move input + gait keys,
#                  'speed', 'accel', 'clip', 'clip_t', 'mont', 'f': {player / motion property name: value}}
# builtins.TELE_FIELDS = player property names; builtins.TELE_MFIELDS = AC_Sph_Motion property names; builtins.TELE_SCENE = scene id.
# A field that cannot be read is stored as the string 'ERR:<reason>' (never silently 0).
import builtins, time, unreal as _ut
_bt = builtins.VID_TICKHOOK; _st = {'f': 0, 'v': None, 't0': time.time()}
def _tv(v):
    if isinstance(v, bool) or v is None: return v
    if isinstance(v, (int, float)): return round(float(v), 4)
    if isinstance(v, _ut.Vector): return [round(v.x, 2), round(v.y, 2), round(v.z, 2)]
    return str(v)[-80:]
def _hkt(pw, ai, st, w_):
    o = _bt(pw, ai, st, w_); _st['f'] += 1
    try:
        m = [c for c in pw.get_components_by_class(_ut.ActorComponent) if c.get_name() == 'SphMotion']; m = m[0] if m else None
        v = pw.get_velocity(); sp = (v.x * v.x + v.y * v.y) ** 0.5; dt = float(st.get('tstep', 1 / 60.0)) if isinstance(st, dict) else 1 / 60.0
        acc = (sp - _st['v']) / max(dt, 1e-3) if _st['v'] is not None else 0.0; _st['v'] = sp
        f = {}
        for n in (getattr(builtins, 'TELE_FIELDS', None) or ()):
            try: f[n] = _tv(pw.get_editor_property(n))
            except Exception as e: f[n] = 'ERR:' + type(e).__name__
        for n in (getattr(builtins, 'TELE_MFIELDS', None) or ()):
            try: f['M.' + n] = _tv(m.get_editor_property(n))
            except Exception as e: f['M.' + n] = 'ERR:' + type(e).__name__
        clip = None; ct = None
        try: clip = str(ai.get_editor_property('CurrentSelectedAnim').get_name()); ct = round(float(ai.get_editor_property('SphSelTime')), 3)
        except Exception: pass
        ri = pw.get_editor_property('GR_RawIn')
        o['tele'] = {'schema': 'sph-tele/5.1', 'scene': getattr(builtins, 'TELE_SCENE', None), 'frame': _st['f'], 'gt': round(float(st.get('tg', 0.0)) if isinstance(st, dict) else 0.0, 4),
                     'rt': round(time.time() - _st['t0'], 4), 'input': [round(ri.x, 3), round(ri.y, 3), int(pw.get_editor_property('GR_Gait')), int(pw.get_editor_property('GR_Pace'))],
                     'speed': round(sp, 2), 'accel': round(acc, 1), 'clip': clip, 'clip_t': ct, 'f': f}
    except Exception as e: o['tele'] = {'schema': 'sph-tele/5.1', 'error': repr(e)[:160]}
    return o
builtins.VID_TICKHOOK = _hkt
