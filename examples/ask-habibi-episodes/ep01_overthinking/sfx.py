import numpy as np, soundfile as sf, os
from scipy.signal import butter, sosfilt
SR=48000; OUT="D:/why habibi/1st video/claude_sfx/"
rng=np.random.default_rng(7)
def t(d): return np.arange(int(SR*d))/SR
def env(n,a,r,shape=4.0):
    e=np.ones(n); A=int(a*SR); R=int(r*SR)
    if A>0: e[:A]=np.linspace(0,1,A)**1.5
    if R>0: e[-R:]*=np.exp(-shape*np.linspace(0,1,R))*np.linspace(1,0,R)**0.3
    return e
def bp(x,lo,hi,o=2): return sosfilt(butter(o,[lo,hi],'bandpass',fs=SR,output='sos'),x)
def lp(x,f,o=4): return sosfilt(butter(o,f,'lowpass',fs=SR,output='sos'),x)
def hp(x,f,o=2): return sosfilt(butter(o,f,'highpass',fs=SR,output='sos'),x)
def sweep_bp(noise,f0,f1,bw=0.6,blocks=64):
    n=len(noise); out=np.zeros(n); edges=np.linspace(0,n,blocks+1).astype(int)
    # overlap-add with crossfade blocks
    for i in range(blocks):
        a,b=edges[i],edges[i+1]; fc=f0*(f1/f0)**(i/blocks)
        lo=max(30,fc*(1-bw/2)); hi=min(SR/2-100,fc*(1+bw/2))
        pad=2048; s=max(0,a-pad)
        seg=bp(noise[s:b],lo,hi); out[a:b]+=seg[a-s:]
    return out
def norm(x,peak=0.89):
    m=np.max(np.abs(x)); return x/m*peak if m>0 else x
def stereo(x,pan=None):
    if pan is None: return np.stack([x,x],1)
    l=x*np.sqrt(np.clip(1-pan,0,1)); r=x*np.sqrt(np.clip(pan,0,1)); return np.stack([l,r],1)
def save(name,x,peak=0.89):
    if x.ndim==1: x=stereo(x)
    x=x/np.max(np.abs(x))*peak
    sf.write(OUT+name+".wav",x.astype(np.float32),SR,subtype='PCM_16'); print(name,len(x)/SR)

# whoosh short / long (rise then fall, stereo pan L->R)
for name,d,f0,f1 in [("whoosh_fast",0.45,400,3500),("whoosh_long",0.9,250,2800)]:
    n=int(SR*d); nz=rng.standard_normal(n)
    x=sweep_bp(nz,f0,f1,0.9)
    tt=np.linspace(0,1,n); e=np.sin(np.pi*tt**0.8)**2.2
    x*=e; pan=0.15+0.7*tt
    save(name,stereo(x,pan))
# reverse whoosh into hit (swoosh in)
n=int(SR*0.6); nz=rng.standard_normal(n); x=sweep_bp(nz,300,5000,0.8); tt=np.linspace(0,1,n); x*=tt**2.5*(1-np.clip((tt-0.93)/0.07,0,1)); save("swoosh_in",x)
# pop
tt=t(0.14); f=900*np.exp(-tt*28)+180; ph=2*np.pi*np.cumsum(f)/SR
x=np.sin(ph)*np.exp(-tt*38); x[:int(0.002*SR)]+=rng.standard_normal(int(0.002*SR))*0.6; save("pop",lp(x,6000))
# bubble pop higher
tt=t(0.1); f=1500*np.exp(-tt*40)+400; x=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*50); save("pop_high",x)
# ding (bell)
tt=t(1.6); x=np.zeros_like(tt)
for r,a,dcy in [(1,1,2.2),(2.0,0.35,3.5),(2.76,0.4,4),(5.4,0.15,7),(8.93,0.06,10)]:
    x+=a*np.sin(2*np.pi*1318*r*tt)*np.exp(-tt*dcy)
x*=env(len(tt),0.002,0.05); save("ding",x,0.8)
# sparkle / good news arpeggio
notes=[1046.5,1318.5,1568,2093]; x=np.zeros(int(SR*1.3))
for i,f in enumerate(notes):
    s=int(i*0.07*SR); tt=t(1.3)[:len(x)-s]
    x[s:]+=np.sin(2*np.pi*f*tt)*np.exp(-tt*4)*0.6+np.sin(2*np.pi*f*2.01*tt)*np.exp(-tt*7)*0.2
x+=hp(rng.standard_normal(len(x)),7000)*np.exp(-t(1.3)*5)*0.08; save("sparkle",x,0.75)
# impact / boom
tt=t(1.4); f=85*np.exp(-tt*3)+38; sub=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*3.2)
nz=lp(rng.standard_normal(len(tt)),1800)*np.exp(-tt*14)*0.9
x=np.tanh(1.8*(sub+nz)); save("impact_boom",x)
# riser (2s)
n=int(SR*2.0); tt=np.linspace(0,1,n); nz=rng.standard_normal(n); x=sweep_bp(nz,200,6000,0.5)*tt**2
f=220*(4**tt); x+=0.35*np.sin(2*np.pi*np.cumsum(f)/SR)*tt**1.5
x*=1-np.clip((tt-0.97)/0.03,0,1); save("riser",x)
# clock tick-tock (2s, 4 ticks)
x=np.zeros(int(SR*2.0))
for i in range(4):
    s=int(i*0.5*SR); f=3200 if i%2==0 else 2400; tt=t(0.04)
    c=np.sin(2*np.pi*f*tt)*np.exp(-tt*180)+bp(rng.standard_normal(len(tt)),2000,6000)*np.exp(-tt*250)*0.5
    x[s:s+len(c)]+=c
save("clock_ticks",x,0.8)
# heartbeat (2 beats)
x=np.zeros(int(SR*1.7))
for s0 in [0.0,0.28,0.85,1.13]:
    tt=t(0.22); f=60*np.exp(-tt*6)+35; b=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*18)*(1 if s0 in (0.0,0.85) else 0.7)
    s=int(s0*SR); x[s:s+len(b)]+=b
save("heartbeat",np.tanh(2*x))
# glitch / error buzz
tt=t(0.5); sq=np.sign(np.sin(2*np.pi*110*tt))*0.5+np.sign(np.sin(2*np.pi*233*tt))*0.3
gate=(np.floor(tt*32)%3!=1).astype(float); x=lp(sq*gate,5000)*env(len(tt),0.003,0.08)
x+=bp(rng.standard_normal(len(tt)),1500,7000)*0.25*(np.floor(tt*45)%4==0); save("glitch_error",x,0.7)
# boing (cartoon)
tt=t(0.7); f=260+140*np.sin(2*np.pi*11*tt)*np.exp(-tt*4)+tt*120; x=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*4.5); save("boing",x,0.8)
# soft ui click
tt=t(0.035); x=np.sin(2*np.pi*1800*tt)*np.exp(-tt*300)+bp(rng.standard_normal(len(tt)),3000,9000)*np.exp(-tt*400)*0.4; save("click",x,0.7)
# typing (8 keys)
x=np.zeros(int(SR*0.9))
for i in range(8):
    s=int((i*0.1+rng.uniform(-0.02,0.02)+0.02)*SR); tt=t(0.03)
    c=bp(rng.standard_normal(len(tt)),1500,8000)*np.exp(-tt*350)*rng.uniform(0.6,1)+np.sin(2*np.pi*rng.uniform(500,800)*tt)*np.exp(-tt*200)*0.4
    x[s:s+len(c)]+=c
save("typing",x,0.6)
# camera shutter-ish (for "memory flash")
x=np.zeros(int(SR*0.25)); tt=t(0.04)
for s0 in [0,0.09]:
    c=bp(rng.standard_normal(len(tt)),1000,9000)*np.exp(-tt*150); s=int(s0*SR); x[s:s+len(c)]+=c
save("shutter",x,0.7)
# dramatic sting (low brass-ish chord swell)
tt=t(1.6); x=np.zeros_like(tt)
for f in [110,130.8,164.8,220]:
    saw=2*((f*tt)%1)-1; x+=saw
x=lp(x,1200)*np.minimum(tt/0.05,1)*np.exp(-tt*1.6); save("dramatic_sting",np.tanh(1.5*x),0.75)
# record scratch-ish
tt=t(0.45); spd=np.concatenate([np.linspace(1,-1.5,len(tt)//2),np.linspace(-1.5,0.2,len(tt)-len(tt)//2)])
base=bp(rng.standard_normal(len(tt)),300,4000); idx=np.clip(np.cumsum(np.abs(spd))*1.0,0,len(tt)-1).astype(int)
x=base[idx]*env(len(tt),0.005,0.1)*(0.4+np.abs(spd)); save("record_scratch",lp(x,5000),0.75)
