"""GD39 body derivative (isolated): SKM_GD39_BodyMesh + ABP_GD39_Body_PostProcess in /Game/Sphirus/CharacterLab/GD39_Body_20261012/Body.
  - duplicates of the (read-only) lookdev body mesh / post-process ABP (SKM_LK_BodyMesh / ABP_LK_Body_PostProcess are not modified)
  - ABP_GD39 gets one more always-on Modify Curve GD39_Body = 1 (Blend), inserted right before Root (after the LK nodes): the GD39 body tone
    morph, same pattern as BR_Neutral / LK_Neutral
  - the curve name is registered as a morph curve on the isolated ShoulderFix skeleton copy (ADDITIVE curve metadata only, the same method
    as BR_Neutral / RV_* / LK_Neutral; no bone, retarget or SHCB change). The skeleton .uasset is checkpointed first (GD39 folder).
Refuses to overwrite existing GD39 assets."""
import unreal as u, sys, pathlib, json, shutil
P = pathlib.Path(u.Paths.project_dir()).resolve()
sys.path.insert(0, str(P/'Saved/Codex/GraceRanger_QA_20260914/Scripts'))
from editor_toolset.toolsets.blueprint import BlueprintTools as B
from qa_graph import connect, disconnect, src, pn, info, obj
EAL = u.EditorAssetLibrary; S = P/'Saved/Codex/GD39_Body_20261012'
F = '/Game/Sphirus/CharacterLab/GD39_Body_20261012/Body'; LK = '/Game/Sphirus/CharacterLab/CharacterLookdev_20260930/Body'
SKEL = '/Game/Sphirus/CharacterLab/ShoulderFix_20260928/Common/Female/Medium/NormalWeight/Body/metahuman_base_skel'
CURVE = 'GD39_Body'
out = {'dirty_before': [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]}
assert not out['dirty_before'], out
for b in ('SKM_GD39_BodyMesh', 'ABP_GD39_Body_PostProcess'): assert not EAL.does_asset_exist(F+'/'+b), 'exists, no overwrite: '+b
ck = S/'checkpoint_skeleton'; ck.mkdir(exist_ok=True); f = P/('Content'+SKEL[len('/Game'):]+'.uasset'); shutil.copy2(f, ck/f.name); out['skeleton_checkpoint'] = str(ck/f.name)
for a, b in (('SKM_LK_BodyMesh', 'SKM_GD39_BodyMesh'), ('ABP_LK_Body_PostProcess', 'ABP_GD39_Body_PostProcess')): assert EAL.duplicate_asset(LK+'/'+a, F+'/'+b), b
bm = u.load_asset(F+'/SKM_GD39_BodyMesh'); bp = u.load_asset(F+'/ABP_GD39_Body_PostProcess')
ag = [g for g in B.list_graphs(bp) if g.get_name() == 'AnimGraph'][0]
root = [n for n in B.find_nodes(ag) if pn(n).rsplit('.', 1)[-1].startswith('AnimGraphNode_Root')][0]; rootp = pn(root)
rpins = [q.name for q in info(rootp).input_pins]; rin = 'Result' if 'Result' in rpins else rpins[0]
prev = src((rootp, rin)); assert len(prev) == 1, prev; out['before_root'] = str(prev[0])
mc = pn(B.create_node(ag, 'Animasyon|Eğrileri|EğriyiDeğiştir', u.IntPoint(5600, 1300)))
o = obj(mc); o.set_editor_property('tag', 'GD39_BodyCurve'); nd = o.get_editor_property('node')
nd.set_editor_property('apply_mode', u.ModifyCurveApplyMode.BLEND); nd.set_editor_property('curve_map', {CURVE: 1.0}); nd.set_editor_property('alpha', 1.0); o.set_editor_property('node', nd)
ins = [q.name for q in info(mc).input_pins]; outs = [q.name for q in info(mc).output_pins]; pin_in = [x for x in ins if 'Pose' in x][0]; pin_out = [x for x in outs if 'Pose' in x][0]
disconnect((rootp, rin)); connect(prev[0], (mc, pin_in)); connect((mc, pin_out), (rootp, rin))
u.BlueprintEditorLibrary.compile_blueprint(bp); out['abp_status'] = str(bp.status)
bm.set_editor_property('post_process_anim_blueprint', bp.generated_class())
sk = u.load_asset(SKEL); out['skel_curves_before'] = sk.get_num_curve_meta_data()
sk.add_curve_meta_data(CURVE); sk.set_curve_meta_data_morph_target(CURVE, True); out['skel_curves_after'] = sk.get_num_curve_meta_data()
mc_nodes = [str(n.get_editor_property('tag')) for n in u.AnimationLibrary.get_nodes_of_class(bp, u.AnimGraphNode_ModifyCurve, True)]; out['modify_curve_nodes'] = mc_nodes
if 'UP_TO_DATE' in out['abp_status']: out['saved'] = [EAL.save_loaded_asset(a, False) for a in (bp, bm, sk)]
out['dirty_after'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
(S/'data'/'gd39_body_setup.json').write_text(json.dumps(out, indent=1)); print('GD39_BODY_SETUP', json.dumps(out))
