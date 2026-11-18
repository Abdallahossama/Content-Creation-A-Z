import json,wave,numpy as np
E=json.load(open('edl2.json',encoding='utf8'))
wf=wave.open('audio16k.wav');a=np.frombuffer(wf.readframes(wf.getnframes()),dtype=np.int16).astype(np.float32)/32768
F=1/30
for c in E:
  s,e=c['r'];x=a[int(s*16000):int(e*16000)];fr=x[:len(x)//160*160].reshape(-1,160)  # 10ms
  db=20*np.log10(np.sqrt((fr**2).mean(1))+1e-9);sp=db>db.max()-32
  # islands
  isl=[];i=0
  while i<len(sp):
    if sp[i]:
      j=i
      while j<len(sp) and sp[j]:j+=1
      isl.append([s+i*0.01,s+j*0.01]);i=j
    else:i+=1
  m=[]
  for p,q in isl:
    if m and p-m[-1][1]<0.16:m[-1][1]=q
    else:m.append([p,q])
  m=[x for x in m if x[1]-x[0]>0.07]
  # pad, clamp to range
  out=[]
  for k,(p,q) in enumerate(m):
    p=max(s,p-0.05);q=min(e,q+0.07)
    out.append([p,q])
  out[0][0]=s;out[-1][1]=e
  # frame-quantize
  segs=[]
  for p,q in out:
    n=max(3,round((q-p)/F));segs.append([round(p,3),n])
  c['segs']=segs
  print(c['id'],[(p,round(n*F,2)) for p,n in segs])
json.dump(E,open('edl2_segs.json','w',encoding='utf8'),ensure_ascii=False,indent=0)
