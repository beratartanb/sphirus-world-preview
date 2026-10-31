"""RefreshTools probe (control job, read-only for assets): runs the console command ModelContextProtocol.RefreshTools in the
running editor and records the ToolsetRegistry inventory and the in-process tool dispatch before and after.
The MCP HTTP server is NOT started (port 8000 stays closed), so the tools/list_changed broadcast to clients is not exercised.
Nothing is written to config, assets or maps. Output: <OUT>/refresh_probe.json (+ the log lines are read afterwards from the editor log).
"""
import unreal as u, json, os, time

OUT = r'C:\Users\berat\AppData\Local\Temp\claude\C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS\5f49a232-b001-47ad-8881-1eb04d9cb1c5\scratchpad\t1'


def inventory():
    s = u.ToolsetRegistry.get_all_toolset_json_schemas()
    try:
        d = json.loads(s)
    except Exception:
        return {'raw_len': len(s)}
    names = sorted(d.keys()) if isinstance(d, dict) else sorted(str(x.get('name', x))[:80] for x in d) if isinstance(d, list) else []
    return {'json_len': len(s), 'toolset_count': len(names), 'names': names}


def dispatch_ok():
    r = u.ToolsetRegistry.execute_tool('EditorToolset.EditorAppToolset', 'IsPIERunning', '{}')
    try:
        return {'complete': r.get_editor_property('is_complete'), 'value': r.get_editor_property('value'), 'error': str(r.get_editor_property('error'))}
    except Exception as ex:
        return {'err': repr(ex)}


res = {'time': time.strftime('%Y-%m-%d %H:%M:%S'), 'before': inventory(), 'dispatch_before': dispatch_ok()}
w = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
u.SystemLibrary.execute_console_command(w, 'ModelContextProtocol.RefreshTools')
res['after'] = inventory()
res['dispatch_after'] = dispatch_ok()
res['same_toolsets'] = res['before'].get('names') == res['after'].get('names')
S = u.EditorLoadingAndSavingUtils
res['dirty_after'] = sorted([p.get_name() for p in S.get_dirty_content_packages()] + [p.get_name() for p in S.get_dirty_map_packages()])
with open(os.path.join(OUT, 'refresh_probe.json'), 'w') as f:
    json.dump(res, f, indent=1, default=str)
print('REFRESH_PROBE toolsets before %s after %s same %s dispatch_after %s' % (res['before'].get('toolset_count'), res['after'].get('toolset_count'),
                                                                                res['same_toolsets'], res['dispatch_after']))
