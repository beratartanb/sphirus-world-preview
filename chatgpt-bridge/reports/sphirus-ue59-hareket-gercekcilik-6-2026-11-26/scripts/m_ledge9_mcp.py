# m_ledge9_mcp.py (MCP, in-memory): ledge catch only on non-moving geometry + let go when the hold disappears (pass 6).
# Bug (fl8_throw): a thrown physics box pushed her up (Falling for a few frames), the ledge detector took the flying box as a wall and its
# top as a ledge; she hung (Flying) in mid-air for the rest of the recording after the box had gone.
# Fix: (1) the wall and the top surface must not be simulating physics; (2) while catching / hanging (states 1-2) a trace from the chest
# height toward the wall must still hit a non-simulating surface, else she lets go (falling, slot stopped, 0.8 s re-grab cooldown).
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10); BQ = chr(96)
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; L = rv['dsl'].split(NL)
if any('_lghok' in x or 'LG_Hold' in x for x in L): print('LG9 already'); sys.exit()
def one(pred, what):
    a = [i for i, x in enumerate(L) if pred(x)]; assert len(a) == 1, (what, a); return a[0]
def SIM(h): return '(`PrimitiveComponent.IsSimulatingPhysics` (`.HitComponent` (`GameplayStatics.BreakHitResult` %s)) "None")' % h
edits = []
import re
# the editor renames bind variables on round-trip: anchor on the structure (first lines after the LG_Reach wall trace)
w = one(lambda x: 'LineTraceSingle' in x and 'LG_Reach' in x, 'walltrace')
mw = re.match(r'\s*\(bind \((\S+) (\S+)\)', L[w]); hw, okw = mw.group(1), mw.group(2)
i = w + 1; assert L[i].strip().startswith('(if (and %s (< (`KismetMathLibrary.Abs` (.z (`.ImpactNormal`' % okw), L[i]
edits.append({'oldString': L[i], 'newString': L[i].replace('(if (and %s ' % okw, '(if (and (and %s (not %s)) ' % (okw, SIM(hw)), 1)})
t = i + 1
while not re.match(r'\s*\(bind \(\S+ \S+\) \(`KismetSystemLibrary.LineTraceSingle`', L[t]): t += 1
mt = re.match(r'\s*\(bind \((\S+) (\S+)\)', L[t]); ht, okt = mt.group(1), mt.group(2)
i = t + 1; assert L[i].strip().startswith('(if (and %s (> (.z (`.ImpactNormal`' % okt), L[i]
edits.append({'oldString': L[i], 'newString': L[i].replace('(if (and %s ' % okt, '(if (and (and %s (not %s)) ' % (okt, SIM(ht)), 1)})
i = one(lambda x: x.strip().startswith('(set `self.LG_N2`'), 'n2'); ind = L[i][:len(L[i]) - len(L[i].lstrip())]
A = '(`Actor.K2_GetActorLocation` self)'; H = '(+ %s (`KismetMathLibrary.MakeVector` 0.0 0.0 20.0))' % A
AI = '(`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`))'
hold = [ind + '(if (< (`self.LG_State`) 2.5)',
        ind + '  (bind (_lgh _lghok) (`KismetSystemLibrary.LineTraceSingle` %s (- %s (* (`self.LG_N`) 85.0))))' % (H, H),
        ind + '  (if (or (not _lghok) %s)' % SIM('_lgh'),
        ind + '    (`AnimInstance.StopSlotAnimation` %s 0.25 "DefaultSlot")' % AI,
        ind + '    (`CharacterMovementComponent.SetMovementMode` (`self.CharacterMovement`) "MOVE_Falling" 0)',
        ind + '    (set `self.LG_Cool` 0.8)',
        ind + '    (set `self.LG_State` 0.0)))']
edits.append({'oldString': L[i], 'newString': L[i] + NL + NL.join(hold)})
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': edits})
print('LG9', len(edits), 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:2500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200])
