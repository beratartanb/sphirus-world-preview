"""Loose-groom simulation stability pass: every loose strand is a guide (HairToGuideDensity 1.0 -> no interpolation streaks
from sparse fast guides), stretch projection on (hard length), stiffer / damped bend, more iterations. Rebuild via the
global-interpolation toggle; save in a later job (ue_rv_hair_save.py)."""
import unreal as u, re, builtins
TAG = getattr(builtins, 'RV_HAIR_TAG', 'v12'); g = u.load_asset(f'/Game/Sphirus/CharacterLab/CharacterRevision_20260930/Hair/GR_RV_Hair_Loose_{TAG}')
out = []
for q in g.get_editor_property('hair_groups_physics'):
    t = q.export_text()
    for k, v in (('BendStiffness', '0.150000'), ('BendDamping', '0.080000'), ('AirDrag', '0.350000'), ('StretchDamping', '0.050000')): t = re.sub(k+r'=[0-9.]+', k+'='+v, t, 1)
    t = re.sub(r'SubSteps=[0-9]+', 'SubSteps=5', t, 1); t = re.sub(r'IterationCount=[0-9]+', 'IterationCount=10', t, 1)
    t = t.replace('ProjectStretch=False', 'ProjectStretch=True').replace('ProjectBend=False', 'ProjectBend=True')
    q.import_text(t); out.append(q)
g.set_editor_property('hair_groups_physics', out)
iv = []
for q in g.get_editor_property('hair_groups_interpolation'):
    t = q.export_text(); t = re.sub(r'HairToGuideDensity=[0-9.]+', 'HairToGuideDensity=1.000000', t, 1); t = t.replace('bOverrideGuides=True', 'bOverrideGuides=False'); q.import_text(t); iv.append(q)
    print('INTERP', t[:300])
g.set_editor_property('hair_groups_interpolation', iv)
g.set_editor_property('enable_global_interpolation', True); g.set_editor_property('enable_global_interpolation', False)
print('SIM2_SET', [p.export_text()[:260] for p in g.get_editor_property('hair_groups_physics')])
