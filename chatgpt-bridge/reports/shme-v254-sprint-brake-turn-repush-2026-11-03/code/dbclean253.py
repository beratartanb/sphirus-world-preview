"""dbclean253.py (dry = measure; write = manifest v253_settle / v253_apa3 = the NEW assets only): the V2.53 copies inherited the source
BranchIn tracks (SHME_V237_JogStop -> production PSD_SHM237_JogStop; copy trap). For every clip under V253 whose BranchIn points at a
database outside V253: Database := None (PostEditChange removes the entry), then the track is removed. Prints the full-path entry lists of
the production and the new databases before / after. builtins.V253_DBC = {'dry': bool}. Prints DBC253 {...}."""
import unreal as u, json, builtins
AL = u.AnimationLibrary; EAL = u.EditorAssetLibrary
DRY = bool(dict(getattr(builtins, 'V253_DBC', {})).get('dry', True))
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
V = '/Game/GraceRanger/SHME/Animations/V253'
DBS = ['/Game/GraceRanger/SHME/Animations/V237/PSD_SHM237_JogStop', V + '/PSD_SHM253_JogStop', '/Game/GraceRanger/SHME/Animations/StartTransfer/PSD_SHM_StartTransfer_L',
       '/Game/GraceRanger/SHME/Animations/StartTransfer/PSD_SHM_StartTransfer_R', V + '/PSD_SHM253_StartTransferAPA_L', V + '/PSD_SHM253_StartTransferAPA_R',
       '/Game/GraceRanger/SHME/Animations/V252/PSD_SHM252_StartTransferAPA_L', '/Game/GraceRanger/SHME/Animations/V252/PSD_SHM252_StartTransferAPA_R']
def entries():
    o = {}
    for d in DBS:
        db = u.load_asset(d); o[d.split('/')[-1]] = sorted(db.get_animation_asset(i).get_path_name().split('.')[0].replace('/Game/GraceRanger/SHME/Animations/', '') for i in range(db.get_num_animation_assets()))
    return o
out = {'dry': DRY, 'before': entries(), 'fixed': []}
ar = u.AssetRegistryHelpers.get_asset_registry()
for a in ar.get_assets_by_path(V, False):
    if str(a.asset_class_path.asset_name) != 'AnimSequence': continue
    p = str(a.package_name); seq = u.load_asset(p); changed = False
    for ev in AL.get_animation_notify_events(seq):
        st = ev.get_editor_property('notify_state_class')
        if st and 'BranchIn' in st.get_class().get_name():
            db = st.get_editor_property('database'); dp = db.get_path_name() if db else ''
            if dp and not dp.startswith(V):
                out['fixed'].append([p.split('/')[-1], '', dp.split('.')[-1]])
                if not DRY: st.set_editor_property('database', None); changed = True
    if changed:
        for tr in [str(t) for t in AL.get_animation_notify_track_names(seq)]:
            if tr == 'SHME_V237_JogStop' or tr.startswith('SHME_StartTransfer_Role'):
                AL.remove_animation_notify_events_by_track(seq, tr); AL.remove_animation_notify_track(seq, tr)
        assert EAL.save_loaded_asset(seq, False), p
if not DRY:
    for d in DBS[:2]:
        if any(q.get_name() == d for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()): EAL.save_asset(d, False)
out['after'] = entries()
out['dirty'] = [q.get_name().split('/')[-1] for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('DBC253 ' + json.dumps(out, default=str))
