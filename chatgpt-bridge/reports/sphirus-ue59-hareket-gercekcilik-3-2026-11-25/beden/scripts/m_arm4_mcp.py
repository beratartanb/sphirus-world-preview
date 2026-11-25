# m_arm4_mcp.py (MCP, in-memory; BP_HybridA_Player GR_Posture; after m_arm3; re-appliable) - B4 follow-up.
# Real-surface measurement (b4_armsurf.py: offline skinning of the B4 body + shorts with the logged bone transforms) showed the PALM and
# FINGERS entering the shorts layer (up to 4.6 cm forward, 7.3 cm in the backward jog) while the wrist proxy said "clear": the clearance
# point moves from the wrist joint to the palm centre (hand -> middle_01 at CA_Palm), and the B4 thigh radius + shorts layer is used.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10); K = '`KismetMathLibrary.%s`'; V = lambda n: '(`self.%s`)' % n
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
if '"CA_Palm"' not in have:
    T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': 'CA_Palm', 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': 'CA_Palm', 'bInstanceEditable': True}); T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '`self.CA_Palm`' in dsl: print('ARM4 already'); sys.exit(0)
S = lambda b: '(`SceneComponent.GetSocketLocation` (`self.Manny`) "%s")' % b; edits = []
for f, h in (('L', '_returnvalue_13'), ('R', '_returnvalue_14')):
    s = f.lower(); m = [x for x in dsl.split(NL) if x.startswith('  (set `self.CA_C%s` ' % f)]; assert len(m) == 1; l = m[0]; assert l.count(h) == 2, l.count(h)
    palm = '(%s %s %s %s)' % (K % 'VLerp', h, S('middle_01_' + s), V('CA_Palm'))
    edits.append({'oldString': l, 'newString': l.replace(h, palm)})
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': edits})
print('ARM4', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:2500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200])
