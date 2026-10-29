#!/bin/sh
# 23 Oct 2026: re-render the scheduled Last Hours files without flat black screens, cut the spoken ident + mid-video ask.
cd "D:/why habibi/_newchannel"
UV="uv run --no-project --offline --with pillow --with numpy --with soundfile --with scipy python"
Q="D:/why habibi/_upload_queue_last_hours"; A="D:/why habibi/_archive/exports_before_fix_2026-10-23"
while tasklist | grep -qi "python" && [ -f "D:/why habibi/10th video/build/.rendering" ]; do sleep 30; done
until [ "$(ffprobe -v error -show_entries format=duration -of csv=p=0 'D:/why habibi/10th video/export/Ask_Habibi_Ep10_Why_Diesel_Costs_More.mp4' | cut -d. -f1)" -gt 480 ]; do sleep 30; done
echo "diesel done, start $(date)"
for spec in "03_franklin render_franklin.py TheLastHours_02_Franklin 61.67:63.88 297.38:309.21" \
            "04_dbcooper render_cooper.py TheLastHours_03_DBCooper 46.39:48.87 273.53:285.36" \
            "06_flannan render_flannan.py TheLastHours_05_Flannan"; do
  set -- $spec; d=$1; s=$2; n=$3; shift 3
  cp "$d/export/$n.mp4" "$A/$n.mp4"
  (cd $d && PYTHONUTF8=1 $UV $s all 8) > "$d/build/fix_render.log" 2>&1
  if [ $# -gt 0 ]; then $UV _tools/cut_ranges.py "$d/export/$n.mp4" "$d/export/${n}_v2.mp4" "$@"; else cp "$d/export/$n.mp4" "$d/export/${n}_v2.mp4"; fi
  cp "$d/export/${n}_v2.mp4" "$Q/"
  echo "DONE $n $(ffprobe -v error -show_entries format=duration -of csv=p=0 $d/export/${n}_v2.mp4) $(date)"
done
