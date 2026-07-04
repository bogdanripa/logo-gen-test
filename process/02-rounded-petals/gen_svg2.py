import math

DARK_GREEN = "#344636"
GOLD = "#C3A35A"
GOLD_LIGHT = "#C9B98D"
PETAL_LIGHT = "#E3C6C8"
PETAL_DARK = "#BE8085"

SIZE = 336
C = SIZE / 2

def petal_path(L, w, f):
    """Petal from base (0,0) to tip (0,-L), with max half-width w at fraction f of L."""
    py = -L * f
    return (
        f"M 0,0 "
        f"C {-w*0.55:.2f},0 {-w:.2f},{py*0.55:.2f} {-w:.2f},{py:.2f} "
        f"C {-w:.2f},{(py + (-L - py) * 0.55):.2f} {-w*0.35:.2f},{-L:.2f} 0,{-L:.2f} "
        f"C {w*0.35:.2f},{-L:.2f} {w:.2f},{(py + (-L - py) * 0.55):.2f} {w:.2f},{py:.2f} "
        f"C {w:.2f},{py*0.55:.2f} {w*0.55:.2f},0 0,0 "
        f"Z"
    )

def petal_group(path_d, color, angles):
    parts = []
    for a in angles:
        parts.append(f'<path d="{path_d}" fill="{color}" transform="rotate({a})"/>')
    return "\n      ".join(parts)

light_angles = [0, 60, 120, 180, 240, 300]
dark_angles = [30, 90, 150, 210, 270, 330]

dark_path = petal_path(L=90, w=35, f=0.55)
light_path = petal_path(L=138, w=36, f=0.65)

def leaf_path(length, half_width):
    return (
        f"M {-length/2:.2f},0 "
        f"C {-length*0.2:.2f},{-half_width:.2f} {length*0.2:.2f},{-half_width:.2f} {length/2:.2f},0 "
        f"C {length*0.2:.2f},{half_width:.2f} {-length*0.2:.2f},{half_width:.2f} {-length/2:.2f},0 Z"
    )

leaf_len = 80
leaf_half_w = 8
leaf_d = leaf_path(leaf_len, leaf_half_w)

outer_r = 156
leaf_angle_deg = 128
leaf_placement_r = 156
def point_on_circle(r, angle_deg):
    a = math.radians(angle_deg)
    return (r * math.sin(a), -r * math.cos(a))

lx, ly = point_on_circle(leaf_placement_r, -leaf_angle_deg)
rx_, ry_ = point_on_circle(leaf_placement_r, leaf_angle_deg)
leaf_tilt = 12

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SIZE} {SIZE}">
  <g transform="translate({C},{C})">
    <g transform="translate({lx:.2f},{ly:.2f}) rotate({-leaf_tilt})">
      <path d="{leaf_d}" fill="{DARK_GREEN}"/>
    </g>
    <g transform="translate({rx_:.2f},{ry_:.2f}) rotate({leaf_tilt})">
      <path d="{leaf_d}" fill="{DARK_GREEN}"/>
    </g>
    <circle r="{outer_r}" fill="none" stroke="{DARK_GREEN}" stroke-width="3"/>
    <circle r="143" fill="none" stroke="{GOLD_LIGHT}" stroke-width="1.5"/>
    <g id="flower">
      {petal_group(light_path, PETAL_LIGHT, light_angles)}
      {petal_group(dark_path, PETAL_DARK, dark_angles)}
      <circle r="21.5" fill="none" stroke="{GOLD}" stroke-width="9"/>
      <circle r="8.5" fill="{DARK_GREEN}"/>
    </g>
  </g>
</svg>
'''

out = "/tmp/claude-0/-home-user-logo-gen-test/66515361-52e5-52b5-a0b3-4f402867e455/scratchpad/logo/logo2.svg"
with open(out, "w") as f:
    f.write(svg)
print("written", out)
