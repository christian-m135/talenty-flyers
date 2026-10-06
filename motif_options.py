import os, sys
# The renderer is shared by both flyer repos and lives in the meta-campaign skill.
sys.path.insert(0, os.environ.get("FLYER_RENDERER") or os.path.join(
    os.path.expanduser("~"), ".claude", "skills", "meta-campaign", "renderer"))
from PIL import Image, ImageDraw
from flyer_common import *
from flyer_common import _node, _arrow
import os

SLUG = "ai-creative-designer"


def _dashed_rect(d, x0, y0, x1, y1, color, w=2, dash=9, gap=7):
    """A dashed rectangle - safe-area marks read as design craft, not decoration."""
    def run(ax, ay, bx, by):
        span = max(abs(bx - ax), abs(by - ay))
        if not span:
            return
        n = int(span // (dash + gap))
        for i in range(n + 1):
            t0 = (i * (dash + gap)) / span
            t1 = min(1.0, (i * (dash + gap) + dash) / span)
            if t0 > 1:
                break
            d.line([(ax + (bx - ax) * t0, ay + (by - ay) * t0),
                    (ax + (bx - ax) * t1, ay + (by - ay) * t1)], fill=color, width=w)
    run(x0, y0, x1, y0); run(x1, y0, x1, y1)
    run(x1, y1, x0, y1); run(x0, y1, x0, y0)


def _corner_marks(d, x0, y0, x1, y1, color=TALENTY_BLUE, w=3, ln=12):
    """Crop marks on a selected frame."""
    for (px, py, sx, sy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        d.line([(px, py), (px + ln * sx, py)], fill=color, width=w)
        d.line([(px, py), (px, py + ln * sy)], fill=color, width=w)


# ---------------------------------------------------------------- A
def artboard_motif(img, cx, cy, w, h, label_room=True):
    """A dimensioned design artboard - image well, headline bar, baseline rules, safe area."""
    d = ImageDraw.Draw(img)
    x0, y0 = cx - w // 2, cy - h // 2
    x1, y1 = cx + w // 2, cy + h // 2

    def px(f): return x0 + (x1 - x0) * f
    def py(f): return y0 + (y1 - y0) * f

    # the artboard itself, a tall frame centred in the box
    fw = w * 0.56
    fx0, fx1 = px(0.5) - fw / 2, px(0.5) + fw / 2
    d.rectangle([fx0, y0, fx1, y1], outline=DARK_BLUE, width=3)

    for i in range(1, 4):
        gx = fx0 + (fx1 - fx0) * i / 4
        d.line([(gx, y0), (gx, y1)], fill=FAINT, width=1)
    for i in range(1, 6):
        gy = y0 + (y1 - y0) * i / 6
        d.line([(fx0, gy), (fx1, gy)], fill=FAINT, width=1)

    _dashed_rect(d, fx0 + fw * 0.09, py(0.05), fx1 - fw * 0.09, py(0.95), TALENTY_BLUE, 2)

    iw0, iw1 = fx0 + fw * 0.16, fx1 - fw * 0.16
    d.rectangle([iw0, py(0.12), iw1, py(0.44)], outline=DARK_BLUE, width=3)
    d.line([(iw0, py(0.44)), (iw1, py(0.12))], fill=FAINT, width=2)
    d.line([(iw0, py(0.12)), (iw1, py(0.44))], fill=FAINT, width=2)

    d.line([(iw0, py(0.545)), (iw1 - fw * 0.10, py(0.545))], fill=TALENTY_BLUE, width=6)
    for i, frac in enumerate((0.63, 0.69, 0.75)):
        rw = (iw1 - iw0) * (0.92 if i < 2 else 0.55)
        d.line([(iw0, py(frac)), (iw0 + rw, py(frac))], fill=BODY_GRAY, width=2)

    d.rounded_rectangle([iw0, py(0.83), iw0 + fw * 0.34, py(0.90)], radius=int(h * 0.035),
                        outline=TALENTY_BLUE, width=2)

    d.line([(fx0 - 24, y0), (fx0 - 24, y1)], fill=TALENTY_BLUE, width=2)
    dimension_line(d, fx0 - 24, y0, fx0 - 24, y1)
    dimension_line(d, fx0, y1 + 22, fx1, y1 + 22)
    return (x0, y0, x1, y1)


# ---------------------------------------------------------------- B
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

    d.line([(x0 - 24, gty), (x0 - 24, oy0 + oh)], fill=TALENTY_BLUE, width=2)
    dimension_line(d, x0 - 24, gty, x0 - 24, oy0 + oh)
    return (x0, y0, x1, y1)


# ---------------------------------------------------------------- C
def storyboard_motif(img, cx, cy, w, h, label_room=True):
    """Three platform frames over an edit timeline - short-form video, cut for each format."""
    d = ImageDraw.Draw(img)
    x0, y0 = cx - w // 2, cy - h // 2
    x1, y1 = cx + w // 2, cy + h // 2

    def px(f): return x0 + (x1 - x0) * f
    def py(f): return y0 + (y1 - y0) * f

    for i in range(1, 4):
        d.line([(px(i / 4), y0), (px(i / 4), y1)], fill=FAINT, width=1)
    for i in range(1, 4):
        d.line([(x0, py(i / 4)), (x1, py(i / 4))], fill=FAINT, width=1)

    # True 9:16, 1:1 and 4:5 frames, laid out left to right and baseline-aligned.
    # Sizing off the box width rather than the height is what keeps them from
    # overlapping - the aspect ratios have to earn their room, not be given it.
    tall = h * 0.40
    specs = [(tall * 9 / 16, tall), (tall * 0.72, tall * 0.72), (tall * 0.80, tall)]
    specs[2] = (tall * 0.86 * 4 / 5, tall * 0.86)
    total = sum(s[0] for s in specs)
    gap = (w - total) / 4
    base_y = py(0.04) + tall
    ax = x0 + gap
    for i, (fw, fh) in enumerate(specs):
        ay0 = base_y - fh
        d.rounded_rectangle([ax, ay0, ax + fw, base_y], radius=7, outline=DARK_BLUE, width=3)
        if i == 1:
            r = fw * 0.17
            ccx, ccy = ax + fw / 2, ay0 + fh / 2
            d.polygon([(ccx - r * 0.6, ccy - r), (ccx + r * 0.85, ccy), (ccx - r * 0.6, ccy + r)],
                      outline=TALENTY_BLUE, width=3)
        else:
            for k in range(2):
                ly = ay0 + fh * (0.60 + k * 0.15)
                d.line([(ax + fw * 0.18, ly), (ax + fw * (0.82 if k == 0 else 0.56), ly)],
                       fill=FAINT, width=2)
        dimension_line(d, ax, base_y + 15, ax + fw, base_y + 15, w=2, tick=5)
        ax += fw + gap

    # the edit timeline - three cuts on the video track, one audio track under it
    ty = py(0.68)
    th = h * 0.095
    d.line([(x0, ty - h * 0.045), (x1, ty - h * 0.045)], fill=FAINT, width=1)
    for (a, b) in ((0.0, 0.33), (0.36, 0.69), (0.72, 1.0)):
        d.rectangle([px(a), ty, px(b), ty + th], outline=DARK_BLUE, width=3)
        d.ellipse([px((a + b) / 2) - 5, ty + th / 2 - 5, px((a + b) / 2) + 5, ty + th / 2 + 5],
                  fill=TALENTY_BLUE)
    ay = ty + th + h * 0.06
    ah = h * 0.055
    d.rectangle([px(0.0), ay, px(0.69), ay + ah], outline=DARK_BLUE, width=3)
    for k in range(5):
        wx = px(0.06 + k * 0.14)
        d.line([(wx, ay + ah * 0.22), (wx, ay + ah * 0.78)], fill=TALENTY_BLUE, width=2)
    # playhead, crossing both tracks
    d.line([(px(0.53), ty - h * 0.05), (px(0.53), ay + ah + h * 0.03)], fill=TALENTY_BLUE, width=3)
    return (x0, y0, x1, y1)


# ---------------------------------------------------------------- preview
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", SLUG)
os.makedirs(OUT, exist_ok=True)

W, H = 1200, 520
img = Image.new("RGBA", (W, H), (255, 255, 255, 255))
d = ImageDraw.Draw(img)
for i, (label, fn) in enumerate([("A", artboard_motif), ("B", genstack_motif), ("C", storyboard_motif)]):
    cx = int(W * (i + 0.5) / 3)
    lf = osw_b(44)
    d.text((cx - text_w(d, label, lf) // 2, 26), label, font=lf, fill=INK)
    fn(img, cx, 300, 290, 300)
img.convert("RGB").save(os.path.join(OUT, "_motif-options.png"), "PNG")
print("wrote", os.path.join(OUT, "_motif-options.png"))
