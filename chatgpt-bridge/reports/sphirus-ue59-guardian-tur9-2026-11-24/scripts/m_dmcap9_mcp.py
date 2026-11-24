# m_dmcap9_mcp.py (MCP, in-memory; AC_Sph_Motion + BP_Sph_GASPCharacter; re-appliable) - round 9.
# Run -> walk, real cause: the trajectory prediction of the gait step-down reaches walk speed in ~0.25 s (velocity is pulled to
# input x MaxWalkSpeed by friction), whatever the braking is. Motion Matching therefore takes the walk loop at once, or leaves the
# transition clip the moment its braking steps begin. The step-down is now a RAMPED SPEED LIMIT: AC_Sph_Motion.DmCap remembers the
# speed and falls by max(DmRate, DmCap x DmRateK) per second while the input is held (no reversal); MaxWalkSpeed = max(gait speed, DmCap).
# The capsule, the prediction and the transition clip slow down together (run -> walk ~0.8 s, sprint -> walk ~1.05 s).
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
MA = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; MB = MA + '.AC_Sph_Motion'; AP = '/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'; BP = AP + '.BP_Sph_GASPCharacter'; NL = chr(10); out = {}
M = '`/Game/Sphirus/Player/Motion/AC_Sph_Motion.%s` (`self.SphMotion`)'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': MB}}))
for n in ('DmCap', 'DmRate', 'DmRateK'):
    if '"%s"' % n not in have:
        T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': MB}, 'name': n, 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': MB}, 'variableName': n, 'bInstanceEditable': True})
T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': MB}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': MA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if 'self.DmCap`' in dsl: out['cap'] = 'already'
else:
    l = [x for x in dsl.split(NL) if x.strip().startswith('(set `self.RcT` ')]; assert len(l) == 1; l = l[0]; ind = l[:len(l) - len(l.lstrip())]
    SP = '(`KismetMathLibrary.VSizeXY` (`Actor.GetVelocity` _ascharacter))'
    new = ind + '(set `self.DmCap` (`KismetMathLibrary.SelectFloat` (`KismetMathLibrary.FMax` %s (- (`self.DmCap`) (* (`KismetMathLibrary.FMax` (`self.DmRate`) (* (`self.DmCap`) (`self.DmRateK`))) DeltaSeconds))) %s (and (> (`KismetMathLibrary.VSizeXY` (`Pawn.GetLastMovementInputVector` _ascharacter)) 0.1) (<= (`self.RcW`) 0.01))))' % (SP, SP)
    r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': MA, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': l, 'newString': l + NL + new}]})
    out['cap'] = 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1200]
out['compM'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': MB}, 'bWarningsAsErrors': False}))[:100]
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': 'CalculateMaxSpeed'}); rv = r['content']['returnValue']; dsl = rv['dsl']
l = [x for x in dsl.split(NL) if x.strip().startswith('(return ')]; assert len(l) == 1; l = l[0]
pre = '(return (`KismetMathLibrary.FMin` '; suf = ' (%s))' % (M % 'TurnCap')
s_ = l.strip()
if 'DmCap' in l: out['max'] = 'already'
elif s_.startswith(pre) and suf in s_:
    i = s_.rindex(suf); G = s_[len(pre):i]; tail = s_[i:]
    new = l[:len(l) - len(l.lstrip())] + pre + '(`KismetMathLibrary.FMax` %s (`KismetMathLibrary.SelectFloat` (%s) 0.0 (%s)))' % (G, M % 'DmCap', M % 'DmOn') + tail
    r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': 'CalculateMaxSpeed', 'edits': [{'oldString': l, 'newString': new}]})
    out['max'] = 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1200]
else: out['max'] = 'PATTERN? ' + s_[-200:]
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:100]
print('DMCAP9', json.dumps(out))
