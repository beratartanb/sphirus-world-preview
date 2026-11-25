# m_coast4b_mcp.py (MCP, in-memory; after m_coast4; re-appliable) - the coast budget becomes dynamic: CS_Budget = usable distance
# (min(sweep, floor) - CS_Margin); the coast continues only while travelled + v^2 / (2 CS_ClipDec) < CS_Budget, i.e. the remaining stop
# from the CURRENT speed still fits (the earlier fixed budget assumed the stop starts at CS_VEnd: 10 cm left at a wall from 545 cm/s).
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10); K = '`KismetMathLibrary.%s`'; V = lambda n: '(`self.%s`)' % n
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
L = dsl.split(NL)
def one(p):
    m = [x for x in L if x.startswith(p)]; assert len(m) == 1, (p, len(m)); return m[0]
SPD = '(%s (`self.GetVelocity`))' % (K % 'VSizeXY'); SD = '(/ (* %s %s) (* 2.0 %s))' % (SPD, SPD, V('CS_ClipDec'))
lb = one('      (set `self.CS_Budget` '); lc = one('      (set `self.CS_Clear` (> '); le = one('        (set `self.CS_Clear` (< ')
if 'CS_Margin`)) 0.0))' in lb: print('COAST4B already'); sys.exit(0)
edits = [{'oldString': lb, 'newString': '      (set `self.CS_Budget` (%s (- (%s %s %s) %s) 0.0))' % (K % 'FMax', K % 'FMin', V('CS_Avail'), V('CS_Floor'), V('CS_Margin'))},
         {'oldString': lc, 'newString': '      (set `self.CS_Clear` (> (- %s %s) 1.0))' % (V('CS_Budget'), SD)},
         {'oldString': le, 'newString': '        (set `self.CS_Clear` (< (+ %s %s) %s))))' % (V('CS_Dist'), SD, V('CS_Budget'))}]
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': edits})
print('COAST4B', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:3000], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:300])
