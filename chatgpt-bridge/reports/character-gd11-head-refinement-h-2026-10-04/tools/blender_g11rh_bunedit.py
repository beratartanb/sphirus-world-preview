"""GD11 refinement H: edit the bun_loops collection INSIDE the guides .blend (lower loop groups: smaller radius, centre raised and moved toward the head)
and save a new .blend. usage: blender -b <in.blend> --python blender_g11rh_bunedit.py -- <out.blend> <r_scale> <dz> <dy>"""
import bpy, sys, os, json
a = sys.argv[sys.argv.index('--')+1:]; OUTB, RS, DZ, DY = a[0], float(a[1]), float(a[2]), float(a[3]); log = []
for ob in bpy.data.collections['bun_loops'].objects:
    if ob['c_off_z'] < -0.2:
        ob['r'] = ob['r']*RS; ob['c_off_z'] = ob['c_off_z']+DZ; ob['c_off_y'] = ob['c_off_y']+DY; ob.location.z += DZ; ob.location.y += DY; log.append(ob.name)
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUTB)); print('BUNEDIT', log)
