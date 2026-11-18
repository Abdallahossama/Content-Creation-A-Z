import json,wave,numpy as np
C=json.load(open('cands.json',encoding='utf8'));W=[w for s in json.load(open('words_medium.json',encoding='utf8')) for w in s['words']]
wf=wave.open('audio16k.wav');sr=wf.getframerate();a=np.frombuffer(wf.readframes(wf.getnframes()),dtype=np.int16).astype(np.float32)/32768
if wf.getnchannels()>1:a=a[::wf.getnchannels()]
for k,arr in C.items():
  print('==',k)
  for i,(s,e) in enumerate(arr):
    x=a[int(s*sr):int(e*sr)];fr=x[:len(x)//400*400].reshape(-1,400);rms=np.sqrt((fr**2).mean(1));db=20*np.log10(rms+1e-9)
    sp=db[db>db.max()-25];ws=[w for w in W if w['s']>=s-0.05 and w['e']<=e+0.05]
    print(f"T{i} {s}-{e} loud={sp.mean():.1f} var={sp.std():.1f} wps={len(ws)/(e-s):.2f} |"," ".join(w['w'] for w in ws))
