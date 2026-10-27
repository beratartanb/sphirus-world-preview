import unreal as u, json
AR = u.AssetRegistryHelpers.get_asset_registry(); AL = u.AnimationLibrary
out = {}
for p in ['/Game/GraceRanger/Animations/Continuity/SampleReference/A_CT_Ref_Walk_Stop_F_Lfoot', '/Game/GraceRanger/Animations/Continuity/SampleReference/A_CT_Ref_Walk_Stop_F_Rfoot',
          '/Game/GraceRanger/Animations/Continuity/SampleCandidates/A_CT_Sample_M_Relaxed_Run_Stop_F_Lfoot', '/Game/GraceRanger/Animations/Continuity/SampleCandidates/A_CT_Sample_M_Relaxed_Run_Stop_F_Rfoot',
          '/Game/GraceRanger/Animations/Continuity/SampleCandidates/A_CT_Sample_M_Relaxed_Sprint_Stop_F_Lfoot', '/Game/GraceRanger/Animations/Continuity/SampleCandidates/A_CT_Sample_M_Relaxed_Sprint_Stop_F_Rfoot']:
    opt = u.AssetRegistryDependencyOptions(include_soft_package_references=True, include_hard_package_references=True)
    refs = AR.get_referencers(p, opt) or []
    s = u.load_asset(p); bi = []
    for ev in AL.get_animation_notify_events(s):
        st = ev.get_editor_property('notify_state_class')
        if st and 'BranchIn' in st.get_class().get_name():
            db = st.get_editor_property('database'); bi.append(db.get_name() if db else None)
    out[p.rsplit('/', 1)[-1]] = {'referencers': [str(r) for r in refs][:12], 'branchin_dbs': bi}
print('REFACT ' + json.dumps(out))
