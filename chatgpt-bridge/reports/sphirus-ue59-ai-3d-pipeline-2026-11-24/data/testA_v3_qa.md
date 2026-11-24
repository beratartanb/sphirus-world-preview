# QA SM_SPH_TEST_MaskStand.blend (static) - REVIEW

Blender 5.3.0; triangles 1350; {'PASS': 46, 'WARN': 3, 'FAIL': 0, 'NOT_TESTED': 0}

| object | check | value | limit | status |
|---|---|---|---|---|
| SM_SPH_TEST_MaskStand | triangles | 1350 | warn 15000 / fail 60000 | PASS |
| SM_SPH_TEST_MaskStand | open_boundary_edges | 64 | info | WARN |
| SM_SPH_TEST_MaskStand | uv_coverage_0_1 | 0.5024 | warn 0.55 / fail 0.3 | WARN |
| SM_SPH_TEST_MaskStand | texel_density_px_per_m | 1190.8 | 512-2048 px/m (1024 nominal at 2k) | PASS |
| SM_SPH_TEST_MaskStand | dimensions_m | [0.3, 0.26, 0.637] | real-world metres | PASS |
| T_SPH_TEST_MaskStand_ORM.png | roughness_variation_sd | 0.0296 | warn 0.04 / fail 0.015 | WARN |
