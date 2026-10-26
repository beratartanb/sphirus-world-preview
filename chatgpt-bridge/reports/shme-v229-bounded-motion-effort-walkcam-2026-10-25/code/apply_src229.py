"""apply_src229.py (offline, run ONLY when no QA chain runs): V2.29 DSL / schema additions.
(1) shm_profiles.RESPONSE: effort knobs (installed OFF: EffortEnabled False). (2) shm_component_vars: EffortE, EffortLoad, EffortLoadDir,
EffortAccScale, EffortTurnScale. (3) shm_src SHM_UpdateState: the effort state (appended at the end of the function).
Idempotent (markers). Prints APPLY229 {...}."""
import pathlib, json
T = pathlib.Path(__file__).resolve().parents[2] / 'Tools/SHME_V1_20260925'
out = {}
p = T / 'shm_profiles.py'; s = p.read_text(encoding='utf8')
if "'EffortEnabled'" in s: out['profiles'] = 'already'
else:
    add = """    # ---- V2.29 (2026-10-25, Saved/Codex/SHME_V229_20261025): effort / momentary load -> GR capability scales (SHM_UpdateState)
    ('EffortEnabled', 'bool', False, 'V229'), ('EffortGain', 'float', 0.45, 'V229'), ('EffortA0', 'float', 250.0, 'V229'), ('EffortA1', 'float', 500.0, 'V229'),
    ('EffortMinSpeed', 'float', 300.0, 'V229'), ('EffortSprintGain', 'float', 0.02, 'V229'), ('EffortSprintV0', 'float', 380.0, 'V229'),
    ('EffortTauRec', 'float', 6.0, 'V229'), ('EffortLoadTau', 'float', 0.2, 'V229'), ('EffortLoadA', 'float', 900.0, 'V229'),
    ('EffortAccK', 'float', 0.4, 'V229'), ('EffortTurnK', 'float', 0.45, 'V229'), ('EffortLoadK', 'float', 0.6, 'V229'), ('EffortScaleMin', 'float', 0.4, 'V229'),
]"""
    i = s.rindex(']'); s = s[:i] + add[:-1] + s[i:]   # insert before the final ']' of RESPONSE (last list in the file)
    p.write_text(s, encoding='utf8'); out['profiles'] = 'added'
p = T / 'shm_component_vars.py'; s = p.read_text(encoding='utf8')
if "'EffortE'" in s: out['vars'] = 'already'
else:
    i = s.rindex(']'); s = s[:i] + "    ('EffortE', F, 'SHM|V229'), ('EffortLoad', F, 'SHM|V229'), ('EffortLoadDir', F, 'SHM|V229'), ('EffortAccScale', F, 'SHM|V229'), ('EffortTurnScale', F, 'SHM|V229'),\n" + s[i:]
    p.write_text(s, encoding='utf8'); out['vars'] = 'added'
p = T / 'shm_src.py'; s = p.read_text(encoding='utf8', newline='') if False else open(T / 'shm_src.py', encoding='utf8', newline='').read()
if 'V2.29 effort' in s: out['src'] = 'already'
else:
    a = "  (set Gait (select (< sp 10.0) 0.0 (select (< sp 200.0) 1.0 (select (< sp 400.0) 2.0 3.0)))))\n"
    if a not in s: a = a.replace('\n', '\r\n')
    assert s.count(a) == 1, 'anchor'
    nl = '\r\n' if a.endswith('\r\n') else '\n'
    b = """  (set Gait (select (< sp 10.0) 0.0 (select (< sp 200.0) 1.0 (select (< sp 400.0) 2.0 3.0))))
  ; V2.29 effort (HEURISTIC over measured CMC kinematics): EffortE = short-term exertion 0..1 from horizontal acceleration above walking
  ; level (x speed fraction) + a small sustained-sprint term; recovers (tau EffortTauRec) only while the demand is ~0 (standing, looking
  ; around or calm walking never build it). EffortLoad = low-pass |a_h| / EffortLoadA (the support is busy with the current impulse);
  ; EffortLoadDir = EffortLoad x (1 - dot(acc dir, desired dir)) / 2 = load against a NEW direction only (a single brake / push along the
  ; request costs nothing). GR consumes EffortAccScale (max acceleration) and EffortTurnScale (redirect friction): 1.0 = neutral.
  (bind efOn (R EffortEnabled))
  (bind ah (vlenxy Accel))
  (bind wd (* (clamp (/ (- ah (R EffortA0)) (max (R EffortA1) 1.0)) 0.0 2.0) (clamp (/ sp (max (R EffortMinSpeed) 1.0)) 0.0 1.0)))
  (bind ws (* (R EffortSprintGain) (clamp (/ (- sp (R EffortSprintV0)) 200.0) 0.0 1.0)))
  (bind dem (+ wd ws))
  (bind rec (select (> dem 0.05) 0.0 (/ EffortE (max (R EffortTauRec) 0.1))))
  (set EffortE (select efOn (clamp (+ EffortE (* dt (- (* (R EffortGain) dem) rec))) 0.0 1.0) 0.0))
  (bind la (- 1.0 (exp (/ (- dt) (max (R EffortLoadTau) 0.01)))))
  (set EffortLoad (select efOn (+ EffortLoad (* (- (clamp (/ ah (max (R EffortLoadA) 1.0)) 0.0 1.0) EffortLoad) la)) 0.0))
  (bind adir (Matematik|Vektör|Normalize2D(Vector) :A (vec (.x Accel) (.y Accel) 0.0) :Tolerance 0.0001))
  (bind dd (+ (* (.x adir) (.x DesiredDir)) (* (.y adir) (.y DesiredDir))))
  (set EffortLoadDir (select (and efOn HasIntent) (* EffortLoad (clamp (* 0.5 (- 1.0 dd)) 0.0 1.0)) 0.0))
  (set EffortAccScale (select efOn (max (R EffortScaleMin) (- 1.0 (* (R EffortAccK) EffortE))) 1.0))
  (set EffortTurnScale (select efOn (max (R EffortScaleMin) (* (- 1.0 (* (R EffortTurnK) EffortE)) (- 1.0 (* (R EffortLoadK) EffortLoadDir)))) 1.0)))
""".replace('\n', nl)
    s = s.replace(a, b); open(T / 'shm_src.py', 'w', encoding='utf8', newline='').write(s); out['src'] = 'added'
print('APPLY229 ' + json.dumps(out))
