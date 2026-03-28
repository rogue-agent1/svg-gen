#!/usr/bin/env python3
"""svg_gen - Programmatic SVG generation."""
import argparse, sys, math

class SVG:
    def __init__(self, w=400, h=400):
        self.w, self.h, self.elems = w, h, []
    def rect(self, x, y, w, h, fill="black", stroke="none"):
        self.elems.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}"/>')
    def circle(self, cx, cy, r, fill="black"):
        self.elems.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>')
    def line(self, x1, y1, x2, y2, stroke="black", width=1):
        self.elems.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{width}"/>')
    def text(self, x, y, txt, size=16, fill="black"):
        self.elems.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}">{txt}</text>')
    def polygon(self, points, fill="black"):
        pts = " ".join(f"{x},{y}" for x,y in points)
        self.elems.append(f'<polygon points="{pts}" fill="{fill}"/>')
    def render(self):
        lines = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}">']
        lines.extend(self.elems)
        lines.append("</svg>")
        return "\n".join(lines)

def demo_chart(output):
    s = SVG(500, 300)
    data = [40, 80, 60, 95, 50, 70, 85]
    labels = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    bw = 50; gap = 10; base = 250
    for i, v in enumerate(data):
        x = 40 + i * (bw + gap)
        h = v * 2
        s.rect(x, base - h, bw, h, fill=f"hsl({i*50},70%,50%)")
        s.text(x + 10, base + 20, labels[i], size=12)
        s.text(x + 15, base - h - 5, str(v), size=11)
    s.text(150, 30, "Weekly Stats", size=20, fill="#333")
    with open(output, "w") as f: f.write(s.render())
    print(f"Wrote {output}")

def demo_shapes(output):
    s = SVG(400, 400)
    for i in range(6):
        a = i * math.pi / 3
        cx, cy = 200 + 100*math.cos(a), 200 + 100*math.sin(a)
        s.circle(cx, cy, 30, fill=f"hsl({i*60},80%,60%)")
    s.circle(200, 200, 40, fill="#333")
    with open(output, "w") as f: f.write(s.render())
    print(f"Wrote {output}")

def main():
    p = argparse.ArgumentParser(description="Generate SVG graphics")
    p.add_argument("demo", choices=["chart","shapes"], help="Demo to generate")
    p.add_argument("-o","--output", default="out.svg")
    a = p.parse_args()
    {"chart": demo_chart, "shapes": demo_shapes}[a.demo](a.output)

if __name__ == "__main__": main()
