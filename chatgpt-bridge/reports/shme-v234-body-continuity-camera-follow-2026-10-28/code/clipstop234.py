"""clipstop234.py (measure job) - the forward jog stop closing step: is the trailing-foot drag in the SOURCE clip or made at runtime?
For SHM_A_CP2_Jog_Fwd_Stop (+ its source A_CP2_Jog_Fwd_Stop when present) prints per 1/30 s from ct 0.5 to the end: root position
(world from root motion), ball_l / ball_r in WORLD (root motion applied) and their height. A planted foot is world-still in the clip; a
closing step lifts (z > 3 cm) while it travels. Prints CLIPSTOP234 {...}."""
import unreal as u, json, pathlib, sys, importlib
P = pathlib.Path(u.Paths.project_dir()).resolve(); sys.path.insert(0, str(P / 'Tools/SHME_V1_20260925'))
import v137_animedit as ae; importlib.reload(ae)
out = {}
for path in ('/Game/GraceRanger/SHME/Animations/V228/SHM_A_CP2_Jog_Fwd_Stop', '/Game/GraceRanger/Animations/Continuity/CorePhase2/A_CP2_Jog_Fwd_Stop'):
    a = u.load_asset(path)
    if not a:
        found = u.AssetRegistryHelpers.get_asset_registry().get_assets_by_class(u.TopLevelAssetPath('/Script/Engine', 'AnimSequence'))
        cand = [x for x in found if str(x.asset_name) == path.rsplit('/', 1)[1]]
        if not cand: out[path] = 'missing'; continue
        a = cand[0].get_asset(); path = str(cand[0].package_name)
    clip = ae.Clip(a, ['root', 'pelvis', 'ball_l', 'ball_r'])
    rows = []
    for f in range(clip.nf):
        t = f / max(clip.nf - 1, 1) * float(a.get_play_length())
        if t < 0.5: continue
        r = clip.comp('root', f, None)[0]; bl = clip.comp('ball_l', f, None)[0]; br = clip.comp('ball_r', f, None)[0]
        rows.append([round(t, 3), [round(x, 1) for x in r], [round(x, 1) for x in bl], [round(x, 1) for x in br]])
    out[path] = {'len': round(float(a.get_play_length()), 3), 'nf': clip.nf, 'rows': rows}
print('CLIPSTOP234 ' + json.dumps(out))
