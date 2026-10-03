import bpy, sys, json, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; tr = json.load(open(a[0])); out = {}
for tag, path in zip(a[1::2], a[2::2]):
    C = tr[tag]['curves']; im = bpy.data.images.load(path); Wd, Hd = im.size
    P = np.array(im.pixels[:]).reshape(Hd, Wd, 4)[::-1, :, :3]; L = P @ np.array([0.3, 0.59, 0.11])
    res = {}
    for s in 'lr':
        E = np.array(C['crv_eyelid_upper_'+s]+C['crv_eyelid_lower_'+s]); U = np.array(C['crv_eyelid_upper_'+s])
        cx = E[:, 0].mean(); cy = (E[:, 1].min()+E[:, 1].max())/2; top = U[:, 1].min(); w = E[:, 0].max()-E[:, 0].min()
        xs = slice(int(cx-0.15*w), int(cx+0.15*w)); prof = L[:, xs].mean(1)
        lo, hi = int(top-1.1*w), int(top-0.12*w); seg = prof[lo:hi]; seg = np.convolve(seg, np.ones(5)/5, 'same')
        by = lo+int(np.argmin(seg[3:-3]))+3
        res[s] = dict(eye_c=round(cy, 1), lid_top=round(float(top), 1), brow=by)
    el = tr[tag]['curves']; ipd = abs(np.array(el['crv_eyelid_upper_l']+el['crv_eyelid_lower_l'])[:, 0].mean()-np.array(el['crv_eyelid_upper_r']+el['crv_eyelid_lower_r'])[:, 0].mean())
    out[tag] = dict(ipd=round(float(ipd), 1), brow_to_eyecentre_ipd=round(float(np.mean([res[s]['eye_c']-res[s]['brow'] for s in 'lr']))/ipd, 3), brow_to_lidtop_ipd=round(float(np.mean([res[s]['lid_top']-res[s]['brow'] for s in 'lr']))/ipd, 3), raw=res)
print('BROWPROF', json.dumps(out))
