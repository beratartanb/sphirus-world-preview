# m_slidestep2_mcp.py (MCP, in-memory; BP_HybridA_Player GR_Foot; re-appliable) - movement realism pass 2.
# RELOCATION STEP. Two measured slide classes are not a moving planted foot in the clip but a foot that has to change place while the
# clip already calls it planted: (a) walk start with a 135 deg turn enters M_Neutral_Walk_Reface_Start_F_*_180 at 0.20 s, after the clip's
# first step; the real foot is still at its idle place and the blend drags it ~50 cm along the ground; (b) a new command in the middle of
# a turn drops the turn clip for a start clip whose stance foot is under the body while the real foot stands ~50 cm ahead.
# A foot can only change place by stepping. When the driver's contact curve says planted (< 10) and the foot bone still travels faster
# than SL_V0 over the ground, the visible foot is raised by (speed - SL_V0) x SL_K, at most SL_Max cm, through the existing foot IK
# (ABP_Sph_Body_GASP FootTR/TL + FootAR/AL). A truly planted foot does not move, so steady gait is untouched. SL_On 0 switches it off.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = AP + '.BP_HybridA_Player'; NL = chr(10); K = '`KismetMathLibrary.%s`'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for n in ('SL_On', 'SL_K', 'SL_V0', 'SL_Max', 'SL_In', 'SL_Out', 'SL_VR', 'SL_VL', 'SL_LR', 'SL_LL'):
    if '"%s"' % n not in have:
        T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True})
T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '`self.SL_LR`' in dsl: print('SLIDESTEP2 already'); sys.exit(0)
V = lambda n: '(`self.%s`)' % n
L_ = dsl.split(NL); i0 = [i for i, x in enumerate(L_) if x.startswith('(event `GR_Foot`')][0]; ev = L_[i0:]; ev = ev[:[i for i, x in enumerate(ev) if x.strip() == ''][0]] if '' in [x.strip() for x in ev] else ev
def one(pfx):
    m = [x for x in ev if x.strip().startswith(pfx)]; assert len(m) == 1, (pfx, len(m)); return m[0]
edits = []
for f, sock, rv_, cur in (('R', '_returnvalue_3', None, 'contact_r'), ('L', '_returnvalue_5', None, 'contact_l')):
    lp = one('(set `self.FT_P%s` ' % f); assert sock in lp
    edits.append({'oldString': lp, 'newString': '  (set `self.SL_V%s` (/ (%s (- %s %s)) _returnvalue))' % (f, K % 'VSizeXY', sock, V('FT_P' + f)) + NL + lp})
    ll = one('(set `self.FT_L%s` ' % f)
    tgt = '(%s (%s (* (- %s %s) %s) 0.0 %s) 0.0 (and (and _returnvalue_7 (> %s 0.5)) (< (`AnimInstance.GetCurveValue` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)) "%s") 10.0)))' % (K % 'SelectFloat', K % 'FClamp', V('SL_V' + f), V('SL_V0'), V('SL_K'), V('SL_Max'), V('SL_On'), cur)
    edits.append({'oldString': ll, 'newString': ll + NL + '  (set `self.SL_L%s` (%s %s %s _returnvalue (%s %s %s (> %s %s))))' % (f, K % 'FInterpTo', V('SL_L' + f), tgt, K % 'SelectFloat', V('SL_In'), V('SL_Out'), tgt, V('SL_L' + f))})
    lt = one('(set `/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP.FootT%s` ' % f); a = '0.0 0.0 %s)' % V('FT_L' + f); assert lt.count(a) == 1
    edits.append({'oldString': lt, 'newString': lt.replace(a, '0.0 0.0 (+ %s %s))' % (V('FT_L' + f), V('SL_L' + f)))})
    la = one('(set `/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP.FootA%s` ' % f); a = V('FT_A' + f); assert la.count(a) == 1
    edits.append({'oldString': la, 'newString': la.replace(a, '(%s %s (%s %s 0.0 1.0))' % (K % 'FMax', V('FT_A' + f), K % 'FClamp', V('SL_L' + f)))})
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': edits})
print('SLIDESTEP2', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:2500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:160])
