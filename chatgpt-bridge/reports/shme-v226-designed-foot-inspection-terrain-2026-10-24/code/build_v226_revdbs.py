"""build_v226_revdbs.py (editor job): V2.25 jog reversal databases from the AUTHORED clips (gen225_rev.py).
  PSD_SHM226_JogRevBwd : SHM226_JogRev_B_F_P* (backpedal -> forward; BranchIn window 0..ENTRY s = entries near frame 0 only) + the rear loops
  PSD_SHM226_JogRevFwd : SHM226_JogRev_F_B_P* (forward -> backward) + the rear loops
Schema / biases copied from PSD_SHM224_JogRevBwdO. Loops keep full 0..len windows. New assets only; nothing in production is edited.
A/B: abp_flags SHM224_DB_JRBwd / JRBwdM -> PSD_SHM226_JogRevBwd, SHM224_DB_JRFwd / JRFwdM -> PSD_SHM226_JogRevFwd (the V2.24 route then
serves the authored clips in every planted-foot case: the phase bins cover both feet). builtins.V226_DRY prints only. Prints RDB226 {...}."""
import unreal as u, json, builtins
L = u.AnimationLibrary; EAL = u.EditorAssetLibrary; AT = u.AssetToolsHelpers.get_asset_tools()
DRY = bool(getattr(builtins, 'V226_DRY', True)); ENTRY = float(getattr(builtins, 'V226_ENTRY', 0.12)); NPH = int(getattr(builtins, 'V226_NPH', 8))
V = '/Game/GraceRanger/SHME/Animations/V226/'; V4 = '/Game/GraceRanger/SHME/Animations/V224/'
CT = '/Game/GraceRanger/Animations/Continuity/'; RB = '/Game/GraceRanger/Animations/LocomotionBehavior/RearRevision/'
REAR = [CT + 'A_CT_Jog_Bwd', RB + 'A_RB_Jog_Rear', RB + 'A_RB_Jog_RearLeft', RB + 'A_RB_Jog_RearRight']
PLAN = {'PSD_SHM226_JogRevBwd': [V + 'SHM226_JogRev_B_F_P%d' % k for k in range(NPH)] + REAR, 'PSD_SHM226_JogRevFwd': [V + 'SHM226_JogRev_F_B_P%d' % k for k in range(NPH)] + REAR}
seed = u.load_asset(V4 + 'PSD_SHM224_JogRevBwdO'); assert seed
out = {'dry': DRY, 'missing': [c for cs in PLAN.values() for c in cs if not EAL.does_asset_exist(c)]}
if not DRY and not out['missing']:
    res = {}
    for n, clips in PLAN.items():
        path = V + n
        if not EAL.does_asset_exist(path):
            f = u.DataAssetFactory(); f.set_editor_property('data_asset_class', u.PoseSearchDatabase)
            db = AT.create_asset(n, V.rstrip('/'), u.PoseSearchDatabase, f); assert db, n
            db.set_editor_property('schema', seed.get_editor_property('schema'))
            for k in ('base_cost_bias', 'continuing_pose_cost_bias', 'looping_cost_bias', 'normalization_set'):
                try: db.set_editor_property(k, seed.get_editor_property(k))
                except Exception as e: out.setdefault('prop_err', []).append([n, k, str(e)[:80]])
            assert EAL.save_asset(path, False)
        db = u.load_asset(path); tr = 'SHME_V226_' + n.replace('PSD_SHM226_', '')
        for c in clips:
            s = u.load_asset(c); names = [str(t) for t in L.get_animation_notify_track_names(s)]
            if tr in names: L.remove_animation_notify_track(s, tr)
            L.add_animation_notify_track(s, tr); ln = float(s.get_play_length())
            win = ln if 'JogRev' not in c else min(ENTRY, ln - 0.01)
            st = L.add_animation_notify_state_event(s, tr, 0.0, win, u.AnimNotifyState_PoseSearchBranchIn)
            st.set_editor_property('database', db); assert EAL.save_asset(c, False), c
        assert EAL.save_asset(path, False)
        res[n] = [db.get_animation_asset(i).get_name() for i in range(db.get_num_animation_assets())]
    out['dbs'] = res
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('RDB226 ' + json.dumps(out, default=str))
