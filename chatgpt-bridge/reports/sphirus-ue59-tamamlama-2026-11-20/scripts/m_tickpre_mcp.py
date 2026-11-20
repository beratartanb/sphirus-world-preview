# m_tickpre_mcp.py (MCP, in-memory): the pawn ticks after its controller (AddTickPrerequisiteActor once), so the input handled by the
# controller in this frame (GR_RawIn) is already known when the pawn tick writes the back/strafe/gait state.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = AP + '.BP_HybridA_Player'; out = {}
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
if '"GR_TickPre"' not in have:
    T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': 'GR_TickPre', 'typeName': 'bool'})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
L = [l for l in dsl.split('\n') if l.strip().startswith('(set `self.GR_StopHold`')]; assert len(L) == 1; ind = L[0][:len(L[0]) - len(L[0].lstrip())]
new = '\n'.join(ind + s for s in ("(if (and (not (`self.GR_TickPre`)) (`KismetSystemLibrary.IsValid` (`self.GetController`)))",
                                  "  (`self.AddTickPrerequisiteActor` (`self.GetController`))",
                                  "  (set `self.GR_TickPre` true))")) + '\n' + L[0]
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': L[0], 'newString': new}]})
out['edit'] = str(r2)[:900] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200]
print('TICKPRE', json.dumps(out)[:1200])
