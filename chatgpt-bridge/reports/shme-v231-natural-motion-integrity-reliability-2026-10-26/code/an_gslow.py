import json,sys
t=open(sys.argv[1],encoding='utf8',errors='replace').read()
i=t.find(sys.argv[2]+' ')
if i<0: print(t[-3000:]); raise SystemExit
d=json.loads(t[i+len(sys.argv[2])+1:].split('\n')[0])
for n,v in d['clips'].items():
    if v.get('err'): print(n, v['err'][-600:]); continue
    print(n.split('_',2)[-1], v['B'], v.get('s_planted0'), 'tB',v.get('tB'),'tC',v.get('tC'),'tz',v.get('tz'),'tS',v.get('tS',v.get('tF')),'len',v['len'],'ferr',v['foot_err'],'drift',v['planted_drift'],'pen',v['penetration'],'in',v['entry_err'],'out',v['exit_err'],'dip',v['pelvis_min_minus_final'],'steps',v['steps'][:5])
