# m_contact14_mcp.py (MCP, in-memory): contact strength also from the physical impulse of the hit (pass 6).
# Bug (fl8_throw): a 1400 cm/s box registered vn 380 - the hit event reports the other body's velocity AFTER the collision was resolved
# (the box had already bounced off), so a moving object's approach speed is lost. The hit's NormalImpulse (kg cm/s) is the momentum the
# contact exchanged; divided by the body mass RC_Mass (60 kg) it is the velocity change the hit imposes on her. RC_VN = max(relative normal
# speed, |NormalImpulse| / RC_Mass); RC_Imp keeps |NormalImpulse| for telemetry. (Own-movement hits into static geometry report no impulse
# and keep the relative-speed measure.)
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10)
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for n in ('RC_Mass', 'RC_Imp'):
    if '"%s"' % n not in have:
        T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True})
T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; L = rv['dsl'].split(NL)
if any('RC_Imp`' in x for x in L): print('RC14 already'); sys.exit()
i = [k for k, x in enumerate(L) if x.strip().startswith('(set `self.RC_VN` (`KismetMathLibrary.Abs`')]; assert len(i) == 1, i; i = i[0]
ind = L[i][:len(L[i]) - len(L[i].lstrip())]
add = [ind + '(set `self.RC_Imp` (`KismetMathLibrary.VSize` NormalImpulse))',
       ind + '(set `self.RC_VN` (`KismetMathLibrary.FMax` (`self.RC_VN`) (/ (`self.RC_Imp`) (`KismetMathLibrary.FMax` (`self.RC_Mass`) 1.0))))']
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': L[i], 'newString': L[i] + NL + NL.join(add)}]})
print('RC14', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:2500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200])
