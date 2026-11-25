# m_aware_mcp.py (MCP, in-memory; BP_HybridA_Player GR_Posture + GR_Bob; re-appliable) - movement pass 4.
# NEAR-SURFACE AWARENESS (visual body adaptation only; never touches input, velocity or steering).
# Probes (GR_Posture, every frame while moving on the ground): per side one sphere trace at chest height straight out to the side and
# one forward-diagonal (45 deg) trace, so an approaching door edge / furniture corner is seen before it is beside the body.
# Side clearance c = min(side hit distance, 0.7 x diagonal hit distance). Hysteresis: a side engages below AW_In, releases above AW_Out.
# Strength s = clamp((AW_Out - c) / (AW_Out - AW_Min)) x speed factor (0 below 30 cm/s, 0.5 at 60, 1 at 400), smoothed (AW_RIn / AW_ROut).
# Outputs, all bounded and in the existing owners:
#  - near arm tucks: its abduction target (PS_DAL/PS_DAR feedback) is reduced by s x AW_Arm deg (the thigh-clearance term CA_* still
#    keeps the hand off the thigh);
#  - torso turns so the near shoulder goes back: SphSpineRot yaw += (sL - sR) x AW_Yaw;
#  - head / gaze: a short glance toward the surface when a side engages (impulse decays in ~0.7 s): VI_Head yaw axis x AW_Head.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10); K = '`KismetMathLibrary.%s`'; V = lambda n: '(`self.%s`)' % n
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}})); ch = False
FL = ('AW_On', 'AW_In', 'AW_Out', 'AW_Min', 'AW_RIn', 'AW_ROut', 'AW_Arm', 'AW_Yaw', 'AW_Head', 'AW_CL', 'AW_CR', 'AW_SL', 'AW_SR', 'AW_GL', 'AW_GR', 'AW_AL', 'AW_AR', 'AW_TY', 'AW_HY')
for nme, ty in [(n, 'float') for n in FL] + [('AW_EL', 'bool'), ('AW_ER', 'bool'), ('AW_ELp', 'bool'), ('AW_ERp', 'bool')]:
    if '"%s"' % nme not in have:
        T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': nme, 'typeName': ty}); ch = True
        if ty == 'float': T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': nme, 'bInstanceEditable': True})
if ch: T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '(set `self.AW_ELp`' in dsl: print('AWARE already'); sys.exit(0)
L = dsl.split(NL)
# 1. probes + state at the start of GR_Posture (after its params / first binds: insert right after the event line)
ip = [k for k, x in enumerate(L) if x.startswith('(event `GR_Posture`')]; assert len(ip) == 1; ip = ip[0]
LOC = '(`self.K2_GetActorLocation`)'; SPD = '(%s (`self.GetVelocity`))' % (K % 'VSizeXY'); DT = '(%s (`self.GR_PDt`) 0.004 0.05)' % (K % 'FClamp')
MV = lambda a, b, c: '(%s %s %s %s)' % (K % 'MakeVector', a, b, c)
CH = '(+ %s %s)' % (LOC, MV('0.0', '0.0', '42.0'))
RG = '(`self.GetActorRightVector`)'; FW = '(`self.GetActorForwardVector`)'
def sc(v, d): return '(* %s %s)' % (v, MV(d, d, d))
probes = []
for side, sg in (('L', '-1.0'), ('R', '1.0')):
    dirs = sc(RG, sg); diag = '(%s (+ %s %s))' % (K % 'Normal', FW, dirs)
    probes += ['  (bind (_aws%s _awsb%s) (`KismetSystemLibrary.SphereTraceSingle` (+ %s %s) (+ %s %s) 10.0))' % (side, side, CH, sc(dirs, '20.0'), CH, sc(dirs, '75.0')),
               '  (bind (_awd%s _awdb%s) (`KismetSystemLibrary.SphereTraceSingle` (+ %s %s) (+ %s %s) 10.0))' % (side, side, CH, sc(diag, '20.0'), CH, sc(diag, '95.0')),
               '  (set `self.AW_C%s` (%s (%s (`.Distance` (`GameplayStatics.BreakHitResult` _aws%s)) 99.0 _awsb%s) (%s (* (`.Distance` (`GameplayStatics.BreakHitResult` _awd%s)) 0.7) 99.0 _awdb%s)))' % (
                   side, K % 'FMin', K % 'SelectFloat', side, side, K % 'SelectFloat', side, side),
               '  (set `self.AW_E%s` (and (and (and (> %s 0.5) (> %s 30.0)) (`NavMovementComponent.IsMovingOnGround` (`self.CharacterMovement`))) (or (< %s %s) (and %s (< %s %s)))))' % (
                   side, V('AW_On'), SPD, V('AW_C' + side), V('AW_In'), V('AW_E' + side), V('AW_C' + side), V('AW_Out')),
               '  (set `self.AW_S%s` (%s %s (%s (* (%s (/ (- %s %s) (- %s %s)) 0.0 1.0) (%s %s 30.0 400.0 0.4 1.0)) 0.0 %s) %s (%s %s %s %s)))' % (
                   side, K % 'FInterpTo', V('AW_S' + side), K % 'SelectFloat', K % 'FClamp', V('AW_Out'), V('AW_C' + side), V('AW_Out'), V('AW_Min'), K % 'MapRangeClamped', SPD,
                   V('AW_E' + side), DT, K % 'SelectFloat', V('AW_RIn'), V('AW_ROut'), V('AW_E' + side)),
               '  (set `self.AW_G%s` (%s 1.0 (%s %s 0.0 %s 1.4) (and %s (not %s))))' % (side, K % 'SelectFloat', K % 'FInterpTo', V('AW_G' + side), DT, V('AW_E' + side), V('AW_E%sp' % side)),
               '  (set `self.AW_E%sp` %s)' % (side, V('AW_E' + side)),
               '  (set `self.AW_A%s` (* %s %s))' % (side, V('AW_S' + side), V('AW_Arm'))]
probes += ['  (set `self.AW_TY` (* (- %s %s) %s))' % (V('AW_SL'), V('AW_SR'), V('AW_Yaw')),
           '  (set `self.AW_HY` (* (- (* %s %s) (* %s %s)) %s))' % (V('AW_GL'), V('AW_SL'), V('AW_GR'), V('AW_SR'), V('AW_Head'))]
# insert after the event header's params line
assert L[ip + 1].strip().startswith('(params') or True
ins = ip + 1 if L[ip + 1].strip().startswith('(params') else ip
edits = [{'oldString': NL.join(L[ip:ins + 2]), 'newString': NL.join(L[ip:ins + 1] + probes + [L[ins + 1]])}]
# 2. arm tuck: reduce the abduction target of each arm
for side, ca in (('L', 'CA_L'), ('R', 'CA_R')):
    o = '(+ (+ _returnvalue_43 (`self.%s`))' % ca; lines_ = [x for x in L if o in x]; assert len(lines_) == 1, (side, len(lines_))
    edits.append({'oldString': lines_[0], 'newString': lines_[0].replace(o, '(+ (+ (- _returnvalue_43 (`self.AW_A%s`)) (`self.%s`))' % (side, ca))})
# 3. torso yaw in SphSpineRot (GR_Bob) and head glance in VI_Head
i = [k for k, x in enumerate(L) if x.startswith('  (set `/Game/Sphirus/Player/GASP/ABP_Sph_GASP.SphSpineRot` (`KismetMathLibrary.MakeRotator` ')]; assert len(i) == 1
old = L[i[0]]; cut = old.rindex(' _asabp_sph_gasp)'); tailp = old[cut:]
body = old[len('  (set `/Game/Sphirus/Player/GASP/ABP_Sph_GASP.SphSpineRot` '):cut]
edits.append({'oldString': old, 'newString': '  (set `/Game/Sphirus/Player/GASP/ABP_Sph_GASP.SphSpineRot` (`KismetMathLibrary.ComposeRotators` %s (`KismetMathLibrary.MakeRotator` 0.0 0.0 %s))%s' % (body, V('AW_TY'), tailp)})
j = [k for k, x in enumerate(L) if x.lstrip().startswith('(set `/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP.VI_Head` ')]; assert len(j) == 1
oh = L[j[0]]; pre_ = oh[:oh.index('(set ')]; assert oh.endswith(')')
# value expression is between the property and the trailing target argument; wrap the whole set by adding the glance vector
hb = oh[len(pre_ + '(set `/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP.VI_Head` '):]; cut = hb.rindex(' _asabp_sph_body_gasp)')
edits.append({'oldString': oh, 'newString': pre_ + '(set `/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP.VI_Head` (+ %s %s)%s' % (MV('(* %s 0.98)' % V('AW_HY'), '(* %s -0.199)' % V('AW_HY'), '0.0'), hb[:cut], hb[cut:])})
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': edits})
print('AWARE', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:3000], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:300])
