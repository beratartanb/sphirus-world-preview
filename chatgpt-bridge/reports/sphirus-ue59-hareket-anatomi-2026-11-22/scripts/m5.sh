# m5.sh '<json overrides>' : set round-5 motion A/B overrides (empty {} = defaults)
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; echo "$1" > Saved/UE59Work/r5/m5v.json
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/UE59_20261122/c_m5_set.py" emb_m5s 120 2>&1 | grep -E "M5SET|Error|Traceback" | cut -c1-300
