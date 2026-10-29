import json,sys,os
p=sys.argv[1]
d=json.load(open(p,encoding='utf-8'))
print("duration s", d['duration']/1e6, "canvas", d.get('canvas_config'))
print("top keys", list(d.keys()))
mats=d['materials']
print("material kinds with counts:", {k:len(v) for k,v in mats.items() if isinstance(v,list) and v})
idx={}
for k,v in mats.items():
    if isinstance(v,list):
        for m in v:
            if isinstance(m,dict) and 'id' in m: idx[m['id']]=(k,m)
for ti,t in enumerate(d['tracks']):
    print(f"\n=== track {ti} type={t['type']} name={t.get('name')} attr={t.get('attribute')} flag={t.get('flag')} segs={len(t['segments'])}")
    for s in t['segments']:
        tr=s['target_timerange']; sr=s.get('source_timerange')
        k,m=idx.get(s['material_id'],('?',{}))
        desc=m.get('path') or m.get('name') or ''
        if k=='texts':
            try: desc=json.loads(m['content'])['text'][:60]
            except Exception: desc=str(m.get('content'))[:60]
        print(f"  {tr['start']/1e6:8.2f} +{tr['duration']/1e6:6.2f}  src={None if not sr else round(sr['start']/1e6,2)}  {k:14s} {m.get('type','')}  vol={s.get('volume')} spd={s.get('speed')} :: {desc}")
