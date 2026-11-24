# c_mr1_defaults.py (control, in memory; re-appliable; runs LAST in alldef) - movement realism pass 1 (2026-11-24): hip-line and trunk-twist
# attenuation (m_hip1 / m_hip2). Shares removed from the cyclic part only: hip yaw walk 0.45 / run 0 / sprint 0.35, hip tilt 0.38 / 0.2 /
# 0.33, shoulder yaw run 0.35 / sprint 0.3. HIP_On 0 switches the whole layer off.
import unreal as u
c=u.get_default_object(u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player').generated_class())
M={'HIP_On':1.0,'HIP_LP':1.5,'HIP_KSp':1.0,'HIP_KYW':0.45,'HIP_KYR':0.0,'HIP_KYS':0.35,'HIP_KOW':0.38,'HIP_KOR':0.2,'HIP_KOS':0.33,'SH_KR':0.35,'SH_KS':0.3}
for k,v in M.items(): c.set_editor_property(k,v)
print('MR1DEF',{k:c.get_editor_property(k) for k in M})
