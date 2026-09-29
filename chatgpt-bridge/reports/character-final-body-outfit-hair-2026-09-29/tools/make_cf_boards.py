"""Board specs for the CharacterFinal captures -> Tools/OutfitHome_20260929/make_boards.ps1.
usage: python make_cf_boards.py <board_set> [prefix]   sets: audit | audit_ab (prefixA,prefixB) | final | deform | gameplay | lods | hair | closeups"""
import json, subprocess, pathlib, sys
R = pathlib.Path(__file__).resolve().parents[2]; C = R/'Saved/Codex/CharacterFinal_20260929/captures'; B = R/'Saved/Codex/CharacterFinal_20260929/boards'; B.mkdir(parents=True, exist_ok=True)
PS = R/'Tools/OutfitHome_20260929/make_boards.ps1'
which = sys.argv[1] if len(sys.argv) > 1 else 'audit'; args = sys.argv[2:]
def img(name, view): return f'{name}_{view}.png'
V5 = ['front', 'side', 'back', 'front3q', 'rear3q']
CU_A = ['neck_clavicle', 'chest_ribcage', 'chest_3q', 'abdomen_waist', 'waist_side', 'pelvis_hip', 'hip_3q']
CU_B = ['glutes_rear', 'glutes_3q', 'thigh_knee', 'knee_side', 'calf_ankle', 'calf_side', 'back_upper']
CU_C = ['back_lower', 'shoulder_arm', 'arm_side', 'hand_l', 'hand_dorsal', 'feet_front', 'feet_side', 'feet_3q', 'feet_medial']
GZ = ['chest_3q', 'abdomen_waist', 'glutes_3q', 'thigh_knee', 'feet_3q', 'back_upper']
specs = {}
if which == 'audit':
    P = args[0] if args else 'a5'; T = args[1] if len(args) > 1 else P
    specs[f'{P}_audit_full'] = {'title': f'BODY AUDIT {T} | clay neutral | 5 views + grazing', 'cell': 420, 'rows': [
        {'label': 'neutral', 'images': [img(f'{P}_body', v) for v in V5], 'labels': V5}, {'label': 'grazing', 'images': [img(f'{P}_bodyg', v) for v in ['front', 'back', 'side']]+[img(f'{P}_skin', 'front'), img(f'{P}_skin', 'back')], 'labels': ['grazing front', 'grazing back', 'grazing side', 'skin front', 'skin back']}]}
    for k, cu in (('a', CU_A), ('b', CU_B), ('c', CU_C)):
        specs[f'{P}_audit_cu_{k}'] = {'title': f'BODY AUDIT {T} | close-ups {k} (clay)', 'cell': 400, 'rows': [{'label': 'cu', 'images': [img(f'{P}_cu_'+c, 'custom') for c in cu], 'labels': cu}]}
    specs[f'{P}_audit_grazing'] = {'title': f'BODY AUDIT {T} | grazing-light close-ups + skin close-ups', 'cell': 400, 'rows': [
        {'label': 'gz', 'images': [img(f'{P}_cug_'+c, 'custom') for c in GZ], 'labels': ['grazing '+c for c in GZ]},
        {'label': 'skin', 'images': [img(f'{P}_skincu_'+c, 'custom') for c in ['chest_3q', 'back_upper', 'feet_3q', 'knee_side', 'hand_l']], 'labels': ['skin '+c for c in ['chest_3q', 'back_upper', 'feet_3q', 'knee_side', 'hand_l']]}]}
elif which == 'audit_ab':
    A, Bp = args[0], args[1]; LA, LB = (args[2], args[3]) if len(args) > 3 else (A, Bp)
    specs[f'ab_{A}_{Bp}_full'] = {'title': f'BODY A/B | rows: {LA} / {LB} | clay, same cameras', 'cell': 420, 'rows': [
        {'label': LA, 'images': [img(f'{A}_body', v) for v in V5], 'labels': [f'{LA} {v}' for v in V5]}, {'label': LB, 'images': [img(f'{Bp}_body', v) for v in V5], 'labels': [f'{LB} {v}' for v in V5]}]}
    for k, cu in (('a', CU_A), ('b', CU_B), ('c', CU_C)):
        specs[f'ab_{A}_{Bp}_cu_{k}'] = {'title': f'BODY A/B close-ups {k} | rows: {LA} / {LB}', 'cell': 400, 'rows': [
            {'label': LA, 'images': [img(f'{A}_cu_'+c, 'custom') for c in cu], 'labels': [f'{LA} {c}' for c in cu]}, {'label': LB, 'images': [img(f'{Bp}_cu_'+c, 'custom') for c in cu], 'labels': [f'{LB} {c}' for c in cu]}]}
    specs[f'ab_{A}_{Bp}_grazing'] = {'title': f'BODY A/B grazing close-ups | rows: {LA} / {LB}', 'cell': 400, 'rows': [
        {'label': LA, 'images': [img(f'{A}_cug_'+c, 'custom') for c in GZ], 'labels': [f'{LA} {c}' for c in GZ]}, {'label': LB, 'images': [img(f'{Bp}_cug_'+c, 'custom') for c in GZ], 'labels': [f'{LB} {c}' for c in GZ]}]}
elif which == 'body_dfm':
    P = args[0] if args else 'cf'; DEFB = ['neutral', 'armsfwd', 'elev90', 'elev120', 'elev150', 'elev165', 'elev180', 'twist', 'hipflex', 'backext', 'crouch', 'squat', 'sprint', 'elbow', 'forward90']
    for bi, chunk in enumerate([DEFB[:5], DEFB[5:10], DEFB[10:]]):
        specs[f'{P}_body_dfm_{bi+1}'] = {'title': f'BODY DEFORMATION {P} {bi+1}/3 | clay | front / side / rear 3/4', 'cell': 400, 'rows': [{'label': p, 'images': [img(f'{P}_bdfm_'+p, v) for v in ['front', 'side', 'rear3q']], 'labels': [f'{p} {v}' for v in ['front', 'side', 'rear 3/4']]} for p in chunk]}
else:
    P = args[0] if args else 'cf'
    if which == 'final':
        specs[f'{P}_final_neutral'] = {'title': f'FINAL CHARACTER {P} | body + Henley + shorts + hair | neutral, real materials, LOD0', 'cell': 440, 'rows': [
            {'label': 'final', 'images': [img(f'{P}_neutral', v) for v in V5], 'labels': V5}, {'label': 'clay', 'images': [img(f'{P}_clay_neutral', 'front'), img(f'{P}_clay_neutral', 'rear3q'), img(f'{P}_clay_elev180', 'front'), img(f'{P}_clay_squat', 'front'), img(f'{P}_clay_squat', 'rear3q')], 'labels': ['clay front', 'clay rear 3/4', 'clay 180', 'clay squat', 'clay squat rear 3/4']}]}
    if which in ('final', 'closeups'):
        CU = ['hair_face', 'hair_3q', 'hair_rear', 'hair_side', 'neckline', 'clavicle_chest', 'henley_chest', 'waist_hem', 'waist_hem_side', 'waistband_drawstring', 'side_hip', 'seat', 'seat_3q', 'crotch', 'short_hem', 'thigh_opening', 'foot_ankle', 'shoulder_armpit', 'sleeve_elbow', 'back_waist']
        specs[f'{P}_closeups'] = {'title': f'FINAL CHARACTER {P} | close-ups (neutral, LOD0)', 'cell': 400, 'rows': [{'label': 'cu', 'images': [img(f'{P}_cu_'+k, 'custom') for k in CU[i:i+5]], 'labels': CU[i:i+5]} for i in range(0, len(CU), 5)]}
    if which in ('final', 'deform'):
        DEF = ['neutral', 'armsfwd', 'elev90', 'elev120', 'elev150', 'elev165', 'elev180', 'twist', 'crouch', 'squat', 'elbow', 'hipflex', 'backext', 'internal90', 'external90']
        for bi, chunk in enumerate([DEF[:5], DEF[5:10], DEF[10:]]):
            specs[f'{P}_deform_{bi+1}'] = {'title': f'FINAL CHARACTER {P} | deformation {bi+1}/3 | front / side / rear 3/4', 'cell': 400, 'rows': [{'label': p, 'images': [img(f'{P}_dfm_'+p, v) for v in ['front', 'side', 'rear3q']], 'labels': [f'{p} {v}' for v in ['front', 'side', 'rear 3/4']]} for p in chunk]}
    if which in ('final', 'gameplay'):
        GP = ['idle', 'walk', 'jog', 'sprint', 'crouch', 'jump']
        specs[f'{P}_gameplay'] = {'title': f'FINAL CHARACTER {P} | gameplay poses | front / side / rear 3/4 + third-person camera', 'cell': 400, 'rows': [{'label': p, 'images': [img(f'{P}_gp_'+p, v) for v in ['front', 'side', 'rear3q']]+[img(f'{P}_gpcam_'+p, 'custom')], 'labels': [f'{p} {v}' for v in ['front', 'side', 'rear 3/4', 'gameplay cam']]} for p in GP]}
    if which in ('final', 'lods'):
        specs[f'{P}_lods'] = {'title': f'FINAL CHARACTER {P} | LOD0 / LOD1 / LOD2 | neutral, walk, squat, 180 (+ rear 3/4 neutral, squat)', 'cell': 400, 'rows': [
            {'label': 'LOD0', 'images': [img(f'{P}_dfm_neutral', 'front'), img(f'{P}_gp_walk', 'front'), img(f'{P}_dfm_squat', 'front'), img(f'{P}_dfm_elev180', 'front'), img(f'{P}_dfm_neutral', 'rear3q'), img(f'{P}_dfm_squat', 'rear3q')], 'labels': ['LOD0 neutral', 'LOD0 walk', 'LOD0 squat', 'LOD0 180', 'LOD0 neutral rear', 'LOD0 squat rear']}] +
            [{'label': f'LOD{L}', 'images': [img(f'{P}_lod{L}_'+p, 'front') for p in ['neutral', 'walk', 'squat', 'elev180']]+[img(f'{P}_lod{L}_neutral', 'rear3q'), img(f'{P}_lod{L}_squat', 'rear3q')], 'labels': [f'LOD{L} {p}' for p in ['neutral', 'walk', 'squat', '180', 'neutral rear', 'squat rear']]} for L in (1, 2)]}
    if which in ('final', 'hair'):
        HP = ['neutral', 'idle', 'walk', 'sprint', 'crouch', 'twist']
        specs[f'{P}_hair'] = {'title': f'FINAL CHARACTER {P} | hair | front / side / rear 3/4 per pose + close-ups', 'cell': 400, 'rows': [{'label': p, 'images': [img(f'{P}_hair_'+p, v) for v in ['front', 'side', 'rear3q']], 'labels': [f'hair {p} {v}' for v in ['front', 'side', 'rear 3/4']]} for p in HP] +
                                  [{'label': 'cu', 'images': [img(f'{P}_haircu_'+k, 'custom') for k in ['hair_face', 'hair_3q', 'hair_rear', 'hair_side']], 'labels': ['hair face', 'hair 3/4', 'hair rear', 'hair side']}]}
for name, spec in specs.items():
    spec['ncol'] = max(len(r['images']) for r in spec['rows']); spec['nrows'] = len(spec['rows'])
    sp = B/(name+'.json'); sp.write_text(json.dumps(spec)); out = B/(name+'.jpg')
    r = subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', str(PS), '-spec', str(sp), '-captures', str(C), '-out', str(out)], capture_output=True, text=True, encoding='utf-8', errors='ignore')
    print(name, (r.stdout or '').strip()[-60:], (r.stderr or '').strip()[-200:])
