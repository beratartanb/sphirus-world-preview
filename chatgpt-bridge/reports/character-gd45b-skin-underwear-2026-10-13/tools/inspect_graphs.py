"""GD45 audit (read-only): nodes in the player Blueprints' graphs that touch leader pose / grooms / bindings / anim class / skeletal meshes; all component classes of the pawn."""
import unreal as u, json
out = {}
KEYS = ('LeaderPose', 'MasterPose', 'Binding', 'Groom', 'SetSkeletalMesh', 'SetAnimClass', 'SetAnimInstanceClass', 'LODSync', 'Henley', 'Shorts', 'Manny', 'Face', 'CopyPose', 'SetSkinnedAsset')
for bpp in ('/Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/BP_Player_MM', '/Game/GraceRanger/BP_GR_Player', '/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player', '/Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/BP_ExampleCharacter_MotionMatching'):
    bp = u.load_asset(bpp); hits = []; ng = 0; nn = 0
    graphs = []
    for prop in ('ubergraph_pages', 'function_graphs', 'macro_graphs'):
        try: graphs += list(bp.get_editor_property(prop))
        except Exception as e: hits.append('ERR ' + prop + ' ' + str(e)[:50])
    for g in graphs:
        ng += 1
        try: nodes = list(g.get_editor_property('nodes'))
        except Exception as e: hits.append('ERR nodes ' + str(e)[:60]); continue
        for n in nodes:
            nn += 1; cls = n.get_class().get_name(); title = ''
            try: title = str(n.get_node_title(u.NodeTitleType.FULL_TITLE))[:90]
            except Exception: pass
            fn = ''
            try:
                mr = n.get_editor_property('function_reference'); fn = str(mr.get_editor_property('member_name')) if mr else ''
            except Exception: pass
            text = cls + '|' + title + '|' + fn
            if any(k.lower() in text.lower() for k in KEYS): hits.append({'graph': g.get_name(), 'node': cls, 'title': title, 'fn': fn})
    out[bpp.rsplit('/', 1)[-1]] = {'graphs': ng, 'nodes': nn, 'hits': hits[:40]}
gen = u.load_asset('/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player').generated_class(); a = u.EditorLevelLibrary.spawn_actor_from_class(gen, u.Vector(0, 0, -100000))
out['pawn_component_classes'] = sorted(set(c.get_class().get_name() for c in a.get_components_by_class(u.ActorComponent))); a.destroy_actor()
json.dump(out, open('C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/GD45_Promote_20261013/data/graphs.json', 'w'), indent=1); print('GD45_GRAPHS', json.dumps(out)[:2500], flush=True)
