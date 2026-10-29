---
name: clean-voice-mix
description: "'Whoosh when I speak' = my VO join saved the voice as 8-BIT (ffmpeg concat with anullsrc→u8). Decode ElevenLabs MP3s straight to float; check bit depth"
metadata:
  node_type: memory
  type: feedback
  originSessionId: eff32ef8-e3b2-4b1b-abb9-4566220676dd
  modified: 2026-10-12T21:04:59.988Z
---

ROOT CAUSE (found 2026-10-13, after many wrong guesses): to join the ElevenLabs parts I used
`ffmpeg ... -f lavfi -i anullsrc ... concat`. lavfi anullsrc comes in as pcm_u8, and concat negotiated the WHOLE voice down
to **8-bit**. The joined WAV had only 209 distinct sample values. 8-bit quantization noise = "a whoosh while I speak that
stops when I stop".

It poisoned every Ep 4 version. Ep 3's `ep03_vo_joined.wav` has the same 8-bit damage (Ep 1 and Ep 2 are fine). The user
proved it in CapCut: the raw MP3 is clean, vo_timeline.wav is not.

My wrong turns: blamed the music duck, SFX, room tone, sibilance (de-esser), breaths, the limiter. I also told the user a
file was "identical to ElevenLabs" when it was derived from the 8-bit join. Never claim identity without comparing
against the original MP3 itself.

**Rules:**
- Decode ElevenLabs MP3s straight to float32 in Python (`ep04_common.vo_untouched()`). Insert silence as numpy zeros.
- Never concat with anullsrc. If ffmpeg must join, force `aformat=sample_fmts=fltp` on EVERY input.
- QA every voice file for bit depth: distinct values, share of samples on 256-steps (must be ~0.3%, not 100%).
- Ep 4 voice is now untouched (no limiter, -21 LUFS master via `audio_master.gain_only`). Whether a gentle limiter is fine
  on clean audio is untested; ask before making it louder.
- Music flat under spoken passages, no whoosh SFX under the voice, no room_tone (harmless, keep).

**Why:** the user is extremely sensitive to anything riding on their cloned voice, and three rounds were lost guessing.
**How to apply:** when the user reports noise on the voice, first compare each stage against the source MP3
sample-by-sample. Give them CapCut stems early; they found the culprit by muting tracks.
Related: [[doc-mode]], [[episode-status]].

Shorts music level (user, 18 Oct 2026: "where is the background music"): -21 dB under the VO was inaudible on a phone. Now
`shortkit.mix()` ducks the CC-BY bed to -15 dB under speech and -10 dB in pauses longer than 0.3 s (attack 60 ms, release
400 ms); measured ~12 dB below speech in pauses (old mix: ~18 dB). Every Short uses it; long videos keep the old quieter rule
unless the user says otherwise.

UPDATE 25 Oct 2026 (The Last Hours, Gaddafi file): the user asked "make the music more listened, a little bit louder, and much shown at the
beginning". New Last Hours levels (music() in the renderers, dB vs the voice RMS): cold open (line 0 to the date line) -11, easing to -15,
then -17 for the body (-18 in the execution/stadium chapter), -16 for the ending. Measured: ~13 dB under the voice in pauses. This replaces
the old "19-22 dB under the voice" rule for Last Hours long files.
