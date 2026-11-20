# m_fwdhold_mcp.py (MCP, in-memory edit of BP_HybridA_Player): back-tempo -> forward run. Shift+S (234 cm/s, Core Motion jog back)
# followed by Shift+W switched to the run tier at once, so the Relaxed run pivot B->F (authored for 375 cm/s) played from 234 and the
# planted foot slid 21-30 cm. While the tempo tier was active and the input still opposes the velocity (reversal not finished,
# speed < 300), the tempo tier is kept (jog pivot B->F of the same family); the run tier takes over once the velocity turned.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = AP + '.BP_HybridA_Player'
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
L = [l for l in dsl.split('\n') if l.strip().startswith('(set `self.GR_TempoAct`')]; assert len(L) == 1
old = L[0]; a = "(or (`self.GR_Back`) (not "; assert old.count(a) == 1
DOT = "(`KismetMathLibrary.Dot_VectorVector` (`KismetMathLibrary.Vector_Normal2D` (`self.GR_RawIn`)) (`KismetMathLibrary.Vector_Normal2D` (`self.GetVelocity`)))"
FH = "(and (and (`self.GR_TempoPrev`) (< (`KismetMathLibrary.VSizeXY` (`self.GetVelocity`)) 300.0)) (and (> (`KismetMathLibrary.VSizeXY` (`self.GetVelocity`)) 30.0) (< %s -0.2)))" % DOT
new = old.replace(a, "(or (or (`self.GR_Back`) %s) (not " % FH)
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': old, 'newString': new}]})
print('FWDHOLD', str(r2)[:600] if r2.get('isError') else 'ok', str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:120])
