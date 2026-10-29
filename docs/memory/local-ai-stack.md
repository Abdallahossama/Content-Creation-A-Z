---
name: local-ai-stack
description: "Ask Habibi local/free production stack on E:\\AskHabibiAI (Chatterbox voice clone approved, Blender 3D, Qwen3-TTS); setup gotchas and speeds"
metadata:
  node_type: memory
  type: project
  originSessionId: eff32ef8-e3b2-4b1b-abb9-4566220676dd
  modified: 2026-10-18T08:11:01.527Z
---

Since 2026-10-18 the user wants everything made locally and free (no ElevenLabs spend). Stack on `E:\AskHabibiAI`:
- **Voice:** Chatterbox Turbo (MIT) in `venv-chatterbox` (Python 3.12), model in `hf/` (HF_HOME). Conditioned on a 13 s
  clip of the user's own ElevenLabs clone voice (`voice/ref_s01_12s.wav`, from Short #1). User verdict: "very good".
  ~37 s of narration in ~2.3 min on CPU. Script: `_pipeline/shorts/s02_hypnic_jerk/vo_chatterbox.py` (one sentence per
  call, trimmed, pauses). Qwen3-TTS 1.7B-Base (Apache) in `venv-qwen` as the backup.
- **3D:** Blender 5.2.2 portable (`blender/`), Eevee on the Radeon 780M via HIP (~7 s/frame 1080x1920, 16-32 samples).
  3D Batata = UV sphere + real potato photo front-projected + face PNG layers (shock/xray via object properties).
  Scripts: `_pipeline/shorts/s02_hypnic_jerk/scene.py` + `anim.py` (beats.json from whisper word times).
- **Assets:** Poly Haven CC0 via API (`assets/polyhaven/`); Quaternius CC0 packs available.

**Gotchas:** uv's Python 3.11 link is broken here → use 3.12. Hugging Face Xet downloads stall → `HF_HUB_DISABLE_XET=1`.
Chatterbox's watermark module needs `setuptools<80` (pkg_resources). Keyframes closer than 1 frame overwrite each other.
Ask before downloading anything new. Related: [[shorts-standalone-only]], [[potato-cast-brand]], [[clean-voice-mix]].

3D props gotcha (user spotted it in the scheduled hypnic-jerk Short, 18 Oct 2026): the Poly Haven nightstand top is at z=0.70, not 0.62,
so the alarm clock, mug and phone were sunk into / floating off the table; the clock hands were separate glTF roots and the
clock glass rendered as a black disc in Eevee. Fixed in `batata3d.import_gltf(..., surface=z)` (one parent empty, sits the lowest
point on the surface) + `clear_glass()`. Rule: before any final 3D render, render stills of EVERY shot that shows props and
check they rest on surfaces; `B3.render(mode="visible")` lists the frames that show given objects for partial re-renders.

21 Oct 2026: Chatterbox MULTILINGUAL downloaded (user approved; ResembleAI/chatterbox, MIT, 3.21 GB in hf/) -> Arabic ("ar") + 22 other
languages in the user's cloned voice: from chatterbox.mtl_tts import ChatterboxMultilingualTTS (venv-chatterbox). Qwen3-TTS has NO Arabic
and is very slow on this CPU (~30x real time); user rejected it. NEVER time-stretch the cloned voice (Rubber Band slow-down made it "really bad").
