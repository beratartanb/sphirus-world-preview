# c_cr1_defaults.py (control, in memory; re-appliable) - character realism pass 1 (2026-11-24): idle arm carriage.
# PS_AbdBase 12.5 -> 8.5 deg (arms hung 12.5 deg off the torso at rest = mannequin A-stance); PS_AbdRun 9.5 -> 13.5 keeps the run total (22 deg).
import unreal as u
c=u.get_default_object(u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player').generated_class())
for k,v in {'PS_AbdBase':8.5,'PS_AbdRun':13.5}.items(): c.set_editor_property(k,v)
print('CR1DEF',{k:c.get_editor_property(k) for k in ('PS_AbdBase','PS_AbdRun')})
