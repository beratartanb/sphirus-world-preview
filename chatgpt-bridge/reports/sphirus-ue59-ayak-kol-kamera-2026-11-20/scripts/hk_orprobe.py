# hk_orprobe.py (read-only runtime probe): per frame OffsetRootBoneEnabled / OffsetRootTranslationRadius of the GASP ABP and the
# DDCvar.OffsetRootBone.* console variables. Optional builtins.ORSET = dict(prop=value) applied each frame (in-memory candidate).
import builtins, unreal as u
def _or_hook(pw, ai, st, w_):
    for k, v in (getattr(builtins, 'ORSET', None) or {}).items():
        try: ai.set_editor_property(k, v, u.PropertyAccessChangeNotifyMode.NEVER)
        except Exception: pass
    o = {}
    for k in ('OffsetRootBoneEnabled', 'OffsetRootTranslationRadius'):
        try: v = ai.get_editor_property(k); o[k[10:14] if k.startswith('OffsetRoot') else k] = (round(float(v), 1) if not isinstance(v, bool) else v)
        except Exception as e: o[k] = str(e)[:40]
    if st['f'] % 30 == 0:
        for c in ('DDCvar.OffsetRootBone.TranslationRadius', 'DDCvar.OffsetRootBone.Enable'):
            try: o[c[22:]] = u.SystemLibrary.get_console_variable_float_value(c)
            except Exception as e: o[c[22:]] = 'x'
    return o
builtins.VID_TICKHOOK = _or_hook
print('ORHOOK set')
