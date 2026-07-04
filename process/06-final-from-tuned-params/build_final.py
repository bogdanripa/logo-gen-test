import math

p = {
  "cx": 203.5, "cy": 180.5,
  "outerR": 156, "outerStroke": 3, "outerColor": "#344636",
  "innerR": 143, "innerStroke": 1.5, "innerColor": "#c9b98d",
  "goldR": 21.5, "goldStroke": 9, "goldColor": "#c3a35a",
  "dotR": 8.5, "dotColor": "#344636",
  "lightCount": 6, "lightAngleOffset": 0, "lightDist": 78, "lightRx": 32, "lightRy": 62, "lightRot": 0, "lightColor": "#e3c6c8",
  "darkCount": 6, "darkAngleOffset": 30, "darkDist": 46, "darkRx": 29, "darkRy": 46, "darkRot": 0, "darkColor": "#be8085",
  "leafAngle": 120, "leafDist": 135, "leafRx": 38, "leafRy": 14, "leafTilt": 4, "leafColor": "#344636",
}

# Bounding box: circle + stroke, and leaves (approximate leaf extent conservatively as a circle of radius leafRx around its center)
def leaf_center(angle_sign):
    a = math.radians(p["leafAngle"] * angle_sign)
    x = p["leafDist"] * math.sin(a) * (1 if angle_sign > 0 else -1)
    # match editor's leafPt: (r*sin(a), -r*cos(a)) with angle passed as -leafAngle / +leafAngle
    return x

def leaf_pt(r, angle_deg):
    a = math.radians(angle_deg)
    return (r * math.sin(a), -r * math.cos(a))

lx, ly = leaf_pt(p["leafDist"], -p["leafAngle"])
rx2, ry2 = leaf_pt(p["leafDist"], p["leafAngle"])

margin = p["outerStroke"]/2 + 4
half = p["outerR"] + margin
# also ensure leaves fit (they sit inside/near the circle so outer circle bbox should dominate, but check)
leaf_reach = max(
    abs(lx) + p["leafRx"], abs(rx2) + p["leafRx"],
)
half = max(half, leaf_reach + 4)

view_min_x = p["cx"] - half
view_min_y = p["cy"] - half
view_size = half * 2

def fnum(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return s if s != "-0" else "0"

def petal_ellipses(count, angle_offset, dist, rx, ry, rot, color):
    out = []
    for i in range(count):
        angle = angle_offset + (360/count)*i
        g = f' transform="rotate({fnum(angle)})"' if angle % 360 != 0 else ""
        rotg = f' transform="rotate({fnum(rot)})"' if rot != 0 else ""
        out.append(
            f'<g{g}><ellipse cx="0" cy="{fnum(-dist)}" rx="{fnum(rx)}" ry="{fnum(ry)}" '
            f'fill="{color}"{rotg}/></g>'
        )
    return "\n      ".join(out)

def leaf_path(rx, ry):
    return (
        f"M {fnum(-rx)},0 C {fnum(-rx*0.4)},{fnum(-ry)} {fnum(rx*0.4)},{fnum(-ry)} {fnum(rx)},0 "
        f"C {fnum(rx*0.4)},{fnum(ry)} {fnum(-rx*0.4)},{fnum(ry)} {fnum(-rx)},0 Z"
    )

leaf_d = leaf_path(p["leafRx"], p["leafRy"])

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{fnum(view_min_x)} {fnum(view_min_y)} {fnum(view_size)} {fnum(view_size)}" role="img" aria-labelledby="logo-title">
  <title id="logo-title">Flower logo</title>
  <g transform="translate({fnum(p['cx'])},{fnum(p['cy'])})">
    <g transform="translate({fnum(lx)},{fnum(ly)}) rotate({fnum(-p['leafTilt'])})">
      <path d="{leaf_d}" fill="{p['leafColor']}"/>
    </g>
    <g transform="translate({fnum(rx2)},{fnum(ry2)}) rotate({fnum(p['leafTilt'])})">
      <path d="{leaf_d}" fill="{p['leafColor']}"/>
    </g>
    <circle r="{p['outerR']}" fill="none" stroke="{p['outerColor']}" stroke-width="{p['outerStroke']}"/>
    <circle r="{p['innerR']}" fill="none" stroke="{p['innerColor']}" stroke-width="{p['innerStroke']}"/>
    <g id="flower">
      {petal_ellipses(p['lightCount'], p['lightAngleOffset'], p['lightDist'], p['lightRx'], p['lightRy'], p['lightRot'], p['lightColor'])}
      {petal_ellipses(p['darkCount'], p['darkAngleOffset'], p['darkDist'], p['darkRx'], p['darkRy'], p['darkRot'], p['darkColor'])}
      <circle r="{p['goldR']}" fill="none" stroke="{p['goldColor']}" stroke-width="{p['goldStroke']}"/>
      <circle r="{p['dotR']}" fill="{p['dotColor']}"/>
    </g>
  </g>
</svg>
'''

out = "/home/user/logo-gen-test/logo.svg"
with open(out, "w") as f:
    f.write(svg)
print(svg)
