import wave,numpy as np,sys
wf=wave.open('audio16k.wav');a=np.frombuffer(wf.readframes(wf.getnframes()),dtype=np.int16).astype(np.float32)/32768
for rg in sys.argv[1:]:
  s,e=map(float,rg.split(':'));x=a[int(s*16000):int(e*16000)];fr=x[:len(x)//320*320].reshape(-1,320)
  db=20*np.log10(np.sqrt((fr**2).mean(1))+1e-9);thr=db.max()-30
  sp=db>thr;segs=[];i=0
  while i<len(sp):
    if sp[i]:
      j=i
      while j<len(sp) and sp[j]:j+=1
      segs.append((s+i*0.02,s+j*0.02));i=j
    else:i+=1
  m=[]
  for a0,b0 in segs:
    if m and a0-m[-1][1]<0.1:m[-1]=(m[-1][0],b0)
    else:m.append((a0,b0))
  print(rg,'floor',round(np.percentile(db,10),1),'max',round(db.max(),1),' '.join(f'{p:.2f}-{q:.2f}' for p,q in m if q-p>0.06))
