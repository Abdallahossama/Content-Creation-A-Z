# re-voice the misread lines (Chatterbox alone, one model at a time), then whisper pick + splice + re-time
I="/d/why habibi/_newchannel/15_uss_indianapolis"; C="/d/why habibi/_newchannel/16_cole_roe_1937"; PY="E:/AskHabibiAI/venv-chatterbox/Scripts/python.exe"
UV="uv run --no-project --with faster-whisper --with soundfile --with numpy python"
cd "$I/vo" && HF_HUB_OFFLINE=1 "$PY" fix_lines.py gen 12 35 52 61 > fixgen.log 2>&1; echo "indy gen exit $? $(date +%T)"
cd "$C/vo" && HF_HUB_OFFLINE=1 "$PY" fix_lines.py gen 62 67 > fixgen.log 2>&1; echo "coleroe gen exit $? $(date +%T)"
cd "$I/vo" && $UV fix_lines.py pick 12 35 52 61 > fixpick.log 2>&1 && $UV retime_words.py 12 35 52 61 > retime.log 2>&1; echo "indy pick+retime exit $? $(date +%T)"
cd "$C/vo" && $UV fix_lines.py pick 62 67 > fixpick.log 2>&1 && $UV retime_words.py 62 67 > retime.log 2>&1; echo "coleroe pick+retime exit $? $(date +%T)"
