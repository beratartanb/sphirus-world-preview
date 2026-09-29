"""Outfit QA scene: temp blank map, BR body + face rig (validated BodyRealism candidate, its PostProcess ABPs), the two
garment skeletal-mesh components following the body pose (leader pose), lights, scene capture. Nothing saved."""
import unreal, pathlib, json, builtins
R = pathlib.Path(unreal.Paths.project_dir()).resolve(); E = R/'Saved/Codex/OutfitHome_20260929/captures'; E.mkdir(parents=True, exist_ok=True)
OF = '/Game/Sphirus/CharacterLab/Outfit_Home_20260929'
for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages():
    if p.get_path_name().startswith(OF): unreal.EditorAssetLibrary.save_asset(p.get_path_name(), False)   # candidate folder only
assert not [p for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()], 'dirty packages outside the candidate folder'
previous = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world().get_path_name()
world = unreal.EditorLoadingAndSavingUtils.new_blank_map(False); actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
BR = '/Game/Sphirus/CharacterLab/BodyRealism_20260929'; OF = '/Game/Sphirus/CharacterLab/Outfit_Home_20260929'
clay = unreal.load_asset('/Game/Sphirus/CharacterLab/HeadMetaHuman_20260928/Diagnostics/M_QA_Clay'); comps = {}
for part, mesh in [('Body', BR+'/SKM_BR_BodyMesh'), ('Head', BR+'/SKM_BR_FaceMesh')]:
    a = actors.spawn_actor_from_class(unreal.SkeletalMeshActor, unreal.Vector(0, 0, 0)); a.set_actor_label('OutfitQA_'+part); c = a.get_component_by_class(unreal.SkeletalMeshComponent)
    m = unreal.load_asset(mesh); c.set_skeletal_mesh_asset(m); c.set_forced_lod(1); c.set_update_animation_in_editor(True)
    c.set_editor_property('visibility_based_anim_tick_option', unreal.VisibilityBasedAnimTickOption.ALWAYS_TICK_POSE_AND_REFRESH_BONES)
    c.set_override_post_process_anim_bp(m.post_process_anim_blueprint); comps[part] = c
b = comps['Body']; h = comps['Head']
h.attach_to_component(b, 'None', unreal.AttachmentRule.KEEP_WORLD, unreal.AttachmentRule.KEEP_WORLD, unreal.AttachmentRule.KEEP_WORLD, False); h.add_tick_prerequisite_component(b)
h.set_anim_instance_class(unreal.load_class(None, '/Game/Sphirus/CharacterLab/ShoulderFix_20260928/Common/Face/ABP_Face.ABP_Face_C'))
garments = {}
for g, mesh in [('Henley', OF+'/SKM_Home_Henley'), ('Trousers', OF+'/SKM_Home_Trousers')]:
    a = actors.spawn_actor_from_class(unreal.SkeletalMeshActor, unreal.Vector(0, 0, 0)); a.set_actor_label('OutfitQA_'+g); c = a.get_component_by_class(unreal.SkeletalMeshComponent)
    c.set_skeletal_mesh_asset(unreal.load_asset(mesh)); c.set_forced_lod(1); c.set_update_animation_in_editor(True)
    c.attach_to_component(b, 'None', unreal.AttachmentRule.KEEP_WORLD, unreal.AttachmentRule.KEEP_WORLD, unreal.AttachmentRule.KEEP_WORLD, False)
    c.set_leader_pose_component(b, True, False); c.add_tick_prerequisite_component(b); garments[g] = c
for loc, intensity, size in [((-180, 260, 250), 65, 240), ((210, 180, 180), 38, 220), ((50, -220, 230), 65, 200)]:
    a = actors.spawn_actor_from_class(unreal.RectLight, unreal.Vector(*loc)); a.set_actor_rotation(unreal.MathLibrary.find_look_at_rotation(a.get_actor_location(), unreal.Vector(0, 0, 110)), False)
    lc = a.get_component_by_class(unreal.RectLightComponent); lc.set_intensity(intensity); lc.set_editor_property('source_width', size); lc.set_editor_property('source_height', size)
sky = actors.spawn_actor_from_class(unreal.SkyLight, unreal.Vector(0, 0, 300)); slc = sky.get_component_by_class(unreal.SkyLightComponent); slc.set_intensity(0.6); slc.set_editor_property('source_type', unreal.SkyLightSourceType.SLS_SPECIFIED_CUBEMAP)
cap = actors.spawn_actor_from_class(unreal.SceneCapture2D, unreal.Vector(0, 700, 100)); cap.set_actor_rotation(unreal.Rotator(yaw=-90), False); cc = cap.get_component_by_class(unreal.SceneCaptureComponent2D)
for k, v in {'projection_type': unreal.CameraProjectionMode.PERSPECTIVE, 'fov_angle': 5.0, 'capture_every_frame': False, 'capture_on_movement': False, 'always_persist_rendering_state': True, 'capture_source': unreal.SceneCaptureSource.SCS_FINAL_COLOR_LDR}.items(): cc.set_editor_property(k, v)
pp = cc.get_editor_property('post_process_settings'); pp.override_auto_exposure_min_brightness = True; pp.auto_exposure_min_brightness = 1; pp.override_auto_exposure_max_brightness = True; pp.auto_exposure_max_brightness = 1; cc.set_editor_property('post_process_settings', pp)
rt = unreal.RenderingLibrary.create_render_target2d(world, 1400, 1400, unreal.TextureRenderTargetFormat.RTF_RGBA8, unreal.LinearColor(.06, .06, .065, 1)); cc.set_editor_property('texture_target', rt)
builtins.SPH_OF_QA = {'world': world, 'actors': actors, 'components': comps, 'garments': garments, 'clay': clay, 'capture': cap, 'cc': cc, 'rt': rt, 'previous_world': previous}
(E/'qa_setup.json').write_text(json.dumps({'world': world.get_path_name(), 'previous_world': previous, 'body': b.skeletal_mesh_asset.get_path_name(), 'garments': {g: c.skeletal_mesh_asset.get_path_name() for g, c in garments.items()}}, indent=2)); print('OUTFIT_QA_SCENE_READY')
