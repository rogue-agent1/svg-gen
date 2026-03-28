#!/usr/bin/env python3
"""svg_gen - SVG chart generator."""
import argparse, json, math

def bar_chart(data, width=600, height=400):
    n = len(data); bar_w = width / (n * 1.5)
    max_val = max(v for _, v in data)
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">']
    colors = ["#4CAF50","#2196F3","#FF9800","#E91E63","#9C27B0","#00BCD4","#FFC107","#795548"]
    for i, (label, value) in enumerate(data):
        x = i * bar_w * 1.5 + bar_w * 0.5
        h = (value / max_val) * (height - 60)
        y = height - 40 - h
        color = colors[i % len(colors)]
        svg.append(f'<rect x="{x}" y="{y}" width="{bar_w}" height="{h}" fill="{color}"/>')
        svg.append(f'<text x="{x+bar_w/2}" y="{height-20}" text-anchor="middle" font-size="12">{label}</text>')
        svg.append(f'<text x="{x+bar_w/2}" y="{y-5}" text-anchor="middle" font-size="11">{value}</text>')
    svg.append('</svg>')
    return '\n'.join(svg)

def pie_chart(data, size=400):
    cx, cy, r = size/2, size/2, size/2-20
    total = sum(v for _, v in data)
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}">']
    colors = ["#4CAF50","#2196F3","#FF9800","#E91E63","#9C27B0","#00BCD4"]
    angle = 0
    for i, (label, value) in enumerate(data):
        sweep = value / total * 360
        a1 = math.radians(angle); a2 = math.radians(angle + sweep)
        x1, y1 = cx + r*math.cos(a1), cy + r*math.sin(a1)
        x2, y2 = cx + r*math.cos(a2), cy + r*math.sin(a2)
        large = 1 if sweep > 180 else 0
        svg.append(f'<path d="M{cx},{cy} L{x1},{y1} A{r},{r} 0 {large},1 {x2},{y2} Z" fill="{colors[i%len(colors)]}"/>')
        mid = math.radians(angle + sweep/2)
        tx, ty = cx + r*0.6*math.cos(mid), cy + r*0.6*math.sin(mid)
        svg.append(f'<text x="{tx}" y="{ty}" text-anchor="middle" font-size="11" fill="white">{label}</text>')
        angle += sweep
    svg.append('</svg>')
    return '\n'.join(svg)

def main():
    p = argparse.ArgumentParser(description="SVG chart generator")
    p.add_argument("type", choices=["bar", "pie"])
    p.add_argument("data", help="JSON array of [label, value] pairs")
    p.add_argument("-o", "--output", default="chart.svg")
    p.add_argument("-W", "--width", type=int, default=600)
    args = p.parse_args()
    data = json.loads(args.data)
    if args.type == "bar": svg = bar_chart(data, args.width)
    else: svg = pie_chart(data, args.width)
    open(args.output, 'w').write(svg)
    print(f"Generated {args.type} chart -> {args.output}")

if __name__ == "__main__":
    main()
