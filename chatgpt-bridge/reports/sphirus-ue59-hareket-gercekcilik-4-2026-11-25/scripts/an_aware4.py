# an_aware4.py <label> [wall_face_y]: near-surface awareness along the test wall (face at y = 2048 by default, path y = 2000).
# Path deviation (capsule y), awareness strength / torso yaw / head glance telemetry (ex indices 3..8), right hand and right shoulder
# clearance to the wall face, and shoulder-line yaw relative to the travel direction while beside the wall.
import json, sys, math
lab = sys.argv[1]; wy = float(sys.argv[2]) if len(sys.argv) > 2 else 2048.0
rows = json.load(open('Saved/Codex/Grip_20261106/rec/%s.json' % lab))['rows']
H = lambda r: r['hook'] if isinstance(r['hook'], dict) else {}
side = [r for r in rows if -5900 < r['x'] < -4500 and math.hypot(r['vx'], r['vy']) > 30]
def ex(r):
    e = H(r).get('ex'); return e if isinstance(e, list) and len(e) >= 9 else [0] * 9
sR = [ex(r)[4] for r in side]; ty = [ex(r)[7] for r in side]; hy = [ex(r)[8] for r in side]
ys = [r['y'] for r in side]
hand = [wy - r['v_hand_r'][1] for r in side]
sh = []
for r in side:
    d = H(r).get('sh', {}).get('d', {}) if isinstance(H(r).get('sh'), dict) else {}
    if 'clavicle_l' in d and 'clavicle_r' in d:
        a = math.degrees(math.atan2(d['clavicle_l'][1] - d['clavicle_r'][1], d['clavicle_l'][0] - d['clavicle_r'][0])); sh.append(a)
print('%s | beside wall %d frames | capsule y %.1f..%.1f (path 2000) | strength R max %.2f | torso yaw cmd %.1f..%.1f | head glance %.1f..%.1f | right hand to wall min %.1f cm p10 %.1f | shoulder line yaw %.1f..%.1f (mean %.1f)' % (
    lab, len(side), min(ys) if ys else 0, max(ys) if ys else 0, max(sR) if sR else 0, min(ty) if ty else 0, max(ty) if ty else 0, min(hy) if hy else 0, max(hy) if hy else 0,
    min(hand) if hand else 0, sorted(hand)[len(hand) // 10] if hand else 0, min(sh) if sh else 0, max(sh) if sh else 0, sum(sh) / len(sh) if sh else 0))
