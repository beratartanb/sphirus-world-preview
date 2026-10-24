"""datacontract226.py (editor job, read-only): which animation DATA the runtime reads from a clip, and what the authored reversal clips carry.
1. Clips: float curve names + notify names of the loops, the production pivots and the SHM225 reversal clips.
2. Consumers: every curve name referenced by the production ABPs (GetCurveValue nodes, curve-driven anim nodes: export_text 'CurveName'),
   the PoseSearch schema channels of the JR databases (curve channels would read clip curves), the AnimGraph nodes reading notifies
   (BranchIn is the database membership, not data). Prints DATACONTRACT226 {...}."""
import unreal as u, json, re
from editor_toolset.toolsets.blueprint import BlueprintTools as B
AL = u.AnimationLibrary; reg = u.AssetRegistryHelpers.get_asset_registry()
def find(name):
    for a in reg.get_assets_by_class(u.TopLevelAssetPath('/Script/Engine', 'AnimSequence'), True):
        if str(a.asset_name) == name: return str(a.package_name)
out = {'clips': {}, 'abp_curves': {}, 'schema': {}, 'notify_consumers': {}}
for n in ('A_RB_Jog_Rear', 'A_CT_Jog_Fwd', 'SHM_DPP_Jog_Bwd_Pivot', 'A_CP2_Jog_Fwd_Pivot', 'SHM224_Jog_Fwd_Pivot_M', 'SHM224_Jog_Bwd_Pivot_M', 'SHM225_JogRev_B_F_P6', 'SHM225_JogRev_F_B_P1'):
    p = find(n); seq = u.load_asset(p) if p else None
    if not seq: out['clips'][n] = 'missing'; continue
    try: curves = [str(c) for c in AL.get_animation_curve_names(seq, u.RawCurveTrackTypes.RCT_FLOAT)]
    except Exception as e: curves = 'ERR ' + str(e)[:60]
    try: nots = sorted(set(str(ev.notify_name) for ev in AL.get_animation_notify_events(seq)))
    except Exception as e: nots = 'ERR ' + str(e)[:60]
    try: syncs = [(str(m.marker_name), round(float(m.time), 3)) for m in seq.get_editor_property('authored_sync_markers')]
    except Exception as e: syncs = 'ERR ' + str(e)[:60]
    out['clips'][n] = {'curves': curves, 'notifies': nots, 'sync_markers': syncs, 'root_motion': str(seq.get_editor_property('enable_root_motion')), 'force_root_lock': str(seq.get_editor_property('force_root_lock'))}
for AP in ('/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase', '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching'):
    bp = u.load_asset(AP); names = {}
    for g in B.list_graphs(bp):
        try: nodes = B.find_nodes(g)
        except Exception: continue
        for nd in nodes:
            cn = nd.get_class().get_name(); txt = ''
            try: txt = nd.get_editor_property('node').export_text()
            except Exception: pass
            for m in re.findall(r'CurveName="?([A-Za-z0-9_]+)"?', txt): names.setdefault(m, set()).add(cn)
            if 'GetCurveValue' in cn or 'CurveValue' in str(getattr(nd, 'get_name', lambda: '')()):
                for pin in nd.get_editor_property('pins') if hasattr(nd, 'get_editor_property') else []:
                    try:
                        if str(pin.pin_name) == 'CurveName': names.setdefault(str(pin.default_value), set()).add('K2 GetCurveValue')
                    except Exception: pass
            if 'Notify' in cn or 'Notify' in txt[:200]: out['notify_consumers'].setdefault(AP.rsplit('/', 1)[-1], []).append((g.get_name(), cn))
    out['abp_curves'][AP.rsplit('/', 1)[-1]] = {k: sorted(v) for k, v in names.items()}
for db in ('/Game/GraceRanger/SHME/Animations/V224/PSD_SHM224_JogRevBwdO', '/Game/GraceRanger/SHME/Animations/V225/PSD_SHM225_JogRevBwd'):
    d = u.load_asset(db)
    if not d: out['schema'][db] = 'missing'; continue
    try:
        sch = d.get_editor_property('schema'); chans = sch.get_editor_property('channels')
        out['schema'][db.rsplit('/', 1)[-1]] = {'schema': sch.get_name(), 'channels': [c.get_class().get_name() + ':' + (c.export_text()[:160] if hasattr(c, 'export_text') else '') for c in chans]}
    except Exception as e: out['schema'][db.rsplit('/', 1)[-1]] = 'ERR ' + str(e)[:120]
print('DATACONTRACT226 ' + json.dumps(out, default=str))
