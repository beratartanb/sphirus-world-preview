import unreal as u
print([n for n in dir(u.MaterialProperty) if n.startswith('MP_')])
