# m_trav6_mcp.py (MCP, in-memory; BP_HybridA_Player jump input; replaces the m_trav5 jump block; re-appliable) - movement pass 4.
# PLAYER-SIDE TRAVERSAL CHECK. The GASP check (TryTraversalAction) only accepts LevelBlock_Traversable actors and its chooser node
# cannot be edited through the graph DSL, so the check and the action choice live here; the project component SphTraversal
# (copy of AC_TraversalLogic) only performs: plays the chosen motion-warped montage, sets the FrontLedge / BackLedge / BackFloor warp
# targets, flying mode during the action, end movement mode afterwards.
# On the jump key (player initiated only; never crouched / two-hand carry):
#  1. forward capsule sweep (bottom 30 cm above the feet) over 90..230 cm by speed: a facing, near-vertical surface;
#  2. top: downward probe just behind the face from feet + 330 cm; walkable top required (taller walls / no top -> no action);
#  3. depth: the top is followed 20..200 cm; a drop = back ledge; then the floor behind it (back floor) is probed;
#  4. head room: a standing capsule just in front of the ledge at top height must be free, and on top (mantle / climb) or across the
#     top (hurdle) must be free;
#  5. reach: horizontal distance to the face within the gait's reach (stand 110, walk 170, run 260 cm);
#  6. choice: H < 35 -> nothing (a step); thin obstacle (depth <= 70, back floor, H <= 130) -> hurdle (run / walk / stand variant);
#     otherwise H <= 160 -> mantle; H <= 260 -> 2.5 m climb-up; higher -> nothing. Foot variant = the foot in support now.
# Montage start time 0; motion warping keeps the root on the measured ledges (no limb stretch, no teleport).
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10); K = '`KismetMathLibrary.%s`'; V = lambda n: '(`self.%s`)' % n
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}})); ch = False
for nme, ty in (('GT_N', 'vector'), ('GT_P', 'vector'), ('GT_Top', 'float'), ('GT_D', 'float'), ('GT_H', 'float'), ('GT_Dist', 'float'), ('GT_FloorZ', 'float'),
                ('GT_Ok', 'bool'), ('GT_Done', 'bool'), ('GT_FlOk', 'bool'), ('GT_Room', 'bool'), ('GT_Left', 'bool'), ('TR_Kind', 'float')):
    if '"%s"' % nme not in have: T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': nme, 'typeName': ty}); ch = True
if '"TR_Res"' not in have:
    print('struct var', str(T('BlueprintToolsets.BlueprintToolset.AddStructVariable', {'blueprint': {'refPath': BP}, 'name': 'TR_Res', 'structType': '/Game/Blueprints/Data/S_TraversalCheckResult.S_TraversalCheckResult'}))[:200]); ch = True
if ch: T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '(set `self.GT_Room`' in dsl: print('TRAV6 already'); sys.exit(0)
L = dsl.split(NL)
a = [i for i, x in enumerate(L) if x.strip() == '(set `self.TR_Fail` true)']; assert len(a) == 1, a; a = a[0]
b = a + 1; assert L[b].strip().startswith('(if (and (and (not (`self.GR_Load2H`)) (not (`self.bIsCrouched`))) (> (`self.TR_On`) 0.5))'), L[b][:120]
c = b + 2; assert L[c].strip().startswith('(set `self.TR_Fail` _'), L[c][:100]
ind = L[a][:len(L[a]) - len(L[a].lstrip())]
MV = lambda x, y, z: '(%s %s %s %s)' % (K % 'MakeVector', x, y, z)
LOC = '(`self.K2_GetActorLocation`)'; SPD = '(%s (`self.GetVelocity`))' % (K % 'VSizeXY'); FW = '(`self.GetActorForwardVector`)'
FEET = '(- (.z %s) 88.0)' % LOC
N = V('GT_N'); P = V('GT_P')
at = lambda d, z: MV('(- (.x %s) (* (.x %s) %s))' % (P, N, d), '(- (.y %s) (* (.y %s) %s))' % (P, N, d), z)
REACH = '(%s %s 0.0 300.0 110.0 260.0)' % (K % 'MapRangeClamped', SPD)
g = ['(set `self.TR_Fail` true)',
     '(if (and (and (not (`self.GR_Load2H`)) (not (`self.bIsCrouched`))) (> %s 0.5))' % V('TR_On'),
     '  (bind (_tvh _tvb) (`KismetSystemLibrary.CapsuleTraceSingle` :`Start` %s :`End` (+ %s (* %s %s)) :`Radius` 30.0 :`HalfHeight` 58.0))' % (LOC, LOC, FW, MV(REACH, REACH, REACH)),
     '  (bind (_tvb2 _tvi _tvt _tvd _tvl _tvip _tvn _tvin _tvpm _tvha _tvhc) (`GameplayStatics.BreakHitResult` _tvh))',
     '  (set `self.GT_N` (%s _tvin))' % (K % 'Vector_Normal2D'),
     '  (set `self.GT_P` _tvip)',
     '  (set `self.GT_Dist` (- (%s (- _tvip %s)) 35.0))' % (K % 'VSizeXY', LOC),
     '  (bind (_tvt1 _tvt1b) (`KismetSystemLibrary.LineTraceSingle` %s %s))' % (at('5.0', '(+ %s 330.0)' % FEET), at('5.0', '(+ %s 25.0)' % FEET)),
     '  (bind (_tvt1x _tvt1i _tvt1t _tvt1d _tvt1l _tvt1p _tvt1n _tvt1in) (`GameplayStatics.BreakHitResult` _tvt1))',
     '  (set `self.GT_Ok` (and (and (and (and _tvb (< (%s (.z _tvin)) 0.35)) (> (%s %s %s) 0.5)) (and _tvt1b (not _tvt1i))) (> (.z _tvt1in) 0.7)))' % (K % 'Abs', K % 'Dot_VectorVector', N, '(%s %s)' % (K % 'NegateVector', FW)),
     '  (set `self.GT_Top` (.z _tvt1p))',
     '  (set `self.GT_H` (- %s %s))' % (V('GT_Top'), FEET),
     '  (set `self.GT_D` 0.0)', '  (set `self.GT_Done` false)']
for k, d in enumerate((20, 40, 60, 80, 100, 130, 160, 200)):
    g += ['  (bind (_tvs%d _tvsb%d) (`KismetSystemLibrary.LineTraceSingle` %s %s))' % (k, k, at('%.1f' % d, '(+ %s 40.0)' % V('GT_Top')), at('%.1f' % d, '(- %s 30.0)' % V('GT_Top'))),
          '  (if (not %s)' % V('GT_Done'),
          '    (if (and _tvsb%d (< (%s (- (.z (`.ImpactPoint` (`GameplayStatics.BreakHitResult` _tvs%d))) %s)) 12.0))' % (k, K % 'Abs', k, V('GT_Top')),
          '      (set `self.GT_D` %.1f)' % d,
          '      (else',
          '        (set `self.GT_Done` true))))']
DB = '(+ %s 45.0)' % V('GT_D')
g += ['  (bind (_tvf _tvfb) (`KismetSystemLibrary.LineTraceSingle` %s %s))' % (at(DB, '(+ %s 10.0)' % V('GT_Top')), at(DB, '(- %s 60.0)' % FEET)),
      '  (set `self.GT_FlOk` (and (and %s _tvfb) (> (.z (`.ImpactNormal` (`GameplayStatics.BreakHitResult` _tvf))) 0.7)))' % V('GT_Done'),
      '  (set `self.GT_FloorZ` (.z (`.ImpactPoint` (`GameplayStatics.BreakHitResult` _tvf))))',
      # head room: standing capsule in front of the ledge at top height, and on top (mantle / climb) or past the top (hurdle)
      '  (bind (_tvr1 _tvr1b) (`KismetSystemLibrary.CapsuleTraceSingle` :`Start` (+ %s %s) :`End` %s :`Radius` 33.0 :`HalfHeight` 86.0))' % (LOC, MV('0.0', '0.0', '2.0'), at('-38.0', '(+ %s 90.0)' % V('GT_Top'))),
      '  (bind (_tvr2 _tvr2b) (`KismetSystemLibrary.CapsuleTraceSingle` :`Start` %s :`End` %s :`Radius` 33.0 :`HalfHeight` 86.0))' % (at('-38.0', '(+ %s 90.0)' % V('GT_Top')), at('(%s (+ %s 40.0) 45.0 (and %s %s))' % (K % 'SelectFloat', V('GT_D'), V('GT_Done'), '(< %s 70.0)' % V('GT_D')), '(+ %s 90.0)' % V('GT_Top'))),
      '  (set `self.GT_Room` (not (or _tvr1b _tvr2b)))',
      '  (set `self.GT_Left` (> (`AnimInstance.GetCurveValue` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)) "contact_l") (`AnimInstance.GetCurveValue` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)) "contact_r")))',
      '  (set `self.TR_Kind` 0.0)',
      '  (if (and (and (and %s %s) (> %s 35.0)) (< %s %s))' % (V('GT_Ok'), V('GT_Room'), V('GT_H'), V('GT_Dist'), REACH),
      '    (if (and (and (and %s (<= %s 70.0)) %s) (<= %s 130.0))' % (V('GT_Done'), V('GT_D'), V('GT_FlOk'), V('GT_H')),
      '      (set `self.TR_Kind` 2.0)',
      '      (elif (<= %s 160.0)' % V('GT_H'),
      '        (set `self.TR_Kind` 3.0)',
      '        (elif (<= %s 260.0)' % V('GT_H'),
      '          (set `self.TR_Kind` 4.0)))))']
def mont(kind, gait, foot):
    base = {'2': 'Hurdle/AM_M_Relaxed_Traversal_Hurdle_1_0_%s', '3': 'Mantle/AM_M_Relaxed_Traversal_Mantle_1_0_%s', '4': 'Climb/AM_M_Relaxed_Traversal_Climb_Start_2_5_%s'}[kind]
    tail = {'run': 'run_F_%s', 'walk': 'walk_F_%s', 'stand': ('stand_F_V2_%s' if kind == '2' else 'stand_F_%s')}[gait] % foot
    n = (base % tail).split('/')[-1]; return '"/Game/Characters/UEFN_Mannequin/Animations/Traversal/%s.%s"' % (base % tail, n)
def pick(kind):
    sel = lambda a_, b_, c_: '(%s %s %s %s)' % (K % 'SelectObject', a_, b_, c_)
    byfoot = lambda gait: sel(mont(kind, gait, 'Lfoot'), mont(kind, gait, 'Rfoot'), V('GT_Left'))
    return '(cast `AnimMontage` %s)' % sel(byfoot('run'), sel(byfoot('walk'), byfoot('stand'), '(> %s 60.0)' % SPD), '(> %s 300.0)' % SPD)
FL = MV('(.x %s)' % P, '(.y %s)' % P, V('GT_Top')); BLc = at(V('GT_D'), V('GT_Top')); BF = at('(+ %s 60.0)' % V('GT_D'), V('GT_FloorZ'))
for kind, enum in (('2', 'NewEnumerator2'), ('3', 'NewEnumerator3'), ('4', 'NewEnumerator3')):
    g += ['  (if (== %s %s.0)' % (V('TR_Kind'), kind),
          '    (setmembers `/Game/Blueprints/Data/S_TraversalCheckResult` :`StructRef` (`self.TR_Res`) :`ActionType` "%s" :`HasFrontLedge` true :`FrontLedgeLocation` %s :`FrontLedgeNormal` %s :`HasBackLedge` %s :`BackLedgeLocation` %s :`BackLedgeNormal` (%s %s) :`HasBackFloor` %s :`BackFloorLocation` %s :`ObstacleHeight` %s :`ObstacleDepth` %s :`BackLedgeHeight` (- %s %s) :`HitComponent` _tvhc :`ChosenMontage` %s :`StartTime` 0.0 :`PlayRate` 1.0)' % (
              enum, FL, N, 'true' if kind == '2' else 'false', BLc, K % 'NegateVector', N, 'true' if kind == '2' else 'false', BF, V('GT_H'), V('GT_D'), V('GT_Top'), V('GT_FloorZ'), pick(kind)),
          '    (`/Game/Sphirus/Player/Traversal/AC_Sph_Traversal.PerformTraversalAction_Clients` (`self.SphTraversal`) (`self.TR_Res`))',
          '    (set `self.TR_Fail` false))']
g[-1] = g[-1] + ')'   # closes the outer (if (and ... TR_On
new = NL.join(ind + x for x in g)
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': NL.join(L[a:c + 1]), 'newString': new}]})
print('TRAV6', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:4000], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:400])
