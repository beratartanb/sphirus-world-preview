# m_airturn_mcp.py (MCP, in-memory; BP_HybridA_Player GR_Bob; re-appliable) - movement pass 4.
# SPRINT / RUN TURN AIR HOLD. Sprint_Turn_180_R_Lfoot has a 0.30-0.32 s flight in which the pelvis turns up to 60 deg with no foot
# on the ground (an_air, pass 3 / B4 final). While both driver contact curves are in flight (< ATH_Air) inside a TURN clip above
# ATH_VMin, the hip layer's yaw (SphHipRot yaw, same owner as HIP_Yaw) counter-rotates ATH_K of the visible hip line's world yaw change,
# so the pelvis keeps most of its facing in the air; the held yaw is released only while a foot is in support (ATH_Rel deg/s), i.e.
# the remaining turn happens over the planted foot. Normal running flight (not a turn clip) is untouched; |ATH_Y| <= ATH_Max.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10); K = '`KismetMathLibrary.%s`'; V = lambda n: '(`self.%s`)' % n
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}})); ch = False
for nme in ('ATH_On', 'ATH_Y', 'ATH_Y2', 'ATH_Yo', 'ATH_Prev', 'ATH_K', 'ATH_Rel', 'ATH_Max', 'ATH_Air', 'ATH_VMin'):
    if '"%s"' % nme not in have:
        T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': nme, 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': nme, 'bInstanceEditable': True}); ch = True
if ch: T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '(set `self.ATH_Prev`' in dsl: print('AIRTURN already'); sys.exit(0)
L = dsl.split(NL)
i = [k for k, x in enumerate(L) if x.startswith('  (set `/Game/Sphirus/Player/GASP/ABP_Sph_GASP.SphHipRot` ')]; assert len(i) == 1, i; i = i[0]
old = L[i]; assert old.count('(+ (`self.HIP_Yaw`) ') == 1
CUR = lambda c: '(`AnimInstance.GetCurveValue` _returnvalue_2 "%s")' % c
HL = '(- (`SceneComponent.GetSocketLocation` (`self.Mesh`) "thigh_r") (`SceneComponent.GetSocketLocation` (`self.Mesh`) "thigh_l"))'
YAW = '(%s (.y %s) (.x %s))' % (K % 'DegAtan2', HL, HL)
D = '(%s (- %s %s))' % (K % 'NormalizeAxis', YAW, V('ATH_Prev'))
CLIP = '(`KismetSystemLibrary.GetObjectName` (`/Game/Sphirus/Player/GASP/ABP_Sph_GASP.CurrentSelectedAnim` _asabp_sph_gasp))'
AIR = '(and (and (and (and (< %s %s) (< %s %s)) (`KismetStringLibrary.Contains` %s "Turn")) (> _returnvalue_3 %s)) (> %s 0.5))' % (CUR('contact_l'), V('ATH_Air'), CUR('contact_r'), V('ATH_Air'), CLIP, V('ATH_VMin'), V('ATH_On'))
DA = '(- %s (- %s %s))' % (D, V('ATH_Y'), V('ATH_Y2'))   # animation's own yaw change: remove the hold applied between the previous two poses
new = NL.join(['  (set `self.ATH_Yo` %s)' % V('ATH_Y'),
               '  (set `self.ATH_Y` (%s (%s (- %s (* %s %s)) (%s %s 0.0 _returnvalue %s) %s) (- %s) %s))' % (
                   K % 'FClamp', K % 'SelectFloat', V('ATH_Y'), DA, V('ATH_K'), K % 'FInterpTo_Constant', V('ATH_Y'), V('ATH_Rel'), AIR, V('ATH_Max'), V('ATH_Max')),
               '  (set `self.ATH_Y2` %s)' % V('ATH_Yo'),
               '  (set `self.ATH_Prev` %s)' % YAW,
               old.replace('(+ (`self.HIP_Yaw`) ', '(+ (+ (`self.HIP_Yaw`) (`self.ATH_Y`)) ')])
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': old, 'newString': new}]})
print('AIRTURN', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:3000], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:300])
