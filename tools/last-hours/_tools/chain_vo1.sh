# wait for the Indianapolis VO, then: whisper word times + QA, OCR of the Navy pages, then the Cole & Roe VO (Chatterbox alone, LESSONS 35)
I="/d/why habibi/_newchannel/15_uss_indianapolis"; C="/d/why habibi/_newchannel/16_cole_roe_1937"
until grep -q "WROTE\|Traceback\|Error" "$I/vo/vo.log"; do sleep 5; done
grep -q WROTE "$I/vo/vo.log" || { echo "INDY VO FAILED"; exit 1; }
echo "indy vo done $(date +%T)"
cd "$I/vo" && uv run --no-project --with faster-whisper --with soundfile --with numpy python transcribe_lines.py > transcribe.log 2>&1; echo "indy transcribe exit $? $(date +%T)"
cd "$I" && uv run --no-project --with rapidocr_onnxruntime python ../_tools/ocr_pages.py "$I" build/pages/A[1-8]p*.jpg > build/ocr_pages.log 2>&1; echo "indy ocr exit $? $(date +%T)"
cd "$C/vo" && HF_HUB_OFFLINE=1 "E:/AskHabibiAI/venv-chatterbox/Scripts/python.exe" vo_chatterbox.py "E:/AskHabibiAI/voice/ref_s01_12s.wav" "D:/why habibi/_newchannel/16_cole_roe_1937/vo/coleroe_vo_chatterbox.wav" "D:/why habibi/_newchannel/16_cole_roe_1937/vo/vo_tts.txt" > vo.log 2>&1; echo "coleroe vo exit $? $(date +%T)"
