# Rendu des plans de carte (5a, 6a, 7) - charte : 7016 fond, 9006 contexte, 1003 circuits
import math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H,SS,FPS=1920,1080,2,24
BG=(56,62,66); CTX=(165,165,165); GOLD=(249,168,0); WHITE=(240,240,236)
F="/usr/share/fonts/opentype/inter/"
def font(w,s): return ImageFont.truetype(F+("Inter-%s.otf"%w),s*SS)
OUT=sys.argv[1] if len(sys.argv)>1 else "out"

# --- géométrie (coordonnées relevées sur tes captures) ---
C1=dict(src=(1600,839),
  routes=[[(630,160),(410,205),(493,665)],                       # branche ouest puis sud (aéroport)
          [(650,158),(740,135),(840,118),(890,103),(1000,103),(1300,118),(1450,123)]], # branche est (CHU)
  ctx=[[(0,300),(160,285),(410,205),(660,0)],[(1130,839),(1530,0)],[(1440,0),(1600,250)]],
  runway=[(430,839),(740,370)],
  marks=[((630,160),"Départ",(20,-50)),((493,665),"Aéroport",(-140,-14)),((1450,123),"CHU",(-70,-52))],
  title="CIRCUIT 1")
C2=dict(src=(1397,1238),
  routes=[[(622,160),(622,545)],[(622,655),(622,1010)],[(30,594),(568,598)],[(680,598),(930,597)]],
  ctx=[[(80,1238),(80,100),(640,110)],[(640,110),(1397,1050)]],
  ring=((625,600),55),
  marks=[((625,600),"Monument des Héros nationaux",(40,-78)),((622,1010),"Palais de Kossyam",(24,-12)),((622,160),"Bd des Tensoba",(24,-40))],
  title="CIRCUIT 2")

def fit(c,box):
    sw,sh=c["src"]; x0,y0,bw,bh=box; s=min(bw/sw,bh/sh)
    ox=x0+(bw-sw*s)/2; oy=y0+(bh-sh*s)/2
    return lambda p:((ox+p[0]*s)*SS,(oy+p[1]*s)*SS), s
def ease(t): return 0 if t<=0 else 1 if t>=1 else t*t*(3-2*t)
def plen(pts): return sum(math.dist(pts[i],pts[i+1]) for i in range(len(pts)-1))
def partial(pts,f):
    L=plen(pts)*f; out=[pts[0]]
    for i in range(len(pts)-1):
        d=math.dist(pts[i],pts[i+1])
        if L>=d: out.append(pts[i+1]); L-=d
        else:
            t=L/d if d else 0; out.append((pts[i][0]+(pts[i+1][0]-pts[i][0])*t,pts[i][1]+(pts[i+1][1]-pts[i][1])*t)); break
    return out
def point_at(pts,f): return partial(pts,f)[-1]

def draw_map(img,c,box,t,draw_t,sweep=None,alpha=1.0):
    P,s=fit(c,box); d=ImageDraw.Draw(img,"RGBA"); a=int(255*alpha)
    for seg in c["ctx"]: d.line([P(p) for p in seg],fill=CTX+(int(70*alpha),),width=3*SS)
    if "runway" in c: d.line([P(p) for p in c["runway"]],fill=CTX+(int(55*alpha),),width=14*SS)
    if "ring" in c:
        (cx,cy),r=c["ring"]; X,Y=P((cx,cy)); R=r*s*SS
        d.ellipse([X-R,Y-R,X+R,Y+R],outline=CTX+(int(120*alpha),),width=3*SS)
    # tracés : vitesse constante (ils racontent un parcours)
    total=sum(plen(r) for r in c["routes"]); f=min(1,max(0,draw_t))*total
    glow=Image.new("RGBA",img.size,(0,0,0,0)); g=ImageDraw.Draw(glow)
    for r in c["routes"]:
        L=plen(r); fr=max(0,min(1,f/L+1e-6)); f-=L
        if fr>0:
            pts=[P(p) for p in partial(r,fr)]
            d.line(pts,fill=GOLD+(a,),width=7*SS,joint="curve"); g.line(pts,fill=GOLD+(int(110*alpha),),width=22*SS,joint="curve")
            hx,hy=pts[-1]
            if fr<0.999: d.ellipse([hx-9*SS,hy-9*SS,hx+9*SS,hy+9*SS],fill=WHITE+(a,))
    if sweep is not None:   # balayage de lumière le long des tracés (allumage)
        for r in c["routes"]:
            for k in range(14):
                q=sweep-k*0.012
                if 0<=q<=1:
                    x,y=P(point_at(r,q)); rr=(20-k)*SS
                    g.ellipse([x-rr,y-rr,x+rr,y+rr],fill=(255,236,190,int(max(0,160-k*11)*alpha)))
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(10*SS)))
    d=ImageDraw.Draw(img,"RGBA"); fm=font("Medium",22)
    for i,(p,label,off) in enumerate(c["marks"]):
        k=ease((t-0.35-i*0.12)/0.4)
        if k<=0: continue
        X,Y=P(p); R=8*SS
        d.ellipse([X-R,Y-R,X+R,Y+R],fill=WHITE+(int(a*k),))
        d.text((X+off[0]*SS,Y+off[1]*SS+(1-k)*12*SS),label,font=fm,fill=WHITE+(int(a*k),))

def title(img,txt,t,x=110,y=96,sub=None):
    k=ease(t/0.35); d=ImageDraw.Draw(img,"RGBA")
    d.text((x*SS,(y+(1-k)*12)*SS),txt,font=font("SemiBold",34),fill=GOLD+(int(255*k),),spacing=0)
    if sub: d.text((x*SS,(y+52+(1-k)*12)*SS),sub,font=font("Regular",24),fill=WHITE+(int(220*k),))
    d.line([(x*SS,(y-22)*SS),((x+int(60*k))*SS,(y-22)*SS)],fill=GOLD+(int(255*k),),width=3*SS)

def render(name,dur,frame_fn):
    os.makedirs(OUT,exist_ok=True)
    p=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
        "-c:v","libx264","-crf","14","-pix_fmt","yuv420p","-movflags","+faststart",f"{OUT}/{name}.mp4"],stdin=subprocess.PIPE)
    n=int(dur*FPS)
    for i in range(n):
        img=Image.new("RGBA",(W*SS,H*SS),BG+(255,)); frame_fn(img,i/FPS,dur)
        im=img.convert("RGB").resize((W,H),Image.LANCZOS)
        if i==int(n*0.85): im.save(f"{OUT}/{name}_apercu.png")
        p.stdin.write(im.tobytes())
    p.stdin.close(); p.wait()

FULL=(110,170,1700,860)
def plan(c,sub):
    def fn(img,t,dur):
        fade=ease(t/0.5)
        draw_map(img,c,FULL,t,(t-0.5)/2.5,alpha=fade)
        title(img,c["title"],t,sub=sub)
    return fn
render("plan5a_circuit1",4,plan(C1,"Tracé et points lumineux"))
render("plan6a_circuit2",4,plan(C2,"Tracé et points lumineux"))

def synth(img,t,dur):
    fade=ease(t/0.6)*(1-ease((t-dur+0.8)/0.8))
    draw_map(img,C1,(60,200,1000,760),t,1,sweep=(t-1.0)/5.5,alpha=fade)
    draw_map(img,C2,(1080,170,780,820),t,1,sweep=(t-1.6)/5.5,alpha=fade)
    k=ease((t-6.8)/0.6)*fade; d=ImageDraw.Draw(img,"RGBA")
    d.text((110*SS,96*SS),"DEUX CIRCUITS, UNE NUIT RENDUE À LA VILLE",font=font("SemiBold",34),fill=GOLD+(int(255*fade),))
    d.text((110*SS,148*SS),"Ouagadougou",font=font("Regular",24),fill=WHITE+(int(220*fade),))
render("plan7_synthese",10,synth)
print("ok")
