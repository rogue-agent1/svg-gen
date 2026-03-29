#!/usr/bin/env python3
"""SVG generator. Zero dependencies."""
import sys, math

class SVG:
    def __init__(self, width=400, height=300):
        self.width, self.height = width, height
        self.elements = []

    def rect(self, x, y, w, h, fill="black", stroke="none", stroke_width=1):
        self.elements.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>')
        return self

    def circle(self, cx, cy, r, fill="black", stroke="none"):
        self.elements.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}"/>')
        return self

    def line(self, x1, y1, x2, y2, stroke="black", stroke_width=1):
        self.elements.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{stroke_width}"/>')
        return self

    def text(self, x, y, content, font_size=16, fill="black", anchor="start"):
        self.elements.append(f'<text x="{x}" y="{y}" font-size="{font_size}" fill="{fill}" text-anchor="{anchor}">{content}</text>')
        return self

    def polygon(self, points, fill="black", stroke="none"):
        pts = " ".join(f"{x},{y}" for x,y in points)
        self.elements.append(f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}"/>')
        return self

    def path(self, d, fill="none", stroke="black", stroke_width=1):
        self.elements.append(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>')
        return self

    def group(self, transform=""):
        return SVGGroup(self, transform)

    def render(self):
        header = f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}">'
        return header + "\n".join(self.elements) + "</svg>"

    def save(self, path):
        with open(path, "w") as f:
            f.write(self.render())

class SVGGroup:
    def __init__(self, svg, transform):
        self.svg = svg
        self.svg.elements.append(f'<g transform="{transform}">' if transform else "<g>")
    def __enter__(self): return self.svg
    def __exit__(self, *a): self.svg.elements.append("</g>")

def bar_chart(data, labels=None, width=400, height=300, colors=None):
    svg = SVG(width, height)
    n = len(data); mx = max(data) if data else 1
    bar_w = (width - 60) / n; margin = 40
    for i, v in enumerate(data):
        h = (v / mx) * (height - 60)
        color = colors[i % len(colors)] if colors else f"hsl({i*360//n}, 70%, 50%)"
        svg.rect(margin + i*bar_w + 2, height - 20 - h, bar_w - 4, h, fill=color)
        if labels and i < len(labels):
            svg.text(margin + i*bar_w + bar_w/2, height - 5, labels[i], font_size=10, anchor="middle")
    return svg

if __name__ == "__main__":
    svg = bar_chart([30, 50, 80, 45, 60], ["A","B","C","D","E"])
    svg.save("chart.svg")
    print("Wrote chart.svg")
