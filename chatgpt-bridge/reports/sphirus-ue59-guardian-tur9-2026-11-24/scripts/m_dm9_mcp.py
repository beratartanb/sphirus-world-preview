# m_dm9_mcp.py (MCP, in-memory; AC_Sph_Motion + BP_Sph_GASPCharacter; re-appliable) - round 9.
# Run -> walk (gait step down with the input held): the capsule lost 235 cm/s in 0.35 s (governor decel clamped to 500..650 and a 500
# base braking), while the transition clip M_Neutral_Transition_Run_to_Walk needs ~0.9 s (514 -> 205 cm/s). The capsule reached walk
# speed while the clip was still in its run steps, so Motion Matching dropped the clip after 0.0-0.4 s (its braking steps never played)
# and showed the walk loop on a capsule still at 250-350 cm/s.
# Now: the governor may follow the clip all the way down (lower clamp DmMin instead of 500), the 500 base braking is off while the
# governor is active, and on the frame the gait drops (governor not active yet) the braking is DmOpen so the first predicted
# trajectory is the slow, clip-like one.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
MA = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; MB = MA + '.AC_Sph_Motion'; AP = '/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'; BP = AP + '.BP_Sph_GASPCharacter'; NL = chr(10); out = {}
M = '`/Game/Sphirus/Player/Motion/AC_Sph_Motion.%s` (`self.SphMotion`)'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': MB}}))
for n in ('DmMin', 'DmOpen'):
    if '"%s"' % n not in have:
        T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': MB}, 'name': n, 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': MB}, 'variableName': n, 'bInstanceEditable': True})
T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': MB}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': MA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
l = [x for x in dsl.split(NL) if x.strip().startswith('(set `self.DmDecel` ')]; assert len(l) == 1; l = l[0]; a = '500.0 (`self.DmMax`)'
if a in l:
    r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': MA, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': l, 'newString': l.replace(a, '(`self.DmMin`) (`self.DmMax`)')}]})
    out['dm'] = 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:900]
else: out['dm'] = 'already' if 'DmMin' in l else 'PATTERN?'
out['compM'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': MB}, 'bWarningsAsErrors': False}))[:100]
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': 'CalculateBrakingDeceleration'}); rv = r['content']['returnValue']; dsl = rv['dsl']
l = [x for x in dsl.split(NL) if x.strip().startswith('(return ')]; assert len(l) == 1; l = l[0]
a = '(`KismetMathLibrary.SelectFloat` 0.0 500.0 (> (%s) 0.01))' % (M % 'RcW')
SP = '(`KismetMathLibrary.VSizeXY` (`MovementComponent.Velocity` (`self.CharacterMovement`)))'
b = '(`KismetMathLibrary.SelectFloat` 0.0 (`KismetMathLibrary.SelectFloat` (`KismetMathLibrary.SelectFloat` 0.0 (%s) (> (%s) 0.0)) 500.0 (> %s (+ (`self.CalculateMaxSpeed`) (%s)))) (> (%s) 0.01))' % (M % 'DmOpen', M % 'DmT', SP, M % 'DmMargin', M % 'RcW')
if a in l:
    r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': 'CalculateBrakingDeceleration', 'edits': [{'oldString': l, 'newString': l.replace(a, b)}]})
    out['brk'] = 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1200]
else: out['brk'] = 'already' if 'DmOpen' in l else 'PATTERN? ' + l[:300]
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:100]
print('DM9', json.dumps(out))
