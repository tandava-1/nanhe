#!/usr/bin/env python3
"""Render Nanhe packaging from docs/product/products.json.

Writes:
  assets/packaging/<slug>.svg      one lit pack render per product
  assets/packaging/lineup.svg      the full line-up
  docs/product/product-line.md     human-readable product sheet
  brand-book/index.html            replaces the block between
                                   <!-- BEGIN:packaging --> and <!-- END:packaging -->

Run from anywhere:  python3 scripts/build_packaging.py
No dependencies beyond the standard library.
"""
import html
import json
import math
import pathlib
import random

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "docs/product/products.json").read_text())
CATS = DATA["categories"]
PRODUCTS = DATA["products"]
BY_SLUG = {p["slug"]: p for p in PRODUCTS}

MILK = "#FBF7F0"
PACK = "#F8F3EA"   # pack plastic, a hair darker than the page so it reads
MOSS = "#1F3A2B"
LEAF = "#5E8E4E"
MARIGOLD = "#EFA43A"

DISPLAY = "Fraunces, Georgia, serif"
BODY = "Figtree, 'Avenir Next', 'Segoe UI', sans-serif"
DEVA = "'Baloo 2', 'Kohinoor Devanagari', 'Noto Sans Devanagari', sans-serif"
SOFT = "font-variation-settings:'SOFT' 100"
FONT_IMPORT = ("@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@600"
               "&family=Figtree:wght@500;700&family=Fraunces:opsz,wght,SOFT@9..144,500,100&display=swap');")

_uid = 0


def uid():
    global _uid
    _uid += 1
    return f"u{_uid}"


def esc(s):
    return html.escape(s, quote=True)


def f(n):
    """Compact number formatting for path data."""
    return f"{n:.2f}".rstrip("0").rstrip(".")


# ---------------------------------------------------------------- symbols

WORDMARK = """
  <g fill="none" stroke="currentColor" stroke-width="14" stroke-linecap="round" stroke-linejoin="round">
    <path d="M7 40V100M7 68a28 28 0 0 1 56 0V100"/><circle cx="121" cy="70" r="30"/><path d="M151 40V100"/>
    <path d="M181 40V100M181 68a28 28 0 0 1 56 0V100"/><path d="M267 14V100M267 68a28 28 0 0 1 56 0V100"/>
    <path d="M351 70H411A30 30 0 1 0 402.2 91.2"/>
  </g>
  <path d="M267 12Q295 16 297 -14Q269 -16 267 12Z" fill="#5E8E4E"/>"""

MARK = """
  <g fill="none" stroke="currentColor" stroke-width="13" stroke-linecap="round" stroke-linejoin="round">
    <path d="M30 41V83M30 61a20 20 0 0 1 40 0V83"/>
  </g>
  <path d="M50 36Q74 34 70 10Q46 12 50 36Z" fill="#5E8E4E"/>"""


def leaf(bx, by, tx, ty, k=0.35):
    mx, my = (bx + tx) / 2, (by + ty) / 2
    vx, vy = tx - bx, ty - by
    px, py = -vy * k, vx * k
    return (f"M{f(bx)} {f(by)}Q{f(mx + px)} {f(my + py)} {f(tx)} {f(ty)}"
            f"Q{f(mx - px)} {f(my - py)} {f(bx)} {f(by)}Z")


def hexagon(cx, cy, r):
    pts = [(cx + r * math.cos(math.radians(30 + 60 * i)), cy + r * math.sin(math.radians(30 + 60 * i)))
           for i in range(6)]
    return "M" + "L".join(f"{f(x)} {f(y)}" for x, y in pts) + "Z"


def icon_body(name):
    """Fine-line ingredient illustrations on a 48 grid, drawn in currentColor."""
    if name == "oat":
        d = ["M24 46C24 34 23 20 25 4"]
        for y in (9, 16, 23, 30):
            d.append(leaf(24, y + 6, 15.5, y - 1, 0.36))
            d.append(leaf(24.6, y + 9, 33, y + 2, 0.36))
        d.append(leaf(25, 9, 25.5, 1, 0.4))
        return f'<path d="{"".join(d)}"/>'
    if name == "calendula":
        petals = "".join(
            f'<ellipse cx="24" cy="12.5" rx="3.1" ry="7" transform="rotate({i * 360 / 14:.1f} 24 24)"/>'
            for i in range(14))
        return petals + '<circle cx="24" cy="24" r="5.2"/><circle cx="24" cy="24" r="2" fill="currentColor"/>'
    if name == "coconut":
        # a whole coconut behind, a cracked half in front
        return ('<circle cx="18" cy="23" r="11"/>'
                '<circle cx="15.5" cy="16" r="1" fill="currentColor"/><circle cx="19.5" cy="15" r="1" fill="currentColor"/>'
                '<circle cx="17.5" cy="18.5" r="1" fill="currentColor"/>'
                '<path d="M20 31H44A12 12 0 0 1 20 31Z"/><path d="M23.5 31A8.5 8.5 0 0 0 40.5 31"/>'
                f'<path d="{leaf(18, 12, 28, 3, 0.3)}"/>')
    if name == "shea":
        return ('<path d="M24 5C37 13 39 32 24 43C9 32 11 13 24 5Z"/>'
                '<path d="M24 11C21.5 21 21.5 30 24 38"/><path d="M29 15c2 5 2 11 0 17" opacity=".6"/>')
    if name == "honeycomb":
        r = 8
        w = r * math.sqrt(3)
        return ('<path d="' + hexagon(24 - w / 2, 19, r) + hexagon(24 + w / 2, 19, r)
                + hexagon(24, 19 + 1.5 * r, r) + '"/><path d="M24 31.5v5" opacity=".6"/>'
                '<circle cx="24" cy="40" r="2.4" fill="currentColor"/>')
    if name == "sun":
        rays = "".join(
            f'<path d="M{f(24 + 13 * math.cos(a))} {f(24 + 13 * math.sin(a))}L{f(24 + 19 * math.cos(a))} {f(24 + 19 * math.sin(a))}"/>'
            for a in (math.radians(i * 30) for i in range(12)))
        return '<circle cx="24" cy="24" r="8.5"/>' + rays
    if name == "neem":
        ax, ay, bx, by = 9, 43, 39, 7
        L = math.hypot(bx - ax, by - ay)
        dx, dy = (bx - ax) / L, (by - ay) / L
        nx, ny = -dy, dx
        d = [f"M{ax} {ay}L{bx} {by}"]
        for t in (0.2, 0.36, 0.52, 0.68, 0.84):
            px, py = ax + (bx - ax) * t, ay + (by - ay) * t
            d.append(leaf(px, py, px + nx * 9 + dx * 4, py + ny * 9 + dy * 4, 0.32))
            d.append(leaf(px, py, px - nx * 9 + dx * 4, py - ny * 9 + dy * 4, 0.32))
        d.append(leaf(bx, by, bx + dx * 7, by + dy * 7, 0.34))
        return f'<path d="{"".join(d)}"/>'
    if name == "drop":
        return ('<path d="M24 5C31 15 36 22 36 30A12 12 0 0 1 12 30C12 22 17 15 24 5Z"/>'
                '<path d="M18 30a6 6 0 0 0 5 6" opacity=".7"/>')
    if name == "soapnut":
        return ('<path d="M24 4V12M24 12L18 20M24 12L30 20M24 12V17"/>'
                '<circle cx="17" cy="28" r="8"/><circle cx="31" cy="28" r="8"/><circle cx="24" cy="23" r="7"/>'
                '<path d="M14 26a4 4 0 0 1 3-3M28 26a4 4 0 0 1 3-3" opacity=".6"/>')
    raise ValueError(name)


ICONS = ["oat", "calendula", "coconut", "shea", "honeycomb", "sun", "neem", "drop", "soapnut"]


def defs(p):
    """Gradients and symbols. `p` prefixes every id so the page can hold several sets."""
    icons = "".join(
        f'<symbol id="{p}ic-{n}" viewBox="0 0 48 48"><g fill="none" stroke="currentColor" stroke-width="1.5" '
        f'stroke-linecap="round" stroke-linejoin="round">{icon_body(n)}</g></symbol>' for n in ICONS)
    return f"""
<linearGradient id="{p}shade" x1="0" x2="1" y1="0" y2="0">
  <stop offset="0" stop-color="#000" stop-opacity=".2"/><stop offset=".1" stop-color="#000" stop-opacity=".06"/>
  <stop offset=".27" stop-color="#fff" stop-opacity=".42"/><stop offset=".42" stop-color="#fff" stop-opacity=".05"/>
  <stop offset=".7" stop-color="#000" stop-opacity="0"/><stop offset=".9" stop-color="#000" stop-opacity=".1"/>
  <stop offset="1" stop-color="#000" stop-opacity=".24"/>
</linearGradient>
<linearGradient id="{p}top" x1="0" x2="0" y1="0" y2="1">
  <stop offset="0" stop-color="#fff" stop-opacity=".35"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/>
  <stop offset="1" stop-color="#000" stop-opacity=".08"/>
</linearGradient>
<linearGradient id="{p}spec" x1="0" x2="0" y1="0" y2="1">
  <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".12" stop-color="#fff" stop-opacity=".95"/>
  <stop offset=".8" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
</linearGradient>
<linearGradient id="{p}oil" x1="0" x2="0" y1="0" y2="1">
  <stop offset="0" stop-color="#F3CB72"/><stop offset="1" stop-color="#D9952C"/>
</linearGradient>
<radialGradient id="{p}ground"><stop offset="0" stop-color="{MOSS}" stop-opacity=".32"/>
  <stop offset=".55" stop-color="{MOSS}" stop-opacity=".1"/><stop offset="1" stop-color="{MOSS}" stop-opacity="0"/></radialGradient>
<symbol id="{p}wm" viewBox="-6 -20 426 134">{WORDMARK}</symbol>
<symbol id="{p}mk" viewBox="0 0 100 100">{MARK}</symbol>
{icons}"""


# ---------------------------------------------------------------- label art

def text(x, y, s, size, family=BODY, weight=None, fill=MOSS, ls=None, anchor=None, style=None):
    a = [f'x="{f(x)}"', f'y="{f(y)}"', f'font-family="{family}"', f'font-size="{f(size)}"', f'fill="{fill}"']
    if weight:
        a.append(f'font-weight="{weight}"')
    if ls:
        a.append(f'letter-spacing="{ls}"')
    if anchor:
        a.append(f'text-anchor="{anchor}"')
    if style:
        a.append(f'style="{style}"')
    return f"<text {' '.join(a)}>{esc(s)}</text>"


def seal(p, cx, cy, r):
    return (f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{MARIGOLD}"/>'
            f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r * .68)}" fill="{MILK}"/>'
            f'<use href="#{p}mk" x="{f(cx - r * .6)}" y="{f(cy - r * .6)}" width="{f(r * 1.2)}" height="{f(r * 1.2)}" '
            f'style="color:{MOSS}"/>')


def footer_left(pr):
    return pr.get("footer") or f"{pr['natural']}% naturally derived**"


def label_tall(pr, p):
    """Front label on a 100 x 150 box."""
    deep = CATS[pr["category"]]["deep"]
    o = [f'<use href="#{p}wm" x="3" y="3" width="46" height="14.5" style="color:{MOSS}"/>', seal(p, 88, 12, 9),
         text(4, 34, pr["eyebrow"].upper(), 4.2, weight=700, fill=deep, ls=".5")]
    y = 50
    for line in pr["name"]:
        o.append(text(4, y, line, 13, DISPLAY, 500, style=SOFT))
        y += 13.5
    o.append(text(4, y - 1.5, pr["hindi"], 7.4, DEVA, 600, fill="#55695C"))
    o.append(f'<use href="#{p}ic-{pr["icon"]}" x="30" y="83" width="40" height="40" style="color:{deep}"/>')
    o.append(f'<path d="M4 132.5H96" stroke="{MOSS}" stroke-opacity=".18" stroke-width=".5"/>')
    o.append(text(4, 142, footer_left(pr).upper(), 3.4, weight=700, ls=".3"))
    o.append(text(96, 143, pr["size"], 8, DISPLAY, 500, anchor="end", style=SOFT))
    return "".join(o)


def label_wide(pr, p):
    """Front label on a 160 x 90 box."""
    deep = CATS[pr["category"]]["deep"]
    name = " ".join(pr["name"])
    return "".join([
        f'<use href="#{p}wm" x="5" y="5" width="48" height="15.1" style="color:{MOSS}"/>', seal(p, 149, 14, 9.5),
        text(6, 36, pr["eyebrow"].upper(), 4.3, weight=700, fill=deep, ls=".5"),
        text(6, 53, name, 15, DISPLAY, 500, style=SOFT),
        text(6, 65, pr["hindi"], 8, DEVA, 600, fill="#55695C"),
        f'<use href="#{p}ic-{pr["icon"]}" x="114" y="27" width="38" height="38" style="color:{deep}"/>',
        f'<path d="M6 73.5H154" stroke="{MOSS}" stroke-opacity=".18" stroke-width=".5"/>',
        text(6, 83, footer_left(pr).upper(), 4.3, weight=700, ls=".4"),
        text(154, 84, pr["size"], 9.5, DISPLAY, 500, anchor="end", style=SOFT),
    ])


def place(content, x, y, s):
    return f'<g transform="translate({f(x)} {f(y)}) scale({f(s)})">{content}</g>'


# ---------------------------------------------------------------- packs
# Every pack is drawn with its base on y=0, centred on x=0, growing upwards.

def ground(p, l, r):
    return f'<ellipse cx="{f((l + r) / 2)}" cy="2" rx="{f((r - l) * .56)}" ry="10" fill="url(#{p}ground)"/>'


def lit(d, p, fill, stroke=True):
    s = ' stroke="#1F3A2B" stroke-opacity=".1" stroke-width=".8"' if stroke else ""
    return f'<path d="{d}" fill="{fill}"{s}/><path d="{d}" fill="url(#{p}shade)"/>'


def rect_d(x, y, w, h, r):
    return (f"M{f(x + r)} {f(y)}H{f(x + w - r)}A{f(r)} {f(r)} 0 0 1 {f(x + w)} {f(y + r)}V{f(y + h - r)}"
            f"A{f(r)} {f(r)} 0 0 1 {f(x + w - r)} {f(y + h)}H{f(x + r)}A{f(r)} {f(r)} 0 0 1 {f(x)} {f(y + h - r)}"
            f"V{f(y + r)}A{f(r)} {f(r)} 0 0 1 {f(x + r)} {f(y)}Z")


def spec(p, x, y, w, h, op=.6):
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(w / 2)}" fill="url(#{p}spec)" opacity="{op}"/>'


def pack_pump(pr, p, foam=False):
    cap = CATS[pr["category"]]["base"]
    w, H = (130, 234) if foam else (120, 222)
    W = w / 2
    body = (f"M{-W} -18Q{-W} 0 {-W + 18} 0H{W - 18}Q{W} 0 {W} -18V{-(H - 44)}"
            f"C{W} {-(H - 10)} 30 {-H} 22 {-H}H-22C-30 {-H} {-W} {-(H - 10)} {-W} {-(H - 44)}Z")
    s = (w - 24) / 100
    o = [ground(p, -W, W), lit(body, p, PACK), place(label_tall(pr, p), -(w - 24) / 2, -(H - 34), s),
         spec(p, -W + 5, -(H - 40), 5, H - 70)]
    collar = rect_d(-26, -H - 24, 52, 27, 5)
    if foam:
        o += [lit(rect_d(-6, -H - 40, 12, 18, 2), p, "#ECE5D8", False),
              lit(rect_d(24, -H - 68, 32, 12, 6), p, cap),
              lit(rect_d(-32, -H - 76, 64, 38, 15), p, cap),
              f'<path d="{rect_d(-32, -H - 76, 64, 38, 15)}" fill="url(#{p}top)"/>']
        top, right = -H - 76, 56
    else:
        o += [lit(rect_d(-5, -H - 44, 10, 22, 2), p, "#ECE5D8", False),
              lit(rect_d(18, -H - 64, 46, 11, 5.5), p, cap),
              lit(rect_d(-28, -H - 68, 56, 24, 9), p, cap),
              f'<path d="{rect_d(-28, -H - 68, 56, 24, 9)}" fill="url(#{p}top)"/>']
        top, right = -H - 68, 64
    o.append(lit(collar, p, cap))
    o.append(f'<path d="M-26 {-H - 14}H26" stroke="#000" stroke-opacity=".08"/>')
    return {"svg": "".join(o), "l": -W, "r": max(W, right), "top": top}


def pack_oil(pr, p):
    cap = CATS[pr["category"]]["base"]
    W, H = 46, 176
    body = (f"M{-W} -16Q{-W} 0 -30 0H30Q{W} 0 {W} -16V{-(H - 40)}C{W} {-(H - 12)} 22 {-H} 15 {-H}"
            f"V{-(H + 12)}H-15V{-H}C-22 {-H} {-W} {-(H - 12)} {-W} {-(H - 40)}Z")
    cid = f"{p}clip-{uid()}"
    o = [ground(p, -W, W),
         f'<clipPath id="{cid}"><path d="{body}"/></clipPath>',
         f'<path d="{body}" fill="#FFFFFF" fill-opacity=".55" stroke="{MOSS}" stroke-opacity=".2" stroke-width=".8"/>',
         f'<g clip-path="url(#{cid})"><rect x="{-W}" y="-152" width="{2 * W}" height="152" fill="url(#{p}oil)" opacity=".92"/>'
         f'<path d="M{-W} -152H{W}" stroke="#fff" stroke-opacity=".7" stroke-width="1.2"/>'
         f'<rect x="{-W}" y="-138" width="{2 * W}" height="120" fill="{PACK}"/></g>',
         place(label_tall(pr, p), -37, -136, .74),
         f'<path d="{body}" fill="url(#{p}shade)"/>',
         spec(p, -W + 3, -(H - 6), 5, H - 20, .7),
         lit(rect_d(-21, -H - 48, 42, 38, 7), p, cap),
         lit(rect_d(-18, -H - 54, 36, 8, 3), p, cap),
         f'<path d="{rect_d(-21, -H - 48, 42, 38, 7)}" fill="url(#{p}top)"/>']
    return {"svg": "".join(o), "l": -W, "r": W, "top": -H - 54}


def pack_jar(pr, p):
    cap = CATS[pr["category"]]["base"]
    W, H = 86, 104
    body = f"M{-W} -16Q{-W} 0 {-W + 16} 0H{W - 16}Q{W} 0 {W} -16V{-H}H{-W}Z"
    lid = rect_d(-90, -H - 48, 180, 50, 10)
    ridges = "".join(f'<path d="M{x} {-H - 44}V{-H - 2}" stroke="#000" stroke-opacity=".05"/>' for x in range(-84, 88, 6))
    o = [ground(p, -W, W), lit(body, p, PACK), place(label_wide(pr, p), -76, -97, .95),
         spec(p, -W + 3, -H + 8, 6, H - 22, .5),
         lit(lid, p, cap), ridges, f'<path d="{lid}" fill="url(#{p}top)"/>']
    return {"svg": "".join(o), "l": -90, "r": 90, "top": -H - 48}


def pack_tube(pr, p):
    cap = CATS[pr["category"]]["base"]
    body = "M-31 -40C-33 -90 -52 -150 -52 -208V-222H52V-208C52 -150 33 -90 31 -40Z"
    crimp = rect_d(-54, -236, 108, 16, 2)
    lines = "".join(f'<path d="M-52 {y}H52" stroke="#000" stroke-opacity=".07"/>' for y in (-232, -228, -224))
    o = [ground(p, -32, 32), lit(rect_d(-30, -44, 60, 44, 9), p, cap),
         f'<path d="{rect_d(-30, -44, 60, 44, 9)}" fill="url(#{p}top)"/>',
         lit(body, p, PACK), place(label_tall(pr, p), -39, -212, .78),
         spec(p, -48, -204, 5, 80, .55), lit(crimp, p, PACK), lines]
    return {"svg": "".join(o), "l": -54, "r": 54, "top": -236}


def pack_tin(pr, p):
    cat = CATS[pr["category"]]
    R, ry = 57, 17
    base_d = f"M-56 {-ry - 18}V{-ry}A56 {ry} 0 0 0 56 {-ry}V{-ry - 18}Z"
    lid_d = f"M{-R} {-ry - 36}V{-ry - 18}A{R} {ry} 0 0 0 {R} {-ry - 18}V{-ry - 36}Z"
    cy = -ry - 36
    print_top = (f'<g transform="translate(0 {cy}) scale(1 {f(ry / R)})">'
                 f'<circle r="{R - 5}" fill="none" stroke="{MOSS}" stroke-opacity=".12"/>'
                 f'<use href="#{p}wm" x="-23" y="-27" width="46" height="14.5" style="color:{MOSS}"/>'
                 + text(0, 6, " ".join(pr["name"]), 11, DISPLAY, 500, anchor="middle", style=SOFT)
                 + text(0, 19, pr["hindi"], 8, DEVA, 600, fill="#55695C", anchor="middle")
                 + text(0, 33, pr["size"], 7, BODY, 700, anchor="middle") + "</g>")
    o = [ground(p, -R, R), lit(base_d, p, PACK),
         text(0, -ry - 6, f"{pr['natural']}% NATURALLY DERIVED**  ·  {pr['size'].upper()}", 4.6, BODY, 700, anchor="middle", ls=".4"),
         lit(lid_d, p, cat["base"]),
         f'<ellipse cx="0" cy="{cy}" rx="{R}" ry="{ry}" fill="{cat["base"]}"/>',
         f'<ellipse cx="0" cy="{cy}" rx="{R}" ry="{ry}" fill="#fff" fill-opacity=".28"/>', print_top,
         f'<ellipse cx="0" cy="{cy}" rx="{R}" ry="{ry}" fill="none" stroke="#000" stroke-opacity=".08"/>']
    return {"svg": "".join(o), "l": -R, "r": R, "top": cy - ry}


def pack_wipes(pr, p):
    cap = CATS[pr["category"]]["base"]
    body = "M-140 -8C-149 -60 -149 -118 -140 -168H140C149 -118 149 -60 140 -8Z"

    def crimp(x0, x1):
        pts, y, i = [], -166, 0
        while y <= -10:
            pts.append((x1 if i % 2 else x0, y))
            y += 6
            i += 1
        inner = -138 if x0 < 0 else 138
        return "M" + f"{inner} -166L" + "L".join(f"{f(x)} {f(yy)}" for x, yy in pts) + f"L{inner} -10Z"

    lid = rect_d(16, -142, 108, 108, 28)
    o = [ground(p, -150, 150), lit(crimp(-153, -147), p, PACK), lit(crimp(153, 147), p, PACK), lit(body, p, PACK),
         f'<path d="M-140 -168H140" stroke="#000" stroke-opacity=".06"/>',
         place(label_wide(pr, p), -132, -128, .86),
         lit(lid, p, cap), f'<path d="{lid}" fill="url(#{p}top)"/>',
         f'<path d="{rect_d(25, -133, 90, 90, 21)}" fill="none" stroke="#000" stroke-opacity=".08"/>',
         f'<use href="#{p}mk" x="46" y="-112" width="48" height="48" style="color:{MOSS}"/>',
         spec(p, -139, -150, 5, 120, .45)]
    return {"svg": "".join(o), "l": -153, "r": 153, "top": -168}


def pack_shaker(pr, p):
    cap = CATS[pr["category"]]["base"]
    W, H = 48, 172
    body = (f"M{-W} -12Q{-W} 0 -36 0H36Q{W} 0 {W} -12V-150C{W} -168 30 {-H} 26 {-H}"
            f"H-26C-30 {-H} {-W} -168 {-W} -150Z")
    dome = f"M-34 {-H - 26}Q0 {-H - 48} 34 {-H - 26}Z"
    holes = "".join(f'<circle cx="{x}" cy="{-H - 33 + abs(x) * .08}" r="1.7" fill="#000" fill-opacity=".25"/>'
                    for x in (-14, -7, 0, 7, 14))
    o = [ground(p, -W, W), lit(body, p, PACK), place(label_tall(pr, p), -39, -152, .78),
         spec(p, -W + 3, -150, 5, 130, .55),
         lit(dome, p, cap), lit(rect_d(-34, -H - 30, 68, 34, 8), p, cap),
         f'<path d="{rect_d(-34, -H - 30, 68, 34, 8)}" fill="url(#{p}top)"/>', holes]
    return {"svg": "".join(o), "l": -W, "r": W, "top": -H - 40}


def render(pr, p):
    kind = pr["pack"]
    return {"pump": lambda: pack_pump(pr, p), "foam": lambda: pack_pump(pr, p, foam=True),
            "oil": lambda: pack_oil(pr, p), "jar": lambda: pack_jar(pr, p), "tube": lambda: pack_tube(pr, p),
            "tin": lambda: pack_tin(pr, p), "wipes": lambda: pack_wipes(pr, p),
            "shaker": lambda: pack_shaker(pr, p)}[kind]()


def viewbox(pk, pad=26):
    l, r, t = pk["l"] - pad, pk["r"] + pad, pk["top"] - pad
    return f"{f(l)} {f(t)} {f(r - l)} {f(-t + 16)}"


# ---------------------------------------------------------------- line-up

GROUPS = [("moisturise", ["rich-cream", "daily-lotion", "massage-oil"]),
          ("care", ["diaper-rash-cream", "all-purpose-balm", "mineral-sunscreen"]),
          ("hygiene", ["talc-free-powder", "bottle-wash", "water-wipes"])]


def lineup(p):
    x, parts, arches = 0.0, [], []
    for gi, (cat, slugs) in enumerate(GROUPS):
        g0 = x
        for si, slug in enumerate(slugs):
            pk = render(BY_SLUG[slug], p)
            if si:
                x += 30
            x -= pk["l"]
            parts.append(f'<g transform="translate({f(x)} 0)">{pk["svg"]}</g>')
            x += pk["r"]
        g1 = x
        c = CATS[cat]
        x0, x1 = g0 - 36, g1 + 36
        half = (x1 - x0) / 2
        top = -352
        arches.append(f'<path d="M{f(x0)} 46V{f(top + half)}A{f(half)} {f(half)} 0 0 1 {f(x1)} {f(top + half)}V46Z" fill="{c["wash"]}"/>'
                      + text((x0 + x1) / 2, 32, c["name"].upper(), 12, BODY, 700, fill=c["deep"], ls="2.4", anchor="middle"))
        x += 110
    width = x - 110
    return f'<g>{"".join(arches)}{"".join(parts)}</g>', width


# ---------------------------------------------------------------- brand book fragment

WHY = {  # what each hero ingredient is there to do (Daily Lotion back label)
    "Colloidal oat": "calms and protects dry, itchy skin",
    "Shea butter": "locks in moisture",
    "Coconut oil": "softens and smooths",
}


def barcode():
    rnd = random.Random(890)
    x, bars = 0, []
    for i in range(58):
        w = rnd.choice((1, 1, 1.5, 2))
        if i % 2 == 0:
            tall = i < 3 or 28 <= i <= 31 or i > 54
            bars.append(f'<rect x="{f(x)}" y="0" width="{f(w)}" height="{46 if tall else 40}" fill="{MOSS}"/>')
        x += w
    return (f'<svg class="barcode" viewBox="-4 -4 {f(x + 8)} 60" role="img" aria-label="Barcode placeholder">'
            f'{"".join(bars)}<text x="{f(x / 2)}" y="54" font-family="{BODY}" font-size="7" text-anchor="middle" fill="{MOSS}">'
            f'890 · placeholder</text></svg>')


RECYCLE = (f'<svg class="recycle" viewBox="0 0 48 52" role="img" aria-label="Recycling code 5, PP">'
           f'<path d="M24 5L42 37H6Z" fill="none" stroke="{MOSS}" stroke-width="2.4" stroke-linejoin="round"/>'
           f'<path d="M30 15l2-5 4 3M38 37l3 4-5 1M10 37l-5 1 2-5" fill="none" stroke="{MOSS}" stroke-width="2"/>'
           f'<text x="24" y="32" font-family="{BODY}" font-weight="700" font-size="13" text-anchor="middle" fill="{MOSS}">5</text>'
           f'<text x="24" y="50" font-family="{BODY}" font-weight="700" font-size="8" text-anchor="middle" fill="{MOSS}">PP</text></svg>')


def back_label(pr):
    cat = CATS[pr["category"]]
    hero = "".join(f"<li><b>{esc(h)}</b> {esc(WHY.get(h, ''))}</li>" for h in pr["hero"])
    rows = [("Net quantity", pr["size"]), ("MRP", "₹ [—] incl. of all taxes"), ("Unit sale price", "₹ [—] per ml"),
            ("Mfg. date", "MM/YYYY"), ("Use before", "MM/YYYY"), ("Batch no.", "[—]"),
            ("Mfg. licence no.", "[State licence no.]"), ("Country of origin", "India")]
    meta = "".join(f"<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>" for k, v in rows)
    return f"""
<div class="backlabel" style="--cat:{cat['base']};--deep:{cat['deep']}">
  <div class="bl-head">
    <svg viewBox="0 0 426 134" class="bl-wm" aria-label="nanhe"><use href="#wordmark"/></svg>
    <span>{esc(' '.join(pr['name']))} · <span class="deva">{esc(pr['hindi'])}</span></span>
  </div>
  <div class="bl-grid">
    <div class="bl-col">
      <h4>What's inside, and why</h4>
      <ul class="bl-why">{hero}</ul>
      <h4>Ingredients</h4>
      <p class="bl-inci">{esc(pr['inci'])}</p>
      <p class="bl-note">Formula shown is indicative until the formulator confirms it.</p>
    </div>
    <div class="bl-col">
      <h4>How to use</h4>
      <p>{esc(pr['use'])}</p>
      <h4>Caution</h4>
      <p>For external use only. Avoid contact with eyes. Stop use if irritation occurs. Keep out of reach of children. Store below 30°C, away from direct sunlight.</p>
      <h4>Our claims, explained</h4>
      <p class="bl-foot">*Clinically tested under dermatological supervision on [n] infants aged [x–y] months, [lab name], [year]. **{pr['natural']}% naturally derived content, calculated per ISO 16128. Free from parabens, SLS/SLES, mineral oil, synthetic fragrance, phthalates and artificial dyes.</p>
    </div>
  </div>
  <dl class="bl-meta">{meta}</dl>
  <div class="bl-bottom">
    <div class="bl-who">
      <p><b>Manufactured by:</b> [Manufacturer name], [full address, PIN].</p>
      <p><b>Marketed by:</b> [Nanhe legal entity], [full address, PIN].</p>
      <p><b>Customer care:</b> [phone] · [email] · [address]. Mon–Sat, 10am–6pm.</p>
    </div>
    <div class="bl-marks">{RECYCLE}{barcode()}</div>
  </div>
</div>"""


def product_card(pr, p):
    cat = CATS[pr["category"]]
    pk = render(pr, p)
    chips = "".join(f"<li>{esc(h)}</li>" for h in pr["hero"])
    caution = f'<p class="pc-caution">{esc(pr["caution"])}</p>' if pr.get("caution") else ""
    return f"""
<article class="pcard">
  <div class="pc-stage" style="background:{cat['wash']}">
    <svg viewBox="{viewbox(pk)}" role="img" aria-label="{esc(' '.join(pr['name']))} pack render">{pk['svg']}</svg>
  </div>
  <div class="pc-body">
    <span class="pc-eyebrow" style="color:{cat['deep']}">{esc(pr['age'])} · {esc(pr['size'])}</span>
    <h3>{esc(' '.join(pr['name']))}</h3>
    <span class="pc-deva">{esc(pr['hindi'])}</span>
    <p class="pc-line">{esc(pr['line'])}</p>
    <ul class="pc-chips" style="--chip:{cat['wash']}">{chips}</ul>
    <p class="pc-use"><b>How to use.</b> {esc(pr['use'])}</p>
    {caution}
  </div>
</article>"""


FRAGMENT_CSS = """
<style>
.lineup-band{background:linear-gradient(180deg,var(--milk) 0%,var(--paper) 100%);overflow:hidden}
.lineup-scroll{overflow-x:auto;margin-top:8px;padding-bottom:8px}
.lineup-scroll svg{width:100%;min-width:760px;height:auto}
.lineup-notes{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:28px}
.lineup-notes div{border-top:2px solid var(--c);padding-top:12px;font-size:.95rem;color:var(--moss-2)}
.lineup-notes b{display:block;color:var(--moss);font-family:var(--f-display);font-variation-settings:"SOFT" 100;font-weight:500;font-size:var(--s1);margin-bottom:2px}
.cat-block{margin-top:56px}
.cat-block:first-of-type{margin-top:0}
.cat-head{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;margin-bottom:18px}
.cat-head h3{font-size:var(--s3)}
.cat-head .sw-dot{width:16px;height:16px;border-radius:50%;align-self:center}
.cat-head p{color:var(--moss-2);flex:1 1 280px}
.pgrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.pcard{background:var(--milk);border:1px solid var(--line);border-radius:var(--r);overflow:hidden;display:grid;grid-template-rows:auto 1fr}
.pc-stage{aspect-ratio:1/1;display:grid;place-items:center;padding:18px;max-width:100%}
.pc-stage svg{width:100%;height:100%;max-height:300px}
.pc-body{padding:20px 22px 24px;display:grid;gap:8px;align-content:start}
.pc-eyebrow{font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase}
.pc-body h3{font-size:var(--s2)}
.pc-deva{font-family:var(--f-deva);font-weight:600;color:var(--moss-2);line-height:1}
.pc-line{font-size:1rem;margin-top:4px}
.pc-chips{display:flex;flex-wrap:wrap;gap:6px;list-style:none;padding:0;margin:4px 0 0}
.pc-chips li{background:var(--chip);border-radius:999px;padding:4px 10px;font-size:12px;font-weight:600}
.pc-use{font-size:.9rem;color:var(--moss-2);margin-top:4px}
.pc-use b{color:var(--moss)}
.pc-caution{font-size:.85rem;color:var(--alert);font-weight:500}
.label-pair{display:grid;grid-template-columns:minmax(0,.7fr) minmax(0,1.3fr);gap:24px;align-items:start}
.front-flat{background:var(--apricot-wash);border-radius:var(--r);padding:28px;display:grid;place-items:center;gap:12px}
.front-flat svg{width:min(260px,100%);filter:drop-shadow(0 18px 30px rgba(31,58,43,.18))}
.front-flat p{font-size:var(--s-1);color:var(--moss-2);text-align:center}
.backlabel{background:var(--milk);border-radius:var(--r);border:1px solid var(--line);border-top:12px solid var(--cat);padding:26px 26px 22px;display:grid;gap:18px;font-size:.88rem;box-shadow:0 24px 60px -34px rgba(31,58,43,.4);min-width:0}
.bl-head{display:flex;align-items:center;gap:14px;flex-wrap:wrap;font-family:var(--f-display);font-variation-settings:"SOFT" 100;font-size:var(--s1)}
.bl-wm{width:92px;color:var(--moss)}
.bl-head .deva{font-size:1rem;color:var(--moss-2)}
.bl-grid{display:grid;grid-template-columns:1fr 1fr;gap:22px}
.bl-col{display:grid;gap:6px;align-content:start;min-width:0}
.bl-col h4{margin:8px 0 0;font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--deep)}
.bl-col h4:first-child{margin-top:0}
.bl-why{list-style:none;margin:0;padding:0;display:grid;gap:4px}
.bl-why b{font-weight:700}
.bl-inci{font-size:.8rem;line-height:1.5;color:var(--moss-2)}
.bl-note{font-size:.75rem;color:var(--apricot-dp)}
.bl-foot{font-size:.8rem;color:var(--moss-2)}
.bl-meta{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:0;margin:0;border:1px solid var(--line);border-radius:14px;overflow:hidden}
.bl-meta div{padding:10px 12px;border-right:1px solid var(--line);border-bottom:1px solid var(--line)}
.bl-meta div:nth-child(4n){border-right:0}
.bl-meta div:nth-last-child(-n+4){border-bottom:0}
.bl-meta dt{font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--moss-2)}
.bl-meta dd{margin:2px 0 0;font-weight:600;font-variant-numeric:tabular-nums}
.bl-bottom{display:flex;gap:18px;justify-content:space-between;align-items:end;flex-wrap:wrap}
.bl-who{display:grid;gap:4px;font-size:.8rem;color:var(--moss-2);flex:1 1 280px}
.bl-who b{color:var(--moss)}
.bl-marks{display:flex;align-items:end;gap:16px}
.recycle{width:34px}
.barcode{width:130px}
.mandatory{margin-top:16px;display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.mandatory div{border-radius:var(--r);padding:18px 20px;background:var(--milk);border:1px solid var(--line);font-size:.92rem;color:var(--moss-2)}
.mandatory b{display:block;color:var(--moss);margin-bottom:4px}
@media (max-width:900px){
  .pgrid{grid-template-columns:repeat(2,minmax(0,1fr))}
  .label-pair,.bl-grid{grid-template-columns:1fr}
  .lineup-notes,.mandatory{grid-template-columns:1fr}
}
@media (max-width:560px){
  .pgrid{grid-template-columns:1fr}
  .bl-meta{grid-template-columns:1fr 1fr}
  .bl-meta div:nth-child(4n){border-right:1px solid var(--line)}
  .bl-meta div:nth-child(2n){border-right:0}
  .bl-meta div:nth-last-child(-n+4){border-bottom:1px solid var(--line)}
  .bl-meta div:nth-last-child(-n+2){border-bottom:0}
}
</style>"""

CAT_BLURBS = {
    "moisturise": "Daily softness, from the first massage to bedtime.",
    "care": "For when skin needs fixing or protecting.",
    "hygiene": "The things parents reach for ten times a day.",
}


def fragment():
    p = "pk-"
    lu, width = lineup(p)
    cats_html = []
    for cat, slugs in GROUPS:
        c = CATS[cat]
        cards = "".join(product_card(BY_SLUG[s], p) for s in slugs)
        cats_html.append(f"""
  <div class="cat-block">
    <div class="cat-head"><span class="sw-dot" style="background:{c['base']}"></span><h3>{esc(c['name'])}</h3><p>{esc(CAT_BLURBS[cat])}</p></div>
    <div class="pgrid">{cards}</div>
  </div>""")
    lotion = BY_SLUG["daily-lotion"]
    front = label_tall(lotion, p)
    return f"""<!-- BEGIN:packaging -->
<!-- Generated by scripts/build_packaging.py from docs/product/products.json. Edit those, not this block. -->
{FRAGMENT_CSS}
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{defs(p)}</defs></svg>

<section class="lineup-band" id="line">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">The line</span>
      <h2>Nine products, three colours, one family</h2>
      <p class="lede">Every pack is matte milk-white with the wordmark in the same place. Only the cap and the category text change colour, so the line looks calm on a shelf and each product is easy to find.</p>
    </div>
    <div class="lineup-scroll">
      <svg viewBox="-40 -372 {f(width + 80)} 430" role="img" aria-label="The Nanhe line-up: nine packs in three category groups">{lu}</svg>
    </div>
    <div class="lineup-notes">
      <div style="--c:{CATS['moisturise']['base']}"><b>Moisturise</b>Lotion in a 200 ml pump, massage oil in a clear bottle that shows the oil, and a rich cream in a 100 g jar.</div>
      <div style="--c:{CATS['care']['base']}"><b>Care &amp; Protect</b>Rash cream and sunscreen in 50 g tubes that stand on their caps, and a 25 g balm tin for the changing bag.</div>
      <div style="--c:{CATS['hygiene']['base']}"><b>Everyday Hygiene</b>Talc-free powder in a sifter shaker, bottle wash in a 300 ml foam pump, and 72 wipes in a soft pack with a rigid lid.</div>
    </div>
  </div>
</section>

<section id="products">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Products</span>
      <h2>What's in each one, and who it's for</h2>
      <p class="lede">Hero ingredients, age range and directions for every product. Formulas and percentages are placeholders until the formulator and lab confirm them.</p>
    </div>
    {''.join(cats_html)}
  </div>
</section>

<section class="band-paper" id="labels">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Labels</span>
      <h2>The front makes the promise. The back proves it.</h2>
      <p class="lede">The Daily Lotion labels show the template every product follows. The back label explains every front claim and carries all the details Indian law requires on a cosmetics pack.</p>
    </div>
    <div class="label-pair">
      <div class="front-flat">
        <svg viewBox="-6 -6 112 162" role="img" aria-label="Daily Lotion front label, flat">
          <rect x="-4" y="-4" width="108" height="158" rx="8" fill="{PACK}"/>{front}
        </svg>
        <p>Front label, flat · 96 × 144 mm on the 200 ml bottle</p>
      </div>
      {back_label(lotion)}
    </div>
    <div class="mandatory">
      <div><b>Legal Metrology</b>Net quantity, MRP including all taxes, unit sale price, month and year of manufacture, and the manufacturer or marketer's name, address and customer care details.</div>
      <div><b>Cosmetics Rules, 2020</b>Manufacturing licence number, batch number, use-before date, full ingredient list, directions and warnings.</div>
      <div><b>Placeholders</b>Everything in [brackets] is filled in from the real licence, lab reports and pricing before print. A regulatory consultant signs off the final artwork.</div>
    </div>
  </div>
</section>
<!-- END:packaging -->"""


# ---------------------------------------------------------------- outputs

def write_standalone():
    out = ROOT / "assets/packaging"
    out.mkdir(parents=True, exist_ok=True)
    for pr in PRODUCTS:
        pk = render(pr, "")
        vb = viewbox(pk, 30)
        (out / f"{pr['slug']}.svg").write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="{esc(" ".join(pr["name"]))}">'
            f'<title>Nanhe {esc(" ".join(pr["name"]))}</title><style><![CDATA[{FONT_IMPORT}]]></style>'
            f'<rect x="{vb.split()[0]}" y="{vb.split()[1]}" width="100%" height="100%" fill="{CATS[pr["category"]]["wash"]}"/>'
            f'<defs>{defs("")}</defs>{pk["svg"]}</svg>\n')
    lu, width = lineup("")
    (out / "lineup.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-40 -372 {f(width + 80)} 430" role="img" aria-label="Nanhe line-up">'
        f'<title>Nanhe line-up</title><style><![CDATA[{FONT_IMPORT}]]></style>'
        f'<rect x="-40" y="-372" width="{f(width + 80)}" height="430" fill="{MILK}"/>'
        f'<defs>{defs("")}</defs>{lu}</svg>\n')


def write_product_md():
    lines = ["# Nanhe product line", "",
             "Generated from `docs/product/products.json` by `scripts/build_packaging.py`. "
             "Formulas and percentages are indicative until the formulator and lab confirm them.", ""]
    for cat, slugs in GROUPS:
        lines += [f"## {CATS[cat]['name']}", ""]
        for s in slugs:
            pr = BY_SLUG[s]
            lines += [f"### {' '.join(pr['name'])} ({pr['hindi']})", "",
                      f"- **Pack:** {pr['size']}, {pr['pack']} · `assets/packaging/{s}.svg`",
                      f"- **Age:** {pr['age']}",
                      f"- **Promise:** {pr['line']}",
                      f"- **Hero ingredients:** {', '.join(pr['hero'])}",
                      f"- **Naturally derived:** {pr['natural']}% (placeholder)",
                      f"- **How to use:** {pr['use']}"]
            if pr.get("caution"):
                lines.append(f"- **Caution:** {pr['caution']}")
            lines += [f"- **Ingredients (indicative):** {pr['inci']}", ""]
    (ROOT / "docs/product/product-line.md").write_text("\n".join(lines))


def inject_brand_book():
    path = ROOT / "brand-book/index.html"
    page = path.read_text()
    frag = fragment()
    start, end = "<!-- BEGIN:packaging -->", "<!-- END:packaging -->"
    if start in page:
        a = page.index(start)
        b = page.index(end) + len(end)
        page = page[:a] + frag + page[b:]
    else:
        anchor = "<!-- ============ VOICE ============ -->"
        page = page.replace(anchor, frag + "\n\n" + anchor, 1)
    path.write_text(page)


if __name__ == "__main__":
    write_standalone()
    write_product_md()
    inject_brand_book()
    print(f"Rendered {len(PRODUCTS)} packs, line-up, product sheet and brand book block.")
