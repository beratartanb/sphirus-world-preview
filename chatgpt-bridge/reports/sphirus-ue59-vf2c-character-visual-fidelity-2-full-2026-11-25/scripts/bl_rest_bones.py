import bpy, sys, os, math
D = sys.argv[sys.argv.index('--') + 1]
bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.fbx(filepath=os.path.join(D, 'body.fbx'), automatic_bone_orientation=False)
arm = [o for o in bpy.data.objects if o.type == 'ARMATURE'][0]; mesh = [o for o in bpy.data.objects if o.type == 'MESH'][0]
H = {b.name: arm.matrix_world @ b.head_local for b in arm.data.bones}
d = lambda a, b: (H[a] - H[b]).length * 100
print('RB upperarm', round(d('upperarm_l', 'lowerarm_l'), 1), 'forearm', round(d('lowerarm_l', 'hand_l'), 1), 'joint-centre shoulder width', round(d('upperarm_l', 'upperarm_r'), 1), 'clavicle', round(d('clavicle_l', 'upperarm_l'), 1),
      'thigh', round(d('thigh_l', 'calf_l'), 1), 'shank', round(d('calf_l', 'foot_l'), 1), 'hip w', round(d('thigh_l', 'thigh_r'), 1), 'head z', round(H['head'].z * 100, 1), 'neck', round(d('neck_01', 'head'), 1))
V = [mesh.matrix_world @ v.co for v in mesh.data.vertices]
# surface widths: widest x extent of the mesh in thin z slabs (arms hang in A-pose, so use torso-only x at shoulder: verts with |x| < 0.30)
def width(z0, z1, xlim=9):
    xs = [v.x for v in V if z0 <= v.z < z1 and abs(v.x) < xlim]; return (max(xs) - min(xs)) * 100 if xs else 0
sz = H['upperarm_l'].z
print('RB acromial surface width (slab at shoulder joint z, |x|<0.26)', round(width(sz - 0.01, sz + 0.03, 0.26), 1), '| waist min width', round(min(width(z / 100, z / 100 + 0.02, 0.25) for z in range(100, 125, 2)), 1), '| hip max width', round(max(width(z / 100, z / 100 + 0.02, 0.30) for z in range(80, 100, 2)), 1), '| mesh z max', round(max(v.z for v in V) * 100, 1))
