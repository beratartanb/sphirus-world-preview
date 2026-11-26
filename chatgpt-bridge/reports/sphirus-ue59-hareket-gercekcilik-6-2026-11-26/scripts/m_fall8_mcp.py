# m_fall8_mcp.py (MCP, in-memory): falls driven by real ground contact + safe get-up (pass 6).
# 1. Ground phase: when the pelvis or the chest (spine_05) has the floor within 30 cm below it (line traces; the ragdoll itself is ignored)
#    after at least 0.15 s - instead of the fixed FL_GndT 0.8 s timer, which stays only as a fallback (FL_GndMax).
# 2. Roll-over: each failed attempt alternates the roll direction and grows 25 % stronger (supine bodies wedged on an arm or a slope).
# 3. Get-up clearance: before standing up, a standing capsule (r 30, hh 84) must fit at the pelvis; else the four 45 cm neighbours (along
#    and across the body) are tried and the first free one is used (repositioning); if none is free she stays down (FL_Blocked counts the
#    waits) and tries again after the next settle - no get-up into a wall / under a table.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10); BQ = chr(96)
def K(f): return BQ + 'KismetMathLibrary.' + f + BQ
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for n, ty in (('FL_Gnd', 'float'), ('FL_GndMax', 'float'), ('FL_Free', 'float'), ('FL_Blocked', 'float'), ('FL_Tgt', 'Vector')):
    if '"%s"' % n not in have:
        T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': ty}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True})
T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if 'FL_Gnd`' in dsl and 'FL_Free' in dsl: print('FALL8 already'); sys.exit()
L = dsl.split(NL); edits = []
def SL(b): return '(`SceneComponent.GetSocketLocation` (`self.Mesh`) "%s")' % b
def one(pred, what):
    a = [i for i, x in enumerate(L) if pred(x)]; assert len(a) == 1, (what, a); return a[0]
# 1
i = one(lambda x: x.lstrip().startswith('(set `self.FL_NZ`'), 'nz'); ind = L[i][:len(L[i]) - len(L[i].lstrip())]
g = [ind + '(bind (_flg1 _flg1ok) (`KismetSystemLibrary.LineTraceSingle` %s (- %s (%s 0.0 0.0 30.0))))' % (SL('pelvis'), SL('pelvis'), K('MakeVector')),
     ind + '(bind (_flg2 _flg2ok) (`KismetSystemLibrary.LineTraceSingle` %s (- %s (%s 0.0 0.0 30.0))))' % (SL('spine_05'), SL('spine_05'), K('MakeVector')),
     ind + '(set `self.FL_Gnd` (%s 1.0 0.0 (or _flg1ok _flg2ok)))' % K('SelectFloat')]
edits.append({'oldString': L[i], 'newString': L[i] + NL + NL.join(g)})
i = one(lambda x: x.lstrip().startswith('(if (and (< (`self.FL_Ph`) 0.5) (> (`self.FL_T`) (`self.FL_GndT`)))'), 'gnd')
edits.append({'oldString': L[i], 'newString': L[i].replace('(> (`self.FL_T`) (`self.FL_GndT`))', '(or (and (> (`self.FL_Gnd`) 0.5) (> (`self.FL_T`) 0.15)) (> (`self.FL_T`) (`self.FL_GndMax`)))')})
# 2
alt = '(* (`self.FL_RollW`) (* (+ 1.0 (* 0.25 (`self.FL_Tries`))) (%s 1.0 -1.0 (< (%s (`self.FL_Tries`) 2.0) 0.5))))' % (K('SelectFloat'), K('Percent_FloatFloat'))
for k, x in enumerate(L):
    if 'AddAngularImpulseInDegrees' in x and '(`self.FL_RollW`)' in x:
        edits.append({'oldString': x, 'newString': x.replace('(`self.FL_RollW`)', alt)})
# 3
a = one(lambda x: 'K2_SetActorLocation' in x and '74.0' in x, 'tp'); b = one(lambda x: x.strip().startswith('(set `self.FL_State` 2.0)'), 'st2')
ind = L[a][:len(L[a]) - len(L[a].lstrip())]
last = L[b]; core = '(set `self.FL_State` 2.0)'; closers = last.strip()[len(core):]
P = SL('pelvis'); fw = '(%s (- %s %s))' % (K('Vector_Normal2D'), SL('head'), P); rt = '(%s (%s 0.0 0.0 1.0) %s)' % (K('Cross_VectorVector'), K('MakeVector'), fw)
t0 = '(%s (.x %s) (.y %s) (+ (.z %s) 74.0))' % (K('MakeVector'), P, P, P)
sel = [ind + '(set `self.FL_Tgt` %s)' % t0, ind + '(set `self.FL_Free` 0.0)']
for nm, off in (('_fc0', None), ('_fc1', (fw, 45.0)), ('_fc2', (fw, -45.0)), ('_fc3', (rt, 45.0)), ('_fc4', (rt, -45.0))):
    tgt = t0 if off is None else '(+ %s (* %s %s))' % (t0, off[0], off[1])
    sel += [ind + '(if (< (`self.FL_Free`) 0.5)',
            ind + '  (bind (%s %sok) (`KismetSystemLibrary.CapsuleTraceSingle` (+ %s (%s 0.0 0.0 4.0)) (+ %s (%s 0.0 0.0 5.0)) 30.0 84.0))' % (nm, nm, tgt, K('MakeVector'), tgt, K('MakeVector')),
            ind + '  (if (not %sok)' % nm, ind + '    (set `self.FL_Tgt` %s)' % tgt, ind + '    (set `self.FL_Free` 1.0)))']
body = L[a:b + 1]; body[0] = ind + '(`Actor.K2_SetActorLocation` self (`self.FL_Tgt`) false true)'; body[-1] = ind + core
new = sel + [ind + '(if (> (`self.FL_Free`) 0.5)'] + ['  ' + x for x in body] + [ind + '  (else', ind + '    (set `self.FL_Still` 0.0)', ind + '    (set `self.FL_T` 0.0)', ind + '    (set `self.FL_Blocked` (+ (`self.FL_Blocked`) 1.0))))' + closers]
edits.append({'oldString': NL.join(L[a:b + 1]), 'newString': NL.join(new)})
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': edits})
print('FALL8', len(edits), 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:3000])
print('FALL8 compile', str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:300])
