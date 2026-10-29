"""Insert a freshly generated voice line (e.g. the smooth mid-video subscribe line) into a finished long-video VO,
without re-generating or re-transcribing the rest: the hand-fixed vo_words.json is kept, later words are shifted.
  uv run --no-project --with faster-whisper --with soundfile python vo_insert.py <vo_dir> <src.wav> <out.wav> <at_s> <line.wav> [pad_s]
  -> <out.wav> and <vo_dir>/vo_words.json (the old file is kept once as vo_words.before_insert.json)
at_s must sit inside a pause (the chapter "##" gap): the line goes in there with pad_s of silence on both sides."""
import json, os, shutil, subprocess, sys
import numpy as np, soundfile as sf

def words_of(wav_path):
    from faster_whisper import WhisperModel
    tmp = wav_path + ".16k.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav_path, "-ac", "1", "-ar", "16000", tmp], check=True)
    a, _ = sf.read(tmp, dtype="float32"); os.remove(tmp)
    segs, _ = WhisperModel("medium.en", device="cpu", compute_type="int8", cpu_threads=8).transcribe(a, word_timestamps=True, beam_size=5, condition_on_previous_text=False)
    return [{"start": s.start, "end": s.end, "text": s.text, "words": [{"w": w.word, "s": w.start, "e": w.end, "p": w.probability} for w in s.words]} for s in segs]

def main():
    vo_dir, src, out, at, line = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]), sys.argv[5]
    pad = float(sys.argv[6]) if len(sys.argv) > 6 else 0.30
    y, sr = sf.read(src, dtype="float32"); l, sr2 = sf.read(line, dtype="float32"); assert sr == sr2, (sr, sr2)
    nz = np.where(np.abs(l) > 0.01)[0]; l = l[max(0, nz[0] - int(0.03 * sr)): nz[-1] + int(0.08 * sr)]
    ins = np.concatenate([np.zeros(int(pad * sr), np.float32), l, np.zeros(int(pad * sr), np.float32)]); i = int(at * sr); shift = len(ins) / sr
    sf.write(out, np.concatenate([y[:i], ins, y[i:]]), sr, subtype="FLOAT")
    wj = os.path.join(vo_dir, "vo_words.json"); bak = os.path.join(vo_dir, "vo_words.before_insert.json")
    if not os.path.exists(bak): shutil.copy(wj, bak)
    segs = json.load(open(wj, encoding="utf-8")); new = words_of(line)
    lead = (int(max(0, nz[0] - int(0.03 * sr))) / sr)                                  # words_of() timed the untrimmed line
    for s in new:
        s["start"] += at + pad - lead; s["end"] += at + pad - lead
        for w in s["words"]: w["s"] += at + pad - lead; w["e"] += at + pad - lead
    before, after = [], []                                                        # split at word level (a segment may span the gap)
    for s in segs:
        wb = [w for w in s["words"] if w["s"] < at]; wa = [w for w in s["words"] if w["s"] >= at]
        if wb: before.append(dict(s, start=wb[0]["s"], end=wb[-1]["e"], text="".join(w["w"] for w in wb), words=wb))
        if wa: after.append(dict(s, start=wa[0]["s"], end=wa[-1]["e"], text="".join(w["w"] for w in wa), words=wa))
    for s in after:
        s["start"] += shift; s["end"] += shift
        for w in s["words"]: w["s"] += shift; w["e"] += shift
    json.dump(before + new + after, open(wj, "w", encoding="utf-8"), indent=1)
    print(f"inserted {len(l) / sr:.2f}s line (+{shift:.2f}s) at {at:.2f}s:", " | ".join(s["text"] for s in new))

if __name__ == "__main__":
    main()
