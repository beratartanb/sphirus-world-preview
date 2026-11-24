import json,sys
# fallz.py <label>... : visible hand / head / pelvis height above the floor through the fall (state changes + every 0.25 s)
for lab in sys.argv[1:]:
    rows=json.load(open('Saved/Codex/Grip_20261106/rec/%s.json'%lab))['rows']; z0=min(min(r['v_foot_l'][2],r['v_foot_r'][2]) for r in rows[:30])-9.4+9.4
    fl=rows[0]['z']-92; print('==',lab); nt=0
    for r in rows:
        if r['t']<2.9 or r['t']>8.3: continue
        if r['t']>=nt:
            nt=r['t']+0.25; g=lambda k: r[k][2]-fl
            print('  %.2f handL %5.1f handR %5.1f head %5.1f pelvis %5.1f footL %5.1f footR %5.1f | %s'%(r['t'],g('v_hand_l'),g('v_hand_r'),g('v_head'),g('v_pelvis'),g('v_foot_l'),g('v_foot_r'),r['gasp'][0][-28:] if not r.get('mont') else str(r['mont'])[-40:]))
