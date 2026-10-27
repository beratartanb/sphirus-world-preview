"""probe233_subsys.py (write, manifest gt_subsys: a scratch BP /Game/_GateTest233/BP_SubsysProbe, deleted at the end): can the graph editor
create the 'Get Engine Subsystem (InputDeviceSubsystem)' node + GetMostRecentlyUsedHardwareDevice? Prints SUBSYS233 {...}."""
import unreal as u, json
out = {}
f = u.BlueprintFactory(); f.set_editor_property('parent_class', u.Actor)
bp = u.load_asset('/Game/_GateTest233/BP_SubsysProbe') or u.AssetToolsHelpers.get_asset_tools().create_asset('BP_SubsysProbe', '/Game/_GateTest233', u.Blueprint, f)
ge = u.BlueprintGraphEditor.get_graph_editor_by_name(bp, 'EventGraph')
try:
    av = [str(x) for x in ge.list_available_nodes([])]
    out['n_available'] = len(av); out['subsys'] = [x for x in av if 'Subsystem' in x and ('Input Device' in x or 'InputDevice' in x)][:12]
    out['hw'] = [x for x in av if 'Recently' in x][:8]
    out['break'] = [x for x in av if 'HardwareDevice' in x][:20]
    out['pf'] = [x for x in av if 'PlatformUser' in x][:10]
    out['enum_eq'] = [x for x in av if ('Enum' in x or 'enum' in x) and ('Equal' in x or 'E015fit' in x or '==' in x or 'Esit' in x or 'Eşit' in x)][:12]
except Exception as e: out['list_err'] = str(e)[:300]
for name in []:
    try:
        n = ge.create_node_from_name(name, u.Vector2D(0, 0), [])
        out.setdefault('created', {})[name] = n.get_class().get_name() if n else None
    except Exception as e: out.setdefault('created', {})[name] = 'ERR ' + str(e)[:120]
u.EditorAssetLibrary.delete_loaded_asset(bp)
out['deleted'] = not u.EditorAssetLibrary.does_asset_exist('/Game/_GateTest233/BP_SubsysProbe')
try: u.EditorAssetLibrary.delete_directory('/Game/_GateTest233')
except Exception: pass
print('SUBSYS233 ' + json.dumps(out, default=str))
