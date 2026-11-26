# m_fall6_mcp.py (MCP, in-memory): ground phase / roll-over by the body's actual facing.
# Measured (gu3/gu4): the on-ground target v1 used (M_ragdoll_poses_OnGround frame 0) is a SUPINE curl (shoulder normal z -1.0), so the
# muscles turned forward falls onto the back; the thigh-based prone test failed with bent legs. Now:
# - facing FL_NZ = normalized cross(neck_01 - pelvis, clavicle_r - clavicle_l).z every tick of the fall (get-up clip first frame +0.64);
# - at the ground switch the target pose follows the facing: OnGround t0.15 (prone, arms under the shoulders) when FL_NZ > -0.2, else
#   t0.01 (supine curl);
# - prone test = FL_NZ > FL_ProneMin; roll-over = side pose (OnGround t0.08) + mild lateral/up impulse (FL_Roll, up 0.35), then 0.6 s
#   later the prone pose (FL_Ph 2 -> 1).
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10); BQ = chr(96)
def K(f): return BQ + 'KismetMathLibrary.' + f + BQ
def S(v): return '(' + BQ + 'self.' + v + BQ + ')'
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for nme in ('FL_NZ', 'FL_ProneMin'):
    if '"%s"' % nme not in have:
        T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': nme, 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': nme, 'bInstanceEditable': True})
T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '(set `self.FL_NZ`' in dsl: print('FALL6 already'); sys.exit()
L = dsl.split(NL); edits = []
def one(pred, what):
    a = [i for i, x in enumerate(L) if pred(x)]; assert len(a) == 1, (what, a); return a[0]
M = S('Mesh'); AI = '(`SkeletalMeshComponent.GetAnimInstance` %s)' % M
def SL(b): return '(`SceneComponent.GetSocketLocation` %s "%s")' % (M, b)
OG = '"/Game/Characters/UEFN_Mannequin/Animations/Ragdoll/M_ragdoll_poses_OnGround.M_ragdoll_poses_OnGround"'
def pose(t, ind): return ind + '(`AnimInstance.PlaySlotAnimationAsDynamicMontage` %s %s "DefaultSlot" 0.3 0.2 0.001 1 -1.0 %s)' % (AI, OG, t)
nz = '(.z (%s (%s (- %s %s) (- %s %s))))' % (K('Normal'), K('Cross_VectorVector'), SL('neck_01'), SL('pelvis'), SL('clavicle_r'), SL('clavicle_l'))
# facing every tick of the fall (after the stillness timer)
i = one(lambda x: x.lstrip().startswith('(set `self.FL_Still` (`KismetMathLibrary.SelectFloat`'), 'still'); ind = L[i][:len(L[i]) - len(L[i].lstrip())]
edits.append({'oldString': L[i], 'newString': L[i] + NL + ind + '(set `self.FL_NZ` %s)' % nz})
# ground-phase target by facing
i = one(lambda x: 'M_ragdoll_poses_OnGround' in x and 'PlaySlotAnimationAsDynamicMontage' in x, 'gnd'); ind = L[i][:len(L[i]) - len(L[i].lstrip())]
edits.append({'oldString': L[i], 'newString': ind + '(if (> %s -0.2)' % S('FL_NZ') + NL + pose('0.15', ind + '  ') + NL + ind + '  (else' + NL + pose('0.01', ind + '    ') + '))'})
# prone test
i = one(lambda x: x.lstrip().startswith('(set `self.FL_Prone`'), 'prone'); ind = L[i][:len(L[i]) - len(L[i].lstrip())]
edits.append({'oldString': L[i], 'newString': ind + '(set `self.FL_Prone` (%s 1.0 0.0 (> %s %s)))' % (K('SelectFloat'), S('FL_NZ'), S('FL_ProneMin'))})
# roll-over: milder impulse + side pose, prone pose 0.6 s later
i = one(lambda x: 'AddImpulseToAllBodiesBelow' in x and 'FL_Roll' in x, 'roll'); ind = L[i][:len(L[i]) - len(L[i].lstrip())]
edits.append({'oldString': L[i], 'newString': L[i].replace('(* 0.6 (`self.FL_Roll`))', '(* 0.35 (`self.FL_Roll`))') + NL + pose('0.08', ind) + NL + ind + '(set `self.FL_Ph` 2.0)'})
i = one(lambda x: x.lstrip().startswith('(if (and (< (`self.FL_Ph`) 0.5) (> (`self.FL_T`) (`self.FL_GndT`)))'), 'gndif'); ind = L[i][:len(L[i]) - len(L[i].lstrip())]
edits.append({'oldString': L[i], 'newString': ind + '(if (and (> %s 1.5) (> %s 0.6))' % (S('FL_Ph'), S('FL_T')) + NL + pose('0.15', ind + '  ') + NL + ind + '  (set `self.FL_Ph` 1.0))' + NL + L[i]})
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': edits})
print('FALL6', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:3000])
print('FALL6 compile', str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:300])
