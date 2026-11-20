# m_tickfix_mcp.py (MCP, in-memory edit of BP_HybridA_Player): the engine gives the pawn's actor tick a prerequisite on its
# CharacterMovementComponent; with "AC_PreCMCTick after the pawn" (round 4) that formed a cycle and the engine dropped an edge with
# a LogTick warning every frame. The pawn-after-CMC prerequisite is now removed explicitly before the new one is added.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = AP + '.BP_HybridA_Player'; NL = chr(10)
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
assert 'RemoveTickPrerequisiteComponent' not in dsl, 'already built'
L = [l for l in dsl.split(NL) if 'AddTickPrerequisiteActor` (`self.AC_PreCMCTick`) self)' in l]; assert len(L) == 1, len(L)
ind = L[0][:len(L[0]) - len(L[0].lstrip())]
new = ind + '(`self.RemoveTickPrerequisiteComponent` (`self.CharacterMovement`))' + NL + L[0]
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': L[0], 'newString': new}]})
out = {'edit': str(r2)[:1500] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'}
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:300]
print('TICKFIX', json.dumps(out)[:2000])
