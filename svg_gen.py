#!/usr/bin/env python3
"""SVG generator."""

class SVG:
    def __init__(self, width=200, height=200):
        self.width = width
        self.height = height
        self.elements = []

    def rect(self, x, y, w, h, fill="black", stroke=None, rx=0):
        attrs = f'x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"'
        if stroke: attrs += f' stroke="{stroke}"'
        if rx: attrs += f' rx="{rx}"'
        self.elements.append(f"<rect {attrs}/>")
        return self

    def circle(self, cx, cy, r, fill="black", stroke=None):
        attrs = f'cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"'
        if stroke: attrs += f' stroke="{stroke}"'
        self.elements.append(f"<circle {attrs}/>")
        return self

    def line(self, x1, y1, x2, y2, stroke="black", width=1):
        self.elements.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{width}"/>')
        return self

    def text(self, x, y, content, size=16, fill="black", anchor="start"):
        self.elements.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}">{content}</text>')
        return self

    def path(self, d, fill="none", stroke="black", width=1):
        self.elements.append(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')
        return self

    def render(self) -> str:
        header = f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}">'
        body = "\n  ".join(self.elements)
        return f"{header}\n  {body}\n</svg>"

    def save(self, path):
        with open(path, "w") as f:
            f.write(self.render())

if __name__ == "__main__":
    svg = SVG(200, 200)
    svg.rect(10, 10, 80, 80, fill="blue")
    svg.circle(150, 50, 40, fill="red")
    svg.text(100, 150, "Hello SVG", size=20)
    print(svg.render())

def test():
    s = SVG(100, 100)
    s.rect(0, 0, 50, 50, fill="red")
    s.circle(75, 75, 20, fill="blue")
    s.line(0, 0, 100, 100)
    s.text(50, 50, "Hi")
    s.path("M 10 10 L 90 90")
    xml = s.render()
    assert "<svg" in xml and "</svg>" in xml
    assert "<rect" in xml
    assert "<circle" in xml
    assert "<line" in xml
    assert "<text" in xml and "Hi" in xml
    assert "<path" in xml
    assert 'width="100"' in xml
    print("  svg_gen: ALL TESTS PASSED")
