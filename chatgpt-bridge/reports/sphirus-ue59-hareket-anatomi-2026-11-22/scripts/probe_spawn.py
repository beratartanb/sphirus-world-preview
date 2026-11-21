import unreal as u
print('SPAWNAPI', [x for x in dir(u.GameplayStatics) if 'spawn' in x.lower()], [x for x in dir(u.SystemLibrary) if 'spawn' in x.lower()][:5], [x for x in dir(u) if 'spawn' in x.lower() and 'actor' in x.lower()][:12])
