#!/usr/bin/env bash
# Ask Habibi local AI setup (approved by the user 18 Oct 2026). Everything lives on E:\AskHabibiAI.
#   venv-chatterbox : chatterbox-tts 0.1.7 (MIT) + torch 2.6 CPU      -> model ResembleAI/chatterbox-turbo (MIT, 4.0 GB)
#   venv-qwen       : qwen-tts 0.1.1 (Apache-2.0) + torch CPU         -> model Qwen/Qwen3-TTS-12Hz-1.7B-Base (Apache-2.0, 4.5 GB)
#   blender         : Blender 5.2.2 portable (GPL), sha256-verified
set -u
R="E:/AskHabibiAI"; export UV_CACHE_DIR="$R/uv-cache" HF_HOME="$R/hf" HF_HUB_DISABLE_XET=1 HF_HUB_ENABLE_HF_TRANSFER=0 HF_HUB_DISABLE_SYMLINKS_WARNING=1 PYTHONUTF8=1
cd "$R"
step() { echo; echo "=== $(date +%H:%M:%S) $*"; }

if [ ! -d blender/blender-5.2.2-windows-x64 ]; then echo "run the Blender step first"; fi

step "venv-chatterbox"
[ -x venv-chatterbox/Scripts/python.exe ] || uv venv venv-chatterbox --python 3.12 -q; uv pip install -q --python venv-chatterbox/Scripts/python.exe chatterbox-tts==0.1.7 huggingface_hub && echo "CHATTERBOX PKG OK"
step "chatterbox-turbo model"
venv-chatterbox/Scripts/python.exe -c "from huggingface_hub import snapshot_download as s; print(s('ResembleAI/chatterbox-turbo'))" && echo "CHATTERBOX MODEL OK"

step "venv-qwen"
uv venv venv-qwen --python 3.12 -q && uv pip install -q --python venv-qwen/Scripts/python.exe qwen-tts==0.1.1 torch torchaudio huggingface_hub && echo "QWEN PKG OK"
step "Qwen3-TTS 1.7B Base model"
venv-qwen/Scripts/python.exe -c "from huggingface_hub import snapshot_download as s; print(s('Qwen/Qwen3-TTS-12Hz-1.7B-Base'))" && echo "QWEN MODEL OK"

step "DONE"; du -sh "$R"/* 2>/dev/null
