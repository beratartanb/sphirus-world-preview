"""V2.25 SHME source patch T2c: same behaviour as T2b, rebuilt so the editor can build it.
T2b made the funcs build run out of memory twice (editor 18 -> 94 GB committed inside one write_graph_dsl call, OOM in
TryCreateConnection): the block shared the same pure wildcard (select) results through several nested selects (spAct x3, spRebased x3,
spPlan x4). T2c writes the shared intermediates to component variables first (StepPrepCapDz, StepPrepAct, StepPrepPlan, and the re-based
StepPrepZ), so each later expression reads a plain variable getter instead of re-joining the shared pure chain. Same order of evaluation:
capDz is stored before StepPrepPrevZ is updated."""
import pathlib
V1 = pathlib.Path(__file__).resolve().parents[2] / 'Tools/SHME_V1_20260925'
def patch(fname, old, new, marker):
    p = V1 / fname; t = p.read_bytes().decode('utf8')
    if marker in t: print(fname, marker, 'already'); return
    for nl in ('\n', '\r\n'):
        o = old.replace('\n', nl)
        if t.count(o) == 1: p.write_bytes(t.replace(o, new.replace('\n', nl)).encode('utf8')); print(fname, marker, 'patched'); return
    raise AssertionError((fname, marker))
patch('shm_component_vars.py', "('StepPrepPrevZ', F, 'SHM|V225'),", "('StepPrepPrevZ', F, 'SHM|V225'), ('StepPrepCapDz', F, 'SHM|V225'), ('StepPrepAct', B_, 'SHM|V225'), ('StepPrepPlan', F, 'SHM|V225'),", 'StepPrepCapDz')
OLD = ("  (bind spPlan (select (and spOn (and (> (abs spDiff) (R StepPrepMin)) (< (abs spDiff) (R StepPrepMax)))) (* (R StepPrepGain) spDiff) 0.0))\n"
       "  ; V2.25 T2b: the capsule's own height change is absorbed by the offset (pelvis world-continuous) and released in the human order\n"
       "  (bind capDz (select TerrainInit (- (.z Position) StepPrepPrevZ) 0.0))\n"
       "  (bind spBig (> (abs capDz) 6.0))\n"
       "  (set StepPrepActT (select spBig 0.30 (max 0.0 (- StepPrepActT dt))))\n"
       "  (bind spAct (or spBig (and (> StepPrepActT 0.0) (> (abs capDz) 1.0))))\n"
       "  (bind contactEdge (or (and ContactL (not StepPrepPrevCL)) (and ContactR (not StepPrepPrevCR))))\n"
       "  (set StepPrepRel (select spAct 0.0 (select contactEdge 1.0 StepPrepRel)))\n"
       "  (bind aSp (- 1.0 (exp (/ (- 0.0 h) (max (R StepPrepTau) 0.02)))))\n"
       "  (bind aSpR (- 1.0 (exp (/ (- 0.0 h) (max (R StepPrepReleaseTau) 0.02)))))\n"
       "  (bind aSpH (- 1.0 (exp (/ (- 0.0 h) (max (R StepPrepHoldTau) 0.02)))))\n"
       "  (bind spRebased (select spAct (- StepPrepZ capDz) StepPrepZ))\n"
       "  (bind spHeld (> (abs (- spRebased spPlan)) 2.0))\n"
       "  (bind aSpUse (select spAct 0.0 (select (and spHeld (< StepPrepRel 0.5)) aSpH (select spHeld aSpR aSp))))\n"
       "  (set StepPrepZ (select spOn (+ spRebased (* (- spPlan spRebased) aSpUse)) 0.0))\n"
       "  (set StepPrepPrevZ (.z Position))\n"
       "  (set StepPrepPrevCL ContactL)\n"
       "  (set StepPrepPrevCR ContactR)\n"
       "  (set StepPrepSeen (select (> (abs spPlan) 0.1) 1.0 0.0))\n")
NEW = ("  (set StepPrepPlan (select (and spOn (and (> (abs spDiff) (R StepPrepMin)) (< (abs spDiff) (R StepPrepMax)))) (* (R StepPrepGain) spDiff) 0.0))\n"
       "  ; V2.25 T2c: the capsule's own height change is absorbed by the offset (pelvis world-continuous) and released in the human order;\n"
       "  ; shared intermediates are stored in variables (T2b's shared nested selects ran the funcs build out of memory)\n"
       "  (set StepPrepCapDz (select TerrainInit (- (.z Position) StepPrepPrevZ) 0.0))\n"
       "  (set StepPrepPrevZ (.z Position))\n"
       "  (set StepPrepActT (select (> (abs StepPrepCapDz) 6.0) 0.30 (max 0.0 (- StepPrepActT dt))))\n"
       "  (set StepPrepAct (or (> (abs StepPrepCapDz) 6.0) (and (> StepPrepActT 0.0) (> (abs StepPrepCapDz) 1.0))))\n"
       "  (set StepPrepRel (select StepPrepAct 0.0 (select (or (and ContactL (not StepPrepPrevCL)) (and ContactR (not StepPrepPrevCR))) 1.0 StepPrepRel)))\n"
       "  (set StepPrepPrevCL ContactL)\n"
       "  (set StepPrepPrevCR ContactR)\n"
       "  (set StepPrepZ (select StepPrepAct (- StepPrepZ StepPrepCapDz) StepPrepZ))\n"
       "  (bind aSp (- 1.0 (exp (/ (- 0.0 h) (max (R StepPrepTau) 0.02)))))\n"
       "  (bind aSpR (- 1.0 (exp (/ (- 0.0 h) (max (R StepPrepReleaseTau) 0.02)))))\n"
       "  (bind aSpH (- 1.0 (exp (/ (- 0.0 h) (max (R StepPrepHoldTau) 0.02)))))\n"
       "  (bind aHeld (select (< StepPrepRel 0.5) aSpH aSpR))\n"
       "  (bind aFree (select (> (abs (- StepPrepZ StepPrepPlan)) 2.0) aHeld aSp))\n"
       "  (set StepPrepZ (select spOn (+ StepPrepZ (* (- StepPrepPlan StepPrepZ) (select StepPrepAct 0.0 aFree))) 0.0))\n"
       "  (set StepPrepSeen (select (> (abs StepPrepPlan) 0.1) 1.0 0.0))\n")
patch('shm_src.py', OLD, NEW, 'V2.25 T2c')
print('done')
