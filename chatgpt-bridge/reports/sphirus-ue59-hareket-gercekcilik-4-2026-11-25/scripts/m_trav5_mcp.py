# m_trav5_mcp.py (MCP, in-memory; AC_Sph_Traversal (project copy of GASP AC_TraversalLogic) + BP_HybridA_Player jump; re-appliable)
# GENERIC LEDGES. The vendor TryTraversalAction only accepted LevelBlock_Traversable actors (cast + the block's own ledge splines), so
# real level geometry never produced a traversal. In the project copy the cast step is replaced by probing the geometry that the
# vendor forward capsule trace hit:
#  - front ledge: a downward line trace just behind the hit face from feet + 320 cm; the top must be walkable (normal.z > 0.7);
#    an obstacle taller than the probe (start inside it) or with no walkable top has no front ledge -> no traversal;
#  - depth: the top is followed across the obstacle (20..200 cm); the first sample that is not at the top height is the back ledge;
#    no drop within 200 cm = no back ledge (a mantle onto a platform);
# then the vendor steps run unchanged: room check to the front ledge (head clearance), room across the top, back-floor trace,
# chooser (hurdle / vault / mantle by height, depth, speed, pose) and the motion-warped montage. The player's jump key asks the
# copy first (player initiated only, never while crouched / carrying); if nothing is chosen the normal jump runs.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10); K = '`KismetMathLibrary.%s`'; V = lambda n: '(`self.%s`)' % n
CA = '/Game/Sphirus/Player/Traversal/AC_Sph_Traversal'; CB = CA + '.AC_Sph_Traversal'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': CB}})); ch = False
for nme, ty in (('GT_Top', 'float'), ('GT_D', 'float'), ('GT_Ok', 'bool'), ('GT_Done', 'bool'), ('GT_N', 'vector'), ('GT_P', 'vector')):
    if '"%s"' % nme not in have: T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': CB}, 'name': nme, 'typeName': ty}); ch = True
if ch: T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': CB}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': CA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Saved', 'UE59Work', 'p4', 'travcopy_dsl.txt'), 'w', encoding='utf8').write(dsl)
if '(set `self.GT_Done` true)' in dsl: print('TRAV5 copy already')
else:
    L = dsl.split(NL)
    a = [i for i, x in enumerate(L) if x.strip().startswith('(bind _aslevel_block_traversable (cast `/Game/Levels/LevelPrototyping/LevelBlock_Traversable`')]; assert len(a) == 1, a; a = a[0]
    b = [i for i in range(a, a + 40) if L[i].strip() == '(:`CastFailed`']; assert b, 'castfailed'; b = b[0]
    assert L[b + 1].strip() == '_)))', L[b + 1]
    ind = L[a][:len(L[a]) - len(L[a].lstrip())]
    FEET = '(- (.z (`local.ActorLocation`)) (`local.CapsuleHalfHeight`))'
    N = V('GT_N'); P = V('GT_P'); MV = lambda x, y, z: '(%s %s %s %s)' % (K % 'MakeVector', x, y, z)
    at = lambda d, z: MV('(- (.x %s) (* (.x %s) %s))' % (P, N, d), '(- (.y %s) (* (.y %s) %s))' % (P, N, d), z)
    g = ['(setmembers `/Game/Blueprints/Data/S_TraversalCheckResult` :`StructRef` (`local.TraversalCheckResult`) :`HitComponent` _outhit_hitcomponent)',
         '(set `self.GT_N` (%s _outhit_impactnormal))' % (K % 'Vector_Normal2D'),
         '(set `self.GT_P` _outhit_impactpoint)',
         '(bind (_gtt _gttb) (`KismetSystemLibrary.LineTraceSingle` %s %s))' % (at('5.0', '(+ %s 320.0)' % FEET), at('5.0', '(+ %s 25.0)' % FEET)),
         '(bind (_gtb _gti _gtt2 _gtd _gtl _gtip _gtn _gtin) (`GameplayStatics.BreakHitResult` _gtt))',
         '(set `self.GT_Ok` (and (and _gttb (not _gti)) (> (.z _gtin) 0.7)))',
         '(set `self.GT_Top` (.z _gtip))', '(set `self.GT_D` 0.0)', '(set `self.GT_Done` false)']
    for k, d in enumerate((20, 40, 60, 80, 100, 130, 160, 200)):
        g += ['(bind (_gs%d _gsb%d) (`KismetSystemLibrary.LineTraceSingle` %s %s))' % (k, k, at('%.1f' % d, '(+ %s 40.0)' % V('GT_Top')), at('%.1f' % d, '(- %s 30.0)' % V('GT_Top'))),
              '(if (not %s)' % V('GT_Done'),
              '  (if (and _gsb%d (< (%s (- (.z (`.ImpactPoint` (`GameplayStatics.BreakHitResult` _gs%d))) %s)) 12.0))' % (k, K % 'Abs', k, V('GT_Top')),
              '    (set `self.GT_D` %.1f)' % d,
              '    (else',
              '      (set `self.GT_Done` true))))']
    g += ['(setmembers `/Game/Blueprints/Data/S_TraversalCheckResult` :`StructRef` (`local.TraversalCheckResult`) :`HasFrontLedge` %s :`FrontLedgeLocation` %s :`FrontLedgeNormal` %s :`HasBackLedge` (and %s %s) :`BackLedgeLocation` %s :`BackLedgeNormal` (%s %s))' % (
              V('GT_Ok'), MV('(.x %s)' % P, '(.y %s)' % P, V('GT_Top')), N, V('GT_Ok'), V('GT_Done'), at('(+ %s 5.0)' % V('GT_D'), V('GT_Top')), K % 'NegateVector', N)]
    new = NL.join(ind + x for x in g)
    new = new + ')'   # closes the enclosing (if _outhit_bblockinghit
    r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': CA, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': NL.join(L[a:b + 2]), 'newString': new}]})
    print('TRAV5 copy', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:3000], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': CB}, 'bWarningsAsErrors': False}))[:300])
# player jump: ask the project copy first
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for nme, ty in (('TR_On', 'float'), ('TR_Fail', 'bool')):
    if '"%s"' % nme not in have:
        T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': nme, 'typeName': ty})
        if ty == 'float': T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': nme, 'bInstanceEditable': True})
T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '(set `self.TR_Fail` true)' in dsl: print('TRAV5 jump already'); sys.exit(0)
g = '(and (not (`self.GR_Load2H`)) (not (`self.bIsCrouched`)))'; old = '    (if %s' % g + NL + '      (set `CharacterMovementComponent.JumpZVelocity`'; assert dsl.count(old) == 1, dsl.count(old)
new = NL.join(['    (set `self.TR_Fail` true)',
    '    (if (and %s (> %s 0.5))' % (g, V('TR_On')),
    '      (bind (_trfail _trmfail) (`/Game/Sphirus/Player/Traversal/AC_Sph_Traversal.TryTraversalAction` (`self.SphTraversal`) (`self.GetTraversalCheckInputs`) "None"))',
    '      (set `self.TR_Fail` _trfail))',
    '    (if (and %s %s)' % (g, V('TR_Fail')),
    '      (set `CharacterMovementComponent.JumpZVelocity`'])
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': old, 'newString': new}]})
print('TRAV5 jump', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:3000], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:300])
