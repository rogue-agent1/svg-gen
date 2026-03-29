from svg_gen import SVG, bar_chart
s = SVG(100, 100)
s.rect(0, 0, 100, 100, fill="white")
s.circle(50, 50, 25, fill="red")
r = s.render()
assert "<svg" in r and "<circle" in r and "<rect" in r
bc = bar_chart([10, 20, 30])
assert "<rect" in bc.render()
print("SVG tests passed")