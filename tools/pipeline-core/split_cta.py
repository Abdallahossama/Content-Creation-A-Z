"""Split ONE ElevenLabs recording that contains many lines into separate, levelled clips.
Lines are found by their words (Whisper word timestamps + fuzzy match), so pause length doesn't matter.

usage: python split_cta.py <recording> [out_dir] [--targets targets.json]
default targets = the generic Shorts end lines (GENERIC_CTA in shorts.py) -> D:\\why habibi\\_cta_library\\"""
import json, os, re, subprocess, sys, tempfile, difflib
import numpy as np, soundfile as sf

DEFAULT_TARGETS = {
    "cta_to_part2_A": "Part two is already on my profile. Subscribe, so the next one finds you.",
    "cta_to_part3_A": "Part three is waiting on my profile. Go check it, then subscribe.",
    "cta_to_part4_A": "Part four is on my profile. Subscribe for the rest.",
    "cta_to_part5_A": "Part five is on my profile. Subscribe so you don't miss it.",
    "cta_full_video_A": "That's the short version. The full video is on my channel. Subscribe, and send me your next midnight question.",
    "cta_to_part2_B": "This is only part one. Part two is on my profile. Subscribe, then go watch it.",
    "cta_to_part3_B": "It gets deeper. Part three is on my profile. Subscribe.",
    "cta_to_part4_B": "Don't stop here. Part four is on my profile. Subscribe for the rest.",
    "cta_to_part5_B": "One part left. Part five is on my profile. Subscribe so you catch it.",
    "cta_full_video_B": "Want the full answer? It's on my channel. Subscribe, so the next midnight question finds you.",
}
NUM = {"2": "two", "3": "three", "4": "four", "5": "five", "1": "one"}

def norm(t):
    t = t.lower().replace("’", "'")
    t = re.sub(r"\b(\d)\b", lambda m: NUM.get(m.group(1), m.group(1)), t)
    return re.sub(r"[^a-z' ]+", " ", t).split()

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    src = args[0]
    out = args[1] if len(args) > 1 else "D:/why habibi/_cta_library/"
    targets = DEFAULT_TARGETS
    if "--targets" in sys.argv:
        targets = json.load(open(sys.argv[sys.argv.index("--targets") + 1], encoding="utf-8"))
    os.makedirs(out, exist_ok=True)
    tmp = tempfile.mkdtemp()
    w16 = os.path.join(tmp, "a16.wav"); w48 = os.path.join(tmp, "a48.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ac", "1", "-ar", "16000", w16], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ac", "2", "-ar", "48000", w48], check=True)
    from faster_whisper import WhisperModel
    audio, _ = sf.read(w16, dtype="float32")
    segs, _ = WhisperModel("medium.en", device="cpu", compute_type="int8").transcribe(audio, word_timestamps=True, beam_size=5)
    words = [(w.word, w.start, w.end) for s in segs for w in s.words]
    toks = []                                   # normalised token -> word index
    for i, (w, a, b) in enumerate(words):
        for t in norm(w): toks.append((t, i))
    seq = [t for t, _ in toks]
    found, used = {}, set()
    cands = []
    for stem, line in targets.items():
        tl = norm(line); n = len(tl)
        for L in range(max(1, n - 3), n + 4):
            for i in range(0, max(1, len(seq) - L + 1)):
                r = difflib.SequenceMatcher(None, tl, seq[i:i + L]).ratio()
                if r >= 0.72: cands.append((r, stem, i, i + L))
    for r, stem, i0, i1 in sorted(cands, reverse=True):          # best matches first, no overlaps
        if stem in found or any(k in used for k in range(i0, i1)): continue
        found[stem] = (toks[i0][1], toks[i1 - 1][1], r); used.update(range(i0, i1))
    full, sr = sf.read(w48, dtype="float32")
    starts = sorted(a for _, a, _ in words)
    for stem, (w0, w1, r) in sorted(found.items(), key=lambda x: x[1][0]):
        a = max(0.0, words[w0][1] - 0.15); b = words[w1][2] + 0.30
        nxt = [s for s in starts if s > words[w1][2] + 0.05]
        if nxt: b = min(b, nxt[0] - 0.05)
        clip = full[int(a * sr):int(b * sr)].copy()
        fi, fo = int(0.01 * sr), int(0.06 * sr)
        clip[:fi] *= np.linspace(0, 1, fi)[:, None]; clip[-fo:] *= np.linspace(1, 0, fo)[:, None]
        raw = os.path.join(tmp, stem + ".wav"); sf.write(raw, clip, sr)
        dst = os.path.join(out, stem + ".mp3")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000",
                        "-c:a", "libmp3lame", "-b:a", "192k", dst], check=True)
        print(f"  {stem:20s} {b - a:5.2f}s  match {r:.2f}  \"{' '.join(w for w, _, _ in words[w0:w1 + 1]).strip()}\"")
    missing = [s for s in targets if s not in found]
    print(f"\n{len(found)}/{len(targets)} lines saved to {out}" + (f"\nNOT FOUND: {missing}" if missing else ""))

if __name__ == "__main__":
    main()
