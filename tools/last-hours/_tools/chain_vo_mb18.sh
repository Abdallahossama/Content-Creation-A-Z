# File 18 Muslim Brotherhood: Chatterbox VO (alone: nothing else rendering, LESSONS 43), then whisper word times + QA lines
G="/d/why habibi/_newchannel/18_muslim_brotherhood"
cd "$G/vo" && HF_HUB_OFFLINE=1 "E:/AskHabibiAI/venv-chatterbox/Scripts/python.exe" vo_chatterbox.py "E:/AskHabibiAI/voice/ref_s01_12s.wav" "D:/why habibi/_newchannel/18_muslim_brotherhood/vo/mb_vo_chatterbox.wav" "D:/why habibi/_newchannel/18_muslim_brotherhood/vo/vo_tts.txt" > vo.log 2>&1; echo "mb vo exit $? $(date +%T)"
grep -q WROTE vo.log || { echo "MB VO FAILED"; tail -5 vo.log; exit 1; }
uv run --no-project --with faster-whisper --with soundfile --with numpy python transcribe_lines.py > transcribe.log 2>&1; echo "mb transcribe exit $? $(date +%T)"
