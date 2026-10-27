"""gen232_loaded.py (editor job): gen231_loaded (loaded catch-step reversal) + V2.32 'catch_natural' (default off = the V2.31 plan):
the entry phases where the other foot S is in its swing and LANDS on its own (entry loop) between tB - CATCH_NAT_PRE and the planned catch
time tC (F_B P21 / P30: the plan re-lifted S 0.13 s after its natural landing -> a double landing, 13 / 29 cm planted drift) take that
natural landing AS the catch: S is not redirected, stays pinned where it landed through the brake, and the exit plan pins it there.
Same output names as gen231_loaded (SHM231L_LoadRev_<fam>_P<k>, V231 folder). builtins.G231L as gen231_loaded + 'catch_natural' (bool),
'catch_nat_pre' (s, 0.25)."""
import builtins, io
SRC = r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V231_20261026/gen231_loaded.py'
src = io.open(SRC, encoding='utf8').read()
REPL = [
    ("    tC = max(tRedir + 0.26, tB + 0.20, tz - CATCH_LEAD)\n",
     "    tC = max(tRedir + 0.26, tB + 0.20, tz - CATCH_LEAD)\n"
     "    # V2.32 catch_natural: S in swing at entry lands on its own before the planned catch -> that landing IS the catch (no re-lift)\n"
     "    natC = False\n"
     "    if bool(CFG231.get('catch_natural', False)) and not s_planted0:\n"
     "        tSL = (EL.next_land(S, tau0) - tau0) / r0t\n"
     "        if tB - float(CFG231.get('catch_nat_pre', 0.25)) <= tSL <= min(tC, tB + 0.15):   # the entry-loop pose freezes after tB + 0.15\n"
     "            natC = True; tRedir = 1.0e9\n"
     "            LSL = EL.at(EL.next_land(S, tau0)); bl_ = EL.rel(LSL, 'ball_' + S)[0]; rS_ = ae.vsc(FWD, df(tSL))\n"
     "            ballC = (rS_[0] + bl_[0], rS_[1] + bl_[1], EL.BZ0[S]); qS = EL.rel(LSL, 'foot_' + S)[1]; cTarget = foot_at_ball(S, ballC, qS)\n"),
    ("    info = {'fam': fam, 'B': B, 'S': S,", "    info = {'nat_catch': natC, 'fam': fam, 'B': B, 'S': S,"),
    ("                bb = ae.vadd(landB, ae.qrot(qB_hs, BALL_LOCAL[B])); pin[B] = (bb[0], bb[1], XL.BZ0[B]); pin[S] = ballC\n",
     "                bb = ae.vadd(landB, ae.qrot(qB_hs, BALL_LOCAL[B])); pin[B] = (bb[0], bb[1], XL.BZ0[B]); pin[S] = sLand if (natC and sLand is not None) else ballC\n"),
]
for a, b in REPL:
    assert src.count(a) == 1, a[:80]
    src = src.replace(a, b)
exec(compile(src, 'gen232_loaded.py', 'exec'), {'__name__': 'g232'})
