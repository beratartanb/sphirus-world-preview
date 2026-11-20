# m_revclip4_mcp.py (MCP, in-memory): RcVin back to the speed of the first reversal frame (the capsule is already braked in that
# frame; binding K to the pre-brake speed made the capsule 10 % faster than the clip: run A->D planted foot 5 -> 22 cm).
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; BP = AP + '.AC_Sph_Motion'; NL = chr(10)
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
SPD = '(`KismetMathLibrary.VSizeXY` (`Actor.GetVelocity` _ascharacter))'
old = '(`KismetMathLibrary.FMax` %s (`self.RcPrevV`))' % SPD
L = [l for l in dsl.split(NL) if l.strip().startswith('(set `self.RcVin`')]; assert len(L) == 1 and L[0].count(old) == 1, 'RcVin form'
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': L[0], 'newString': L[0].replace(old, SPD)}]})
out = {'edit': str(r2)[:1500] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'}
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200]
print('REVCLIP4', json.dumps(out)[:2000])
