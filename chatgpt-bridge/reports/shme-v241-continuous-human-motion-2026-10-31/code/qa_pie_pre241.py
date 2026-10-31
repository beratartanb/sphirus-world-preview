import os
"""PIE-only QA run: start PIE, spawn the QA fixtures and the BP_LTP_QA protocol into the *game* world
(never the editor world, so the production map is never dirtied), end PIE on LTP_FINISHED/PBI_FINISHED
or timeout. Request: Saved/Codex/SHME_V1_20260925/run_request.json.
Each watcher owns exactly its own slate-tick handle (see runner-and-pitfalls: orphaned watchers)."""
import math, unreal as u, pathlib, json, time, builtins
P = pathlib.Path(u.Paths.project_dir()); N = P / 'Saved/Codex/SHME_V1_20260925'
F = '/Game/GraceRanger/Experimental/BodyInertia'
req = json.loads((N / 'run_request.json').read_text()); label = req['label']; timeout = req.get('timeout', 420)
LOG = max([f for f in (P / 'Saved/Logs').glob('*.log') if not f.name.lower().startswith('cef')], key=lambda f: f.stat().st_mtime); start_size = LOG.stat().st_size
les = u.get_editor_subsystem(u.LevelEditorSubsystem); ed = u.get_editor_subsystem(u.UnrealEditorSubsystem)
assert ed.get_game_world() is None, 'PIE already running'

# ---- V2.26 run state (replaces the schema-default reset): two modes.
#   "state_mode": "production" - the SAVED production state runs unchanged (only TelemetryEnabled is forced on; no flag of any kind applied).
#   "state_mode": "candidate" (default) - production + exactly this run's explicit overrides (behavior_flags / pbi_flags / pawn_flags /
#   shme_flags / abp_flags). Overrides never carry into the next run: every key a run touches is restored to its production value
#   (captured the first time the key is touched in this editor session, i.e. the value loaded from disk) before the next run applies its own.
#   A schema default is NOT production. The effective state (every touched key + a fixed identity set: SHME DA fields, the ABP database
#   references, the cvars) is recorded at run start and at run end into <label>_pie.json; a mismatch marks the run INVALID_STATE.
import sys, importlib; sys.path.insert(0, str(P / 'Tools/SHME_V1_20260925')); import shm_profiles; importlib.reload(shm_profiles)
MODE = req.get('state_mode', 'candidate'); assert MODE in ('production', 'candidate'), MODE
_shm = u.load_asset('/Game/GraceRanger/SHME/DA_SHM_Response_Default')
_ABPS = ['/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching', '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase']
_PAWNS = ['/Game/GraceRanger/BP_GR_Player', F + '/BP_PBI_Player']
def _obj(cat, path):
    if cat in ('abp', 'pawn'): return u.get_default_object(u.load_asset(path).generated_class())
    return u.load_asset(path)
_TARGETS = {'behavior': ['/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior'], 'pbi': [F + '/DA_PBI_Prototype'], 'shme': ['/Game/GraceRanger/SHME/DA_SHM_Response_Default'], 'abp': _ABPS, 'pawn': _PAWNS}
def _norm(v):
    if hasattr(v, 'get_path_name') and not isinstance(v, str): return v.get_path_name()
    if hasattr(v, 'x') and hasattr(v, 'z'): return [round(v.x, 4), round(v.y, 4), round(v.z, 4)]
    if hasattr(v, 'roll'): return [round(v.roll, 4), round(v.pitch, 4), round(v.yaw, 4)]
    return round(v, 6) if isinstance(v, float) else v
TOUCHED = getattr(builtins, 'SHM_PROD_TOUCHED', None)
if TOUCHED is None:   # first run of this editor session: the loaded values ARE the saved production (a fresh editor); refuse a dirty base
    _dirty = [p_.get_name() for p_ in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
    _bad = [n_ for n_ in _dirty if any(n_ == t_ for ts in _TARGETS.values() for t_ in ts)]
    if _bad: u.log_error('SHM_STATE: dirty base packages at first run ' + str(_bad))
    TOUCHED = {c_: {} for c_ in _TARGETS}; builtins.SHM_PROD_TOUCHED = TOUCHED; builtins.SHM_PROD_DIRTY_BASE = _bad
def _gp(o_, key):   # V2.31: 'cm.<prop>' = the CharacterMovement component template of a pawn class (CMC perch / step settings as candidates)
    if key.startswith('cm.'): return o_.get_editor_property('character_movement').get_editor_property(key[3:])
    if '.' in key:   # V2.32: '<struct var>.<field>' (e.g. PlantSettings_Walk.unplant_angle on the ABP CDO; restored per field)
        s_, f_ = key.split('.', 1); return o_.get_editor_property(s_).get_editor_property(f_)
    return o_.get_editor_property(key)
def _sp(o_, key, v):
    if key.startswith('cm.'): o_.get_editor_property('character_movement').set_editor_property(key[3:], v)
    elif '.' in key:
        s_, f_ = key.split('.', 1); st_ = o_.get_editor_property(s_); st_.set_editor_property(f_, v); o_.set_editor_property(s_, st_)
    else: o_.set_editor_property(key, v)
def _restore():
    for cat, keys in TOUCHED.items():
        for key, vals in keys.items():
            for path, v0 in vals.items(): _sp(_obj(cat, path), key, u.load_asset(v0) if isinstance(v0, str) and v0.startswith('/Game/') else v0)
def _apply(cat, flags):
    # V2.33: record EVERY target's original first, then set (two passes): a child Blueprint CDO (BP_PBI_Player) inherits a parent CDO change
    # (BP_GR_Player) at once, so a single pass recorded the child's 'original' AFTER the parent was set -> the restore kept the candidate
    # value in the child = the pawn (GR233_RecMouseScale leaked from the Qp runs into the next Q runs, F30 2026-10-27)
    for key, val in (flags or {}).items():
        if key not in TOUCHED[cat]: TOUCHED[cat][key] = {}
        for path in _TARGETS[cat]:
            if path not in TOUCHED[cat][key]: TOUCHED[cat][key][path] = _norm(_gp(_obj(cat, path), key))
        for path in _TARGETS[cat]:
            _sp(_obj(cat, path), key, u.load_asset(val) if isinstance(val, str) and val.startswith('/Game/') else val)
_restore()
if MODE == 'candidate':
    _apply('behavior', req.get('behavior_flags')); _apply('pbi', req.get('pbi_flags')); _apply('pawn', req.get('pawn_flags'))
    _apply('shme', req.get('shme_flags')); _apply('abp', req.get('abp_flags'))
else:
    for k_ in ('behavior_flags', 'pbi_flags', 'pawn_flags', 'shme_flags', 'abp_flags'):
        if req.get(k_): u.log_warning('SHM_STATE: production mode ignores ' + k_ + ' ' + str(list(req[k_])[:6]))
_shm.set_editor_property('TelemetryEnabled', True)
_IDENT_ABP = ['SHM236_DB_JogStop', 'SHM224_JRMode', 'SHM224_DB_JRFwd', 'SHM224_DB_JRBwd', 'SHM224_DB_JRLat', 'SHM224_DB_JRFwdM', 'SHM224_DB_JRBwdM', 'SHM_RedirectDB_JR', 'SHM223_RevRearGate', 'SHM28_StartMode', 'SHM28_StartL', 'SHM28_StartR', 'SHM225_SWAlpha', 'SHM225_OWAlpha', 'SHM220_RecHold', 'SHM221_RecThrottle']
def state_record():
    rec = {'mode': MODE, 'dirty_base': getattr(builtins, 'SHM_PROD_DIRTY_BASE', []), 'shme': {}, 'abp': {}, 'behavior': {}, 'pbi': {}, 'pawn': {}, 'console': list(req.get('console', [])), 'db': {}}
    for key, typ, dflt, cat in shm_profiles.RESPONSE:
        try: rec['shme'][key] = _norm(_shm.get_editor_property(key))
        except Exception: rec['shme'][key] = 'err'
    for cat in ('behavior', 'pbi', 'pawn', 'abp'):
        keys = set(TOUCHED[cat]) | (set(_IDENT_ABP) if cat == 'abp' else set())
        for key in sorted(keys):
            for path in _TARGETS[cat]:
                try: rec[cat][key + '@' + path.rsplit('/', 1)[-1]] = _norm(_gp(_obj(cat, path), key))
                except Exception: rec[cat][key + '@' + path.rsplit('/', 1)[-1]] = 'err'
    try:   # database identity: asset path + package file time + entry count (a rebuilt or edited database changes these)
        cdo_ = _obj('abp', _ABPS[1])
        for key in ('SHM224_DB_JRFwd', 'SHM224_DB_JRBwd', 'SHM224_DB_JRLat', 'SHM224_DB_JRFwdM', 'SHM224_DB_JRBwdM', 'SHM_RedirectDB_JR', 'SHM236_DB_JogStop'):
            db_ = cdo_.get_editor_property(key)
            if db_:
                pk_ = db_.get_path_name().split('.')[0]; fn_ = P / ('Content' + pk_[len('/Game'):] + '.uasset')
                try: n_ = len(db_.get_editor_property('animation_assets'))
                except Exception: n_ = -1
                rec['db'][key] = {'asset': pk_, 'mtime': int(fn_.stat().st_mtime) if fn_.exists() else None, 'entries': n_}
    except Exception as e: rec['db']['err'] = str(e)[:120]
    return rec
STATE0 = state_record(); u.log('SHM_STATE %s touched %s' % (MODE, {c_: sorted(k) for c_, k in TOUCHED.items() if k}))
SHM_CLS = u.load_asset('/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent').generated_class()

# same as the previous harness: a background editor window is otherwise throttled to a few FPS during PIE
u.get_default_object(u.load_class(None, '/Script/UnrealEd.EditorPerformanceSettings')).set_editor_property('bThrottleCPUWhenNotForeground', False)
CUBE = u.load_asset('/Engine/BasicShapes/Cube')
def spawn(world, cls, loc, props=None):
    """Spawn into the GAME world via the PIE cheat 'summon' (Python exposes no game-world spawn), then configure.
    BP_LTP_QA waits 1.5 s after BeginPlay before reading its settings, so post-spawn configuration is in time."""
    pc = u.GameplayStatics.get_player_controller(world, 0)
    path = cls.static_class().get_path_name() if isinstance(cls, type) else cls.get_path_name()
    before = set(a.get_path_name() for a in u.GameplayStatics.get_all_actors_of_class(world, cls))
    u.SystemLibrary.execute_console_command(world, 'summon ' + (path if path.startswith('/Game/') else path.rsplit('.', 1)[-1]), pc)
    new = [a for a in u.GameplayStatics.get_all_actors_of_class(world, cls) if a.get_path_name() not in before]
    assert len(new) == 1, ('summon failed', path, len(new))
    a = new[0]
    root = a.get_editor_property('root_component')
    if root: root.set_mobility(u.ComponentMobility.MOVABLE)
    a.set_actor_location(loc, False, True)
    for k, v in (props or {}).items(): a.set_editor_property(k, v, u.PropertyAccessChangeNotifyMode.NEVER)
    return a
def box(world, name, x, y, z, sx, sy, sz, hidden=False, collide=True):
    a = spawn(world, u.StaticMeshActor, u.Vector(x, y, z))
    if name.startswith('INS_'):
        try: a.rename(name)   # V2.25: object name = what GetDisplayName returns in a packaged build
        except Exception as e_: u.log_warning('INS rename: ' + str(e_))
        try: a.set_actor_label(name)   # V2.25 t7: in editor/PIE GetDisplayName returns the actor LABEL (a runtime-spawned actor's label defaults to 'StaticMeshActor')
        except Exception as e_: u.log_warning('INS label: ' + str(e_))
    c = a.static_mesh_component; c.set_static_mesh(CUBE)
    a.set_actor_scale3d(u.Vector(sx / 100, sy / 100, sz / 100)); c.set_collision_profile_name('BlockAll')
    a.set_actor_hidden_in_game(hidden); a.set_actor_enable_collision(collide); a.tags = [u.Name('SHM_QA_' + name)] + ([u.Name('GR_Inspect')] if name.startswith('INS_') else [])   # V2.25: inspectable test props
    return a

def build(world):
    suite = req.get('suite', 0)
    HOUSE = bool(req.get('house', False)); ORIGIN = req.get('origin', [7000, 0, -500])
    if not HOUSE: box(world, 'Floor', 7000, 0, -12, 60000, 60000, 20)
    # V2.9: test surfaces [name, x, y, z, sx, sy, sz, pitch, yaw, roll] (transient, PIE world only)
    for b_ in req.get('boxes', []):
        a_ = box(world, str(b_[0]), *[float(v_) for v_ in b_[1:7]])
        if len(b_) > 7: a_.set_actor_rotation(u.Rotator(roll=float(b_[9]) if len(b_) > 9 else 0.0, pitch=float(b_[7]), yaw=float(b_[8]) if len(b_) > 8 else 0.0), False)
    if HOUSE: suite_fixtures = False
    if suite == 6 and not HOUSE:
        for i in range(12):
            h = (i + 1) * 20; box(world, 'Step_%d' % i, 7180 + (i + .5) * 35, 0, -2 + h / 2, 35, 260, h)
        box(world, 'UpperLanding', 7925, 0, 118, 650, 260, 240)
    if suite == 7 and not HOUSE: box(world, 'ImpactWall', 7600, 3000, 198, 20, 4000, 400)
    if suite == 8 and not HOUSE:
        box(world, 'CorridorLeft', 7450, 3895, 148, 1100, 20, 300); box(world, 'CorridorRight', 7450, 4105, 148, 1100, 20, 300)
        box(world, 'CorridorEnd', 8010, 4000, 148, 20, 230, 300); box(world, 'CorridorRoof', 7450, 4000, 308, 1100, 230, 20)
        box(world, 'OuterCorner', 8090, 4250, 148, 180, 320, 300)
    CAMOFF = req.get('cam_offset', [-300, -330, 680])
    cam = spawn(world, u.CameraActor, u.Vector(ORIGIN[0] + CAMOFF[0], ORIGIN[1] + CAMOFF[1], ORIGIN[2] + CAMOFF[2])); cam.get_components_by_class(u.CameraComponent)[0].set_editor_property('field_of_view', 52); st['obs_cam'] = cam
    props = {'Suite': suite, 'RunLabel': label, 'PBIEnabled': req['enabled'], 'SmokeOnly': req.get('smoke', False), 'Observer': cam,
             'GameplayCamera': req.get('gameplay', True), 'RecordVideo': req.get('record', True)}
    if req.get('fps') is not None: props['CaptureMaxFPS'] = float(req['fps'])
    # house mode: the protocol's hard-coded teleport points (7000,0,86.15 = QA floor + capsule) are shifted to ORIGIN
    if HOUSE: props['WorldOffset'] = u.Vector(ORIGIN[0] - 7000, ORIGIN[1] - 0, ORIGIN[2] - 86.15)
    if 'gait' in req: props['MatrixGait'] = float(req['gait'])
    if req.get('regression', False):
        props['RegressionOnly'] = True
        props['TestRoof'] = box(world, 'Roof', 7000, 0, 250, 1200, 1200, 20, hidden=True, collide=False)
        props['TestWall'] = box(world, 'Wall', 7400, 0, 150, 20, 800, 300, hidden=True, collide=False)
    if not NO_LTP: spawn(world, u.load_asset(F + '/BP_LTP_QA').generated_class(), u.Vector(ORIGIN[0], ORIGIN[1], ORIGIN[2]), props)
    st['yaw0'] = None
    if NO_LTP: st['rec'] = True
    # 1x capture: run the game at slomo S while screenshots fire every `shots` seconds of wall time -> one frame per shots*S of game time
    if req.get('slomo'): u.GameplayStatics.set_global_time_dilation(world, float(req['slomo']))
    # V1.3.1 closure: protocol-less runs start at ORIGIN (house) or on the QA floor, BEFORE the observer camera aims
    if NO_LTP:
        pw_ = u.GameplayStatics.get_player_character(world, 0)
        if pw_: pw_.set_actor_location(u.Vector(ORIGIN[0], ORIGIN[1], ORIGIN[2]) if HOUSE else u.Vector(7000, 0, 86.15), False, True)
    if NO_LTP and not req.get('gameplay', True):
        try:
            pw0 = u.GameplayStatics.get_player_character(world, 0)
            if pw0: cam.set_actor_rotation(u.MathLibrary.find_look_at_rotation(cam.get_actor_location(), pw0.get_actor_location() + u.Vector(0, 0, 20)), False)
            u.GameplayStatics.get_player_controller(world, 0).set_view_target_with_blend(cam, 0.0)
        except Exception as e: u.log_warning('observer view target failed: ' + str(e)); u.SystemLibrary.execute_console_command(world, 't.MaxFPS %d' % int(req.get('fps', 30)))
    # V1.3.1 closure: open named hinged doors (BP_SphirusHinged: R4_IsOpen, interpolated by its tick) in the PIE world only
    for lab_ in req.get('open_doors', []):
        for a_ in u.GameplayStatics.get_all_actors_of_class(world, u.load_asset('/Game/SphirusHouse/Playable_R04/Blueprints/BP_SphirusHinged').generated_class()):
            if a_.get_actor_label() == lab_:
                try: a_.set_editor_property('R4_IsOpen', True); u.log('SHM_QA door opened ' + lab_)
                except Exception as e_: u.log_warning('door open failed %s: %s' % (lab_, e_))
    pawn = u.GameplayStatics.get_player_character(world, 0)
    # V1.3.4 true-FPS capture: Take Recorder records the pawn and a cine camera that mirrors the gameplay camera each tick;
    # the take is rendered afterwards by render_take.py at a fixed frame rate (Sequencer legacy capture, AVI / PNG)
    if req.get('take'):
        cine = spawn(world, u.CineCameraActor, u.Vector(ORIGIN[0], ORIGIN[1], ORIGIN[2] + 100)); cine.set_actor_label('SHM_TakeCam_' + label)
        cc = cine.get_cine_camera_component(); fs = cc.get_editor_property('focus_settings'); fs.set_editor_property('focus_method', u.CameraFocusMethod.DISABLE); cc.set_editor_property('focus_settings', fs)
        st['take'] = {'cam': cine, 'on': False, 'start': float(req['take'].get('start', 1.0)), 'fps': int(req['take'].get('fps', 60)), 'seq': None}
    # V1.3.1 closure: protocol-less runs in the house start at ORIGIN (capsule centre) facing yaw0 (control yaw driven by the loop)
    # NEVER notify: an edit notification on a pawn component re-runs the pawn construction script in PIE and
    # TRASHes its camera/boom components (AAMS BP_Timeline then logs TRASH_ errors and camera data is invalid)
    for c in pawn.get_components_by_class(SHM_CLS): c.set_editor_property('TelemetryLabel', label, u.PropertyAccessChangeNotifyMode.NEVER)
    # V2.31: PIE-only CharacterMovement overrides on the SPAWNED pawn (BP_Player_MM; the class CDO / templates are never touched): request
    # 'live_cm' {prop: value}, e.g. the perch settings for the step-down study; NEVER notify (no construction script in PIE)
    # V2.31 determinism study: log the pawn meshes' visibility-based anim tick / update-rate optimisation settings; request 'live_anim'
    # {'always_tick': true} forces AlwaysTickPoseAndRefreshBones + URO off on the SPAWNED pawn only (PIE world, NEVER notify)
    try:
        _la = req.get('live_anim') or {}
        for c_ in pawn.get_components_by_class(u.SkeletalMeshComponent):
            vb_ = c_.get_editor_property('visibility_based_anim_tick_option'); uro_ = c_.get_editor_property('enable_update_rate_optimizations')
            u.log('SHM_QA_ANIMTICK %s vis=%s uro=%s' % (c_.get_name(), vb_, uro_))
            if _la.get('always_tick'):
                c_.set_editor_property('visibility_based_anim_tick_option', u.VisibilityBasedAnimTickOption.ALWAYS_TICK_POSE_AND_REFRESH_BONES, u.PropertyAccessChangeNotifyMode.NEVER)
                c_.set_editor_property('enable_update_rate_optimizations', False, u.PropertyAccessChangeNotifyMode.NEVER)
    except Exception as e_: u.log_warning('live_anim failed: ' + str(e_))
    for k_, v_ in (req.get('live_cm') or {}).items():
        try: pawn.get_editor_property('character_movement').set_editor_property(k_, v_, u.PropertyAccessChangeNotifyMode.NEVER); u.log('SHM_QA_LIVECM %s=%s' % (k_, v_))
        except Exception as e_: u.log_warning('live_cm failed %s: %s' % (k_, e_))
    # V2.32 tick-order study (request 'live_tick' {'shm_pre': true}, SPAWNED pawn only, assets untouched): the SHME component ticks in
    # TG_PrePhysics after the CharacterMovement and the pawn's skeletal meshes tick after it -> the ABP reads THIS frame's SHME routing
    # (production: SHME in TG_PostPhysics, the ABP one frame behind = the one-frame selection blips at authored-clip ends / starts)
    _lt = req.get('live_tick') or {}
    if _lt.get('shm_pre'):
        try:
            shc_ = [c_ for c_ in pawn.get_components_by_class(u.ActorComponent) if 'SHM_HumanMotion' in c_.get_class().get_name()][0]
            cmv_ = pawn.get_editor_property('character_movement')
            shc_.set_tick_group(u.TickingGroup.TG_PRE_PHYSICS); shc_.add_tick_prerequisite_component(cmv_)
            for c_ in pawn.get_components_by_class(u.SkeletalMeshComponent): c_.add_tick_prerequisite_component(shc_)
            u.log('SHM_QA_LIVETICK shm_pre ok (%d meshes)' % len(pawn.get_components_by_class(u.SkeletalMeshComponent)))
        except Exception as e_: u.log_warning('live_tick failed: ' + str(e_))
    # V2.32 plant-settings study (request 'live_plant' {'PlantSettings_Walk': {'unplant_angle': 120.0}, ...}, the SPAWNED pawn's anim
    # instances only, assets untouched): FootPlacement reads these structs through the Get_FootPlacementPlantSettings binding every update
    for sn_, fields_ in (req.get('live_plant') or {}).items():
        try:
            n_ok = 0
            for c_ in pawn.get_components_by_class(u.SkeletalMeshComponent):
                ai_ = c_.get_anim_instance()
                if ai_ is None: continue
                try: s_ = ai_.get_editor_property(sn_)
                except Exception: continue
                for fk_, fv_ in fields_.items(): s_.set_editor_property(fk_, fv_)
                ai_.set_editor_property(sn_, s_, u.PropertyAccessChangeNotifyMode.NEVER); n_ok += 1
            u.log('SHM_QA_LIVEPLANT %s %s on %d instances' % (sn_, fields_, n_ok))
        except Exception as e_: u.log_warning('live_plant failed %s: %s' % (sn_, e_))
    # V2.9: neutral test light - point lights attached to the pawn [dx, dy, dz, intensity, radius] (no shadows, PIE only)
    for l_ in req.get('fill_lights', []):
        try:
            la = spawn(world, u.PointLight, pawn.get_actor_location() + u.Vector(float(l_[0]), float(l_[1]), float(l_[2])))
            lc = la.point_light_component; lc.set_editor_property('intensity', float(l_[3])); lc.set_editor_property('attenuation_radius', float(l_[4]) if len(l_) > 4 else 2000.0)
            lc.set_editor_property('cast_shadows', False); la.attach_to_actor(pawn, u.Name(''), u.AttachmentRule.KEEP_WORLD, u.AttachmentRule.KEEP_WORLD, u.AttachmentRule.KEEP_WORLD, False)
        except Exception as e_: u.log_warning('fill light failed: ' + str(e_))
    # V2.10 diagnostic test look (PIE world only, assets untouched): the pawn's skeletal-mesh components whose name contains one of
    # test_look.components get an opaque neutral material on every slot (default the project QA clay) - the body under the garments
    # reads as grey instead of skin where the garment is pierced; garments / face / grooms keep the production look unless listed
    TL_ = req.get('test_look')
    if TL_:
        try:
            mat_ = u.load_asset(TL_.get('material', '/Game/Sphirus/CharacterLab/HeadMetaHuman_20260928/Diagnostics/M_QA_Clay')); nset_ = []
            for c_ in pawn.get_components_by_class(u.SkeletalMeshComponent):
                if any(k_.lower() == c_.get_name().lower() for k_ in TL_.get('components', ['Manny'])):
                    for i_ in range(c_.get_num_materials()): c_.set_material(i_, mat_)
                    nset_.append('%s:%d' % (c_.get_name(), c_.get_num_materials()))
            u.log('SHM_QA_TESTLOOK ' + ','.join(nset_))
        except Exception as e_: u.log_warning('test look failed: ' + str(e_))
    u.log('SHM_QA_SPAWNED ' + label)

st = {'t': time.monotonic(), 'phase': 'wait', 'pos': start_size, 'shot': 0, 'n': 0, 'dead': False}
# V1.3.7 real-time capture: MediaIOFramework FileMediaOutput on the active (PIE) viewport, every rendered frame, JPEG,
# game capped at MCAP['fps'] (real simulation, no time dilation); frames -> Saved/Codex/SHME_V138_20260927/Video/<label>
MCAP = req.get('mcap')
TRACK = req.get('track_cam')
def track_step(gw, dt_):
    pw_ = u.GameplayStatics.get_player_character(gw, 0)
    if not pw_: return
    pc_ = u.GameplayStatics.get_player_controller(gw, 0)
    if 'track' not in st:
        cam_ = st.get('obs_cam')
        if not cam_: u.log_warning('SHM_TRACK: no observer camera'); st['track'] = None; return
        try: cam_.get_components_by_class(u.CameraComponent)[0].set_editor_property('field_of_view', float(TRACK.get('fov', 55)))
        except Exception: pass
        pc_.set_view_target_with_blend(cam_, 0.0); st['track'] = {'cam': cam_, 'pos': None}
    tr_ = st.get('track')
    if not tr_: return
    v_ = pw_.get_velocity(); sp = (v_.x * v_.x + v_.y * v_.y) ** 0.5
    yaw = math.radians(pw_.get_actor_rotation().yaw) if sp < 30 else math.atan2(v_.y, v_.x)
    # V2.9: world_yaw = fixed world orientation of the offset frame (the camera translates with the pawn but never swings
    # round during a turn: side / diagonal leg views stay comparable through cuts and reversals)
    if TRACK.get('world_yaw') is not None: yaw = math.radians(float(TRACK['world_yaw']))
    f_ = (math.cos(yaw), math.sin(yaw)); r_ = (-f_[1], f_[0])
    L_ = pw_.get_actor_location(); hh = pw_.capsule_component.get_scaled_capsule_half_height(); base = L_.z - hh
    want = (L_.x + r_[0] * float(TRACK.get('side', 320)) - f_[0] * float(TRACK.get('back', 120)), L_.y + r_[1] * float(TRACK.get('side', 320)) - f_[1] * float(TRACK.get('back', 120)), base + float(TRACK.get('up', 60)))
    if tr_['pos'] is None: tr_['pos'] = want
    # V2.8: "fixed" = the camera position is frozen once the capture is running (side / three-quarter contact views of a start or
    # stop); it only pans to keep the pawn framed. Without it the camera follows with `lag`.
    if TRACK.get('fixed') and st.get('mcap') and not st['mcap'].get('err'):
        tr_.setdefault('frozen', tr_['pos']); tr_['pos'] = tr_['frozen']
    else:
        a_ = 1.0 - math.exp(-dt_ / max(float(TRACK.get('lag', 0.25)), 0.01)); tr_['pos'] = tuple(p0 + (w - p0) * a_ for p0, w in zip(tr_['pos'], want))
    tgt = (L_.x, L_.y, base + float(TRACK.get('look_z', 55)))
    d_ = (tgt[0] - tr_['pos'][0], tgt[1] - tr_['pos'][1], tgt[2] - tr_['pos'][2])
    rot = u.Rotator(roll=0.0, pitch=math.degrees(math.atan2(d_[2], math.hypot(d_[0], d_[1]))), yaw=math.degrees(math.atan2(d_[1], d_[0])))
    tr_['cam'].set_actor_location_and_rotation(u.Vector(*tr_['pos']), rot, False, True)
def mcap_start(gw):
    try:
        vd = P / 'Saved/Codex/SHME_V138_20260927/Video' / label; vd.mkdir(parents=True, exist_ok=True)
        for f_ in vd.glob('*.jpg'): f_.unlink()
        u.SystemLibrary.execute_console_command(gw, 't.MaxFPS %d' % int(MCAP.get('fps', 30)))
        out_ = u.FileMediaOutput(); out_.set_editor_property('file_path', u.DirectoryPath(path=str(vd)))
        out_.set_editor_property('base_file_name', 'f')
        try:
            wo = out_.get_editor_property('write_options'); wo.set_editor_property('format', u.DesiredImageFormat.JPG)
            wo.set_editor_property('compression_quality', int(MCAP.get('quality', 85))); wo.set_editor_property('async_', True); out_.set_editor_property('write_options', wo)
        except Exception as e_: u.log_warning('SHM_MCAP write options: ' + str(e_))
        if MCAP.get('size'):
            out_.set_editor_property('override_desired_size', True); out_.set_editor_property('desired_size', u.IntPoint(int(MCAP['size'][0]), int(MCAP['size'][1])))
        # V1.3.7 safety: FileMediaOutput needs tightly packed rows (width * 4 bytes a multiple of 256); an unaligned PIE
        # viewport (e.g. 1523 px) raised 'only supports tightly packed rows' and then crashed the editor in MediaIOCore twice
        try: vs_ = u.WidgetLayoutLibrary.get_viewport_size(gw); vw_, vh_ = int(round(vs_.x)), int(round(vs_.y))
        except Exception: vw_, vh_ = -1, -1
        crop_ = MCAP.get('crop')   # [w, h]: centre crop to an aligned size (a copy region, no resize pass)
        cw_ = int(crop_[0]) if crop_ else vw_
        if vw_ <= 0 or cw_ % 64 != 0 or (crop_ and (int(crop_[0]) > vw_ or int(crop_[1]) > vh_)):
            st['mcap'] = {'err': 'capture width %d (viewport %dx%d) not a multiple of 64 or crop larger than the viewport - refused (MediaIOCore crash guard)' % (cw_, vw_, vh_), 'viewport': [vw_, vh_]}
            u.log_warning('SHM_MCAP refused: viewport %dx%d crop %s' % (vw_, vh_, crop_)); return
        if crop_:
            out_.set_editor_property('override_desired_size', True); out_.set_editor_property('desired_size', u.IntPoint(int(crop_[0]), int(crop_[1])))
        cap = out_.create_media_capture(); opts = u.MediaCaptureOptions()
        if crop_: opts.set_editor_property('crop', u.MediaCaptureCroppingType.CENTER)
        # V1.3.7: native viewport size only - RESIZE_IN_CAPTURE_PASS is rejected by FileMediaOutput (conversion op) and stops the capture
        if MCAP.get('size'):
            try: opts.set_editor_property('resize_method', u.MediaCaptureResizeMethod.RESIZE_IN_CAPTURE_PASS)
            except Exception: pass
        ok = cap.capture_active_scene_viewport(opts)
        st['mcap'] = {'cap': cap, 'out': out_, 'dir': str(vd), 't0': u.GameplayStatics.get_time_seconds(gw), 'w0': time.monotonic(), 'ticks': 0, 'ok': bool(ok)}
        u.log('SHM_MCAP start %s ok=%s' % (label, ok))
    except Exception as e:
        st['mcap'] = {'err': str(e)}; u.log_error('SHM_MCAP start failed: ' + str(e))
def mcap_stop(gw=None):
    m_ = st.get('mcap')
    if not m_ or 'cap' not in m_ or m_.get('stopped'): return
    try: m_['cap'].stop_capture(True)
    except Exception as e: u.log_error('SHM_MCAP stop failed: ' + str(e))
    m_['stopped'] = True; m_['wall'] = round(time.monotonic() - m_['w0'], 3)
    try: m_['game'] = round(u.GameplayStatics.get_time_seconds(gw) - m_['t0'], 3) if gw else None
    except Exception: m_['game'] = None
    u.log('SHM_MCAP stop %s ticks=%d wall=%s game=%s' % (label, m_['ticks'], m_['wall'], m_.get('game')))
SH = req.get('shots', 0)
# V1.3.2 turn-in-place test: a deterministic control-yaw schedule driven by the harness (no movement input).
# yaw: {'start': 3.0, 'hold': 2.0, 'steps': [30, 60, 90, 135, 180, -30, ...], 'sweep': [rate_deg_s, seconds]} ; no_ltp: run without the protocol
YAW = req.get('yaw'); NO_LTP = bool(req.get('no_ltp', False))
# V1.3.1 closure: protocol-less movement through the same Enhanced Input console injection the protocol actor uses.
# move: {'start': 2.0, 'gait': 'walk'|'jog'|'sprint', 'segments': [[seconds, input_angle_deg], ...], 'stop': 1.5}; angle 0 = forward
# (Y), 90 = right (X), relative to the control rotation; gait pressed 1 s before start (tap = jog, 0.45 s hold = sprint).
LOOK_IA = req.get('look') == 'ia'; IA_LOOK = '/Game/AAMS/Demo/MotionMatching/Input/IA_Look.IA_Look'
MOVE = req.get('move'); IA_MOVE = '/Game/AAMS/Demo/MotionMatching/Input/IA_Move.IA_Move'; IA_GAIT = '/Game/ActionAdventureMovementS/Input/IA_Ranger_GaitShift.IA_Ranger_GaitShift'
def key_step(gw, gt):
    """V2.12 real-key path: move.keys = [[dt, key, 1|0], ...] relative to move.start, sent as Enhanced Input forced KEYS (Input.+key /
    Input.-key) so they go through the player's mapping context (W/S/A/D -> IA_Move with its modifiers, LeftShift -> IA_Ranger_GaitShift).
    Overlapping W+S therefore sums to zero exactly like a keyboard. Stage label mv_kb[s]_<angle of held WASD | rel>_<event index>."""
    cmd = lambda c: u.SystemLibrary.execute_console_command(gw, c)
    t0 = float(MOVE.get('start', 2.0)); ev = sorted(MOVE['keys'], key=lambda e: float(e[0])); stop = float(MOVE.get('stop', 1.5))
    held = st.setdefault('held', set())
    if gt < t0: return 'mv_pre', False
    t = gt - t0; n = st.setdefault('kev', 0)
    while n < len(ev) and float(ev[n][0]) <= t:
        k_, d_ = str(ev[n][1]), int(ev[n][2])
        if d_: cmd('Input.+key %s true' % k_); held.add(k_)
        else: cmd('Input.-key %s' % k_); held.discard(k_)
        u.log('SHM_KEY %s %s %.3f' % ('+' if d_ else '-', k_, t)); n += 1; st['kev'] = n
    # V2.39: optional external pushes [[dt, vx, vy], ...] (world cm/s, velocity change) through CharacterMovement.AddImpulse - a real,
    # unplanned velocity change (no falling mode, unlike LaunchCharacter); logged as SHM_PUSH
    pe = MOVE.get('pushes') or []; pn_ = st.setdefault('pev', 0)
    while pn_ < len(pe) and float(pe[pn_][0]) <= t:
        try:
            pw = u.GameplayStatics.get_player_pawn(gw, 0); cm = pw.get_component_by_class(u.CharacterMovementComponent)
            cm.add_impulse(u.Vector(float(pe[pn_][1]), float(pe[pn_][2]), 0.0), True); u.log('SHM_PUSH %.1f %.1f %.3f' % (float(pe[pn_][1]), float(pe[pn_][2]), t))
        except Exception as e_: u.log('SHM_PUSH_ERR ' + str(e_)[:160])
        pn_ += 1; st['pev'] = pn_
    x = ('D' in held) - ('A' in held); y = ('W' in held) - ('S' in held)
    ang = 'rel' if (x == 0 and y == 0) else '%g' % round(math.degrees(math.atan2(x, y)))
    if n >= len(ev) and t > float(ev[-1][0]) + stop:
        for k_ in list(held): cmd('Input.-key %s' % k_)
        held.clear(); return 'mv_stop', True
    return 'mv_kb%s_%s_%d_%s' % ('s' if 'LeftShift' in held else '', ang, n, ''.join(k_ for k_ in 'WASD' if k_ in held) or '0'), False
def move_step(gw, gt):
    if not MOVE: return None, False
    if MOVE.get('keys'): return key_step(gw, gt)
    t0 = float(MOVE.get('start', 2.0)); gait = MOVE.get('gait', 'walk'); segs = MOVE.get('segments', [[3, 0]]); stop = float(MOVE.get('stop', 1.5))
    cmd = lambda c: u.SystemLibrary.execute_console_command(gw, c)
    if gait != 'walk' and gt >= t0 - 1.0 and not st.get('gdown'): st['gdown'] = True; cmd('Input.+action ' + IA_GAIT + ' true')
    # jog = tap (toggle); sprint = hold for the whole run (the protocol holds it too), released with the stop
    # V2.2: the jog tap must span >= 3 distinct game frames (a hitch put press + release into one input frame: the toggle was lost
    # and 'jog' runs walked, 5 of 10 on 2026-10-14)
    if st.get('gdown') and not st.get('gup') and gait == 'jog':
        if st.get('gfr_t') != gt: st['gfr_t'] = gt; st['gfr'] = st.get('gfr', 0) + 1
        if gt >= t0 - 0.9 and st['gfr'] >= 3: st['gup'] = True; cmd('Input.-action ' + IA_GAIT)
    if gt < t0: return 'mv_pre', False
    t = gt - t0
    # V1.3.8 mid-run gait changes through the real gait button: gait_events [[t, '+'|'-'], ...] relative to the move start
    for i_, ev_ in enumerate(MOVE.get('gait_events', [])):
        if t >= float(ev_[0]) and not st.get('gev%d' % i_):
            st['gev%d' % i_] = True; cmd(('Input.+action %s true' % IA_GAIT) if ev_[1] == '+' else ('Input.-action ' + IA_GAIT)); u.log('SHM_GAIT_EVENT %s %.2f' % (ev_[1], t))
    for k, seg in enumerate(segs):
        dur = float(seg[0]); ang = None if seg[1] is None else float(seg[1])
        if t < dur:
            key = 'mv_%s_%s_%d' % (gait, 'rel' if ang is None else '%g' % ang, k)
            if st.get('mseg') != key:
                st['mseg'] = key
                if ang is None: cmd('Input.-action ' + IA_MOVE)   # a null angle = release the stick (stop segment)
                else: mg_ = float(seg[2]) if len(seg) > 2 else 1.0; cmd('Input.+action %s X=%.6f Y=%.6f' % (IA_MOVE, mg_ * math.sin(math.radians(ang)), mg_ * math.cos(math.radians(ang))))   # V2.29: optional stick magnitude seg[2]
            return key, False
        t -= dur
    if st.get('mseg') != 'mv_stop':
        st['mseg'] = 'mv_stop'; cmd('Input.-action ' + IA_MOVE)
        if st.get('gdown') and not st.get('gup'): st['gup'] = True; cmd('Input.-action ' + IA_GAIT)
    return 'mv_stop', t >= stop
def yaw_target(t):
    if not YAW: return None
    t0 = YAW.get('start', 3.0); hold = YAW.get('hold', 2.0); steps = YAW.get('steps', []); sweep = YAW.get('sweep')
    if t < t0: return 0.0, 'yaw_pre'
    osc = YAW.get('osc')
    if osc:
        # V1.3.7 real-map mouse: left/right sweeps (sine per cycle, amplitude cycling through 'amps'), optional slow drift
        ts = t - t0
        if ts >= float(osc.get('seconds', 120.0)): return None, 'yaw_done'
        per = float(osc.get('period', 1.2)); amps = osc.get('amps', [15, 25, 40]); k = int(ts // per)
        a = float(amps[k % len(amps)]); ph = (ts % per) / per
        dr = osc.get('drift', 0.0); base = 0.0
        if isinstance(dr, list):   # piecewise drift [[seconds, deg_per_s], ...] repeated: a wandering player path
            tot = sum(float(x[0]) for x in dr) or 1.0; full = int(ts // tot); rem = ts - full * tot
            base = full * sum(float(x[0]) * float(x[1]) for x in dr)
            for x in dr:
                d_ = min(rem, float(x[0])); base += d_ * float(x[1]); rem -= d_
                if rem <= 0: break
        else: base = float(dr) * ts
        return a * math.sin(2.0 * math.pi * ph) + base, 'yaw_osc'
    k = int((t - t0) // hold)
    if k < len(steps):
        rp = YAW.get('ramp')
        if rp:   # V1.3.8: sweep from the previous step to this one at rp deg/s (a slow mouse turn), then hold
            prev_ = float(steps[k - 1]) if k > 0 else 0.0; dlt = float(steps[k]) - prev_; el = (t - t0) - k * hold
            return prev_ + math.copysign(min(abs(dlt), float(rp) * el), dlt), 'yaw_%s_%d' % (steps[k], k)
        return float(steps[k]), 'yaw_%s_%d' % (steps[k], k)
    if sweep:
        ts = t - t0 - hold * len(steps)
        if ts < sweep[1]: return (sweep[0] * ts) % 360.0, 'yaw_sweep'
    return None, 'yaw_done'
def done(status):
    if st['dead']: return
    st['dead'] = True
    u.unregister_slate_post_tick_callback(st['h'])
    if st.get('take') and st['take'].get('on'):
        try:
            panel = u.TakeRecorderBlueprintLibrary.get_take_recorder_panel(); panel.stop_recording()
            last = panel.get_last_recorded_level_sequence(); st['take']['rec'] = last.get_path_name() if last else None; u.log('SHM_TAKE stopped ' + str(st['take']['rec']))
        except Exception as e: u.log_error('SHM_TAKE stop failed: ' + str(e))
    if LOOK_IA and ed.get_game_world():
        u.SystemLibrary.execute_console_command(ed.get_game_world(), 'Input.-action ' + IA_LOOK); u.log('SHM_LOOK ticks %s scripted %.1f deg observed %.1f deg' % (st.get('lk_n'), st.get('lk_sum', 0.0), st.get('lk_obs', 0.0)))
    for k_ in list(st.get('held', [])):   # V2.12: never leave a forced key down
        if ed.get_game_world(): u.SystemLibrary.execute_console_command(ed.get_game_world(), 'Input.-key %s' % k_)
    mcap_stop(ed.get_game_world())
    for c_ in req.get('console_after', []): u.SystemLibrary.execute_console_command(ed.get_game_world() or ed.get_editor_world(), c_)
    if ed.get_game_world(): les.editor_request_end_play()
    if st.get('pw_prev'):   # V2.25: restore the editor main window
        try:
            h_, x_, y_, w_, hh_, z_ = st['pw_prev']; ctypes.windll.user32.SetWindowPos(h_, None, x_, y_, w_, hh_, 0x0004 | 0x0010)
            if z_: ctypes.windll.user32.ShowWindow(h_, 3)
        except Exception as e: u.log_error('SHM_PIEWIN restore failed: ' + str(e))
    u.SystemLibrary.execute_console_command(ed.get_editor_world(), 't.MaxFPS 0')
    if req.get('slomo'):
        try: u.GameplayStatics.set_global_time_dilation(ed.get_game_world(), 1.0)
        except Exception: pass
    try:
        STATE1 = state_record(); _diff = {k_: (STATE0[k_], STATE1[k_]) for k_ in ('shme', 'abp', 'behavior', 'pbi', 'pawn', 'db') if STATE0[k_] != STATE1[k_]}
        _diffkeys = {k_: sorted(set(a_) ^ set(b_) | {x_ for x_ in a_ if x_ in b_ and a_[x_] != b_[x_]}) for k_, (a_, b_) in _diff.items()}
        if _diffkeys or STATE0.get('dirty_base'):
            u.log_error('SHM_STATE mismatch ' + str(_diffkeys) + ' dirty_base ' + str(STATE0.get('dirty_base'))); status = 'INVALID_STATE'
    except Exception as e: STATE1 = {'err': str(e)[:200]}; _diffkeys = {'err': 1}
    (N / (label + '_state.json')).write_text(json.dumps({'mode': MODE, 'start': STATE0, 'end': STATE1, 'diff': _diffkeys}, indent=1, default=str))
    (N / (label + '_pie.json')).write_text(json.dumps({'status': status, 'state_mode': MODE, 'state_diff': _diffkeys, 'seconds': round(time.monotonic() - st['t'], 1), 'log_start': start_size, 'take': (st.get('take') or {}).get('rec'), 'take_seq': (st.get('take') or {}).get('seq'), 'mcap': {k_: v_ for k_, v_ in (st.get('mcap') or {}).items() if k_ not in ('cap', 'out')}, 'bp_errors': st.get('errs', 0), 'bp_error_first': st.get('err_first'), 'shm_side': st.get('shm_path')}))
    u.log('LR_PIE_DONE ' + label + ' ' + status)
def MW(ai_, mon):
    """V2.16: montage position, slot local weight and blend-in time of the active montage (first-frame handoff record)"""
    if not (ai_ and mon): return 'mpos=-1|mslw=0|mbt=0|'
    try:
        sl = 'DefaultSlot'
        try: sl = str(mon.get_editor_property('slot_anim_tracks')[0].get_editor_property('slot_name'))
        except Exception: pass
        w = ai_.blueprint_get_slot_montage_local_weight(sl)
        return 'mpos=%.4f|mslw=%.4f|mbt=%.3f|' % (ai_.montage_get_position(mon), w, ai_.montage_get_blend_time(mon))
    except Exception as e: return 'mpos=err|'
def MONA(mon):
    """V1.3.8: animation asset(s) inside a montage (dynamic slot montages hide the clip behind AnimMontage_N)"""
    if not mon: return 'none'
    try:
        names = []
        for tr in mon.get_editor_property('slot_anim_tracks'):
            for sg in tr.get_editor_property('anim_track').get_editor_property('anim_segments'):
                r = sg.get_editor_property('anim_reference'); names.append(r.get_path_name().split('.')[0] if r else '?')
        return ','.join(names) or '?'
    except Exception as e: return 'ERR' + str(e)[:30]
def MV(pw_):
    """V1.3.7: movement internals per tick - input acceleration yaw / size, max walk speed, ground friction, active montage"""
    try:
        cm_ = pw_.get_editor_property('character_movement'); ac = cm_.get_current_acceleration()
        ai_ = pw_.mesh.get_anim_instance(); mon = ai_.get_current_active_montage() if ai_ else None
        vb = st.get('vbody')
        if vb is None:
            vb = [c for c in pw_.get_components_by_class(u.SkeletalMeshComponent) if c.get_name() == 'Manny']; vb = vb[0] if vb else False; st['vbody'] = vb
        vbs = ''
        if vb:
            for sk, nm in (('pelvis', 'vb_pelvis'), ('spine_03', 'vb_chest'), ('head', 'vb_head'), ('ball_l', 'vb_ball_l'), ('ball_r', 'vb_ball_r'), ('foot_l', 'vb_foot_l'), ('foot_r', 'vb_foot_r'), ('upperarm_l', 'vb_sh_l'), ('upperarm_r', 'vb_sh_r'), ('spine_05', 'vb_chest5')):
                l_ = vb.get_socket_location(sk); vbs += '%s=X=%.3f Y=%.3f Z=%.3f|' % (nm, l_.x, l_.y, l_.z)
        gz = ''
        if req.get('ground_trace', True):
            w_ = pw_.get_world()
            for sk, nm in (('ball_l', 'gzl'), ('ball_r', 'gzr')):
                b_ = pw_.mesh.get_socket_location(sk)
                h_ = u.SystemLibrary.line_trace_single(w_, u.Vector(b_.x, b_.y, b_.z + 60.0), u.Vector(b_.x, b_.y, b_.z - 90.0), u.TraceTypeQuery.TRACE_TYPE_QUERY1, False, [pw_], u.DrawDebugTrace.NONE, True)
                if h_: gz += '%s=%.2f|' % (nm, h_.to_tuple()[4].z)
        pvs = ''
        if req.get('pvars'):   # V1.3.9: player / spring-arm rig variables per tick (camera diagnosis)
            arm_ = st.get('arm')
            if arm_ is None:
                arm_ = pw_.get_components_by_class(u.SpringArmComponent); arm_ = arm_[0] if arm_ else False; st['arm'] = arm_
            if arm_:
                so_ = arm_.get_editor_property('socket_offset'); to_ = arm_.get_editor_property('target_offset')
                pvs += 'arm_len=%.1f|arm_so=X=%.1f Y=%.1f Z=%.1f|arm_to=X=%.1f Y=%.1f Z=%.1f|' % (arm_.get_editor_property('target_arm_length'), so_.x, so_.y, so_.z, to_.x, to_.y, to_.z)
            for n_ in req['pvars']:
                try:
                    x_ = pw_.get_editor_property('character_movement').get_editor_property(n_[3:]) if n_.startswith('cm.') else pw_.get_editor_property(n_)   # V2.17: cm.<prop> = CharacterMovement
                    if hasattr(x_, 'yaw') and not isinstance(x_, float): x_ = 'P%.0f Y%.0f R%.0f' % (x_.pitch, x_.yaw, x_.roll)
                    pvs += 'pv_%s=%s|' % (n_, ('%.2f' % x_) if isinstance(x_, float) else str(x_).replace('|', '/')[:60])
                except Exception: pvs += 'pv_%s=err|' % n_
        if req.get('cvars'):   # V1.3.9: SHME component variables per tick (routing diagnosis)
            cmp_ = st.get('shmc')
            if cmp_ is None:
                cmp_ = [c for c in pw_.get_components_by_class(u.ActorComponent) if 'SHM_HumanMotion' in c.get_class().get_name()]; cmp_ = cmp_[0] if cmp_ else False; st['shmc'] = cmp_
            for n_ in req['cvars']:
                try:
                    x_ = cmp_.get_editor_property(n_) if cmp_ else None
                    if hasattr(x_, 'x') and hasattr(x_, 'z'): x_ = 'X=%.2f Y=%.2f Z=%.2f' % (x_.x, x_.y, x_.z)   # V2.26: vectors readable (the struct repr was truncated)
                    elif hasattr(x_, 'roll'): x_ = 'P=%.2f Y=%.2f R=%.2f' % (x_.pitch, x_.yaw, x_.roll)
                    pvs += 'cv_%s=%s|' % (n_, ('%.3f' % x_) if isinstance(x_, float) else str(x_).replace('|', '/')[:40])
                except Exception: pvs += 'cv_%s=err|' % n_
        if req.get('avars'):   # V2.3: anim-instance (ABP) variables per tick (zero-crossing diagnosis); vectors/rotators as x/y/z
            for n_ in req['avars']:
                try:
                    x_ = ai_.get_editor_property(n_) if ai_ else None
                    if hasattr(x_, 'x') and hasattr(x_, 'z'): x_ = '%.3f/%.3f/%.3f' % (x_.x, x_.y, x_.z)
                    elif hasattr(x_, 'roll'): x_ = '%.3f/%.3f/%.3f' % (x_.roll, x_.pitch, x_.yaw)
                    elif hasattr(x_, 'get_name') and not isinstance(x_, str): x_ = x_.get_name()   # V2.9: object refs (e.g. CurrentSelectedDatabase) by name
                    pvs += 'av_%s=%s|' % (n_, ('%.4f' % x_) if isinstance(x_, float) else str(x_).replace('|', '/')[:40])
                except Exception: pvs += 'av_%s=err|' % n_
        if req.get('acurves'):   # V2.9: driver anim-instance curve values per tick (ac_<name>; last evaluated pose)
            for n_ in req['acurves']:
                try: pvs += 'ac_%s=%.4f|' % (n_, ai_.get_curve_value(n_) if ai_ else 0.0)
                except Exception: pvs += 'ac_%s=err|' % n_
        if req.get('vbones') and vb:   # V2.5: extra VISIBLE-body (Manny) bone world locations per tick (vx_<bone>), e.g. hand_l / lowerarm_l
            for n_ in req['vbones']:
                try:
                    l_ = vb.get_socket_location(n_); pvs += 'vx_%s=X=%.3f Y=%.3f Z=%.3f|' % (n_, l_.x, l_.y, l_.z)
                except Exception: pvs += 'vx_%s=err|' % n_
        for key_, comp_, pre_ in (('vaxes', vb, 'v'), ('maxes', pw_.mesh, 'm')):   # V2.9: bone orientation as two world axes
            if req.get(key_) and comp_:
                for n_ in req[key_]:
                    try:
                        r_ = comp_.get_socket_rotation(n_); fx = u.MathLibrary.get_forward_vector(r_); fz = u.MathLibrary.get_up_vector(r_)
                        pvs += '%sax_%s=X=%.4f Y=%.4f Z=%.4f|%saz_%s=X=%.4f Y=%.4f Z=%.4f|' % (pre_, n_, fx.x, fx.y, fx.z, pre_, n_, fz.x, fz.y, fz.z)
                    except Exception: pvs += '%sax_%s=err|' % (pre_, n_)
        if req.get('mbones'):   # WDLOCK: extra MM-mesh bone world locations per tick (mx_<bone>), e.g. ik_foot_l / thigh_l
            for n_ in req['mbones']:
                try:
                    l_ = pw_.mesh.get_socket_location(n_); pvs += 'mx_%s=X=%.3f Y=%.3f Z=%.3f|' % (n_, l_.x, l_.y, l_.z)
                except Exception: pvs += 'mx_%s=err|' % n_
        if req.get('acurves'):   # WDLOCK: final anim curve values of the MM anim instance per tick (ac_<curve>)
            for n_ in req['acurves']:
                try: pvs += 'ac_%s=%.4f|' % (n_, ai_.get_curve_value(n_) if ai_ else -1.0)
                except Exception: pvs += 'ac_%s=err|' % n_
        # V2.18: engine frame number + world delta (separates a dropped telemetry row from a long frame) and the RAW player input the
        # movement component consumed this frame (last input vector) - the intent before GR / CMC turn it into acceleration
        try:
            li_ = cm_.get_last_input_vector(); fx_ = 'fc=%d|wdt=%.4f|lix=%.3f|liy=%.3f|' % (u.SystemLibrary.get_frame_count(), u.GameplayStatics.get_world_delta_seconds(pw_), li_.x, li_.y)
        except Exception as e2_: fx_ = 'fcerr=%s|' % str(e2_)[:30]
        # V2.23: position-authority trace (capsule / actor world location + velocity, MM mesh and visible-body component world location
        # and relative offset, root motion flag, spring-arm pivot) - separates a capsule jump from a mesh / root / camera jump
        try:
            al_ = pw_.get_actor_location(); v_ = pw_.get_velocity(); mw_ = pw_.mesh.get_world_location(); mr_ = pw_.mesh.get_editor_property('relative_location')
            fx_ += 'ax=X=%.3f Y=%.3f Z=%.3f|avx=%.2f|avy=%.2f|mwl=X=%.3f Y=%.3f Z=%.3f|mrl=X=%.3f Y=%.3f Z=%.3f|mry=%.2f|' % (al_.x, al_.y, al_.z, v_.x, v_.y, mw_.x, mw_.y, mw_.z, mr_.x, mr_.y, mr_.z, pw_.mesh.get_editor_property('relative_rotation').yaw)
            if vb:
                vw_ = vb.get_world_location(); fx_ += 'vwl=X=%.3f Y=%.3f Z=%.3f|vwy=%.2f|' % (vw_.x, vw_.y, vw_.z, vb.get_world_rotation().yaw)
            if vb:   # V2.29: visible-body render state (disappearance diagnosis): visible flag, hidden-in-game, owner-no-see, recently rendered, bounds radius / origin offset from the actor
                try:
                    bo_ = vb.bounds.origin if hasattr(vb, 'bounds') else None
                    fx_ += 'vvis=%d|vhid=%d|vons=%d|vrr=%d|' % (1 if vb.is_visible() else 0, 1 if vb.get_editor_property('hidden_in_game') else 0, 1 if vb.get_editor_property('owner_no_see') else 0, 1 if vb.was_recently_rendered(0.1) else 0)
                    b3_ = vb.get_local_bounds() if hasattr(vb, 'get_local_bounds') else None
                except Exception as e4_: fx_ += 'vviserr=%s|' % str(e4_)[:30]
            try: fx_ += 'rmp=%d|' % (1 if pw_.is_playing_root_motion() else 0)
            except Exception: fx_ += 'rmp=err|'
            arm2_ = st.get('arm')
            if arm2_ is None:
                arm2_ = pw_.get_components_by_class(u.SpringArmComponent); arm2_ = arm2_[0] if arm2_ else False; st['arm'] = arm2_
            if arm2_:
                pl_ = arm2_.get_world_location(); fx_ += 'apv=X=%.3f Y=%.3f Z=%.3f|' % (pl_.x, pl_.y, pl_.z)
        except Exception as e3_: fx_ += 'axerr=%s|' % str(e3_)[:30]
        return fx_ + vbs + gz + pvs + 'acc=%.1f|accyaw=%.1f|mws=%.1f|gfr=%.2f|mont=%s|' % ((ac.x * ac.x + ac.y * ac.y) ** 0.5, math.degrees(math.atan2(ac.y, ac.x)), cm_.get_editor_property('max_walk_speed'), cm_.get_editor_property('ground_friction'), (mon.get_name() if mon else 'none')) + 'mona=%s|' % MONA(mon) + MW(ai_, mon)
    except Exception as e_:
        return 'mverr=%s|' % str(e_)[:40]
def tick(dt):
    if st['dead']: return
    try:
        now = time.monotonic(); gw = ed.get_game_world()
        if st['phase'] == 'wait':
            if gw and u.GameplayStatics.get_player_character(gw, 0):
                build(gw); st['phase'] = 'run'
            elif now - st['t'] > 120: done('NOT_STARTED')
            return
        if not gw: done('INTERRUPTED'); return
        if req.get('console') and not st.get('console_done'):
            st['console_done'] = True
            for c_ in req['console']: u.SystemLibrary.execute_console_command(gw, c_)
        # V2.19: controlled hitches for the frame-rate study - hitches = [[game_time, seconds], ...]: the slate post-tick sleeps once,
        # so the NEXT world frame carries that wall time as its delta (a real stall, not a scripted dt)
        for i_h, h_ in enumerate(req.get('hitches', [])):
            if not st.get('hit%d' % i_h) and u.GameplayStatics.get_time_seconds(gw) >= float(h_[0]):
                st['hit%d' % i_h] = True; u.log('SHM_HITCH %.3f %.3f' % (u.GameplayStatics.get_time_seconds(gw), float(h_[1]))); time.sleep(float(h_[1]))
        if PW and not st.get('pw', {}).get('ok') and st.get('pw', {}).get('n', 0) < 6 and u.GameplayStatics.get_time_seconds(gw) > 0.3 + 0.3 * st.get('pw', {}).get('n', 0):
            fit_window(gw)
        if TRACK: track_step(gw, dt)
        if MCAP:
            gt_ = u.GameplayStatics.get_time_seconds(gw)
            if 'mcap' not in st and gt_ >= float(MCAP.get('start', 1.0)): mcap_start(gw)
            elif st.get('mcap', {}).get('cap') and not st['mcap'].get('stopped'):
                st['mcap']['ticks'] += 1
                if gt_ >= float(MCAP.get('start', 1.0)) + float(MCAP.get('seconds', 10.0)): mcap_stop(gw)
        if st.get('take'):
            tk = st['take']; pc_ = u.GameplayStatics.get_player_controller(gw, 0); cm_ = pc_.player_camera_manager
            tk['cam'].set_actor_location_and_rotation(cm_.get_camera_location(), cm_.get_camera_rotation(), False, True)
            cc_ = tk['cam'].get_cine_camera_component(); fov_ = cm_.get_fov_angle(); sw_ = cc_.get_editor_property('filmback').sensor_width
            cc_.set_editor_property('current_focal_length', sw_ / (2.0 * math.tan(math.radians(fov_) / 2.0)))
            if not tk['on'] and u.GameplayStatics.get_time_seconds(gw) >= tk['start']:
                tk['on'] = True
                try:
                    panel = u.TakeRecorderBlueprintLibrary.get_take_recorder_panel() or u.TakeRecorderBlueprintLibrary.open_take_recorder_panel()
                    at_ = u.AssetToolsHelpers.get_asset_tools(); seq = at_.create_asset('LS_' + label, '/Game/GraceRanger/SHME/QA/Takes', u.LevelSequence, u.LevelSequenceFactoryNew())
                    panel.setup_for_recording_level_sequence(seq); panel.set_frame_rate(u.FrameRate(tk['fps'], 1))
                    srcs = panel.get_sources(); pw_ = u.GameplayStatics.get_player_character(gw, 0)
                    for act_ in (pw_, tk['cam']):
                        src_ = srcs.add_source(u.TakeRecorderActorSource)
                        try: src_.set_editor_property('target', act_)
                        except Exception: src_.target = act_
                    panel.start_recording(); tk['seq'] = seq.get_path_name(); u.log('SHM_TAKE started ' + tk['seq'])
                except Exception as e: u.log_error('SHM_TAKE start failed: ' + str(e))
        if YAW or MOVE:
            pc = u.GameplayStatics.get_player_controller(gw, 0); gt = u.GameplayStatics.get_time_seconds(gw)
            if st['yaw0'] is None: st['yaw0'] = float(req['yaw0']) if 'yaw0' in req else pc.get_control_rotation().yaw; st['yaw_stage'] = ''
            tgt, stage = yaw_target(gt) if YAW else (0.0, 'yaw_hold')
            mstage, mdone = move_step(gw, gt)
            if mstage and mstage != 'mv_pre': stage = mstage if not YAW else stage + '+' + mstage
            if stage != st['yaw_stage']: st['yaw_stage'] = stage
            if (YAW and tgt is None and (not MOVE or mdone)) or (not YAW and mdone): done('FINISHED'); return
            if tgt is None: tgt = st.get('yaw_last', 0.0)
            st['yaw_last'] = tgt
            # look input like a mouse: the camera rig owns the control rotation, so a direct SetControlRotation is overridden
            cur = pc.get_control_rotation().yaw; want = st['yaw0'] + tgt; d = ((want - cur + 180.0) % 360.0) - 180.0
            if LOOK_IA:
                # V1.3.8 real player path: the look action through Enhanced Input (controller BP_GR_InputBase: TW_BeforeNativeLook ->
                # pawn TW_CameraLookPulse / camera intent rebase -> sensitivity -> AddYawInput). OPEN LOOP like a hand on a mouse:
                # per-frame delta of the scripted yaw path / fixed gain (deg per action unit), no feedback from the control yaw.
                k_ = float(req.get('look_gain', 0.5)); lt_ = st.get('lk_last')
                val = 0.0 if lt_ is None else ((tgt - lt_ + 180.0) % 360.0 - 180.0) / k_
                st['lk_last'] = tgt; st['lk_n'] = st.get('lk_n', 0) + 1; st['lk_sum'] = st.get('lk_sum', 0.0) + val * k_
                prv = st.get('lk_cy'); st['lk_obs'] = st.get('lk_obs', 0.0) + (0.0 if prv is None else ((cur - prv + 180.0) % 360.0 - 180.0)); st['lk_cy'] = cur
                u.SystemLibrary.execute_console_command(gw, 'Input.+action %s X=%.6f Y=0.000000' % (IA_LOOK, val))
            else: pc.add_yaw_input(d)
            # protocol-compatible telemetry from the harness (no LTP actor): yaws + mesh sockets, one line per tick
            pw = u.GameplayStatics.get_player_character(gw, 0)
            if pw:
                m = pw.mesh; v = pw.get_velocity()
                def CAM(pc_):
                    cm = pc_.player_camera_manager; l = cm.get_camera_location(); r = cm.get_camera_rotation()
                    return ('X=%.3f Y=%.3f Z=%.3f' % (l.x, l.y, l.z), 'P=%.3f Y=%.3f R=%.3f' % (r.pitch, r.yaw, r.roll), cm.get_fov_angle())
                def V(n):
                    l = m.get_socket_location(n); return 'X=%.3f Y=%.3f Z=%.3f' % (l.x, l.y, l.z)
                _ltp('LTP|%s|stage=%s|t=%.3f|dt=%.4f|Speed2D=%.1f|cy=%.1f|ay=%.1f|my=%.1f|py=%.1f|mh_ball_l=%s|mh_ball_r=%s|mh_pelvis=%s|mh_root=%s|mh_head=%s|camera=%s|camrot=%s|fov=%.1f|mh_chest=%s|mh_shoulder=%s|%s' % (label, stage, gt, dt, (v.x * v.x + v.y * v.y) ** 0.5, cur, pw.get_actor_rotation().yaw, m.get_world_rotation().yaw, m.get_socket_rotation('pelvis').yaw, V('ball_l'), V('ball_r'), V('pelvis'), V('root'), V('head'), CAM(pc)[0], CAM(pc)[1], CAM(pc)[2], V('spine_03'), V('clavicle_r'), MV(pw)))
                # V2.33: SHM| telemetry goes to Saved/Codex/SHME_V1_20260925/SHM/<label>.shm (component TelemetryLine) instead of the editor log
                c_ = st.get('shmc2')
                if c_ is None:
                    c_ = [c for c in pw.get_components_by_class(u.ActorComponent) if 'SHM_HumanMotion' in c.get_class().get_name()]; c_ = c_[0] if c_ else False; st['shmc2'] = c_
                if c_:
                    try: tl_ = c_.get_editor_property('TelemetryLine')
                    except Exception: tl_ = None
                    if tl_ and tl_ != st.get('shm_last'):
                        st['shm_last'] = tl_
                        if not st.get('shm_path'):
                            d_ = os.path.join(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/SHME_V1_20260925', 'SHM'); os.makedirs(d_, exist_ok=True)
                            st['shm_path'] = os.path.join(d_, label + '.shm'); open(st['shm_path'], 'w', encoding='utf8').close()
                        with open(st['shm_path'], 'a', encoding='utf8') as fh_: fh_.write(tl_ + chr(10))
        if SH and st.get('rec') and now - st['shot'] >= SH:
            st['shot'] = now; st['n'] += 1; u.SystemLibrary.execute_console_command(gw, req.get('shot_cmd', 'Shot'))   # V2.6: 'HighResShot 1' writes a PNG ('Shot' only traces in 5.8)
        if now - st.get('chk', 0) < (0.25 if not st.get('rec') else 1): return
        st['chk'] = now
        with open(LOG, 'rb') as f:
            f.seek(st['pos']); chunk = f.read(); st['pos'] = max(st['pos'], f.tell() - 200)
        if b'PBI_CAPTURE_START|run=' + label.encode() in chunk: st['rec'] = True
        # V2.33 early error stop: a repeated Blueprint runtime error flood (V2.32 LastHitBy: 3 per frame for hours) ends the run at once with
        # the first cause kept (ERROR_FLOOD); single errors only count. ERR_MAX via request 'err_max' (default 200 per run).
        _ek = (b'Accessed None', b'Blueprint Runtime Error', 'Blueprint Çalışma Zamanı Hatası'.encode('utf8'))
        _en = sum(chunk.count(k_) for k_ in _ek)
        if _en:
            st['errs'] = st.get('errs', 0) + _en
            if not st.get('err_first'):
                for ln_ in chunk.split(chr(10).encode()):
                    if any(k_ in ln_ for k_ in _ek): st['err_first'] = ln_.decode('utf8', 'replace')[-400:]; break
            if st['errs'] > int(req.get('err_max', 200)): u.log_error('SHM_ERROR_FLOOD %s errors=%d first=%s' % (label, st['errs'], st.get('err_first'))); done('ERROR_FLOOD'); return
        if ('LTP_FINISHED|' + label).encode() in chunk or ('PBI_FINISHED|run=' + label).encode() in chunk: done('FINISHED'); return
        if now - st['t'] > timeout: done('TIMEOUT')
    except Exception as e:
        u.log_error('LR_PIE_ERR ' + str(e)); done('ERROR')
for h in list(getattr(builtins, 'LR_PIE_ALL', [])):
    try: u.unregister_slate_post_tick_callback(h)
    except Exception: pass
builtins.LR_PIE_ALL = []
st['h'] = u.register_slate_post_tick_callback(tick); builtins.LR_PIE_ALL.append(st['h'])
# V2.25: "pie_window": [w, h] plays in a NEW editor window of that client size (full-frame captures at a MediaIOCore-safe width,
# e.g. 1728x972 = 16:9, instead of centre-cropping the docked viewport). The previous play settings are restored when PIE ends.
PW = req.get('pie_window')   # V2.25: any value = fit the DOCKED PIE viewport to a MediaIOCore-safe width (multiple of 64) by narrowing the
# editor main window by (width % 64) px once PIE runs; the full frame is then captured uncropped at the viewport's own aspect; restored at PIE end.
# (LevelEditorPlaySettings is not exposed to Python and editor_request_begin_play ignores the floating-window play mode.)
import ctypes, ctypes.wintypes as _W
def _main_hwnd():
    pid = ctypes.windll.kernel32.GetCurrentProcessId(); found = []
    def cb(h, _):
        p_ = _W.DWORD(); ctypes.windll.user32.GetWindowThreadProcessId(h, ctypes.byref(p_))
        if p_.value == pid and ctypes.windll.user32.IsWindowVisible(h):
            r_ = _W.RECT(); ctypes.windll.user32.GetWindowRect(h, ctypes.byref(r_)); found.append(((r_.right - r_.left) * (r_.bottom - r_.top), h, r_))
        return True
    ctypes.windll.user32.EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool, _W.HWND, _W.LPARAM)(cb), 0)
    return max(found)[1:] if found else (None, None)
def _ltp(line):
    """V2.30: the per-frame LTP telemetry line (~12 KB) goes to a side file Saved/Codex/SHME_V1_20260925/LTP/<label>.ltp with the
    log-style UTC timestamp prefix, NOT to the editor log: the Output Log widget kept every line (Slate memory grew ~1 GB per short
    PIE run). evidence.py reads the side file first and falls back to the log."""
    import time as _t
    tm = _t.time(); g = _t.gmtime(tm)
    pre = '[%04d.%02d.%02d-%02d.%02d.%02d:%03d]' % (g.tm_year, g.tm_mon, g.tm_mday, g.tm_hour, g.tm_min, g.tm_sec, int((tm % 1) * 1000))
    d = os.path.join(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/SHME_V1_20260925', 'LTP')
    if not st.get('ltp_path'):
        os.makedirs(d, exist_ok=True); st['ltp_path'] = os.path.join(d, label + '.ltp')
        open(st['ltp_path'], 'w', encoding='utf8').close()
    with open(st['ltp_path'], 'a', encoding='utf8') as fh: fh.write(pre + line + chr(10))

def fit_window(gw):
    """One fitting step; called every 0.3 s until the viewport width is a multiple of 64 (window px != viewport px under DPI scaling:
    the window->viewport ratio is measured from the previous step)."""
    vs_ = u.WidgetLayoutLibrary.get_viewport_size(gw); vw_ = int(round(vs_.x)); rem = vw_ % 64; pw_ = st.setdefault('pw', {'n': 0})
    if rem == 0: pw_['ok'] = True; u.log('SHM_PIEWIN viewport %dx%d fits' % (vw_, int(round(vs_.y)))); return
    h_, r_ = _main_hwnd()
    if not h_: u.log_warning('SHM_PIEWIN no main window'); pw_['ok'] = True; return
    if 'pw_prev' not in st: st['pw_prev'] = (h_, r_.left, r_.top, r_.right - r_.left, r_.bottom - r_.top, bool(ctypes.windll.user32.IsZoomed(h_)))
    if ctypes.windll.user32.IsZoomed(h_):   # V2.29: a maximized window ignores SetWindowPos -> restore first, keep the maximized rect
        ctypes.windll.user32.ShowWindow(h_, 9); ctypes.windll.user32.SetWindowPos(h_, None, r_.left, r_.top, r_.right - r_.left, r_.bottom - r_.top, 0x0004 | 0x0010)
        u.log('SHM_PIEWIN restored a maximized main window %dx%d' % (r_.right - r_.left, r_.bottom - r_.top)); pw_['n'] = pw_['n'] + 1; return
    ratio = pw_.get('ratio', 1.0)
    if pw_.get('last_vw') is not None and pw_.get('last_cut') and pw_['last_vw'] != vw_: ratio = pw_['last_cut'] / float(pw_['last_vw'] - vw_); pw_['ratio'] = ratio
    cut = max(1, int(round(rem * ratio)))
    ctypes.windll.user32.SetWindowPos(h_, None, r_.left, r_.top, (r_.right - r_.left) - cut, r_.bottom - r_.top, 0x0004 | 0x0010)
    pw_.update({'n': pw_['n'] + 1, 'last_vw': vw_, 'last_cut': cut})
    u.log('SHM_PIEWIN viewport %dx%d rem %d -> window -%d px (ratio %.3f, step %d)' % (vw_, int(round(vs_.y)), rem, cut, ratio, pw_['n']))
les.editor_request_begin_play(); print('PIE requested', label)
