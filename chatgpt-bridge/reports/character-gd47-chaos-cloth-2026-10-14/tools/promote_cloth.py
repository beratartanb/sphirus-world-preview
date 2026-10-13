"""GD47 promotion (checkpoint of the 3 pawn Blueprints taken before, checkpoint/hashes.txt): in BP_Player_MM add ChaosClothComponents
HenleyCloth (CA_GD47_Henley_w2) + ShortsCloth (CA_CR_Shorts_m1) as children of Manny; hide the skinned Henley / Shorts templates (kept for
revert); compile + save owner and the two child Blueprints. Leader pose is set afterwards in the construction script (tools/mcp_leaderpose_gd47.py).
builtins.GD47X = {'HenleyCloth': CA path, 'ShortsCloth': CA path}. Idempotent: existing components of the same name are reused. Writes data/promote.json"""
import unreal as u, json, builtins, pathlib
C = builtins.GD47X; R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/GD47_ChaosCloth_20261014/data'
sds = u.get_engine_subsystem(u.SubobjectDataSubsystem); BFL = u.SubobjectDataBlueprintFunctionLibrary; EAL = u.EditorAssetLibrary
BP = '/Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/BP_Player_MM'; bp = u.load_asset(BP); rep = {'cfg': C}
def gather():
    m = {}
    for h in sds.k2_gather_subobject_data_for_blueprint(bp):
        o = BFL.get_object(BFL.get_data(h))
        if o is not None: m[o.get_name().replace('_GEN_VARIABLE', '')] = (h, o)
    return m
objs = gather(); mh, manny = objs['Manny']
for nm, ca in C.items():
    if nm in objs: c = objs[nm][1]; rep.setdefault('reused', []).append(nm)
    else:
        nh, fail = sds.add_new_subobject(u.AddNewSubobjectParams(parent_handle=mh, new_class=u.ChaosClothComponent, blueprint_context=bp))
        assert str(fail) == '' or not str(fail).strip(), fail
        sds.rename_subobject(nh, nm); c = BFL.get_object(BFL.get_data(nh)); assert isinstance(c, u.ChaosClothComponent), c
    c.modify(); c.set_cloth_asset(u.load_asset(ca))
    for k, v in (('use_attach_parent_bound', True), ('visibility_based_anim_tick_option', u.VisibilityBasedAnimTickOption.ALWAYS_TICK_POSE_AND_REFRESH_BONES)):
        try: c.set_editor_property(k, v)
        except Exception as e: rep.setdefault('prop_err', []).append(f'{k}: {str(e)[:80]}')
for nm in ('Henley', 'Shorts'):
    c = objs[nm][1]; c.modify(); c.set_editor_property('visible', False)
u.BlueprintEditorLibrary.compile_blueprint(bp)
objs = gather(); rep['after'] = {}
for nm in ('HenleyCloth', 'ShortsCloth', 'Henley', 'Shorts'):
    h, o = objs[nm]; e = {'class': o.get_class().get_name(), 'visible': o.get_editor_property('visible')}
    p = sds.find_parent_handle(h) if hasattr(sds, 'find_parent_handle') else None
    try: e['scs_parent'] = BFL.get_object(BFL.get_data(BFL.get_data(h).get_parent_handle() if hasattr(BFL.get_data(h), 'get_parent_handle') else p)).get_name()
    except Exception: pass
    if isinstance(o, u.ChaosClothComponent): e['asset'] = o.get_cloth_asset().get_path_name() if o.get_cloth_asset() else None
    rep['after'][nm] = e
rep['owner_saved'] = EAL.save_loaded_asset(bp, False)
for p in ('/Game/GraceRanger/BP_GR_Player', '/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player'):
    b2 = u.load_asset(p); u.BlueprintEditorLibrary.compile_blueprint(b2); rep[p.rsplit('/', 1)[-1] + '_saved'] = EAL.save_loaded_asset(b2, False)
rep['dirty_after'] = [str(x.get_path_name()) for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()][:10]
(O/'promote.json').write_text(json.dumps(rep, indent=1, default=str)); print('GD47_PROMOTE', json.dumps(rep, default=str)[:1500], flush=True)
