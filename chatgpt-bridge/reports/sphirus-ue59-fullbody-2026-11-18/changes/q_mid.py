import unreal as u
print('QMID', [n for n in dir(u) if 'MaterialLibrary' in n or n == 'MaterialInstanceDynamic'], [n for n in dir(u.MaterialInstanceDynamic) if 'create' in n.lower()][:5])
