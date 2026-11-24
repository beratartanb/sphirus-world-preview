# m_flip9_mcp.py (MCP, in-memory; BP_Sph_GASPCharacter; re-appliable) - round 9.
# Quick A/D slide root cause, part 1: the reversal governor (AC_Sph_Motion RcW/RcA) reads the LAST consumed input, so on the frame the input
# flips the CharacterMovement still has the normal acceleration / friction. The trajectory prediction made on that frame says "reversed in
# 0.25 s, 17 cm overshoot" (real: 0.3-0.45 s, 50-70 cm), and Motion Matching - which selects on that frame - enters the 180 turn clip just
# before its FINAL plant (clip time ~1.0 s: 9-24 cm of travel left). The capsule then travels ~50 cm and the plant foot slides 33-58 cm.
# Fix: on the flip frame (pending input opposes the velocity, speed > RcSpMin, governor not active yet) the pre-CMC update already uses the
# governor's opening values (acceleration RcMin, friction x RcFric), so the first prediction is the governed one.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'; BP = AP + '.BP_Sph_GASPCharacter'; NL = chr(10); M = '`/Game/Sphirus/Player/Motion/AC_Sph_Motion.%s` (`self.SphMotion`)'
SP = '(`KismetMathLibrary.VSizeXY` (`MovementComponent.Velocity` (`self.CharacterMovement`)))'
OPP = '(< (`KismetMathLibrary.Dot_VectorVector` (`KismetMathLibrary.Vector_Normal2D` (`self.GetPendingMovementInputVector`)) (`KismetMathLibrary.Vector_Normal2D` (`MovementComponent.Velocity` (`self.CharacterMovement`)))) -0.7)'
out = {}
# 1 acceleration
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': 'CalculateMaxAcceleration'}); rv = r['content']['returnValue']; dsl = rv['dsl']
l = [x for x in dsl.split(NL) if x.strip().startswith('(return ')]; assert len(l) == 1; l = l[0]
if 'GetPendingMovementInputVector' in l: out['acc'] = 'already'
else:
    s_ = l.strip(); k_ = 0; e_ = None
    for i_, c_ in enumerate(s_):
        k_ += (c_ == '(') - (c_ == ')')
        if k_ == 0: e_ = i_; break
    inner = s_[len('(return '):e_]; tail = s_[e_ + 1:]
    cond = '(and (and (%s) (<= (%s) 1.0)) (and (> %s (%s)) %s))' % (M % 'RcOn', M % 'RcA', SP, M % 'RcSpMin', OPP)
    new = l[:len(l) - len(l.lstrip())] + '(return (`KismetMathLibrary.SelectFloat` (%s) %s %s))' % (M % 'RcMin', inner, cond) + tail
    r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': 'CalculateMaxAcceleration', 'edits': [{'oldString': l, 'newString': new}]})
    out['acc'] = 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1200]
# 2 friction
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': 'CalculateGroundFriction'}); rv = r['content']['returnValue']; dsl = rv['dsl']
l = [x for x in dsl.split(NL) if x.strip().startswith('(return ')]; assert len(l) == 1; l = l[0]
a = '(> %s 480.0)' % SP
if a not in l: out['fric'] = 'already' if 'RcSpMin' in l else 'PATTERN?'
else:
    r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': 'CalculateGroundFriction', 'edits': [{'oldString': l, 'newString': l.replace(a, '(> %s (%s))' % (SP, M % 'RcSpMin'))}]})
    out['fric'] = 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1200]
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200]
print('FLIP9', json.dumps(out))
