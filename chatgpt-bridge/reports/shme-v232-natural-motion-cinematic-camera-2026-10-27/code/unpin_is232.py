"""unpin_is232.py (editor job): neutralise the V2.32 idle-stance start copies SHM232_IS_* (NOT promoted: idle backward starts 38 -> 22 cm, but
the stop -> re-press start j30_rel_3200 35 -> 54 because Motion Matching also picked the copy there; a stand-time route is the open fix).
The PoseSearch database API offers no entry removal in Python and removing a BranchIn track leaves the clip listed (V2.31 trap), so every
copy gets the restored ORIGINAL's bone tracks back (all tracks, raw local keys) and loses the curves the original does not carry (the
V2.32 start-bind witness / speed curves): the copies become exact duplicates of their originals = no behaviour change, databases untouched.
builtins.UP232 = {'dry': bool}. Prints UP232 {...} (max bone-track difference to the original after the write, read back)."""
import unreal as u, json, builtins, sys, pathlib, importlib
P = pathlib.Path(u.Paths.project_dir()).resolve(); sys.path.insert(0, str(P / 'Tools/SHME_V1_20260925'))
import v137_animedit as ae; importlib.reload(ae)
AL = u.AnimationLibrary; EAL = u.EditorAssetLibrary; DRY = bool(getattr(builtins, 'UP232', {}).get('dry', True))
S = '/Game/GraceRanger/SHME/Animations/Starts/Jog/'
out = {'dry': DRY, 'copies': {}}
for p in EAL.list_assets(S, recursive=False):
    pk = p.split('.')[0]; nm = pk.rsplit('/', 1)[-1]
    if not nm.startswith('SHM232_IS_'): continue
    src = S + nm.replace('SHM232_IS_', 'SHM_JogQ_')
    so = u.load_asset(src); co = u.load_asset(pk)
    bones = [str(b) for b in AL.get_animation_track_names(so)]
    nf = ae.num_frames(so); assert nf == ae.num_frames(co), (nm, nf, ae.num_frames(co))
    L = ae.read_local(so, bones, list(range(nf)))
    sc = set(str(c) for c in AL.get_animation_curve_names(so, u.RawCurveTrackTypes.RCT_FLOAT))
    extra = [str(c) for c in AL.get_animation_curve_names(co, u.RawCurveTrackTypes.RCT_FLOAT) if str(c) not in sc]
    info = {'tracks': len(bones), 'frames': nf, 'extra_curves': extra}
    if not DRY:
        c = ae.controller(co)
        try: c.open_bracket(u.Text('SHME V2.32 neutralise idle-stance copy'), True)
        except Exception: c.open_bracket('SHME V2.32 neutralise', True)
        try:
            for b in bones:
                ks = L[b]
                if not c.set_bone_track_keys(b, [u.Vector(*k[0]) for k in ks], [u.Quat(*k[1]) for k in ks], [u.Vector(*k[2]) for k in ks], True): raise RuntimeError('keys ' + b)
        finally: c.close_bracket(True)
        for cn in extra: AL.remove_curve(co, cn, False)
        info['saved'] = bool(EAL.save_asset(pk, False))
        L2 = ae.read_local(u.load_asset(pk), bones, list(range(nf)))
        info['max_diff_cm'] = round(max(ae.vlen(ae.vsub(L2[b][f][0], L[b][f][0])) for b in bones for f in range(nf)), 4)
    out['copies'][nm] = info
print('UP232 ' + json.dumps(out, default=str))
