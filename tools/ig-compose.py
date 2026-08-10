#!/usr/bin/env python3
"""Carrusel IG 4:5 (1080x1350) con GRÁFICOS reales de la app enmarcados.
Formato preferido por el fundador. Colores/tipografía alineados con los posts
publicados: azul de marca (28,153,248), Montserrat + Inter, fondo navy."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H=1080,1350
BG_TOP=(9,15,27); BG_BOT=(12,20,36); GLOW=(20,34,58)
ACCENT=(28,153,248); WHITE=(245,248,252); SUB=(148,163,184)
FM="/usr/share/fonts/truetype/montserrat"; FI="/usr/share/fonts/opentype/inter"
HELP="/home/amos/oceanpex-repos/op_surf_webapp/public/help"
OUT="/tmp/claude-1000/-home-amos-oceanpex-repos-op-surf-ceo/08769478-5b4d-4322-a5ce-42b669a01530/scratchpad/ig_out"
os.makedirs(OUT,exist_ok=True)

def mont(w,s):
    n={"black":"Montserrat-Black.ttf","bold":"Montserrat-Bold.ttf","semibold":"Montserrat-SemiBold.ttf","medium":"Montserrat-Medium.ttf"}[w]
    return ImageFont.truetype(f"{FM}/{n}",s)
def inter(w,s):
    n={"regular":"Inter-Regular.otf","medium":"Inter-Medium.otf","semibold":"Inter-SemiBold.otf"}[w]
    return ImageFont.truetype(f"{FI}/{n}",s)

def bg():
    im=Image.new("RGB",(W,H),BG_TOP); d=ImageDraw.Draw(im)
    for y in range(H):
        t=y/H; c=tuple(int(BG_TOP[i]+(BG_BOT[i]-BG_TOP[i])*t) for i in range(3))
        d.line([(0,y),(W,y)],fill=c)
    g=Image.new("RGB",(W,H),(0,0,0)); ImageDraw.Draw(g).ellipse([540,360,1200,1120],fill=GLOW)
    g=g.filter(ImageFilter.GaussianBlur(200))
    return Image.blend(im,g,0.5).convert("RGBA")

def tracked(d,text,x,y,font,fill,track,right=None):
    text=text.upper(); ws=[d.textlength(c,font=font)+track for c in text]; tot=sum(ws)-track
    if right is not None: x=right-tot
    for c,w in zip(text,ws): d.text((x,y),c,font=font,fill=fill); x+=w
    return tot

def wrap(d,text,font,maxw):
    o=[]
    for para in text.split("\n"):
        cur=""
        for w in para.split():
            t=(cur+" "+w).strip()
            if d.textlength(t,font=font)<=maxw: cur=t
            else: o.append(cur); cur=w
        o.append(cur)
    return o

def rounded(img,rad):
    m=Image.new("L",img.size,0); ImageDraw.Draw(m).rounded_rectangle([0,0,img.size[0],img.size[1]],rad,fill=255)
    out=Image.new("RGBA",img.size,(0,0,0,0)); out.paste(img,(0,0),m); return out

def load_shot(name):
    im=Image.open(f"{HELP}/{name}").convert("RGB")
    if "golden-window" in name:      # quitar divisor + cabecera "FRANJAS/Ver detalle"; dejar puntos+horas
        im=im.crop((0,92,im.width,im.height))
    return im

def place_shot(canvas,name,x,y,maxw,maxh):
    im=load_shot(name); r=min(maxw/im.width,maxh/im.height); nw,nh=int(im.width*r),int(im.height*r)
    im=rounded(im.resize((nw,nh),Image.LANCZOS),26)
    px=x+(maxw-nw)//2; py=y
    sh=Image.new("RGBA",canvas.size,(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle([px,py+10,px+nw,py+nh+10],26,fill=(0,0,0,120))
    canvas.alpha_composite(sh.filter(ImageFilter.GaussianBlur(24))); canvas.alpha_composite(im.convert("RGBA"),(px,py))
    return py+nh

def logo(d): d.text((90,H-72),"oceanpex.com",font=mont("semibold",34),fill=SUB)
def kicker(d,t,y): tracked(d,t,90,y,mont("bold",30),ACCENT,4); return y+50
def save(c,n): c.convert("RGB").save(f"{OUT}/{n}",quality=95); print("→",n)

# Slide 1 — hook (tamaños de antes)
c=bg(); d=ImageDraw.Draw(c)
kicker(d,"El mar, sin atajos",150)
y=250
for ln in wrap(d,"Casi todas las apps de surf te resumen el mar en una nota.",mont("bold",72),900):
    d.text((90,y),ln,font=mont("bold",72),fill=WHITE); y+=86
d.text((90,y+34),"Nosotros no.",font=mont("black",92),fill=ACCENT)
logo(d); save(c,"01-hook.png")

def shot_slide(name,kick,shot,caption):
    c=bg(); d=ImageDraw.Draw(c); kicker(d,kick,110)
    bottom=place_shot(c,shot,70,210,940,760); d=ImageDraw.Draw(c)
    yy=bottom+80
    for ln in wrap(d,caption,inter("medium",42),900): d.text((90,yy),ln,font=inter("medium",42),fill=WHITE); yy+=60
    logo(d); save(c,name)

shot_slide("02-verdict.png","Sin veredicto","help-verdict.webp",
    "«Valora con los datos y la marea.» Te damos el rango del día y la tendencia — el veredicto lo pones tú.")
shot_slide("03-rojo.png","Las horas en rojo","help-golden-window.webp",
    "Las horas en rojo, directamente, no valen. El resto lo lees tú. Sin estrellitas.")
shot_slide("04-swell.png","Por dónde entra el mar","help-swell.webp",
    "Tamaño, periodo y dirección de cada swell. No un número suelto que decide por ti.")

# Slide 5 — CTA
c=bg(); d=ImageDraw.Draw(c)
kicker(d,"125 spots · España y Portugal",150)
d.text((90,300),"Tu spot.",font=mont("black",104),fill=WHITE)
d.text((90,424),"Gratis.",font=mont("black",104),fill=ACCENT)
yy=620
for ln in wrap(d,"Oleaje, viento y marea por franjas, en escala humana. La decisión, tuya.",inter("medium",44),900):
    d.text((90,yy),ln,font=inter("medium",44),fill=SUB); yy+=62
d.text((90,yy+30),"oceanpex.com",font=mont("bold",60),fill=ACCENT)
save(c,"05-cta.png"); print("OK")
