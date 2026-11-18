import json,wave,numpy as np
from faster_whisper import WhisperModel
E=json.load(open('edl2_segs.json',encoding='utf8'))
m=WhisperModel('medium',device='cpu',compute_type='int8',cpu_threads=8)
wf=wave.open('audio16k.wav');a=np.frombuffer(wf.readframes(wf.getnframes()),dtype=np.int16).astype(np.float32)/32768
for c in E:
  for i,(p,n) in enumerate(c['segs']):
    x=a[int(p*16000):int((p+n/30)*16000)]
    x=np.concatenate([np.zeros(8000,np.float32),x,np.zeros(8000,np.float32)])
    segs,_=m.transcribe(x,language='ar',word_timestamps=True,beam_size=5,vad_filter=False,condition_on_previous_text=False)
    print(c['id'],i,p,round(n/30,2),'|',' '.join(f"{w.word.strip()}@{p+w.start-0.5:.2f}" for s in segs for w in s.words),flush=True)
