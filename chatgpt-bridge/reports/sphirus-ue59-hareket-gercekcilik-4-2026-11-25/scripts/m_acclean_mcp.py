# m_acclean_mcp.py (MCP, in-memory; AC_Sph_Motion tick; re-appliable) - movement pass 4.
# ACCELERATION LEAN. EffLean (read by ABP_Sph_Body_GASP) followed only effort (sustained speed > 250) and slope with a 0.5 s lag, so
# the trunk did not prepare / commit when the body propels itself from rest or a lower gait, and did not lean back when it brakes.
# New fast term AccLean from the measured longitudinal acceleration AccL (already computed above): forward up to AL_Deg at AL_Ref
# cm/s^2 while speeding up, back up to AL_DegB while slowing down (ground only), smoothed with AL_Rate. It is ADDED after the slow
# interpolation (EffLean = slow part + AccLean), so the existing effort / slope behaviour is unchanged. AL_Deg 0 = off.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10); K = '`KismetMathLibrary.%s`'; V = lambda n: '(`self.%s`)' % n
PA = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; BP = PA + '.AC_Sph_Motion'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}})); ch = False
for nme in ('AccLean', 'AccLeanPrev', 'AL_Deg', 'AL_DegB', 'AL_Ref', 'AL_RefB', 'AL_Rate'):
    if '"%s"' % nme not in have:
        T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': nme, 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': nme, 'bInstanceEditable': True}); ch = True
if ch: T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '`self.AccLeanPrev`' in dsl and '(set `self.AccLean`' in dsl: print('ACCLEAN already'); sys.exit(0)
L = dsl.split(NL); i = [k for k, x in enumerate(L) if x.startswith('  (set `self.EffLean` (`KismetMathLibrary.FInterpTo` (`self.EffLean`) ')]; assert len(i) == 1; i = i[0]
old = L[i]; assert old.endswith(' DeltaSeconds 2.0))'), old[-60:]
slow = old[len('  (set `self.EffLean` '):-1].replace('(`KismetMathLibrary.FInterpTo` (`self.EffLean`) ', '(`KismetMathLibrary.FInterpTo` (- (`self.EffLean`) (`self.AccLeanPrev`)) ', 1)
GND = '(`NavMovementComponent.IsMovingOnGround` (`Pawn.GetMovementComponent` _ascharacter))'
tgt = '(%s (+ (* (%s (/ %s %s) 0.0 1.0) %s) (* (%s (/ %s %s) -1.0 0.0) %s)) 0.0 (and _bodyon %s))' % (
    K % 'SelectFloat', K % 'FClamp', V('AccL'), V('AL_Ref'), V('AL_Deg'), K % 'FClamp', V('AccL'), V('AL_RefB'), V('AL_DegB'), GND)
new = NL.join(['  (set `self.AccLean` (%s %s %s DeltaSeconds %s))' % (K % 'FInterpTo', V('AccLean'), tgt, V('AL_Rate')),
               '  (set `self.EffLean` (+ %s %s))' % (slow, V('AccLean')),
               '  (set `self.AccLeanPrev` %s)' % V('AccLean')])
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': old, 'newString': new}]})
print('ACCLEAN', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:3000], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:300])
