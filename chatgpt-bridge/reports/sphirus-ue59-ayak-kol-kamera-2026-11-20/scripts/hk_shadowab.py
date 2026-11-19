# hk_shadowab.py (runtime A/B, console only): alternates r.Shadow.Virtual.ResolutionLodBiasDirectional between -1.5 (Epic) and
# 0.0 (project) every SBN frames, starting with -1.5; row['hook'] = {'sb': value in effect}. The last value is restored to 0.0
# (project setting) by the sequence after the run.
import builtins, unreal as u
builtins.SBN = getattr(builtins, 'SBN', 45)
def _sb_hook(pw, ai, st, w_):
    b = -1.5 if (st['f'] // builtins.SBN) % 2 == 0 else 0.0
    if st.get('sb') != b:
        u.SystemLibrary.execute_console_command(w_, 'r.Shadow.Virtual.ResolutionLodBiasDirectional %s' % b); st['sb'] = b
    return {'sb': b}
builtins.VID_TICKHOOK = _sb_hook
