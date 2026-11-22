# m_softstart6_mcp.py (MCP, in-memory; BP_HybridA_Player, one line after the GR_GaitSel selection; re-appliable) - round 6b.
# SOFT START. Every run / sprint start clip of the project is an athletic lunge (trunk 41-61 deg, pelvis drop 15-22 cm; in game the head
# dipped 33 cm within 0.45 s). A start from rest now begins as a WALK start (raw: pelvis drop 5-9 cm, trunk 6-16 deg) for the first
# GR_SoftStartT seconds / until GR_SoftStartV cm/s, then the requested gait takes over through the walk-to-run transition clips.
# The input is taken at once; only the first step is a walking step. Not applied to backward starts, held brakes or reversal re-pushes.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = AP + '.BP_HybridA_Player'; MOT = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; NL = chr(10)
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for n, ty in (('GR_SoftStartT', 'float'), ('GR_SoftStartV', 'float'), ('GR_SoftStartOn', 'bool')):
    if '"%s"' % n in have: continue
    T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': ty}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if 'GR_SoftStartT' in dsl: print('SOFTSTART already'); sys.exit(0)
l = [x for x in dsl.split(NL) if x.strip().startswith('(set `self.GR_GaitSel`')]; assert len(l) == 1; l = l[0]; ind = l[:len(l) - len(l.lstrip())]
def mot(n): return '(`%s.%s` (`self.SphMotion`))' % (MOT, n)
cond = '(and (and (and (`self.GR_SoftStartOn`) (< %s (`self.GR_SoftStartT`))) (and (< (`KismetMathLibrary.VSizeXY` (`self.GetVelocity`)) (`self.GR_SoftStartV`)) (<= %s 0.0))) (and (not (`self.GR_Back`)) (not (`self.GR_BrakeHold`))))' % (mot('StartT'), mot('RcExit'))
new = l + NL + ind + '(set `self.GR_GaitSel` (`KismetMathLibrary.SelectInt` 0 (`self.GR_GaitSel`) %s))' % cond
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': l, 'newString': new}]})
print('SOFTSTART', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:120])
