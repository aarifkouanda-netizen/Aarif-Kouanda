import os, subprocess, numpy as np, math, wave
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H,FPS=1920,1080,24; BEAT=0.5           # 120 BPM : 1 temps = 12 images
GOLD=(249,168,0); WHITE=(240,240,236); BG=(27,32,35)
F=os.environ.get("INTER_DIR","C:/Windows/Fonts/")  # dossier contenant Inter-Bold.otf, Inter-SemiBold.otf…; OSW=None
import glob
from functools import lru_cache
@lru_cache(maxsize=None)
def font(w,s):
    # Inter statique (Inter-Bold.otf…) si INTER_DIR la fournit, sinon la police variable du projet
    p=F+f"Inter-{w}.otf"
    if os.path.exists(p): return ImageFont.truetype(p,s)
    f=ImageFont.truetype(ROOT+"fonts/InterVariable.ttf",s); f.set_variation_by_name(w); return f
def ease(t): return 0 if t<=0 else 1 if t>=1 else 1-(1-t)**3
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/"
N=ROOT+"nuit/"; U=ROOT+"sources/"; P=ROOT+"plaques/"
C1=U+"Ensemble_1_-_2_minutes_-_version_nettoyee.mp4"; C2=U+"Circuit_complet_-_1_min_30_-_variations_de_vitesse.mp4"
NIGHT="deband=1thr=0.03:2thr=0.03:3thr=0.03:range=24:blur=1,noise=alls=4:allf=t"
CUTS=[]   # instants de coupe, pour le son

def frames(src,ss=0,dur=None,vf=""):
    cmd=["ffmpeg","-v","error"]+(["-ss",str(ss)] if ss else [])+["-i",src]
    f=(vf+"," if vf else "")+f"scale={W}:{H}:flags=lanczos,fps={FPS},format=rgb24"
    cmd+=["-vf",f]+(["-t",str(dur)] if dur else [])+["-f","rawvideo","-"]
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE); n=0; last=None
    while True:
        b=p.stdout.read(W*H*3)
        if len(b)<W*H*3: break
        last=Image.frombytes("RGB",(W,H),b); n+=1; yield last
    # complète si la source est un peu courte
    if dur and last is not None:
        for _ in range(int(round(dur*FPS))-n): yield last

y,x=np.ogrid[:H,:W]; VIG=np.clip(1-0.22*np.clip(np.sqrt(((x-W/2)/(W/2))**2+((y-H/2)/(H/2))**2)-0.6,0,1)**1.5,0,1)[...,None]
def grade(im,sat=1.0):
    a=np.asarray(im).astype(np.float32)/255
    if sat!=1.0:
        g=a.mean(axis=2,keepdims=True); a=g+(a-g)*sat
    a=0.03+a*VIG*0.97
    return Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8)).convert("RGBA")

def txt(img,xy,s,f,col,a=1.0,anchor="la"):
    o=Image.new("RGBA",img.size,(0,0,0,0)); ImageDraw.Draw(o).text(xy,s,font=f,fill=col+(int(255*max(0,min(1,a))),),anchor=anchor)
    img.alpha_composite(o)
def word(img,t,t0,t1,s,size=150,col=WHITE,y=540):
    # mot posé sur le temps : arrive en 4 images, part net à t1 (pas de fondu)
    if not (t0<=t<t1): return
    k=ease((t-t0)/(4/FPS)); f=font("Bold",size)
    sh=Image.new("RGBA",img.size,(0,0,0,0)); ImageDraw.Draw(sh).text((W/2,y+3),s,font=f,fill=(0,0,0,int(150*k)),anchor="mm")
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
    txt(img,(W/2,y+(1-k)*24),s,f,col,k,"mm")

out=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
  "-c:v","libx264","-crf","16","-preset","slow","-pix_fmt","yuv420p",ROOT+"rendus/v2_video.mp4"],stdin=subprocess.PIPE)
T=[0]  # compteur d'images
def now(): return T[0]/FPS
SAVE=set(range(6,1300,24))
os.makedirs(ROOT+"rendus/apercus",exist_ok=True)
def emit(im):
    im=im.convert("RGB"); out.stdin.write(im.tobytes()); T[0]+=1
    if T[0] in SAVE: im.save(ROOT+f"rendus/apercus/v2_ap_{T[0]:04d}.jpg",quality=85)
def cut(): CUTS.append(now())

COUNTER=[None]  # (valeur_affichée, cible, t_debut)
def counter(img,t):
    c=COUNTER[0]
    if c is None: return
    v0,v1,ts=c; k=ease((t-ts)/0.3); v=v0+(v1-v0)*k
    s=f"{v:.1f}".replace(".",",")
    f1=font("Bold",64); f2=font("Medium",24)
    sh=Image.new("RGBA",img.size,(0,0,0,0)); d=ImageDraw.Draw(sh); d.rectangle([W/2-260,950,W/2+260,1050],fill=(0,0,0,110))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(30)))
    txt(img,(W/2-14,1000),s,f1,GOLD,1,"rm"); txt(img,(W/2+4,1006),"KM ÉCLAIRÉS",f2,WHITE,1,"lm")
def set_counter(v):
    c=COUNTER[0]; cur=c[1] if c else 0.0; COUNTER[0]=(cur,v,now())

# ---------- ACTE 1 · le jour en rafale (0–12 s), 8 plans de 1,5 s accélérés ×2
day=[(C1,1,371),(C1,14,371),(C1,38.5,371),(C1,56,371),(C1,84,371),(C1,90.5,371),(C2,5.2,180),(C2,72,180)]
WORDS=[(0.0,3.5,"OUAGADOUGOU"),(4.0,7.5,"DEUX CIRCUITS"),(8.0,11.5,"11,4 KM D'AVENUES")]
for src,ss,cx in day:
    cut()
    for fr in frames(src,ss,1.5,f"crop=1038:584:{cx}:0,setpts=0.5*PTS"):
        t=now(); im=grade(fr,0.5)
        for a,b,s in WORDS: word(im,t,a,b,s,140 if len(s)<14 else 120)
        emit(im)

# ---------- ACTE 2 · la bascule (12–19 s)
# repère de la tête LED la plus brillante dans le premier plan de nuit
first=next(frames(N+"C2-S1_nuit_seedance_v1.mov",2.0,0.05))
L=np.asarray(first.convert("L").filter(ImageFilter.GaussianBlur(6))).astype(float); L[int(H*0.55):]=0
hy,hx=np.unravel_index(L.argmax(),L.shape); DOT=(int(hx),int(hy))
for i in range(int(0.5*FPS)): emit(Image.new("RGB",(W,H),(6,7,8)))          # silence, noir
cut()
for i in range(int(0.5*FPS)):                                                # clac : le point s'allume
    t=i/FPS; k=ease(t/0.25); im=Image.new("RGBA",(W,H),(6,7,8,255)); d=ImageDraw.Draw(im); r=4+10*k
    d.ellipse([DOT[0]-r,DOT[1]-r,DOT[0]+r,DOT[1]+r],fill=GOLD+(255,)); emit(im)
cut()
for fr in frames(N+"C2-S1_nuit_seedance_v1.mov",2.0,2.0,NIGHT): emit(grade(fr))   # le point devient la tête LED
# volet unique, ralenti 50 %, sur l'avenue aux drapeaux
cut()
dayg=frames(P+"C1-S1_plaque_16x9_720p_5s.mp4",0,4.0,"setpts=2.0*PTS,minterpolate=fps=24:mi_mode=mci")
nig=frames(N+"C1-S1_nuit_seedance_v1.mov",0,4.0,NIGHT+",setpts=2.0*PTS,minterpolate=fps=24:mi_mode=mci")
t0=now()
for fd,fn in zip(dayg,nig):
    t=now()-t0; x=int(W*(1-ease((t-0.5)/2.5))) if t<3.0 else 0
    a=grade(fd); im=grade(fn); im.paste(a.crop((0,0,x,H)),(0,0))     # le jour recule vers la gauche : la nuit gagne
    d=ImageDraw.Draw(im)
    if 0<x<W:
        d.line([(x,0),(x,H)],fill=GOLD+(255,),width=4)
        txt(im,(x-24,880),"AVANT",font("SemiBold",30),WHITE,1,"rm"); txt(im,(x+24,880),"APRÈS",font("SemiBold",30),GOLD,1,"lm")
    emit(im)

# ---------- ACTE 3 · le produit (19–29 s), 5 détails de 2 s tirés des plans de nuit Seedance
def still(clip,t):
    return grade(list(frames(N+f"{clip}_nuit_seedance_v1.mov",t,0.05,NIGHT))[0])
def rect(cx,cy,w):
    h=w*9/16; x0=min(max(cx-w/2,0),W-w); y0=min(max(cy-h/2,0),H-h); return (x0,y0,w)
shots=[("C1-S1",3.25,rect(610,260,900),rect(610,230,760),"COURONNE EN DENTELLE LED"),
       ("C1-S1",3.25,rect(900,170,560),rect(905,150,460),"DOUBLE CROSSE · 4,5 M"),
       ("C1-S3",0.75,rect(880,760,760),rect(880,214,760),"MÂT DE 10 À 12 M"),
       ("C1-S3",2.0,rect(520,800,900),rect(520,820,760),"SOCLE ÉCLAIRÉ · 1,3 M"),
       ("C1-S1",2.5,rect(700,600,1100),rect(960,540,1920),"ACIER GALVANISÉ")]
for clip,ts,a,b,label in shots:
    cut(); src=still(clip,ts)
    for i in range(int(2.0*FPS)):
        t=i/FPS; k=t/2.0; k=k*k*(3-2*k)
        x0,y0,w=[a[j]+(b[j]-a[j])*k for j in range(3)]; h=w*9/16
        im=src.crop((int(x0),int(y0),int(x0+w),int(y0+h))).resize((W,H),Image.BICUBIC)
        word(im,t,0.5,2.0,label,84,GOLD,930); emit(im)

# ---------- ACTE 4 · la ville, mât à mât (29–43 s)
pieces=[("C1-S3",0.0,2.0,None,1.4,"CIRCUIT 1"),("C1-S2",1.0,2.0,None,2.9,None),
        ("C1-S1",1.9,1.15,(3.05,0.54),4.4,None),("C1-S3",2.5,2.0,None,5.8,None),("C1-S2",3.25,1.5,None,7.2,None)]
def play_piece(clip,ss,dur,slow,val,label):
    cut(); set_counter(val); t0=now()
    gens=[frames(N+f"{clip}_nuit_seedance_v1.mov",ss,dur,NIGHT)]
    if slow: gens.append(frames(N+f"{clip}_nuit_seedance_v1.mov",slow[0],slow[1]/0.4,NIGHT+",setpts=2.5*PTS,minterpolate=fps=24:mi_mode=mci"))
    for g in gens:
        for fr in g:
            t=now(); im=grade(fr)
            if label: word(im,t,t0,t0+1.5,label,110,WHITE,470)
            counter(im,t); emit(im)
for p in pieces: play_piece(*p)
# mini-carte : la carte de synthèse plonge sur le circuit 2 (1 s)
cut(); mapf=list(frames(ROOT+"cartes/plan7_synthese_v3.mp4",9.0,0.05))[0].convert("RGBA")
for i in range(FPS):
    k=ease(i/FPS); x0=60+1020*k; y0=190-15*k; w=1560-720*k; h=w*9/16
    im=mapf.crop((int(x0),int(y0),int(x0+w),int(y0+h))).resize((W,H),Image.BICUBIC); counter(im,now()); emit(im)
play_piece("C2-S1",2.0,2.0,None,9.3,"CIRCUIT 2")
play_piece("C2-S1",0.0,1.0,None,11.4,None)
COUNTER[0]=None

# ---------- ACTE 5 · synthèse (43–49 s) puis fin (49–53 s)
cut()
for fr in frames(ROOT+"cartes/plan7_synthese_v3.mp4",0,6.0,"setpts=0.6*PTS"): emit(fr.convert("RGBA"))
cut(); still=list(frames(N+"C1-S1_nuit_seedance_v1.mov",3.5,0.05,NIGHT))[0]; still=grade(still)
L=np.asarray(still.convert("L").filter(ImageFilter.GaussianBlur(6))).astype(float); L[int(H*0.4):]=0
hy,hx=np.unravel_index(L.argmax(),L.shape); END=(int(hx),int(hy))
for i in range(int(2.5*FPS)):
    t=i/FPS; s=1+0.05*t/2.5; w=W/s; h=H/s; x0=END[0]-(END[0])/s; y0=END[1]-(END[1])/s
    im=still.crop((int(x0),int(y0),int(x0+w),int(y0+h))).resize((W,H),Image.BICUBIC)
    sh=Image.new("RGBA",im.size,(0,0,0,0)); ImageDraw.Draw(sh).rectangle([60,760,1500,1010],fill=(0,0,0,120)); im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(50)))
    k=ease((t-0.2)/0.3); txt(im,(110,830+(1-k)*16),"DEUX CIRCUITS, UNE NUIT RENDUE À LA VILLE",font("Bold",54),WHITE,k)
    k2=ease((t-0.6)/0.3); txt(im,(110,910),"Ouagadougou · octobre 2026 · [maître d'ouvrage]",font("Regular",30),GOLD,k2)
    emit(im)
cut()
for i in range(int(1.5*FPS)):                                                    # tout s'éteint sauf une lampe
    t=i/FPS; im=Image.new("RGBA",(W,H),(6,7,8,255)); r=14*(1-ease((t-0.8)/0.6))
    if r>0.5: ImageDraw.Draw(im).ellipse([END[0]-r,END[1]-r,END[0]+r,END[1]+r],fill=GOLD+(255,))
    emit(im)
out.stdin.close(); out.wait()
open(ROOT+"rendus/v2_cuts.txt","w").write("\n".join(f"{c:.4f}" for c in CUTS)+f"\nEND {now():.4f}\n")
print("durée",now(),"s ; coupes",len(CUTS), "DOT",DOT,"END",END)
