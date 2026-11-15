PY=/e/AskHabibiAI/venv-chatterbox/Scripts/python.exe; T=/d/the-bill-explained/tools; V=/d/the-bill-explained/videos/01_diesel
export HF_HUB_OFFLINE=1 HF_HOME=E:/AskHabibiAI/hf TMP=D:/tmp TEMP=D:/tmp TMPDIR=D:/tmp UV_CACHE_DIR=D:/tmp/uvcache
for s in s1_gap s2_semi; do
  cd "$V/shorts/$s/vo" && "$PY" $T/vo_chatterbox.py "E:/AskHabibiAI/voice/ref_s01_12s.wav" "D:/the-bill-explained/videos/01_diesel/shorts/$s/vo/vo.wav" "D:/the-bill-explained/videos/01_diesel/shorts/$s/vo/vo_tts.txt" > vo.log 2>&1; echo "$s vo $? $(date +%T)"
done
P="diesel, gasoline, EIA, Energy Information Administration, Hormuz, Ryazan, Benicia, crack spread, Treasury, semi, Farm Bureau"
cd $T
for r in "$V" "$V/shorts/s1_gap" "$V/shorts/s2_semi"; do
  HF_HOME=C:/Users/ossam/.cache/huggingface uv run --no-project --with faster-whisper --with soundfile --with numpy python transcribe_lines.py "$r" "$P" > "$r/vo/transcribe.log" 2>&1; echo "words $r $? $(date +%T)"
done
