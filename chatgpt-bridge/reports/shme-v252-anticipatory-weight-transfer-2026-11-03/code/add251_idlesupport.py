"""add251_idlesupport.py (dry = measure job, write = manifest of the idle clips): V2.51 SUPPORT curve on the weighted idle.
Measured (v251b30 w42 oiL): in SHM244_Idle_Weighted the COM stays centred between the feet (pelvis/spine at t = 0.48) - the weight cue
is the RELAXED leg: right heel lifted (ankle 7.7 cm vs 4.9 cm), so the COM-based SupportLoad split stays 50/50 and the start latch kept
the last-step side (left foot stepped, the relaxed right foot was the 'support' of the transfer clip and skated 19.7 cm).
Curve SHM251_IdleSupport per frame = clamp((ankle_r_z - ankle_l_z) / 2 cm, -1, 1): +1 = right heel up (left leg carries the weight, the
right foot is free to step), -1 = the opposite. Read by install251_startload2.py. builtins.V251_IS = {'dry': bool, 'clips': [paths]}.
Prints IDLESUP251 {...}."""
import unreal as u, json, builtins, sys, importlib
sys.path.insert(0, r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925')
import v137_animedit as ae; importlib.reload(ae)
AL = u.AnimationLibrary; EAL = u.EditorAssetLibrary
cfg = dict(getattr(builtins, 'V251_IS', {})); DRY = bool(cfg.get('dry', True))
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
db = u.load_asset('/Game/GraceRanger/SHME/Animations/V244/PSD_SHM242_IdleC')
paths = cfg.get('clips') or sorted(set(db.get_animation_asset(i).get_path_name().split('.')[0] for i in range(db.get_num_animation_assets())))
out = {'dry': DRY, 'clips': {}, 'saved': 0}; NAME = 'SHM251_IdleSupport'
for p in paths:
    seq = u.load_asset(p)
    if not isinstance(seq, u.AnimSequence): out['clips'][p] = 'not a sequence'; continue
    c = ae.Clip(seq, ['foot_l', 'foot_r']); nf = c.nf; L = seq.get_play_length()
    ts = [L * f / max(1, nf - 1) for f in range(nf)]; ks = []
    for f in range(nf):
        zl = c.comp('foot_l', f)[0][2]; zr = c.comp('foot_r', f)[0][2]; ks.append(max(-1.0, min(1.0, (zr - zl) / 2.0)))
    rec = {'nf': nf, 'len': round(L, 2), 'min': round(min(ks), 2), 'max': round(max(ks), 2), 'mean': round(sum(ks) / nf, 2), 'frac_left_loaded': round(sum(1 for k in ks if k > 0.5) / nf, 2), 'frac_right_loaded': round(sum(1 for k in ks if k < -0.5) / nf, 2)}
    if not DRY:
        if AL.does_curve_exist(seq, NAME, u.RawCurveTrackTypes.RCT_FLOAT): AL.remove_curve(seq, NAME, False)
        AL.add_curve(seq, NAME, u.RawCurveTrackTypes.RCT_FLOAT); AL.add_float_curve_keys(seq, NAME, ts, ks)
        assert EAL.save_asset(p, False), p; out['saved'] += 1
    out['clips'][p.split('/')[-1]] = rec
out['dirty'] = [q.get_name().split('/')[-1] for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('IDLESUP251 ' + json.dumps(out, default=str))
