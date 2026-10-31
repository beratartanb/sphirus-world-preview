"""install241_sch.py (editor job, write manifest = the 96 V2.40 entry databases + new schema PSS_SHM241_TkEntry) - V2.41 takeover ENTRY
continuity. Measured (v241a30_j41_rl_p10_tkh / _p16_tkh, request gated on the same jog phase): the request at cut time 0.44-0.47 entered
the WRONG contact clip far ahead (P10: K3 @0.67 instead of K2 @0.47; P02: K4 @1.10 instead of K2 @0.47) - the reversal began 0.4-0.65 s
late while the body accelerated out of the old turn. The entry schema PSS_SHM239_Takeover matched only ONE foot position (foot_l) + foot
velocities + pelvis heading + trajectory 0.15: with identical-prefix copies the pose cannot separate the phase, the future trajectory
(which already turns back later in the clip) pulled the time forward. New entry schema = PSS_SHM239_Takeover duplicate with the trajectory
weight 0 (pose decides; V2.41 first try also ADDED a foot_r position channel via new_object -> PoseSearch indexer assert, editor crash:
never add channels from Python - weights only). builtins.V241_SCH =
{'dry': bool, 'traj_w': 0.0, 'foot_r': True}. Prints SCH241 {...}."""
import unreal as u, json, builtins
EAL = u.EditorAssetLibrary; AT = u.AssetToolsHelpers.get_asset_tools()
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
c = dict(getattr(builtins, 'V241_SCH', {})); DRY = bool(c.get('dry', True))
SRC = '/Game/GraceRanger/SHME/Animations/V239/PSS_SHM239_Takeover'; DST_DIR = '/Game/GraceRanger/SHME/Animations/V241'; NAME = 'PSS_SHM241_TkEntry'; DST = DST_DIR + '/' + NAME
out = {'dry': DRY}
if not DRY:
    if not EAL.does_asset_exist(DST):
        s = AT.duplicate_asset(NAME, DST_DIR, u.load_asset(SRC)); assert s, 'duplicate failed'
    s = u.load_asset(DST); chs = list(s.get_editor_property('channels'))
    for ch in chs:
        if 'Trajectory' in ch.get_class().get_name(): ch.set_editor_property('weight', float(c.get('traj_w', 0.0)))
    if c.get('foot_r', False):
        grp = [x for x in chs if 'Group' in x.get_class().get_name()][0]; sub = list(grp.get_editor_property('sub_channels'))
        if not any('Position' in x.get_class().get_name() and str(x.get_editor_property('bone').get_editor_property('bone_name')) == 'foot_r' for x in sub):
            pl = [x for x in sub if 'Position' in x.get_class().get_name()][0]
            nr = u.new_object(type(pl), grp); br = u.BoneReference(); br.set_editor_property('bone_name', 'foot_r')
            nr.set_editor_property('bone', br); nr.set_editor_property('weight', float(pl.get_editor_property('weight')))
            for k in ('sample_time_offset', 'input_query_pose', 'component_stripping', 'origin_bone', 'permutation_time_type', 'color_preset_index'):
                try: nr.set_editor_property(k, pl.get_editor_property(k))
                except Exception: pass
            sub.append(nr); grp.set_editor_property('sub_channels', sub)
    try: s.modify()
    except Exception: pass
    assert EAL.save_asset(DST, False)
    s = u.load_asset(DST)
    def d(ch):
        r = [ch.get_class().get_name().replace('PoseSearchFeatureChannel_', ''), round(float(ch.get_editor_property('weight')), 3) if hasattr(ch, 'get_editor_property') and 'Group' not in ch.get_class().get_name() else None]
        try: r.append(str(ch.get_editor_property('bone').get_editor_property('bone_name')))
        except Exception: pass
        try: r.append([d(x) for x in ch.get_editor_property('sub_channels')])
        except Exception: pass
        return r
    out['schema'] = [d(x) for x in s.get_editor_property('channels')]
    n = 0; errs = []
    for e in range(96):
        p = '/Game/GraceRanger/SHME/Animations/V240/PSD_SHM240_E%02d' % e
        try:
            db = u.load_asset(p); db.set_editor_property('schema', s); assert EAL.save_asset(p, False); n += 1
        except Exception as ex: errs.append('%d %s' % (e, str(ex)[:100]))
    out['set'] = n; out['errors'] = errs
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
out['ok'] = DRY or (out.get('set') == 96 and not out.get('errors') and not out['dirty'])
print('SCH241 ' + json.dumps(out, default=str))
