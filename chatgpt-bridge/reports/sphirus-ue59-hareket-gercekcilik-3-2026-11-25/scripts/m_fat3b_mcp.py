# m_fat3b_mcp.py (MCP, in-memory; BP_HybridA_Player GR_Posture; after m_fat3; re-appliable) - movement realism pass 3.
# The breathing layer only pitched spine_05 by +-0.5..2 deg (chest 0.3-0.5 cm, not visible). Breathing now also lifts both shoulders
# through the existing clavicle inputs of the body graph (VI_ClavL / VI_ClavR): sin(breath phase) x BR_Sh degrees x breathing drive.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10); K = '`KismetMathLibrary.%s`'; V = lambda n: '(`self.%s`)' % n
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
if '"BR_Sh"' not in have:
    T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': 'BR_Sh', 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': 'BR_Sh', 'bInstanceEditable': True}); T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '`self.BR_Sh`' in dsl: print('FAT3B already'); sys.exit(0)
edits = []; br = '(* (* (%s %s) %s) %s)' % (K % 'Sin', V('PS_BrT'), V('BR_Sh'), V('PS_BrE'))
for f, sg in (('L', '+'), ('R', '-')):
    m = [x for x in dsl.split(NL) if x.startswith('    (set `/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP.VI_Clav%s` ' % f)]; assert len(m) == 1; l = m[0]; a = V('PS_CP' + f); assert l.count(a) == 3, l.count(a)
    edits.append({'oldString': l, 'newString': l.replace(a, '(%s %s %s)' % (sg, a, br))})
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': edits})
print('FAT3B', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:2500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:160])
