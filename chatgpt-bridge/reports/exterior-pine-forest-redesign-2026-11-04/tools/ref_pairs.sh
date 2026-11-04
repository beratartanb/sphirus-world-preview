#!/bin/bash
# ref_pairs.sh <final_tag> : reference (Pine Forest Pack L_Showcase captures, same engine, same capture size) next to the closest FINAL station
# of our area, as six labelled pairs + sheet: cap/ref_vs_<tag>/. Pairing by subject (shore / rock mass / sunlit rock+log / path / glade / boulders).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
TAG=${1:-final}; D=Saved/Codex/PineForestRedesign_20261104; W="$D/cap/ref_vs_$TAG"; rm -rf "$W"; mkdir -p "$W/ref" "$W/fin"
pair() { cp "$D/ref/showcase/$1.png" "$W/ref/$3.png"; cp "$D/cap/views_$TAG/$2.png" "$W/fin/$3.png"; }
pair f30_L90   P1_landing_fwd      1_shore_ferns_water
pair c090_L90  P2_rockshelf_fwd    2_mossy_rock_mass
pair f15_R90   P2_rockshelf_back   3_sunlit_rock_log_floor
pair ps0_fwd   D08_narrows_fwd     4_forest_path_roots
pair c190_fwd  P3_glade_fwd        5_glade_light_shafts
pair f50_R90   P3_glade_R90        6_boulders_on_floor
powershell.exe -NoProfile -ExecutionPolicy Bypass -File Tools/PineForestRedesign_20261104/compare_pairs.ps1 -Dirs "$W/ref|$W/fin" -Labels "REFERENCE: Pine Forest Pack L_Showcase|FINAL: Sphirus first area ($TAG)" -Out "$W" -W 800 | tail -1
ls "$W"/*.jpg | wc -l
