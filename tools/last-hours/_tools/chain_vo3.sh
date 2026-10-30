# Cole & Roe VO (alone), then the 4 Indianapolis re-voices (gen, pick, re-time), then Cole & Roe whisper word times
I="/d/why habibi/_newchannel/15_uss_indianapolis"; C="/d/why habibi/_newchannel/16_cole_roe_1937"; PY="E:/AskHabibiAI/venv-chatterbox/Scripts/python.exe"
cd "$C/vo" && HF_HUB_OFFLINE=1 "$PY" vo_chatterbox.py "E:/AskHabibiAI/voice/ref_s01_12s.wav" "D:/why habibi/_newchannel/16_cole_roe_1937/vo/coleroe_vo_chatterbox.wav" "D:/why habibi/_newchannel/16_cole_roe_1937/vo/vo_tts.txt" > vo.log 2>&1; echo "coleroe vo exit $? $(date +%T)"
cd "$I/vo" && HF_HUB_OFFLINE=1 "$PY" fix_lines.py gen 12 35 52 61 > fixgen.log 2>&1; echo "indy fix gen exit $? $(date +%T)"
cd "$I/vo" && uv run --no-project --with faster-whisper --with soundfile --with numpy python fix_lines.py pick 12 35 52 61 > fixpick.log 2>&1; echo "indy fix pick exit $? $(date +%T)"
cd "$I/vo" && uv run --no-project --with faster-whisper --with soundfile --with numpy python retime_words.py 12 35 52 61 > retime.log 2>&1; echo "indy retime exit $? $(date +%T)"
cd "$C/vo" && uv run --no-project --with faster-whisper --with soundfile --with numpy python transcribe_lines.py > transcribe.log 2>&1; echo "coleroe transcribe exit $? $(date +%T)"
