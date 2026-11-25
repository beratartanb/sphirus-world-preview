# m_foothold_mcp.py (MCP, in-memory; BP_HybridA_Player GR_Foot; re-appliable) - movement pass 4.
# STOP FOOT HOLD. Every Relaxed stop clip ends with an authored feet-squaring step 0.3-0.7 s after its root speed reaches zero
# (probe_stopclip: walk stop R foot 18 cm at clip 2.0-2.4 s). In game the feet land in a different layout than the clip expects, so
# this fixed step plays 0.6-0.9 s after the capsule is at rest and can even go backwards (-20 cm). Once the capsule has been at rest
# SH_Rest s with both contact curves in support (= after the natural closing step), and the stance is already usable (fore-aft spread
# <= SH_MaxFwd, width SH_MinLat..SH_MaxLat), both visible feet are latched where they stand (visible-body foot IK targets FootTR/TL,
# alpha FootAR/AL - same owner as the foot clearance). Released (alpha back to the animation in SH_Out) by any move input, any capsule
# motion, a turn-in-place / start clip, a montage or air. A wide or crossed stance is NOT held: then the clip's step is a real need.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10); K = '`KismetMathLibrary.%s`'; V = lambda n: '(`self.%s`)' % n
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}})); ch = False
for nme, ty in (('SH_On', 'float'), ('SH_T', 'float'), ('SH_Rest', 'float'), ('SH_MaxFwd', 'float'), ('SH_MinLat', 'float'), ('SH_MaxLat', 'float'), ('SH_In', 'float'), ('SH_Out', 'float'),
                ('SH_AR', 'float'), ('SH_AL', 'float'), ('SH_Lat', 'bool'), ('SH_LatPrev', 'bool'), ('SH_PR', 'vector'), ('SH_PL', 'vector')):
    if '"%s"' % nme not in have:
        T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': nme, 'typeName': ty}); ch = True
        if ty == 'float': T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': nme, 'bInstanceEditable': True})
if ch: T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '(set `self.SH_LatPrev`' in dsl: print('FOOTHOLD already'); sys.exit(0)
anchor = '  (bind _asabp_sph_body_gasp (cast `/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP` (`SkeletalMeshComponent.GetAnimInstance` (`self.Manny`))))' + NL + '  (set `/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP.FootTR`'
assert dsl.count(anchor) == 1, dsl.count(anchor)
CR = '(`AnimInstance.GetCurveValue` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)) "contact_r")'; CL = CR.replace('contact_r', 'contact_l')
SPD = '(%s (`self.GetVelocity`))' % (K % 'VSizeXY')
D = '(- _returnvalue_5 _returnvalue_3)'
FWD = '(%s %s (`self.GetActorForwardVector`))' % (K % 'Dot_VectorVector', D); RGT = '(%s %s (`self.GetActorRightVector`))' % (K % 'Dot_VectorVector', D)
CLIPN = '(`KismetSystemLibrary.GetObjectName` (`/Game/Sphirus/Player/GASP/ABP_Sph_GASP.CurrentSelectedAnim` _shabp))'
REST = '(and (and (and (and (> %s 0.5) (< %s 3.0)) (< (%s %s) 0.1)) (`NavMovementComponent.IsMovingOnGround` (`self.CharacterMovement`))) (not (`AnimInstance.IsAnyMontagePlaying` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)))))' % (V('SH_On'), SPD, K % 'VSize', V('GR_RawIn'))
NOTURN = '(not (or (`KismetStringLibrary.Contains` _shclip "Turn") (`KismetStringLibrary.Contains` _shclip "Start")))'
OKST = '(and (and (< (%s %s) %s) (> (%s %s) %s)) (< (%s %s) %s))' % (K % 'Abs', FWD, V('SH_MaxFwd'), K % 'Abs', RGT, V('SH_MinLat'), K % 'Abs', RGT, V('SH_MaxLat'))
pre = ['  (bind _shabp (cast `/Game/Sphirus/Player/GASP/ABP_Sph_GASP` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`))))',
       '  (bind _shclip %s)' % CLIPN,
       '  (set `self.SH_T` (%s (+ %s _returnvalue) 0.0 %s))' % (K % 'SelectFloat', V('SH_T'), REST),
       '  (set `self.SH_Lat` (and (and %s %s) (or %s (and (and (and (> %s %s) (> %s 50.0)) (> %s 50.0)) %s))))' % (REST, NOTURN, V('SH_Lat'), V('SH_T'), V('SH_Rest'), CR, CL, OKST),
       '  (if (and %s (not %s))' % (V('SH_Lat'), V('SH_LatPrev')),
       '    (set `self.SH_PR` _returnvalue_3)',
       '    (set `self.SH_PL` _returnvalue_5))',
       '  (set `self.SH_LatPrev` %s)' % V('SH_Lat'),
       '  (set `self.SH_AR` (%s %s (%s 1.0 0.0 %s) _returnvalue (%s %s %s %s)))' % (K % 'FInterpTo', V('SH_AR'), K % 'SelectFloat', V('SH_Lat'), K % 'SelectFloat', V('SH_In'), V('SH_Out'), V('SH_Lat'))]
new = NL.join(pre) + NL + anchor
edits = [{'oldString': anchor, 'newString': new}]
# final targets: blend the held positions in
for side, ret in (('R', '_returnvalue_3'), ('L', '_returnvalue_5')):
    sidev = 'SH_P' + side
    ot = '  (set `/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP.FootT%s` (+ %s (`KismetMathLibrary.MakeVector` 0.0 0.0 (+ (`self.FT_L%s`) (`self.SL_L%s`)))) _asabp_sph_body_gasp)' % (side, ret, side, side)
    assert dsl.count(ot) == 1, (side, dsl.count(ot))
    edits.append({'oldString': ot, 'newString': '  (set `/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP.FootT%s` (%s (+ %s (`KismetMathLibrary.MakeVector` 0.0 0.0 (+ (`self.FT_L%s`) (`self.SL_L%s`)))) %s %s) _asabp_sph_body_gasp)' % (side, K % 'VLerp', ret, side, side, V(sidev), V('SH_AR'))})
    oa = '  (set `/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP.FootA%s` (`KismetMathLibrary.FMax` (`self.FT_A%s`) (`KismetMathLibrary.FClamp` (`self.SL_L%s`))) _asabp_sph_body_gasp)' % (side, side, side)
    assert dsl.count(oa) == 1, (side, 'a', dsl.count(oa))
    edits.append({'oldString': oa, 'newString': '  (set `/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP.FootA%s` (`KismetMathLibrary.FMax` (`KismetMathLibrary.FMax` (`self.FT_A%s`) (`KismetMathLibrary.FClamp` (`self.SL_L%s`))) %s) _asabp_sph_body_gasp)' % (side, side, side, V('SH_AR'))})
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': edits})
print('FOOTHOLD', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:3000], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:300])
