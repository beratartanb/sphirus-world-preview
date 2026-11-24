# m_hip1_mcp.py (MCP, in-memory; BP_HybridA_Player GR_Bob; re-appliable; needs c_hip1.py first) - movement realism pass 1.
# Hip sway owner = the gait clips' hip-line rotation (yaw) and tilt (obliquity), see c_hip1.py. Each tick: hip line from the driver's
# thigh sockets (component space), minus the correction applied last tick = the clip's own value; its slow mean (HIP_LP) is kept (turns,
# leans), only the cyclic deviation is reduced by a speed-dependent share (HIP_KY* yaw, HIP_KO* tilt: walk / run / sprint). The trunk gets
# HIP_KSp of the opposite rotation at spine_01. Active on the ground, moving, no montage (HIP_A); HIP_On 0 = off.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = AP + '.BP_HybridA_Player'; NL = chr(10); K = '`KismetMathLibrary.%s`'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for n in ('HIP_On', 'HIP_A', 'HIP_Yaw', 'HIP_Obl', 'HIP_MY', 'HIP_MO', 'HIP_LP', 'HIP_KSp', 'HIP_KYW', 'HIP_KYR', 'HIP_KYS', 'HIP_KOW', 'HIP_KOR', 'HIP_KOS'):
    if '"%s"' % n not in have:
        T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True})
T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if 'ABP_Sph_GASP.SphHipRot`' in dsl: print('HIP1M already'); sys.exit(0)
l = [x for x in dsl.split(NL) if x.strip().startswith('(set `/Game/Sphirus/Player/GASP/ABP_Sph_GASP.SphBob` ')]; assert len(l) == 1, len(l); l = l[0]; ind = l[:len(l) - len(l.lstrip())]
V = lambda n: '(`self.%s`)' % n
S = lambda b: '(.location (`SceneComponent.GetSocketTransform` (`self.Mesh`) "%s" "RTS_Component"))' % b
D = lambda ax: '(- (.%s %s) (.%s %s))' % (ax, S('thigh_r'), ax, S('thigh_l'))
YAWS = '(%s (/ %s %s))' % (K % 'DegAtan', D('y'), D('x')); OBLS = '(%s (/ %s %s))' % (K % 'DegAtan', D('z'), D('x'))
SPD = '_returnvalue_3'; DT = '_returnvalue'; GR = '_returnvalue_5'
def gain(w, r_, s): return '(%s (%s %s 415.0 585.0 %s %s) (%s %s 180.0 415.0 %s %s) (> %s 415.0))' % (K % 'SelectFloat', K % 'MapRangeClamped', SPD, V(r_), V(s), K % 'MapRangeClamped', SPD, V(w), V(r_), SPD)
lines = [
 '(set `self.HIP_A` (%s %s (%s 1.0 0.0 (and %s (and (> %s 40.0) (> %s 0.5)))) %s 4.0))' % (K % 'FInterpTo', V('HIP_A'), K % 'SelectFloat', GR, SPD, V('HIP_On'), DT),
 '(set `self.HIP_MY` (%s %s (- %s %s) %s %s))' % (K % 'FInterpTo', V('HIP_MY'), YAWS, V('HIP_Yaw'), DT, V('HIP_LP')),
 '(set `self.HIP_MO` (%s %s (- %s %s) %s %s))' % (K % 'FInterpTo', V('HIP_MO'), OBLS, V('HIP_Obl'), DT, V('HIP_LP')),
 '(set `self.HIP_Yaw` (%s (* (* (- %s) (- (- %s %s) %s)) %s) -12.0 12.0))' % (K % 'FClamp', gain('HIP_KYW', 'HIP_KYR', 'HIP_KYS'), YAWS, V('HIP_Yaw'), V('HIP_MY'), V('HIP_A')),
 '(set `self.HIP_Obl` (%s (* (* (- %s) (- (- %s %s) %s)) %s) -10.0 10.0))' % (K % 'FClamp', gain('HIP_KOW', 'HIP_KOR', 'HIP_KOS'), OBLS, V('HIP_Obl'), V('HIP_MO'), V('HIP_A')),
 '(set `/Game/Sphirus/Player/GASP/ABP_Sph_GASP.SphHipRot` (%s 0.0 %s %s) _asabp_sph_gasp)' % (K % 'MakeRotator', V('HIP_Obl'), V('HIP_Yaw')),
 '(set `/Game/Sphirus/Player/GASP/ABP_Sph_GASP.SphSpineRot` (%s 0.0 (* (- %s) %s) (* (- %s) %s)) _asabp_sph_gasp)' % (K % 'MakeRotator', V('HIP_KSp'), V('HIP_Obl'), V('HIP_KSp'), V('HIP_Yaw'))]
assert l.rstrip().endswith('_asabp_sph_gasp))'), l[-60:]   # the SphBob line also closes the event
new = l.rstrip()[:-1] + NL + NL.join(ind + x for x in lines) + ')'
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': l, 'newString': new}]})
print('HIP1M', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1800], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:100])
