# m_stophold8_mcp.py (MCP, in-memory; BP_HybridA_Player; re-appliable) - round 8.
# Sprint/run -> back: GR_StopHold keeps the input off (stop clip) until the capsule is slower than 80 cm/s, then the back input returns and
# Motion Matching chooses between the PIVOT database (capsule still moving forward) and the back START database (capsule already at / past
# zero). At 60 Hz the choice happened at ~40 cm/s forward -> pivot (right foot 2 cm). At 30 Hz one frame of braking is 33 cm/s, the choice
# happened at -1..-2 cm/s -> back start with the left foot while the right foot is still the loaded front foot -> 16-17 cm drag
# (g7s_B_30 / g8_B_30 / g8_K_30; bisect r8/bis8.txt: every run that chose the start clip slid, every run that chose the pivot did not).
# The release speed now leads by the braking of the coming frames: GR_StopRel + GR_StopLead x frame time (80 + 2000 x dt:
# 113 cm/s at 60 Hz, 147 at 30 Hz), so the choice is made at a clearly forward speed at any frame rate.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = AP + '.BP_HybridA_Player'; NL = chr(10)
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for n in ('GR_StopRel', 'GR_StopLead'):
    if '"%s"' % n not in have:
        T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
l = [x for x in dsl.split(NL) if x.strip().startswith('(set `self.GR_StopHold`')]; assert len(l) == 1, len(l); l = l[0]
if 'GR_StopRel' in l: print('STOPHOLD8 already'); sys.exit(0)
a = '(and (`self.GR_StopHold`) (> (`KismetMathLibrary.VSizeXY` (`self.GetVelocity`)) 80.0))'; assert l.count(a) == 1, l.count(a)
b = '(and (`self.GR_StopHold`) (> (`KismetMathLibrary.VSizeXY` (`self.GetVelocity`)) (+ (`self.GR_StopRel`) (* (`self.GR_StopLead`) DeltaSeconds))))'
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': l, 'newString': l.replace(a, b)}]})
print('STOPHOLD8', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200])
