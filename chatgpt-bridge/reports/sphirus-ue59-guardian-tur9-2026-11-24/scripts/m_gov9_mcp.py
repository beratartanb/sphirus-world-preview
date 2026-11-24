# m_gov9_mcp.py (MCP, in-memory; AC_Sph_Motion; re-appliable) - round 9. Needs c_selt9.py (ABP_Sph_GASP.SphSelTime).
# Quick A/D slide root cause, part 2: the reversal governor bound the capsule to the BLENDED 'movedata_speed' curve. For ~0.25 s after a
# turn clip is entered that curve still carries the previous clip (run, ~375 cm/s) while the entered clip is already braking, so the
# capsule overran the clip's final plant by ~30 cm and the planted foot slid 33-40 cm at the reversal.
# Now: ClipSp = speed curve of the SELECTED clip evaluated at its own time one frame ahead (AnimationWarpingLibrary), fallback = blended
# curve. RcK latch / RcA tracking / "clip speed rising" test use ClipSp. RcK upper clamp 1.8 -> RcKMax.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; BP = AP + '.AC_Sph_Motion'; NL = chr(10); out = {}
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for n in ('ClipSp', 'ClipSpPrev', 'RcKMax'):
    if '"%s"' % n not in have:
        T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True})
T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']; L = dsl.split(NL)
if 'self.ClipSp`' in dsl: print('GOV9 already'); sys.exit(0)
C = '(`AnimInstance.GetCurveValue` (`SkeletalMeshComponent.GetAnimInstance` (`Character.Mesh` _ascharacter)) "movedata_speed")'
ABP = '/Game/Sphirus/Player/GASP/ABP_Sph_GASP'
edits = []
l0 = [x for x in L if x.strip().startswith('(bind _ascharacter ')]; assert len(l0) == 1; l0 = l0[0]; ind = l0[:len(l0) - len(l0.lstrip())]
add = [l0,
 ind + '(bind _r9abp (cast `%s` (`SkeletalMeshComponent.GetAnimInstance` (`Character.Mesh` _ascharacter))))' % ABP,
 ind + '(bind (_r9v _r9ok) (`AnimationWarpingLibrary.GetCurveValueFromAnimation` (cast `AnimSequenceBase` (`%s.CurrentSelectedAnim` _r9abp)) "movedata_speed" (+ (`%s.SphSelTime` _r9abp) DeltaSeconds)))' % (ABP, ABP),
 ind + '(set `self.ClipSpPrev` (`self.ClipSp`))',
 ind + '(set `self.ClipSp` (`KismetMathLibrary.SelectFloat` _r9v %s _r9ok))' % C]
edits.append({'oldString': l0, 'newString': NL.join(add)})
lk = [x for x in L if x.strip().startswith('(set `self.RcK` (`KismetMathLibrary.SelectFloat` (`KismetMathLibrary.FClamp`')]; assert len(lk) == 1; lk = lk[0]
assert lk.count(C) == 1 and lk.count('1.8') == 2
edits.append({'oldString': lk, 'newString': lk.replace(C, '(`self.ClipSp`)').replace('1.8', '(`self.RcKMax`)')})
la = [x for x in L if x.strip().startswith('(set `self.RcA` ')]; assert len(la) == 1; la = la[0]
a1 = '(`KismetMathLibrary.FMax` (- (* 2.0 %s) (`self.RcPrevC`)))' % C; a2 = '(> %s (+ (`self.RcPrevC`) 2.0))' % C
assert la.count(a1) == 1 and la.count(a2) == 1, (la.count(a1), la.count(a2))
edits.append({'oldString': la, 'newString': la.replace(a1, '(`self.ClipSp`)').replace(a2, '(> (`self.ClipSp`) (+ (`self.ClipSpPrev`) 2.0))')})
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': edits})
out['edit'] = 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1800]
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:160]
print('GOV9', json.dumps(out))
