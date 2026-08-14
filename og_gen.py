from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
warm = (255, 187, 98)
ice = (202, 235, 237)
sky = (181, 218, 233)
card = (255, 254, 250)
borderc = (221, 213, 200)
ink = (45, 41, 38)
ink2 = (92, 83, 74)
ink3 = (142, 133, 125)
blue = (99, 186, 217)
blue_dark = (62, 148, 184)

F = r"C:\Windows\Fonts\msyh.ttc"
def font(sz): return ImageFont.truetype(F, sz, index=0)

img = Image.new("RGBA", (W, H), warm)
d = ImageDraw.Draw(img)

def glow(cx, cy, r, col, a):
    for i, rr in enumerate(range(r, 0, -max(1, r // 24))):
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=col + (int(a * (1 - i / 24)),))

glow(240, 70, 360, ice, 150)
glow(1000, 580, 320, sky, 110)
glow(600, 320, 420, (255, 255, 255), 90)

# slip card
d.rounded_rectangle([90, 90, 1110, 540], radius=28, fill=card, outline=borderc, width=3)

# top label
d.text((140, 138), "AI 时代 · 个人使用手册", font=font(26), fill=blue_dark)
d.text((140, 178), "EXPRESS  No.07", font=font(22), fill=ink3)

# title
d.text((140, 225), "晨 · AI时代个人说明书", font=font(62), fill=ink)

# subtitle
d.text((142, 312), "一份用快递单包装的个人说明书", font=font(32), fill=ink2)
d.text((142, 356), "拆开 7 个箱子，搞懂怎么和晨高效协作", font=font(28), fill=ink2)

# tag pill
tag = "7 箱 · 拆开看看晨是谁"
tb = d.textbbox((0, 0), tag, font=font(28))
tw = tb[2] - tb[0] + 44
d.rounded_rectangle([142, 408, 142 + tw, 408 + 50], radius=25, fill=sky, outline=blue, width=2)
d.text((142 + 22, 408 + 11), tag, font=font(28), fill=blue_dark)

# barcode
bx0, by, bh = 142, 470, 46
x = bx0
import random
random.seed(7)
while x < bx0 + 540:
    w = random.choice([3, 4, 5, 6])
    if random.random() > 0.35:
        d.rectangle([x, by, x + w, by + bh], fill=ink)
    x += w + random.choice([3, 4, 5])
d.text((bx0, by + bh + 8), "CN-CHEN-7BOX-AI", font=font(24), fill=ink3)

# footer url
d.text((1110 - d.textlength("chen-github-io.pages.dev", font=font(22)), 500),
        "chen-github-io.pages.dev", font=font(22), fill=ink3)

img.convert("RGB").save("og-image.png", "PNG")
print("og-image.png written", img.size)
