"""probe249_compressed.py (measure job, read-only): is the in-game (compressed) pose of the repaired turn clips the repaired raw data?
In game (v249a60 before the foot repair = v249n60/q60 after it) the left ball dips to -9 cm with the foot bent ~110 deg at the
TurnL135 crop entry, while the repaired raw data (clipdump) keeps it at -0.9 cm. Samples each repaired clip RAW vs COMPRESSED at
several times (component space): ball z, ankle z, foot pitch; also reports compression / data GUID state. Prints CMPPROBE249 {...}."""
import unreal as u, json, math
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
ar = u.AssetRegistryHelpers.get_asset_registry()
allseq = {str(a.asset_name): str(a.package_name) for a in ar.get_assets_by_class(u.TopLevelAssetPath('/Script/Engine', 'AnimSequence'), True)}
names = sorted(n for n, p in allseq.items() if p.startswith('/Game/GraceRanger/SHME/') and ((n.startswith('SHM248_Jog_Start_Turn') and n.endswith('_crop')) or (n.startswith('SHM_JogQ_af_Loco_Jog_Start_Turn'))))
out = {'clips': {}, 'api': {}}
def opts(kind):
    o = u.AnimPoseEvaluationOptions()
    try: o.set_editor_property('evaluation_type', getattr(u.AnimDataEvalType, kind))
    except Exception as e: out['api']['opt_' + kind] = str(e)[:120]
    return o
def comp(pose, b):
    tr = u.AnimPoseExtensions.get_bone_pose(pose, b, u.AnimPoseSpaces.WORLD); v = tr.translation; return (v.x, v.y, v.z)
for n in names:
    seq = u.load_asset(allseq[n]); L = seq.get_play_length(); rec = {'len': round(L, 3)}
    try: rec['guid'] = str(seq.get_editor_property('raw_data_guid')) if hasattr(seq, 'raw_data_guid') else 'n/a'
    except Exception as e: rec['guid'] = 'err'
    for kind in ('RAW', 'COMPRESSED'):
        rows = []
        for t in (0.0, 0.05, 0.1, 0.15, 0.2, 0.3):
            if t > L: continue
            try:
                p = u.AnimPoseExtensions.get_anim_pose_at_time(seq, t, opts(kind))
                fl = comp(p, 'foot_l'); bl = comp(p, 'ball_l'); fr = comp(p, 'foot_r'); br = comp(p, 'ball_r')
                pit = lambda a, b: round(math.degrees(math.atan2(a[2] - b[2], math.hypot(b[0] - a[0], b[1] - a[1]))), 1)
                rows.append([t, round(bl[2], 1), round(fl[2], 1), pit(fl, bl), round(br[2], 1), round(fr[2], 1), pit(fr, br)])
            except Exception as e:
                rows.append([t, 'err ' + str(e)[:100]])
        rec[kind] = rows
    out['clips'][n] = rec
print('CMPPROBE249 ' + json.dumps(out, default=str))
