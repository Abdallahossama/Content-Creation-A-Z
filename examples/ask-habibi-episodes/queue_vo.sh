#!/bin/sh
# generate + transcribe the long-video voice-overs one after another (local Chatterbox clone, then faster-whisper)
cd "D:/why habibi"
until [ -f "6th video/vo/sub_mid.wav" ]; do sleep 15; done
for pair in "07_ancient_fun:7th video:ep07" "08_dog:8th video:ep08" "09_walking:9th video:ep09"; do
  ep=$(echo "$pair" | cut -d: -f1); dir=$(echo "$pair" | cut -d: -f2); tag=$(echo "$pair" | cut -d: -f3)
  P="_pipeline/episodes/ep$ep"
  E:/AskHabibiAI/venv-chatterbox/Scripts/python.exe _pipeline/shorts/s02_hypnic_jerk/vo_chatterbox.py E:/AskHabibiAI/voice/ref_s01_12s.wav "$dir/vo/${tag}_vo_chatterbox.wav" "$P/vo_lines.txt" > "$P/vo.log" 2>&1
  PYTHONUTF8=1 uv run --no-project --with faster-whisper --with soundfile python _pipeline/shorts/s02_hypnic_jerk/transcribe_vo.py "$dir/vo/${tag}_vo_chatterbox.wav" "$dir/vo/vo_words.json" > "$P/transcribe.log" 2>&1
  cp "$dir/vo/vo_words.json" "$dir/vo/vo_words.raw.json"; echo "DONE $tag"
done
