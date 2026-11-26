# m_contact15_mcp.py (MCP, in-memory): push direction of an impulse-driven hit = away from the object (pass 6).
# Bug (fl10_table): the thrown box knocked her down TOWARD the box. RC_NS (sign of the contact normal) is taken from prevVel - otherVel, and
# the other body's velocity is already post-bounce, so the sign flips for moving-object hits. When the hit's impulse is the strong measure
# (|NormalImpulse| > RC_Mass * 200, i.e. a physics body hit her), RC_NS is chosen so that HitNormal * RC_NS points from the object to her.
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10)
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; L = rv['dsl'].split(NL)
i = [k for k, x in enumerate(L) if x.strip().startswith('(set `self.RC_VN` (`KismetMathLibrary.FMax` (`self.RC_VN`) (/ (`self.RC_Imp`)')]; assert len(i) == 1, i; i = i[0]
if 'RC_Mass`) 200.0' in L[i + 1]: print('RC15 already'); sys.exit()
ind = L[i][:len(L[i]) - len(L[i].lstrip())]
add = [ind + '(if (and (> (`self.RC_Imp`) (* (`self.RC_Mass`) 200.0)) (`KismetSystemLibrary.IsValid` OtherComp))',
       ind + '  (set `self.RC_NS` (`KismetMathLibrary.SelectFloat` 1.0 -1.0 (>= (`KismetMathLibrary.Dot_VectorVector` HitNormal (- (`Actor.K2_GetActorLocation` self) (`SceneComponent.K2_GetComponentLocation` OtherComp))) 0.0))))']
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': L[i], 'newString': L[i] + NL + NL.join(add)}]})
print('RC15', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:2500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200])
