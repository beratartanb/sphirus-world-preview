# m_fat3_mcp.py (MCP, in-memory; BP_HybridA_Player GR_Posture; re-appliable) - movement realism pass 3.
# EXERTION AFTER THE STOP. The breathing layer followed the short-term effort (AC_Sph_Motion.E, gone ~3 s after a stop), not the
# fatigue state (Fat, the existing single stamina value: pace, acceleration). After 15 s of running (Fat 0.67) the standing chest moved
# 0.4 cm against 0.2 cm at rest. The breathing drive is now max(effort, Fat x BR_FatK): breathing stays deeper and faster for as long
# as the existing fatigue value takes to recover, and returns to the calm idle with it. No second stamina system, no canned pose.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10); K = '`KismetMathLibrary.%s`'; V = lambda n: '(`self.%s`)' % n
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
if '"BR_FatK"' not in have:
    T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': 'BR_FatK', 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': 'BR_FatK', 'bInstanceEditable': True}); T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '`self.BR_FatK`' in dsl: print('FAT3 already'); sys.exit(0)
m = [x for x in dsl.split(NL) if x.startswith('  (set `self.PS_BrE` ')]; assert len(m) == 1; l = m[0]
E = '(`/Game/Sphirus/Player/Motion/AC_Sph_Motion.E` (`self.SphMotion`))'; a = '(%s %s %s)' % (K % 'FMax', V('PS_Eff'), E); assert l.count(a) == 1
new = '(%s %s (* (`/Game/Sphirus/Player/Motion/AC_Sph_Motion.Fat` (`self.SphMotion`)) %s))' % (K % 'FMax', a, V('BR_FatK'))
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': l, 'newString': l.replace(a, new)}]})
print('FAT3', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:2500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:160])
