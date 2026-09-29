import unreal as u
print('compact_mesh', hasattr(u.GeometryScript_MeshRepair, 'compact_mesh'), [f for f in dir(u.GeometryScript_MeshRepair) if not f.startswith('_') and 'compact' in f.lower()])
