# Current editor world

Read bridge_status.json first, then scene_summary.json, then Screenshots/.
For environment review read foliage_summary, landscape_summary, water_summary and lighting_summary. For specific objects read actors_index and asset_usage. camera_plan describes capture poses; verification records preservation checks.

Run: 2026-09-23_215018_334205_be8f4c
Map: /Game/GraceRanger/Maps/L_GR_SphirusHouse.L_GR_SphirusHouse
Engine: 5.8.1-56057345+++UE5+Release-5.8

Loaded world only. Null metadata is unknown. Grid estimates are not exact per-cell counts.

Screenshots:
- 00_current_view.png
- 01_world_overview.png
- 02_environment_angle_a.png
- 03_environment_angle_b.png
- 04_environment_angle_c.png
- 05_top_overview.png
- 06_house_exterior.png
- 07_house_to_environment.png
- 08_water_to_house.png
- 09_house_to_forest.png
- 10_forest_to_house.png
- 11_forest_edge.png
- 12_house_to_pond_slope.png
- 13_pond_side_path.png
- 14_uphill_path.png
- 15_uphill_forest_lookback.png
- 16_small_front_footpath.png
- 17_shoreline_gameplay.png

Warnings:
- Scope: currently loaded editor actors only; unloaded World Partition cells and levels are not loaded or modified.
- Null fields mean unavailable in the Python reflection API, not zero or absent.
- Native FoliageType-to-component mapping is not exposed by this engine Python API; mesh/component identity is authoritative. No type guessed from mesh.
- Texture dependency traversal is not performed; direct world material references are reported.
- Framing excludes sky/helpers and robust spatial/size outliers; full actor bounds remain in index.
- Forest views use sampled tree-density cells; a walkable path/entrance is not inferred from actor names.
- Automatically framed cameras are geometric candidates; visibility/occlusion and terrain height should be checked in screenshots.

Errors:

