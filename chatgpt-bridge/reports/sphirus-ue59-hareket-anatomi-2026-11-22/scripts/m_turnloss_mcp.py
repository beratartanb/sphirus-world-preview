# m_turnloss_mcp.py (MCP, in-memory edit of AC_Sph_Motion) - 2026-11-22 round 5.
# TURN SPEED LOSS. The movement component turns the velocity toward the input with (almost) constant magnitude: a 90 deg change of
# direction at run speed cost no speed (arcade). The mocap turn clips lose speed (Relaxed_Run_Turn_090: 375 -> 286 cm/s = -24 %).
# While the input direction differs from the travel direction the max speed is capped (TurnCap) to
#     TlPeak x g(angle),  g: 0 deg 1.0 | 45 deg TlG45 | 90 deg TlG90 | 135 deg TlG135   (180 deg = clip-bound reversal, Rc)
# TlPeak = recent speed (falls TlDecay cm/s per s); effect scaled 0.3..1 between TlSpLo and TlSpHi (walk loses little). As the velocity
# aligns with the input the cap opens again and the normal acceleration brings the speed back.
import json, sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; BP = AP + '.AC_Sph_Motion'; out = {}; NL = chr(10)
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for n, ty in [(n, 'float') for n in ('TlPeak', 'TlG45', 'TlG90', 'TlG135', 'TlDecay', 'TlSpLo', 'TlSpHi', 'TlG')] + [('TlOn', 'bool')]:
    if '"%s"' % n in have: continue
    T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': ty})
    T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
open('Saved/UE59Work/dsl/AC_Sph_Motion_before_turnloss.dsl', 'w', encoding='utf8').write(dsl)
assert '`self.TlPeak`' not in dsl, 'already built'
def line(prefix):
    L = [l for l in dsl.split(NL) if l.strip().startswith(prefix)]; assert len(L) == 1, (prefix, len(L)); return L[0]
M = '`KismetMathLibrary.%s`'
def v(n): return '(`self.%s`)' % n
rcw = line('(set `self.RcW`'); tc = line('(set `self.TurnCap`'); ind = tc[:len(tc) - len(tc.lstrip())]
i0 = rcw.index('(%s ' % (M % 'Dot_VectorVector')); d = 0
for i1 in range(i0, len(rcw)):
    if rcw[i1] == '(': d += 1
    elif rcw[i1] == ')':
        d -= 1
        if d == 0: break
DOT = rcw[i0:i1 + 1]
m = re.search(r'\(> \(`KismetMathLibrary\.VSizeXY` (_[a-z0-9_]+)\) 0\.1\)', rcw); assert m; HASIN = m.group(0)
SPD = '(%s (`Actor.GetVelocity` _ascharacter))' % (M % 'VSizeXY')
MR = M % 'MapRangeClamped'
G = '(%s (%s %s 0.7 0.95 %s 1.0) (%s (%s %s 0.0 0.7 %s %s) (%s %s -0.7 0.0 %s %s) (> %s 0.0)) (> %s 0.7))' % (
    M % 'SelectFloat', MR, DOT, v('TlG45'), M % 'SelectFloat', MR, DOT, v('TlG90'), v('TlG45'), MR, DOT, v('TlG135'), v('TlG90'), DOT, DOT)
pre = [
    '(set `self.TlPeak` (%s (%s %s (- %s (* %s DeltaSeconds))) %s %s))' % (M % 'SelectFloat', M % 'FMax', SPD, v('TlPeak'), v('TlDecay'), SPD, HASIN),
    '(set `self.TlG` (%s (%s 1.0 %s (%s %s %s %s 0.3 1.0)) 1.0 (and (and %s (`self.TlOn`)) (and (> %s 100.0) (<= %s 0.01)))))' % (
        M % 'SelectFloat', M % 'Lerp', G, MR, v('TlPeak'), v('TlSpLo'), v('TlSpHi'), HASIN, SPD, v('RcW')),
]
s = tc.strip(); p = '(set `self.TurnCap` '; assert s.startswith(p) and s.count('(') == s.count(')')
inner = s[len(p):-1]
cap = '(%s (+ (* %s %s) 10.0) 100000.0 (< %s 0.999))' % (M % 'SelectFloat', v('TlPeak'), v('TlG'), v('TlG'))
tc_new = ind + '(set `self.TurnCap` (%s %s %s))' % (M % 'FMin', inner, cap)
edits = [{'oldString': tc, 'newString': NL.join(ind + x for x in pre) + NL + tc_new}]
if '--dry' in sys.argv: print(NL.join(pre)[:1800]); sys.exit(0)
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': edits})
out['edit'] = str(r2)[:2200] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200]
print('TURNLOSS', json.dumps(out)[:3000])
