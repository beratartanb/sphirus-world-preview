# m_gov6_mcp.py (MCP, in-memory edit of AC_Sph_Motion + BP_Sph_GASPCharacter.CalculateMaxAcceleration; re-appliable) - 2026-11-23 round 6.
# CLIP-SPEED GOVERNOR. Measured root cause of the remaining planted-foot slides (b6 baseline, an_dump6.py):
#   the capsule follows K x movedata_speed of the transition clip with K latched at the entry (release speed / clip speed). While a foot is
#   planted the foot slides by (K - 1) x distance travelled: run stop K 1.18 -> 17.7 cm (b6_A_var t 41.33), sprint 180 K 0.80 / 0.89 ->
#   45 / 19 cm (b6_B_30 / _60 t 15.4), back start after a sprint stop v/md 0.65 -> 23 cm (b6_B_60 t 5.7).
#   The sprint-reversal K was additionally wrong: it was latched AFTER the first CMC frame had already removed 60-125 cm/s (entry 584 / clip
#   572 should give 1.02), and the brake had a floor of Vin / RcTz that kept decelerating when the capsule was already slower than the clip.
# Changes:
#   1 KRelax: StK / RcK / DmK move toward 1.0 at KRelax per second while NO foot is planted (both contact curves > 50) - the mismatch is
#     absorbed in the flight / swing part, the next plant happens at clip speed.
#   2 RcVin = max(speed, previous-frame speed) at the engage frame.
#   3 RcA floor: RcMin while RcT <= RcTz, the old Vin / RcTz floor only after that (a reversal can still never hang).
#   4 StBoost: during a start (StartT 0..StBoostDur) with a planted foot and the capsule slower than the clip, the max acceleration may rise
#     to (clip speed - speed) / dt (<= StBoostMax) - the start follows the clip's own push-off instead of lagging behind it.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
MOT = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; MBP = MOT + '.AC_Sph_Motion'; GC = '/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'; out = {}; NL = chr(10)
M = '`KismetMathLibrary.%s`'
AI = '(`SkeletalMeshComponent.GetAnimInstance` (`Character.Mesh` _ascharacter))'
def cv(n): return '(`AnimInstance.GetCurveValue` %s "%s")' % (AI, n)
MD = cv('movedata_speed'); V = '(`KismetMathLibrary.VSizeXY` (`Actor.GetVelocity` _ascharacter))'; INP = '(> (`KismetMathLibrary.VSizeXY` (`Pawn.GetLastMovementInputVector` _ascharacter)) 0.1)'
FREE = '(and (> %s 50.0) (> %s 50.0))' % (cv('contact_l'), cv('contact_r'))
PLANT = '(or (< %s 10.0) (< %s 10.0))' % (cv('contact_l'), cv('contact_r'))
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': MBP}}))
for n, ty in (('KRelax', 'float'), ('StBoost', 'float'), ('StBoostMax', 'float'), ('StBoostDur', 'float'), ('StBoostOn', 'bool')):
    if '"%s"' % n in have: continue
    r = T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': MBP}, 'name': n, 'typeName': ty})
    if isinstance(r, dict) and r.get('isError'): out['var_' + n] = str(r)[:200]
    T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': MBP}, 'variableName': n, 'bInstanceEditable': True})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': MOT, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
def line(prefix):
    X = [l for l in dsl.split(NL) if l.strip().startswith(prefix)]; assert len(X) == 1, (prefix, len(X)); return X[0]
def relax(var, cond): return '(set `self.%s` (%s (`self.%s`) 1.0 DeltaSeconds (%s (`self.KRelax`) 0.0 (and %s %s))))' % (var, M % 'FInterpTo_Constant', var, M % 'SelectFloat', FREE, cond)
edits = []
if '`self.KRelax`' not in dsl:
    l = line('(set `self.StK`'); ind = l[:len(l) - len(l.lstrip())]
    edits.append({'oldString': l, 'newString': l + NL + ind + relax('StK', '(and (not %s) (>= (`self.StT`) (`self.StLatch`)))' % INP)})
    l = line('(set `self.DmK`'); edits.append({'oldString': l, 'newString': l + NL + ind + relax('DmK', '(>= (`self.DmT`) 0.12)')})
    l = line('(set `self.RcK`'); edits.append({'oldString': l, 'newString': l + NL + ind + relax('RcK', '(>= (`self.RcT`) (`self.RcLatch`))')})
    l = line('(set `self.RcVin`'); a = '(set `self.RcVin` (`KismetMathLibrary.SelectFloat` ' + V + ' '; assert l.strip().startswith(a), l[:200]
    edits.append({'oldString': l, 'newString': l.replace(a, '(set `self.RcVin` (`KismetMathLibrary.SelectFloat` (%s %s (`self.RcPrevV`)) ' % (M % 'FMax', V), 1)})
    l = line('(set `self.RcA`'); fl = '(`KismetMathLibrary.FMax` (`self.RcMin`) (/ (`self.RcVin`) (`KismetMathLibrary.FMax` (`self.RcTz`) 0.1)))'; assert l.count(fl) == 1, l.count(fl)
    edits.append({'oldString': l, 'newString': l.replace(fl, '(`KismetMathLibrary.SelectFloat` %s (`self.RcMin`) (> (`self.RcT`) (`self.RcTz`)))' % fl)})
    l = line('(set `self.RcPrevC`')
    sb = '(set `self.StBoost` (%s (%s (/ (- (%s (- (* 2.0 %s) (`self.RcPrevC`)) 0.0) %s) (%s DeltaSeconds 0.001)) 0.0 (`self.StBoostMax`)) 0.0 (and (and (and (`self.StBoostOn`) %s) (and (> (`self.StartT`) 0.0) (< (`self.StartT`) (`self.StBoostDur`)))) (and (and (> %s 5.0) (< %s 330.0)) (and (<= (`self.RcW`) 0.01) %s)))))' % (
        M % 'SelectFloat', M % 'FClamp', M % 'FMax', MD, V, M % 'FMax', INP, MD, MD, PLANT)
    edits.append({'oldString': l, 'newString': sb + NL + ind + l.strip()})
    r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': MOT, 'revision': rv['revision'], 'scope': '', 'edits': edits})
    out['mot_edit'] = str(r2)[:2500] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
out['mot_compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': MBP}, 'bWarningsAsErrors': False}))[:200]
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': GC, 'scope': 'CalculateMaxAcceleration'}); rv = r['content']['returnValue']; d2 = rv['dsl']
if 'StBoost' not in d2:
    l = [x for x in d2.split(NL) if x.strip().startswith('(return ')]; assert len(l) == 1; l = l[0]; s = l.strip(); ind = l[:len(l) - len(s)]
    assert s.endswith('))'); new = ind + '(return (`KismetMathLibrary.FMax` %s (`%s.StBoost` (`self.SphMotion`)))))' % (s[len('(return '):-2], MOT)
    r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': GC, 'revision': rv['revision'], 'scope': 'CalculateMaxAcceleration', 'edits': [{'oldString': l, 'newString': new}]})
    out['gc_edit'] = str(r2)[:1500] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
    out['gc_compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': GC + '.BP_Sph_GASPCharacter'}, 'bWarningsAsErrors': False}))[:200]
print('GOV6', json.dumps(out)[:4000])
