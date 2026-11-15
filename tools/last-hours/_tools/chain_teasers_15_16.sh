# Teaser Shorts for files 15 (Indianapolis) and 16 (Cole & Roe), one render at a time, then <10 MB 2-pass copies in teasers/lt10/
export PYTHONUTF8=1
T="/d/why habibi/_newchannel/_tools"; cd "$T"
RUN="uv run --no-project --with pillow --with numpy --with soundfile python"
for f in indy coleroe; do $RUN teasers_more.py all $f > "$T/teasers_$f.log" 2>&1; echo "$f teasers exit $? $(date +%T)"; done
for d in 15_uss_indianapolis 16_cole_roe_1937; do
  cd "/d/why habibi/_newchannel/$d/teasers" && mkdir -p lt10
  for v in TheLastHours_Short_*.mp4; do
    dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$v")
    vb=$(awk -v d="$dur" 'BEGIN{printf "%d", (9.4*8*1024*1024/d - 128000)}')
    ffmpeg -v error -y -i "$v" -c:v libx264 -b:v $vb -pass 1 -an -f mp4 NUL && ffmpeg -v error -y -i "$v" -c:v libx264 -b:v $vb -pass 2 -c:a aac -b:a 128k "lt10/$v"
    echo "$d $v $(stat -c %s "lt10/$v")"
  done
  rm -f ffmpeg2pass-0.log ffmpeg2pass-0.log.mbtree
done
