#!/usr/bin/env python3
"""Compositor de carrusel IG 4:5 (1080x1350) — enmarca capturas REALES de la app
con la marca Oceanpex. Reutiliza paleta/fuentes de spot-compose.py."""
import os, textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1350
NAVY_DARK=(5,11,24); NAVY_MID=(10,22,46); NAVY_LIGHT=(15,41,66)
CYAN=(56,224,232); CORAL=(255,107,122); WHITE=(255,255,255); MUTED=(148,172,196)
F_DIR="/usr/share/fonts/truetype/montserrat"; F_INT="/usr/share/fonts/opentype/inter"
HELP="/home/amos/oceanpex-repos/op_surf_webapp/public/help"
OUT="/tmp/claude-1000/-home-amos-oceanpex-repos-op-surf-ceo/08769478-5b4d-4322-a5ce-42b669a01530/scratchpad/ig_out"
os.makedirs(OUT, exist_ok=True)

def mont(w,s):
    n={"black":"Montserrat-Black.ttf","bold":"Montserrat-Bold.ttf","semibold":"Montserrat-SemiBold.ttf","medium":"Montserrat-Medium.ttf"}[w]
    return ImageFont.truetype(f"{F_DIR}/{n}", s)
def inter(w,s):
    n={"regular":"Inter-Regular.otf","medium":"Inter-Medium.otf","semibold":"Inter-SemiBold.otf"}[w]
    return ImageFont.truetype(f"{F_INT}/{n}", s)

def bg():
    im=Image.new("RGB",(W,H),NAVY_DARK); d=ImageDraw.Draw(im)
    for y in range(H):
        t=y/H
        c=tuple(int(NAVY_DARK[i]+(NAVY_MID[i]-NAVY_DARK[i])*t) for i in range(3))
        d.line([(0,y),(W,y)],fill=c)
    # glow suave arriba
    g=Image.new("RGB",(W,H),NAVY_DARK); gd=ImageDraw.Draw(g)
    gd.ellipse([W//2-420,-360,W//2+420,300],fill=NAVY_LIGHT)
    g=g.filter(ImageFilter.GaussianBlur(160))
    return Image.blend(im,g,0.35)

def wrap(d,text,font,maxw):
    words=text.split(); lines=[]; cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if d.textlength(t,font=font)<=maxw: cur=t
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines

def kicker(d,text,y,color=CYAN):
    f=mont("bold",30)
    tx="  ".join(list(text.upper()))  # tracking
    tx=text.upper()
    d.text((90,y),tx,font=f,fill=color)
    return y+52

def draw_text_block(d,lines,font,x,y,fill,lh):
    for ln in lines:
        d.text((x,y),ln,font=font,fill=fill); y+=lh
    return y

def rounded(img,rad):
    m=Image.new("L",img.size,0); ImageDraw.Draw(m).rounded_rectangle([0,0,img.size[0],img.size[1]],rad,fill=255)
    out=Image.new("RGBA",img.size,(0,0,0,0)); out.paste(img,(0,0),m); return out

def place_shot(canvas,path,box):
    """box=(x,y,w,h); encaja la captura preservando aspecto, centrada en X, ANCLADA ARRIBA en Y
    (para agrupar con el texto debajo). Marco redondeado + sombra. Devuelve el borde inferior."""
    bx,by,bw,bh=box
    im=Image.open(path).convert("RGB")
    r=min(bw/im.width, bh/im.height)
    nw,nh=int(im.width*r),int(im.height*r)
    im=im.resize((nw,nh),Image.LANCZOS)
    im=rounded(im,28)
    px,py=bx+(bw-nw)//2, by
    sh=Image.new("RGBA",canvas.size,(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle([px,py+10,px+nw,py+nh+10],28,fill=(0,0,0,120))
    sh=sh.filter(ImageFilter.GaussianBlur(24)); canvas.alpha_composite(sh)
    canvas.alpha_composite(im.convert("RGBA"),(px,py))
    return py+nh

def base():
    return bg().convert("RGBA")

def save(canvas,name):
    canvas.convert("RGB").save(f"{OUT}/{name}",quality=95)
    print("→",name)

def logo(d):
    d.text((90,H-70),"oceanpex.com",font=mont("semibold",34),fill=MUTED)

# ---- Slide 1: hook (texto) ----
c=base(); d=ImageDraw.Draw(c)
y=kicker(d,"El mar, sin intermediarios",150)
y=170
lines=wrap(d,"Casi todas las apps de surf te resumen el mar en una nota.",mont("bold",72),900)
y=draw_text_block(d,lines,mont("bold",72),90,260,WHITE,88)
d.text((90,y+40),"Nosotros no.",font=mont("black",96),fill=CYAN)
logo(d); save(c,"01-hook.png")

# ---- Slides 2-4: captura + panel ----
def shot_slide(name,kick,kcol,shot,caption,capcolor=WHITE):
    c=base(); d=ImageDraw.Draw(c)
    kicker(d,kick,110,kcol)
    bottom=place_shot(c,f"{HELP}/{shot}",(70,210,940,780))
    d=ImageDraw.Draw(c)
    lines=wrap(d,caption,inter("medium",42),900)
    draw_text_block(d,lines,inter("medium",42),90,bottom+80,capcolor,60)
    logo(d); save(c,name)

shot_slide("02-verdict.png","Sin veredicto",CYAN,"help-verdict.webp",
    "«Valora con los datos y la marea.» Te damos el rango del día y la tendencia — el veredicto lo pones tú.")
shot_slide("03-rojo.png","Las horas en rojo",CORAL,"help-golden-window.webp",
    "Las horas en rojo, directamente, no valen. El resto lo lees tú. Sin estrellitas.")
shot_slide("04-swell.png","Por dónde entra el mar",CYAN,"help-swell.webp",
    "Tamaño, periodo y dirección de cada swell. No un número suelto que decide por ti.")

# ---- Slide 5: CTA ----
c=base(); d=ImageDraw.Draw(c)
kicker(d,"125 spots · España y Portugal",150)
d.text((90,300),"Tu spot.",font=mont("black",110),fill=WHITE)
d.text((90,430),"Gratis.",font=mont("black",110),fill=CYAN)
lines=wrap(d,"Oleaje, viento y marea por franjas, en escala humana. La decisión, tuya.",inter("medium",44),900)
draw_text_block(d,lines,inter("medium",44),90,640,MUTED,62)
d.text((90,900),"oceanpex.com",font=mont("bold",64),fill=CYAN)
save(c,"05-cta.png")
print("OK")
