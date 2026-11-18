import json,wave,numpy as np
from faster_whisper import WhisperModel
C=json.load(open('cands.json',encoding='utf8'))
m=WhisperModel('medium',device='cpu',compute_type='int8',cpu_threads=8)
wf=wave.open('audio16k.wav');a=np.frombuffer(wf.readframes(wf.getnframes()),dtype=np.int16).astype(np.float32)/32768
P="أغلب الرسايل اللي بتجيلي بتبدأ كده: عايز سيستم، بس مش عارف أبدأ منين. أغلب الشركات بتبدأ من هنا: الطلبات على إكسل والمتابعة على واتساب. وكل يوم فيه طلب بيضيع أو غلطة محدش واخد باله منها. أول حاجة ما بنكتبش كود، بنفهم الشغل كله من A to Z. بعد كده بنكتب PRD فيها كل المتطلبات في مستند واحد، والعميل يوافق عليه قبل أي تنفيذ. التنفيذ على مراحل. التسليم. تدريب الفريق على النظام ودعم مستمر. والفرق؟ لو إنت كمان مش عارف تبدأ منين، احجز استشارة مجانية 20 دقيقة."
out={}
for k,arr in C.items():
  for i,(s,e) in enumerate(arr):
    s0=max(0,s-0.4);x=a[int(s0*16000):int((e+0.6)*16000)]
    segs,_=m.transcribe(x,language='ar',word_timestamps=True,beam_size=5,initial_prompt=P,condition_on_previous_text=False,vad_filter=False)
    ws=[{"w":w.word.strip(),"s":round(s0+w.start,2),"e":round(s0+w.end,2),"p":round(w.probability,2)} for sg in segs for w in sg.words]
    out[f"{k}|T{i}"]=ws
    print(k,f"T{i}",s,e,'|',' '.join(w['w'] for w in ws),flush=True)
json.dump(out,open('cand_words.json','w',encoding='utf8'),ensure_ascii=False,indent=0)
