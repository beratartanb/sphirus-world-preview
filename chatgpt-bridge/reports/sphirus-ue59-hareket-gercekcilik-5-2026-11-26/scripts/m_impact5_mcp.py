# m_impact5_mcp.py (MCP, in-memory): region impacts follow the body's state - the PhysicalAnimation motor strengths of a hit are scaled
# by clamp(1 - IMP_FatK * fatigue, 0.4, 1): a tired body gives way more to the same hit.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
if '"IMP_FatK"' not in have:
    T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': 'IMP_FatK', 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': 'IMP_FatK', 'bInstanceEditable': True})
T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
old = '(make `PhysicalAnimationData` false (`self.IMP_OS`) (`self.IMP_AVS`))'
if 'IMP_FatK' in dsl: print('IMP5 already'); sys.exit()
assert dsl.count(old) == 1, dsl.count(old)
k = '(`KismetMathLibrary.FClamp` (- 1.0 (* (`self.IMP_FatK`) (`/Game/Sphirus/Player/Motion/AC_Sph_Motion.Fat` (`self.SphMotion`)))) 0.4 1.0)'
new = '(make `PhysicalAnimationData` false (* (`self.IMP_OS`) %s) (* (`self.IMP_AVS`) %s))' % (k, k)
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': old, 'newString': new}]})
print('IMP5', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200])
