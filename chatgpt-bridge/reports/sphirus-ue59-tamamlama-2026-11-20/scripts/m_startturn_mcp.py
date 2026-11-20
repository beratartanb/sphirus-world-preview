# m_startturn_mcp.py (MCP, in-memory edit of AC_Sph_Motion): the start cap applies only to turn-starts. StartTurn is latched on the
# first input frame from standstill when the input direction is more than ~100 deg away from the facing held while idle (PrevFwd).
# Straight starts stay uncapped (first-step drift 2-4 cm without it; the cap made them worse and slower).
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; BP = AP + '.AC_Sph_Motion'; out = {}
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for n, ty in (('StartTurn', 'bool'), ('PrevFwd', 'Vector'), ('StartTurnCos', 'float')):
    if '"%s"' % n in have: continue
    T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': ty})
    T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
def line(prefix):
    L = [l for l in dsl.split('\n') if l.strip().startswith(prefix)]; assert len(L) == 1, (prefix, len(L)); return L[0]
INV = '(`Pawn.GetLastMovementInputVector` _ascharacter)'; HASIN = '(> (`KismetMathLibrary.VSizeXY` %s) 0.1)' % INV
st = line('(set `self.StartT`'); ind = st[:len(st) - len(st.lstrip())]
pre = [
    "(set `self.StartTurn` (or (and (> (`self.StartT`) 0.0) (`self.StartTurn`)) (and (and (<= (`self.StartT`) 0.0) %s) (< (`KismetMathLibrary.Dot_VectorVector` (`KismetMathLibrary.Vector_Normal2D` %s) (`self.PrevFwd`)) (`self.StartTurnCos`)))))" % (HASIN, INV),
    "(set `self.PrevFwd` (`KismetMathLibrary.SelectVector` (`self.PrevFwd`) (`Actor.GetActorForwardVector` _ascharacter) %s))" % HASIN,
]
tc = line('(set `self.TurnCap`'); a = "(and (and (`self.StartCapOn`) (> (`self.StartT`) 0.0))"; assert tc.count(a) == 1
edits = [{'oldString': st, 'newString': '\n'.join(ind + s for s in pre) + '\n' + st}, {'oldString': tc, 'newString': tc.replace(a, "(and (and (and (`self.StartCapOn`) (`self.StartTurn`)) (> (`self.StartT`) 0.0))")}]
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': edits})
out['edit'] = str(r2)[:1200] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200]
print('STARTTURN', json.dumps(out)[:1500])
