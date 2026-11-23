# rd_cam_dsl.py (read-only, diagnostic MCP client): dump the live AC_Sph_Camera graph DSL to Saved/UE59Work/r2g/cam_live.dsl
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = sys.argv[1] if len(sys.argv) > 1 else '/Game/Sphirus/Player/Camera/AC_Sph_Camera'; out = sys.argv[2] if len(sys.argv) > 2 else 'Saved/UE59Work/r2g/cam_live.dsl'
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']
open(out, 'w', encoding='utf8').write(rv['dsl']); print('DSL', len(rv['dsl']), 'rev', rv.get('revision'))
