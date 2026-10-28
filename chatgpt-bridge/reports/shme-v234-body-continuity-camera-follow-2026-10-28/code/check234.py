"""check234.py <label> [...] : behaviour check of the V2.34 locomotion frame from the LTP rows (offline): rows with the component fields,
LocoState distribution, max |InFrameOff|, LocoYaw range, max |CamRecDelta|. A run whose fields are missing / 'err' is INVALID (not a pass)."""
import sys, os, math
H = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [H + '/../SHME_V232_20261027', H + '/../SHME_V231_20261026']
from ltp231 import load
def f(x):
    try: return float(x)
    except Exception: return None
for lab in sys.argv[1:]:
    try: R = load(lab)
    except Exception as e: print('CHECK234', lab, 'NO_DATA', e); continue
    ls = [f(r.get('cv_LocoState')) for r in R]; io = [f(r.get('cv_InFrameOff')) for r in R]; ly = [f(r.get('cv_LocoYaw')) for r in R]; cd = [f(r.get('cv_CamRecDelta')) for r in R]
    ok = [x for x in ls if x is not None]
    if not ok: print('CHECK234', lab, 'INVALID fields missing', list(R[0].keys())[:8] if R else []); continue
    st = {k: sum(1 for x in ok if abs(x - k) < 0.5) for k in (0, 1, 2)}
    print('CHECK234 %s rows %d state %s |InFrameOff|max %.1f LocoYaw %.1f..%.1f |CamRecDelta|max %.2f' % (lab, len(R), st, max(abs(x) for x in io if x is not None),
          min(x for x in ly if x is not None), max(x for x in ly if x is not None), max(abs(x) for x in cd if x is not None)))
