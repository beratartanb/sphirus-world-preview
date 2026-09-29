"""Return path, step 1 (Blender side, read-only): ARTIST_SCULPT -> BR_ArtistNeutral morph deltas (UE bind space, cm).
Refuses to export unless validate_sculpt.py reports no FAIL. Deltas are relative to ACCEPTED_B2 (full realism layer,
replacing BR_Neutral in its own isolated asset set); seam pairs must be identical; head identity region must be 0.
blender -b <sculpt.blend> --python export_artist_delta.py -- <package> <validator> <out.json>"""
import bpy, sys, json, hashlib
import numpy as np
a = sys.argv[sys.argv.index('--')+1:]; PKG, VAL, OUT = a
g = {'__name__': 'v'}; exec(compile(open(VAL).read(), VAL, 'exec'), g); P = g['load_pkg'](PKG)
R = g['validate'](P); print(g['summary'](R))
if R['overall'] == 'FAIL': raise SystemExit('EXPORT REFUSED: validation FAIL')
ob = bpy.data.objects['SPH_BR_ArtistSculpt']; NB, NH = P['NB'], P['NH']
def kco(n):
    c = np.zeros((NB+NH)*3, np.float32); ob.data.shape_keys.key_blocks[n].data.foreach_get('co', c); return c.astype(np.float64)
D = g['to_ue'](kco('ARTIST_SCULPT')-kco('ACCEPTED_B2'))  # key-to-key: float32 storage noise cancels on unmoved vertices
for b, h in P['weld_pairs']:  # seam twins must carry identical deltas (as in the BR bake); SEAM_LOCK keeps both ~0
    assert np.abs(D[b]-D[h]).max() < 1e-4, ('seam pair mismatch', b, h, D[b], D[h]); D[h] = D[b]
out = {'Body': {'BR_ArtistNeutral': {}}, 'Head': {'BR_ArtistNeutral': {}}}
for u in range(NB+NH):
    if np.abs(D[u]).max() < 1e-5: continue
    part, vid = ('Body', u) if u < NB else ('Head', u-NB)
    out[part]['BR_ArtistNeutral'][str(vid)] = [float(x) for x in D[u]]
fq = [u for u in range(NB, NB+NH) if P['accepted_b2'][u][2] > 149.0]
assert float(np.abs(D[fq]).max()) == 0.0, 'face identity region moved'
out['_meta'] = {'source_blend': bpy.data.filepath, 'validation': R['overall'], 'package': P['version'],
                'blend_sha256': hashlib.sha256(open(bpy.data.filepath, 'rb').read()).hexdigest(),
                'body_verts_moved': len(out['Body']['BR_ArtistNeutral']), 'head_verts_moved': len(out['Head']['BR_ArtistNeutral'])}
open(OUT, 'w').write(json.dumps(out)); print('EXPORT_OK', out['_meta'])
