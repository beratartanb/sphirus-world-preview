# m_turnloss2_mcp.py (MCP, in-memory edit of AC_Sph_Motion; refinement of m_turnloss_mcp.py) - 2026-11-22 round 5.
#  1 Turn speed loss only in established movement (StartT > TlArm s since the start) and only up to ~100 deg: a reface start (the
#    capsule still turning while accelerating) was throttled to 0.76 x its own speed (planted foot 34 cm) and the 135 deg diamond
#    turn was braked ahead of its clip (22 cm). For input-velocity dot below -0.5 the factor is 1 again (diamond / reversal clips
#    and the clip-bound reversal own those).
#  2 Soft first push: for the first StSoftT s after leaving standstill the acceleration is scaled StSoftK..1 (the start clips move
#    0 / 21 / 86 / 161 cm/s in their first 0.3 s; the capsule was 20-35 cm/s ahead).
import json, sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; BP = AP + '.AC_Sph_Motion'; out = {}; NL = chr(10)
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for n in ('TlArm', 'StSoftT', 'StSoftK', 'MoveT'):
    if '"%s"' % n in have: continue
    T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': 'float'})
    T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
assert '`self.TlPeak`' in dsl and '`self.TlArm`' not in dsl, 'state unexpected'
def line(prefix):
    L = [l for l in dsl.split(NL) if l.strip().startswith(prefix)]; assert len(L) == 1, (prefix, len(L)); return L[0]
M = '`KismetMathLibrary.%s`'
def v(n): return '(`self.%s`)' % n
tg = line('(set `self.TlG`'); rcw = line('(set `self.RcW`'); acc = line('(set `self.AccScale`')
i0 = rcw.index('(%s ' % (M % 'Dot_VectorVector')); d = 0
for i1 in range(i0, len(rcw)):
    if rcw[i1] == '(': d += 1
    elif rcw[i1] == ')':
        d -= 1
        if d == 0: break
DOT = rcw[i0:i1 + 1]; MR = M % 'MapRangeClamped'
old135 = '(%s %s -0.7 0.0 %s %s)' % (MR, DOT, v('TlG135'), v('TlG90')); assert tg.count(old135) == 1, 'G135 branch not found'
tg2 = tg.replace(old135, '(%s %s -0.5 -0.2 1.0 %s)' % (MR, DOT, v('TlG90')))
oldg = '(`self.TlOn`))'; assert tg2.count(oldg) == 1
tg2 = tg2.replace(oldg, '(and (`self.TlOn`) (> (`self.MoveT`) (`self.TlArm`))))')
s = acc.strip(); p = '(set `self.AccScale` '; assert s.startswith(p) and s.count('(') == s.count(')')
ind = acc[:len(acc) - len(acc.lstrip())]
acc2 = ind + '(set `self.AccScale` (* %s (%s (`self.MoveT`) 0.0 (`self.StSoftT`) (`self.StSoftK`) 1.0)))' % (s[len(p):-1], MR)
SPD = '(%s (`Actor.GetVelocity` _ascharacter))' % (M % 'VSizeXY')
acc2 = ind + '(set `self.MoveT` (%s (+ (`self.MoveT`) DeltaSeconds) 0.0 (> %s 30.0)))' % (M % 'SelectFloat', SPD) + NL + acc2
# StartT is updated after AccScale in the tick (uses last frame's value: fine)
edits = [{'oldString': tg, 'newString': tg2}, {'oldString': acc, 'newString': acc2}]
if '--dry' in sys.argv: print(tg2[-500:]); print(acc2[-300:]); sys.exit(0)
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': edits})
out['edit'] = str(r2)[:2200] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200]
print('TURNLOSS2', json.dumps(out)[:3000])
