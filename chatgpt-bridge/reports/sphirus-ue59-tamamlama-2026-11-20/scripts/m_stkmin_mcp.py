# m_stkmin_mcp.py (MCP, in-memory edit of AC_Sph_Motion): the stop scale latch takes the LOWEST ratio (release speed / driver
# movedata_speed) seen during the latch window instead of the last one. At 30 Hz the 0.1 s window is 3 frames and the blended curve
# fell from 320 to 157 within it, so the last ratio clamped at 1.8 and the capsule outran the run stop clip (planted foot 30 cm).
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; BP = AP + '.AC_Sph_Motion'
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
L = [l for l in dsl.split('\n') if l.strip().startswith('(set `self.StK`')]; assert len(L) == 1; old = L[0]
a = "(`KismetMathLibrary.SelectFloat` (`KismetMathLibrary.FClamp` "; assert old.count(a) == 1
i = old.index(a) + len("(`KismetMathLibrary.SelectFloat` "); depth = 0; j = i
while True:
    ch = old[j]
    if ch == '(': depth += 1
    elif ch == ')':
        depth -= 1
        if depth == 0: break
    j += 1
ratio = old[i:j + 1]
new = old[:i] + "(`KismetMathLibrary.SelectFloat` %s (`KismetMathLibrary.FMin` (`self.StK`) %s) (<= (`self.StT`) (* DeltaSeconds 1.01)))" % (ratio, ratio) + old[j + 1:]
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': old, 'newString': new}]})
print('STKMIN', str(r2)[:600] if r2.get('isError') else 'ok', str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:120])
