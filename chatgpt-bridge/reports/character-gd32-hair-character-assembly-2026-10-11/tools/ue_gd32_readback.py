"""GD32 read-back (no writes except data/assembly_check.json): Blueprint component templates (subobject data) and the placed instance in the
current editor world - mesh, LOD, override materials, anim mode / class, groom + binding - with None-safe access; level actors and cameras."""
import unreal as u, json, pathlib
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/GD32_Identity_20261011/data'
G = '/Game/Sphirus/CharacterLab/GD32_IdentityMaster_20261011'; BP_PATH = G+'/Assembly/BP_GD32_Character_G31'; MAP_PATH = G+'/Maps/L_GD32_Eval_G31'
def pn(o): return o.get_path_name() if o is not None else None
def gp(o, k):
    try: return o.get_editor_property(k)
    except Exception as e: return 'ERR '+repr(e)[:80]
def desc(o):
    if isinstance(o, u.SkeletalMeshComponent):
        ov = gp(o, 'override_materials'); return {'class': 'SkeletalMesh', 'mesh': pn(gp(o, 'skeletal_mesh_asset')), 'forced_lod_model': gp(o, 'forced_lod_model'),
            'override_materials': {i: m.get_name() for i, m in enumerate(ov) if m} if isinstance(ov, (list, u.Array)) else str(ov), 'anim_mode': str(gp(o, 'animation_mode')), 'anim_class': str(gp(o, 'anim_class')),
            'attach_parent': pn(o.get_attach_parent()) if hasattr(o, 'get_attach_parent') else None}
    if isinstance(o, u.GroomComponent):
        return {'class': 'Groom', 'groom': pn(gp(o, 'groom_asset')), 'binding': pn(gp(o, 'binding_asset')), 'attach_parent': pn(o.get_attach_parent())}
    return {'class': o.get_class().get_name()}
sds = u.get_engine_subsystem(u.SubobjectDataSubsystem); BFL = u.SubobjectDataBlueprintFunctionLibrary; bp = u.load_asset(BP_PATH)
chk = {'blueprint': BP_PATH, 'map': MAP_PATH, 'bp_templates': {}, 'instance': {}}
for hdl in sds.k2_gather_subobject_data_for_blueprint(bp):
    o = BFL.get_object(BFL.get_data(hdl))
    if o is not None and isinstance(o, u.ActorComponent): chk['bp_templates'][o.get_name()] = desc(o)
eas = u.get_editor_subsystem(u.EditorActorSubsystem); world = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world(); chk['editor_world'] = pn(world)
acts = eas.get_all_level_actors(); chk['level_actors'] = sorted(a.get_actor_label() for a in acts); cams = {}
for a in acts:
    if a.get_actor_label() == 'GD32_Character_G31':
        for c in a.get_components_by_class(u.ActorComponent): chk['instance'][c.get_name()] = desc(c)
    if a.get_actor_label().startswith('CAM_'):
        l = a.get_actor_location(); r = a.get_actor_rotation(); cams[a.get_actor_label()] = [round(l.x, 3), round(l.y, 3), round(l.z, 3), round(r.yaw, 3), round(r.pitch, 3), a.get_component_by_class(u.CameraComponent).field_of_view]
chk['cameras'] = dict(sorted(cams.items()))
(O/'assembly_check.json').write_text(json.dumps(chk, indent=1, default=str)); print('GD32_READBACK_OK', pn(world), len(chk['bp_templates']), len(chk['instance']), len(cams))
