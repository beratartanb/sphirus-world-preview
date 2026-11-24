#!/bin/bash
# rec.sh <tag> ['<python run once in PIE before recording>'] : PIE on the open map, optional runtime candidate (PIE pawn only), then the
# recorder of rec_motion.py; frames are encoded to Saved/UE59Work/vf2b/vid/<tag>.mp4 (30 fps game time) and every 15th frame is kept as PNG.
# Env: POS="x,y,z" YAW=deg REC='<python dict for builtins.VF2B_REC>' WAITS=real seconds to wait (default 80)
source "<PROJECT>/Tools/VF2B_20261125/lib.sh"
TAG=$1; OUT=Saved/UE59Work/vf2b/vid; mkdir -p $OUT/$TAG; rm -f Saved/UE59Work/vf2b/_rec_done.txt Saved/Screenshots/WindowsEditor/HighresScreenshot*.png Saved/Screenshots/WindowsEditor/ScreenShot*.png $OUT/$TAG/*.png
PIE_ON
J "tp(${POS:-850,2080,90},${YAW:-90},-6); PW.set_actor_rotation(u.Rotator(pitch=0,yaw=${YAW:-90},roll=0),False); print(1)" >/dev/null; W 5
[ -n "$2" ] && { J "$2" measure 3; W ${PREWAIT:-6}; }
J "cmd('r.DepthOfFieldQuality 0')" >/dev/null
J "import builtins; builtins.VF2B_REC=${REC:-{\}}
exec(open(u.Paths.project_dir()+'Tools/VF2B_20261125/rec_motion.py',encoding='utf8').read())" measure 1
for i in $(seq 1 ${WAITS:-90}); do [ -f Saved/UE59Work/vf2b/_rec_done.txt ] && break; W 1; done; W 3
J "cmd('r.DepthOfFieldQuality 2'); u.GameplayStatics.set_global_time_dilation(W,1.0); print(1)" >/dev/null
PIE_OFF
n=0; for f in $(ls -tr Saved/Screenshots/WindowsEditor/ScreenShot*.png Saved/Screenshots/WindowsEditor/HighresScreenshot*.png 2>/dev/null); do n=$((n+1)); mv "$f" $OUT/$TAG/f$(printf %04d $n).png; done
cp Saved/UE59Work/vf2b/_rec_done.txt $OUT/$TAG.rows.txt 2>/dev/null; echo "frames $n"
[ "$n" -gt 10 ] || exit 1
WH=$(powershell.exe -NoProfile -Command "Add-Type -AssemblyName System.Drawing; \$i=[System.Drawing.Image]::FromFile('$(cygpath -w "$P/$OUT/$TAG/f0001.png")'); \"\$(\$i.Width) \$(\$i.Height)\"; \$i.Dispose()" | tr -d '\r')
"<TOOLS>/Blender/blender-5.3.0-windows-x64/blender.exe" --background --factory-startup --python "$(cygpath -m "$P/Tools/Day_20261107/mkvid.py")" -- "$(cygpath -m "$P/$OUT/$TAG.mp4")" 30 0 0 $WH "$(cygpath -m "$P/$OUT/$TAG")" 2>&1 | grep VIDEO
mkdir -p $OUT/${TAG}_keys; i=0; for f in $OUT/$TAG/f*.png; do i=$((i+1)); [ $((i % 15)) -eq 1 ] && cp $f $OUT/${TAG}_keys/; done; rm -rf $OUT/$TAG; ls -la $OUT/$TAG.mp4 | awk '{print $5,$9}'
