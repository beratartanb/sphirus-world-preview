# m_revclip2_mcp.py (MCP, in-memory edit of AC_Sph_Motion; refinement of m_revclip_mcp.py) - 2026-11-21 round 4.
#  RcVin  speed latched when the reversal starts.   RcK = min over the first RcLatch s of RcVin / curve (entry speed against the
#         clip's speed BEFORE its brake; the first version tracked the current speed and drifted to 0.5-0.8 or 1.8).
#  RcA    lower bound = max(RcMin, RcVin / RcTz): the velocity crosses zero within about RcTz s even when Motion Matching enters the
#         turn clip long before its brake (control response); upper bound RcMax.
#  exit cap only while input is held (a stop after the turn is owned by the clip-bound stop).
import json, sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; BP = AP + '.AC_Sph_Motion'; out = {}; NL = chr(10)
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for n in ('RcVin', 'RcTz'):
    if '"%s"' % n in have: continue
    T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': 'float'})
    T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
open('Saved/UE59Work/dsl/AC_Sph_Motion_before_revclip2.dsl', 'w', encoding='utf8').write(dsl)
assert '`self.RcW`' in dsl and '`self.RcVin`' not in dsl, 'state unexpected'
def line(prefix):
    L = [l for l in dsl.split(NL) if l.strip().startswith(prefix)]; assert len(L) == 1, (prefix, len(L)); return L[0]
M = '`KismetMathLibrary.%s`'
def v(n): return '(`self.%s`)' % n
C = '(`AnimInstance.GetCurveValue` (`SkeletalMeshComponent.GetAnimInstance` (`Character.Mesh` _ascharacter)) "movedata_speed")'
SPD = '(%s (`Actor.GetVelocity` _ascharacter))' % (M % 'VSizeXY')
DT = '(%s DeltaSeconds 0.001)' % (M % 'FMax')
rcw = line('(set `self.RcW`'); rct = line('(set `self.RcT`'); rck = line('(set `self.RcK`'); rca = line('(set `self.RcA`'); tc = line('(set `self.TurnCap`')
ind = rck[:len(rck) - len(rck.lstrip())]
m = re.search(r'\(> \(`KismetMathLibrary\.VSizeXY` (_[a-z0-9_]+)\) 0\.1\)', rcw); assert m; HASIN = m.group(0)
RATIO = '(/ %s (%s %s 50.0))' % (v('RcVin'), M % 'FMax', C)
# RcT is still the value of the previous frame when RcVin / RcK are evaluated: the lines are placed BEFORE the RcT update
vin = ind + '(set `self.RcVin` (%s %s %s (and (> %s 0.01) (<= %s 0.0))))' % (M % 'SelectFloat', SPD, v('RcVin'), v('RcW'), v('RcT'))
k_new = ind + '(set `self.RcK` (%s (%s (%s (%s 1.8 %s (<= %s 0.0)) %s) 0.5 1.8) %s (and (> %s 0.01) (< %s %s))))' % (
    M % 'SelectFloat', M % 'FClamp', M % 'FMin', M % 'SelectFloat', v('RcK'), v('RcT'), RATIO, v('RcK'), v('RcW'), v('RcT'), v('RcLatch'))
a_new = ind + '(set `self.RcA` (%s (%s %s (%s (/ (- %s (* %s (%s (- (* 2.0 %s) %s) 0.0))) %s) (%s %s (/ %s (%s %s 0.1))) %s) (and (> %s (+ %s 2.0)) (> %s 0.15))) 0.0 (> %s 0.01)))' % (
    M % 'SelectFloat', M % 'SelectFloat', v('RcMax'), M % 'FClamp', SPD, v('RcK'), M % 'FMax', C, v('RcPrevC'), DT,
    M % 'FMax', v('RcMin'), v('RcVin'), M % 'FMax', v('RcTz'), v('RcMax'), C, v('RcPrevC'), v('RcT'), v('RcW'))
old_cond = '(and (and (> %s 0.0) (<= %s 0.01)) (> %s 1.0))' % (v('RcExit'), v('RcW'), C)
assert tc.count(old_cond) == 1, 'exit cap condition not found'
tc_new = tc.replace(old_cond, '(and (and (and (> %s 0.0) (<= %s 0.01)) (> %s 1.0)) %s)' % (v('RcExit'), v('RcW'), C, HASIN))
# order: RcW, RcVin, RcK (use previous RcT), RcT, RcA
edits = [{'oldString': rct + NL + rck, 'newString': vin + NL + k_new + NL + rct}, {'oldString': rca, 'newString': a_new}, {'oldString': tc, 'newString': tc_new}]
assert dsl.count(rct + NL + rck) == 1, 'RcT/RcK lines not adjacent'
if '--dry' in sys.argv: print(vin); print(k_new); print(a_new[:900]); sys.exit(0)
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': edits})
out['edit'] = str(r2)[:2200] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200]
print('REVCLIP2', json.dumps(out)[:3000])
