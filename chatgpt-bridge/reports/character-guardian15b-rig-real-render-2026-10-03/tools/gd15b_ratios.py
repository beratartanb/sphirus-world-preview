import json, sys
def m(C):
    e={}
    for s in 'lr':
        P=C['crv_eyelid_upper_'+s]+C['crv_eyelid_lower_'+s]; xs=[p[0] for p in P]; ys=[p[1] for p in P]; e[s]=((min(xs)+max(xs))/2,(min(ys)+max(ys))/2,max(xs)-min(xs),max(ys)-min(ys))
    ipd=abs(e['l'][0]-e['r'][0]); ey=(e['l'][1]+e['r'][1])/2; nl=C['crv_nasolabial_l']; nr=C['crv_nasolabial_r']; al=(nl[0][1]+nr[0][1])/2
    L=[p for k in C if k.startswith('crv_lip') for p in C[k]]; xs=[p[0] for p in L]
    U=C['crv_lip_upper_inner_l']+C['crv_lip_upper_inner_r']; st=sum(p[1] for p in U)/len(U); inner=abs((e['l'][0]-e['l'][2]/2)-(e['r'][0]+e['r'][2]/2))
    return dict(ipd_px=round(ipd,1), mouth_ipd=round((max(xs)-min(xs))/ipd,3), eye_stomion_ipd=round((st-ey)/ipd,3), eye_alarbase_ipd=round((al-ey)/ipd,3), inner_canthal_ipd=round(inner/ipd,3), eye_open=round(((e['l'][3]+e['r'][3])/2)/((e['l'][2]+e['r'][2])/2),3))
r=json.load(open(sys.argv[1])); out={k: m(v['curves']) for k, v in r.items() if v.get('curves')}
json.dump(out, open(sys.argv[2], 'w'), indent=1); [print(k, v) for k, v in out.items()]
