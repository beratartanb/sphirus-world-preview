# QA SM_SPH_TEST_MaskStand_uv.blend (static) - FAIL

Blender 5.3.0; triangles 1476; {'PASS': 20, 'WARN': 3, 'FAIL': 3, 'NOT_TESTED': 0}

| object | check | value | limit | status |
|---|---|---|---|---|
| SM_SPH_TEST_MaskStand | triangles | 1476 | warn 15000 / fail 60000 | PASS |
| SM_SPH_TEST_MaskStand | ngons | 6 | warn 0 / fail 0 | FAIL |
| SM_SPH_TEST_MaskStand | uv_texel_density_dev_p90_log | 1.8946 | warn 0.7 / fail 1.4 | FAIL |
| SM_SPH_TEST_MaskStand | uv_coverage_0_1 | 0.426 | warn 0.55 / fail 0.3 | WARN |
| SM_SPH_TEST_MaskStand | texel_density_px_per_m | 2153.4 | 512-2048 px/m (1024 nominal at 2k) | WARN |
| SM_SPH_TEST_MaskStand | uv_flipped_faces | 21 | warn 0 / fail 14.92 | FAIL |
| SM_SPH_TEST_MaskStand | dimensions_m | [0.3, 0.26, 0.637] | real-world metres | PASS |
| M_SPH_TEST_MaskStand_Iron | basecolor_constant_linear_lum | 0.351 | 0.02-0.85 (no texture => homogeneous) | WARN |
