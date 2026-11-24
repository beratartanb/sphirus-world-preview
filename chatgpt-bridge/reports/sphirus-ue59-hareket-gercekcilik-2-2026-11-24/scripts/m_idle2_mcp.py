# m_idle2_mcp.py (MCP, in-memory; BP_HybridA_Player GR_Bob; after m_hip6; re-appliable) - movement realism pass 2.
# IDLE STANCE. The idle loop stands symmetric on both legs (mannequin). After ID_Delay s of standing (on ground, no montage, not crouched)
# the weight settles onto one leg through the EXISTING pelvis / spine nodes of the driver (no new controller): pelvis shifts ID_X cm to
# the stance side and sinks ID_Z, the hip line drops ID_O deg on the free side and turns ID_Y deg, the trunk takes back ID_KS of the tilt
# and all of the turn (shoulders stay square, slightly counter-tilted). FootPlacement runs after these nodes, so both feet stay planted.
# Eased in over ~1.7 s, released in ~0.2 s when movement starts. Every ID_Period s of standing the stance side changes slowly.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = AP + '.BP_HybridA_Player'; NL = chr(10); K = '`KismetMathLibrary.%s`'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for n in ('ID_On', 'ID_X', 'ID_Z', 'ID_O', 'ID_Y', 'ID_KS', 'ID_Delay', 'ID_Period', 'ID_A', 'ID_T', 'ID_T2', 'ID_Flip', 'ID_SideS'):
    if '"%s"' % n not in have:
        T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True})
T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '`self.ID_A`' in dsl: print('IDLE2 already'); sys.exit(0)
V = lambda n: '(`self.%s`)' % n; SF = K % 'SelectFloat'; L_ = dsl.split(NL)
def one(pfx):
    m = [x for x in L_ if x.strip().startswith(pfx)]; assert len(m) == 1, (pfx, len(m)); return m[0]
lb = one('(set `/Game/Sphirus/Player/GASP/ABP_Sph_GASP.SphBob` '); ind = lb[:len(lb) - len(lb.lstrip())]
idle = '(and (and _returnvalue_5 (< _returnvalue_3 5.0)) (> %s 0.5))' % V('ID_On'); on = '(> %s %s)' % (V('ID_T'), V('ID_Delay'))
E_ = '(* (* (* %s %s) (- 3.0 (* 2.0 %s))) %s)' % (V('ID_A'), V('ID_A'), V('ID_A'), V('ID_SideS'))   # eased weight x side
pre = ['(set `self.ID_T` (%s (+ %s _returnvalue) 0.0 %s))' % (SF, V('ID_T'), idle),
       '(set `self.ID_Flip` (%s (- 1.0 %s) %s (> %s %s)))' % (SF, V('ID_Flip'), V('ID_Flip'), V('ID_T2'), V('ID_Period')),
       '(set `self.ID_T2` (%s 0.0 (+ %s (%s _returnvalue 0.0 %s)) (> %s %s)))' % (SF, V('ID_T2'), SF, idle, V('ID_T2'), V('ID_Period')),
       '(set `self.ID_SideS` (%s %s (%s -1.0 1.0 (> %s 0.5)) _returnvalue 0.7))' % (K % 'FInterpTo', V('ID_SideS'), SF, V('ID_Flip')),
       '(set `self.ID_A` (%s %s (%s 1.0 0.0 %s) _returnvalue (%s 0.6 5.0 %s)))' % (K % 'FInterpTo_Constant', V('ID_A'), SF, on, SF, on)]
edits = []
a = V('BOB_Prev') + ' _asabp_sph_gasp)'; assert lb.count(a) == 1
edits.append({'oldString': lb, 'newString': NL.join(ind + x for x in pre) + NL + lb.replace(a, '(+ %s (%s (* %s %s) 0.0 (* (- %s) (%s %s)))) _asabp_sph_gasp)' % (V('BOB_Prev'), K % 'MakeVector', E_, V('ID_X'), V('ID_Z'), K % 'Abs', E_))})
lh = one('(set `/Game/Sphirus/Player/GASP/ABP_Sph_GASP.SphHipRot` '); a = '0.0 %s %s) _asabp_sph_gasp)' % (V('HIP_Obl'), V('HIP_Yaw')); assert lh.count(a) == 1
edits.append({'oldString': lh, 'newString': lh.replace(a, '0.0 (+ %s (* %s %s)) (+ %s (* %s %s))) _asabp_sph_gasp)' % (V('HIP_Obl'), E_, V('ID_O'), V('HIP_Yaw'), E_, V('ID_Y')))})
ls = one('(set `/Game/Sphirus/Player/GASP/ABP_Sph_GASP.SphSpineRot` ')
a1 = '(* (- %s) %s) (+' % (V('HIP_KSp'), V('HIP_Obl')); assert ls.count(a1) == 1, ls
a2 = V('SH_Yaw') + ')) _asabp_sph_gasp)'; assert ls.count(a2) == 1, ls
n = ls.replace(a1, '(- (* (- %s) %s) (* (* %s %s) %s)) (+' % (V('HIP_KSp'), V('HIP_Obl'), E_, V('ID_O'), V('ID_KS'))).replace(a2, '(- %s (* %s %s)))) _asabp_sph_gasp)' % (V('SH_Yaw'), E_, V('ID_Y')))
edits.append({'oldString': ls, 'newString': n})
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': edits})
print('IDLE2', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:2500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:160])
