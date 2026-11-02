"""authdrift_req.py (measure job): authored planted-foot motion of the turning-start copies, in the clip's own root-motion frame, so the
in-game contact231 DRAG numbers (ball drift while in contact) can be compared with what the clip itself authors (a heel pivot moves the
ball). Per clip: per 1/30 s, ball_l / ball_r component-space xy (root motion included) and z; reports the ball displacement of the foot
that stays low during the first 0.6 s and the root planar path."""
import unreal as u, json, math, sys, importlib
sys.path.insert(0, r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925')
import v137_animedit as ae; importlib.reload(ae)
J = '/Game/GraceRanger/SHME/Animations/Starts/Jog/SHM_JogQ_af_Loco_Jog_Start_Turn%s%s_%sfoot_AAMS'
out = {}
for s, d in (('L', '135'), ('L', '180'), ('R', '135')):
    seq = u.load_asset(J % (s, d, s)); c = ae.Clip(seq, ['root', 'ball_l', 'ball_r', 'foot_l', 'foot_r'])
    n = min(c.nf, 24); rows = []
    for f in range(n):
        r = c.comp('root', f)[0]; bl = c.comp('ball_l', f)[0]; br = c.comp('ball_r', f)[0]
        rows.append([round(r[0], 1), round(r[1], 1), round(bl[0], 1), round(bl[1], 1), round(bl[2], 1), round(br[0], 1), round(br[1], 1), round(br[2], 1)])
    # planted foot in the first 0.6 s = the ball whose z stays lowest on average
    zl = sum(x[4] for x in rows[:18]) / 18.0; zr = sum(x[7] for x in rows[:18]) / 18.0
    planted = 'r' if zr < zl else 'l'; i0, i1 = (5, 6) if planted == 'r' else (2, 3)
    drift = [round(math.hypot(x[i0] - rows[0][i0], x[i1] - rows[0][i1]), 1) for x in rows]
    out['Turn%s%s' % (s, d)] = {'nf': c.nf, 'planted_first': planted, 'ball_drift_cm_per_frame': drift, 'root_xy': [[x[0], x[1]] for x in rows[::3]]}
print('AUTHDRIFT248 ' + json.dumps(out))
