"""src240_cut.py (editor job, write manifest = the 48 V2.38 cut clips): add ONLY the V2.40 source-index curve SHM240_Src (R P00..P23 =
0..23, L P00..P23 = 24..47; constant) - the takeover entry picks the database of THIS source (install240_edb). Bone keys untouched.
Idempotent. builtins.V240_SRC = {'dry_run': bool}. Prints SRC240 {...}."""
import unreal as u, json, builtins
AL = u.AnimationLibrary; EAL = u.EditorAssetLibrary
DRY = bool(dict(getattr(builtins, 'V240_SRC', {})).get('dry_run', True))
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
out = {'errors': [], 'n': 0}
for sd, base in (('R', 0), ('L', 24)):
    for p in range(24):
        name = 'SHM238_Cut_%s_P%02d' % (sd, p)
        try:
            s = u.load_asset('/Game/GraceRanger/SHME/Animations/V238/' + name); ln = float(s.get_play_length()); v = float(base + p)
            if not DRY:
                if 'shm240_src' in [str(x).lower() for x in AL.get_animation_curve_names(s, u.RawCurveTrackTypes.RCT_FLOAT)]: AL.remove_curve(s, 'SHM240_Src', False)
                AL.add_curve(s, 'SHM240_Src', u.RawCurveTrackTypes.RCT_FLOAT, False); AL.add_float_curve_keys(s, 'SHM240_Src', [0.0, ln], [v, v])
                assert EAL.save_loaded_asset(s, False), name
            out['n'] += 1
        except Exception as e: out['errors'].append('%s: %s' % (name, str(e)[:160]))
out['ok'] = out['n'] == 48 and not out['errors']
print('SRC240 ' + json.dumps(out))
