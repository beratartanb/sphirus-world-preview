# m_trav7_mcp.py (MCP, in-memory; BP_HybridA_Player; re-appliable) - pass 5.
# APPROACH SPEED FOR TRAVERSAL. The contact system's anticipation brake slows the capsule in the last metre before a wall-like obstacle,
# so the pass-4 traversal check (which read the current speed) chose stand variants (31-36 cm/s at the key press) after a run-up.
# The approach speed is now TR_SpPk: the ground speed peak, decaying TR_PkDecay cm/s per second (tick). The traversal reach and the
# run / walk / stand variant use it; the capsule speed itself is untouched (no added velocity).
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10); K = '`KismetMathLibrary.%s`'
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for nme in ('TR_SpPk', 'TR_PkDecay'):
    if '"%s"' % nme not in have:
        T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': nme, 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': nme, 'bInstanceEditable': True})
T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '(set `self.TR_SpPk`' in dsl: print('TRAV7 already'); sys.exit(0)
L = dsl.split(NL); SPD = '(`KismetMathLibrary.VSizeXY` (`self.GetVelocity`))'
a = [i for i, x in enumerate(L) if x.strip() == '(set `self.TR_Fail` true)']; assert len(a) == 1; a = a[0]
b = max(i for i, x in enumerate(L) if 'PerformTraversalAction_Clients' in x); assert b > a
edits = []
for i in range(a, b + 1):
    if SPD in L[i] and ('MapRangeClamped' in L[i] or 'SelectObject' in L[i]):
        edits.append({'oldString': L[i], 'newString': L[i].replace(SPD, '(`self.TR_SpPk`)')})
assert edits, 'no speed reads in the traversal block'
t = [i for i, x in enumerate(L) if x.startswith('  (set `self.CS_Latch` ')]; assert len(t) == 1
gnd = '(`NavMovementComponent.IsMovingOnGround` (`self.CharacterMovement`))'
ins = '  (set `self.TR_SpPk` (%s (%s %s 0.0 (not %s)) (- (`self.TR_SpPk`) (* (`self.TR_PkDecay`) DeltaSeconds))))' % (K % 'FMax', K % 'SelectFloat', SPD, gnd)
edits.append({'oldString': L[t[0]], 'newString': ins + NL + L[t[0]]})
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': edits})
print('TRAV7', len(edits), 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:2000], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200])
