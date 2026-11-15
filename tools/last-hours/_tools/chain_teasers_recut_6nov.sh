# 6 Nov: re-cut ALL Indianapolis + Cole & Roe teasers from the face-fixed shot lists (LESSONS 55), one render at a time, then <10 MB copies
export PYTHONUTF8=1
T="/d/why habibi/_newchannel/_tools"; cd "$T"
RUN="/e/AskHabibiAI/venv-chatterbox/Scripts/python.exe -u"
for job in "indy T1_antenna" "indy T2_twelve_minutes" "indy T3_the_rule" "indy T4_the_witness" "coleroe T1_the_count"; do
  set -- $job; $RUN teasers_more.py render $1 $2 >> "$T/teasers_recut_6nov.log" 2>&1; echo "$1 $2 exit $? $(date +%T)"
done
for d in 15_uss_indianapolis 16_cole_roe_1937; do
  cd "/d/why habibi/_newchannel/$d/teasers" && mkdir -p lt10
  for v in TheLastHours_Short_T*.mp4; do
    dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$v")
    vb=$(awk -v d="$dur" 'BEGIN{printf "%d", (9.4*8*1024*1024/d - 128000)}')
    ffmpeg -v error -y -i "$v" -c:v libx264 -b:v $vb -pass 1 -an -f mp4 NUL && ffmpeg -v error -y -i "$v" -c:v libx264 -b:v $vb -pass 2 -c:a aac -b:a 128k "lt10/$v"
    echo "$d $v $dur s, lt10 $(stat -c %s "lt10/$v") bytes"
  done
  rm -f ffmpeg2pass-0.log ffmpeg2pass-0.log.mbtree
done
echo DONE
