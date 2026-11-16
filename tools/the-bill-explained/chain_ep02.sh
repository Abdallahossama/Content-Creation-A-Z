PY=/e/AskHabibiAI/venv-chatterbox/Scripts/python.exe; T=/d/the-bill-explained/tools; V=/d/the-bill-explained/videos/02_ai_power
export HF_HUB_OFFLINE=1 TMP=D:/tmp TEMP=D:/tmp TMPDIR=D:/tmp UV_CACHE_DIR=D:/tmp/uvcache
for r in "$V" "$V/shorts/s1_homes" "$V/shorts/s2_auction"; do
  cd "$r/vo" && HF_HOME=E:/AskHabibiAI/hf "$PY" $T/vo_chatterbox.py "E:/AskHabibiAI/voice/ref_s01_12s.wav" "$r/vo/vo.wav" "$r/vo/vo_tts.txt" > vo.log 2>&1; echo "vo $r $? $(date +%T)"
done
P="PJM, data center, kilowatt-hour, Berkeley Lab, Abilene, Oracle, OpenAI, Meta Hyperion, megawatt, gigawatt, Dallas Fed, EIA, New Jersey, Maryland, Virginia"
cd $T
for r in "$V" "$V/shorts/s1_homes" "$V/shorts/s2_auction"; do
  HF_HOME=C:/Users/ossam/.cache/huggingface uv run --no-project --with faster-whisper --with soundfile --with numpy python transcribe_lines.py "$r" "$P" > "$r/vo/transcribe.log" 2>&1; echo "words $r $? $(date +%T)"
done
