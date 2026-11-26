# m_fall5_mcp.py (MCP, in-memory): during the ragdoll the capsule (camera owner) follows the pelvis in XY without teleporting physics,
# so the camera keeps the body in view; the roll-over impulse goes to every body (pelvis down) instead of the upper body only.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10)
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if 'FALL5' in dsl or '(.z (`Actor.K2_GetActorLocation` self)) ) false false)' in dsl: print('FALL5 already'); sys.exit()
L = dsl.split(NL); edits = []
s1 = [i for i, x in enumerate(L) if '(< (`self.FL_State`) 1.5))' in x and x.lstrip().startswith('(if')]; assert len(s1) == 1, s1
j = s1[0] + 1; assert L[j].strip() == '(set `self.FL_T` (+ (`self.FL_T`) DeltaSeconds))', L[j]
ind = L[j][:len(L[j]) - len(L[j].lstrip())]; P = '(`SceneComponent.GetSocketLocation` (`self.Mesh`) "pelvis")'
follow = ind + '(`Actor.K2_SetActorLocation` self (`KismetMathLibrary.MakeVector` (.x %s) (.y %s) (.z (`Actor.K2_GetActorLocation` self))) false false)' % (P, P)
edits.append({'oldString': L[s1[0]] + NL + L[j], 'newString': L[s1[0]] + NL + L[j] + NL + follow})
rl = [i for i, x in enumerate(L) if 'AddImpulseToAllBodiesBelow' in x and '"spine_02" true true' in x and 'FL_Roll' in x]; assert len(rl) == 1, rl
edits.append({'oldString': L[rl[0]], 'newString': L[rl[0]].replace('"spine_02" true true', '"pelvis" true true')})
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': edits})
print('FALL5', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:2000], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200])
