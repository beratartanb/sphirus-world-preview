# m_impact4_mcp.py (MCP, in-memory): capsule push only when IMP_Push > 0 (LaunchCharacter with a zero vector still switches the movement
# mode to Falling -> landing crouch 20-30 cm while running, measured imp5_walk).
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
L = [x for x in dsl.split('\n') if 'self.LaunchCharacter' in x and 'IMP_Push' in x]; assert len(L) == 1, L
old = L[0]; ind = old[:len(old) - len(old.lstrip())]
if '(if (> (`self.IMP_Push`) 0.0)' in dsl: print('IMP4 already'); sys.exit()
new = ind + '(if (> (`self.IMP_Push`) 0.0)\n' + ind + '  ' + old.strip() + ')'
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': old, 'newString': new}]})
print('IMP4', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200])
