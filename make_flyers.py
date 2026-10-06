import os, sys
# The renderer is shared by both flyer repos and lives in the meta-campaign skill.
sys.path.insert(0, os.environ.get("FLYER_RENDERER") or os.path.join(
    os.path.expanduser("~"), ".claude", "skills", "meta-campaign", "renderer"))
from PIL import Image, ImageDraw
import flyer_common as fc
fc.use_brand("talenty")         # before the star import, which copies the colours as they stand
from flyer_common import *

# Output dir, resolved relative to this file so the script works from any cwd.
SLUG = "data-scientist"
NAME = "DataScientist"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", SLUG)

# Copy language: English. No client name, no salary.
TITLE = "Data Scientist"
KICKER = "WE'RE HIRING"
SUBHEAD = "Analytics + AI  ·  100% Remote  ·  Full-Time"
DESC = "Interrogate real data with sound statistical reasoning and use AI as a force-multiplier for a Tokyo-based consultancy."
DESC_SHORT = "Statistical reasoning + AI, end-to-end, for a Tokyo-based consultancy."
BULLETS = [
    "Reason clearly about uncertainty and cause",
    "Python + SQL on real client data",
    "AI as a force-multiplier, verified",
    "3h+ daily overlap with Tokyo (JST)",
]
BULLETS_SHORT = [
    "Statistical reasoning on real data",
    "Python + SQL, AI-accelerated",
    "3h+ daily Tokyo (JST) overlap",
]
CHIPS = ["Statistics", "Python", "SQL", "C1 English", "JST +3h"]
CHIPS_SHORT = ["Statistics", "Python", "SQL", "JST +3h"]
CAPTION = "Think in data. Build with AI."

PANEL_W = 0.60


def fits(y, img, foot, what):
    """The footer overflow is silent in PIL, so make it loud."""
    limit = img.size[1] - foot - 14
    if y > limit:
        raise RuntimeError("%s ends at y=%d, under the footer band (limit %d) on %dx%d"
                           % (what, y, limit, img.size[0], img.size[1]))


def max_rows(rows, n, what):
    if rows > n:
        raise RuntimeError("chips wrapped to %d rows on %s - cut a chip" % (rows, what))


def save(img, suffix):
    save_flyer(img, os.path.join(OUT, "%s_Talenty_%s.png" % (NAME, suffix)))


def render_1x1():
    W = H = 1080; img = new_canvas(W, H); M = int(W * 0.065); FOOT_H = 92
    light_panel(img, [0, 0, int(W * PANEL_W), H]); d = ImageDraw.Draw(img)
    lw, lh = paste_logo(img, M, M, 74, role="logo"); d = ImageDraw.Draw(img)
    y = M + lh + 40; y = kicker_line(img, d, M, y, 30, KICKER) + 34
    tf = osw_b(104)
    text(img, d, (M, y), TITLE, tf, INK, large=True, role="title"); th, off = bbox_h(d, TITLE, tf); y += th + off + 16
    sf = osw_m(34)
    text(img, d, (M, y), SUBHEAD, sf, TEXT_ACCENT, role="subhead"); sh, so = bbox_h(d, SUBHEAD, sf); y += sh + 30
    dimension_line(d, M, y, int(W * 0.55), y); y += 28
    df = inter(29)
    for ln in wrap(d, DESC_SHORT, df, int(W * 0.52)):
        text(img, d, (M, y), ln, df, BODY, role="body"); lh2, o2 = bbox_h(d, ln, df); y += lh2 + 11
    y += 20
    bf = inter_m(30)
    for b in BULLETS_SHORT:
        d.rectangle([M, y + 8, M + 16, y + 24], fill=ACCENT)
        for ln in wrap(d, b, bf, int(W * 0.46)):
            text(img, d, (M + 32, y), ln, bf, INK, role="bullet"); bh, bo = bbox_h(d, ln, bf); y += bh + 9
        y += 8
    y += 16
    y, rows = chip_row(img, d, M, y, CHIPS, inter_sb(26), int(W * 0.54)); max_rows(rows, 2, "1x1")
    y += 34
    cf = osw_sb(38); text(img, d, (M, y), CAPTION, cf, INK, role="caption"); ch, co = bbox_h(d, CAPTION, cf)
    fits(y + ch + co, img, FOOT_H, "caption")
    ds_motif(img, int(W * 0.835), int(H * 0.44), int(W * 0.27), int(H * 0.32))
    footer_band(img, FOOT_H); save(img, "1x1_1080x1080")


def render_9x16():
    """Stories and Reels. Everything a reader must see - logo, kicker, title, subhead,
    bullets, chips - sits in the safe zone y=270..1250; the renderer fails the render
    otherwise. The description is left to the ad's primary text. Motif, caption and
    footer sit in the lower zone that the Reels interface covers, so nothing there is
    essential."""
    W, H = 1080, 1920; img = new_canvas(W, H); M = int(W * 0.075); FOOT_H = 118
    top, bottom = safe_zone(img)
    light_panel(img, [0, top - 34, W, bottom + 16]); d = ImageDraw.Draw(img)
    y = top + 14
    lw, lh = paste_logo(img, M, y, 92, role="logo"); d = ImageDraw.Draw(img)
    y += lh + 40; y = kicker_line(img, d, M, y, 34, KICKER) + 34
    tf = osw_b(fit_size(d, TITLE, osw_b, W - 2 * M, 150))
    text(img, d, (M, y), TITLE, tf, INK, large=True, role="title"); th, off = bbox_h(d, TITLE, tf); y += th + off + 24
    sf = osw_m(fit_size(d, SUBHEAD, osw_m, W - 2 * M, 46))
    text(img, d, (M, y), SUBHEAD, sf, TEXT_ACCENT, role="subhead"); sh, so = bbox_h(d, SUBHEAD, sf); y += sh + so + 30
    dimension_line(d, M, y, W - M, y); y += 36
    # One size for all four bullets: the largest at which the longest one still fits.
    longest = max(BULLETS, key=lambda b: text_w(d, b, inter_m(46)))
    bf = inter_m(fit_size(d, longest, inter_m, W - 2 * M - 42, 46, floor=34))
    for b in BULLETS:
        d.rectangle([M, y + 14, M + 22, y + 36], fill=ACCENT)
        text(img, d, (M + 42, y), b, bf, INK, role="bullet"); y += 72
    y += 14
    y, rows = chip_row(img, d, M, y, CHIPS, inter_sb(34), W - 2 * M, gap=14, padx=22, pady=12); max_rows(rows, 2, "9x16")
    # Below the safe zone: decorative only.
    ds_motif(img, W // 2 + 13, 1452, int(W * 0.56), 250)
    cf = osw_sb(54); ch, co = bbox_h(d, CAPTION, cf); cy = 1672
    text(img, d, (M, cy), CAPTION, cf, INK, role="caption")
    fits(cy + ch + co, img, FOOT_H, "caption")
    footer_band(img, FOOT_H); save(img, "9x16_1080x1920")


def render_191x1():
    """Right column and search results. Facebook search results cuts this format to its
    central square, so logo, kicker, title, subhead, bullets, chips and the footer URL
    all sit inside x=286..914; the renderer fails the render otherwise. The motif and
    the dimension line outside the square are decoration."""
    W, H = 1200, 628; img = new_canvas(W, H); FOOT_H = 70
    x0, _, x1, _ = safe_box(img)
    M = x0 + 26; CW = x1 - 26 - M                    # the text column inside the square
    light_panel(img, [x0 - 8, 0, x1 + 8, H]); d = ImageDraw.Draw(img)
    y = 36
    lw, lh = paste_logo(img, M, y, 58, role="logo"); d = ImageDraw.Draw(img)
    y += lh + 18; y = kicker_line(img, d, M, y, 23, KICKER) + 12
    tf = osw_b(fit_size(d, TITLE, osw_b, CW, 84))
    text(img, d, (M, y), TITLE, tf, INK, large=True, role="title"); th, off = bbox_h(d, TITLE, tf); y += th + off + 12
    sf = osw_m(fit_size(d, SUBHEAD, osw_m, CW, 27, floor=20))
    text(img, d, (M, y), SUBHEAD, sf, TEXT_ACCENT, role="subhead"); sh, so = bbox_h(d, SUBHEAD, sf); y += sh + so + 16
    bf = inter_m(25)
    for b in BULLETS_SHORT:
        d.rectangle([M, y + 8, M + 14, y + 22], fill=ACCENT)
        text(img, d, (M + 28, y), b, bf, INK, role="bullet"); y += 36
    y += 6
    y, rows = chip_row(img, d, M, y, CHIPS_SHORT, inter_sb(22), CW); max_rows(rows, 1, "1.91x1")
    fits(y, img, FOOT_H, "chips")
    # Outside the square: decoration only.
    ds_motif(img, (x1 + W) // 2 + 16, int(H * 0.43), 200, int(H * 0.46))
    dimension_line(d, x0 // 2, 60, x0 // 2, H - FOOT_H - 60)
    footer_band(img, FOOT_H, x=M, dot_x=x1 - 26); save(img, "1.91x1_1200x628")


def render_4x5():
    W, H = 1080, 1350; img = new_canvas(W, H); M = int(W * 0.065); FOOT_H = 96
    light_panel(img, [0, 0, int(W * PANEL_W), H]); d = ImageDraw.Draw(img)
    lw, lh = paste_logo(img, M, M, 74, role="logo"); d = ImageDraw.Draw(img)
    y = M + lh + 34; y = kicker_line(img, d, M, y, 30, KICKER) + 30
    tf = osw_b(104)
    text(img, d, (M, y), TITLE, tf, INK, large=True, role="title"); th, off = bbox_h(d, TITLE, tf); y += th + off + 18
    sf = osw_m(35)
    text(img, d, (M, y), SUBHEAD, sf, TEXT_ACCENT, role="subhead"); sh, so = bbox_h(d, SUBHEAD, sf); y += sh + 34
    dimension_line(d, M, y, int(W * 0.55), y); y += 30
    df = inter(30)
    for ln in wrap(d, DESC, df, int(W * 0.52)):
        text(img, d, (M, y), ln, df, BODY, role="body"); lh2, o2 = bbox_h(d, ln, df); y += lh2 + 12
    y += 20
    bf = inter_m(31)
    for b in BULLETS:
        d.rectangle([M, y + 8, M + 16, y + 25], fill=ACCENT)
        for ln in wrap(d, b, bf, int(W * 0.46)):
            text(img, d, (M + 32, y), ln, bf, INK, role="bullet"); bh, bo = bbox_h(d, ln, bf); y += bh + 10
        y += 8
    y += 14
    y, rows = chip_row(img, d, M, y, CHIPS, inter_sb(27), int(W * 0.54)); max_rows(rows, 2, "4x5")
    y += 34
    cf = osw_sb(40); text(img, d, (M, y), CAPTION, cf, INK, role="caption"); ch, co = bbox_h(d, CAPTION, cf)
    fits(y + ch + co, img, FOOT_H, "caption")
    ds_motif(img, int(W * 0.835), int(H * 0.42), int(W * 0.27), int(H * 0.28))
    footer_band(img, FOOT_H); save(img, "4x5_1080x1350")


os.makedirs(OUT, exist_ok=True)
render_1x1(); render_9x16(); render_191x1(); render_4x5()
print("rendered:", sorted(f for f in os.listdir(OUT) if not f.startswith("_")))
print("contrast:", contrast_report())
