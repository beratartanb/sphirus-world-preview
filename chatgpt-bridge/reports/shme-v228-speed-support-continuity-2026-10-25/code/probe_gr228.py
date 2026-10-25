"""probe_gr228.py (editor job, READ-ONLY): (a) BP_GR_MotionProfile variables (all names) + DA_GR_LocomotionBehavior values of the redirect /
friction knobs; (b) BP_GR_Player function graphs (names) and, for CalculateGroundFriction / CalculateMaxAcceleration / UpdateMovement_PreCMC,
the node class counts; (c) ABP_GR_MotionMatchingBase root motion mode; (d) the authored clip root track sampled every 0.1 s (designed
capsule displacement) for F_B_P4 and B_F_P3; (e) PoseSearch trajectory channel sample structs. Prints PROBEGR228 and writes
Saved/Codex/SHME_V228_20261025/probe_gr228.json. No save, no compile."""
import unreal as u, json, pathlib
out = {}
def props(o, names):
    d = {}
    for n in names:
        try: d[n] = str(o.get_editor_property(n))[:120]
        except Exception as e: d[n] = 'ERR'
    return d
pc = u.load_asset('/Game/GraceRanger/Profiles/BP_GR_MotionProfile')
try:
    names = [str(v.var_name) if hasattr(v, 'var_name') else str(v) for v in pc.get_editor_property('new_variables')]
except Exception as e:
    names = ['ERR ' + str(e)[:80]]
    try:
        cdo = u.get_default_object(pc.generated_class()); names = [p for p in dir(cdo) if 'redirect' in p.lower() or 'friction' in p.lower() or 'gr21' in p.lower() or 'gr22' in p.lower()]
    except Exception as e2: names.append('ERR2 ' + str(e2)[:80])
out['profile_vars'] = names[:200]
da = u.load_asset('/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior')
keys = [n for n in names if isinstance(n, str) and any(k in n for k in ('Redirect', 'Friction', 'GR21', 'GR22', 'Brake', 'Accel'))]
out['da_redirect_values'] = props(da, keys)
bp = u.load_asset('/Game/GraceRanger/BP_GR_Player')
try:
    fg = [g.get_name() for g in bp.get_editor_property('function_graphs')]; out['gr_functions'] = fg
except Exception as e: out['gr_functions'] = 'ERR ' + str(e)[:80]
try:
    B = u.BlueprintEditorLibrary
    for fn in ('CalculateGroundFriction', 'CalculateMaxAcceleration', 'UpdateMovement_PreCMC', 'GR_Impl_CP_PhysicalRedirect', 'GR_UpdateSHMSignals'):
        g = next((x for x in bp.get_editor_property('function_graphs') + bp.get_editor_property('ubergraph_pages') if x.get_name() == fn), None)
        if not g: out['fn_' + fn] = 'not found'; continue
        cls = {}
        for n in B.find_nodes(g) if hasattr(B, 'find_nodes') else []:
            c = n.get_class().get_name(); cls[c] = cls.get(c, 0) + 1
        out['fn_' + fn] = cls
except Exception as e: out['fn_err'] = str(e)[:120]
abp = u.load_asset('/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase')
try:
    cdo = u.get_default_object(abp.generated_class()); out['abp_root_motion_mode'] = str(cdo.get_editor_property('root_motion_mode'))
except Exception as e: out['abp_root_motion_mode'] = 'ERR ' + str(e)[:80]
for cp in ('/Game/GraceRanger/SHME/Animations/V226/SHM226_JogRev_F_B_P4', '/Game/GraceRanger/SHME/Animations/V226/SHM226_JogRev_B_F_P3', '/Game/GraceRanger/SHME/Animations/V226/SHM226_JogRev_F_B_P21'):
    seq = u.load_asset(cp)
    if not seq: continue
    L = float(seq.get_editor_property('sequence_length')); rows = []
    t = 0.0
    while t <= L + 1e-6:
        tr = u.AnimationLibrary.get_bone_pose_for_time(seq, 'root', t, False).translation; rows.append((round(t, 3), round(tr.x, 1), round(tr.y, 1), round(tr.z, 1))); t += 0.0333333
    out['root_' + cp.rsplit('_', 2)[-2] + '_' + cp.rsplit('_', 1)[-1]] = rows
    out['len_' + cp.rsplit('_', 1)[-1]] = L
db = u.load_asset('/Game/GraceRanger/SHME/Animations/V226/PSD_SHM226_JogRevFwd')
try:
    sch = db.get_editor_property('schema'); chans = []
    for c in sch.get_editor_property('channels'):
        cd = {'class': c.get_class().get_name()}
        try:
            smp = c.get_editor_property('samples'); cd['samples'] = [{k: str(s.get_editor_property(k))[:60] for k in ('offset', 'flags', 'weight') if True} for s in smp]
        except Exception as e: cd['samples_err'] = str(e)[:80]
        try: cd['sub'] = [x.get_class().get_name() for x in c.get_editor_property('sub_channels')]
        except Exception: pass
        chans.append(cd)
    out['schema_channels'] = chans
except Exception as e: out['schema_err'] = str(e)[:120]
pathlib.Path(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/SHME_V228_20261025/probe_gr228.json').write_text(json.dumps(out, indent=1, default=str), encoding='utf8')
print('PROBEGR228 ' + json.dumps({k: v for k, v in out.items() if not k.startswith('root_')}, default=str)[:2500])
