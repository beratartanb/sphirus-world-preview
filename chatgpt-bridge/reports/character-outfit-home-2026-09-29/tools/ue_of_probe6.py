import unreal as u
print([f for f in dir(u.SkeletalMeshLODSettings) if not f.startswith('_') and f not in dir(u.Object)])
print([f for f in dir(u.SkeletalMesh) if 'lod' in f.lower()])
