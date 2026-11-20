# r_dsl.py <asset> <scope> <out>: read-only MCP DSL read of one scope of a Blueprint
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': sys.argv[1], 'scope': sys.argv[2]})
c = r.get('content')
if isinstance(c, str):
    try: c = json.loads(c)
    except Exception: print('RAW', sys.argv[2], c[:500]); sys.exit(0)
rv = c.get('returnValue', c); d = rv.get('dsl') if isinstance(rv, dict) else None
open(sys.argv[3], 'w', encoding='utf8').write(d if d else json.dumps(r, indent=1)); print('DSL', sys.argv[2], len(d) if d else 'ERR', str(r)[:300] if not d else '')

