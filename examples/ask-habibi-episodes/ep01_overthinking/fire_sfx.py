import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
SR=48000; rng=np.random.default_rng(11)
def lp(x,f,o=4): return sosfilt(butter(o,f,'lowpass',fs=SR,output='sos'),x)
def hp(x,f,o=2): return sosfilt(butter(o,f,'highpass',fs=SR,output='sos'),x)
def bp(x,a,b,o=2): return sosfilt(butter(o,[a,b],'bandpass',fs=SR,output='sos'),x)
dur=3.2; n=int(SR*dur); t=np.arange(n)/SR
def chan(seed):
    r=np.random.default_rng(seed)
    # low roar: brown-ish noise with slow flicker
    roar=lp(np.cumsum(r.standard_normal(n))*0.02,320); roar-=lp(roar,25)
    flick=1+0.35*lp(r.standard_normal(n),3)*8
    roar*=np.clip(flick,0.4,1.8)
    # airy hiss of flames
    hiss=bp(r.standard_normal(n),900,4200)*0.12*np.clip(1+0.5*lp(r.standard_normal(n),6)*6,0.3,1.8)
    # crackles: poisson impulses
    cr=np.zeros(n)
    for rate,amp,lo,hi,length in [(32,0.55,2500,9000,0.004),(9,0.9,900,4000,0.012),(2.5,1.0,300,2500,0.03)]:
        k=r.poisson(rate*dur)
        for p in r.uniform(0,dur-0.05,k):
            L=int(length*SR*r.uniform(0.5,1.5)); s=int(p*SR)
            burst=bp(r.standard_normal(L+64),lo,hi)[64:]*np.exp(-np.linspace(0,6,L))*amp*r.exponential(0.6)
            cr[s:s+L]+=burst
    return roar*0.9+hiss+cr*0.8
x=np.stack([chan(1),chan(2)],1)
env=np.minimum(1,t/0.18)[:,None]*np.minimum(1,(dur-t)/0.6)[:,None]
x*=env; x/=np.max(np.abs(x)); x*=0.89
sf.write("D:/why habibi/1st video/claude_sfx/fire_crackle.wav",x.astype(np.float32),SR,subtype='PCM_16')
print("fire_crackle.wav",dur,"s")
