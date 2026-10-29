#!/bin/sh
cd "D:/why habibi/_newchannel"
UV="uv run --no-project --offline --with pillow --with numpy --with soundfile --with scipy --with pyproj python"
Q="D:/why habibi/_upload_queue_last_hours"
run2() { d=$1; s=$2; n=$3; a=$4; b=$5; (cd $d && PYTHONUTF8=1 $UV $s seg $a $n > build/seg_$a.log 2>&1 &); (cd $d && PYTHONUTF8=1 $UV $s seg $b $n > build/seg_$b.log 2>&1); while ! grep -q "seg done" $d/build/seg_$a.log && ! grep -qi "error" $d/build/seg_$a.log; do sleep 10; done; }
run2 03_franklin render_franklin.py 8 3 4
run2 03_franklin render_franklin.py 8 5 6
run2 04_dbcooper render_cooper.py 8 5 7
for spec in "03_franklin render_franklin.py TheLastHours_02_Franklin 61.67:63.88 297.38:309.21" "04_dbcooper render_cooper.py TheLastHours_03_DBCooper 46.39:48.87 273.53:285.36"; do
  set -- $spec; d=$1; s=$2; n=$3; shift 3
  for f in $d/build/seg_[0-7].mp4; do echo "$f $(ffprobe -v error -show_entries format=duration -of csv=p=0 $f)"; done
  (cd $d && PYTHONUTF8=1 $UV $s final 8)
  $UV _tools/cut_ranges.py "$d/export/$n.mp4" "$d/export/${n}_v2.mp4" "$@"
  cp "$d/export/${n}_v2.mp4" "$Q/"
  echo "DONE $n $(ffprobe -v error -show_entries format=duration -of csv=p=0 $d/export/${n}_v2.mp4)"
done
