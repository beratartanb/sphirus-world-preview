# m_dmcap9b_mcp.py (MCP, in-memory; re-appliable; run after m_dmcap9_mcp.py) - round 9: corrected ramp.
# m_dmcap9 made DmCap = max(speed, DmCap - rate x dt): the capsule runs AT the limit, so the limit reset itself every frame and never fell.
# Now the character publishes the RAW gait speed (gait x direction map, before turn / context scales) as AC_Sph_Motion.GaitV and
#   DmCap = max(GaitV, DmCap - max(DmRate, DmCap x DmRateK) x dt)   while the input is held and no reversal is active; otherwise = speed.
# MaxWalkSpeed = min(max(raw gait speed, DmCap) x SpeedScale x context, TurnCap): only gait step-downs are ramped; turn speed loss,
# context scale and the turn cap act as before.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
MA = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; MB = MA + '.AC_Sph_Motion'; AP = '/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'; BP = AP + '.BP_Sph_GASPCharacter'; NL = chr(10); out = {}
M = '`/Game/Sphirus/Player/Motion/AC_Sph_Motion.%s` (`self.SphMotion`)'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': MB}}))
if '"GaitV"' not in have:
    T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': MB}, 'name': 'GaitV', 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': MB}, 'variableName': 'GaitV', 'bInstanceEditable': True})
T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': MB}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': MA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
l = [x for x in dsl.split(NL) if x.strip().startswith('(set `self.DmCap` ')]; assert len(l) == 1; l = l[0]; ind = l[:len(l) - len(l.lstrip())]
SP = '(`KismetMathLibrary.VSizeXY` (`Actor.GetVelocity` _ascharacter))'
new = ind + '(set `self.DmCap` (`KismetMathLibrary.SelectFloat` (`KismetMathLibrary.FMax` (`self.GaitV`) (- (`self.DmCap`) (* (`KismetMathLibrary.FMax` (`self.DmRate`) (* (`self.DmCap`) (`self.DmRateK`))) DeltaSeconds))) %s (and (> (`KismetMathLibrary.VSizeXY` (`Pawn.GetLastMovementInputVector` _ascharacter)) 0.1) (<= (`self.RcW`) 0.01))))' % SP
if l.strip() == new.strip(): out['cap'] = 'already'
else:
    r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': MA, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': l, 'newString': new}]})
    out['cap'] = 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1200]
out['compM'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': MB}, 'bWarningsAsErrors': False}))[:100]
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': 'CalculateMaxSpeed'}); rv = r['content']['returnValue']; dsl = rv['dsl']
l = [x for x in dsl.split(NL) if x.strip().startswith('(return ')]; assert len(l) == 1; l = l[0]; s_ = l.strip(); ind = l[:len(l) - len(l.lstrip())]
if 'GaitV' in dsl: out['max'] = 'already'
else:
    a0 = '(`KismetMathLibrary.SelectFloat` (`KismetMathLibrary.MapRangeClamped` _strafespeedmap 0.0 1.0'; a1 = ' (%s))' % (M % 'SpeedScale')
    i0 = s_.index(a0); i1 = s_.index(a1); SEL = s_[i0:i1]
    wrap = '(`KismetMathLibrary.FMax` %s (`KismetMathLibrary.SelectFloat` (%s) 0.0 (%s)))' % ('%s', M % 'DmCap', M % 'DmOn')
    old_w = wrap % ''  # not used
    pre = '(return (`KismetMathLibrary.FMin` '; cur_wrap_start = pre + '(`KismetMathLibrary.FMax` (* (* '
    assert s_.startswith(cur_wrap_start), s_[:120]
    suf_old = ' (`KismetMathLibrary.SelectFloat` (%s) 0.0 (%s)))' % (M % 'DmCap', M % 'DmOn')
    j = s_.rindex(suf_old); G = s_[len(pre) + len('(`KismetMathLibrary.FMax` '):j]; tail = s_[j + len(suf_old):]
    assert G.count(SEL) == 1
    newret = ind + pre + G.replace(SEL, wrap % SEL) + tail
    setl = ind + '(set `/Game/Sphirus/Player/Motion/AC_Sph_Motion.GaitV` %s (`self.SphMotion`))' % SEL
    r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': 'CalculateMaxSpeed', 'edits': [{'oldString': l, 'newString': setl + NL + newret}]})
    out['max'] = 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1500]
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:100]
print('DMCAP9B', json.dumps(out))
