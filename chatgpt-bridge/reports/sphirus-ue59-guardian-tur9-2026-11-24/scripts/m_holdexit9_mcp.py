# m_holdexit9_mcp.py (MCP, in-memory; BP_HybridA_Player; re-appliable) - round 9.
# 30 Hz sprint -> back regression on the saved round-9 state (16 cm, back START clip instead of the PIVOT): the reversal governor's exit
# speed limit (AC_Sph_Motion.RcExit, armed on the flip frame) is still counting when the back-input hold (GR_StopHold) releases. On the
# release frame the limit is "stop clip speed x RcK" = 42 cm/s (57 in round 8), so the predicted trajectory is a slow start and Motion
# Matching forks to the start clip. The hold already replaces the governor for this manoeuvre: while it holds, the exit limit is cleared.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; NL = chr(10); out = {}
import glob
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
l = [x for x in dsl.split(NL) if x.strip().startswith('(set `self.GR_StopHold` ')]; assert len(l) == 1, len(l); l = l[0]
X = '`/Game/Sphirus/Player/Motion/AC_Sph_Motion.RcExit`'
if 'AC_Sph_Motion.RcExit` (`KismetMathLibrary.SelectFloat` 0.0' in dsl: out['edit'] = 'already'
else:
    ind = l[:len(l) - len(l.lstrip())]
    new = l + NL + ind + '(set %s (`KismetMathLibrary.SelectFloat` 0.0 (%s (`self.SphMotion`)) (`self.GR_StopHold`)) (`self.SphMotion`))' % (X, X)
    r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': l, 'newString': new}]})
    out['edit'] = 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1500]
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': AP + '.BP_HybridA_Player'}, 'bWarningsAsErrors': False}))[:200]
print('HOLDEXIT9', json.dumps(out))
