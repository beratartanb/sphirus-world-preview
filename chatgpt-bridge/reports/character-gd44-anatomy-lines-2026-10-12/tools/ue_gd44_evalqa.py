"""GD38 (copy of the GD33 job): load the SAVED evaluation level L_GD38_Eval_G31 and hand its actors to the standard lookdev capture harness (ue_lk_capture.py) as
builtins.SPH_LK_QA: Body / Face / garments / grooms = the components of the placed BP_GD38_Character_T38 instance, lights = the level's studio
rig, plus one transient SceneCapture2D with the same settings as ue_lk_qa_setup.py. So every capture is a render of the saved Blueprint in the
saved level. Instance-only changes (garment leader pose, the capture actor, harness material / visibility switches) are never saved."""
import unreal as u, builtins, json, pathlib
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/GD44_Lines_20261012/data'
MAP = '/Game/Sphirus/CharacterLab/GD44_Lines_20261012/Maps/L_GD44_Eval_Body'
world = u.EditorLoadingAndSavingUtils.load_map(MAP); eas = u.get_editor_subsystem(u.EditorActorSubsystem)
acts = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
ch = acts['GD44_Character_Body']; sk = {c.get_name(): c for c in ch.get_components_by_class(u.SkeletalMeshComponent)}
b, h = sk['Body'], sk['Face']; comps = {'Body': b, 'Head': h}; garments = {}   # GD44: no garments
grooms = {c.get_name(): c for c in ch.get_components_by_class(u.GroomComponent)}
for c in sk.values(): c.set_update_animation_in_editor(True)
for g in garments.values(): g.set_leader_pose_component(b, True, False); g.add_tick_prerequisite_component(b)
h.add_tick_prerequisite_component(b)
lights = {n: (acts['LKQA_'+n].get_component_by_class(u.RectLightComponent), acts['LKQA_'+n].get_component_by_class(u.RectLightComponent).intensity) for n in ('key', 'fill', 'rim')}
gz = acts['LKQA_Grazing']; lights['grazing'] = (gz.get_component_by_class(u.SpotLightComponent), 110.0); lights['sun'] = (acts['LKQA_GameplaySun'].get_component_by_class(u.DirectionalLightComponent), 4.5)
slc = acts['LKQA_Sky'].get_component_by_class(u.SkyLightComponent)
def ov(c): return {i: m for i, m in enumerate(c.get_editor_property('override_materials')) if m}
overrides = {'Body': ov(b), 'Head': ov(h)}
cap = eas.spawn_actor_from_class(u.SceneCapture2D, u.Vector(0, 700, 100)); cap.set_actor_label('GD44_TransientCapture'); cap.set_actor_rotation(u.Rotator(yaw=-90), False); cc = cap.get_component_by_class(u.SceneCaptureComponent2D)
for k, v in {'projection_type': u.CameraProjectionMode.PERSPECTIVE, 'fov_angle': 15.5, 'capture_every_frame': False, 'capture_on_movement': False, 'always_persist_rendering_state': True, 'capture_source': u.SceneCaptureSource.SCS_FINAL_COLOR_LDR}.items(): cc.set_editor_property(k, v)
pp = acts['GD44_PostProcess_CaptureExposure'].get_editor_property('settings')   # the level's post-process = the capture exposure (same values as ue_lk_qa_setup)
cc.set_editor_property('post_process_settings', pp); cc.set_editor_property('post_process_blend_weight', 1.0)
rt = u.RenderingLibrary.create_render_target2d(world, 1600, 1600, u.TextureRenderTargetFormat.RTF_RGBA8, u.LinearColor(0.18, 0.18, 0.18, 1)); cc.set_editor_property('texture_target', rt)
builtins.SPH_LK_QA = {'world': world, 'actors': eas, 'components': comps, 'garments': garments, 'grooms': grooms, 'lights': lights, 'grazing_actor': gz, 'sky': slc,
                      'clay': u.load_asset('/Game/Sphirus/CharacterLab/HeadMetaHuman_20260928/Diagnostics/M_QA_Clay'), 'capture': cap, 'cc': cc, 'rt': rt, 'previous_world': MAP,
                      'overrides': overrides, 'backdrop': acts['LKQA_Backdrop'].static_mesh_component, 'floor': acts['LKQA_Floor'].static_mesh_component}
info = {'world': world.get_path_name(), 'grooms': {n: [g.groom_asset.get_name() if g.groom_asset else None, g.binding_asset.get_name() if g.binding_asset else None] for n, g in grooms.items()},
        'overrides': {p: {i: m.get_name() for i, m in d.items()} for p, d in overrides.items()}, 'face_anim': str(h.get_anim_instance().get_class().get_name() if h.get_anim_instance() else None),
        'lights': {n: round(float(v[1]), 3) for n, v in lights.items()}}
(O/'evalqa_setup.json').write_text(json.dumps(info, indent=1)); print('GD44_EVALQA_READY', json.dumps(info)[:400])
