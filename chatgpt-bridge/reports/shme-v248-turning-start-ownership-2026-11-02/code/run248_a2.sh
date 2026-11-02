#!/bin/bash
# run248_a.sh : V2.48 chain A = turning-start databases + look-aware start ownership install (knob off) + A/B at 30 / real time / 60 FPS
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V248_20261102; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
source $D/lib248.sh
SHME_KIND=measure SHME_OWNER=v248 bash $RUN $REQ/tdb_dry_req.py v248tdbdry3 300 | grep -a 'DB248' > $D/data/tdb_dry.out
echo "[tdb dry] $(cut -c1-900 $D/data/tdb_dry.out)" >> $O
"$PY" - <<'PYEOF' >> $O
import json
s = open('Saved/Codex/SHME_V248_20261102/data/tdb_dry.out', encoding='utf8', errors='ignore').read(); d = json.loads(s[s.index('{'):])
clips = sorted(set(sum([v['keep'] for v in d['sides'].values()], []))); new = [v['dst'] for v in d['sides'].values()]
json.dump(clips, open('Saved/Codex/SHME_V248_20261102/data/turnstart_clips.json', 'w')); json.dump(new, open('Saved/Codex/SHME_V248_20261102/data/turnstart_new.json', 'w'))
print('TDB_PLAN clips %d new %s drop %s foreign %s' % (len(clips), new, [v['drop'] for v in d['sides'].values()], [v['foreign'] for v in d['sides'].values()]))
PYEOF
grep -q "foreign \[\[\], \[\]\]" $O || { echo "TDB_ABORT foreign entries or parse failure" >> $O; exit 1; }
NEW=$("$PY" -c "import json; print(' '.join(json.load(open('Saved/Codex/SHME_V248_20261102/data/turnstart_new.json'))))")
"$PY" Tools/SHME_V233_20261027/manifest233.py v248_tdb --from $D/data/turnstart_clips.json --new $NEW | tail -1 | cut -c1-160 >> $O
echo "[tdb build] $(SHME_KIND=write SHME_OWNER=v248 SHME_MANIFEST=$M/v248_tdb.json bash $RUN $REQ/tdb_build_req.py v248tdb 900 | grep -a 'DB248\|REFUSED\|WRITE_GUARD\|Error\|Traceback\|Assertion' | cut -c1-1500)" >> $O
grep -q '"entries"' $O || { echo "TDB_ABORT build produced no entries" >> $O; exit 1; }
"$PY" Tools/SHME_V233_20261027/manifest233.py v248_abp --assets /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching | tail -1 | cut -c1-120 >> $O
echo "[turnstart] $(SHME_KIND=write SHME_OWNER=v248 SHME_MANIFEST=$M/v248_abp.json bash $RUN $REQ/turnstart_req.py v248turnstart 900 | grep -a 'TURNSTART248\|REFUSED\|WRITE_GUARD\|Error\|Traceback\|Assertion' | cut -c1-900)" >> $O
grep -q '"saved": true' $O || { echo "TS_ABORT install not saved" >> $O; exit 1; }
echo "[verify] $(SHME_KIND=measure SHME_OWNER=v248 bash $RUN /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v248verify 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*')" >> $O
relaunch ts30 30; WARM=1 ab ts "j45_sl:ts j45_sl:o jstart:ts taps:ts wstart:ts j45_sl:ts:2"
relaunch tsreal real; WARM=1 ab tsreal "j45_sl:ts j45_sl:ts:2 j45_sl:ts:3 j45_sl:o j45_sl:o:2 jstart:ts taps:ts"
relaunch ts60 60; WARM=1 ab ts60 "j45_sl:ts jstart:ts"
echo TS248_DONE >> $O
