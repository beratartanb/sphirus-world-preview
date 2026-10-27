"""exclude233_is.py (editor job) - V2.33: take the rejected V2.32 idle-stance start copies SHM232_IS_* out of the ACTIVE search with the
supported PoseSearch mechanism: an AnimNotifyState_PoseSearchExcludeFromDatabase over the whole clip (the database index skips every pose
of it; Python has no entry-removal API and removing BranchIn leaves the entry - V2.31 trap). The copies stay on disk (referenced by the
start databases). builtins.EX233 = {'dry': True}. Dry run: prints the copy list + every database that lists them (the write manifest).
Prints EX233 {...}."""
import unreal as u, json, builtins
EAL = u.EditorAssetLibrary; AL = u.AnimationLibrary
cfg = dict(getattr(builtins, 'EX233', {})); builtins.EX233 = {}; DRY = bool(cfg.get('dry', True))
S = '/Game/GraceRanger/SHME/Animations/Starts/'
copies = [p.split('.')[0] for p in EAL.list_assets(S + 'Jog', recursive=False) if p.split('.')[0].rsplit('/', 1)[-1].startswith('SHM232_IS_')]
dbs = {}
for p in EAL.list_assets(S, recursive=False):
    pk = p.split('.')[0]
    if not pk.rsplit('/', 1)[-1].startswith('PSD_'): continue
    d = u.load_asset(pk)
    try: names = [d.get_animation_asset(i).get_name() for i in range(d.get_num_animation_assets()) if d.get_animation_asset(i)]
    except Exception: continue
    k = [n for n in names if n.startswith('SHM232_IS_')]
    if k: dbs[pk] = k
out = {'dry': DRY, 'copies': copies, 'dbs_listing_them': dbs, 'done': {}}
if not DRY:
    tr = 'SHME_V233_Excluded'
    for c in copies:
        s = u.load_asset(c); names = [str(t) for t in AL.get_animation_notify_track_names(s)]
        if tr in names: out['done'][c.rsplit('/', 1)[-1]] = 'already'; continue
        AL.add_animation_notify_track(s, tr)
        AL.add_animation_notify_state_event(s, tr, 0.0, float(s.get_play_length()), u.AnimNotifyState_PoseSearchExcludeFromDatabase)
        out['done'][c.rsplit('/', 1)[-1]] = bool(EAL.save_asset(c, False))
print('EX233 ' + json.dumps(out, default=str))
