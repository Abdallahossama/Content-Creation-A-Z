# Gaddafi 17 teasers (6 Nov): the spoken end line (Chatterbox ALONE, nothing else rendering), pick the cleanest take,
# then the 4 teasers one at a time and <10 MB 2-pass copies in teasers/lt10/
export PYTHONUTF8=1 HF_HUB_OFFLINE=1 PYTHONUNBUFFERED=1
C="/d/why habibi/_newchannel/_cta"; T="/d/why habibi/_newchannel/_tools"
cd "$C" && "/e/AskHabibiAI/venv-chatterbox/Scripts/python.exe" -u cta_teasers.py gaddafi17 > "$T/cta_gaddafi17.log" 2>&1; echo "cta voice exit $? $(date +%T)"
cd "$C" && uv run --no-project --with faster-whisper --with soundfile --with numpy python pick_teasers.py gaddafi17 >> "$T/cta_gaddafi17.log" 2>&1; echo "pick exit $? $(date +%T)"; grep PICK "$T/cta_gaddafi17.log"
cd "$T"; RUN="uv run --no-project --with pillow --with numpy --with soundfile python"
for n in T1_the_convoy T2_whose_aircraft T3_the_grenade T4_king_of_kings; do $RUN teasers_more.py render gaddafi17 $n >> "$T/teasers_gaddafi17.log" 2>&1; echo "gaddafi17 $n exit $? $(date +%T)"; done
cd "/d/why habibi/_newchannel/17_gaddafi_last_day/teasers" && mkdir -p lt10
for v in TheLastHours_Short_T*.mp4; do
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$v")
  vb=$(awk -v d="$dur" 'BEGIN{printf "%d", (9.4*8*1024*1024/d - 128000)}')
  ffmpeg -v error -y -i "$v" -c:v libx264 -b:v $vb -pass 1 -an -f mp4 NUL && ffmpeg -v error -y -i "$v" -c:v libx264 -b:v $vb -pass 2 -c:a aac -b:a 128k "lt10/$v"
  echo "$v $dur s, lt10 $(stat -c %s "lt10/$v") bytes"
done
rm -f ffmpeg2pass-0.log ffmpeg2pass-0.log.mbtree
