# Indy re-voices + teaser CTA lines (Chatterbox, alone), then whisper picks + Indy re-time
I="/d/why habibi/_newchannel/15_uss_indianapolis"; PY="E:/AskHabibiAI/venv-chatterbox/Scripts/python.exe"; CT="/d/why habibi/_newchannel/_cta"
UV="uv run --no-project --with faster-whisper --with soundfile --with numpy python"
cd "$I/vo" && rm -f takes/line_12_* takes/line_35_* takes/line_52_* takes/line_61_* && HF_HUB_OFFLINE=1 "$PY" fix_lines.py gen 12 35 52 61 > fixgen.log 2>&1; echo "indy gen exit $? $(ls takes | wc -l) takes $(date +%T)"
cd "$CT" && HF_HUB_OFFLINE=1 "$PY" cta_teasers.py indy coleroe > cta_indy_coleroe.log 2>&1; echo "cta gen exit $? $(date +%T)"
cd "$I/vo" && $UV fix_lines.py pick 12 35 52 61 > fixpick.log 2>&1 && $UV retime_words.py 12 35 52 61 > retime.log 2>&1; echo "indy pick+retime exit $? $(date +%T)"
cd "$CT" && $UV pick_teasers.py indy coleroe > pick_indy_coleroe.log 2>&1; echo "cta pick exit $? $(date +%T)"
