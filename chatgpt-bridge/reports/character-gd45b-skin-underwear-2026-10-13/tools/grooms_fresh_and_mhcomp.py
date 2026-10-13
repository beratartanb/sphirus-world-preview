"""GD45: (a) audit MetaHumanComponentUE / LODSyncComponent properties on the pawn (does the MetaHuman component manage grooms / clothing / leader pose?),
placed BP_PBI_Player actors in the editor map and their auto-possess; (b) mutation (checkpoint exists): the three MetaHuman-named groom components
(Hair / Eyebrows / Eyelashes, attachment FACIAL_C_FacialRoot) lose their binding at PIE while the freshly added HairLoose keeps it -> add fresh
components HairMain2 / Eyebrows2 / Eyelashes2 under Face with the GD38 grooms + bindings (no attachment name) and clear the old three (groom None,
hidden). Owner BP_Player_MM; children recompiled + saved."""
import unreal as u, json
OUT = 'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/GD45_Promote_20261013/data/grooms2.json'
out = {}; sds = u.get_engine_subsystem(u.SubobjectDataSubsystem); BFL = u.SubobjectDataBlueprintFunctionLibrary; EAL = u.EditorAssetLibrary
def props(o, keys=None):
    d = {}
    for p_ in dir(o):
        if p_.startswith('_') or p_ in ('name',): continue
        try: v = o.get_editor_property(p_)
        except Exception: continue
        if callable(v): continue
        s = v.get_path_name() if hasattr(v, 'get_path_name') else str(v)
        if keys is None or any(k.lower() in p_.lower() for k in keys): d[p_] = s[:120]
    return d
gen = u.load_asset('/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player').generated_class(); a = u.EditorLevelLibrary.spawn_actor_from_class(gen, u.Vector(0, 0, -100000))
for c in a.get_components_by_class(u.ActorComponent):
    cn = c.get_class().get_name()
    if cn == 'MetaHumanComponentUE': out['metahuman_component'] = props(c)
    if cn == 'LODSyncComponent': out['lodsync'] = props(c, ['component', 'lod', 'sync', 'forced', 'num'])
a.destroy_actor()
world = u.EditorLevelLibrary.get_editor_world(); placed = []
for act in u.EditorLevelLibrary.get_all_level_actors():
    if act.get_class() == gen or 'BP_PBI_Player' in act.get_class().get_name():
        try: ap = str(act.get_editor_property('auto_possess_player'))
        except Exception: ap = '?'
        placed.append({'label': act.get_actor_label(), 'name': act.get_name(), 'auto_possess': ap, 'loc': [round(v, 1) for v in (act.get_actor_location().x, act.get_actor_location().y, act.get_actor_location().z)]})
out['placed_pawns'] = placed
# (b) fresh groom components
BP = '/Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/BP_Player_MM'; bp = u.load_asset(BP)
GR = {'HairMain2': ('/Game/Sphirus/CharacterLab/GD11_HairQ_20261006/Hair/GR_LK_Hair_Main_h75c', '/Game/Sphirus/CharacterLab/GD38_IdentityMaster_20261011/Face/Bindings/GB_GD38_HairMain_t38h75c'),
      'Eyebrows2': ('/Game/Sphirus/CharacterLab/GD38_IdentityMaster_20261011/Grooms/GR_GD38_BrowCustom_ds8s', '/Game/Sphirus/CharacterLab/GD38_IdentityMaster_20261011/Face/Bindings/GB_GD38_EyebrowsCustom_ds8s_t38'),
      'Eyelashes2': ('/Game/Sphirus/CharacterLab/GD31_IdentityMaster_20261011/Grooms/GR_GD31_Eyelashes_S_Thin', '/Game/Sphirus/CharacterLab/GD38_IdentityMaster_20261011/Face/Bindings/GB_GD38_EyelashesS_Thin31_t38')}
handles = {}; objs = {}
for h in sds.k2_gather_subobject_data_for_blueprint(bp):
    o = BFL.get_object(BFL.get_data(h))
    if o is None: continue
    nm = o.get_name().replace('_GEN_VARIABLE', ''); handles[nm] = h; objs[nm] = o
for nm, (g, b) in GR.items():
    if nm not in objs:
        h, fail = sds.add_new_subobject(u.AddNewSubobjectParams(parent_handle=handles['Face'], new_class=u.GroomComponent, blueprint_context=bp)); assert not str(fail), str(fail)
        sds.rename_subobject(h, u.Text(nm)); objs[nm] = BFL.get_object(BFL.get_data(h)); handles[nm] = h
    c = objs[nm]; c.modify(); c.set_editor_property('groom_asset', u.load_asset(g)); c.set_binding_asset(u.load_asset(b)); c.set_editor_property('binding_asset', u.load_asset(b))
for nm in ('Hair', 'Eyebrows', 'Eyelashes'):
    c = objs[nm]; c.modify(); c.set_editor_property('groom_asset', None); c.set_editor_property('binding_asset', None); c.set_editor_property('visible', False)
u.BlueprintEditorLibrary.compile_blueprint(bp); out['owner_saved'] = EAL.save_loaded_asset(bp, False)
for bpp in ('/Game/GraceRanger/BP_GR_Player', '/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player'):
    b2 = u.load_asset(bpp); u.BlueprintEditorLibrary.compile_blueprint(b2); out[bpp.rsplit('/', 1)[-1] + '_saved'] = EAL.save_loaded_asset(b2, False)
out['dirty_after'] = [str(p.get_path_name()) for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()][:20]
json.dump(out, open(OUT, 'w'), indent=1); print('GD45_GROOMS2', json.dumps({k: v for k, v in out.items() if k not in ('metahuman_component', 'lodsync')}), flush=True)
