"""RV J-drivers: pose-space curve drivers for the soft-tissue and garment correctives, installed at the end of the isolated
revision body PostProcess ABP (ABP_RV_Body_PostProcess) after the existing (accepted, untouched) SHC drivers.
PoseDriver DriveCurves mode: target DrivenNames are curves (morph targets of the same name on the body AND on the leader-posed
garments); RVn_* targets are null anchors that pin the curves to 0 near those poses.
  RV_Bend:  spine_05 in root space (swing)      -> RV_Bend30 / RV_Bend60 / RV_Bend90
  RV_Twist: spine_05 in pelvis space (twist)    -> RV_Twist_l / RV_Twist_r
  RV_Arm_s: upperarm_s in spine_05 space (swing)-> RV_Arm090_s / RV_Arm120_s / RV_Arm150_s / RV_Arm180_s / RV_ArmFwd_s
  RV_Hip_s: thigh_s in pelvis space (swing)     -> RV_Hip075_s (hip flexion) / RV_Hip110_s (deep squat)
Target rotations: captured bone transforms of this body (b0_bodyrev_*_front.json) and the SHC arm ladder (driver_targets.json)."""
import unreal as u, sys, pathlib, json, shutil, math
P = pathlib.Path(u.Paths.project_dir()).resolve()
sys.path.insert(0, str(P/'Saved/Codex/GraceRanger_QA_20260914/Scripts'))
from editor_toolset.toolsets.blueprint import BlueprintTools as B
from qa_graph import connect, disconnect, src, pn, info, obj
S = P/'Saved/Codex/CharacterRevision_20260930'; C = S/'captures'
BP = '/Game/Sphirus/CharacterLab/CharacterRevision_20260930/Body/ABP_RV_Body_PostProcess'
TG = json.loads((P/'Saved/Codex/CharacterShoulderFix_20260928/HighElevCorrective_20260929/driver_targets.json').read_text())
def bt(pose):
    return json.loads((C/f'b0_bodyrev_{pose}_front.json').read_text())['bone_transforms']['Body']
def rel(pose, src_bone, space):
    T = bt(pose); qa = u.Quat(*T[space]['rotation']) if space != 'root' else u.Quat(0, 0, 0, 1); qb = u.Quat(*T[src_bone]['rotation'])
    r = (qa.inversed()*qb).rotator(); return [r.pitch, r.yaw, r.roll]
def target(rot, name):
    return '(BoneTransforms=((TargetTranslation=(X=0.000000,Y=0.000000,Z=0.000000),TargetRotation=(Pitch=%.6f,Yaw=%.6f,Roll=%.6f))),DrivenName="%s")' % (rot[0], rot[1], rot[2], name)
DRIVERS = []
DRIVERS.append(('RV_Bend', 'spine_05', 'root', 'SwingAngle', 32.0, [(rel('neutral', 'spine_05', 'root'), 'RVn_bend0'), (rel('backext', 'spine_05', 'root'), 'RVn_backext'),
               (rel('pl_bend30', 'spine_05', 'root'), 'RV_Bend30'), (rel('pl_bend60', 'spine_05', 'root'), 'RV_Bend60'), (rel('pl_bend90', 'spine_05', 'root'), 'RV_Bend90')]))
DRIVERS.append(('RV_Twist', 'spine_05', 'pelvis', 'TwistAngle', 30.0, [(rel('neutral', 'spine_05', 'pelvis'), 'RVn_twist0'), (rel('pl_twist_l', 'spine_05', 'pelvis'), 'RV_Twist_l'),
               (rel('pl_twist_r', 'spine_05', 'pelvis'), 'RV_Twist_r')]))
for s in 'lr':
    arm = [(TG[f'{s}_{p}']['rot'], f'RVn_{p}_{s}') for p in ('neutral', 'elev_0', 'elev_30', 'elev_60')]
    arm += [(TG[f'{s}_elev_90']['rot'], f'RV_Arm090_{s}'), (TG[f'{s}_elev_120']['rot'], f'RV_Arm120_{s}'), (TG[f'{s}_elev_150']['rot'], f'RV_Arm150_{s}'),
            (TG[f'{s}_elev_180']['rot'], f'RV_Arm180_{s}'), (TG[f'{s}_forward90']['rot'], f'RV_ArmFwd_{s}')]
    DRIVERS.append((f'RV_Arm_{s}', f'upperarm_{s}', 'spine_05', 'SwingAngle', 30.0, arm))
    hip = [(rel('neutral', f'thigh_{s}', 'pelvis'), f'RVn_hip0_{s}'), (rel('hipflex', f'thigh_{s}', 'pelvis'), f'RV_Hip075_{s}'), (rel('squat', f'thigh_{s}', 'pelvis'), f'RV_Hip110_{s}')]
    DRIVERS.append((f'RV_Hip_{s}', f'thigh_{s}', 'pelvis', 'SwingAngle', 40.0, hip))
# report target angles (sanity)
def qang(pose_a, pose_b, src_bone, space):
    ra = u.Rotator(*[0, 0, 0]);
    return None
ck = S/'checkpoint_pre_drivers'; ck.mkdir(exist_ok=True)
f = P/('Content'+BP[len('/Game'):]+'.uasset'); shutil.copy2(f, ck/f.name)
bp = u.load_asset(BP)
assert not [n for n in u.AnimationLibrary.get_nodes_of_class(bp, u.AnimGraphNode_PoseDriver, True) if str(n.get_editor_property('tag')).startswith('RV_')], 'RV drivers already installed'
ag = [g for g in B.list_graphs(bp) if g.get_name() == 'AnimGraph'][0]
root = [n for n in B.find_nodes(ag) if pn(n).rsplit('.', 1)[-1].startswith('AnimGraphNode_Root')][0]; rootp = pn(root)
rpins = [q.name for q in info(rootp).input_pins]; rin = 'Result' if 'Result' in rpins else rpins[0]
prev = src((rootp, rin)); assert len(prev) == 1, prev
nodes = []; out = {'drivers': {}}
for i, (tag, sbone, space, dist, radius, targets) in enumerate(DRIVERS):
    n = pn(B.create_node(ag, 'Animasyon|Pozlar|PozSürücüsü', u.IntPoint(1400+300*i, 1300)))
    o = obj(n); o.set_editor_property('tag', tag); nd = o.get_editor_property('node')
    txt = ('(SourceBones=((BoneName="%s")),EvalSpaceBone=(BoneName="%s"),bEvalFromRefPose=False,OnlyDriveBones=,'
           'PoseTargets=(%s),RBFParams=(TargetDimensions=3,SolverType=Interpolative,Radius=%.6f,bAutomaticRadius=False,Function=Gaussian,'
           'DistanceMethod=%s,TwistAxis=BA_X,WeightThreshold=0.030000,NormalizeMethod=AlwaysNormalize,MedianReference=(X=0.000000,Y=0.000000,Z=0.000000),'
           'MedianMin=45.000000,MedianMax=60.000000),DriveSource=Rotation,DriveOutput=DriveCurves,PoseAsset=None)') % (sbone, space, ','.join(target(r, nm) for r, nm in targets), radius, dist)
    nd.import_text(txt); chk = nd.export_text()
    assert 'DriveOutput=DriveCurves' in chk and targets[-1][1] in chk and f'EvalSpaceBone=(BoneName="{space}")' in chk, chk[:600]
    o.set_editor_property('node', nd); nodes.append(n)
    out['drivers'][tag] = {'source': sbone, 'space': space, 'distance': dist, 'radius': radius, 'targets': {nm: [round(x, 2) for x in r] for r, nm in targets}}
ins = [q.name for q in info(nodes[0]).input_pins]; outs = [q.name for q in info(nodes[0]).output_pins]
sp = [x for x in ins if 'Pose' in x][0]; op = [x for x in outs if 'Pose' in x][0]
disconnect((rootp, rin)); connect(prev[0], (nodes[0], sp))
for a, b in zip(nodes, nodes[1:]): connect((a, op), (b, sp))
connect((nodes[-1], op), (rootp, rin))
u.BlueprintEditorLibrary.compile_blueprint(bp)
out['status'] = str(bp.status); out['root_src_before'] = prev[0][0].rsplit('.', 1)[-1]
if 'UP_TO_DATE' in out['status']: out['saved'] = u.EditorAssetLibrary.save_loaded_asset(bp, False)
# register the new curves as morph-target curves on the (shared) skeleton copy is NOT done here: see ue_rv_curvemeta.py
out['dirty_after'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
(S/'rv_drivers.json').write_text(json.dumps(out, indent=1)); print(json.dumps({k: v for k, v in out.items() if k != 'drivers'}, indent=1)); print({k: list(v['targets']) for k, v in out['drivers'].items()})
