"""probe232.py (editor job, read-only): (1) owned backward / stop / start clips: length, root speed profile along the clip forward (+y) from
the root track (cm/s at 0 / 0.1 / 0.2 / 0.3 / 0.5 s), existing SHM226_V / SHM226_W / footspeed curves; (2) which PoseSearch databases list
them; (3) the ABP FootPlacement plant settings structs (CDO). Prints PROBE232 {...}."""
import unreal as u, json
AL = u.AnimationLibrary; EAL = u.EditorAssetLibrary; AR = u.AssetRegistryHelpers.get_asset_registry()
out = {'clips': {}, 'dbs': {}, 'plant': {}}
def root_y(seq, t):
    try:
        tr = AL.get_bone_pose_for_time(seq, 'root', t, False)
        return tr.translation.y
    except Exception as e: return None
names = []
for d in ('/Game/GraceRanger/SHME/Animations', '/Game/GraceRanger/Animations'):
    for a in AR.get_assets_by_path(d, recursive=True):
        n = str(a.asset_name)
        if str(a.asset_class_path.asset_name) == 'AnimSequence' and (('Bwd_Start' in n) or ('Back' in n and 'Start' in n) or n.startswith('SHM_JogQ')):
            names.append(str(a.package_name))
for p in names[:40]:
    s = u.load_asset(p); L = float(s.get_editor_property('sequence_length'))
    ys = {t: root_y(s, t) for t in (0.0, 0.1, 0.2, 0.3, 0.5, 0.7) if t <= L}
    vs = {}
    ks = sorted(ys)
    for i in range(1, len(ks)):
        a, b = ks[i - 1], ks[i]
        if ys[a] is not None and ys[b] is not None: vs['%.1f-%.1f' % (a, b)] = round((ys[b] - ys[a]) / (b - a), 1)
    cur = [str(c) for c in AL.get_animation_curve_names(s, u.RawCurveTrackTypes.RCT_FLOAT)]
    out['clips'][p.rsplit('/', 1)[-1]] = {'path': p, 'len': round(L, 3), 'root_v': vs, 'curves': [c for c in cur if c.startswith('SHM') or 'speed' in c.lower()][:12]}
for a in AR.get_assets_by_class(u.TopLevelAssetPath('/Script/PoseSearch', 'PoseSearchDatabase'), True):
    pk = str(a.package_name)
    if not pk.startswith('/Game/GraceRanger'): continue
    try:
        db = u.load_asset(pk); txt = db.export_text() if hasattr(db, 'export_text') else ''
    except Exception: continue
    hits = [n for n in out['clips'] if n in txt]
    if hits: out['dbs'][pk.rsplit('/', 1)[-1]] = hits
abp = u.load_asset('/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase')
cdo = u.get_default_object(abp.generated_class())
for n in ('PlantSettings_Default', 'PlantSettings_Walk', 'PlantSettings_Stops', 'PlantSettings_Landing'):
    try:
        st = cdo.get_editor_property(n)
        out['plant'][n] = {k: str(st.get_editor_property(k)) for k in ('speed_threshold', 'distance_to_ground', 'lock_type', 'unplant_radius', 'replant_radius_ratio', 'unplant_angle', 'unalignment_speed_threshold')}
    except Exception as e: out['plant'][n] = 'ERR ' + str(e)[:80]
print('PROBE232 ' + json.dumps(out, default=str))
# (4) tick order: the pawn's component templates (tick group, tick enabled) - the ABP reads SHME state one frame late (V2.31)
tk = {}
try:
    pc = u.load_asset('/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player').generated_class(); cdo_p = u.get_default_object(pc)
    for c in cdo_p.get_components_by_class(u.ActorComponent):
        try:
            t_ = c.get_editor_property('primary_component_tick'); tk[c.get_name()] = {'cls': c.get_class().get_name(), 'group': str(t_.get_editor_property('tick_group')), 'enabled': bool(t_.get_editor_property('start_with_tick_enabled'))}
        except Exception as e: tk[c.get_name()] = 'ERR ' + str(e)[:60]
    t_ = cdo_p.get_editor_property('primary_actor_tick'); tk['__actor'] = str(t_.get_editor_property('tick_group'))
except Exception as e: tk['err'] = str(e)[:120]
scs = {}
try:
    bpa = u.load_asset('/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent'); cc = u.get_default_object(bpa.generated_class()); t_ = cc.get_editor_property('primary_component_tick')
    scs = {'group': str(t_.get_editor_property('tick_group')), 'enabled': bool(t_.get_editor_property('start_with_tick_enabled')), 'interval': float(t_.get_editor_property('tick_interval'))}
except Exception as e: scs = 'ERR ' + str(e)[:80]
print('PROBE232TICK ' + json.dumps({'pawn': tk, 'shm_component_cdo': scs}, default=str))
