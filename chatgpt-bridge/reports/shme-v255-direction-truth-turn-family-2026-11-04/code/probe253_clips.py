"""probe253_clips.py (measure job, read-only): component-space bone positions (root motion included, i.e. the clip's own world) of named
clips over time windows, sampled at 60 Hz, for offline blend-stack reconstruction (V2.53: 180 crop -> CP2 pop, FwdLeft landing dip,
start-entry stance foot surge). builtins.P253 = {'jobs': [[asset_name_or_path, t0, t1], ...], 'bones': [...], 'tag': 'x'}.
Writes Saved/Codex/SHME_V253_20261104/data/clips_<tag>.json (local only, derived from paid clips: never published) and prints CLIPS253 {...}."""
import unreal as u, json, builtins, sys, importlib, math, pathlib
sys.path.insert(0, r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925')
import v137_animedit as ae; importlib.reload(ae)
cfg = dict(getattr(builtins, 'P253', {})); BONES = cfg.get('bones', ['root', 'pelvis', 'spine_05', 'head', 'clavicle_r', 'upperarm_r', 'upperarm_l', 'foot_l', 'foot_r', 'ball_l', 'ball_r'])
ar = u.AssetRegistryHelpers.get_asset_registry(); out = {'clips': {}}
def find(n):
    if n.startswith('/'): return n
    f = u.ARFilter(class_paths=[u.TopLevelAssetPath('/Script/Engine', 'AnimSequence')], recursive_paths=True, package_paths=['/Game'])
    al = ar.get_assets(f); hits = [str(a.package_name) for a in al if str(a.asset_name) == n]
    return hits or [str(a.package_name) for a in al if n in str(a.asset_name)][:4]
for n, t0, t1 in cfg.get('jobs', []):
    paths = find(n); paths = [paths] if isinstance(paths, str) else paths
    if not paths: out['clips'][n] = 'NOT_FOUND'; continue
    p = sorted(paths, key=len)[0]; seq = u.load_asset(p)
    c = ae.Clip(seq, BONES); nf = c.nf; L = float(seq.get_play_length()); dt = L / max(1, nf - 1)
    def at(b, t):
        x = max(0.0, min(L, t)) / dt; i = min(int(math.floor(x)), nf - 2); w = x - i
        a, _ = c.comp(b, i); b_, _ = c.comp(b, i + 1); return [round(a[k] * (1 - w) + b_[k] * w, 3) for k in range(3)]
    ts = [t0 + k / 60.0 for k in range(int(round((t1 - t0) * 60)) + 1)]
    rq = c.comp('root', 0)[1]
    out['clips'][n] = {'path': p, 'all_paths': paths[:4], 'len': round(L, 4), 'nf': nf, 'loop': bool(seq.get_editor_property('loop')) if True else None, 'root_q0': [round(x, 4) for x in rq],
                       'samples': [[round(t, 4)] + [at(b, t) for b in BONES] for t in ts],
                       'keys': [[round(f * dt, 4)] + [[round(x, 3) for x in c.comp(b, f)[0]] for b in BONES] + [[round(x, 5) for x in c.comp('root', f)[1]]] for f in range(nf) if t0 - 0.1 <= f * dt <= t1 + 0.1]}
out['bones'] = BONES
P = pathlib.Path(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/SHME_V253_20261104/data'); P.mkdir(parents=True, exist_ok=True)
(P / ('clips_%s.json' % cfg.get('tag', 'x'))).write_text(json.dumps(out))
print('CLIPS253 ' + json.dumps({k: (v if isinstance(v, str) else {'path': v['path'], 'len': v['len'], 'nf': v['nf'], 'n': len(v['samples'])}) for k, v in out['clips'].items()}))
