"""probe_entry228.py (editor job, READ-ONLY): why the authored reversal clips are entered at ct 0.067-0.10 and who brakes the capsule.
 (a) PoseSearch: PSD_SHM226_JogRevFwd / Bwd database settings (schema, exclusion intervals, continuing pose bias, pose jump threshold,
     reselect history, number of poses), schema channels (trajectory sample offsets = history requirement, sample rate, pose bones);
     one authored clip: length, root motion flags, total root translation, notifies (BranchIn window), float curves;
 (b) GraceRanger movement profile values that own the capsule brake: RedirectInputNow, GR215_RevBrake*, StraightFriction,
     RedirectFriction, CutLatAccelMax, TurnLatAccelMax (BP_GR_MotionProfile defaults + DA_GR_LocomotionBehavior instance).
Prints PROBE228 {...}. Writes Saved/Codex/SHME_V228_20261025/probe_entry228.json. No save, no compile."""
import unreal as u, json, pathlib
out = {}
def props(o, names):
    d = {}
    for n in names:
        try: d[n] = str(o.get_editor_property(n))[:160]
        except Exception as e: d[n] = 'ERR ' + str(e)[:60]
    return d
for db in ('/Game/GraceRanger/SHME/Animations/V226/PSD_SHM226_JogRevFwd', '/Game/GraceRanger/SHME/Animations/V226/PSD_SHM226_JogRevBwd', '/Game/GraceRanger/SHME/Animations/V224/PSD_SHM224_JogRevFwdO'):
    a = u.load_asset(db)
    if not a: out[db.rsplit('/', 1)[-1]] = 'MISSING'; continue
    d = props(a, ['schema', 'exclude_from_database_parameters', 'continuing_pose_cost_bias', 'base_cost_bias', 'looping_cost_bias', 'pose_jump_threshold_time', 'pose_reselect_history', 'search_index_derived_data_key', 'normalization_set', 'additional_cost_bias'])
    try:
        ex = a.get_editor_property('exclude_from_database_parameters'); d['exclude_detail'] = {k: str(ex.get_editor_property(k)) for k in ('sequence_start_interval', 'sequence_end_interval')}
    except Exception as e: d['exclude_detail'] = 'ERR ' + str(e)[:80]
    try:
        sch = a.get_editor_property('schema'); d['schema_name'] = sch.get_name()
        d['schema'] = props(sch, ['sample_rate', 'data_preprocessor', 'mirror_data_table', 'skeleton', 'continuing_pose_cost_bias', 'base_cost_bias', 'looping_cost_bias'])
        chans = []
        for c in sch.get_editor_property('channels'):
            cd = {'class': c.get_class().get_name()}
            for k in ('samples', 'sample_times', 'weight', 'sampled_bones', 'bone', 'sample_time_offset', 'origin_time_offset', 'offset', 'use_sample_time_offset_root_bone', 'history', 'prediction'):
                try: cd[k] = str(c.get_editor_property(k))[:220]
                except Exception: pass
            chans.append(cd)
        d['channels'] = chans
    except Exception as e: d['schema_err'] = str(e)[:120]
    try:
        d['num_poses'] = int(a.get_num_poses()) if hasattr(a, 'get_num_poses') else 'n/a'
    except Exception as e: d['num_poses'] = 'ERR ' + str(e)[:60]
    try:
        seqs = a.get_editor_property('animation_assets'); d['assets'] = len(seqs)
        s0 = seqs[0]; d['asset0'] = props(s0, ['sequence', 'enable_mirroring', 'mirror_option', 'sampling_range', 'is_looping', 'disable_reselection', 'branch_in_id'])
    except Exception as e: d['assets_err'] = str(e)[:120]
    out[db.rsplit('/', 1)[-1]] = d
seq = u.load_asset('/Game/GraceRanger/SHME/Animations/V226/SHM226_JogRev_F_B_P4')
if seq:
    d = props(seq, ['enable_root_motion', 'root_motion_root_lock', 'force_root_lock', 'use_normalized_root_motion_scale', 'rate_scale', 'sequence_length', 'number_of_sampled_keys', 'additive_anim_type', 'interpolation'])
    try:
        rm = seq.extract_root_motion(0.0, seq.get_editor_property('sequence_length'), False); d['root_motion_total'] = str(rm.translation) if hasattr(rm, 'translation') else str(rm)[:120]
    except Exception as e: d['root_motion_total'] = 'ERR ' + str(e)[:80]
    try:
        d['notifies'] = [(str(n.notify_name), round(float(n.trigger_time_offset), 3) if hasattr(n, 'trigger_time_offset') else None, str(n.get_editor_property('notify_state_class'))[:40] if hasattr(n, 'get_editor_property') else '') for n in seq.get_editor_property('notifies')][:6]
        d['notify_detail'] = [{k: str(n.get_editor_property(k))[:80] for k in ('notify_name', 'duration', 'link_value', 'segment_begin_time', 'segment_length')} for n in seq.get_editor_property('notifies')][:4]
    except Exception as e: d['notifies'] = 'ERR ' + str(e)[:80]
    try: d['curves'] = [str(c) for c in u.AnimationLibrary.get_animation_curve_names(seq, u.RawCurveTrackTypes.RCT_FLOAT)]
    except Exception as e: d['curves'] = 'ERR ' + str(e)[:80]
    try:
        d['root_track_first_last'] = [str(u.AnimationLibrary.get_bone_pose_for_time(seq, 'root', t, False).translation) for t in (0.0, 0.5, 1.5)]
    except Exception as e: d['root_track_first_last'] = 'ERR ' + str(e)[:80]
    out['clip_P4'] = d
# (b) movement profile
names = ['RedirectInputNow', 'GR215_RevBrakeAccel', 'GR215_RevBrakeFriction', 'GR215_RevBrakeDot', 'GR215_RevBrakeMinSpeed', 'StraightFriction', 'RedirectFriction', 'CutLatAccelMax', 'TurnLatAccelMax', 'TurnSoftK', 'TurnRateFloor', 'RedirectSpeedDecay', 'GR223_PivotXY', 'GR_TargetGait']
pc = u.load_asset('/Game/GraceRanger/Profiles/BP_GR_MotionProfile')
if pc:
    cdo = u.get_default_object(pc.generated_class()); out['profile_cdo'] = props(cdo, names)
da = u.load_asset('/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior')
if da: out['da_gr'] = props(da, names)
sda = u.load_asset('/Game/GraceRanger/SHME/DA_SHM_Response_Default')
if sda: out['da_shm'] = props(sda, ['RedirectSpeedDecay', 'RedirectHoldEnabled', 'JogReversalMode', 'RedirectMaxDwell', 'InspectRadius', 'InspectJump', 'InspectZoomOn', 'StepEdgeOn', 'SwingLiftMargin', 'StepPrepEnabled'])
pathlib.Path(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/SHME_V228_20261025/probe_entry228.json').write_text(json.dumps(out, indent=1, default=str), encoding='utf8')
print('PROBE228 ' + json.dumps(out, default=str)[:3000])
