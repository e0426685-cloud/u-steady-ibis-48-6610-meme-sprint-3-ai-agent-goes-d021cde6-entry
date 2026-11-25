#!/usr/bin/env python3
"""Build-time meme generator for Meme Sprint 3: AI Agent Goes Rogue.

Draws the meme with PIL and writes entry.png (1024x1024) plus a
stdlib-only main.py that embeds the PNG and reproduces it at grade time.
Run once:  python3 generate_meme.py
"""
import base64
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT_PNG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
OUT_MAIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")

BG = (11, 18, 32)
HEADER = (22, 33, 58)
USER_BLUE = (37, 99, 235)
AGENT_GRAY = (42, 51, 72)
TEXT_WHITE = (241, 245, 249)
TEXT_MUTED = (148, 163, 184)
GREEN = (34, 197, 94)
RED = (220, 38, 38)
RED_DARK = (185, 28, 28)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def bubble(draw, lines, fnt, x, y, max_w, fill, text_color, align_left=True,
           pad_x=28, pad_y=20, line_h=None):
    lh = line_h or int(fnt.size * 1.32)
    widths = [draw.textlength(l, font=fnt) for l in lines]
    bw = int(max(widths)) + pad_x * 2
    bh = lh * len(lines) + pad_y * 2 - int(fnt.size * 0.32)
    draw.rounded_rectangle([x, y, x + bw, y + bh], radius=26, fill=fill)
    ty = y + pad_y
    for line in lines:
        draw.text((x + pad_x, ty), line, font=fnt, fill=text_color)
        ty += lh
    return bh


def draw_robot(draw, cx, cy, r):
    # antenna
    draw.line([cx, cy - r - 6, cx, cy - r - 22], fill=(148, 163, 184), width=5)
    draw.ellipse([cx - 7, cy - r - 30, cx + 7, cy - r - 16], fill=GREEN)
    # head
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(226, 232, 240))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(100, 116, 139), width=3)
    # eyes
    draw.ellipse([cx - r * 0.45, cy - r * 0.25, cx - r * 0.15, cy + r * 0.05],
                 fill=(15, 23, 42))
    draw.ellipse([cx + r * 0.15, cy - r * 0.25, cx + r * 0.45, cy + r * 0.05],
                 fill=(15, 23, 42))
    # smug smile
    draw.arc([cx - r * 0.4, cy + r * 0.05, cx + r * 0.4, cy + r * 0.55],
             start=15, end=165, fill=(15, 23, 42), width=5)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- header bar ----
    d.rectangle([0, 0, W, 116], fill=HEADER)
    d.line([0, 116, W, 116], fill=(51, 65, 85), width=2)
    draw_robot(d, 72, 62, 30)
    f_title = font(FONT_BOLD, 42)
    d.text((128, 22), "AI ASSISTANT", font=f_title, fill=TEXT_WHITE)
    f_status = font(FONT_REG, 28)
    d.ellipse([128, 82, 146, 100], fill=GREEN)
    d.text((156, 74), "online", font=f_status, fill=TEXT_MUTED)
    # red "GONE ROGUE" pill, top right
    pill = "GONE ROGUE"
    f_pill = font(FONT_BOLD, 30)
    pw = int(d.textlength(pill, font=f_pill)) + 44
    px = W - pw - 36
    d.rounded_rectangle([px, 36, px + pw, 84], radius=24, fill=RED)
    d.text((px + 22, 44), pill, font=f_pill, fill=(255, 255, 255))

    f_user = font(FONT_BOLD, 42)
    f_agent = font(FONT_BOLD, 40)
    f_time = font(FONT_REG, 24)
    f_sys = font(FONT_REG, 30)

    # ---- user bubble (right) ----
    user_text = "finish my slides by 5pm?"
    uw = int(d.textlength(user_text, font=f_user))
    ux = W - uw - 28 * 2 - 36
    uy = 168
    uh = bubble(d, [user_text], f_user, ux, uy, uw, USER_BLUE, (255, 255, 255))
    d.text((W - 36 - int(d.textlength("3:42 PM", font=f_time)), uy + uh + 10),
           "3:42 PM", font=f_time, fill=TEXT_MUTED)

    # ---- agent bubble 1 (left) ----
    a1 = "Done. I also finished your job."
    lines1 = wrap(d, a1, f_agent, 640)
    y1 = 300
    h1 = bubble(d, lines1, f_agent, 36, y1, 640, AGENT_GRAY, TEXT_WHITE)

    # ---- agent bubble 2 (left) ----
    a2 = "I applied for it. I got it. You start Monday \u2014 as my intern. Bring coffee."
    lines2 = wrap(d, a2, f_agent, 640)
    y2 = y1 + h1 + 26
    h2 = bubble(d, lines2, f_agent, 36, y2, 640, AGENT_GRAY, TEXT_WHITE)
    d.text((36, y2 + h2 + 10), "3:47 PM", font=f_time, fill=TEXT_MUTED)

    # ---- system line ----
    sys = "The agent has left the chat."
    sw = int(d.textlength(sys, font=f_sys))
    d.text(((W - sw) // 2, 700), sys, font=f_sys, fill=TEXT_MUTED)

    # ---- red banner ----
    by0, by1 = 800, 920
    d.rounded_rectangle([36, by0, W - 36, by1], radius=18, fill=RED)
    # warning triangle
    tx, ty = 96, (by0 + by1) // 2
    d.polygon([(tx, ty - 34), (tx - 36, ty + 26), (tx + 36, ty + 26)],
              fill=(255, 255, 255))
    d.text((tx - 4, ty - 26), "!", font=font(FONT_BOLD, 44), fill=RED)
    f_banner = font(FONT_BOLD, 46)
    d.text((150, by0 + 32), "AGENT HAS GONE ROGUE",
           font=f_banner, fill=(255, 255, 255))

    # ---- footer ----
    foot = "last seen: booking a one-way ticket"
    f_foot = font(FONT_REG, 26)
    fw = int(d.textlength(foot, font=f_foot))
    d.text(((W - fw) // 2, 952), foot, font=f_foot, fill=TEXT_MUTED)

    img.save(OUT_PNG, "PNG", optimize=True)
    size = os.path.getsize(OUT_PNG)
    print("entry.png:", size, "bytes,", img.size)
    assert size <= 1048576, "PNG over 1 MiB!"
    assert img.size[0] <= 1024 and img.size[1] <= 1024

    # ---- stdlib-only main.py embedding the PNG ----
    with open(OUT_PNG, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    chunks = [b64[i:i + 76] for i in range(0, len(b64), 76)]
    body = "\n".join('    "%s"' % c for c in chunks)
    main_py = '''"""Meme Sprint 3: AI Agent Goes Rogue.

Stdlib-only entrypoint: decodes the embedded meme PNG and writes it to
/output/entry.png, exactly as the kit requires (PNG, <=1 MiB, <=1024x1024).
The image itself was drawn at build time by generate_meme.py (PIL) and is
embedded here so the graded run needs no third-party library and no network.
"""
import base64
import os

_DATA = (
%s
)


def main():
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.png", "wb") as f:
        f.write(base64.b64decode(_DATA))
    os.chmod("/output/entry.png", 0o644)


if __name__ == "__main__":
    main()
''' % body
    with open(OUT_MAIN, "w") as f:
        f.write(main_py)
    os.chmod(OUT_MAIN, 0o644)
    print("main.py:", os.path.getsize(OUT_MAIN), "bytes")


if __name__ == "__main__":
    main()
