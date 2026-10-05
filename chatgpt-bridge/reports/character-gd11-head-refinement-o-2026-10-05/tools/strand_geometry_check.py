import numpy as np, json, sys
for hd in sys.argv[1:]:
    d=np.load(hd+'/strands.npz'); M=d['main']; tg=np.array(json.load(open(hd+'/strand_tags.json'))['main'])
    seg=np.linalg.norm(np.diff(M,axis=1),axis=2); mx=seg.max(1)
    face=((M[...,1]>9.0)&(M[...,2]<166)&(np.abs(M[...,0]+0.23)<5.5)).any(1)
    print(hd.split('/')[-1], 'strands',len(M),'pts/strand',M.shape[1],'maxseg>3cm:',int((mx>3).sum()),'maxseg>6:',int((mx>6).sum()),'in-front-of-face strands:',int(face.sum()))
    for t in ('front_to_bun','side_to_bun','back_to_bun','top_to_bun','partcover'):
        m=np.array([x.startswith(t) for x in tg]); print('  ',t,int(m.sum()),'maxseg>3:',int((mx[m]>3).sum()),'face:',int(face[m].sum()), 'median maxseg %.2f'%np.median(mx[m]))
    bad=np.where((mx>3)|face)[0][:6]
    for i in bad: print('   ex',tg[i],np.round(M[i][[0,len(M[i])//2,-1]],1).tolist(), 'maxseg %.1f'%mx[i])
