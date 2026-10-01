"""GUARDIAN-3: joint comparison P (old DNA, archetype joints + BR_Neutral surface) vs NEW (auto-rigged DNA). usage: python gd3_joint_report.py <dump json> <A> <B> <out json>"""
import json, sys, math
D = json.load(open(sys.argv[1])); A, B = D[sys.argv[2]], D[sys.argv[3]]; out = {}
keys = ['FACIAL_L_Eye', 'FACIAL_R_Eye', 'FACIAL_L_EyelidUpperA', 'FACIAL_R_EyelidUpperA', 'FACIAL_L_EyelidLowerA', 'FACIAL_R_EyelidLowerA', 'FACIAL_C_Jaw', 'FACIAL_C_TeethUpper', 'FACIAL_C_TeethLower',
        'FACIAL_C_Nose', 'FACIAL_C_NoseTip', 'FACIAL_L_Nostril', 'FACIAL_R_Nostril', 'FACIAL_L_LipCorner', 'FACIAL_R_LipCorner', 'FACIAL_C_MouthUpper', 'FACIAL_C_MouthLower', 'FACIAL_L_CheekOuter', 'FACIAL_R_CheekOuter',
        'FACIAL_C_Forehead', 'FACIAL_L_ForeheadIn', 'FACIAL_R_ForeheadIn', 'FACIAL_C_Chin', 'head', 'neck_02', 'neck_01']
d = lambda p, q: math.dist(p, q)
for k in keys:
    if k in A and k in B: out[k] = {'P': A[k], 'NEW': B[k], 'delta_cm': [round(b-a, 3) for a, b in zip(A[k], B[k])], 'dist_cm': round(d(A[k], B[k]), 3)}
def ipd(J): return d(J['FACIAL_L_Eye'], J['FACIAL_R_Eye'])
mid = lambda J: [(a+b)/2 for a, b in zip(J['FACIAL_L_Eye'], J['FACIAL_R_Eye'])]
S = {}
for lab, J in (('P', A), ('NEW', B)):
    em = mid(J); S[lab] = {'eye_joint_distance_cm': round(ipd(J), 3), 'eye_centre_z': round(em[2], 3), 'eye_centre_y': round(em[1], 3),
        'eye_to_nosetip_z_cm': round(em[2]-J['FACIAL_C_NoseTip'][2], 3) if 'FACIAL_C_NoseTip' in J else None,
        'eye_to_mouth_z_cm': round(em[2]-(J['FACIAL_L_LipCorner'][2]+J['FACIAL_R_LipCorner'][2])/2, 3), 'mouth_corner_width_cm': round(d(J['FACIAL_L_LipCorner'], J['FACIAL_R_LipCorner']), 3),
        'jaw_joint': J['FACIAL_C_Jaw'], 'eye_to_jaw_z_cm': round(em[2]-J['FACIAL_C_Jaw'][2], 3)}
    if 'FACIAL_L_CheekOuter' in J: S[lab]['cheek_outer_width_cm'] = round(d(J['FACIAL_L_CheekOuter'], J['FACIAL_R_CheekOuter']), 3)
out['_summary'] = S; out['_all_moved_gt_1mm'] = sum(1 for k in A if k in B and k.startswith('FACIAL') and d(A[k], B[k]) > 0.1); out['_n_facial'] = sum(1 for k in A if k.startswith('FACIAL'))
json.dump(out, open(sys.argv[4], 'w'), indent=1); print(json.dumps(S, indent=1)); print('moved>1mm', out['_all_moved_gt_1mm'], '/', out['_n_facial'])
