# m_fall7_mcp.py (MCP, in-memory): roll-over as a spin about the body's long axis instead of a linear shove.
# af3_back: the linear impulse + full-strength side-pose motors bounced the body ~1 m off the ground and 4 tries never turned it over.
# Now: muscle tone drops to FL_RollK of the fall tone, and pelvis / spine_03 / spine_05 / thighs get an angular velocity change of
# FL_RollW deg/s about a = normalize(head - pelvis), direction -sign((clavicle_r - clavicle_l).z): the facing normal n = a x w then turns
# toward +w, i.e. the higher shoulder rolls over the top (n -> up = prone).
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10); BQ = chr(96)
def K(f): return BQ + 'KismetMathLibrary.' + f + BQ
def S(v): return '(' + BQ + 'self.' + v + BQ + ')'
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for nme in ('FL_RollW', 'FL_RollK'):
    if '"%s"' % nme not in have:
        T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': nme, 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': nme, 'bInstanceEditable': True})
T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if 'FL_RollW' in dsl: print('FALL7 already'); sys.exit()
L = dsl.split(NL)
i = [k for k, x in enumerate(L) if 'AddImpulseToAllBodiesBelow' in x and 'FL_Roll' in x]; assert len(i) == 1, i; i = i[0]
ind = L[i][:len(L[i]) - len(L[i].lstrip())]; M = S('Mesh')
def SL(b): return '(`SceneComponent.GetSocketLocation` %s "%s")' % (M, b)
ax = '(%s (- %s %s))' % (K('Normal'), SL('head'), SL('pelvis'))
sgn = '(%s -1.0 1.0 (> (.z (- %s %s)) 0.0))' % (K('SelectFloat'), SL('clavicle_r'), SL('clavicle_l'))
w = '(* %s (* %s %s))' % (ax, sgn, S('FL_RollW'))
new = [ind + '(`PhysicalAnimationComponent.ApplyPhysicalAnimationSettingsBelow` (`self.SphPhysAnim`) "pelvis" (make `PhysicalAnimationData` true (* (* %s %s) %s) (* (* %s %s) %s)) true)' % (S('FL_OS'), S('FL_Str'), S('FL_RollK'), S('FL_AVS'), S('FL_Str'), S('FL_RollK'))]
for b in ('pelvis', 'spine_03', 'spine_05', 'thigh_l', 'thigh_r'):
    new.append(ind + '(`PrimitiveComponent.AddAngularImpulseInDegrees` %s %s "%s" true)' % (M, w, b))
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': L[i], 'newString': NL.join(new)}]})
print('FALL7', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:2500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200])
