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


# ---------------------------------------------------------------- direction A: baby animal characters
# Head-and-shoulders portraits on a 60 grid: moss outline, category-colour fill, dot eyes, blush.
# Each animal is Indian, and each one has a reason to be on its product.

BLUSH = "#F29C84"


def _eyes(y, dx=5.5, cx=30, r=1.9):
    return "".join(f'<circle cx="{f(cx + sx * dx)}" cy="{f(y)}" r="{r}" fill="{MOSS}" stroke="none"/>'
                   f'<circle cx="{f(cx + sx * dx + .6)}" cy="{f(y - .7)}" r=".6" fill="#fff" stroke="none"/>'
                   for sx in (-1, 1))


def _blush(y, dx=10.5, cx=30):
    return "".join(f'<ellipse cx="{f(cx + sx * dx)}" cy="{f(y)}" rx="2.8" ry="1.7" fill="{BLUSH}" fill-opacity=".55" stroke="none"/>'
                   for sx in (-1, 1))


def _smile(y, cx=30, w=2):
    return f'<path d="M{f(cx - w)} {f(y)}q{f(w)} 1.8 {f(2 * w)} 0" fill="none"/>'


def star(cx, cy, R, k=.48):
    pts = []
    for i in range(10):
        a = math.radians(-90 + i * 36)
        rr = R if i % 2 == 0 else R * k
        pts.append(f"{f(cx + rr * math.cos(a))} {f(cy + rr * math.sin(a))}")
    return "M" + "L".join(pts) + "Z"


def cloud(cx, cy, s=1):
    return (f'<g transform="translate({f(cx)} {f(cy)}) scale({f(s)})"><circle cx="-7" cy="1" r="5.5"/>'
            f'<circle cx="0" cy="-3" r="7.5"/><circle cx="8" cy="1" r="5.5"/><rect x="-12" y="0" width="25" height="6.5" rx="3.2"/></g>')


def ch_elephant(B, W):
    return (f'<ellipse cx="13" cy="29" rx="10.5" ry="13" fill="{B}"/><ellipse cx="47" cy="29" rx="10.5" ry="13" fill="{B}"/>'
            f'<ellipse cx="14" cy="30" rx="5.8" ry="8.5" fill="{W}" stroke="none"/><ellipse cx="46" cy="30" rx="5.8" ry="8.5" fill="{W}" stroke="none"/>'
            f'<ellipse cx="30" cy="27" rx="15" ry="14.5" fill="{B}"/>'
            f'<path d="M25 34C24.5 45 27 53 33.5 53C37.5 53 39 49.5 36.3 48.6C33.6 48 33.6 45 34.5 34Z" fill="{B}" stroke="none"/>'
            '<path d="M25 34.5C24.5 45 27 53 33.5 53C37.5 53 39 49.5 36.3 48.6C33.6 48 33.6 45 34.5 34.5" fill="none"/>'
            '<path d="M27 13.5q1.5 -3.5 3 0q1.5 -3.5 3 0" fill="none"/>' + _eyes(25) + _blush(31, 11))


def ch_squirrel(B, W):
    return (f'<path d="M40 46C56 46 60 28 52 18C47 12 39 15 42 21C46 27 49 35 38 38Z" fill="{B}"/>'
            f'<ellipse cx="20.5" cy="20" rx="4.2" ry="5.4" transform="rotate(-20 20.5 20)" fill="{B}"/>'
            f'<ellipse cx="39.5" cy="20" rx="4.2" ry="5.4" transform="rotate(20 39.5 20)" fill="{B}"/>'
            f'<ellipse cx="30" cy="32" rx="14" ry="13" fill="{B}"/>'
            f'<ellipse cx="30" cy="37.5" rx="7.5" ry="4.8" fill="{W}" stroke="none"/>'
            '<path d="M26.5 20.5V25M30 19.5V25.5M33.5 20.5V25" stroke="#fff" stroke-opacity=".9" stroke-width="1.8" fill="none"/>'
            f'<circle cx="30" cy="35.6" r="1.4" fill="{MOSS}" stroke="none"/>' + _smile(38.2) + _eyes(31) + _blush(36, 10))


def ch_bear(B, W):
    return (f'<circle cx="17" cy="19" r="6.5" fill="{B}"/><circle cx="43" cy="19" r="6.5" fill="{B}"/>'
            f'<circle cx="17" cy="19" r="3.2" fill="{W}" stroke="none"/><circle cx="43" cy="19" r="3.2" fill="{W}" stroke="none"/>'
            f'<circle cx="30" cy="33" r="16" fill="{B}"/><ellipse cx="30" cy="39" rx="7.5" ry="5.8" fill="{W}"/>'
            f'<ellipse cx="30" cy="36.6" rx="2.6" ry="1.8" fill="{MOSS}" stroke="none"/>' + _smile(40, w=2.2)
            + _eyes(31, 6.5) + _blush(37, 11.5))


def ch_tortoise(B, W):
    return (f'<path d="M7 43A23 21 0 0 1 53 43Z" fill="{B}"/>'
            '<path d="M30 22.5V33M18.5 27.5L23 33H37L41.5 27.5M23 33L19 43M37 33L41 43" fill="none" stroke-opacity=".45"/>'
            f'<circle cx="30" cy="43" r="10" fill="{W}"/>' + _eyes(41.5, 3.6, r=1.6) + _blush(45.5, 7.2)
            + _smile(46, w=1.7))


def ch_hedgehog(B, W):
    pts = []
    for i, a in enumerate(range(150, 391, 12)):
        r = 22 if i % 2 else 16.5
        pts.append(f"{f(30 + r * math.cos(math.radians(a)))} {f(36 + r * math.sin(math.radians(a)))}")
    return (f'<path d="M{"L".join(pts)}Z" fill="{B}"/>'
            f'<ellipse cx="30" cy="38" rx="12.5" ry="11" fill="{W}"/>'
            f'<circle cx="30" cy="40.5" r="2.2" fill="{MOSS}" stroke="none"/>' + _smile(44, w=1.8)
            + _eyes(35.5, 4.8) + _blush(41, 8.8))


def ch_peacock(B, W):
    crest = "".join(f'<path d="M30 18L{x} {y}" fill="none"/><circle cx="{x}" cy="{y}" r="2.7" fill="{B}"/>'
                    f'<circle cx="{x}" cy="{y}" r="1" fill="{MOSS}" stroke="none"/>'
                    for x, y in ((23.5, 6.5), (30, 4), (36.5, 6.5)))
    return (crest + f'<circle cx="30" cy="32" r="15" fill="{B}"/>'
            '<ellipse cx="24.2" cy="30.6" rx="4" ry="3.1" fill="#fff" stroke="none"/>'
            '<ellipse cx="35.8" cy="30.6" rx="4" ry="3.1" fill="#fff" stroke="none"/>'
            f'<path d="M27 36.2H33L30 40.6Z" fill="{MARIGOLD}"/>' + _eyes(31, 5.8) + _blush(37, 10.5))


def ch_bunny(B, W):
    return (f'<ellipse cx="23" cy="15" rx="4.8" ry="12" transform="rotate(-8 23 15)" fill="{B}"/>'
            f'<ellipse cx="37" cy="15" rx="4.8" ry="12" transform="rotate(8 37 15)" fill="{B}"/>'
            f'<ellipse cx="23" cy="16" rx="2.1" ry="8" transform="rotate(-8 23 16)" fill="{W}" stroke="none"/>'
            f'<ellipse cx="37" cy="16" rx="2.1" ry="8" transform="rotate(8 37 16)" fill="{W}" stroke="none"/>'
            f'<circle cx="30" cy="37" r="14" fill="{B}"/>'
            f'<path d="M28.6 40H31.4L30 41.6Z" fill="{MOSS}" stroke-width="1.2"/>'
            '<path d="M30 41.6V43M30 43q-1.6 1.3 -3 0M30 43q1.6 1.3 3 0" fill="none" stroke-width="1.3"/>'
            + _eyes(35.5) + _blush(40.5, 10))


def ch_duckling(B, W):
    return (f'<path d="M29 18c-1.2 -4.5 2 -7 4.5 -5.8c-2.2 1 -2.4 3.2 -1.4 5.8" fill="{B}"/>'
            f'<circle cx="30" cy="32" r="15" fill="{B}"/>'
            f'<ellipse cx="30" cy="38.6" rx="6.8" ry="3.3" fill="{MARIGOLD}"/>'
            '<path d="M24 38.6H36" fill="none" stroke-opacity=".35"/>' + _eyes(31, 6) + _blush(36, 11))


def ch_dolphin(B, W):
    return (f'<path d="M10 41C5 37 3 33 4 30.5C7 33.5 10 35.5 13 37.5Z" fill="{B}"/>'
            f'<path d="M10 42.5C6 45.5 4.5 49 5 51C8 48.5 11 46.5 14 44.5Z" fill="{B}"/>'
            f'<path d="M26 24.5C27 19.5 31 16.5 35 16.5C33 19 32.5 22 33 25" fill="{B}"/>'
            f'<path d="M8 42C12 28 26 22 40 26C44 27.5 47 29.5 49 31L58 31.5C58.5 33.5 56 35 49 35C44 40 30 46 18 45C13 44.6 10 43.6 8 42Z" fill="{B}"/>'
            f'<path d="M14 41C24 42 36 40 46 35.5" fill="none" stroke="#fff" stroke-opacity=".7"/>'
            f'<circle cx="41.5" cy="30" r="1.8" fill="{MOSS}" stroke="none"/><circle cx="42" cy="29.4" r=".55" fill="#fff" stroke="none"/>'
            f'<ellipse cx="42.5" cy="34" rx="2.6" ry="1.5" fill="{BLUSH}" fill-opacity=".55" stroke="none"/>'
            '<circle cx="40" cy="10" r="1.6" fill="none"/><circle cx="46" cy="6" r="1.2" fill="none"/><circle cx="50" cy="12" r="1" fill="none"/>')


CHARACTERS = {  # slug: (name, animal, why it's on this product, drawing)
    "daily-lotion": ("Haathi", "Elephant calf", "Gentle giant with famously soft skin", ch_elephant),
    "massage-oil": ("Gilu", "Palm squirrel", "Lives in the coconut trees the oil comes from", ch_squirrel),
    "rich-cream": ("Bhalu", "Himalayan bear cub", "Made for cold, dry winter cheeks", ch_bear),
    "diaper-rash-cream": ("Kachhu", "Tortoise", "Its shell is a barrier, like the cream", ch_tortoise),
    "all-purpose-balm": ("Kaantu", "Indian hedgehog", "Small, tough and handy for every prickly patch", ch_hedgehog),
    "mineral-sunscreen": ("Moru", "Peacock chick", "Loves the sun, dances in the rain", ch_peacock),
    "talc-free-powder": ("Khargu", "Hare", "Soft as a powder-puff tail", ch_bunny),
    "bottle-wash": ("Batku", "Duckling", "Happiest around water and bubbles", ch_duckling),
    "water-wipes": ("Susu", "Ganges river dolphin", "Called susu along the Ganga, a creature of pure water", ch_dolphin),
}


def character_defs(p):
    out = []
    for slug, (_, _, _, draw) in CHARACTERS.items():
        c = CATS[BY_SLUG[slug]["category"]]
        out.append(f'<symbol id="{p}ch-{slug}" viewBox="0 0 60 60"><g stroke="{MOSS}" stroke-width="1.8" '
                   f'stroke-linecap="round" stroke-linejoin="round">{draw(c["base"], c["wash"])}</g></symbol>')
    return "".join(out)


# ---------------------------------------------------------------- direction B: nursery motifs

def _tile(col, op):
    return (f'<g fill="{col}" fill-opacity="{op}">'
            '<path d="M11 3.5a6.5 6.5 0 1 0 5 11.2a5.2 5.2 0 1 1 -5 -11.2Z"/>'
            f'<path d="{star(28, 8, 3.4)}"/><circle cx="6" cy="27" r="1.3"/><circle cx="33" cy="22" r="1"/>'
            f'{cloud(21, 29, .55)}</g>')


def pattern_defs(p):
    out = [f'<pattern id="{p}pat-{k}" width="38" height="38" patternUnits="userSpaceOnUse">{_tile(c["base"], .95)}</pattern>'
           for k, c in CATS.items()]
    out.append(f'<pattern id="{p}patw" width="38" height="38" patternUnits="userSpaceOnUse">{_tile("#fff", .55)}</pattern>')
    return "".join(out)


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
{icons}{character_defs(p)}{pattern_defs(p)}"""


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
    if STYLE["chars"]:
        o.append(f'<use href="#{p}ch-{pr["slug"]}" x="23" y="74" width="54" height="54"/>')
    else:
        o.append(f'<use href="#{p}ic-{pr["icon"]}" x="30" y="83" width="40" height="40" style="color:{deep}"/>')
        if STYLE["motif"]:
            base = CATS[pr["category"]]["base"]
            o.append(f'<path d="{star(24, 88, 3.4)}{star(76, 96, 2.6)}{star(71, 118, 2)}" fill="{base}"/>')
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
        (f'<use href="#{p}ch-{pr["slug"]}" x="106" y="20" width="52" height="52"/>' if STYLE["chars"] else
         f'<use href="#{p}ic-{pr["icon"]}" x="114" y="27" width="38" height="38" style="color:{deep}"/>'),
        f'<path d="M6 73.5H154" stroke="{MOSS}" stroke-opacity=".18" stroke-width=".5"/>',
        text(6, 83, footer_left(pr).upper(), 4.3, weight=700, ls=".4"),
        text(154, 84, pr["size"], 9.5, DISPLAY, 500, anchor="end", style=SOFT),
    ])


def place(content, x, y, s):
    return f'<g transform="translate({f(x)} {f(y)}) scale({f(s)})">{content}</g>'


# Visual style switches. The default is the approved look: direction A, "Little friends"
# (founder's pick, 2026-11-17). The comparison page flips these to show the alternatives.
# "chars": baby animal characters on labels and the line-up arches (direction A).
# "motif": nursery pattern on packs, cloud-topped label panels, rainbow arches (direction B).
STYLE = {"chars": True, "motif": False}


def lineup_top():
    return -470 if STYLE["chars"] else (-400 if STYLE["motif"] else -372)
CUR = None


def cloud_panel(x, y, w, h, n):
    r = w / (2 * n)
    d = f"M{f(x)} {f(y + h - 8)}V{f(y + r)}"
    for i in range(n):
        d += f"A{f(r)} {f(r)} 0 0 1 {f(x + (i + 1) * 2 * r)} {f(y + r)}"
    d += f"V{f(y + h - 8)}Q{f(x + w)} {f(y + h)} {f(x + w - 8)} {f(y + h)}H{f(x + 8)}Q{f(x)} {f(y + h)} {f(x)} {f(y + h - 8)}Z"
    return d


def lab(pr, p, kind, x, y, s):
    content = label_tall(pr, p) if kind == "tall" else label_wide(pr, p)
    if not STYLE["motif"]:
        return place(content, x, y, s)
    panel = cloud_panel(-4, -7, 108, 160, 8) if kind == "tall" else cloud_panel(-4, -7, 168, 101, 12)
    k = .88 if kind == "tall" else .9
    dx, dy = (6 * s, 10 * s) if kind == "tall" else (8 * s, 6 * s)
    return place(f'<path d="{panel}" fill="{MILK}" stroke="{MOSS}" stroke-opacity=".08" stroke-width=".8"/>{content}',
                 x + dx, y + dy, s * k)


# ---------------------------------------------------------------- packs
# Every pack is drawn with its base on y=0, centred on x=0, growing upwards.

def ground(p, l, r):
    return f'<ellipse cx="{f((l + r) / 2)}" cy="2" rx="{f((r - l) * .56)}" ry="10" fill="url(#{p}ground)"/>'


def lit(d, p, fill, stroke=True):
    s = ' stroke="#1F3A2B" stroke-opacity=".1" stroke-width=".8"' if stroke else ""
    pat = ""
    if STYLE["motif"] and fill == PACK and CUR:
        pat = f'<path d="{d}" fill="url(#{p}pat-{CUR["category"]})"/>'
    return f'<path d="{d}" fill="{fill}"{s}/>{pat}<path d="{d}" fill="url(#{p}shade)"/>'


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
    o = [ground(p, -W, W), lit(body, p, PACK), lab(pr, p, 'tall', -(w - 24) / 2, -(H - 34), s),
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
         f'<rect x="{-W}" y="-138" width="{2 * W}" height="120" fill="{PACK}"/>'
         + (f'<rect x="{-W}" y="-138" width="{2 * W}" height="120" fill="url(#{p}pat-{pr["category"]})"/>' if STYLE["motif"] else "")
         + '</g>',
         lab(pr, p, 'tall', -37, -136, .74),
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
    o = [ground(p, -W, W), lit(body, p, PACK), lab(pr, p, 'wide', -76, -97, .95),
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
         lit(body, p, PACK), lab(pr, p, 'tall', -39, -212, .78),
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
         lab(pr, p, 'wide', -132, -128, .86),
         lit(lid, p, cap), f'<path d="{lid}" fill="url(#{p}top)"/>',
         f'<path d="{rect_d(25, -133, 90, 90, 21)}" fill="none" stroke="#000" stroke-opacity=".08"/>',
         (f'<path d="{lid}" fill="url(#{p}patw)"/>' if STYLE["motif"] else ""),
         (f'<use href="#{p}ch-{pr["slug"]}" x="34" y="-124" width="72" height="72"/>' if STYLE["chars"]
          else f'<use href="#{p}mk" x="46" y="-112" width="48" height="48" style="color:{MOSS}"/>'),
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
    o = [ground(p, -W, W), lit(body, p, PACK), lab(pr, p, 'tall', -39, -152, .78),
         spec(p, -W + 3, -150, 5, 130, .55),
         lit(dome, p, cap), lit(rect_d(-34, -H - 30, 68, 34, 8), p, cap),
         f'<path d="{rect_d(-34, -H - 30, 68, 34, 8)}" fill="url(#{p}top)"/>', holes]
    return {"svg": "".join(o), "l": -W, "r": W, "top": -H - 40}


def render(pr, p):
    global CUR
    CUR = pr
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
        cx = (x0 + x1) / 2
        if STYLE["motif"]:
            for inset, op in ((16, .9), (34, .55)):
                a0, a1, hh = x0 + inset, x1 - inset, half - inset
                arches.append(f'<path d="M{f(a0)} 46V{f(top + half)}A{f(hh)} {f(hh)} 0 0 1 {f(a1)} {f(top + half)}V46" '
                              f'fill="none" stroke="{c["base"]}" stroke-opacity="{op}" stroke-width="9"/>')
            arches.append(f'<g fill="#fff">{cloud(x0 + 18, top + half - 30, 2.2)}{cloud(x1 - 22, top + half + 40, 1.8)}</g>')
            arches.append(f'<path d="{star(x0 - 14, top + 70, 7)}{star(x1 + 16, top + 30, 5)}{star(cx - half * .62, top + 26, 4.5)}'
                          f'{star(cx + half * .55, top + 10, 6)}" fill="{c["base"]}"/>')
            arches.append(f'<path d="M{f(x1 + 4)} {f(top + 120)}a10 10 0 1 0 8 17a8 8 0 1 1 -8 -17Z" fill="{c["base"]}"/>')
        if STYLE["chars"]:
            hero = {"moisturise": "daily-lotion", "care": "diaper-rash-cream", "hygiene": "bottle-wash"}[cat]
            parts.append(f'<use href="#{p}ch-{hero}" x="{f(cx - 66)}" y="{f(top - 86)}" width="132" height="132"/>')
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
.fgrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.friend{display:grid;grid-template-columns:96px 1fr;gap:16px;align-items:center;background:var(--milk);border:1px solid var(--line);border-radius:var(--r);padding:16px}
.friend .face{width:96px;height:96px;border-radius:50%;display:grid;place-items:center}
.friend .face svg{width:80px;height:80px}
.friend b{font-family:var(--f-display);font-variation-settings:"SOFT" 100;font-weight:500;font-size:1.35rem;display:block}
.friend small{display:block;font-size:.75rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--moss-2)}
.friend p{font-size:.9rem;color:var(--moss-2);margin-top:4px}
.frules{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:16px}
.frules div{border-top:2px solid var(--moss);padding-top:12px;font-size:.95rem;color:var(--moss-2)}
.frules b{display:block;color:var(--moss);margin-bottom:4px}
.fnote{margin-top:18px;font-size:var(--s-1);color:var(--apricot-dp)}
@media (max-width:900px){.fgrid{grid-template-columns:1fr 1fr}.frules{grid-template-columns:1fr}}
@media (max-width:560px){.fgrid{grid-template-columns:1fr}}
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
    friend_cards = "".join(
        f'<div class="friend"><div class="face" style="background:{CATS[BY_SLUG[sl]["category"]]["wash"]}">'
        f'<svg viewBox="0 0 60 60"><use href="#{p}ch-{sl}"/></svg></div><div><small>{esc(animal)} · '
        f'{esc(" ".join(BY_SLUG[sl]["name"]))}</small><b>{esc(name)}</b><p>{esc(why)}</p></div></div>'
        for sl, (name, animal, why, _) in CHARACTERS.items())
    return f"""<!-- BEGIN:packaging -->
<!-- Generated by scripts/build_packaging.py from docs/product/products.json. Edit those, not this block. -->
{FRAGMENT_CSS}
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{defs(p)}</defs></svg>

<section class="lineup-band" id="line">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">The line</span>
      <h2>Nine products, three colours, one family</h2>
      <p class="lede">Every pack is matte milk-white with the wordmark in the same place, and each one has its own baby animal. Only the cap, the category text and the animal change, so the line looks calm on a shelf and each product is easy to find, and easy to ask for.</p>
    </div>
    <div class="lineup-scroll">
      <svg viewBox="-40 {lineup_top()} {f(width + 80)} {58 - lineup_top()}" role="img" aria-label="The Nanhe line-up: nine packs in three category groups">{lu}</svg>
    </div>
    <div class="lineup-notes">
      <div style="--c:{CATS['moisturise']['base']}"><b>Moisturise</b>Lotion in a 200 ml pump, massage oil in a clear bottle that shows the oil, and a rich cream in a 100 g jar.</div>
      <div style="--c:{CATS['care']['base']}"><b>Care &amp; Protect</b>Rash cream and sunscreen in 50 g tubes that stand on their caps, and a 25 g balm tin for the changing bag.</div>
      <div style="--c:{CATS['hygiene']['base']}"><b>Everyday Hygiene</b>Talc-free powder in a sifter shaker, bottle wash in a 300 ml foam pump, and 72 wipes in a soft pack with a rigid lid.</div>
    </div>
  </div>
</section>


<section id="friends">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Little friends</span>
      <h2>Nine Indian baby animals, one on every pack</h2>
      <p class="lede">Each product has a character, and each character is there for a reason. They sit where the ingredient drawing would be, on the wipes lid, and on top of the category arches. Their Hindi pet names give parents and children a way to ask for "the Haathi one".</p>
    </div>
    <div class="fgrid">{friend_cards}</div>
    <div class="frules">
      <div><b>How they're drawn</b>Head and shoulders, facing forward (Susu swims side-on). A moss outline at a constant weight, filled with the category colour and its wash. Dot eyes with a white glint, and blush on the cheeks.</div>
      <div><b>Where they go</b>On front labels, the wipes lid, gift boxes, social media, stickers and the website. Never inside the clinical seal, and never in place of the wordmark.</div>
      <div><b>What they never do</b>Speak, hold products, or appear in claims or safety text. The characters are there for warmth. The proof stays on the back label.</div>
    </div>
    <p class="fnote">These drawings are concept art. An illustrator redraws the set in this style before print.</p>
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
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-40 {lineup_top()} {f(width + 80)} {58 - lineup_top()}" role="img" aria-label="Nanhe line-up">'
        f'<title>Nanhe line-up</title><style><![CDATA[{FONT_IMPORT}]]></style>'
        f'<rect x="-40" y="{lineup_top()}" width="{f(width + 80)}" height="{58 - lineup_top()}" fill="{MILK}"/>'
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


# ---------------------------------------------------------------- baby directions comparison page

def styled(chars, motif, fn):
    old = dict(STYLE)
    STYLE.update(chars=chars, motif=motif)
    try:
        return fn()
    finally:
        STYLE.update(old)


def pack_figure(slug, p):
    pr = BY_SLUG[slug]
    pk = render(pr, p)
    return (f'<div class="stage" style="background:{CATS[pr["category"]]["wash"]}">'
            f'<svg viewBox="{viewbox(pk)}" role="img" aria-label="{esc(" ".join(pr["name"]))}">{pk["svg"]}</svg></div>')


def lineup_svg(p, top):
    lu, width = lineup(p)
    return (f'<div class="lineup"><svg viewBox="-60 {top} {f(width + 120)} {f(-top + 60)}" role="img" '
            f'aria-label="Line-up">{lu}</svg></div>')


DIR_CSS = """
:root{color-scheme:light;--milk:#FBF7F0;--paper:#F2ECE1;--moss:#1F3A2B;--moss-2:#55695C;--line:rgba(31,58,43,.14);
--apricot:#F6BE9A;--apricot-dp:#B4592C;--sage-dp:#43703C;--sky-dp:#2F6689;--marigold:#EFA43A;--alert:#B3412E;
--f-display:"Fraunces",Georgia,serif;--f-body:"Figtree","Avenir Next","Segoe UI",system-ui,sans-serif;
--f-deva:"Baloo 2","Kohinoor Devanagari",sans-serif;--r:22px}
*{box-sizing:border-box}
body{background:var(--milk);color:var(--moss);font-family:var(--f-body);line-height:1.55;-webkit-font-smoothing:antialiased}
.wrap{max-width:1180px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
h1,h2,h3{font-family:var(--f-display);font-variation-settings:"SOFT" 100;font-weight:500;line-height:1.08;margin:0;text-wrap:balance}
h1{font-size:clamp(2.4rem,6vw,4.2rem)}h2{font-size:clamp(2rem,4.5vw,3.1rem)}h3{font-size:1.35rem}
p{margin:0}
.eyebrow{font-size:.8rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--moss-2)}
.lede{font-size:1.15rem;color:var(--moss-2);max-width:62ch}
header{padding-block:56px 32px}
header .wrap{display:grid;gap:16px}
section{padding-block:56px}
.band{background:var(--paper)}
.head{display:grid;gap:12px;margin-bottom:28px;max-width:780px}
.tag{display:inline-flex;align-items:center;gap:10px}
.tag b{display:grid;place-items:center;width:34px;height:34px;border-radius:50%;background:var(--moss);color:var(--milk);font-family:var(--f-body);font-size:.95rem}
.four{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
.four figure{margin:0;display:grid;gap:10px}
.four figcaption{display:grid;gap:2px}
.four figcaption b{font-family:var(--f-display);font-variation-settings:"SOFT" 100;font-weight:500;font-size:1.15rem}
.four figcaption span{font-size:.88rem;color:var(--moss-2)}
.stage{border-radius:var(--r);aspect-ratio:3/4;display:grid;place-items:center;padding:14px;max-width:100%}
.stage svg{width:100%;height:100%}
.lineup{overflow-x:auto;border-radius:var(--r);background:var(--milk);border:1px solid var(--line);padding:18px 8px 8px}
.lineup svg{width:100%;min-width:760px;height:auto;display:block}
.trio{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:14px}
.chars{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:14px}
.char{display:grid;grid-template-columns:96px 1fr;gap:16px;align-items:center;background:var(--milk);border:1px solid var(--line);border-radius:var(--r);padding:16px}
.char .face{width:96px;height:96px;border-radius:50%;display:grid;place-items:center}
.char .face svg{width:80px;height:80px}
.char b{font-family:var(--f-display);font-variation-settings:"SOFT" 100;font-weight:500;font-size:1.3rem;display:block}
.char small{display:block;font-size:.78rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--moss-2)}
.char p{font-size:.9rem;color:var(--moss-2);margin-top:4px}
.swatches{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:14px}
.swatch{border-radius:var(--r);overflow:hidden;border:1px solid var(--line);background:var(--milk)}
.swatch svg{display:block;width:100%;height:150px}
.swatch p{padding:12px 16px;font-weight:600}
.pc{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:20px}
.pc div{border-radius:var(--r);padding:18px 20px;background:var(--milk);border:1px solid var(--line)}
.pc h3{font-family:var(--f-body);font-size:.8rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;margin-bottom:8px}
.pc ul{margin:0;padding-left:18px;display:grid;gap:6px;color:var(--moss-2)}
.good h3{color:var(--sage-dp)}.watch h3{color:var(--alert)}
.rec{background:var(--moss);color:var(--milk);border-radius:28px;padding:clamp(24px,5vw,44px);display:grid;gap:14px}
.rec .eyebrow{color:#C9D6CC}.rec p{color:#DCE5DE;max-width:70ch}
footer{padding-block:28px 48px;font-size:.85rem;color:var(--moss-2)}
@media (max-width:900px){.four{grid-template-columns:repeat(2,minmax(0,1fr))}.trio,.chars,.swatches{grid-template-columns:1fr 1fr}}
@media (max-width:560px){.trio,.chars,.swatches,.pc{grid-template-columns:1fr}.char{grid-template-columns:72px 1fr}.char .face{width:72px;height:72px}.char .face svg{width:60px;height:60px}}
"""


def directions_page():
    p = "x-"
    four = []
    for label, sub, ch, mo in (("Today", "Edition 2, as approved", False, False),
                               ("A · Little friends", "A baby animal on every pack", True, False),
                               ("B · Night nursery", "Moons, stars, clouds and rainbows", False, True),
                               ("A + B together", "For reference only", True, True)):
        four.append(f'<figure>{styled(ch, mo, lambda: pack_figure("daily-lotion", p))}'
                    f'<figcaption><b>{esc(label)}</b><span>{esc(sub)}</span></figcaption></figure>')
    trio_slugs = ("diaper-rash-cream", "water-wipes", "rich-cream")
    trio_a = styled(True, False, lambda: "".join(pack_figure(sl, p) for sl in trio_slugs))
    trio_b = styled(False, True, lambda: "".join(pack_figure(sl, p) for sl in trio_slugs))
    lu_a = styled(True, False, lambda: lineup_svg(p, -470))
    lu_b = styled(False, True, lambda: lineup_svg(p, -400))
    chars = []
    for slug, (name, animal, why, _) in CHARACTERS.items():
        pr = BY_SLUG[slug]
        c = CATS[pr["category"]]
        chars.append(f'<div class="char"><div class="face" style="background:{c["wash"]}"><svg viewBox="0 0 60 60">'
                     f'<use href="#{p}ch-{slug}"/></svg></div><div><small>{esc(animal)} · {esc(" ".join(pr["name"]))}</small>'
                     f'<b>{esc(name)}</b><p>{esc(why)}</p></div></div>')
    swatches = "".join(
        f'<div class="swatch"><svg viewBox="0 0 300 150" preserveAspectRatio="xMidYMid slice"><rect width="300" height="150" fill="{PACK}"/>'
        f'<rect width="300" height="150" fill="url(#{p}pat-{k})"/></svg><p style="color:{c["deep"]}">{esc(c["name"])} pattern</p></div>'
        for k, c in CATS.items())
    page = f"""<title>Nanhe Baby Directions</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600&family=Figtree:wght@400;500;600;700&family=Fraunces:opsz,wght,SOFT@9..144,400..600,100&display=swap">
<!-- Generated by scripts/build_packaging.py. Edit the script, not this file. -->
<style>{DIR_CSS}</style>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{defs(p)}</defs></svg>

<header><div class="wrap">
  <span class="eyebrow">Nanhe · design exploration · Nov 2026</span>
  <h1>Two ways to make Nanhe feel more baby</h1>
  <p class="lede">The logo, colours and type stay as they are. Only the packs and page graphics change. Below is the same bottle four ways, then each direction applied to the full line.</p>
</div></header>

<section><div class="wrap">
  <div class="four">{''.join(four)}</div>
</div></section>

<section class="band"><div class="wrap">
  <div class="head"><span class="tag"><b>A</b><span class="eyebrow">Little friends</span></span>
    <h2>A baby animal on every pack</h2>
    <p class="lede">Nine Indian animals, one per product, each chosen for a reason. The character replaces the ingredient drawing on the label, sits on the wipes lid, and peeks over the category arches. Each one has a Hindi pet name that parents and children can use.</p></div>
  {lu_a}
  <div class="chars">{''.join(chars)}</div>
  <div class="trio">{trio_a}</div>
  <div class="pc">
    <div class="good"><h3>What it does well</h3><ul><li>Gives the brand something no competitor has. "The elephant one" is easy to remember and ask for.</li><li>The Indian animals and Hindi names, Susu the river dolphin especially, make the brand clearly local without looking old-fashioned.</li><li>Characters carry over easily to social media, stickers, bath toys and a mascot.</li></ul></div>
    <div class="watch"><h3>Watch out for</h3><ul><li>The packs read younger, closer to a children's brand than a clinical one. The seal and back label have to do more of the trust work.</li><li>These drawings show the idea. For print, an illustrator should redraw them in this style.</li><li>Each new product needs a new animal, which takes more work to keep consistent.</li></ul></div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="head"><span class="tag"><b>B</b><span class="eyebrow">Night nursery</span></span>
    <h2>Moons, stars, clouds and rainbows</h2>
    <p class="lede">A soft repeating pattern in the category colour covers each pack. The label sits on a cloud-topped panel, and the category arches become rainbows. It feels like a nursery wall, without characters.</p></div>
  {lu_b}
  <div class="swatches">{swatches}</div>
  <div class="trio">{trio_b}</div>
  <div class="pc">
    <div class="good"><h3>What it does well</h3><ul><li>Calm and soft, and it still looks premium and clinical.</li><li>Extends to any new product with no new artwork. The pattern does the work.</li><li>The pattern works well on tissue paper, gift boxes and the website.</li></ul></div>
    <div class="watch"><h3>Watch out for</h3><ul><li>Moons, stars and rainbows are common in baby care, so this won't stand out much on a shelf.</li><li>The busy background competes with the label, which is why the label needs its own cloud panel.</li></ul></div>
  </div>
</div></section>

<section class="band"><div class="wrap">
  <div class="rec">
    <span class="eyebrow">My recommendation</span>
    <h2>Go with A, Little friends</h2>
    <p>The characters are the only one of these ideas that Nanhe could own, and the nine Indian animals tie straight back to the name. Direction B is lovely but generic: it makes the packs softer without making them more recognisable. Using both at once makes the packs look busy, as the fourth bottle at the top shows.</p>
    <p>If A feels too young, a middle path is to keep today's clean packs and use the characters only on the wipes lid, the gift box, social media and the website.</p>
  </div>
</div></section>

<footer><div class="wrap">Rendered from docs/product/products.json by scripts/build_packaging.py. Character drawings are concept art.</div></footer>
"""
    out = ROOT / "docs/design/explorations/baby-directions.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page)


if __name__ == "__main__":
    write_standalone()
    write_product_md()
    inject_brand_book()
    directions_page()
    print(f"Rendered {len(PRODUCTS)} packs, line-up, product sheet and brand book block.")
