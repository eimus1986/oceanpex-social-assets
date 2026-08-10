#!/usr/bin/env python3
"""Carrusel IG 1080x1080 en la plantilla de casa Oceanpex (igual que
s2-cuatro-datos / s1-offshore-onshore ya publicados): wordmark arriba-derecha,
kicker azul en mayúsculas espaciadas, titular blanco Montserrat, subtítulo
gris, contador abajo-izquierda. Tipográfico, sin capturas incrustadas."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S=1080
BG_TOP=(9,15,27); BG_BOT=(12,20,36); GLOW=(20,34,58)
ACCENT=(28,153,248); WHITE=(245,248,252); SUB=(148,163,184); COUNT=(92,108,134)
F="/usr/share/fonts/truetype/montserrat"
OUT="/tmp/claude-1000/-home-amos-oceanpex-repos-op-surf-ceo/08769478-5b4d-4322-a5ce-42b669a01530/scratchpad/ig_out"
os.makedirs(OUT,exist_ok=True)

def mont(w,s):
    n={"black":"Montserrat-Black.ttf","bold":"Montserrat-Bold.ttf","semibold":"Montserrat-SemiBold.ttf","medium":"Montserrat-Medium.ttf"}[w]
    return ImageFont.truetype(f"{F}/{n}",s)

def bg():
    im=Image.new("RGB",(S,S),BG_TOP); d=ImageDraw.Draw(im)
    for y in range(S):
        t=y/S; c=tuple(int(BG_TOP[i]+(BG_BOT[i]-BG_TOP[i])*t) for i in range(3))
        d.line([(0,y),(S,y)],fill=c)
    g=Image.new("RGB",(S,S),(0,0,0)); ImageDraw.Draw(g).ellipse([560,360,1180,1040],fill=GLOW)
    g=g.filter(ImageFilter.GaussianBlur(200))
    return Image.blend(im,g,0.5)

def tracked(d,text,x,y,font,fill,track,anchor_right=None):
    text=text.upper()
    widths=[d.textlength(ch,font=font)+track for ch in text]
    total=sum(widths)-track
    if anchor_right is not None: x=anchor_right-total
    for ch,w in zip(text,widths):
        d.text((x,y),ch,font=font,fill=fill); x+=w
    return total

def wrap(d,text,font,maxw):
    out=[];
    for para in text.split("\n"):
        words=para.split(); cur=""
        for w in words:
            t=(cur+" "+w).strip()
            if d.textlength(t,font=font)<=maxw: cur=t
            else: out.append(cur); cur=w
        out.append(cur)
    return out

def fit_headline(d,text,maxw,maxlines=3):
    for size in (124,116,108,100,92,84):
        f=mont("black",size); ls=wrap(d,text,f,maxw)
        if len(ls)<=maxlines: return f,ls,int(size*1.12)
    f=mont("black",84); return f,wrap(d,text,f,maxw),94

def slide(idx,total,kick,headline,sub,name):
    c=bg(); d=ImageDraw.Draw(c)
    # wordmark
    tracked(d,"OCEANPEX",0,60,mont("bold",34),ACCENT,7,anchor_right=990)
    # medir bloque
    kf=mont("bold",32)
    hf,hls,hlh=fit_headline(d,headline,900)
    sf=mont("medium",46); sls=wrap(d,sub,sf,900); slh=64
    blockH=52+34+len(hls)*hlh+30+len(sls)*slh
    y=(S-blockH)//2-10
    tracked(d,kick,90,y,kf,ACCENT,5); y+=52+30
    for ln in hls: d.text((90,y),ln,font=hf,fill=WHITE); y+=hlh
    y+=30
    for ln in sls: d.text((90,y),ln,font=sf,fill=SUB); y+=slh
    # contador
    d.text((90,1000),f"{idx} / {total}",font=mont("medium",32),fill=COUNT)
    c.save(f"{OUT}/{name}",quality=95); print("→",name)

N=6
slide(1,N,"El parte, sin atajos","Casi todas las apps te resumen el mar en una nota.","Nosotros no.","01-hook.png")
slide(2,N,"La nota","Un «7» no te dice nada.","Con las mismas estrellas, dos días pueden ser opuestos en el agua.","02-nota.png")
slide(3,N,"Las horas en rojo","Marcamos lo que no vale.","En rojo, las horas que no acompañan. El resto lo lees tú.","03-rojo.png")
slide(4,N,"Escala humana","El mar, en tu cuerpo.","Te llega al pecho, te tapa la cabeza. No solo «1,5 m».","04-escala.png")
slide(5,N,"Todo junto","Oleaje, viento y marea. A la vez.","Franja por franja, con la fuente siempre a la vista.","05-junto.png")
slide(6,N,"Gratis · 125 spots","Tu spot. Sin veredicto.","oceanpex.com","06-cta.png")
print("OK")
