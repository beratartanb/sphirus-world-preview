"""dup_pinned232.py (editor job): V2.32 C (second form). The pinned straight JogQ starts (pinstart232 written in place in B11) are DUPLICATED
as SHM232_IS_<name> (idle-stance versions); a duplicate carries the source's BranchIn notify states, so it joins the SAME start databases
(PSD_SHM_JogStartQ_R / JogStartS_*) next to the original. The originals are then restored from the checkpoint with the editor closed (the
run232_c1 pre-step) -> Motion Matching picks the idle-stance version when the body really stands in the idle stance and the original
when it starts from another pose (the release / re-press case). Turn starts get NO idle copy (pinned turn starts regressed jstart 48 -> 69).
builtins.DP232 = {'dry': bool}. Prints DP232 {...} incl. the databases of each copy (read back)."""
import unreal as u, json, builtins
EAL = u.EditorAssetLibrary; AL = u.AnimationLibrary
DRY = bool(getattr(builtins, 'DP232', {}).get('dry', True))
S = '/Game/GraceRanger/SHME/Animations/Starts/Jog/'
NAMES = ['SHM_JogQ_af_Loco_Jog_Bwd_Start_AAMS', 'SHM_JogQ_af_Loco_Jog_Fwd_Start_AAMS', 'SHM_JogQ_af_Loco_Jog_Left_Start_AAMS', 'SHM_JogQ_af_Loco_Jog_Right_Start_AAMS',
         'SHM_JogQ_A_CP2_Jog_Fwd_Start', 'SHM_JogQ_A_RR_M_Relaxed_Run_Start_F_Lfoot', 'SHM_JogQ_A_RR_M_Relaxed_Run_Start_F_Rfoot', 'SHM_JogQ_A_LS_Jog_Left_Start', 'SHM_JogQ_A_LS_Jog_Right_Start']
out = {'dry': DRY, 'copies': {}}
def dbs_of(seq):
    r = []
    for ev in AL.get_animation_notify_events(seq):
        st = ev.get_editor_property('notify_state_class')
        if st and 'BranchIn' in st.get_class().get_name():
            db = st.get_editor_property('database'); r.append(db.get_name() if db else None)
    return sorted(set(x for x in r if x))
for n in NAMES:
    src = S + n; dst = S + n.replace('SHM_JogQ_', 'SHM232_IS_')
    if not EAL.does_asset_exist(src): out['copies'][n] = 'missing'; continue
    info = {'src_dbs': dbs_of(u.load_asset(src))}
    if not DRY:
        if not EAL.does_asset_exist(dst): assert EAL.duplicate_asset(src, dst), dst
        c = u.load_asset(dst)
        # re-create the BranchIn states on the copy (one full-window state per database of the source: the V2.25 full-window rule) the way
        # build_v226_revdbs registers clips in a database
        dbo = {}
        for tr in [str(t) for t in AL.get_animation_notify_track_names(c)]:
            for ev in AL.get_animation_notify_events_for_track(c, tr):
                st = ev.get_editor_property('notify_state_class')
                if st and 'BranchIn' in st.get_class().get_name() and st.get_editor_property('database'): dbo[st.get_editor_property('database').get_path_name()] = (tr, st.get_editor_property('database'))
        for tr in sorted(set(v[0] for v in dbo.values())): AL.remove_animation_notify_track(c, tr)
        ln = float(c.get_play_length())
        for i, (k, (tr, db)) in enumerate(sorted(dbo.items())):
            ntr = 'SHME_V232_IS_%d' % i; AL.add_animation_notify_track(c, ntr)
            ns = AL.add_animation_notify_state_event(c, ntr, 0.0, ln - 0.01, u.AnimNotifyState_PoseSearchBranchIn); ns.set_editor_property('database', db)
        info['dst_dbs'] = dbs_of(c); info['saved'] = bool(EAL.save_asset(dst, False))
        for d in info['src_dbs']:
            hits = [p for p in EAL.list_assets('/Game/GraceRanger/SHME/Animations/Starts', recursive=True) if p.split('.')[0].endswith('/' + d)]
            if hits:
                db = u.load_asset(hits[0].split('.')[0]); names_ = [db.get_animation_asset(i).get_name() for i in range(db.get_num_animation_assets())]
                info.setdefault('in_db', {})[d] = c.get_name() in names_
    out['copies'][n] = info
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('DP232 ' + json.dumps(out, default=str))
