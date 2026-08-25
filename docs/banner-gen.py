#!/usr/bin/env python3
"""Regenerate docs/banner.svg.

The sketchy strokes are seeded (random.seed below), so re-running this
reproduces the committed SVG byte for byte. Change the seed for a different
hand. No dependencies beyond the standard library.

    python3 docs/banner-gen.py
"""
import math, os, random

W, H = 1280, 300
random.seed(7)

def jitter(a): return random.uniform(-a, a)

def rough_line(x1, y1, x2, y2, r=1.6, passes=2):
    """Bezier with control points displaced perpendicular to the line."""
    out = []
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1
    px, py = -dy / L, dx / L          # perpendicular unit
    for p in range(passes):
        sx, sy = x1 + jitter(r*.7), y1 + jitter(r*.7)
        ex, ey = x2 + jitter(r*.7), y2 + jitter(r*.7)
        b1, b2 = jitter(r*2.2), jitter(r*2.2)
        c1x, c1y = x1 + dx*.35 + px*b1, y1 + dy*.35 + py*b1
        c2x, c2y = x1 + dx*.70 + px*b2, y1 + dy*.70 + py*b2
        out.append(f'M{sx:.1f} {sy:.1f}C{c1x:.1f} {c1y:.1f} {c2x:.1f} {c2y:.1f} {ex:.1f} {ey:.1f}')
    return out

def rough_rect(x, y, w, h, r=1.6):
    segs = []
    for a, b, c, d in [(x,y,x+w,y), (x+w,y,x+w,y+h), (x+w,y+h,x,y+h), (x,y+h,x,y)]:
        segs += rough_line(a, b, c, d, r)
    return segs

INK = '#2B2620'
parts = []

# ---------- backdrop: cream -> light grey, no hard seam ----------
parts.append(f'''<defs>
<linearGradient id="paper" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0%"  stop-color="#F7F2E7"/>
  <stop offset="38%" stop-color="#F6F1E6"/>
  <stop offset="62%" stop-color="#F3F2F1"/>
  <stop offset="100%" stop-color="#EFEEED"/>
</linearGradient>
<linearGradient id="glass" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0%" stop-color="#ffffff" stop-opacity=".95"/>
  <stop offset="100%" stop-color="#ffffff" stop-opacity=".55"/>
</linearGradient>
</defs>''')
parts.append(f'<rect width="{W}" height="{H}" fill="url(#paper)"/>')

# ---------- brand swoosh, bottom-right, anchored off-canvas ----------
sw = [('#FFB900', 0, .62), ('#F25022', 30, .62), ('#7FBA00', 60, .58), ('#00A4EF', 90, .66)]
for col, off, op in sw:
    parts.append(
        f'<path d="M{W-196+off} {H} L{W-84+off} {H-118} '
        f'L{W-56+off} {H-118} L{W-168+off} {H}Z" fill="{col}" opacity="{op}"/>')

# ---------- the row of shapes crossing the seam ----------
CY = 150
BW, BH = 108, 74
xs = [96, 300, 504, 708, 912]

for i, x in enumerate(xs):
    t = i / (len(xs) - 1)                     # 0 = sketch, 1 = clean
    y = CY - BH/2
    if i < len(xs) - 1:                       # connector to the next box
        ax1, ax2 = x + BW + 14, xs[i+1] - 14
        if t < .55:
            for d in rough_line(ax1, CY, ax2, CY, 1.5):
                parts.append(f'<path d="{d}" stroke="{INK}" stroke-width="2" fill="none" '
                             f'stroke-linecap="round" opacity=".85"/>')
            for d in rough_line(ax2, CY, ax2-11, CY-6, 1.1) + rough_line(ax2, CY, ax2-11, CY+6, 1.1):
                parts.append(f'<path d="{d}" stroke="{INK}" stroke-width="2" fill="none" '
                             f'stroke-linecap="round" opacity=".85"/>')
        else:
            parts.append(f'<path d="M{ax1} {CY}H{ax2}" stroke="#605E5C" stroke-width="2.4" '
                         f'stroke-linecap="round" opacity=".8"/>')
            parts.append(f'<path d="M{ax2-11} {CY-7}L{ax2} {CY}L{ax2-11} {CY+7}" stroke="#605E5C" '
                         f'stroke-width="2" fill="none" stroke-linecap="round" '
                         f'stroke-linejoin="round" opacity=".8"/>')

    if t < .35:                               # pure hand-drawn
        for d in rough_rect(x, y, BW, BH, 1.9):
            parts.append(f'<path d="{d}" stroke="{INK}" stroke-width="2.4" fill="none" '
                         f'stroke-linecap="round" opacity=".9"/>')
    elif t < .65:                             # mid: sketchy outline + faint fill
        parts.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="7" '
                     f'fill="#ffffff" opacity=".5"/>')
        for d in rough_rect(x, y, BW, BH, 1.2):
            parts.append(f'<path d="{d}" stroke="{INK}" stroke-width="2" fill="none" '
                         f'stroke-linecap="round" opacity=".6"/>')
        for dy, wf in ((18, .45), (34, .72), (47, .58)):
            for d in rough_line(x+14, y+dy, x+14+(BW-28)*wf, y+dy, .9, passes=1):
                parts.append(f'<path d="{d}" stroke="{INK}" stroke-width="3" fill="none" '
                             f'stroke-linecap="round" opacity=".28"/>')
    else:                                     # clean glass card
        accent = '#00A4EF' if t < .9 else '#7FBA00'
        parts.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="9" '
                     f'fill="url(#glass)" stroke="{accent}" stroke-width="1.6" opacity=".92"/>')
        parts.append(f'<rect x="{x+14}" y="{y+18}" width="{BW-52}" height="6" rx="3" '
                     f'fill="{accent}" opacity=".5"/>')
        parts.append(f'<rect x="{x+14}" y="{y+34}" width="{BW-28}" height="5" rx="2.5" '
                     f'fill="#8A8886" opacity=".3"/>')
        parts.append(f'<rect x="{x+14}" y="{y+47}" width="{BW-44}" height="5" rx="2.5" '
                     f'fill="#8A8886" opacity=".3"/>')

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
       f'height="{H}" role="img" aria-label="Slidev Skill Microsoft Style — hand-drawn '
       f'sketch diagrams transitioning into Fluent-style glass cards">\n'
       + '\n'.join(parts) + '\n</svg>\n')
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'banner.svg')
with open(out, 'w') as fh:
    fh.write(svg)
print(f'{out} — {len(svg)} bytes')
