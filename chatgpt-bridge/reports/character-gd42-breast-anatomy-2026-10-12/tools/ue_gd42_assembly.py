"""GD42 body-review assembly (from ue_gd38_assembly.py): BP_GD42_Character_Body = GD38 face t38 (+ its GD38 bindings / looks, read-only) on the
NEW body SKM_GD42_BodyMesh (GD42_Body tone morph, always on via ABP_GD42_Body_PostProcess). NO garments in this pass (user: body first, clothes in a
later pass). Level L_GD42_Eval_Body = the QA review studio + the solved / head-and-shoulders / full-body cameras. Refuses to overwrite.
Original notes follow.
GD38: evaluation assembly (from ue_gd35_assembly.py) of the GD38 candidate = NEW face SKM_GD38_Face_t38 (G31 with the subject's right half
mirrored from the left half: jaw / cheek / malar / brow ridge / temple; lids and lips kept) + hair h75c + GD35 brow ds7n4 rebuilt on the new skin
+ GD31 S_Thin lashes, all bound to the new face; GD31 n3 skin MIs, h6 eyes, calm-eye rest pose + lashes S_Thin + body + Henley + Shorts, face playing the calm rest pose AS_GD33_Rest_lid60 (RigLogic curve
eyeUpperLidUp 0.6, looping single node; the neutral mesh is not modified). GD32 traps fixed: groom bindings set with set_binding_asset() on the
templates; the level is built with new_blank_map() + save_map() (new_level() left the editor in a temp world).
Original GD32 notes:
NEW assets only in /Game/Sphirus/CharacterLab/GD32_IdentityMaster_20261011 (all referenced assets are read-only):
  Assembly/BP_GD32_Character_G31  actor Blueprint: Body (root mesh) > Face (ABP_Face, GD31 n3 skin MIs, h6 eye MIs) > 4 groom components
                                   with their GD31 bindings; Henley + Shorts under Body; every mesh forced to LOD0 (evaluation quality)
  Studio/MI_GD32_Backdrop, MI_GD32_Floor  copies of the QA studio backdrop / floor instances (same parents and values)
  Maps/L_GD32_Eval_G31             the character + the QA review studio (soft key / fill / rim rect lights, sky, grey backdrop + floor,
                                   grazing spot and sun present but off, unbound post-process volume = capture exposure) + pilotable
                                   cameras at the solved reference views, a head-and-shoulders turnaround and full-body views
Composition = the GD31 final capture composition (captures/qa_setup.json of cg31c4 / cg31c4S). Refuses to overwrite. Writes data/assembly_check.json."""
import unreal as u, json, pathlib, math
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/GD42_Breast_20261012/data'
G = '/Game/Sphirus/CharacterLab/GD42_Breast_20261012'; G38 = '/Game/Sphirus/CharacterLab/GD38_IdentityMaster_20261011'; G33 = '/Game/Sphirus/CharacterLab/GD33_IdentityMaster_20261011'; G31 = '/Game/Sphirus/CharacterLab/GD31_IdentityMaster_20261011'; L15 = '/Game/Sphirus/CharacterLab/GD15_IdentityMaster_20261009/Looks'
LKS = '/Game/Sphirus/CharacterLab/CharacterLookdev_20260930/Studio'
EAL = u.EditorAssetLibrary; AT = u.AssetToolsHelpers.get_asset_tools(); ME = u.MaterialEditingLibrary
BP_PATH = G+'/Assembly/BP_GD42_Character_Body'; MAP_PATH = G+'/Maps/L_GD42_Eval_Body'; REST = G33+'/Face/AS_GD33_Rest_lid60'   # GD33 rest pose, read-only
for p in (BP_PATH, MAP_PATH, G+'/Studio/MI_GD42_Backdrop', G+'/Studio/MI_GD42_Floor'): assert not EAL.does_asset_exist(p), 'exists, no overwrite: '+p
MESH = {'Body': G+'/Body/SKM_GD42_BodyMesh', 'Face': G38+'/Face/SKM_GD38_Face_t38'}
MATS = {'Body': {0: L15+'/MI_GD15_Body_s1'},
        'Face': {0: G31+'/Looks/MI_GD31_Face_LOD0_s1t6n_n3', 9: G31+'/Looks/MI_GD31_Face_LOD1_s1t6n_n3', 10: G31+'/Looks/MI_GD31_Face_LOD2_s1t6n_n3', 12: G31+'/Looks/MI_GD31_Face_LOD3_s1t6n_n3',
                 13: G31+'/Looks/MI_GD31_Face_LOD4_s1t6n_n3', 14: G31+'/Looks/MI_GD31_Face_LOD5to7_s1t6n_n3', 3: L15+'/MI_GD15_EyeL_h6', 4: L15+'/MI_GD15_EyeR_h6'}}
HAIR = '/Game/Sphirus/CharacterLab/GD11_HairQ_20261006/Hair'
GROOMS = {'HairMain': (HAIR+'/GR_LK_Hair_Main_h75c', G38+'/Face/Bindings/GB_GD38_HairMain_t38h75c'), 'HairLoose': (HAIR+'/GR_LK_Hair_Loose_h75c', G38+'/Face/Bindings/GB_GD38_HairLoose_t38h75c'),
          'Eyebrows': (G38+'/Grooms/GR_GD38_BrowCustom_ds8s', G38+'/Face/Bindings/GB_GD38_EyebrowsCustom_ds8s_t38'), 'Eyelashes': (G31+'/Grooms/GR_GD31_Eyelashes_S_Thin', G38+'/Face/Bindings/GB_GD38_EyelashesS_Thin31_t38')}
ABP = '/MetaHumanCharacter/Face/ABP_Face.ABP_Face_C'
for p in list(MESH.values())+[v for d in MATS.values() for v in d.values()]+[x for t in GROOMS.values() for x in t]: assert EAL.does_asset_exist(p), 'missing '+p
chk = {'blueprint': BP_PATH, 'map': MAP_PATH, 'components': {}, 'warnings': []}
# ---- Blueprint
fac = u.BlueprintFactory(); fac.set_editor_property('parent_class', u.Actor)
bp = AT.create_asset('BP_GD42_Character_Body', G+'/Assembly', u.Blueprint, fac)
sds = u.get_engine_subsystem(u.SubobjectDataSubsystem); root = sds.k2_gather_subobject_data_for_blueprint(bp)[0]; BFL = u.SubobjectDataBlueprintFunctionLibrary
def add(cls, name, parent):
    h, fail = sds.add_new_subobject(u.AddNewSubobjectParams(parent_handle=parent, new_class=cls, blueprint_context=bp))
    sds.rename_subobject(h, u.Text(name)); return h, BFL.get_object(BFL.get_data(h))
def setp(c, k, v):
    try: c.set_editor_property(k, v); return True
    except Exception as e: chk['warnings'].append('%s.%s: %r' % (c.get_name(), k, e)); return False
def skel(c, part):
    m = u.load_asset(MESH[part]); setp(c, 'skeletal_mesh_asset', m); setp(c, 'forced_lod_model', 1)
    setp(c, 'visibility_based_anim_tick_option', u.VisibilityBasedAnimTickOption.ALWAYS_TICK_POSE_AND_REFRESH_BONES); setp(c, 'update_animation_in_editor', True)
    if part in MATS:
        n = len(m.get_editor_property('materials')); ov = [None]*n
        for i, p in MATS[part].items(): ov[i] = u.load_asset(p)
        setp(c, 'override_materials', ov)
    return m
hb, body = add(u.SkeletalMeshComponent, 'Body', root); skel(body, 'Body')
hf, face = add(u.SkeletalMeshComponent, 'Face', hb); skel(face, 'Face')
setp(face, 'anim_class', u.load_class(None, ABP)); setp(face, 'animation_mode', u.AnimationMode.ANIMATION_SINGLE_NODE)
ad = u.SingleAnimationPlayData(); ad.set_editor_property('anim_to_play', u.load_asset(REST)); ad.set_editor_property('saved_looping', True); ad.set_editor_property('saved_playing', True); ad.set_editor_property('saved_position', 0.5); ad.set_editor_property('saved_play_rate', 0.0)
setp(face, 'animation_data', ad)
for n in ():   # GD42: no garments (body review)
    h, c = add(u.SkeletalMeshComponent, n, hb); skel(c, n)
for n, (gp, bp_) in GROOMS.items():
    h, c = add(u.GroomComponent, n, hf); setp(c, 'groom_asset', u.load_asset(gp)); c.modify(); c.set_binding_asset(u.load_asset(bp_))
u.BlueprintEditorLibrary.compile_blueprint(bp); assert EAL.save_loaded_asset(bp, False)
# ---- studio materials (copies of the QA studio instances: same parents, same values as qa_config studio)
ST = json.loads((R/'Saved/Codex/GD42_Breast_20261012/qa_config_before_gd42.json').read_text()).get('studio', {})
def mic(name, parent, color, lift=None):
    m = AT.create_asset(name, G+'/Studio', u.MaterialInstanceConstant, u.MaterialInstanceConstantFactoryNew()); ME.set_material_instance_parent(m, u.load_asset(parent))
    ME.set_material_instance_vector_parameter_value(m, 'Color', u.LinearColor(color, color, color, 1))
    if lift is not None: ME.set_material_instance_scalar_parameter_value(m, 'EmissiveLift', lift)
    EAL.save_loaded_asset(m, False); return m
mb = mic('MI_GD42_Backdrop', LKS+'/M_LK_StudioBackdrop', ST.get('backdrop', 0.45)); mf = mic('MI_GD42_Floor', LKS+'/M_LK_StudioFloor2', ST.get('floor', 0.14), ST.get('floor_lift', 2.2))
# ---- evaluation level
les = u.get_editor_subsystem(u.LevelEditorSubsystem); eas = u.get_editor_subsystem(u.EditorActorSubsystem)
world = u.EditorLoadingAndSavingUtils.new_blank_map(False); assert world is not None
def spawn(cls, loc, label):
    a = eas.spawn_actor_from_class(cls, u.Vector(*loc)); a.set_actor_label(label); return a
ch = eas.spawn_actor_from_object(bp, u.Vector(0, 0, 0)); ch.set_actor_label('GD42_Character_Body')
dome = spawn(u.StaticMeshActor, (0, 0, -300), 'LKQA_Backdrop'); dc = dome.static_mesh_component; dc.set_static_mesh(u.load_asset('/Engine/BasicShapes/Sphere')); dome.set_actor_scale3d(u.Vector(40, 40, 40)); dc.set_material(0, mb); dc.set_editor_property('cast_shadow', False)
floor = spawn(u.StaticMeshActor, (0, 0, 0), 'LKQA_Floor'); fc = floor.static_mesh_component; fc.set_static_mesh(u.load_asset('/Engine/BasicShapes/Plane')); floor.set_actor_scale3d(u.Vector(ST.get('floor_scale', 44), ST.get('floor_scale', 44), 1)); fc.set_material(0, mf)
def rect(name, loc, intensity, w, h_, tgt=(0, 0, 105)):
    a = spawn(u.RectLight, loc, 'LKQA_'+name); a.set_actor_rotation(u.MathLibrary.find_look_at_rotation(a.get_actor_location(), u.Vector(*tgt)), False)
    lc = a.get_component_by_class(u.RectLightComponent); lc.set_intensity(intensity); lc.set_editor_property('source_width', w); lc.set_editor_property('source_height', h_); lc.set_editor_property('attenuation_radius', 9000.0)
rect('key', ST.get('key_loc', (-230, 300, 280)), ST.get('key', 90.0), 260, 260); rect('fill', ST.get('fill_loc', (300, 220, 150)), ST.get('fill', 28.0), 300, 300)
rect('rim', ST.get('rim_loc', (160, -300, 260)), ST.get('rim', 38.0), 120, 220, (0, 0, 140))
gz = spawn(u.SpotLight, (-280, 40, 130), 'LKQA_Grazing'); gzc = gz.get_component_by_class(u.SpotLightComponent); gzc.set_intensity(0.0); gzc.set_editor_property('outer_cone_angle', 44.0); gzc.set_editor_property('source_radius', 3.0)
gz.set_actor_rotation(u.MathLibrary.find_look_at_rotation(gz.get_actor_location(), u.Vector(0, 0, 161)), False)
sun = spawn(u.DirectionalLight, (0, 0, 500), 'LKQA_GameplaySun'); sun.set_actor_rotation(u.Rotator(pitch=-38, yaw=-125, roll=0), False); sun.get_component_by_class(u.DirectionalLightComponent).set_intensity(0.0)
sky = spawn(u.SkyLight, (0, 0, 300), 'LKQA_Sky'); slc = sky.get_component_by_class(u.SkyLightComponent); slc.set_editor_property('source_type', u.SkyLightSourceType.SLS_CAPTURED_SCENE); slc.set_intensity(ST.get('sky', 0.55))
ppv = spawn(u.PostProcessVolume, (0, 0, 100), 'GD42_PostProcess_CaptureExposure'); ppv.set_editor_property('unbound', True); pp = ppv.get_editor_property('settings')
pp.override_auto_exposure_method = True; pp.auto_exposure_method = u.AutoExposureMethod.AEM_MANUAL
pp.override_auto_exposure_apply_physical_camera_exposure = True; pp.auto_exposure_apply_physical_camera_exposure = False
pp.override_auto_exposure_bias = True; pp.auto_exposure_bias = ST.get('ev_bias', 0.0)
for k in ('bloom_intensity', 'vignette_intensity', 'motion_blur_amount', 'lens_flare_intensity', 'depth_of_field_fstop'):
    try: setattr(pp, 'override_'+k, True); setattr(pp, k, 0.0 if k != 'depth_of_field_fstop' else 32.0)
    except Exception: pass
try: pp.override_local_exposure_highlight_contrast_scale = True; pp.local_exposure_highlight_contrast_scale = 1.0; pp.override_local_exposure_shadow_contrast_scale = True; pp.local_exposure_shadow_contrast_scale = 1.0
except Exception: pass
try: pp.override_white_temp = True; pp.white_temp = 6500.0
except Exception: pass
ppv.set_editor_property('settings', pp)
# cameras (pilot them in the viewport: right-click > Pilot, or Perspective > Cameras)
U = json.loads((R/'Saved/Codex/GD42_Breast_20261012/data/uecams.json').read_text()); cams = {}
for v, c in U['ref'].items(): cams['CAM_REF_'+v] = (c['cam'], U['fov'])
T = (-0.23, 5.0, 150.0); RAD = 165.0
for nm, ph, pit in (('front', 0, 0), ('q3_faceR', -45, 0), ('q3_faceL', 45, 0), ('prof_faceR', -90, 0), ('prof_faceL', 90, 0), ('back_q3R', -135, 0), ('back', 180, 0), ('back_q3L', 135, 0), ('front_high', 0, -22)):
    a = math.radians(ph); el = math.radians(-pit); x = T[0]+RAD*math.cos(el)*math.sin(a); y = T[1]+RAD*math.cos(el)*math.cos(a); z = T[2]+RAD*math.sin(el)
    cams['CAM_HS_'+nm] = ([x, y, z, math.degrees(math.atan2(T[1]-y, T[0]-x)), pit], 24.0)
cams['CAM_BODY_front'] = ([0, 700, 92, -90, 0], 15.5); cams['CAM_BODY_front3q'] = ([-400, 574.456, 92, -55.15, 0], 15.5); cams['CAM_BODY_back'] = ([0, -700, 92, 90, 0], 15.5)
for lb, (cm, fov) in cams.items():
    a = spawn(u.CameraActor, cm[:3], lb); a.set_actor_rotation(u.Rotator(pitch=cm[4], yaw=cm[3], roll=0), False)
    cc = a.get_component_by_class(u.CameraComponent); cc.set_editor_property('field_of_view', fov); cc.set_editor_property('constrain_aspect_ratio', False)
assert u.EditorLoadingAndSavingUtils.save_map(world, MAP_PATH), 'save_map failed'
# ---- read back from the saved Blueprint
gen = u.load_asset(BP_PATH); cdo_tree = sds.k2_gather_subobject_data_for_blueprint(gen)
for hdl in cdo_tree:
    o = BFL.get_object(BFL.get_data(hdl))
    if isinstance(o, u.SkeletalMeshComponent):
        chk['components'][o.get_name()] = {'mesh': o.get_editor_property('skeletal_mesh_asset').get_path_name(), 'forced_lod_model': o.get_editor_property('forced_lod_model'),
            'override_materials': {i: m.get_name() for i, m in enumerate(o.get_editor_property('override_materials')) if m}, 'anim_class': str(o.get_editor_property('anim_class'))}
    elif isinstance(o, u.GroomComponent):
        chk['components'][o.get_name()] = {'groom': o.get_editor_property('groom_asset').get_path_name(), 'binding': o.binding_asset.get_path_name() if o.binding_asset else None}
chk['level_actors'] = sorted(a.get_actor_label() for a in eas.get_all_level_actors()); chk['cameras'] = {k: [round(x, 3) for x in v[0]]+[v[1]] for k, v in cams.items()}
(O/'assembly_check.json').write_text(json.dumps(chk, indent=1, default=str)); print('GD42_ASSEMBLY_OK', len(chk['components']), len(chk['level_actors']), 'warnings', len(chk['warnings']))
