# plant.sh "<python dict body>" : set FootPlacement plant overrides in memory, e.g. plant.sh "'thr':12.0,'rad_def':45.0"
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"
printf 'import builtins, unreal as u\nbuiltins.PLANT={%s}\nexec(open(u.Paths.project_dir()+"Tools/UE59_20261123/c_plant6.py",encoding="utf8").read())\n' "$1" > Saved/UE59Work/r6/plant_job.py
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Saved/UE59Work/r6/plant_job.py" emb_plantj 120 2>&1 | grep -E "PLANT|Error" | cut -c1-200
