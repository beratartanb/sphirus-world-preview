"""build241_kdb.py (editor job, write manifest = every V2.39 takeover clip + the new databases) - V2.41 per-(source, target, contact K)
takeover ENTRY databases. Measured (v241a30 / c30b / d30 j41_rl_p10_tkh, the request gated on the same jog phase): inside one V2.40
(source, target) database the identical-prefix contact clips compete - MM entered K3 @0.667 for a request at cut time 0.44 whose
contact clip is K2 (reversal 0.4 s late, old-side overshoot 49 deg). With K3's window cut to its tail the SAME search entered K2 @0.467
(continuous, overshoot 25 deg, latency 0.30 s). So the entry database must hold ONE clip: PSD_SHM240_E<eidx>_K<k> (V241 folder; the name
keeps the 'PSD_SHM240_E' substring that the V2.40 entry-confirmation / obstacle rules test), schema PSS_SHM241_TkEntry (trajectory 0),
biases as the V2.40 entry database, one BranchIn on a NEW track SHME_V241_K, window [t_(K-1), t_K + 0.05] (the V2.40 track stays, so the
V2.40 path is unchanged). builtins.V241_KDB = {'dry': bool, 'only': [names] (optional)}. Prints KDB241 {...}."""
import unreal as u, json, builtins, glob, re
L = u.AnimationLibrary; EAL = u.EditorAssetLibrary; AT = u.AssetToolsHelpers.get_asset_tools()
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
c = dict(getattr(builtins, 'V241_KDB', {})); DRY = bool(c.get('dry', True)); ONLY = set(c.get('only') or [])
VP9 = '/Game/GraceRanger/SHME/Animations/V239/'; V41 = '/Game/GraceRanger/SHME/Animations/V241'; TR = 'SHME_V241_K'
J = {}
for f in sorted(glob.glob(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/SHME_V239_20261030/gen239_tk_write_part*.json')):
    J.update({n: x for n, x in json.load(open(f))['clips'].items() if x.get('saved')})
spec = []
for n, x in sorted(J.items()):
    m = re.match(r'SHM239_Tk_([RL])_P(\d\d)_K(\d+)_(Back|Opp)$', n); sd, p, k, tg = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)
    e = 2 * ((0 if sd == 'R' else 24) + p) + (1 if tg == 'Opp' else 0)
    spec.append({'clip': VP9 + n, 'db': 'PSD_SHM240_E%02d_K%d' % (e, k), 'eidx': e, 'k': k, 'w0': x['contacts'][k - 1]['t'], 'w1': x['tK'] + 0.05})
if ONLY: spec = [s for s in spec if s['clip'].split('/')[-1] in ONLY or s['db'] in ONLY]
out = {'dry': DRY, 'n': len(spec), 'clips': [s['clip'] for s in spec], 'new': [V41 + '/' + s['db'] for s in spec], 'done': 0, 'errors': []}
if not DRY:
    sch = u.load_asset(V41 + '/PSS_SHM241_TkEntry'); assert sch
    for s in spec:
        try:
            path = V41 + '/' + s['db']
            if not EAL.does_asset_exist(path):
                f = u.DataAssetFactory(); f.set_editor_property('data_asset_class', u.PoseSearchDatabase)
                db = AT.create_asset(s['db'], V41, u.PoseSearchDatabase, f); assert db
                seed = u.load_asset('/Game/GraceRanger/SHME/Animations/V240/PSD_SHM240_E%02d' % s['eidx'])
                db.set_editor_property('schema', sch)
                for kk in ('base_cost_bias', 'continuing_pose_cost_bias', 'looping_cost_bias', 'normalization_set'):
                    try: db.set_editor_property(kk, seed.get_editor_property(kk))
                    except Exception: pass
                assert EAL.save_asset(path, False)
            db = u.load_asset(path); a = u.load_asset(s['clip'])
            names = [str(t) for t in L.get_animation_notify_track_names(a)]
            if TR in names: L.remove_animation_notify_track(a, TR)
            L.add_animation_notify_track(a, TR); ln = float(a.get_play_length())
            w0 = max(0.0, float(s['w0'])); w1 = min(ln, float(s['w1']))
            st = L.add_animation_notify_state_event(a, TR, w0, w1 - w0, u.AnimNotifyState_PoseSearchBranchIn); st.set_editor_property('database', db)
            assert EAL.save_asset(s['clip'], False); assert EAL.save_asset(path, False)
            ent = [db.get_animation_asset(i).get_name() for i in range(db.get_num_animation_assets())]
            if ent != [s['clip'].split('/')[-1]]: out['errors'].append([s['db'], 'entries', ent])
            out['done'] += 1
        except Exception as ex: out['errors'].append([s['db'], str(ex)[:140]])
    out['slots'] = sorted(set((s['eidx'], s['k']) for s in spec))[:3]
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
import os
open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/SHME_V241_20261031/kdb_spec%s.json' % ('_dry' if DRY else ''), 'w').write(json.dumps(spec))
out.pop('clips') if not DRY else None
print('KDB241 ' + json.dumps({k: (v if k not in ('clips', 'new') else len(v)) for k, v in out.items()}, default=str))
