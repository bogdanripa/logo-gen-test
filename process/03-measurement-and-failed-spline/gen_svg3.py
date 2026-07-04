import math

DARK_GREEN = "#344636"
GOLD = "#C3A35A"
GOLD_LIGHT = "#C9B98D"
PETAL_LIGHT = "#E3C6C8"
PETAL_DARK = "#BE8085"

SIZE = 336
C = SIZE / 2

def catmull_rom_to_bezier(points):
    """points: list of (x,y). Returns SVG path 'M ... C ...' through all points."""
    pts = [points[0]] + points + [points[-1]]
    d = f"M {pts[1][0]:.2f},{pts[1][1]:.2f} "
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i-1], pts[i], pts[i+1], pts[i+2]
        c1 = (p1[0] + (p2[0]-p0[0])/6.0, p1[1] + (p2[1]-p0[1])/6.0)
        c2 = (p2[0] - (p3[0]-p1[0])/6.0, p2[1] - (p3[1]-p1[1])/6.0)
        d += f"C {c1[0]:.2f},{c1[1]:.2f} {c2[0]:.2f},{c2[1]:.2f} {p2[0]:.2f},{p2[1]:.2f} "
    return d

def petal_path(profile, base_r):
    """profile: list of (r, half_width) measured from real logo, r increasing to tip (width 0)."""
    right = [(hw, -r) for r, hw in profile]
    left = [(-hw, -r) for r, hw in reversed(profile)]
    base = (0, -base_r)
    pts = [base] + right + left[1:]
    # close back to base
    d = catmull_rom_to_bezier(pts)
    d += f"L {base[0]:.2f},{base[1]:.2f} Z"
    return d

def petal_group(path_d, color, angles):
    parts = []
    for a in angles:
        parts.append(f'<path d="{path_d}" fill="{color}" transform="rotate({a})"/>')
    return "\n      ".join(parts)

light_angles = [0, 60, 120, 180, 240, 300]
dark_angles = [30, 90, 150, 210, 270, 330]

dark_profile = [
    (15, 12), (30, 20.9), (40, 27.9), (50, 34.9), (60, 27.2),
    (70, 24.6), (80, 19.1), (85, 14.8), (88, 10.0), (90, 0),
]
light_profile = [
    (15, 6), (60, 2.2), (70, 9.7), (80, 19.8), (90, 35.8),
    (100, 30.7), (110, 26.4), (120, 18.2), (130, 13.0), (136, 7.2), (138, 0),
]

dark_path = petal_path(dark_profile, base_r=0)
light_path = petal_path(light_profile, base_r=0)

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
      <circle r="18" fill="none" stroke="{GOLD}" stroke-width="7"/>
      <circle r="8.5" fill="{DARK_GREEN}"/>
    </g>
  </g>
</svg>
'''

out = "/tmp/claude-0/-home-user-logo-gen-test/66515361-52e5-52b5-a0b3-4f402867e455/scratchpad/logo/logo3.svg"
with open(out, "w") as f:
    f.write(svg)
print("written", out)
print(dark_path)
print(light_path)
