# m_turn3_mcp.py (MCP, in-memory; BP_HybridA_Player GR_Bob; after pass-2 hip steps; re-appliable) - movement realism pass 3.
# "SNAKE" TURNS. Measured: in a 90 deg cut the hip line rolls 24 deg (run) / 33 deg (sprint) against 9-11 deg in the steady gait, and the
# pelvis drops 15-18 cm. Driver and visible body agree and switching the pass-1/2 hip layer, the posture layer or the bob layer off does
# not change it: it is the content of the vendor turn clips (M_Relaxed_Run_Turn_*_090, M_Relaxed_Sprint_Turn_090_*), an athletic banked
# cut. The clips stay untouched; the pelvis layer now soft-limits the CLIP's hip tilt: above TLM_Free degrees the excess is taken back by
# TLM_K (at most TLM_Max, rate limited), half of it handed to the spine (TLM_KS) so the trunk keeps most of its lean into the turn
# without a sharp lumbar bend. The cyclic correction and its mean tracker read the clip tilt without this term (no interaction).
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10); K = '`KismetMathLibrary.%s`'; V = lambda n: '(`self.%s`)' % n
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}})); ch = False
for n in ('TLM_On', 'TLM_Free', 'TLM_K', 'TLM_Max', 'TLM_Rate', 'TLM_KS', 'TLM', 'TLM_C'):
    if '"%s"' % n not in have:
        T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True}); ch = True
if ch: T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '`self.TLM_C`' in dsl: print('TURN3 already'); sys.exit(0)
L = dsl.split(NL); i0 = [i for i, x in enumerate(L) if x.startswith('(event `GR_Bob`')][0]; i1 = [i for i, x in enumerate(L) if i > i0 and x.startswith('(event ')][0]; ev = L[i0:i1]
def one(p):
    m = [x for x in ev if x.startswith(p)]; assert len(m) == 1, (p, len(m)); return m[0]
lso = one('  (set `self.HIP_SO` '); lmo = one('  (set `self.HIP_MO` '); lob = one('  (set `self.HIP_Obl` '); lhr = one('  (set `/Game/Sphirus/Player/GASP/ABP_Sph_GASP.SphHipRot` '); lsr = one('  (set `/Game/Sphirus/Player/GASP/ABP_Sph_GASP.SphSpineRot` ')
# raw tilt expression: balanced parens from the first DegAtan in the HIP_SO line
a = lso.find('(' + K % 'DegAtan'); assert a > 0; d = 0; b = a
while True:
    d += {'(': 1, ')': -1}.get(lso[b], 0); b += 1
    if d == 0: break
RAW = lso[a:b]; assert 'thigh_r' in RAW and 'thigh_l' in RAW
old = '%s) %s' % (V('HIP_Obl'), V('HIP_MO')); new = '(+ %s %s)) %s' % (V('HIP_Obl'), V('TLM'), V('HIP_MO')); edits = []
pre = ['  (set `self.TLM_C` (- (- %s %s) %s))' % (RAW, V('HIP_Obl'), V('TLM')),
       '  (set `self.TLM` (%s %s (* (* (* -1.0 (%s %s)) (%s (* (- (%s %s) %s) %s) 0.0 %s)) %s) _returnvalue %s))' % (K % 'FInterpTo_Constant', V('TLM'), K % 'SignOfFloat', V('TLM_C'), K % 'FClamp', K % 'Abs', V('TLM_C'), V('TLM_Free'), V('TLM_K'), V('TLM_Max'), V('TLM_On'), V('TLM_Rate'))]
for i, l in enumerate((lso, lmo, lob)):
    assert l.count(old) >= 1, (i, l.count(old)); n = l.replace(old, new)
    edits.append({'oldString': l, 'newString': (NL.join(pre) + NL + n) if i == 0 else n})
a1 = '(+ %s ' % V('HIP_Obl'); assert lhr.count(a1) == 1; edits.append({'oldString': lhr, 'newString': lhr.replace(a1, '(+ (+ %s %s) ' % (V('HIP_Obl'), V('TLM')))})
a2 = '(* (- %s) %s)' % (V('HIP_KSp'), V('HIP_Obl')); assert lsr.count(a2) == 1; edits.append({'oldString': lsr, 'newString': lsr.replace(a2, '(* (- %s) (+ %s (* %s %s)))' % (V('HIP_KSp'), V('HIP_Obl'), V('TLM'), V('TLM_KS')))})
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': edits})
print('TURN3', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:2500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:160])
