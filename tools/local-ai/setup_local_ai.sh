#!/usr/bin/env bash
# Ask Habibi local AI setup (approved by the user 18 Oct 2026). Everything lives on E:\AskHabibiAI.
#   venv-chatterbox : chatterbox-tts 0.1.7 (MIT) + torch 2.6 CPU      -> model ResembleAI/chatterbox-turbo (MIT, 4.0 GB)
#   venv-qwen       : qwen-tts 0.1.1 (Apache-2.0) + torch CPU         -> model Qwen/Qwen3-TTS-12Hz-1.7B-Base (Apache-2.0, 4.5 GB)
#   blender         : Blender 5.2.2 portable (GPL), sha256-verified
set -u
R="E:/AskHabibiAI"; export UV_CACHE_DIR="$R/uv-cache" HF_HOME="$R/hf" HF_HUB_DISABLE_SYMLINKS_WARNING=1 PYTHONUTF8=1
cd "$R"
step() { echo; echo "=== $(date +%H:%M:%S) $*"; }

step "Blender 5.2.2 download"
curl -s -L -o blender-5.2.2.sha256 https://download.blender.org/release/Blender5.2/blender-5.2.2.sha256
curl -L --retry 3 -o blender-5.2.2-windows-x64.zip https://download.blender.org/release/Blender5.2/blender-5.2.2-windows-x64.zip
want=$(grep "blender-5.2.2-windows-x64.zip" blender-5.2.2.sha256 | awk '{print $1}'); got=$(sha256sum blender-5.2.2-windows-x64.zip | awk '{print $1}')
echo "sha256 want $want"; echo "sha256 got  $got"
if [ "$want" = "$got" ] && [ -n "$want" ]; then
  uv run --no-project python -c "import zipfile; zipfile.ZipFile('blender-5.2.2-windows-x64.zip').extractall('blender')" && echo "BLENDER OK" && rm -f blender-5.2.2-windows-x64.zip
else echo "BLENDER CHECKSUM MISMATCH - not extracted"; fi

step "venv-chatterbox"
uv venv venv-chatterbox --python 3.11 -q && uv pip install -q --python venv-chatterbox/Scripts/python.exe chatterbox-tts==0.1.7 huggingface_hub && echo "CHATTERBOX PKG OK"
step "chatterbox-turbo model"
venv-chatterbox/Scripts/python.exe -c "from huggingface_hub import snapshot_download as s; print(s('ResembleAI/chatterbox-turbo'))" && echo "CHATTERBOX MODEL OK"

step "venv-qwen"
uv venv venv-qwen --python 3.11 -q && uv pip install -q --python venv-qwen/Scripts/python.exe qwen-tts==0.1.1 torch torchaudio huggingface_hub && echo "QWEN PKG OK"
step "Qwen3-TTS 1.7B Base model"
venv-qwen/Scripts/python.exe -c "from huggingface_hub import snapshot_download as s; print(s('Qwen/Qwen3-TTS-12Hz-1.7B-Base'))" && echo "QWEN MODEL OK"

step "DONE"; du -sh "$R"/* 2>/dev/null
