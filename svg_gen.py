#!/usr/bin/env python3
"""SVG image generator — vector graphics without libraries."""
import sys, math, random

class SVG:
    def __init__(self, w=200, h=200):
        self.w, self.h = w, h
        self.elements = []
    def rect(self, x, y, w, h, fill='black', **kw):
        self.elements.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>')
    def circle(self, cx, cy, r, fill='black', **kw):
        self.elements.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>')
    def line(self, x1, y1, x2, y2, stroke='black', width=1):
        self.elements.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{width}"/>')
    def text(self, x, y, txt, size=16, fill='black'):
        self.elements.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}">{txt}</text>')
    def polygon(self, points, fill='black'):
        pts = ' '.join(f'{x},{y}' for x,y in points)
        self.elements.append(f'<polygon points="{pts}" fill="{fill}"/>')
    def render(self):
        body = '\n  '.join(self.elements)
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}">\n  {body}\n</svg>'

def demo_circles(n=20):
    s = SVG(400, 400)
    for _ in range(n):
        s.circle(random.randint(20,380), random.randint(20,380), random.randint(5,40),
                 f'rgba({random.randint(0,255)},{random.randint(0,255)},{random.randint(0,255)},0.5)')
    return s

def demo_spiral():
    s = SVG(400, 400)
    for i in range(200):
        a = i * 0.1; r = i * 0.8
        x, y = 200 + r*math.cos(a), 200 + r*math.sin(a)
        hue = i * 1.8
        s.circle(x, y, 3, f'hsl({hue},80%,50%)')
    return s

def demo_grid():
    s = SVG(400, 400)
    for x in range(0, 400, 20):
        for y in range(0, 400, 20):
            c = f'hsl({(x+y)%360},70%,50%)'
            s.rect(x, y, 18, 18, c)
    return s

DEMOS = {'circles': demo_circles, 'spiral': demo_spiral, 'grid': demo_grid}

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('demo', choices=list(DEMOS.keys()), default='spiral', nargs='?')
    p.add_argument('-o', '--output', default='output.svg')
    p.add_argument('-s', '--seed', type=int, default=42)
    args = p.parse_args()
    random.seed(args.seed)
    svg = DEMOS[args.demo]()
    open(args.output, 'w').write(svg.render())
    print(f"Wrote {args.output}")
