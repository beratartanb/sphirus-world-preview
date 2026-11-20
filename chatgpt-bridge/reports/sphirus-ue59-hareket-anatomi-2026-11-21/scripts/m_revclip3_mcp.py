# m_revclip3_mcp.py (MCP, in-memory edit of AC_Sph_Motion; second refinement) - 2026-11-21 round 4.
#  1 The speed cap (TurnCap -> CalculateMaxSpeed -> MaxWalkSpeed) never acted below 150 cm/s: the movement component uses
#    max(MaxWalkSpeed, MinAnalogWalkSpeed 150) as its limit. MinAnalogWalkSpeed now follows min(RcAnalogMin 150, TurnCap), so the
#    exit of a reversal really follows the re-push of the clip (walk S->W: the capsule ran 40-55 cm/s ahead of the start clip,
#    planted foot 20 cm).
#  2 RcVin = max(speed, speed of the previous frame): the first reversal frame is already braked by the movement component.
import json, sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; BP = AP + '.AC_Sph_Motion'; out = {}; NL = chr(10)
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for n in ('RcPrevV', 'RcAnalogMin'):
    if '"%s"' % n in have: continue
    T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': 'float'})
    T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
assert '`self.RcVin`' in dsl and '`self.RcPrevV`' not in dsl, 'state unexpected'
def line(prefix):
    L = [l for l in dsl.split(NL) if l.strip().startswith(prefix)]; assert len(L) == 1, (prefix, len(L)); return L[0]
M = '`KismetMathLibrary.%s`'
SPD = '(%s (`Actor.GetVelocity` _ascharacter))' % (M % 'VSizeXY')
vin = line('(set `self.RcVin`'); pc = line('(set `self.RcPrevC`'); ind = pc[:len(pc) - len(pc.lstrip())]
p0 = '(set `self.RcVin` (%s %s ' % (M % 'SelectFloat', SPD); assert vin.strip().startswith(p0), 'RcVin line form'
vin_new = vin.replace(p0, '(set `self.RcVin` (%s (%s %s (`self.RcPrevV`)) ' % (M % 'SelectFloat', M % 'FMax', SPD), 1)
add = [pc, ind + '(set `self.RcPrevV` %s)' % SPD,
       ind + '(set `CharacterMovementComponent.MinAnalogWalkSpeed` (%s (`self.RcAnalogMin`) (`self.TurnCap`)) (`Character.CharacterMovement` _ascharacter))' % (M % 'FMin')]
edits = [{'oldString': vin, 'newString': vin_new}, {'oldString': pc, 'newString': NL.join(add)}]
if '--dry' in sys.argv: print(vin_new); print(NL.join(add)); sys.exit(0)
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': edits})
out['edit'] = str(r2)[:2200] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200]
print('REVCLIP3', json.dumps(out)[:3000])
