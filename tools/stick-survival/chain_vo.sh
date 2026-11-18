PY=/e/AskHabibiAI/venv-chatterbox/Scripts/python.exe; T=/f/stick-survival/tools; r=$1
export HF_HUB_OFFLINE=1 TMP=D:/tmp TEMP=D:/tmp TMPDIR=D:/tmp UV_CACHE_DIR=D:/tmp/uvcache
for try in 1 2 3; do
  cd "$r/vo" && HF_HOME=E:/AskHabibiAI/hf "$PY" $T/vo_chatterbox.py "E:/AskHabibiAI/voice/ref_s01_12s.wav" "$r/vo/vo.wav" "$r/vo/vo_tts.txt" > vo.log 2>&1; rc=$?; echo "vo try $try rc $rc $(date +%T)"
  [ $rc -eq 0 ] && break
done
cd $T && HF_HOME=C:/Users/ossam/.cache/huggingface uv run --no-project --with faster-whisper --with soundfile --with numpy python transcribe_lines.py "$r" "$2" > "$r/vo/transcribe.log" 2>&1; echo "words $? $(date +%T)"
grep -c . $r/vo/qa_lines.txt; awk '$2<0.8' $r/vo/qa_lines.txt | head -20
