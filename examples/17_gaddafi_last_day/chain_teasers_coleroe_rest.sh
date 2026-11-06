# Cole & Roe teasers T2-T4 (the 31 Oct chain stopped after T1), one render at a time, then <10 MB 2-pass copies in teasers/lt10/
export PYTHONUTF8=1
T="/d/why habibi/_newchannel/_tools"; cd "$T"
RUN="uv run --no-project --with pillow --with numpy --with soundfile python"
for n in T2_the_warden T3_the_postcard T4_tulsa; do $RUN teasers_more.py render coleroe $n >> "$T/teasers_coleroe_rest.log" 2>&1; echo "coleroe $n exit $? $(date +%T)"; done
cd "/d/why habibi/_newchannel/16_cole_roe_1937/teasers" && mkdir -p lt10
for v in TheLastHours_Short_T2_the_warden.mp4 TheLastHours_Short_T3_the_postcard.mp4 TheLastHours_Short_T4_tulsa.mp4; do
  [ -f "$v" ] || continue
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$v")
  vb=$(awk -v d="$dur" 'BEGIN{printf "%d", (9.4*8*1024*1024/d - 128000)}')
  ffmpeg -v error -y -i "$v" -c:v libx264 -b:v $vb -pass 1 -an -f mp4 NUL && ffmpeg -v error -y -i "$v" -c:v libx264 -b:v $vb -pass 2 -c:a aac -b:a 128k "lt10/$v"
  echo "$v $dur s, lt10 $(stat -c %s "lt10/$v") bytes"
done
rm -f ffmpeg2pass-0.log ffmpeg2pass-0.log.mbtree
