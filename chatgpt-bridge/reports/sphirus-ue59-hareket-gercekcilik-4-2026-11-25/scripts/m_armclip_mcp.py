# m_armclip_mcp.py (MCP, in-memory; BP_HybridA_Player GR_Posture; re-appliable) - movement pass 4.
# CLIP-SPECIFIC ARM PATH. Real-surface measurement (armsurf5) puts the hand into the shorts/thigh outline in a few clips only:
# backward jog start / loop (CM_af_Loco_Jog_Bwd*, 4-8 cm), backward run stop (M_Relaxed_Run_Stop_B_*, up to 7-11 cm), forward jog
# (CM_af_Loco_Jog_Fwd, 2-4 cm for ~0.3 s). The arm-clearance feedback (CA_*) reacts too late inside a 0.1-0.3 s swing, and its
# pelvis-front term was no robust gain (A/B p4A0 / p4A1). These clips cross the pelvis front on every cycle, so the arm path of THESE
# clips is widened: while one of them is the selected clip, the abduction target of both arms gets PS_AbdBwd (backward family) or
# PS_AbdFwdJog (forward jog) degrees, blended in/out (PS_AbdRate) - the same channel as the existing backward widening PS_AbdBack,
# which it replaces (max of the two). Off in every other clip: no permanent arms-out layer.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10); K = '`KismetMathLibrary.%s`'; V = lambda n: '(`self.%s`)' % n
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}})); ch = False
for nme in ('PS_AbdClipA', 'PS_AbdBwd', 'PS_AbdFwdJog', 'PS_AbdRate'):
    if '"%s"' % nme not in have:
        T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': nme, 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': nme, 'bInstanceEditable': True}); ch = True
if ch: T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '(set `self.PS_AbdClipA`' in dsl: print('ARMCLIP already'); sys.exit(0)
L = dsl.split(NL)
ip = [k for k, x in enumerate(L) if x.startswith('(event `GR_Posture`')]; assert len(ip) == 1; ip = ip[0]
o = '(`KismetMathLibrary.SelectFloat` (`self.PS_AbdBack`) 0.0 (and (`self.GR_Back`) (> _returnvalue_17 60.0)))'
lines_ = [x for x in L if o in x]; assert len(lines_) == 2, len(lines_)
CLIP = '(`KismetSystemLibrary.GetObjectName` (`/Game/Sphirus/Player/GASP/ABP_Sph_GASP.CurrentSelectedAnim` (cast `/Game/Sphirus/Player/GASP/ABP_Sph_GASP` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)))))'
BWD = '(or (`KismetStringLibrary.Contains` %s "Jog_Bwd") (`KismetStringLibrary.Contains` %s "Stop_B_"))' % (CLIP, CLIP)
FWJ = '(`KismetStringLibrary.Contains` %s "Jog_Fwd")' % CLIP
SPD = '(%s (`self.GetVelocity`))' % (K % 'VSizeXY'); DT = '(%s (`self.GR_PDt`) 0.004 0.05)' % (K % 'FClamp')
tgt = '(%s (%s (%s %s 0.0 (and (`self.GR_Back`) (> %s 60.0))) (%s %s 0.0 %s)) (%s %s 0.0 %s))' % (
    K % 'FMax', K % 'FMax', K % 'SelectFloat', V('PS_AbdBack'), SPD, K % 'SelectFloat', V('PS_AbdBwd'), BWD, K % 'SelectFloat', V('PS_AbdFwdJog'), FWJ)
ins = '  (set `self.PS_AbdClipA` (%s %s %s %s %s))' % (K % 'FInterpTo', V('PS_AbdClipA'), tgt, DT, V('PS_AbdRate'))
edits = [{'oldString': NL.join(L[ip:ip + 2]), 'newString': NL.join([L[ip], ins, L[ip + 1]])}]
for x in lines_: edits.append({'oldString': x, 'newString': x.replace(o, V('PS_AbdClipA'))})
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': edits})
print('ARMCLIP', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:3000], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:300])
