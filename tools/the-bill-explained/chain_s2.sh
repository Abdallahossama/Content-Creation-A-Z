export HF_HUB_OFFLINE=1 HF_HOME=E:/AskHabibiAI/hf TMP=D:/tmp TEMP=D:/tmp TMPDIR=D:/tmp UV_CACHE_DIR=D:/tmp/uvcache
V=/d/the-bill-explained/videos/01_diesel/shorts/s2_semi
cd $V/vo && /e/AskHabibiAI/venv-chatterbox/Scripts/python.exe /d/the-bill-explained/tools/vo_chatterbox.py "E:/AskHabibiAI/voice/ref_s01_12s.wav" "$V/vo/vo.wav" "$V/vo/vo_tts.txt" > vo.log 2>&1; echo "vo $?"
cd /d/the-bill-explained/tools && HF_HOME=C:/Users/ossam/.cache/huggingface uv run --no-project --with faster-whisper --with soundfile --with numpy python transcribe_lines.py "$V" "diesel, semi" > $V/vo/transcribe.log 2>&1; echo "words $?"
