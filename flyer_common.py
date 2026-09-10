from PIL import Image, ImageDraw, ImageFont
import math, random, os

# ---- Talenty brand ----
TALENTY_BLUE = (0, 93, 255)      # #005DFF primary
LIGHT_BLUE   = (232, 240, 255)   # #E8F0FF chip fill
DARK_BLUE    = (10, 42, 67)      # #0A2A43
INK          = (14, 26, 43)      # near-black wordmark tone
GRID_BLUE    = (206, 222, 245)   # faint blueprint lines
FAINT        = (200, 214, 236)   # interior rules inside a motif
BODY_GRAY    = (74, 85, 104)
PANEL        = (250, 252, 255)
WHITE        = (255,255,255)
FOOT_INK     = (26, 33, 45)      # charcoal footer band

# Paths are resolved relative to this file so the scripts work from any cwd.
_HERE = os.path.dirname(os.path.abspath(__file__))
F     = os.path.join(_HERE, "fonts")
LOGO  = os.path.join(_HERE, "assets", "talenty-logo.jpg")
def font(name, sz): return ImageFont.truetype(os.path.join(F, name), sz)
def osw_b(s):  return font("Oswald-Bold.ttf", s)
def osw_sb(s): return font("Oswald-SemiBold.ttf", s)
def osw_m(s):  return font("Oswald-Medium.ttf", s)
def inter(s):  return font("Inter-400.ttf", s)
def inter_m(s):return font("Inter-500.ttf", s)
def inter_sb(s):return font("Inter-600.ttf", s)
def inter_b(s):return font("Inter-700.ttf", s)

def bbox_h(draw, txt, fnt):
    b = draw.textbbox((0,0), txt, font=fnt); return b[3]-b[1], b[1]
def text_w(draw, txt, fnt):
    b = draw.textbbox((0,0), txt, font=fnt); return b[2]-b[0]

def blueprint_grid(img, step=54):
    d = ImageDraw.Draw(img); W,H = img.size
    for x in range(0, W, step): d.line([(x,0),(x,H)], fill=GRID_BLUE, width=1)
    for y in range(0, H, step): d.line([(0,y),(W,y)], fill=GRID_BLUE, width=1)

def light_panel(img, box, radius=0):
    W,H = img.size
    ov = Image.new("RGBA",(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov)
    od.rectangle(box, fill=(250,252,255,238))
    img.alpha_composite(ov)

def paste_logo(img, x, y, target_h):
    lg = Image.open(LOGO).convert("RGB")
    w,h = lg.size; nw = int(w*target_h/h)
    lg = lg.resize((nw, target_h), Image.LANCZOS)
    img.paste(lg, (x,y))
    return nw, target_h

def wrap(draw, txt, fnt, max_w):
    words = txt.split(); lines=[]; cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if text_w(draw,t,fnt)<=max_w: cur=t
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines

def dimension_line(d, x1, y1, x2, y2, color=TALENTY_BLUE, w=2, tick=7):
    d.line([(x1,y1),(x2,y2)], fill=color, width=w)
    ang = math.atan2(y2-y1, x2-x1)
    for (px,py) in [(x1,y1),(x2,y2)]:
        dx=tick*math.cos(ang+math.pi/2); dy=tick*math.sin(ang+math.pi/2)
        d.line([(px-dx,py-dy),(px+dx,py+dy)], fill=color, width=w)

def ds_motif(img, cx, cy, w, h, label_room=True):
    """Regression-scatter technical drawing for the data-science domain."""
    d = ImageDraw.Draw(img)
    x0,y0 = cx-w//2, cy-h//2
    x1,y1 = cx+w//2, cy+h//2
    d.line([(x0,y1),(x1,y1)], fill=DARK_BLUE, width=3)   # x axis
    d.line([(x0,y0),(x0,y1)], fill=DARK_BLUE, width=3)   # y axis
    for i in range(1,5):
        gx = x0 + (x1-x0)*i/5; gy = y0 + (y1-y0)*i/5
        d.line([(gx,y0),(gx,y1)], fill=(200,214,236), width=1)
        d.line([(x0,gy),(x1,gy)], fill=(200,214,236), width=1)
    random.seed(7); pts=[]; n=26
    for i in range(n):
        t=i/(n-1)
        px = x0 + (x1-x0)*(0.06+0.9*t)
        base = y1 - (y1-y0)*(0.10+0.8*t)
        py = base + random.uniform(-1,1)*(y1-y0)*0.09
        pts.append((px,py)); r=5
        d.ellipse([px-r,py-r,px+r,py+r], fill=TALENTY_BLUE, outline=WHITE, width=1)
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    mx=sum(xs)/len(xs); my=sum(ys)/len(ys)
    b=sum((xs[i]-mx)*(ys[i]-my) for i in range(len(xs)))/sum((x-mx)**2 for x in xs)
    a=my-b*mx
    lx0,lx1 = x0+(x1-x0)*0.04, x1-(x1-x0)*0.02
    d.line([(lx0, a+b*lx0),(lx1, a+b*lx1)], fill=DARK_BLUE, width=3)
    d.line([(x0-26,y0),(x0-26,y1)], fill=TALENTY_BLUE, width=2); dimension_line(d, x0-26, y0, x0-26, y1)
    d.line([(x0,y1+26),(x1,y1+26)], fill=TALENTY_BLUE, width=2); dimension_line(d, x0, y1+26, x1, y1+26)
    return (x0,y0,x1,y1)

def _arrow(d, x1, y1, x2, y2, color=DARK_BLUE, w=2, head=8):
    d.line([(x1,y1),(x2,y2)], fill=color, width=w)
    ang = math.atan2(y2-y1, x2-x1)
    for s in (+1,-1):
        a = ang + math.pi + s*0.42
        d.line([(x2,y2),(x2+head*math.cos(a), y2+head*math.sin(a))], fill=color, width=w)

def _node(d, x, y, w, h, lines=2, r=8):
    """A blueprint box with faint blue rules inside, standing in for prompt text."""
    d.rounded_rectangle([x,y,x+w,y+h], radius=r, outline=DARK_BLUE, width=3)
    for i in range(lines):
        ly = y + h*(i+1)/(lines+1)
        lw = w*(0.62 if i%2==0 else 0.44)
        d.line([(x+w*0.13, ly),(x+w*0.13+lw, ly)], fill=TALENTY_BLUE, width=2)

def chain_motif(img, cx, cy, w, h, label_room=True):
    """Prompt-chain DAG: input into a prompt node, branching model calls, merged output."""
    d = ImageDraw.Draw(img)
    x0,y0 = cx-w//2, cy-h//2
    x1,y1 = cx+w//2, cy+h//2
    for i in range(1,4):
        gy = y0 + (y1-y0)*i/4
        d.line([(x0,gy),(x1,gy)], fill=(200,214,236), width=1)
    for i in range(1,3):
        gx = x0 + (x1-x0)*i/3
        d.line([(gx,y0),(gx,y1)], fill=(200,214,236), width=1)
    def px(f): return x0 + (x1-x0)*f
    def py(f): return y0 + (y1-y0)*f
    iw, ih = w*0.30, h*0.075                                  # input
    _node(d, px(0.5)-iw/2, py(0.02), iw, ih, lines=1)
    pw, ph = w*0.62, h*0.15                                   # the prompt itself
    _node(d, px(0.5)-pw/2, py(0.19), pw, ph, lines=3)
    _arrow(d, px(0.5), py(0.02)+ih, px(0.5), py(0.19)-4)
    bw, bh = w*0.40, h*0.14                                   # two model calls
    for bx in (0.235, 0.765):
        _node(d, px(bx)-bw/2, py(0.46), bw, bh, lines=2)
    ymid = py(0.395)
    d.line([(px(0.5), py(0.19)+ph),(px(0.5), ymid)], fill=DARK_BLUE, width=2)
    d.line([(px(0.235), ymid),(px(0.765), ymid)], fill=DARK_BLUE, width=2)
    for bx in (0.235, 0.765):
        _arrow(d, px(bx), ymid, px(bx), py(0.46)-4)
        d.ellipse([px(bx)-4, ymid-4, px(bx)+4, ymid+4], fill=TALENTY_BLUE)
    d.ellipse([px(0.5)-4, ymid-4, px(0.5)+4, ymid+4], fill=TALENTY_BLUE)
    ymrg = py(0.72)                                           # merge back to one output
    for bx in (0.235, 0.765):
        d.line([(px(bx), py(0.46)+bh),(px(bx), ymrg)], fill=DARK_BLUE, width=2)
    d.line([(px(0.235), ymrg),(px(0.765), ymrg)], fill=DARK_BLUE, width=2)
    ow, oh = w*0.46, h*0.12
    _arrow(d, px(0.5), ymrg, px(0.5), py(0.80)-4)
    _node(d, px(0.5)-ow/2, py(0.80), ow, oh, lines=2)
    d.ellipse([px(0.5)-4, ymrg-4, px(0.5)+4, ymrg+4], fill=TALENTY_BLUE)
    dimension_line(d, x0-24, py(0.19), x0-24, py(0.46)+bh)
    return (x0,y0,x1,y1)


def _cylinder(d, x, y, w, h, rules=2):
    """A database cylinder in blueprint line art."""
    ell = h * 0.20
    d.ellipse([x, y, x + w, y + ell * 2], outline=DARK_BLUE, width=3)
    d.line([(x, y + ell), (x, y + h - ell)], fill=DARK_BLUE, width=3)
    d.line([(x + w, y + ell), (x + w, y + h - ell)], fill=DARK_BLUE, width=3)
    d.arc([x, y + h - ell * 2, x + w, y + h], 0, 180, fill=DARK_BLUE, width=3)
    for i in range(rules):
        ry = y + ell * 2 + (h - ell * 3) * (i + 0.5) / rules
        d.arc([x, ry - ell, x + w, ry + ell], 0, 180, fill=TALENTY_BLUE, width=2)


def stack_motif(img, cx, cy, w, h, label_room=True):
    """Integration schematic: an AI model and an API wired through a service into SQL storage."""
    d = ImageDraw.Draw(img)
    x0, y0 = cx - w // 2, cy - h // 2
    x1, y1 = cx + w // 2, cy + h // 2
    for i in range(1, 4):
        gx = x0 + (x1 - x0) * i / 4
        d.line([(gx, y0), (gx, y1)], fill=FAINT, width=1)
    for i in range(1, 5):
        gy = y0 + (y1 - y0) * i / 5
        d.line([(x0, gy), (x1, gy)], fill=FAINT, width=1)

    def px(f): return x0 + (x1 - x0) * f
    def py(f): return y0 + (y1 - y0) * f

    # the model node up top - three tokens in a row
    mw, mh = w * 0.52, h * 0.115
    mx, my = px(0.50) - mw / 2, py(0.02)
    d.rounded_rectangle([mx, my, mx + mw, my + mh], radius=int(mh * 0.42),
                        outline=DARK_BLUE, width=3)
    for i in range(3):
        tx = mx + mw * (0.28 + i * 0.22)
        d.ellipse([tx - 5, my + mh / 2 - 5, tx + 5, my + mh / 2 + 5], fill=TALENTY_BLUE)

    # the external API on the left
    aw, ah = w * 0.20, h * 0.09
    _node(d, x0, py(0.45) - ah / 2, aw, ah, lines=1, r=4)

    # the service in the middle
    sw, sh = w * 0.46, h * 0.145
    sx, sy = px(0.50) - sw / 2, py(0.38)
    d.rectangle([sx, sy, sx + sw, sy + sh], outline=DARK_BLUE, width=3)
    d.line([(sx, sy + sh * 0.34), (sx + sw, sy + sh * 0.34)], fill=DARK_BLUE, width=2)
    for i in range(3):
        vx = sx + sw * (0.22 + i * 0.28)
        d.line([(vx, sy + sh * 0.52), (vx, sy + sh * 0.80)], fill=TALENTY_BLUE, width=2)

    # storage below
    cw, ch = w * 0.40, h * 0.28
    _cylinder(d, px(0.50) - cw / 2, py(0.68), cw, ch, rules=2)

    _arrow(d, px(0.50), my + mh, px(0.50), sy - 4)
    _arrow(d, x0 + aw, py(0.45), sx - 4, py(0.45))
    _arrow(d, px(0.50), sy + sh, px(0.50), py(0.68) - 4)
    for pt in ((0.50, 0.31), (0.50, 0.60)):
        d.ellipse([px(pt[0]) - 4, py(pt[1]) - 4, px(pt[0]) + 4, py(pt[1]) + 4],
                  fill=TALENTY_BLUE)
    d.line([(x0 - 26, my), (x0 - 26, py(0.68) + ch)], fill=TALENTY_BLUE, width=2)
    dimension_line(d, x0 - 26, my, x0 - 26, py(0.68) + ch)
    return (x0, y0, x1, y1)


def _corner_marks(d, x0, y0, x1, y1, color=TALENTY_BLUE, w=3, ln=12):
    """Crop marks on a selected frame."""
    for (px, py, sx, sy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        d.line([(px, py), (px + ln * sx, py)], fill=color, width=w)
        d.line([(px, py), (px, py + ln * sy)], fill=color, width=w)


def genstack_motif(img, cx, cy, w, h, label_room=True):
    """Generation pipeline - a prompt into a generator, a 2x2 candidate grid, one selected out."""
    d = ImageDraw.Draw(img)
    x0, y0 = cx - w // 2, cy - h // 2
    x1, y1 = cx + w // 2, cy + h // 2

    def px(f): return x0 + (x1 - x0) * f
    def py(f): return y0 + (y1 - y0) * f

    for i in range(1, 4):
        d.line([(px(i / 4), y0), (px(i / 4), y1)], fill=FAINT, width=1)
    for i in range(1, 5):
        d.line([(x0, py(i / 5)), (x1, py(i / 5))], fill=FAINT, width=1)

    pw, ph = w * 0.58, h * 0.115
    _node(d, px(0.5) - pw / 2, py(0.0), pw, ph, lines=2, r=8)

    gy = py(0.235)
    gr = h * 0.062
    d.polygon([(px(0.5), gy - gr), (px(0.5) + gr, gy), (px(0.5), gy + gr), (px(0.5) - gr, gy)],
              outline=DARK_BLUE, width=3)
    d.ellipse([px(0.5) - 5, gy - 5, px(0.5) + 5, gy + 5], fill=TALENTY_BLUE)
    _arrow(d, px(0.5), py(0.0) + ph, px(0.5), gy - gr - 4)

    cw, ch = w * 0.30, h * 0.155
    gap = w * 0.06
    gx0 = px(0.5) - cw - gap / 2
    gty = py(0.40)
    cells = []
    for r in range(2):
        for c in range(2):
            ax = gx0 + c * (cw + gap)
            ay = gty + r * (ch + h * 0.045)
            d.rectangle([ax, ay, ax + cw, ay + ch], outline=DARK_BLUE, width=3)
            d.line([(ax + cw * 0.12, ay + ch * 0.66), (ax + cw * 0.88, ay + ch * 0.66)],
                   fill=FAINT, width=2)
            cells.append((ax, ay, ax + cw, ay + ch))
    _arrow(d, px(0.5), gy + gr, px(0.5), gty - 6)

    sel = cells[2]
    _corner_marks(d, *sel)

    ow, oh = w * 0.40, h * 0.13
    ox0 = px(0.5) - ow / 2
    oy0 = py(0.855)
    d.rectangle([ox0, oy0, ox0 + ow, oy0 + oh], outline=DARK_BLUE, width=3)
    d.line([(ox0 + ow * 0.10, oy0 + oh * 0.62), (ox0 + ow * 0.62, oy0 + oh * 0.62)],
           fill=TALENTY_BLUE, width=3)
    mx = (sel[0] + sel[2]) / 2
    d.line([(mx, sel[3]), (mx, py(0.80))], fill=DARK_BLUE, width=2)
    d.line([(mx, py(0.80)), (px(0.5), py(0.80))], fill=DARK_BLUE, width=2)
    _arrow(d, px(0.5), py(0.80), px(0.5), oy0 - 4)
    d.ellipse([mx - 4, py(0.80) - 4, mx + 4, py(0.80) + 4], fill=TALENTY_BLUE)

    dx = gx0 - 26                      # hug the grid, not the empty bounding box
    d.line([(dx, gty), (dx, oy0 + oh)], fill=TALENTY_BLUE, width=2)
    dimension_line(d, dx, gty, dx, oy0 + oh)
    return (x0, y0, x1, y1)
