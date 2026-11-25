# m_arm5_mcp.py (MCP, in-memory; after m_arm4; re-appliable) - the palm also keeps clear of the PELVIS front (hip-joint line thigh_l ->
# thigh_r, radius CA_RadP): in the backward jog the hands cross in front of the pelvis (wrists 0.5 cm from the midline) where the thigh
# segment test sees nothing. Clearance = min(thigh clearance, pelvis clearance).
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10); K = '`KismetMathLibrary.%s`'; V = lambda n: '(`self.%s`)' % n
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
if '"CA_RadP"' not in have:
    T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': 'CA_RadP', 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': 'CA_RadP', 'bInstanceEditable': True}); T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '`self.CA_RadP`' in dsl: print('ARM5 already'); sys.exit(0)
S = lambda b: '(`SceneComponent.GetSocketLocation` (`self.Manny`) "%s")' % b; edits = []
for f, h in (('L', '_returnvalue_13'), ('R', '_returnvalue_14')):
    s = f.lower(); m = [x for x in dsl.split(NL) if x.startswith('  (set `self.CA_C%s` ' % f)]; assert len(m) == 1; l = m[0]
    val = l.strip()[len('(set `self.CA_C%s` ' % f):-1]
    palm = '(%s %s %s %s)' % (K % 'VLerp', h, S('middle_01_' + s), V('CA_Palm'))
    pel = '(- (%s (- %s (%s %s %s %s))) %s)' % (K % 'VSize', palm, K % 'FindClosestPointOnSegment', palm, S('thigh_l'), S('thigh_r'), V('CA_RadP'))
    edits.append({'oldString': l, 'newString': '  (set `self.CA_C%s` (%s %s %s))' % (f, K % 'FMin', val, pel)})
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': edits})
print('ARM5', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:2500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200])
