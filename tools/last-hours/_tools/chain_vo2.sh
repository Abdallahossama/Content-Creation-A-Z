# after the Indianapolis OCR: re-voice 4 Indy lines (Chatterbox), pick + splice + re-time, then the Cole & Roe VO (Chatterbox alone)
I="/d/why habibi/_newchannel/15_uss_indianapolis"; C="/d/why habibi/_newchannel/16_cole_roe_1937"; PY="E:/AskHabibiAI/venv-chatterbox/Scripts/python.exe"
while powershell -NoProfile -Command "if (Get-CimInstance Win32_Process -Filter \"Name like 'python%'\" | Where-Object { \$_.CommandLine -match 'ocr_pages' }) { exit 0 } else { exit 1 }"; do sleep 10; done
echo "ocr done $(ls $I/build/ocr | wc -l) pages $(date +%T)"
cd "$I/vo" && HF_HUB_OFFLINE=1 "$PY" fix_lines.py gen 12 35 52 61 > fixgen.log 2>&1; echo "indy fix gen exit $? $(date +%T)"
cd "$I/vo" && uv run --no-project --with faster-whisper --with soundfile --with numpy python fix_lines.py pick 12 35 52 61 > fixpick.log 2>&1; echo "indy fix pick exit $? $(date +%T)"
cd "$I/vo" && uv run --no-project --with faster-whisper --with soundfile --with numpy python retime_words.py 12 35 52 61 > retime.log 2>&1; echo "indy retime exit $? $(date +%T)"
cd "$C/vo" && HF_HUB_OFFLINE=1 "$PY" vo_chatterbox.py "E:/AskHabibiAI/voice/ref_s01_12s.wav" "D:/why habibi/_newchannel/16_cole_roe_1937/vo/coleroe_vo_chatterbox.wav" "D:/why habibi/_newchannel/16_cole_roe_1937/vo/vo_tts.txt" > vo.log 2>&1; echo "coleroe vo exit $? $(date +%T)"
