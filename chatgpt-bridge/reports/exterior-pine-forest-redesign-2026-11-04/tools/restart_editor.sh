#!/bin/bash
# restart_editor.sh <new_log_name> : clean editor restart for the verification-from-disk step. Refuses while packages are dirty
# (quit_editor would open a save prompt), waits for UnrealEditor.exe to exit (kills it after 240 s), then starts a fresh editor with
# this session's gated runner (Tools/SHME_V2_20261014/v2_editor_launch.sh) and waits for SPH_V2_RUNNER_READY.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
L=${1:-pfr_04}; MY="/c/Users/berat/AppData/Local/Temp/claude/bbc6f8fdff1f8341/58bc34ab-b0fd-4574-9259-4850d781d32b/scratchpad"; T=Tools/PineForestRedesign_20261104
cat > "$MY/quit_editor.py" <<'EOF'
import unreal as u, json, pathlib
S = u.EditorLoadingAndSavingUtils; dm = [p.get_name() for p in S.get_dirty_map_packages()]; dc = [p.get_name() for p in S.get_dirty_content_packages()]
pathlib.Path(u.Paths.project_dir(), 'Saved/Codex/PineForestRedesign_20261104/design/quit_check.json').write_text(json.dumps({'dirty_maps': dm, 'dirty_content': dc}))
assert not dm and not dc, 'dirty packages: %s %s' % (dm[:3], dc[:3])
print('PFR_QUIT clean, quitting'); u.SystemLibrary.quit_editor()
EOF
if [ "${FORCE:-0}" = 1 ]; then   # FORCE=1: the map on disk is already verified; skip the clean-quit attempt (a transient dirty flag would block it)
  echo "FORCE restart: killing the editor without the quit job"; taskkill //F //IM UnrealEditor.exe >/dev/null 2>&1; sleep 8
else
rm -f Saved/Codex/PineForestRedesign_20261104/design/quit_check.json
bash $T/pfr_chain.sh "job:control:$MY/quit_editor.py:40" | tail -1
for i in $(seq 1 20); do [ -f Saved/Codex/PineForestRedesign_20261104/design/quit_check.json ] && break; sleep 2; done
head -c 300 Saved/Codex/PineForestRedesign_20261104/design/quit_check.json; echo
for i in $(seq 1 120); do tasklist | grep -qi "UnrealEditor.exe" || break; sleep 2; done
fi
if tasklist | grep -qi "UnrealEditor.exe"; then echo "editor still running after 240 s -> taskkill"; taskkill //F //IM UnrealEditor.exe >/dev/null 2>&1; sleep 5; fi
taskkill //F //IM CrashReportClientEditor.exe >/dev/null 2>&1
echo "editor exited $(date +%T)"; sleep 5
export V219_EDARGS='-UseFixedTimeStep -FPS=30'
bash Tools/SHME_V2_20261014/v2_editor_launch.sh "$L" | tail -2
