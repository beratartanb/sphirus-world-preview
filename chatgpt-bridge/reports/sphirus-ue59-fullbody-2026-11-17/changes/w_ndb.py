# w_ndb.py (write, gated runner + manifest): forward-only GASP Normal databases for the Sphirus orient-to-movement player.
# Why: profile C mapped the Relaxed forward databases onto the full Dense databases, so the forward walk/jog could select strafe loops,
# arcs and strafe pivots; measured as a 0.5 s hip stall + 18 deg overshoot after a 90 deg turn (H_CW_h1 vs H_AW_h1).
# New assets under /Game/Sphirus/Player/GASP/DB mirror the Relaxed F_* databases' structure with Neutral clips. Clips get one extra
# BranchIn notify track (SphN_*) which is how a database is populated from script (no array API). No ABP change here.
import unreal as u, re, json
EA = u.EditorAssetLibrary; AL = u.AnimationLibrary; AT = u.AssetToolsHelpers.get_asset_tools()
B = '/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases/Dense/PSD_Dense_Stand_'; D = '/Game/Sphirus/Player/GASP/DB'
SETS = {}
for g in ('Walk', 'Run'):
    SETS['PSD_Sph_N_%s_F_Loops' % g] = (g + '_Loops', r'^M_Neutral_%s_Loop_F$' % g if g == 'Run' else r'^M_Neutral_(Walk_Loop_F|Transition_Run_to_Walk_[LR]foot)$')
    SETS['PSD_Sph_N_%s_F_Turns' % g] = (g + '_Pivots', r'^M_Neutral_%s_Turn_' % g)
    SETS['PSD_Sph_N_%s_F_Pivots' % g] = (g + '_Pivots', r'^M_Neutral_%s_(Pivot_B_F|Box_LL_F|Box_RL_F)_' % g)
    SETS['PSD_Sph_N_%s_F_Starts' % g] = (g + '_Starts', r'^M_Neutral_%s_(Reface_Start_F_|Start_F_)' % g)
f = u.DataAssetFactory(); f.set_editor_property('data_asset_class', u.PoseSearchDatabase); res = {}
for name, (src, rx) in SETS.items():
    s = u.load_asset(B + src); assert s, src
    clips = [s.get_animation_asset(i) for i in range(s.get_num_animation_assets())]; clips = [c for c in clips if c and re.search(rx, c.get_name())]
    assert clips, name
    db = u.load_asset(D + '/' + name) if EA.does_asset_exist(D + '/' + name) else AT.create_asset(name, D, u.PoseSearchDatabase, f)
    for k in ('schema', 'continuing_pose_cost_bias', 'base_cost_bias', 'looping_cost_bias', 'tags', 'normalization_set', 'pose_search_mode'):
        try: db.set_editor_property(k, s.get_editor_property(k))
        except Exception as e: print('PROP', name, k, str(e)[:100])
    assert EA.save_loaded_asset(db, False)
    tr = 'SphN_' + name[len('PSD_Sph_N_'):]
    for a in clips:
        if tr in [str(t) for t in AL.get_animation_notify_track_names(a)]: AL.remove_animation_notify_track(a, tr)
        AL.add_animation_notify_track(a, tr); st = AL.add_animation_notify_state_event(a, tr, 0.0, float(a.get_play_length()), u.AnimNotifyState_PoseSearchBranchIn)
        st.set_editor_property('database', db); assert EA.save_loaded_asset(a, False)
    assert EA.save_loaded_asset(db, False)
    got = sorted(db.get_animation_asset(i).get_name() for i in range(db.get_num_animation_assets()) if db.get_animation_asset(i))
    res[name] = dict(want=sorted(c.get_name() for c in clips), got=got); print('DB', name, len(clips), len(got))
json.dump(res, open(u.Paths.project_dir() + 'Saved/UE59Work/probe/ndb_result.json', 'w'), indent=1)
print('ALL_OK', all(v['want'] == v['got'] for v in res.values())); print('DONE')
