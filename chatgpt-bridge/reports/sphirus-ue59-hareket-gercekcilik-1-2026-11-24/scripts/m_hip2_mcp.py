# m_hip2_mcp.py (MCP, in-memory; BP_HybridA_Player GR_Bob; after m_hip1; re-appliable) - movement realism pass 1.
# TRUNK TWIST in run / sprint: the shoulder line turns 44-47 deg per cycle in the run loop and 36-42 in sprint (an_hip.py f9_L), on the
# driver already = the clips. Same method as the hip line: shoulder-line yaw from the driver's upperarm sockets, minus the correction of
# the last tick, slow mean kept, cyclic part reduced by SH_KR (run) / SH_KS (sprint), 0 at walk. Added to the spine_01 rotation.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = AP + '.BP_HybridA_Player'; NL = chr(10); K = '`KismetMathLibrary.%s`'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for n in ('SH_Yaw', 'SH_M', 'SH_KR', 'SH_KS'):
    if '"%s"' % n not in have:
        T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True})
T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '`self.SH_Yaw`' in dsl: print('HIP2M already'); sys.exit(0)
l = [x for x in dsl.split(NL) if x.strip().startswith('(set `/Game/Sphirus/Player/GASP/ABP_Sph_GASP.SphSpineRot` ')]; assert len(l) == 1, len(l); l = l[0]; ind = l[:len(l) - len(l.lstrip())]
V = lambda n: '(`self.%s`)' % n
S = lambda b: '(.location (`SceneComponent.GetSocketTransform` (`self.Mesh`) "%s" "RTS_Component"))' % b
D = lambda ax: '(- (.%s %s) (.%s %s))' % (ax, S('upperarm_r'), ax, S('upperarm_l'))
SHY = '(%s (/ %s %s))' % (K % 'DegAtan', D('y'), D('x')); SPD = '_returnvalue_3'; DT = '_returnvalue'
KSH = '(%s (%s %s 415.0 585.0 %s %s) (%s %s 250.0 415.0 0.0 %s) (> %s 415.0))' % (K % 'SelectFloat', K % 'MapRangeClamped', SPD, V('SH_KR'), V('SH_KS'), K % 'MapRangeClamped', SPD, V('SH_KR'), SPD)
a = '(* (- %s) %s))' % (V('HIP_KSp'), V('HIP_Yaw')); assert l.count(a) == 1, l
lines = ['(set `self.SH_M` (%s %s (- %s %s) %s %s))' % (K % 'FInterpTo', V('SH_M'), SHY, V('SH_Yaw'), DT, V('HIP_LP')),
         '(set `self.SH_Yaw` (%s (* (* (- %s) (- (- %s %s) %s)) %s) -14.0 14.0))' % (K % 'FClamp', KSH, SHY, V('SH_Yaw'), V('SH_M'), V('HIP_A'))]
new = NL.join(ind + x for x in lines) + NL + l.replace(a, '(+ (* (- %s) %s) %s))' % (V('HIP_KSp'), V('HIP_Yaw'), V('SH_Yaw')))
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': l, 'newString': new}]})
print('HIP2M', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1800], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:100])
