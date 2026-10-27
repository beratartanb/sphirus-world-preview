"""remove_is232.py (editor job): take the V2.32 idle-stance start copies SHM232_IS_* OUT of production (not promoted: true-idle backward starts
38 -> 22 cm but the stop -> re-press start j30_rel_3200 35 -> 54: Motion Matching also picked the idle-stance copy there; a stand-time
route is needed). Removing a BranchIn track does not remove a clip from a database (V2.31 trap) -> the entries are filtered out of every
start database's animation_assets array, the databases saved, then the copies (no referencer left) deleted. builtins.RI232 = {'dry': bool}.
Prints RI232 {...} with the entry counts before / after (read back)."""
import unreal as u, json, builtins
EAL = u.EditorAssetLibrary; DRY = bool(getattr(builtins, 'RI232', {}).get('dry', True))
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
S = '/Game/GraceRanger/SHME/Animations/Starts/'
DBS = ['PSD_SHM_JogStartQ_L', 'PSD_SHM_JogStartQ_R', 'PSD_SHM_JogStartS_L', 'PSD_SHM_JogStartS_R', 'PSD_SHM_SprintStartT_L', 'PSD_SHM_SprintStartT_R']
out = {'dry': DRY, 'dbs': {}, 'deleted': []}
def asset_name(e):
    for k in ('animation_asset', 'sequence', 'anim_asset'):
        try:
            a = e.get_editor_property(k)
            if a: return a.get_name()
        except Exception: pass
    return None
for n in DBS:
    db = u.load_asset(S + n)
    if not db: out['dbs'][n] = 'missing'; continue
    arr = list(db.get_editor_property('animation_assets'))
    keep = [e for e in arr if not (asset_name(e) or '').startswith('SHM232_IS_')]
    info = {'before': len(arr), 'is_entries': len(arr) - len(keep), 'names_sample': [asset_name(e) for e in arr][:3]}
    if not DRY and len(keep) != len(arr):
        db.set_editor_property('animation_assets', keep); info['saved'] = bool(EAL.save_asset(S + n, False))
        db2 = u.load_asset(S + n); info['after'] = len(list(db2.get_editor_property('animation_assets')))
        info['after_is'] = sum(1 for e in db2.get_editor_property('animation_assets') if (asset_name(e) or '').startswith('SHM232_IS_'))
    out['dbs'][n] = info
if not DRY:
    for p in EAL.list_assets(S + 'Jog', recursive=False):
        pk = p.split('.')[0]
        if pk.rsplit('/', 1)[-1].startswith('SHM232_IS_'):
            out['deleted'].append((pk.rsplit('/', 1)[-1], bool(EAL.delete_asset(pk))))
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('RI232 ' + json.dumps(out, default=str))
