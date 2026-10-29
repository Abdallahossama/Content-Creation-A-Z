import json,sys
from faster_whisper import WhisperModel
src,out=sys.argv[1],sys.argv[2]
m=WhisperModel("medium.en",device="cpu",compute_type="int8")
import soundfile as sf
audio,_=sf.read(src,dtype="float32")
segs,info=m.transcribe(audio,word_timestamps=True,beam_size=5,vad_filter=False,condition_on_previous_text=True)
res=[]
for s in segs:
    res.append({"start":s.start,"end":s.end,"text":s.text,"words":[{"w":w.word,"s":w.start,"e":w.end,"p":w.probability} for w in s.words]})
    print(f"{s.start:7.2f}-{s.end:7.2f} {s.text}",flush=True)
json.dump(res,open(out,"w",encoding="utf-8"),indent=1,ensure_ascii=False)
print("DONE")
