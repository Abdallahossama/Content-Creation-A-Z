# Free tools research: voice cloning, Higgsfield replacement, Zack D. Films (18 Oct 2026)

Three research agents (web + Reddit via archives + licence files), plus our own scan of 400 Zack D. Films Shorts
(`../2026-10-18_zackdfilms/`). Items marked (unverified) could not be confirmed at a primary source.

**His PC:** AMD Ryzen 7 8700G, integrated Radeon 780M (RDNA3, gfx1103, shares system RAM), 30 GB RAM, no NVIDIA GPU.
Free disk: C 17 GB, D 54 GB, E 79 GB, F 34 GB. Location: Egypt (matters for some licences).

---------------------------------------------------------------------------------------------------------------------
## 1. Free voice cloning (replace ElevenLabs)

| # | Model | Licence code / weights → monetized YouTube? | Clone quality | Long-form | On his 8700G (5-min VO, estimated) |
|---|---|---|---|---|---|
| 1 | **Qwen3-TTS 1.7B-Base** (Jan 2026) | Apache-2.0 / Apache-2.0 → yes | upper tier (#6/28 blind vote); pronunciation/context weak until fine-tuned | chunk ~256 chars | CPU ~25-35 min; GGUF builds faster (unverified) |
| 2 | **Chatterbox Turbo / Nano / Multilingual V3** (Resemble) | MIT / MIT → yes | mid tier (#12/#14 blind vote) | chunking (servers do it) | Turbo ~6-12 min; Nano ~2 min (vendor claim) |
| 3 | **IndexTTS-2** (2.5 Aug 2026) | bilibili licence → yes under 100M MAU / RMB 1bn | top tier (#3) with emotion control | stable, memory-hungry | CPU impractical → free cloud |
| HM | Pocket TTS (Kyutai 100M) | MIT / CC-BY-4.0 (credit) → yes | mid (#8), needs very clean reference | streams | ~1-2 min (fastest CPU cloner) |
| HM | VoxCPM2 | Apache / Apache | voice drifts between takes | warns on long input | cloud |
| HM | Higgs TTS 3 (Boson) | research licence + "Creator Use Grant" (visible credit) | expressive | chunk | cloud |
| HM | RVC via Applio | MIT | very high similarity after 10-30 min training | n/a (converts audio) | CPU to run, cloud to train |

**Not for monetized use:** F5-TTS / E2 (CC-BY-NC), XTTS-v2 (Coqui non-commercial, company gone), OmniVoice (NC since
3 Jul 2026), Echo-TTS, Spark-TTS (CC-BY-NC-SA), Fish S2-Pro / S1-mini, Voxtral TTS (NC), Breeze-TTS-2.
Skip: VibeVoice (research-only, audible AI disclaimer), MegaTTS3 (voice upload to ByteDance), ZONOS2 (Linux+NVIDIA),
Kokoro (no cloning), XTTS/OpenVoice/StyleTTS2 (bottom of blind vote).

**Best setup for his PC:** audio.cpp v0.9.2 (Apache-2.0, native Windows CPU + Vulkan builds, web UI, runs Qwen3-TTS /
Chatterbox / Pocket / IndexTTS-2 / VoxCPM2) → Qwen3-TTS 1.7B-Base Q8, one clean deadpan 10-20 s reference + its exact
transcript, chunks ~256 chars. A/B against Chatterbox Turbo and Pocket with the same reference. If not close enough:
fine-tune Qwen3 on 10-30 min of his clean speech on Kaggle. Easiest GUI: Chatterbox-TTS-Server (MIT, portable Windows,
chunks long scripts). Voicebox (MIT) is CPU-only on AMD.
**AMD:** gfx1103 PyTorch wheels exist for Windows, but the audio.cpp ROCm contributor says 780M performance is
"severely insufficient"; plan CPU-first, test Vulkan.
**Free cloud:** Kaggle (T4/P100, ~30 GPU h/week user-reported, 12 h sessions); Colab free bans web UIs and "creating
deepfakes" (code cells only); HF ZeroGPU 5 min/day (auditions only).
**Reddit:** Chatterbox "11labs quality… much better than xtts" vs "Turbo so-so"; IndexTTS2 "slept on"; VibeVoice
"very unstable"; Chatterbox CPU 27 s for 8 s audio on one Windows PC; Qwen3 own-voice fine-tune helps; "do not use the
780M" (audio.cpp ROCm dev); a creator using his own cloned voice 4 months: viewers didn't notice, emotional range weak.
Threads: r/LocalLLaMA 1q2sfwx, 1s9th61, 1ssugid, 1v4w5cj, 1shn6h4; r/ROCm 1ufmtez; r/TextToSpeech 1vlo1dw, 1v8mop3
(astroturf warning); r/LocalLLM 1uh2xyh; r/YouTubeCreators 1ssbse7. Blind votes: github.com/5uck1ess/tts-bench.
**Gotchas:** licences change (save each LICENSE with the model); Pocket/Higgs need a credit; clone only his own voice.
YouTube Help 14328491 lists "cloning one's own voice to create voice overs or dubs" among uses that do NOT need the
altered-content label (check the page; our upload rule still says Yes).
Sources: github.com/resemble-ai/chatterbox · huggingface.co/ResembleAI/chatterbox(-nano) · github.com/QwenLM/Qwen3-TTS ·
huggingface.co/IndexTeam/IndexTTS-2.5 · huggingface.co/kyutai/pocket-tts · huggingface.co/openbmb/VoxCPM2 ·
huggingface.co/bosonai/higgs-tts-3-4b · github.com/IAHispano/Applio · github.com/0xShug0/audio.cpp (model_licenses.md)
· research.google.com/colaboratory/faq.html · huggingface.co/docs/hub/spaces-zerogpu

---------------------------------------------------------------------------------------------------------------------
## 2. Higgsfield replacement (AI video/images)

Higgsfield is a paid front end, not its own model: it routes to closed models (Kling 3.0, Seedance 2.x, Veo 3.1,
Sora 2, Wan 2.6/2.7, MiniMax, Grok Imagine) and adds Soul/Soul ID images, Cinema Studio 4.0 (camera presets, 30 s,
1080p), LipSync Studio, Genjutsu (swap person/object). Open weights now rival those engines, but only on big GPUs
(Artificial Analysis board: open MiniMax H3 1159 vs Seedance 2.0 1136, Kling 3.0 Omni 1019, Veo 3.1 968).

| Capability | Best open pick | Commercial OK? | On his 780M? |
|---|---|---|---|
| Video, top quality | MiniMax H3 (Jul 2026, audio, 15 s) | community licence, OK under $20M; NOT for residents of US/EU/UK/S. Korea | no (33B + 32B encoder) |
| Video, safest licence | Wan 2.2 TI2V-5B / A14B + LightX2V 4-step | Apache-2.0 | barely: Wan 2.1-14B Q3 on a 780M = 4-6 h per 28-42 s clip |
| Video + audio 4K | LTX-2.5 | OK under $10M revenue | no (NVIDIA ≥15 GB) |
| Small video + lip-sync | Kandinsky 6.0 Lite 3B | MIT | untested, only one worth trying |
| Camera motion | Wan 2.2 Fun Camera, LTX camera LoRAs | as base | no |
| Consistent characters | Qwen-Image-Edit-2511 (Apache), FLUX.2 klein 4B (Apache), FLUX 3 Image Klein (under $5M) + own LoRA | yes | images slow; LoRA training in cloud |
| Lip-sync | MuseTalk (MIT, weights commercial OK), InfiniteTalk/MultiTalk (Apache), LatentSync 1.6 (OpenRAIL++) | yes (Wav2Lip is NOT) | MuseTalk maybe; rest no |
| Images | Z-Image-Turbo (Apache), FLUX.1-schnell (Apache), SDXL | yes (avoid FLUX.1-dev, FLUX.2-dev, FLUX.2-klein-9B, Qwen-Image-2.1) | yes: Z-Image-Turbo ~40 s per 720x1280; SDXL ~2 min |
| Upscale / interpolation | Upscayl (Real-ESRGAN, AGPL), RIFE ncnn-vulkan (MIT), SeedVR2 (Apache) | yes | Upscayl/RIFE yes |
| 3D | TRELLIS.2 (MIT), Hunyuan3D 2.1 (excl. EU/UK/SK) | yes | no (use free online demos) |

**AMD:** AMD now publishes Windows PyTorch wheels for gfx1103 (ROCm 7.14/10.x); ComfyUI has an AMD Windows build;
780M owners still report crashes ("much better after 7.14"). The real limit is hardware: 12 CUs on shared DDR5.
**Verdict for his PC:** images yes (Z-Image-Turbo / FLUX.2 klein 4B in ComfyUI), upscaling yes, video realistically no.
Disk: one video model + encoder = 20-45 GB.
**Free cloud:** Kaggle 2xT4, ~30 h/week (third-party figure) with ComfyUI/WanGP + Wan 2.2 GGUF + LightX2V, est. 5-15 min
per 5 s 480p clip (unverified); HF ZeroGPU 5 min/day for demos; Modal $30/month credit; avoid free Colab for web UIs
(ToS) and deepfakes (banned).
**Reddit:** "open source alternative to Higgsfield" = BYO-API front end, Higgsfield marks up 2-4x (r/StableDiffusion
1sgrgef); "Minimax H3 is as close as you'll get" (1wpnmms); 780M Wan 4-6 h per clip (u/Mr_hexadus 1v72luj); 780M
Z-Image ~40 s (1rojwgk); 8700G FLUX "S L O W" (1if2t2i); 780M crashes (r/ROCm 1wxk8le); free Kaggle LTX notebook
(1vkhq2p).
Sources: higgsfield.ai · artificialanalysis.ai video leaderboard · huggingface.co/Wan-AI · LTX-2 LICENSE ·
MiniMax-H3 LICENSE · Kandinsky-6.0-Lite · FLUX.2-klein-4B · bfl.ai FLUX 3 klein · Z-Image-Turbo · MuseTalk · InfiniteTalk
· LatentSync · Wav2Lip · rocm.docs.amd.com (PyTorch install) · ROCm/TheRock SUPPORTED_GPUS.md · Comfy-Org/ComfyUI ·
Wan2GP AMD-INSTALLATION.md · support.google.com/youtube/answer/1311392 and 14328491.

---------------------------------------------------------------------------------------------------------------------
## 3. Zack D. Films: how it's made

- 29.2M subs, 80.3B views, 4,088 videos since Jun 2021 (~2 uploads/day). Owner "Zack"; "Zack D Films LLC". No process
  interview found. Started with 5-min documentaries (Pepsi contest, Toyota, Ohio balloons), now almost all Shorts.
- **Pipeline (contractor accounts):** voiceover first ("your animation basis"); a pool of remote 3D contractors with
  strict guidelines on content, framing and pacing; channel-supplied characters/assets + look guide; Blender Cycles,
  sometimes Unreal; ~$1k per video, 2-week turnaround (r/blender 1rdsh5v, 1ufn5pp; portfolio
  supersets.chrisreillyportfolio.com/zackdfilms.php: Blender, Cascadeur, BlenderKit, After Effects, EmberGen, Flamenco
  render farm); hiring page zackdfilms.recruitee.com (20-45 s, 9:16, unpaid test).
- **Formula** (our scan of 400 Shorts: median 9.95M views, very consistent): 20-45 s; hook in 1-2 s; Title Case 4-8
  words + one emoji at the end (🤔 97, 😮 95, 😨/🤨 31); topics = body & medicine, survival, odd history, animals (the top
  2: toucan beak 54M, cookiecutter shark 53M), how-it-was-made; extreme close-ups mid-action from frame 1; 1-3 white
  caption words; glow on the point of contact; meme SFX; narration that loops. The doll-like, untextured 3D look shows
  injuries without real gore (closer to ad-safe) and is cheap to mass-produce.
- **Money:** Shorts revenue, Patreon, merch, brand page partners.zackdfilms.com (up to $250k+).
- **Policy risk for imitators:** YouTube's inauthentic-content update (Jul 2025; Tubefilter 13 Jul 2026) demonetizes
  content that "mimic[s] existing formats or stories to a degree that the videos feel interchangeable" and templated,
  mass-produced AI content; reported Jan 2026 wipe of 16 AI channels (~35M subs). YPP changes from 1 Feb 2027 (new
  thresholds per vidIQ, unverified).
- **Free pipeline:** own voice; Blender (GPL) Eevee + Rigify; MPFB2/MakeHuman (CC0 exports), Mixamo (royalty-free, no
  raw redistribution), Quaternius/Kenney/Poly Haven (CC0), Blender Studio chars (CC-BY), BlenderKit free, Sketchfab
  CC0/CC-BY only; TRELLIS.2 (MIT) online demo for props; avoid Cascadeur Free (non-commercial). Unreal/MetaHuman licence
  is free but needs an RTX 3070-class GPU.
- **On his PC:** Blender HIP supports the 780M (driver ≥24.9.1), benchmark ~268 vs ~2,300 RTX 3060 (8-9x slower).
  45 s Short (1,080 frames 1080x1920): Eevee ~20-70 min; Cycles 64 spp ~6-18 h.
- **Time cost (beginner):** ~100-150 h learning first; then ~25-40 h per 45 s Short, ~12-20 h with templates → about one
  Short a week (Zack's team: ~2 a day).
- **Reddit:** the unpaid test = "free labour"; clone channels often stall (145 subs after 20 videos); AI-only clones
  ("looks godawful"); demonetized animators reinstated after documenting their process.

---------------------------------------------------------------------------------------------------------------------
## Recommendation for Ask Habibi
1. Voice: test Qwen3-TTS and Chatterbox Turbo locally against an ElevenLabs take of the same script; keep the free one
   only if it passes a blind listen. Recording his own voice stays the cheapest, best and safest option.
2. Visuals: no local AI video on this PC. Use local AI images only if he drops the "no AI images" rule; Kaggle for any
   AI video experiments.
3. Zack D. Films: copy the FORMULA (frame-1 payoff, 20-45 s, one surprising fact, "How/Why…" + emoji, loop), not the 3D
   look; the potato-cast map engine already makes a Short in hours, and Short #1 is the channel's best video.
