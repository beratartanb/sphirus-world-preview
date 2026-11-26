# m_fall10_mcp.py (MCP, in-memory): get-up hand-over v3 (pass 6), replaces the m_fall9 idea.
# fl8 (original): physics off on all bodies, then spine_01 / thighs back ON in the same frame -> those bodies restarted against a kinematic
#   pelvis already snapped to the clip -> torso whipped upright (face-down -> sitting in 0.2 s).
# fl9 (m_fall9, everything kept simulating): with the pelvis (root body) simulating, the mesh component transform follows the pelvis body,
#   so the get-up clip was drawn around the tumbling pelvis -> she floated ~50 cm and rolled in the air.
# v3: capsule + mesh re-placed with teleport, ALL bodies kinematic (none re-enabled), and the get-up montage blends in over FL_GuBlend
# (0.35 s) from the pose the slot already holds: during the ground phase the slot holds M_ragdoll_poses_OnGround's prone frame and the
# joint motors pull the ragdoll toward it, so the visible hand-over is a short blend from that lying pose into the clip's lying frame 0.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10)
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
if '"FL_GuBlend"' not in have:
    T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': 'FL_GuBlend', 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': 'FL_GuBlend', 'bInstanceEditable': True})
    T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; L = rv['dsl'].split(NL)
a = [i for i, x in enumerate(L) if x.strip() == '(`self.K2_SetActorLocation` self (`self.FL_Tgt`) false false)']
if not a: print('FALL10 already / anchor missing'); sys.exit()
a = a[0]; b = a
while 'SphF_am_InjuredBelly_DropToFloor_GetUp' not in L[b]: b += 1
blk = L[a:b + 1]; ind = blk[0][:len(blk[0]) - len(blk[0].lstrip())]; out = []
for x in blk:
    s = x.strip()
    if s == '(`self.K2_SetActorLocation` self (`self.FL_Tgt`) false false)':
        out.append(x.replace('false false)', 'false true)')); continue
    if s.startswith('(`self.K2_SetActorRotation`') and s.endswith(' false)'):
        out.append(x[:x.rstrip().rfind(' false)')] + ' true)')
        out.append(ind + '(`SkeletalMeshComponent.SetAllBodiesBelowSimulatePhysics` (`self.Mesh`) (`KismetStringLibrary.Conv_StringToName` "pelvis") false true)'); continue
    if s.startswith('(`SceneComponent.K2_SetRelativeLocationAndRotation` (`self.Mesh`)') and s.endswith('false false)'):
        out.append(x[:x.rstrip().rfind('false false)')] + 'false true)'); continue
    if 'SphF_am_InjuredBelly_DropToFloor_GetUp' in s:
        x = x.replace('"DefaultSlot" 0.0 0.5', '"DefaultSlot" (`self.FL_GuBlend`) 0.5', 1); assert 'FL_GuBlend' in x, x
    out.append(x)
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': NL.join(blk), 'newString': NL.join(out)}]})
print('FALL10', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:2000], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200])
