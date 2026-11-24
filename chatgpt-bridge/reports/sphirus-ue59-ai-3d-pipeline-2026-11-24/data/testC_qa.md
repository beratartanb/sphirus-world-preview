# QA SK_SPH_TEST_Dummy.blend (skeletal) - FAIL

Blender 5.3.0; triangles 1652; {'PASS': 39, 'WARN': 4, 'FAIL': 1, 'NOT_TESTED': 0}

| object | check | value | limit | status |
|---|---|---|---|---|
| SK_SPH_TEST_Dummy | triangles | 1652 | warn 40000 / fail 90000 | PASS |
| SK_SPH_TEST_Dummy | uv_coverage_0_1 | 0.1446 | warn 0.55 / fail 0.3 | FAIL |
| SK_SPH_TEST_Dummy | texel_density_px_per_m | 332.1 | info | WARN |
| SK_SPH_TEST_Dummy | dimensions_m | [1.493, 0.314, 1.696] | real-world metres | PASS |
| M_SPH_TEST_Dummy | basecolor_constant_linear_lum | 0.303 | 0.02-0.85 (no texture => homogeneous) | WARN |
| SKEL_SPH_TEST_Dummy | bone_count | 36 | warn 120 / fail 250 | PASS |
| SKEL_SPH_TEST_Dummy | deform_shoulder_raise_upperarm_l_edge_strain_p995 | 0.3649 | warn 0.35 / fail 0.7 | WARN |
| SKEL_SPH_TEST_Dummy | deform_hip_flex_thigh_l_edge_strain_p995 | 0.3639 | warn 0.35 / fail 0.7 | WARN |
