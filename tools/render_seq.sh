# render a long file in N parts ONE AT A TIME (memory-safe), retry a part whose duration is short, then mix + mux.
#   bash render_seq.sh <episode dir> <render_*.py> <N>
E="$1"; R="$2"; N="$3"; cd "$E" || exit 1
RUN="uv run --no-project --with pillow --with numpy --with soundfile python"
export PYTHONUTF8=1
NF=$($RUN "$R" times 2>/dev/null | awk '/^VO_END/ {print $4}'); echo "duration $NF s, $N parts $(date +%T)"
for i in $(seq 0 $((N - 1))); do
  for try in 1 2 3; do
    $RUN "$R" seg $i $N > "build/seg_$i.log" 2>&1
    d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "build/cseg_$i.mp4" 2>/dev/null)
    want=$(awk -v t="$NF" -v n="$N" 'BEGIN { printf "%.1f", t / n - 1.0 }')
    if awk -v d="$d" -v w="$want" 'BEGIN { exit !(d + 0 >= w + 0) }'; then echo "part $i ok ${d}s (try $try) $(date +%T)"; break; fi
    echo "part $i SHORT ${d}s (want >= $want), retry $try $(date +%T)"; tail -2 "build/seg_$i.log"
  done
done
$RUN "$R" audio > build/audio.log 2>&1; echo "audio exit $? $(date +%T)"
$RUN "$R" final $N > build/final.log 2>&1; echo "final exit $? $(date +%T)"
ls -1 export/*.mp4 | while read f; do echo "$f $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")"; done
