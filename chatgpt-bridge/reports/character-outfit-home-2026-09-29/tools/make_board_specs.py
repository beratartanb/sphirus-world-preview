"""Build board specs from the capture set and render them with make_boards.ps1. usage: python make_board_specs.py"""
import json, subprocess, pathlib
R = pathlib.Path(__file__).resolve().parents[2]; C = R/'Saved/Codex/OutfitHome_20260929/captures'; B = R/'Saved/Codex/OutfitHome_20260929/boards'; B.mkdir(parents=True, exist_ok=True)
PS = R/'Tools/OutfitHome_20260929/make_boards.ps1'
def img(name, view): return f'{name}_{view}.png'
specs = {}
specs['board_neutral'] = {'title': 'HOME OUTFIT candidate | neutral | real materials, LOD0 | rows: outfit / body reference + clay', 'cell': 440, 'rows': [
    {'label': 'outfit', 'images': [img('of_neutral', v) for v in ['front', 'side', 'back', 'front3q', 'rear3q']], 'labels': ['outfit front', 'outfit side', 'outfit back', 'outfit front 3/4', 'outfit rear 3/4']},
    {'label': 'ref', 'images': [img('of_neutral_body', 'front'), img('of_neutral_body', 'side'), img('of_clay_neutral', 'front'), img('of_clay_neutral', 'rear3q'), img('of_clay_elev180', 'front')], 'labels': ['body only front', 'body only side', 'clay front', 'clay rear 3/4', 'clay 180']}]}
cu = ['neckline', 'chest', 'shoulder_armpit', 'waist_tuck', 'waistband_drawstring', 'crotch_hip', 'knee_folds', 'hem', 'back_waist', 'sleeve_elbow', 'seat', 'side_hip']
specs['board_closeups'] = {'title': 'HOME OUTFIT candidate | close-ups (neutral, LOD0)', 'cell': 420, 'rows': [
    {'label': 'cu', 'images': [img('of_cu_'+k, 'custom') for k in cu[:6]], 'labels': cu[:6]}, {'label': 'cu', 'images': [img('of_cu_'+k, 'custom') for k in cu[6:]], 'labels': cu[6:]}]}
DEF = ['neutral', 'armsfwd', 'elev150', 'elev165', 'elev180', 'twist', 'crouch', 'squat', 'elbow', 'hipflex', 'backext', 'internal90', 'external90']
for bi, chunk in enumerate([DEF[:5], DEF[5:9], DEF[9:]]):
    specs[f'board_deform_{bi+1}'] = {'title': f'HOME OUTFIT candidate | deformation {bi+1}/3 | front / side / rear 3/4 (real materials, LOD0)', 'cell': 400,
                                     'rows': [{'label': p, 'images': [img('of_dfm_'+p, v) for v in ['front', 'side', 'rear3q']], 'labels': [f'{p} {v}' for v in ['front', 'side', 'rear 3/4']]} for p in chunk]}
specs['board_gameplay'] = {'title': 'HOME OUTFIT candidate | gameplay poses | front / side / rear 3/4', 'cell': 400,
                           'rows': [{'label': p, 'images': [img('of_gp_'+p, v) for v in ['front', 'side', 'rear3q']], 'labels': [f'{p} {v}' for v in ['front', 'side', 'rear 3/4']]} for p in ['idle', 'walk', 'jog', 'sprint', 'jump']]}
specs['board_shcb'] = {'title': 'HOME OUTFIT candidate | SHCB high elevation 150 / 165 / 180 | outfit vs clay', 'cell': 420, 'rows': [
    {'label': 'outfit', 'images': [img('of_dfm_elev150', 'front'), img('of_dfm_elev165', 'front'), img('of_dfm_elev180', 'front'), img('of_dfm_elev180', 'rear3q'), img('of_dfm_elev180', 'side')], 'labels': ['150 front', '165 front', '180 front', '180 rear 3/4', '180 side']},
    {'label': 'clay', 'images': [img('of_clay_elev180', 'front'), img('of_clay_elev180', 'rear3q'), img('of_clay_squat', 'front'), img('of_clay_squat', 'rear3q'), img('of_dfm_squat', 'side')], 'labels': ['clay 180 front', 'clay 180 rear 3/4', 'clay squat front', 'clay squat rear 3/4', 'squat side']}]}
specs['board_lods'] = {'title': 'HOME OUTFIT candidate | LOD0 / LOD1 / LOD2 | neutral, walk, deep squat, 180', 'cell': 400, 'rows': [
    {'label': 'LOD0', 'images': [img('of_dfm_neutral', 'front'), img('of_gp_walk', 'front'), img('of_dfm_squat', 'front'), img('of_dfm_elev180', 'front')], 'labels': ['LOD0 neutral', 'LOD0 walk', 'LOD0 squat', 'LOD0 180']},
    {'label': 'LOD1', 'images': [img('of_lod1_'+p, 'front') for p in ['neutral', 'walk', 'squat', 'elev180']], 'labels': ['LOD1 neutral', 'LOD1 walk', 'LOD1 squat', 'LOD1 180']},
    {'label': 'LOD2', 'images': [img('of_lod2_'+p, 'front') for p in ['neutral', 'walk', 'squat', 'elev180']], 'labels': ['LOD2 neutral', 'LOD2 walk', 'LOD2 squat', 'LOD2 180']}]}
for name, spec in specs.items():
    spec['ncol'] = max(len(r['images']) for r in spec['rows']); spec['nrows'] = len(spec['rows'])
    sp = B/(name+'.json'); sp.write_text(json.dumps(spec)); out = B/(name+'.jpg')
    r = subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', str(PS), '-spec', str(sp), '-captures', str(C), '-out', str(out)], capture_output=True, text=True, encoding='utf-8', errors='ignore')
    print(name, (r.stdout or '').strip()[-60:], (r.stderr or '').strip()[-200:])
