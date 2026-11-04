#!/bin/bash
# publish_pfr_chunks.sh : the single 620 MB push was reset by the remote (curl 55). Re-commit the already staged report folder in the
# sparse clone as three commits (report + sheets + perf + tools, then route A videos, then route B videos) and push each one separately
# with a large post buffer over HTTP/1.1. Idempotent: skips chunks whose files are already on origin/main.
set -e
G="/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/ghpub241"
R=chatgpt-bridge/reports/exterior-pine-forest-redesign-2026-11-04
GIT="git -c core.longpaths=true -c http.postBuffer=1048576000 -c http.version=HTTP/1.1 -c http.lowSpeedLimit=1000 -c http.lowSpeedTime=120"
cd "$G"
# undo the unpushed local commit (keep the files), re-stage nothing
if [ "$($GIT rev-list --count origin/main..HEAD)" != 0 ]; then $GIT reset -q --mixed origin/main; echo "local commit undone, files kept"; fi
commit_push() {   # $1 label, $2.. pathspecs
  local label="$1"; shift
  $GIT add --sparse -- "$@"
  if $GIT diff --cached --quiet; then echo "chunk $label: nothing to commit"; return 0; fi
  $GIT -c user.name=beratartanb -c user.email=beratartanb@gmail.com commit -q -F - <<MSG
Exterior PFR: first gameplay area redesigned on the Pine Forest Pack reference ($label)

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
MSG
  for try in 1 2 3; do if $GIT push -q origin HEAD; then echo "chunk $label pushed (try $try)"; return 0; fi; echo "chunk $label push failed (try $try)"; sleep 20; done
  return 1
}
commit_push "report, sheets, reference, perf, tools" "$R/README.md" "$R/sheets" "$R/reference" "$R/perf" "$R/tools"
commit_push "route A before/after video parts" "$R/video/routeA_before_after_part1.avi" "$R/video/routeA_before_after_part2.avi"
commit_push "route A before/after video parts 3-4" "$R/video/routeA_before_after_part3.avi" "$R/video/routeA_before_after_part4.avi"
commit_push "route B before/after video parts 1-2" "$R/video/routeB_before_after_part1.avi" "$R/video/routeB_before_after_part2.avi"
commit_push "route B before/after video parts 3-4" "$R/video/routeB_before_after_part3.avi" "$R/video/routeB_before_after_part4.avi"
$GIT log --oneline origin/main -6
echo "PUBLISHED https://github.com/beratartanb/sphirus-world-preview/tree/main/$R"
