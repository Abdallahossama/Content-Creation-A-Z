# File 17 Gaddafi: Chatterbox VO (alone: nothing else rendering, LESSONS 35), then whisper word times + QA lines
G="/d/why habibi/_newchannel/17_gaddafi_last_day"
cd "$G/vo" && HF_HUB_OFFLINE=1 "E:/AskHabibiAI/venv-chatterbox/Scripts/python.exe" vo_chatterbox.py "E:/AskHabibiAI/voice/ref_s01_12s.wav" "D:/why habibi/_newchannel/17_gaddafi_last_day/vo/gaddafi_vo_chatterbox.wav" "D:/why habibi/_newchannel/17_gaddafi_last_day/vo/vo_tts.txt" > vo.log 2>&1; echo "gaddafi vo exit $? $(date +%T)"
grep -q WROTE vo.log || { echo "GADDAFI VO FAILED"; tail -5 vo.log; exit 1; }
uv run --no-project --with faster-whisper --with soundfile --with numpy python transcribe_lines.py > transcribe.log 2>&1; echo "gaddafi transcribe exit $? $(date +%T)"
