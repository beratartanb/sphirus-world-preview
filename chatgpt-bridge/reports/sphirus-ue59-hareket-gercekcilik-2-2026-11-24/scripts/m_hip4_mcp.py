# m_hip4_mcp.py (MCP, in-memory; BP_HybridA_Player GR_Bob; after m_hip1/2/3; re-appliable) - movement realism pass 2.
# STABILITY of the hip / shoulder line correction through turns (an_hipstab.py): the line angle is atan(dy/dx) in component space, so a
# 180 deg turn of the mesh root (root offset during pivots / reface starts) wraps it, the slow mean lags behind by up to 180 deg and the
# correction jumps between its clamps (hip yaw single-frame jump p99 7.5 -> 33.7 deg in sprint A/D with the layer on).
# 1 deviation = wrapped difference (period 180 deg): NormalizeAxis(2 x (raw - mean)) / 2  -> an angle wrap is no longer a jump;
# 2 gate: when |deviation| exceeds what a gait cycle can produce (HIP_GY / HIP_GO / SH_G) the mean snaps onto the raw value and the
#   channel's steadiness weight (HIP_SY / HIP_SO / SH_S) drops to 0, then returns at 2.5 /s -> no correction while the body is turning.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = AP + '.BP_HybridA_Player'; NL = chr(10); K = '`KismetMathLibrary.%s`'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for n in ('HIP_SY', 'HIP_SO', 'SH_S', 'HIP_GY', 'HIP_GO', 'SH_G'):
    if '"%s"' % n not in have:
        T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True})
T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '`self.HIP_SY`' in dsl: print('HIP4 already'); sys.exit(0)
V = lambda n: '(`self.%s`)' % n
def grp(s, i):
    k = 0
    for j in range(i, len(s)):
        k += (s[j] == '(') - (s[j] == ')')
        if k == 0: return s[i:j + 1]
    raise Exception('unbalanced')
L_ = dsl.split(NL); edits = []
for M, C, S, G in (('HIP_MY', 'HIP_Yaw', 'HIP_SY', 'HIP_GY'), ('HIP_MO', 'HIP_Obl', 'HIP_SO', 'HIP_GO'), ('SH_M', 'SH_Yaw', 'SH_S', 'SH_G')):
    lm = [x for x in L_ if x.strip().startswith('(set `self.%s` ' % M)]; assert len(lm) == 1, M; lm = lm[0]; ind = lm[:len(lm) - len(lm.lstrip())]
    a = lm.index(V(M) + ' ', lm.index('FInterpTo')) + len(V(M)) + 1; RAW = grp(lm, a); assert RAW.startswith('(- (`KismetMathLibrary.DegAtan`') and RAW.endswith(V(C) + ')'), RAW[:80]
    DEV = '(/ (%s (* 2.0 (- %s %s))) 2.0)' % (K % 'NormalizeAxis', RAW, V(M))
    big = '(> (%s %s) %s)' % (K % 'Abs', DEV, V(G))
    ls = ind + '(set `self.%s` (%s 0.0 (%s %s 1.0 _returnvalue 2.5) %s))' % (S, K % 'SelectFloat', K % 'FInterpTo_Constant', V(S), big)
    nm = ind + '(set `self.%s` (%s (+ %s %s) (%s %s (+ %s %s) _returnvalue %s) %s))' % (M, K % 'SelectFloat', V(M), DEV, K % 'FInterpTo', V(M), V(M), DEV, V('HIP_LP'), big)
    edits.append({'oldString': lm, 'newString': ls + NL + nm})
    lc = [x for x in L_ if x.strip().startswith('(set `self.%s` ' % C)]; assert len(lc) == 1, C; lc = lc[0]
    old = '(- %s %s)' % (RAW, V(M)); assert lc.count(old) == 1, (C, lc.count(old))
    edits.append({'oldString': lc, 'newString': lc.replace(old, '(* %s %s)' % (DEV, V(S)))})
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': edits})
print('HIP4', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:2500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:160])
