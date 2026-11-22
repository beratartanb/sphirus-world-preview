# m_gov6c_mcp.py (MCP, in-memory; BP_Sph_GASPCharacter CalculateBrakingDeceleration + CalculateGroundFriction) - round 6.
# Sprint 180 at 30 Hz / variable Hz (g6_B_30 26 cm, g6_B_var 58 cm; 60 Hz 3.5 cm). Measured (an_dump6 g6_B_var t 15.2-15.5):
#  a) the frame in which the input reverses still ran with full ground friction (the motion component sees the reversal one frame
#     later): 584 -> 392 cm/s in one 45 ms frame;  b) while the capsule was already slower than the clip, the held-input braking floor
#     of 500 cm/s2 (over-max-speed braking) kept decelerating it (650 cm/s2 against a commanded 150), so the capsule ran ~100-160 cm/s
#     below the clip while the pivot foot was planted.
#  -> a) ground friction is scaled by RcFric in the same frame when the acceleration opposes the velocity above RcSpMin;
#     b) the 500 floor does not apply while the clip-bound reversal (RcW) is active.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
GC = '/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'; MOT = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; NL = chr(10); out = {}
def mot(n): return '(`%s.%s` (`self.SphMotion`))' % (MOT, n)
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': GC, 'scope': 'CalculateBrakingDeceleration'}); rv = r['content']['returnValue']; d = rv['dsl']
a = '(`KismetMathLibrary.FMax` 500.0 %s)' % mot('RevDecel')
if a in d:
    r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': GC, 'revision': rv['revision'], 'scope': 'CalculateBrakingDeceleration', 'edits': [{'oldString': a, 'newString': '(`KismetMathLibrary.FMax` (`KismetMathLibrary.SelectFloat` 0.0 500.0 (> %s 0.01)) %s)' % (mot('RcW'), mot('RevDecel'))}]})
    out['brake'] = 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:900]
else: out['brake'] = 'already / not found'
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': GC, 'scope': 'CalculateGroundFriction'}); rv = r['content']['returnValue']; d = rv['dsl']
if 'RcFric' not in d:
    l = [x for x in d.split(NL) if x.strip().startswith('(return ')]; assert len(l) == 1; l = l[0]; s = l.strip(); ind = l[:len(l) - len(s)]; assert s.endswith('))')
    V = '(`MovementComponent.Velocity` (`self.CharacterMovement`))'; A = '(`CharacterMovementComponent.GetCurrentAcceleration` (`self.CharacterMovement`))'
    opp = '(and (> (`KismetMathLibrary.VSizeXY` %s) %s) (< (`KismetMathLibrary.Dot_VectorVector` (`KismetMathLibrary.Vector_Normal2D` %s 0.0001) (`KismetMathLibrary.Vector_Normal2D` %s 0.0001)) -0.7))' % (V, mot('RcSpMin'), A, V)
    new = ind + '(return (* %s (`KismetMathLibrary.SelectFloat` %s 1.0 (and %s %s))))' % (s[len('(return '):-2], mot('RcFric'), mot('RcOn'), opp) + ')'
    r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': GC, 'revision': rv['revision'], 'scope': 'CalculateGroundFriction', 'edits': [{'oldString': l, 'newString': new}]})
    out['fric'] = 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1200]
else: out['fric'] = 'already'
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': GC + '.BP_Sph_GASPCharacter'}, 'bWarningsAsErrors': False}))[:160]
print('GOV6C', json.dumps(out)[:2500])
