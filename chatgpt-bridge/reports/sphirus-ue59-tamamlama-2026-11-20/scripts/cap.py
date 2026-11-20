# cap.py <out stem>: editor image through the Epic MCP CaptureEditorImage tool (read-only); umcp saves <stem>*.png
import json, sys, os, glob
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init(); umcp.tool('list_toolsets', {})
umcp.IMG = sys.argv[1]
r = umcp.tool('call_tool', {'toolset_name': 'EditorToolset.EditorAppToolset', 'tool_name': 'CaptureEditorImage', 'arguments': json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}})
print('CAP', str(r)[:200], glob.glob(sys.argv[1] + '*'))
