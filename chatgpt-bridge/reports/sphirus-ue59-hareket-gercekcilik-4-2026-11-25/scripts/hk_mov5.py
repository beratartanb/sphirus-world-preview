# hk_mov5.py (prelude): moves the PIE copy of the movable scene box (label B4_MOV*, placed by scene_place with flag 1) along x.
# builtins.MOV5 = (start_t, speed_x): from start_t (s after PIE start) the box moves at speed_x cm/s. row.hook.mov = [x, y].
import builtins, unreal as _u5
_b5 = builtins.VID_TICKHOOK; _s5 = {'a': None, 't': 0.0, 'look': False}
def _hk5(pw, ai, st, w_):
    o = _b5(pw, ai, st, w_)
    try:
        m = getattr(builtins, 'MOV5', None)
        if m and not _s5['look']:
            _s5['look'] = True
            for a in _u5.GameplayStatics.get_all_actors_of_class(pw, _u5.StaticMeshActor):
                if a.get_actor_label().startswith('B4_MOV'): _s5['a'] = a
        if m and _s5['a'] is not None:
            dt = 1.0 / 60.0
            try: dt = float(st.get('tstep', dt))
            except Exception: pass
            _s5['t'] += dt
            if _s5['t'] > m[0]:
                l = _s5['a'].get_actor_location(); _s5['a'].set_actor_location(_u5.Vector(l.x + m[1] * dt, l.y, l.z), False, False)
            l = _s5['a'].get_actor_location(); o['mov'] = [round(l.x, 1), round(l.y, 1)]
        elif m: o['moverr'] = 'no B4_MOV actor in PIE'
    except Exception as e: o['moverr'] = repr(e)[:160]
    return o
builtins.VID_TICKHOOK = _hk5
