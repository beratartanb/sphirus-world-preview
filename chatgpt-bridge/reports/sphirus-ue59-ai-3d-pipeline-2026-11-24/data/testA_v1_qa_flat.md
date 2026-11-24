# QA SM_SPH_TEST_MaskStand.blend (static) - FAIL

Blender 5.3.0; triangles 1350; {'PASS': 45, 'WARN': 2, 'FAIL': 2, 'NOT_TESTED': 0}

| object | check | value | limit | status |
|---|---|---|---|---|
| SM_SPH_TEST_MaskStand | triangles | 1350 | warn 15000 / fail 60000 | PASS |
| SM_SPH_TEST_MaskStand | open_boundary_edges | 64 | info | WARN |
| SM_SPH_TEST_MaskStand | uv_coverage_0_1 | 0.5024 | warn 0.55 / fail 0.3 | WARN |
| SM_SPH_TEST_MaskStand | texel_density_px_per_m | 1190.8 | 512-2048 px/m (1024 nominal at 2k) | PASS |
| SM_SPH_TEST_MaskStand | dimensions_m | [0.3, 0.26, 0.637] | real-world metres | PASS |
| T_SPH_TEST_MaskStand_BC.png | flat_block_share | 0.7271 | warn 0.25 / fail 0.5 | FAIL |
| T_SPH_TEST_MaskStand_ORM.png | flat_block_share | 0.72 | warn 0.25 / fail 0.5 | FAIL |
