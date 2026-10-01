"""CharacterLookdev QA scene: NEUTRAL CHARACTER-REVIEW STUDIO (character-lookdev-costume-groom-art-direction skill,
references/character-presentation-lighting.md). Temp blank map; body + face (candidate meshes from qa_config.json) with
their post-process ABPs, garments following the body (leader pose), grooms bound to the face, per-component material
overrides; unlit mid-grey backdrop dome + lit matte grey floor; soft key / gentle fill / controlled rim rect lights, a
grazing spot (off by default), a gameplay-like sun + sky rig (off by default); scene capture with MANUAL exposure, no
bloom / vignette / DOF / motion blur / local exposure. Nothing saved except the studio materials in the lookdev folder."""
import unreal, pathlib, json, builtins
R = pathlib.Path(unreal.Paths.project_dir()).resolve(); E = R/'Saved/Codex/CharacterLookdev_20260930/captures'; E.mkdir(parents=True, exist_ok=True)
CFG = json.loads((E.parent/'qa_config.json').read_text())
F = '/Game/Sphirus/CharacterLab/CharacterLookdev_20260930'; EAL = unreal.EditorAssetLibrary; ME = unreal.MaterialEditingLibrary; AT = unreal.AssetToolsHelpers.get_asset_tools()
for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages():
    if any(p.get_path_name().startswith(x) for x in CFG.get('save_prefixes', [])): EAL.save_asset(p.get_path_name(), False)

def studio_material(name, unlit):
    path = F+'/Studio/'+name
    if EAL.does_asset_exist(path): return unreal.load_asset(path)
    m = AT.create_asset(name, F+'/Studio', unreal.Material, unreal.MaterialFactoryNew())
    if unlit:
        m.set_editor_property('shading_model', unreal.MaterialShadingModel.MSM_UNLIT); m.set_editor_property('two_sided', True)
        c = ME.create_material_expression(m, unreal.MaterialExpressionVectorParameter, -300, 0); c.set_editor_property('parameter_name', 'Color'); c.set_editor_property('default_value', unreal.LinearColor(0.18, 0.18, 0.18, 1))
        ME.connect_material_property(c, '', unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    else:
        c = ME.create_material_expression(m, unreal.MaterialExpressionVectorParameter, -300, 0); c.set_editor_property('parameter_name', 'Color'); c.set_editor_property('default_value', unreal.LinearColor(0.18, 0.18, 0.18, 1))
        ME.connect_material_property(c, '', unreal.MaterialProperty.MP_BASE_COLOR)
        r = ME.create_material_expression(m, unreal.MaterialExpressionScalarParameter, -300, 200); r.set_editor_property('parameter_name', 'Roughness'); r.set_editor_property('default_value', 0.92)
        ME.connect_material_property(r, '', unreal.MaterialProperty.MP_ROUGHNESS)
        e = ME.create_material_expression(m, unreal.MaterialExpressionScalarParameter, -500, 100); e.set_editor_property('parameter_name', 'EmissiveLift'); e.set_editor_property('default_value', 0.0)
        mul = ME.create_material_expression(m, unreal.MaterialExpressionMultiply, -150, 100); ME.connect_material_expressions(c, '', mul, 'A'); ME.connect_material_expressions(e, '', mul, 'B')
        ME.connect_material_property(mul, '', unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    ME.recompile_material(m); EAL.save_loaded_asset(m, False); return m

prev = getattr(builtins, 'SPH_LK_QA', None)
previous = prev['previous_world'] if prev else unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world().get_path_name()
world = unreal.EditorLoadingAndSavingUtils.new_blank_map(False); actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
M_BACK = studio_material('M_LK_StudioBackdrop', True); M_FLOOR = studio_material('M_LK_StudioFloor2', False)
clay = unreal.load_asset('/Game/Sphirus/CharacterLab/HeadMetaHuman_20260928/Diagnostics/M_QA_Clay')
ST = CFG.get('studio', {})
# backdrop dome (unlit, grey) + floor (lit, matte grey)
dome = actors.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(0, 0, -300)); dome.set_actor_label('LKQA_Backdrop')
dc = dome.static_mesh_component; dc.set_static_mesh(unreal.load_asset('/Engine/BasicShapes/Sphere')); dome.set_actor_scale3d(unreal.Vector(40, 40, 40))
SF = CFG.get('studio_folder', F+'/Studio')   # corrective pass: studio instances live in the active candidate folder (older candidates stay byte-identical)
def mic(name, parent, color, lift=None):
    path = SF+'/'+name
    m = unreal.load_asset(path) if EAL.does_asset_exist(path) else AT.create_asset(name, SF, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
    ME.set_material_instance_parent(m, parent); ME.set_material_instance_vector_parameter_value(m, 'Color', unreal.LinearColor(color, color, color, 1))
    if lift is not None: ME.set_material_instance_scalar_parameter_value(m, 'EmissiveLift', lift)
    EAL.save_loaded_asset(m, False); return m
dc.set_material(0, mic('MI_LK_Backdrop', M_BACK, ST.get('backdrop', 0.45))); dc.set_editor_property('cast_shadow', False)
floor = actors.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(0, 0, 0)); floor.set_actor_label('LKQA_Floor')
fc = floor.static_mesh_component; fc.set_static_mesh(unreal.load_asset('/Engine/BasicShapes/Plane')); floor.set_actor_scale3d(unreal.Vector(ST.get('floor_scale', 44), ST.get('floor_scale', 44), 1)); fc.set_material(0, mic('MI_LK_Floor2', M_FLOOR, ST.get('floor', 0.14), ST.get('floor_lift', 2.2)))

comps = {}
for part, mesh in [('Body', CFG['body']), ('Head', CFG['face'])]:
    a = actors.spawn_actor_from_class(unreal.SkeletalMeshActor, unreal.Vector(0, 0, 0)); a.set_actor_label('LKQA_'+part); c = a.get_component_by_class(unreal.SkeletalMeshComponent)
    m = unreal.load_asset(mesh); c.set_skeletal_mesh_asset(m); c.set_forced_lod(1); c.set_update_animation_in_editor(True)
    c.set_editor_property('visibility_based_anim_tick_option', unreal.VisibilityBasedAnimTickOption.ALWAYS_TICK_POSE_AND_REFRESH_BONES)
    c.set_override_post_process_anim_bp(m.post_process_anim_blueprint); comps[part] = c
b = comps['Body']; h = comps['Head']
h.attach_to_component(b, 'None', unreal.AttachmentRule.KEEP_WORLD, unreal.AttachmentRule.KEEP_WORLD, unreal.AttachmentRule.KEEP_WORLD, False); h.add_tick_prerequisite_component(b)
h.set_anim_instance_class(unreal.load_class(None, CFG.get('face_abp', '/Game/Sphirus/CharacterLab/ShoulderFix_20260928/Common/Face/ABP_Face.ABP_Face_C')))
garments = {}
for g, mesh in CFG.get('garments', {}).items():
    a = actors.spawn_actor_from_class(unreal.SkeletalMeshActor, unreal.Vector(0, 0, 0)); a.set_actor_label('LKQA_'+g); c = a.get_component_by_class(unreal.SkeletalMeshComponent)
    c.set_skeletal_mesh_asset(unreal.load_asset(mesh)); c.set_forced_lod(1); c.set_update_animation_in_editor(True)
    c.attach_to_component(b, 'None', unreal.AttachmentRule.KEEP_WORLD, unreal.AttachmentRule.KEEP_WORLD, unreal.AttachmentRule.KEEP_WORLD, False)
    c.set_leader_pose_component(b, True, False); c.add_tick_prerequisite_component(b); garments[g] = c
# corrective pass: runtime Chaos Cloth garments {name: ChaosClothAsset path} replace / add to the skinned garments of the same name
for g, ca in CFG.get('cloth_garments', {}).items():
    if g in garments: garments[g].get_owner().destroy_actor(); garments.pop(g)
    a = actors.spawn_actor_from_class(unreal.Actor, unreal.Vector(0, 0, 0)); a.set_actor_label('LKQA_Cloth_'+g)
    sds = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem); root = sds.k2_gather_subobject_data_for_instance(a)[0]
    nh, fail = sds.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=root, new_class=unreal.ChaosClothComponent, blueprint_context=None))
    c = unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(nh)); assert isinstance(c, unreal.ChaosClothComponent), (fail, c)
    c.set_cloth_asset(unreal.load_asset(ca)); c.attach_to_component(b, 'None', unreal.AttachmentRule.KEEP_WORLD, unreal.AttachmentRule.KEEP_WORLD, unreal.AttachmentRule.KEEP_WORLD, False)
    c.set_leader_pose_component(b, True); c.add_tick_prerequisite_component(b); c.set_simulate_in_editor(True); c.set_enable_simulation(True)
    garments[g] = c
# material overrides {part: {slot_index: material_path}} (candidate lookdev materials; the meshes are not modified)
overrides = {}
for part, slots in CFG.get('material_overrides', {}).items():
    c = comps.get(part) or garments.get(part)
    if not c: continue
    overrides[part] = {int(k): unreal.load_asset(v) for k, v in slots.items()}
grooms = {}
for g, spec in CFG.get('grooms', {}).items():
    a = actors.spawn_actor_from_class(unreal.GroomActor, unreal.Vector(0, 0, 0)); a.set_actor_label('LKQA_'+g)
    gc = a.get_component_by_class(unreal.GroomComponent); gc.set_groom_asset(unreal.load_asset(spec['groom']))
    if spec.get('binding'): gc.set_binding_asset(unreal.load_asset(spec['binding']))
    gc.attach_to_component(comps.get(spec.get('attach', 'Head'), h), 'None', unreal.AttachmentRule.SNAP_TO_TARGET, unreal.AttachmentRule.SNAP_TO_TARGET, unreal.AttachmentRule.KEEP_WORLD, False)
    grooms[g] = gc
# studio rig: soft key (front-left, above), gentle fill (right), controlled rim (back-right)
lights = {}
def rect(name, loc, intensity, w, h_, tgt=(0, 0, 105)):
    a = actors.spawn_actor_from_class(unreal.RectLight, unreal.Vector(*loc)); a.set_actor_label('LKQA_'+name)
    a.set_actor_rotation(unreal.MathLibrary.find_look_at_rotation(a.get_actor_location(), unreal.Vector(*tgt)), False)
    lc = a.get_component_by_class(unreal.RectLightComponent); lc.set_intensity(intensity); lc.set_editor_property('source_width', w); lc.set_editor_property('source_height', h_)
    lc.set_editor_property('attenuation_radius', 9000.0); lights[name] = (lc, intensity); return a
rect('key', ST.get('key_loc', (-230, 300, 280)), ST.get('key', 90.0), 260, 260)
rect('fill', ST.get('fill_loc', (300, 220, 150)), ST.get('fill', 28.0), 300, 300)
rect('rim', ST.get('rim_loc', (160, -300, 260)), ST.get('rim', 38.0), 120, 220, (0, 0, 140))
gz = actors.spawn_actor_from_class(unreal.SpotLight, unreal.Vector(-280, 40, 130)); gz.set_actor_label('LKQA_Grazing')
gzc = gz.get_component_by_class(unreal.SpotLightComponent); gzc.set_intensity(0.0); gzc.set_editor_property('outer_cone_angle', 44.0); gzc.set_editor_property('source_radius', 3.0); lights['grazing'] = (gzc, ST.get('grazing', 110.0))
sun = actors.spawn_actor_from_class(unreal.DirectionalLight, unreal.Vector(0, 0, 500)); sun.set_actor_label('LKQA_GameplaySun')
sun.set_actor_rotation(unreal.Rotator(pitch=-38, yaw=-125, roll=0), False); sunc = sun.get_component_by_class(unreal.DirectionalLightComponent); sunc.set_intensity(0.0); lights['sun'] = (sunc, ST.get('sun', 4.5))
sky = actors.spawn_actor_from_class(unreal.SkyLight, unreal.Vector(0, 0, 300)); slc = sky.get_component_by_class(unreal.SkyLightComponent)
slc.set_editor_property('source_type', unreal.SkyLightSourceType.SLS_CAPTURED_SCENE); slc.set_intensity(ST.get('sky', 0.55))
cap = actors.spawn_actor_from_class(unreal.SceneCapture2D, unreal.Vector(0, 700, 100)); cap.set_actor_rotation(unreal.Rotator(yaw=-90), False); cc = cap.get_component_by_class(unreal.SceneCaptureComponent2D)
for k, v in {'projection_type': unreal.CameraProjectionMode.PERSPECTIVE, 'fov_angle': 15.5, 'capture_every_frame': False, 'capture_on_movement': False, 'always_persist_rendering_state': True, 'capture_source': unreal.SceneCaptureSource.SCS_FINAL_COLOR_LDR}.items(): cc.set_editor_property(k, v)
pp = cc.get_editor_property('post_process_settings')
pp.override_auto_exposure_method = True; pp.auto_exposure_method = unreal.AutoExposureMethod.AEM_MANUAL
pp.override_auto_exposure_apply_physical_camera_exposure = True; pp.auto_exposure_apply_physical_camera_exposure = False
pp.override_auto_exposure_bias = True; pp.auto_exposure_bias = ST.get('ev_bias', 0.0)
for k in ('bloom_intensity', 'vignette_intensity', 'motion_blur_amount', 'lens_flare_intensity', 'depth_of_field_fstop'):
    try: setattr(pp, 'override_'+k, True); setattr(pp, k, 0.0 if k != 'depth_of_field_fstop' else 32.0)
    except Exception: pass
try: pp.override_local_exposure_highlight_contrast_scale = True; pp.local_exposure_highlight_contrast_scale = 1.0; pp.override_local_exposure_shadow_contrast_scale = True; pp.local_exposure_shadow_contrast_scale = 1.0
except Exception: pass
try: pp.override_white_temp = True; pp.white_temp = 6500.0
except Exception: pass
cc.set_editor_property('post_process_settings', pp); cc.set_editor_property('post_process_blend_weight', 1.0)
W, H = CFG.get('capture_size', [1600, 1600])
rt = unreal.RenderingLibrary.create_render_target2d(world, W, H, unreal.TextureRenderTargetFormat.RTF_RGBA8, unreal.LinearColor(0.18, 0.18, 0.18, 1)); cc.set_editor_property('texture_target', rt)
builtins.SPH_LK_QA = {'world': world, 'actors': actors, 'components': comps, 'garments': garments, 'grooms': grooms, 'lights': lights, 'grazing_actor': gz, 'sky': slc, 'clay': clay,
                      'capture': cap, 'cc': cc, 'rt': rt, 'previous_world': previous, 'overrides': overrides, 'backdrop': dc, 'floor': fc}
(E/'qa_setup.json').write_text(json.dumps({'world': world.get_path_name(), 'body': b.skeletal_mesh_asset.get_path_name(), 'garments': {g: (c.get_cloth_asset().get_path_name() if isinstance(c, unreal.ChaosClothComponent) else c.skeletal_mesh_asset.get_path_name()) for g, c in garments.items()}, 'grooms': list(grooms), 'overrides': {p: {k: v.get_path_name() for k, v in s.items()} for p, s in overrides.items()}}, indent=2))
print('LK_QA_SCENE_READY', list(garments), list(grooms), list(overrides))
