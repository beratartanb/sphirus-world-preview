"""step239_cut.py (editor job, write manifest = the 48 V2.38 cut clips): add ONLY the V2.39 contact-clock curves SHM239_Step (+ SHM239_StepN, the last contact a takeover exists for) to the
production cut clips (bone keys untouched): value = number of planned touchdowns at or before each frame (from gen238_cut_write.json,
the plan these clips were generated from), keyed every frame. The ABP takeover switch fires on its rising edge = the exact planned
touchdown (the component's ContactL/R heel-strike flags lag it by ~0.1 s, v238fin4_j38_c90r). Idempotent (replaces the curve).
builtins.V239_STEP = {'dry_run': bool}. Prints STEP239 {...}."""
import unreal as u, json, builtins, pathlib
P = pathlib.Path(u.Paths.project_dir()).resolve(); AL = u.AnimationLibrary; EAL = u.EditorAssetLibrary
cfg = dict(getattr(builtins, 'V239_STEP', {})); DRY = bool(cfg.get('dry_run', True))
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
J = json.loads((P / 'Saved/Codex/SHME_V238_20261030/gen238_cut_write.json').read_text())['clips']
out = {'clips': {}, 'errors': []}
for name, c in sorted(J.items()):
    path = '/Game/GraceRanger/SHME/Animations/V238/' + name
    try:
        seq = u.load_asset(path); n = int(c['frames']); DT = 1.0 / 30.0
        ts = [f * DT for f in range(n)]; vals = [float(sum(1 for k in c['contacts'] if k['t'] <= f * DT + 1e-6)) for f in range(n)]
        pl = float(seq.get_play_length()); assert abs(pl - (n - 1) * DT) < 0.02, (pl, n)
        out['clips'][name] = [vals[0], vals[-1], [round(k['t'], 3) for k in c['contacts']]]
        if not DRY:
            names = [str(x) for x in AL.get_animation_curve_names(seq, u.RawCurveTrackTypes.RCT_FLOAT)]
            if 'SHM239_Step' in names: AL.remove_curve(seq, 'SHM239_Step', False)
            AL.add_curve(seq, 'SHM239_Step', u.RawCurveTrackTypes.RCT_FLOAT, False); AL.add_float_curve_keys(seq, 'SHM239_Step', ts, vals)
            if 'SHM239_StepN' in names: AL.remove_curve(seq, 'SHM239_StepN', False)
            nk = float(len(c['contacts']) - 1)                       # takeovers exist for contacts 1 .. n-1 (gen239_tk K range)
            AL.add_curve(seq, 'SHM239_StepN', u.RawCurveTrackTypes.RCT_FLOAT, False); AL.add_float_curve_keys(seq, 'SHM239_StepN', [ts[0], ts[-1]], [nk, nk])
            assert EAL.save_loaded_asset(seq, False), 'save ' + name
    except Exception as e: out['errors'].append('%s: %s' % (name, str(e)[:200]))
out['n'] = len(out['clips']); out['ok'] = not out['errors'] and out['n'] == 48
print('STEP239 ' + json.dumps({'ok': out['ok'], 'n': out['n'], 'errors': out['errors']}) + ' ' + json.dumps(out['clips'])[:2000])
