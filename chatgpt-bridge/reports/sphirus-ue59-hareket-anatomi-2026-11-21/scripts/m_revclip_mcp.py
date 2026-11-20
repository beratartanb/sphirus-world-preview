# m_revclip_mcp.py (MCP, in-memory edits of AC_Sph_Motion + BP_Sph_GASPCharacter.CalculateMaxAcceleration) - 2026-11-21 round 4.
# CLIP-BOUND REVERSAL. A 180 deg reversal (A<->D, W<->S; input opposing the velocity, dot < -0.7 .. -0.95) was decided by the
# movement component alone: friction turned the velocity at 2 x friction x speed (run A->D: 415 -> 131 cm/s in 0.1 s = 2.9 g,
# zero after 0.22 s) while the turn / pivot clip plays its own brake - plant - re-push (planted foot 11-17 cm, no body weight).
# Now, like the clip-bound stop (StK), the capsule takes the brake from the clip that Motion Matching plays:
#   RcW   0..1 reversal weight (needs input, speed > 80, RcOn)            RcK  speed / movedata_speed latched in the first RcLatch s
#   RcA   max acceleration while reversing = (speed - RcK x next curve value) / dt, clamped RcMin..RcMax  (the capsule reaches the
#         clip's root speed every frame); once the curve rises again (the clip has pivoted) RcMax, so the velocity crosses zero
#   RevFricMul -> RcFric while reversing (the friction turn no longer kills the speed)
#   exit: for RcExitDur s after the crossing the max speed is capped to RcK x curve x RcExitK + RcExitAdd (TurnCap), so the
#         capsule cannot run ahead of the re-push of the clip.
# Any other direction (dot above -0.7) leaves everything as before; the sprint stop-hold and the clip-bound stop are untouched.
import json, sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; BP = AP + '.AC_Sph_Motion'; out = {}; NL = chr(10)
GC = '/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for n, ty in [(n, 'float') for n in ('RcW', 'RcT', 'RcK', 'RcA', 'RcPrevC', 'RcExit', 'RcLatch', 'RcMin', 'RcMax', 'RcFric', 'RcExitDur', 'RcExitK', 'RcExitAdd')] + [('RcOn', 'bool')]:
    if '"%s"' % n in have: continue
    T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': ty})
    T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
open('Saved/UE59Work/dsl/AC_Sph_Motion_before_revclip.dsl', 'w', encoding='utf8').write(dsl)
assert '`self.RcW`' not in dsl, 'already built'
def line(prefix):
    L = [l for l in dsl.split(NL) if l.strip().startswith(prefix)]; assert len(L) == 1, (prefix, len(L)); return L[0]
M = '`KismetMathLibrary.%s`'
rev = line('(set `self.Rev`'); ind = rev[:len(rev) - len(rev.lstrip())]
i0 = rev.index('(%s ' % (M % 'Dot_VectorVector')); d = 0; i1 = i0
for i1 in range(i0, len(rev)):
    if rev[i1] == '(': d += 1
    elif rev[i1] == ')':
        d -= 1
        if d == 0: break
DOT = rev[i0:i1 + 1]
m = re.search(r'\(> \(`KismetMathLibrary\.VSizeXY` (_[a-z0-9_]+)\) 0\.1\)', rev); assert m, 'input test not found'
HASIN = m.group(0)
C = '(`AnimInstance.GetCurveValue` (`SkeletalMeshComponent.GetAnimInstance` (`Character.Mesh` _ascharacter)) "movedata_speed")'
SPD = '(%s (`Actor.GetVelocity` _ascharacter))' % (M % 'VSizeXY')
def v(n): return '(`self.%s`)' % n
DT = '(%s DeltaSeconds 0.001)' % (M % 'FMax')
fr = line('(set `self.RevFricMul`'); tc = line('(set `self.TurnCap`')
def inner(l, name):
    s = l.strip(); p = '(set `self.%s` ' % name; assert s.startswith(p) and s.endswith(')'); assert s.count('(') == s.count(')'), ('unbalanced line', name); return s[len(p):-1]
new = [
    '(set `self.RcW` (%s (%s %s -0.7 -0.95 0.0 1.0) 0.0 (and (and %s (`self.RcOn`)) (> %s 80.0))))' % (M % 'SelectFloat', M % 'MapRangeClamped', DOT, HASIN, SPD),
    '(set `self.RcT` (%s (+ %s DeltaSeconds) 0.0 (> %s 0.01)))' % (M % 'SelectFloat', v('RcT'), v('RcW')),
    '(set `self.RcK` (%s (%s (/ %s (%s %s 50.0)) 0.5 1.8) %s (and (> %s 0.01) (< %s %s))))' % (M % 'SelectFloat', M % 'FClamp', SPD, M % 'FMax', C, v('RcK'), v('RcW'), v('RcT'), v('RcLatch')),
    '(set `self.RcA` (%s (%s %s (%s (/ (- %s (* %s (%s (- (* 2.0 %s) %s) 0.0))) %s) %s %s) (and (> %s (+ %s 2.0)) (> %s 0.15))) 0.0 (> %s 0.01)))' % (
        M % 'SelectFloat', M % 'SelectFloat', v('RcMax'), M % 'FClamp', SPD, v('RcK'), M % 'FMax', C, v('RcPrevC'), DT, v('RcMin'), v('RcMax'), C, v('RcPrevC'), v('RcT'), v('RcW')),
    '(set `self.RcExit` (%s %s (%s (- %s DeltaSeconds) 0.0) (> %s 0.01)))' % (M % 'SelectFloat', v('RcExitDur'), M % 'FMax', v('RcExit'), v('RcW')),
    '(set `self.RevFricMul` (%s %s (%s 1.0 %s %s)))' % (M % 'FMin', inner(fr, 'RevFricMul'), M % 'Lerp', v('RcFric'), v('RcW')),
    '(set `self.RcPrevC` %s)' % C,
]
cap = '(%s (+ (* (* %s %s) %s) %s) 100000.0 (and (and (> %s 0.0) (<= %s 0.01)) (> %s 1.0)))' % (M % 'SelectFloat', C, v('RcK'), v('RcExitK'), v('RcExitAdd'), v('RcExit'), v('RcW'), C)
tc_new = ind + '(set `self.TurnCap` (%s %s %s))' % (M % 'FMin', inner(tc, 'TurnCap'), cap)
# the friction line is replaced by the block (which contains the new friction line); RcPrevC must be written after TurnCap
blk = NL.join(ind + x for x in new[:-1])
edits = [{'oldString': fr, 'newString': blk}, {'oldString': tc, 'newString': tc_new + NL + ind + new[-1]}]
if '--dry' in sys.argv: print(blk[:3000]); print(tc_new[-700:]); sys.exit(0)
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': edits})
out['edit'] = str(r2)[:2200] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200]
# CalculateMaxAcceleration: reversal acceleration from the component while RcA > 1
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': GC, 'scope': 'CalculateMaxAcceleration'}); rv = r['content']['returnValue']; d2 = rv['dsl']
open('Saved/UE59Work/dsl/gc_maxacc_before_revclip.dsl', 'w', encoding='utf8').write(d2)
if 'RcA' not in d2:
    L = [l for l in d2.split(NL) if l.strip().startswith('(return ')]; assert len(L) == 1, len(L)
    s = L[0].strip(); body = s[len('(return '):]; tail = ''
    # strip the parens that close (return ...) and the function
    while body.count(')') > body.count('('): body = body[:-1]; tail += ')'
    RCA = '(`/Game/Sphirus/Player/Motion/AC_Sph_Motion.RcA` (`self.SphMotion`))'
    newl = L[0][:len(L[0]) - len(L[0].lstrip())] + '(return (%s %s %s (> %s 1.0))' % (M % 'SelectFloat', RCA, body, RCA) + tail
    r3 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': GC, 'revision': rv['revision'], 'scope': 'CalculateMaxAcceleration', 'edits': [{'oldString': L[0], 'newString': newl}]})
    out['gc'] = str(r3)[:1500] if (not isinstance(r3, dict) or r3.get('isError')) else 'ok'
    out['gc_compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': GC + '.BP_Sph_GASPCharacter'}, 'bWarningsAsErrors': False}))[:200]
else: out['gc'] = 'present'
print('REVCLIP', json.dumps(out)[:3200])
