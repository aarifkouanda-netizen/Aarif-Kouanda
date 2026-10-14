import os, numpy as np, wave
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/"
SR=48000; DUR=53.0; BPM=120; B=60/BPM
n=int(SR*DUR); L=np.zeros(n); R=np.zeros(n)
rng=np.random.default_rng(7)
cuts=[float(l) for l in open(ROOT+"rendus/v2_cuts.txt") if not l.startswith("END")]
def add(sig,t,g=1.0,pan=0.0):
    i=int(t*SR); j=min(n,i+len(sig))
    if i>=n: return
    L[i:j]+=sig[:j-i]*g*(1-max(0,pan)); R[i:j]+=sig[:j-i]*g*(1+min(0,pan))
def env(d,a=0.002,dec=0.2):
    t=np.arange(int(d*SR))/SR; return np.minimum(t/a,1)*np.exp(-t/dec)
def kick(g=1.0):
    d=0.35; t=np.arange(int(d*SR))/SR; f=45+90*np.exp(-t*30)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*9)*g
def hat(d=0.05):
    s=rng.standard_normal(int(d*SR)); s=np.diff(s,prepend=0); return s*env(d,0.001,0.012)*0.25
def clap():
    s=rng.standard_normal(int(0.2*SR)); s=np.diff(s,prepend=0)
    e=sum(env(0.2,0.001,0.02)*(np.arange(int(0.2*SR))>=int(k*0.011*SR)) for k in range(3))
    return s*e*0.25
def clac():  # contacteur : clic sec + petit choc grave
    c=np.diff(rng.standard_normal(int(0.03*SR)),prepend=0)*env(0.03,0.0005,0.004)*0.9
    t=np.arange(int(0.12*SR))/SR; th=np.sin(2*np.pi*110*t)*np.exp(-t*40)*0.5
    out=np.zeros(len(th)); out[:len(c)]+=c; return out+th
def boom(d=2.5):
    t=np.arange(int(d*SR))/SR; return np.sin(2*np.pi*(38+20*np.exp(-t*3))*t)*np.exp(-t*1.6)*0.9
def mallet(f,d=0.6):  # timbre proche du balafon : partiels inharmoniques, attaque sèche
    t=np.arange(int(d*SR))/SR
    s=np.sin(2*np.pi*f*t)*np.exp(-t*7)+0.45*np.sin(2*np.pi*f*3.9*t)*np.exp(-t*22)+0.25*np.sin(2*np.pi*f*9.2*t)*np.exp(-t*45)
    return s*0.35
def pad(t0,t1,freqs,g=0.12,att=1.5,rel=1.5):
    t=np.arange(int((t1-t0)*SR))/SR; s=sum(np.sin(2*np.pi*f*t+k)+0.3*np.sin(2*np.pi*f*2.003*t) for k,f in enumerate(freqs))/len(freqs)
    e=np.minimum(t/att,1)*np.minimum((t1-t0-t)/rel,1); add(s*e*g,t0)
def riser(t0,t1,g=0.35):
    d=t1-t0; t=np.arange(int(d*SR))/SR; s=rng.standard_normal(len(t))
    # bruit filtré qui s'ouvre : moyenne glissante de plus en plus courte
    out=np.zeros(len(t)); k0=40
    for a in range(0,len(t),2400):
        k=max(1,int(k0*(1-a/len(t)))+1); seg=s[a:a+2400]; out[a:a+2400]=np.convolve(seg,np.ones(k)/k,"same")
    add(out*(t/d)**2*g,t0)
def bass(t0,t1,notes,g=0.3):
    for i,tb in enumerate(np.arange(t0,t1,B)):
        f=notes[i%len(notes)]; d=B*0.9; t=np.arange(int(d*SR))/SR
        add(np.tanh(2*np.sin(2*np.pi*f*t))*np.exp(-t*4)*g,tb)
A,C,D,E,G=110,130.81,146.83,164.81,196.0
# Acte 1 : pulsation qui monte, coupure nette à 12 s
for k,tb in enumerate(np.arange(0,12,B)):
    add(kick(0.55+0.35*tb/12),tb)
    if tb>=4: add(hat(),tb+B/2,0.8)
    if tb>=8: add(hat(),tb+B/4,0.5); add(hat(),tb+3*B/4,0.5)
bass(0,12,[A/2,A/2,C/2,G/4]); pad(0,12,[A,E,A*2],0.06,2,0.05); riser(9.5,12.0)
# Acte 2 : silence, clac, choc, nappe ; respiration en demi-temps
add(clac(),12.5,1.0); add(boom(),13.0,0.9); pad(13.0,19.0,[A,C*2,E*2,A*2],0.10,0.8,1.0)
for tb in np.arange(13.0,19.0,2*B): add(kick(0.45),tb)
mel=[A*2,C*4,D*4,E*4,G*2,E*4,D*4,C*4]
for i,tb in enumerate(np.arange(15.0,19.0,B)): add(mallet(mel[i%8]),tb,0.6,-0.3)
# Acte 3 : temps plein, motif de balafon en croches
for tb in np.arange(19.0,29.0,B): add(kick(0.75),tb)
for i,tb in enumerate(np.arange(19.0,29.0,B/2)): add(mallet(mel[(i*3)%8]*(1 if i%4 else 0.5)),tb,0.5,0.3*((i%2)*2-1))
bass(19,29,[A/2,A/2,D/2,E/2]); pad(19,29,[A,E,A*2],0.07,1,1)
# Acte 4 : groove complet
for tb in np.arange(29.0,43.0,B):
    add(kick(0.9),tb); add(hat(),tb+B/2,0.9)
    for q in (0.25,0.75): add(hat(0.03),tb+q*B,0.4)
for tb in np.arange(29.5,43.0,2*B): add(clap(),tb,0.9)
bass(29,43,[A/2,A/2,C/2,D/2,E/2,E/2,G/4,G/4]); pad(29,43,[A,C*2,E*2],0.06,1,1)
for i,tb in enumerate(np.arange(29.0,43.0,B)):
    if i%2==0: add(mallet(mel[i%8]*2),tb+B/2,0.35,0.4)
riser(41.0,43.0,0.3)
# Acte 5 : impact, groove allégé, puis la nappe seule
add(boom(),43.0,0.8)
for tb in np.arange(43.0,49.0,B): add(kick(0.6),tb)
bass(43,49,[A/2,A/2,E/2,A/2],0.22); pad(43,52.5,[A,E,A*2,C*4],0.10,1,2.5)
for i,tb in enumerate(np.arange(49.0,51.0,B)): add(mallet([E*4,D*4,C*4,A*2][i%4]),tb,0.5)
add(clac(),51.5,1.0)
# un clac discret à chaque coupe sur la nuit
for c in cuts:
    if 12.9<c<43.1: add(clac(),c,0.35,0.2)
mix=np.stack([L,R],1)
# compresseur doux + limiteur
mix=np.tanh(mix*1.2)/np.tanh(1.2); mix*=0.89/np.abs(mix).max()
fade=int(0.02*SR); mix[:fade]*=np.linspace(0,1,fade)[:,None]
with wave.open(ROOT+"rendus/v2_son.wav","wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype("<i2").tobytes())
print("ok")
