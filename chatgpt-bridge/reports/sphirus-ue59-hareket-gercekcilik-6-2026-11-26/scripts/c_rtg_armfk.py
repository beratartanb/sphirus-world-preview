# c_rtg_armfk.py (control/write, in memory): arms FK-only in RTG_Sph_UEFN_to_MH - LeftArm / RightArm removed from the 'Run IK Rig' op chains
# (builtins.RTG_ARMFK = False restores them). With the arm IK goals the target hands were placed at the broad UEFN source's hand positions
# (shoulders 35 cm vs 24.5 cm on B13) -> ~12 deg extra abduction that the posture servo could not remove (saturated at -14).
import unreal as u, builtins
r = u.load_asset('/Game/Sphirus/Player/GASP/Rig/RTG_Sph_UEFN_to_MH'); c = u.IKRetargeterController.get_controller(r)
i = [k for k in range(c.get_num_retarget_ops()) if c.get_op_name(k) == 'Run IK Rig'][0]; oc = c.get_op_controller(i); st = oc.get_settings()
ch = list(st.get_editor_property('chains')); names = [str(x.get_editor_property('target_chain_name')) for x in ch]
fk = getattr(builtins, 'RTG_ARMFK', True)
# pass 6 fix: REMOVING the arm chains did not persist (the op rebuilds its chain list from the IK rig on load: the 13:34 save reloaded with
# LeftArm/RightArm back). The serialized per-chain switch enable_ik is used instead; missing arm chains are re-added first.
have = set(names); tmpl = ch[0]
for n in ('LeftArm', 'RightArm'):
    if n not in have:
        e = type(tmpl)(); e.set_editor_property('target_chain_name', n); ch.append(e)
for x in ch:
    if str(x.get_editor_property('target_chain_name')) in ('LeftArm', 'RightArm'): x.set_editor_property('enable_ik', not fk)
st.set_editor_property('chains', ch); oc.set_settings(st)
print('RTGARMFK', fk, [(str(x.get_editor_property('target_chain_name')), x.get_editor_property('enable_ik')) for x in oc.get_settings().get_editor_property('chains')])
