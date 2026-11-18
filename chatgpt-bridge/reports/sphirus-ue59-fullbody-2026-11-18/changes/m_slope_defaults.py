# m_slope_defaults.py (in memory; saved later by gsave): AC_Sph_Motion slope defaults. builtins.SLD overrides.
import unreal as u, builtins
a = u.load_asset('/Game/Sphirus/Player/Motion/AC_Sph_Motion'); c = u.get_default_object(a.generated_class())
D = dict(SlopeKUp=0.4, SlopeKDown=0.15, SlopeMaxUp=9.0, SlopeMaxDown=3.0, SlopeSlowUp=0.25, SlopeSlowDown=0.12, SlopeOn=True)
D.update(getattr(builtins, 'SLD', None) or {})
for k, v in D.items(): c.set_editor_property(k, v)
u.BlueprintEditorLibrary.compile_blueprint(a)
c = u.get_default_object(a.generated_class())
print('SLOPEDEF', {k: c.get_editor_property(k) for k in D}, 'BodyOn', c.get_editor_property('BodyOn'), 'status', a.get_editor_property('status'))
