"""Final revision boards (aspect-preserving). usage: python make_rv_boards_final.py [prefix=fz]"""
import json, subprocess, pathlib, sys
R = pathlib.Path(__file__).resolve().parents[2]; E = R/'Saved/Codex/CharacterRevision_20260930'; C = E/'captures'; B = E/'boards'; B.mkdir(exist_ok=True)
PS = R/'Tools/CharacterRevision_20260930/make_boards_fit.ps1'; P = sys.argv[1] if len(sys.argv) > 1 else 'fz'
def row(imgs, labels): return {'images': imgs, 'labels': labels}
specs = {}
V5 = ['front', 'side', 'back', 'front3q', 'rear3q']
specs['rv_01_final_views'] = ('FINAL CANDIDATE | body v6 + soft-tissue correctives + Henley V3i + lounge shorts + custom low-bun groom v12 | neutral, real materials, LOD0', 420,
    [row([f'{P}_final_{v}.png' for v in V5]+['ref_full_front.png'], V5+['concept (reference)']),
     row([f'{P}_clay_front.png', f'{P}_clay_rear3q.png', f'{P}_cu_foot_ankle_custom.png', f'{P}_cu_hand_custom.png', f'{P}_cu_back_waist_custom.png', 'ref_full_3q.png'], ['clay front', 'clay rear 3/4', 'foot / ankle', 'hand', 'back waist', 'concept 3/4 (reference)'])])
specs['rv_02_hair_reference'] = ('HAIR REFERENCE MATCH | top: approved concept | below: custom groom (Blender strands -> Alembic -> UE Groom, bound to the MetaHuman face)', 420,
    [row(['ref_hair_front.png', 'ref_hair_3q.png', 'ref_hair_close.png', 'ref_hair_close.png'], ['concept front', 'concept 3/4', 'concept close 3/4', 'concept close 3/4']),
     row([f'{P}_head_front_custom.png', f'{P}_head_front3q_custom.png', f'{P}_head_side_r_custom.png', f'{P}_head_side_custom.png'], ['groom front', 'groom front 3/4', 'groom side (r)', 'groom side (l)']),
     row([f'{P}_head_back_custom.png', f'{P}_head_rear3q_custom.png', f'{P}_final_front.png', f'{P}_final_rear3q.png'], ['groom back (bun)', 'groom rear 3/4', 'full front', 'full rear 3/4'])])
specs['rv_03_shorts_reference'] = ('SHORTS REFERENCE MATCH | top: approved concept | below: new lounge-short pattern (Blender construction + drape)', 420,
    [row(['ref_shorts_front.png', 'ref_shorts_3q.png', 'ref_full_front.png'], ['concept front', 'concept 3/4', 'concept full']),
     row([f'{P}_cu_crotch_custom.png', f'{P}_cu_thigh_opening_custom.png', f'{P}_final_front.png'], ['shorts front (crotch / hem)', 'shorts 3/4 (thigh opening)', 'full front']),
     row([f'{P}_cu_side_hip_custom.png', f'{P}_cu_seat_custom.png', f'{P}_cu_waistband_drawstring_custom.png'], ['side hip / curved hem', 'seat', 'waistband / drawstring'])])
specs['rv_04_henley_neckline'] = ('HENLEY NECKLINE / PLACKET (static) | concept vs candidate', 420,
    [row(['ref_neck_close.png', f'{P}_cu_neckline_custom.png', f'{P}_cu_clavicle_chest_custom.png', f'{P}_cu_henley_chest_custom.png'], ['concept neckline', 'neckline / placket', 'clavicle / upper sternum', 'Henley chest 3/4']),
     row([f'{P}_cu_shoulder_armpit_custom.png', f'{P}_cu_sleeve_elbow_custom.png', f'{P}_cu_waist_hem_custom.png', f'{P}_head_front3q_custom.png'], ['shoulder / armpit', 'sleeve / elbow', 'waist / hem', 'neck framing'])])
NECK = ['neutral', 'pl_bend20', 'pl_bend30', 'pl_bend45', 'pl_bend60', 'pl_bend90']
specs['rv_05_dynamic_neckline'] = ('DYNAMIC HENLEY NECKLINE | forward bend 0 / 20 / 30 / 45 / 60 / 90 deg | chest-tracking close-ups (front, side, front 3/4) + full side', 360,
    [row([f'{P}_{p}_chest_front_custom.png', f'{P}_{p}_chest_side_custom.png', f'{P}_{p}_chest_front3q_custom.png', f'{P}_{p}_side.png'], [f'{p} chest front', f'{p} chest side', f'{p} chest 3/4', f'{p} full side']) for p in NECK])
BR = ['neutral', 'pl_bend30', 'pl_bend60', 'pl_bend90', 'armsfwd', 'elev180', 'pl_twist_l']
specs['rv_06_breast_softtissue'] = ('BREAST / CHEST SOFT TISSUE (clay, body only, same cameras) | BEFORE = skinning + SHCB (RV soft-tissue morphs zeroed) | AFTER = + RV pose-space soft-tissue correctives', 330,
    [row([f'{P}cb_{p}_chest_side_custom.png', f'{P}c_{p}_chest_side_custom.png', f'{P}cb_{p}_chest_front3q_custom.png', f'{P}c_{p}_chest_front3q_custom.png', f'{P}cb_{p}_chest_front_custom.png', f'{P}c_{p}_chest_front_custom.png'],
         [f'{p} side BEFORE', f'{p} side AFTER', f'{p} 3/4 BEFORE', f'{p} 3/4 AFTER', f'{p} front BEFORE', f'{p} front AFTER']) for p in BR])
LOW = ['neutral', 'squat', 'hipflex', 'pl_twist_r', 'pl_bend90']
specs['rv_07_lower_softtissue'] = ('ABDOMEN / GLUTE / THIGH SOFT TISSUE (clay, same cameras) | BEFORE vs AFTER', 330,
    [row([f'{P}cb_{p}_hip_side_custom.png', f'{P}c_{p}_hip_side_custom.png', f'{P}cb_{p}_hip_rear3q_custom.png', f'{P}c_{p}_hip_rear3q_custom.png', f'{P}cb_{p}_hip_front3q_custom.png', f'{P}c_{p}_hip_front3q_custom.png'],
         [f'{p} side BEFORE', f'{p} side AFTER', f'{p} rear 3/4 BEFORE', f'{p} rear 3/4 AFTER', f'{p} front 3/4 BEFORE', f'{p} front 3/4 AFTER']) for p in LOW])
DF = ['neutral', 'armsfwd', 'elev90', 'elev120', 'elev150', 'elev165', 'elev180', 'pl_twist_l', 'pl_twist_r', 'elbow', 'backext', 'pl_bend30', 'pl_bend45', 'pl_bend60', 'pl_bend90', 'crouch', 'squat', 'hipflex', 'pl_highknee_l', 'pl_stride']
for bi, chunk in enumerate([DF[0:7], DF[7:14], DF[14:20]]):
    specs[f'rv_08_deformation_{bi+1}'] = (f'DEFORMATION {bi+1}/3 | body + Henley + shorts | front / side / rear 3/4 (real materials, LOD0)', 330,
        [row([f'{P}_dfm_{p}_{v}.png' for v in ['front', 'side', 'rear3q']], [f'{p} {v}' for v in ['front', 'side', 'rear 3/4']]) for p in chunk])
specs['rv_09_shcb'] = ('SHCB HIGH ELEVATION 90 / 120 / 150 / 165 / 180 | Henley underarm (garment correctives driven by RV_Arm curves; SHCB untouched)', 330,
    [row([f'{P}_dfm_{p}_{v}.png' for p in ['elev90', 'elev120', 'elev150', 'elev165', 'elev180']], [f'{p} {v}' for p in ['90', '120', '150', '165', '180']]) for v in ['front', 'side', 'rear3q']])
GP = ['idle', 'walk', 'jog', 'sprint', 'jump', 'crouch']
specs['rv_10_gameplay'] = ('GAMEPLAY POSES | front / side / rear 3/4 + third-person camera', 330,
    [row([f'{P}_gp_{p}_{v}.png' for v in ['front', 'side', 'rear3q']]+[f'{P}_gpcam_{p}_custom.png'], [f'{p} {v}' for v in ['front', 'side', 'rear 3/4', 'gameplay cam']]) for p in GP])
specs['rv_11_lods'] = ('LOD0 / LOD1 / LOD2 (topology-aware garment LODs) | neutral, walk, deep squat, 180, bend 60 | front + rear 3/4', 300,
    [row([f'{P}_lod{L}_{p}_{v}.png' for p in ['neutral', 'walk', 'squat', 'elev180', 'pl_bend60'] for v in ['front']]+[f'{P}_lod{L}_squat_rear3q.png'], [f'LOD{L} {p}' for p in ['neutral', 'walk', 'squat', '180', 'bend60']]+[f'LOD{L} squat rear']) for L in (0, 1, 2)])
HS = ['idle', 'walk', 'jog', 'sprint', 'crouch', 'jump', 'pl_twist_l', 'pl_bend45']
specs['rv_12_hair_poses'] = ('HAIR PER POSE | front 3/4, rear 3/4, side | clipping / framing check (still frames)', 300,
    [row([f'{P}_{p}_{k}_custom.png' for k in ['front3q', 'rear3q', 'side']], [f'{p} {k}' for k in ['front 3/4', 'rear 3/4', 'side']]) for p in HS])
HM = json.loads((C/'hm_results.json').read_text()) if (C/'hm_results.json').exists() else {'frames': []}
segs = []
for f in HM['frames']:
    if f['seg'] not in segs: segs.append(f['seg'])
hrows = []
for sg in segs:
    fr = [f for f in HM['frames'] if f['seg'] == sg]; pick = [fr[int(round(k*(len(fr)-1)/5))] for k in range(6)] if len(fr) >= 6 else fr
    hrows.append(row([f['img'] for f in pick], [f"{sg} t={f['t']:.1f}s" for f in pick]))
if hrows: specs['rv_13_hair_motion'] = ('HAIR MOTION (editor world, real-time, loose-strand simulation) | in-place animation + body yaw / bend / twist scrub | head-tracking rear 3/4 camera', 260, hrows)
for name, (title, cell, rows) in specs.items():
    spec = {'title': title, 'cell': cell, 'ncol': max(len(r['images']) for r in rows), 'nrows': len(rows), 'rows': rows}
    sp = B/(name+'.json'); sp.write_text(json.dumps(spec), encoding='utf-8'); out = B/(name+'.jpg')
    r = subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', str(PS), '-spec', str(sp), '-captures', str(C), '-out', str(out)], capture_output=True, text=True, encoding='utf-8', errors='ignore')
    print(name, (r.stdout or '').strip()[-30:], (r.stderr or '').strip()[-150:])
