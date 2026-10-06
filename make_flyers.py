import os, sys
# The renderer is shared by both flyer repos and lives in the meta-campaign skill.
sys.path.insert(0, os.environ.get("FLYER_RENDERER") or os.path.join(
    os.path.expanduser("~"), ".claude", "skills", "meta-campaign", "renderer"))
from PIL import Image, ImageDraw
from flyer_common import *
import os

# Output dir, resolved relative to this file so the script works from any cwd.
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "ai-creative-designer")

TITLE = "AI Designer"
KICKER = "WE'RE HIRING"
SUBHEAD = "Social-First  ·  100% Remote  ·  Freelance"
DESC = "Concept and ship social-first creative for an established Canadian consumer brand, with AI image and video generation as the primary engine behind the work - not a finishing touch."
DESC_SHORT = "Social-first creative for a Canadian consumer brand, with AI generation as the primary engine."
BULLETS = [
    "AI generation as the creative engine",
    "Instagram, TikTok, LinkedIn, YouTube",
    "Direct line to the Creative Director",
    "Freelance in USD, long-term fit",
]
BULLETS_SHORT = [
    "AI generation as the creative engine",
    "IG, TikTok, LinkedIn and YouTube",
    "Freelance in USD, 100% remote",
]
# Chip counts are set by measured row width, not taste: five chips overflow every
# format here, and a wrapped second row is what pushes the caption under the
# footer band on the square. Four fit the 9:16, three fit everything else.
CHIPS = ["Midjourney", "Runway", "C1 English", "LATAM"]
CHIPS_SHORT = ["Midjourney", "C1 English", "LATAM"]
CAPTION = "Prompt it. Cut it. Ship it."
URL = "www.talenty.dev"

# "AI Designer" is short enough for the full 104px headline against a 0.63 panel,
# the same envelope "AI Developer" used - it clears the motif's left edge.
PANEL = 0.63
T_SQ = 104


def draw_chips(d, img, x, y, chips, fnt, max_w, gap=14, padx=20, pady=11):
    cx=x; cy=y; rowh=0; placed=[]
    for c in chips:
        tw=text_w(d,c,fnt); th,off=bbox_h(d,c,fnt)
        cw=tw+padx*2; ch=th+pady*2
        if cx+cw > x+max_w:
            cx=x; cy+=ch+gap
        placed.append((cx,cy,cw,ch,c,off,th)); cx+=cw+gap; rowh=ch
    for (bx,by,cw,ch,c,off,th) in placed:
        d.rounded_rectangle([bx,by,bx+cw,by+ch], radius=ch//2, fill=LIGHT_BLUE)
        d.text((bx+padx, by+ch//2 - th//2 - off), c, font=fnt, fill=TALENTY_BLUE)
    return cy+rowh

def base(W,H):
    img=Image.new("RGBA",(W,H),(255,255,255,255)); blueprint_grid(img, step=max(46,W//24)); return img

def footer(img, hpx):
    W,H=img.size; d=ImageDraw.Draw(img)
    d.rectangle([0,H-hpx,W,H], fill=FOOT_INK)
    f=inter_sb(int(hpx*0.30)); th,off=bbox_h(d,URL,f)
    d.text((int(W*0.05), H-hpx//2 - th//2 - off), URL, font=f, fill=WHITE)
    r=int(hpx*0.13); d.ellipse([W-int(W*0.05)-r, H-hpx//2-r, W-int(W*0.05)+r, H-hpx//2+r], fill=TALENTY_BLUE)

def kicker(d, x, y, s):
    f=osw_sb(s); track=6; cx=x
    d.line([(x, y+s//2),(x+s*1.4, y+s//2)], fill=TALENTY_BLUE, width=3); cx=x+int(s*1.7)
    for ch in KICKER:
        d.text((cx,y), ch, font=f, fill=TALENTY_BLUE); cx+=text_w(d,ch,f)+track
    return y+s

def render_1x1():
    W=H=1080; img=base(W,H); d=ImageDraw.Draw(img); M=int(W*0.065)
    light_panel(img, [0,0,int(W*PANEL),H]); d=ImageDraw.Draw(img)
    lw,lh=paste_logo(img, M, M, 74); d=ImageDraw.Draw(img)
    y=M+lh+40; y=kicker(d,M,y,30)+34
    tf=osw_b(T_SQ); d.text((M,y), TITLE, font=tf, fill=INK); th,off=bbox_h(d,TITLE,tf); y+=th+off+16
    sf=osw_m(34); d.text((M,y), SUBHEAD, font=sf, fill=TALENTY_BLUE); sh,so=bbox_h(d,SUBHEAD,sf); y+=sh+30
    dimension_line(d, M, y, int(W*0.58), y); y+=28
    df=inter(29)
    for ln in wrap(d, DESC_SHORT, df, int(W*0.53)):
        d.text((M,y), ln, font=df, fill=BODY_GRAY); lh2,o2=bbox_h(d,ln,df); y+=lh2+11
    y+=20
    bf=inter_m(30)
    for b in BULLETS_SHORT:
        d.rectangle([M, y+8, M+16, y+24], fill=TALENTY_BLUE)
        for ln in wrap(d,b,bf,int(W*0.48)):
            d.text((M+32,y), ln, font=bf, fill=INK); bh,bo=bbox_h(d,ln,bf); y+=bh+9
        y+=8
    y+=16; y=draw_chips(d,img,M,y,CHIPS_SHORT,inter_sb(26),int(W*0.545))+34
    cf=osw_sb(38); d.text((M,y), CAPTION, font=cf, fill=INK)
    genstack_motif(img, int(W*0.845), int(H*0.44), int(W*0.25), int(H*0.32))
    footer(img, 92); img.convert("RGB").save(os.path.join(OUT, "AICreativeDesigner_Talenty_1x1_1080x1080.png"), "PNG")

def render_9x16():
    W,H=1080,1920; img=base(W,H); d=ImageDraw.Draw(img); M=int(W*0.075)
    lw,lh=paste_logo(img, M, int(H*0.055), 82); d=ImageDraw.Draw(img)
    y=int(H*0.055)+lh+56; y=kicker(d,M,y,34)+44
    tf=osw_b(130); d.text((M,y), TITLE, font=tf, fill=INK); th,off=bbox_h(d,TITLE,tf); y+=th+off+24
    sf=osw_m(44); d.text((M,y), SUBHEAD, font=sf, fill=TALENTY_BLUE); sh,so=bbox_h(d,SUBHEAD,sf); y+=sh+44
    dimension_line(d, M, y, W-M, y); y+=54
    # The generation stack is a vertical flow, so it takes a narrow tall box here
    # rather than the wide one a horizontal motif would want.
    genstack_motif(img, W//2, int(H*0.47), int(W*0.34), int(H*0.23)); y=int(H*0.615)
    df=inter(36)
    for ln in wrap(d, DESC, df, W-2*M):
        d.text((M,y), ln, font=df, fill=BODY_GRAY); lh2,o2=bbox_h(d,ln,df); y+=lh2+14
    y+=22
    bf=inter_m(37)
    for b in BULLETS:
        d.rectangle([M, y+10, M+18, y+28], fill=TALENTY_BLUE)
        d.text((M+34,y), b, font=bf, fill=INK); bh,bo=bbox_h(d,b,bf); y+=bh+18
    y+=14; y=draw_chips(d,img,M,y,CHIPS,inter_sb(31),W-2*M)+42
    cf=osw_sb(50); d.text((M,y), CAPTION, font=cf, fill=INK)
    footer(img, 118); img.convert("RGB").save(os.path.join(OUT, "AICreativeDesigner_Talenty_9x16_1080x1920.png"), "PNG")

def render_191x1():
    W,H=1200,628; img=base(W,H); d=ImageDraw.Draw(img); M=int(W*0.05)
    light_panel(img, [0,0,int(W*0.63),H]); d=ImageDraw.Draw(img)
    lw,lh=paste_logo(img, M, int(H*0.09), 58); d=ImageDraw.Draw(img)
    y=int(H*0.09)+lh+22; y=kicker(d,M,y,24)+20
    tf=osw_b(84); d.text((M,y), TITLE, font=tf, fill=INK); th,off=bbox_h(d,TITLE,tf); y+=th+off+12
    sf=osw_m(27); d.text((M,y), SUBHEAD, font=sf, fill=TALENTY_BLUE); sh,so=bbox_h(d,SUBHEAD,sf); y+=sh+22
    bf=inter_m(25)
    for b in BULLETS_SHORT:
        d.rectangle([M, y+7, M+14, y+21], fill=TALENTY_BLUE)
        d.text((M+28,y), b, font=bf, fill=INK); bh,bo=bbox_h(d,b,bf); y+=bh+12
    y+=8; draw_chips(d,img,M,y,CHIPS_SHORT,inter_sb(23),int(W*0.56))
    genstack_motif(img, int(W*0.815), int(H*0.50), int(W*0.24), int(H*0.56))
    footer(img, 70); img.convert("RGB").save(os.path.join(OUT, "AICreativeDesigner_Talenty_1.91x1_1200x628.png"), "PNG")

def render_4x5():
    W,H=1080,1350; img=base(W,H); d=ImageDraw.Draw(img); M=int(W*0.065)
    light_panel(img, [0,0,int(W*PANEL),H]); d=ImageDraw.Draw(img)
    lw,lh=paste_logo(img, M, M, 74); d=ImageDraw.Draw(img)
    y=M+lh+34; y=kicker(d,M,y,30)+30
    tf=osw_b(T_SQ); d.text((M,y), TITLE, font=tf, fill=INK); th,off=bbox_h(d,TITLE,tf); y+=th+off+18
    sf=osw_m(34); d.text((M,y), SUBHEAD, font=sf, fill=TALENTY_BLUE); sh,so=bbox_h(d,SUBHEAD,sf); y+=sh+34
    dimension_line(d, M, y, int(W*0.58), y); y+=30
    df=inter(30)
    for ln in wrap(d, DESC, df, int(W*0.53)):
        d.text((M,y), ln, font=df, fill=BODY_GRAY); lh2,o2=bbox_h(d,ln,df); y+=lh2+12
    y+=20
    bf=inter_m(31)
    for b in BULLETS:
        d.rectangle([M, y+8, M+16, y+25], fill=TALENTY_BLUE)
        # 0.52 is the widest the bullets can run before leaving the narrower panel
        for ln in wrap(d,b,bf,int(W*0.52)):
            d.text((M+32,y), ln, font=bf, fill=INK); bh,bo=bbox_h(d,ln,bf); y+=bh+10
        y+=8
    y+=14; y=draw_chips(d,img,M,y,CHIPS_SHORT,inter_sb(27),int(W*0.545))+34
    cf=osw_sb(40); d.text((M,y), CAPTION, font=cf, fill=INK)
    genstack_motif(img, int(W*0.845), int(H*0.42), int(W*0.25), int(H*0.28))
    footer(img, 96); img.convert("RGB").save(os.path.join(OUT, "AICreativeDesigner_Talenty_4x5_1080x1350.png"), "PNG")

os.makedirs(OUT, exist_ok=True)
render_1x1(); render_9x16(); render_191x1(); render_4x5()
print("rendered:", sorted(os.listdir(OUT)))
